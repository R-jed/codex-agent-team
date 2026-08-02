#!/usr/bin/env python3
"""Deterministically reconcile expected and observed native Subagent runtime facts.

Evidence is typed by route, ancestry, and permission. Observation-object presence is
never enough to establish a matched route: agent_role, model, and effort must all be
present and agree before L1/R1/R2 can be emitted.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, NoReturn

ROUTE_FIELDS = ("agent_role", "model", "effort")
IDENTITY_FIELDS = ("thread_id", "parent_thread_id")
PERMISSION_FIELDS = ("sandbox_policy_type", "permission_profile_type")
READ_ONLY_SANDBOXES = {"read-only", "read_only", "readonly"}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconcile configured Subagent expectations with runtime evidence."
    )
    parser.add_argument("--input", type=Path, help="JSON input file; defaults to stdin.")
    return parser.parse_args()


def load_payload(path: Path | None) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8") if path else sys.stdin.read()
        payload = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid verifier input: {exc}")
    if not isinstance(payload, dict):
        fail("verifier input must be a JSON object")
    return payload


def object_or_none(value: Any, field: str) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        fail(f"{field} must be an object or null")
    return value


def string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def normalized_observation(value: dict[str, Any] | None) -> dict[str, str | None] | None:
    if value is None:
        return None
    allowed = {
        "thread_id",
        "parent_thread_id",
        "agent_role",
        "model",
        "effort",
        "sandbox_policy_type",
        "permission_profile_type",
        "runtime_version",
        "record_format_version",
    }
    return {key: string_or_none(value.get(key)) for key in allowed}


def compare_expected(
    expected: dict[str, Any],
    observed: dict[str, str | None],
    source: str,
) -> list[str]:
    violations: list[str] = []
    for field in (*IDENTITY_FIELDS, *ROUTE_FIELDS):
        wanted = string_or_none(expected.get(field))
        got = observed.get(field)
        if wanted is not None and got is not None and wanted != got:
            violations.append(f"{source}:{field}_mismatch")
    return violations


def compare_sources(
    native: dict[str, str | None],
    local: dict[str, str | None],
) -> list[str]:
    violations: list[str] = []
    for field in (*ROUTE_FIELDS, *IDENTITY_FIELDS, *PERMISSION_FIELDS):
        left = native.get(field)
        right = local.get(field)
        if left is not None and right is not None and left != right:
            violations.append(f"source_conflict:{field}")
    return violations


def observed_fields(observation: dict[str, str | None] | None, fields: tuple[str, ...]) -> list[str]:
    if observation is None:
        return []
    return [field for field in fields if observation.get(field) is not None]


def source_conflict_for(violations: list[str], fields: tuple[str, ...]) -> bool:
    return any(f"source_conflict:{field}" in violations for field in fields)


def route_complete(
    expected: dict[str, Any], observation: dict[str, str | None] | None, source: str, violations: list[str]
) -> bool:
    if observation is None:
        return False
    for field in ROUTE_FIELDS:
        if string_or_none(expected.get(field)) is not None and observation.get(field) is None:
            return False
        if f"{source}:{field}_mismatch" in violations:
            return False
    return all(observation.get(field) is not None for field in ROUTE_FIELDS)


def evidence_source(native: bool, local: bool) -> str:
    if native and local:
        return "both"
    if native:
        return "native"
    if local:
        return "local"
    return "none"


def route_evidence(
    expected: dict[str, Any],
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> tuple[dict[str, Any], bool, bool]:
    native_complete = route_complete(expected, native, "native", violations)
    local_complete = route_complete(expected, local, "local", violations)
    route_conflict = source_conflict_for(violations, ROUTE_FIELDS) or any(
        item == f"{source}:{field}_mismatch"
        for item in violations
        for source in ("native", "local")
        for field in ROUTE_FIELDS
    )
    native_seen = observed_fields(native, ROUTE_FIELDS)
    local_seen = observed_fields(local, ROUTE_FIELDS)
    seen = sorted(set(native_seen + local_seen))
    if route_conflict:
        status = "conflict"
    elif native_complete or local_complete:
        status = "matched"
    elif seen:
        status = "partial"
    else:
        status = "not_observed"
    return (
        {
            "status": status,
            "source": evidence_source(native_complete, local_complete),
            "observed_fields": seen,
            "native_observed_fields": native_seen,
            "local_observed_fields": local_seen,
        },
        native_complete,
        local_complete,
    )


def ancestry_evidence(
    expected: dict[str, Any],
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> dict[str, Any]:
    wanted = string_or_none(expected.get("parent_thread_id"))
    if wanted is None:
        return {"status": "not_required", "source": "none"}
    native_has = native is not None and native.get("parent_thread_id") is not None
    local_has = local is not None and local.get("parent_thread_id") is not None
    if any("parent_thread_id_mismatch" in item for item in violations):
        return {"status": "conflict", "source": evidence_source(native_has, local_has)}
    if not native_has and not local_has:
        return {"status": "not_observed", "source": "none"}
    return {"status": "matched", "source": evidence_source(native_has, local_has)}


def permission_evidence(
    expected: dict[str, Any],
    native: dict[str, str | None] | None,
) -> dict[str, Any]:
    if not bool(expected.get("requires_enforced_read_only", False)):
        return {"status": "not_required", "source": "none"}
    if native is None or native.get("sandbox_policy_type") is None:
        return {"status": "not_observed", "source": "none"}
    sandbox = native["sandbox_policy_type"]
    if sandbox is not None and sandbox.lower() in READ_ONLY_SANDBOXES:
        return {"status": "matched", "source": "native"}
    return {"status": "broader_than_required", "source": "native"}


def compact_grade(
    route: dict[str, Any], native_complete: bool, local_complete: bool, conflicts: bool
) -> str:
    if conflicts:
        return "X0_conflicted"
    if native_complete and local_complete:
        return "R2_runtime_reported_and_local_record_agree"
    if native_complete:
        return "R1_runtime_reported"
    if local_complete:
        return "L1_local_record_observed"
    return "C1_configuration_only"


def main() -> None:
    args = parse_args()
    payload = load_payload(args.input)
    expected = object_or_none(payload.get("expected"), "expected")
    if expected is None:
        fail("expected is required")
    native = normalized_observation(object_or_none(payload.get("native"), "native"))
    local = normalized_observation(object_or_none(payload.get("local"), "local"))

    violations: list[str] = []
    if native is not None:
        violations.extend(compare_expected(expected, native, "native"))
    if local is not None:
        violations.extend(compare_expected(expected, local, "local"))
    if native is not None and local is not None:
        violations.extend(compare_sources(native, local))

    route, native_complete, local_complete = route_evidence(expected, native, local, violations)
    ancestry = ancestry_evidence(expected, native, local, violations)
    permission = permission_evidence(expected, native)

    if permission["status"] == "not_observed":
        violations.append("permission:read_only_native_unobserved")
    elif permission["status"] == "broader_than_required":
        violations.append("permission:read_only_not_enforced")

    identity_conflict = any(
        item.endswith("thread_id_mismatch") or item.startswith("source_conflict:thread_id")
        for item in violations
    )
    source_conflict = any(item.startswith("source_conflict:") for item in violations)
    conflict = (
        route["status"] == "conflict"
        or ancestry["status"] == "conflict"
        or permission["status"] == "broader_than_required"
        or identity_conflict
        or source_conflict
    )
    grade = compact_grade(route, native_complete, local_complete, conflict)
    runtime_required = bool(expected.get("runtime_observation_required", False))

    if conflict:
        status = "mismatch"
        decision = "quarantine"
    elif permission["status"] == "not_observed":
        status = "not_exposed"
        decision = "return_to_root"
    elif runtime_required and not native_complete:
        status = "not_exposed"
        decision = "return_to_root"
    elif not native_complete and not local_complete:
        status = "not_exposed"
        decision = "continue_configuration_only"
    else:
        status = "matched"
        decision = "continue"

    ancestry_match: bool | None
    if ancestry["status"] == "matched":
        ancestry_match = True
    elif ancestry["status"] == "conflict":
        ancestry_match = False
    else:
        ancestry_match = None

    permission_match: bool | None
    if permission["status"] == "matched":
        permission_match = True
    elif permission["status"] in {"broader_than_required", "conflict"}:
        permission_match = False
    else:
        permission_match = None

    result = {
        "status": status,
        "decision": decision,
        "evidence_grade": grade,
        "route_evidence": route,
        "ancestry_evidence": ancestry,
        "permission_evidence": permission,
        "configuration_match": not any(
            item.startswith("native:") or item.startswith("local:") for item in violations
        ),
        "runtime_reported": native_complete,
        "local_record_observed": local_complete,
        "source_agreement": not source_conflict,
        "permission_match": permission_match,
        "ancestry_match": ancestry_match,
        "violations": sorted(set(violations)),
    }
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
