#!/usr/bin/env python3
"""Reconcile expected Codex Subagent route/safety facts with observed metadata.

The tool consumes normalized JSON. It does not scrape Codex internals or infer missing
runtime fields from configured profiles. Native metadata is authoritative for claims
that require host-observed route or permission evidence. An optional ``local`` object
may be supplied only as corroborating evidence from an independently collected source.
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
OBSERVED_FIELDS = (*ROUTE_FIELDS, *IDENTITY_FIELDS, *PERMISSION_FIELDS)
READ_ONLY_SANDBOXES = {"read-only", "read_only", "readonly"}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconcile expected Codex Subagent facts with normalized runtime evidence."
    )
    parser.add_argument("--input", type=Path, help="JSON input file; defaults to stdin.")
    return parser.parse_args()


def load_payload(path: Path | None) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8") if path else sys.stdin.read()
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid runtime-evidence input: {exc}")
    if not isinstance(value, dict):
        fail("runtime-evidence input must be a JSON object")
    return value


def object_or_none(value: Any, field: str) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        fail(f"{field} must be an object or null")
    return value


def string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def validate_expected(expected: dict[str, Any]) -> None:
    missing = [field for field in ROUTE_FIELDS if string_or_none(expected.get(field)) is None]
    if missing:
        fail("expected exact route is incomplete; missing: " + ", ".join(missing))
    for flag in ("runtime_observation_required", "requires_enforced_read_only"):
        value = expected.get(flag, False)
        if not isinstance(value, bool):
            fail(f"expected.{flag} must be boolean when present")


def normalize_observation(value: dict[str, Any] | None) -> dict[str, str | None] | None:
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
    expected: dict[str, Any], observed: dict[str, str | None], source: str
) -> list[str]:
    violations: list[str] = []
    for field in (*IDENTITY_FIELDS, *ROUTE_FIELDS):
        wanted = string_or_none(expected.get(field))
        got = observed.get(field)
        if wanted is not None and got is not None and wanted != got:
            violations.append(f"{source}:{field}_mismatch")
    return violations


def compare_sources(
    native: dict[str, str | None], local: dict[str, str | None]
) -> list[str]:
    return [
        f"source_conflict:{field}"
        for field in OBSERVED_FIELDS
        if native.get(field) is not None
        and local.get(field) is not None
        and native[field] != local[field]
    ]


def source_conflict_for(violations: list[str], fields: tuple[str, ...]) -> bool:
    return any(f"source_conflict:{field}" in violations for field in fields)


def observed_fields(
    observation: dict[str, str | None] | None, fields: tuple[str, ...]
) -> list[str]:
    if observation is None:
        return []
    return [field for field in fields if observation.get(field) is not None]


def route_complete(
    observation: dict[str, str | None] | None, source: str, violations: list[str]
) -> bool:
    if observation is None:
        return False
    return all(observation.get(field) is not None for field in ROUTE_FIELDS) and not any(
        f"{source}:{field}_mismatch" in violations for field in ROUTE_FIELDS
    )


def evidence_source(native: bool, local: bool) -> str:
    if native and local:
        return "both"
    if native:
        return "native"
    if local:
        return "local"
    return "none"


def build_route_evidence(
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> tuple[dict[str, Any], bool, bool]:
    native_complete = route_complete(native, "native", violations)
    local_complete = route_complete(local, "local", violations)
    native_seen = observed_fields(native, ROUTE_FIELDS)
    local_seen = observed_fields(local, ROUTE_FIELDS)
    seen = sorted(set(native_seen + local_seen))
    conflict = source_conflict_for(violations, ROUTE_FIELDS) or any(
        f"{source}:{field}_mismatch" in violations
        for source in ("native", "local")
        for field in ROUTE_FIELDS
    )
    if conflict:
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


def build_ancestry_evidence(
    expected: dict[str, Any],
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> dict[str, Any]:
    native_has = native is not None and native.get("parent_thread_id") is not None
    local_has = local is not None and local.get("parent_thread_id") is not None
    if source_conflict_for(violations, ("parent_thread_id",)):
        return {"status": "conflict", "source": "both"}
    wanted = string_or_none(expected.get("parent_thread_id"))
    if wanted is None:
        return {"status": "not_required", "source": "none"}
    if any("parent_thread_id_mismatch" in item for item in violations):
        return {"status": "conflict", "source": evidence_source(native_has, local_has)}
    if not native_has and not local_has:
        return {"status": "not_observed", "source": "none"}
    return {"status": "matched", "source": evidence_source(native_has, local_has)}


def build_permission_evidence(
    expected: dict[str, Any],
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> dict[str, Any]:
    if source_conflict_for(violations, PERMISSION_FIELDS):
        return {"status": "conflict", "source": "both"}
    if not expected.get("requires_enforced_read_only", False):
        return {"status": "not_required", "source": "none"}
    if native is None or native.get("sandbox_policy_type") is None:
        return {"status": "not_observed", "source": "none"}
    sandbox = native["sandbox_policy_type"]
    if sandbox is not None and sandbox.lower() in READ_ONLY_SANDBOXES:
        return {"status": "matched", "source": "native"}
    return {"status": "broader_than_required", "source": "native"}


def source_agreement(
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> bool | None:
    if native is None or local is None:
        return None
    overlap = any(
        native.get(field) is not None and local.get(field) is not None
        for field in OBSERVED_FIELDS
    )
    if not overlap:
        return None
    return not any(item.startswith("source_conflict:") for item in violations)


def compact_grade(native_complete: bool, local_complete: bool, conflict: bool) -> str:
    if conflict:
        return "X0_conflicted"
    if native_complete and local_complete:
        return "R2_runtime_reported_and_local_record_agree"
    if native_complete:
        return "R1_runtime_reported"
    if local_complete:
        return "L1_local_record_observed"
    return "C1_configuration_only"


def tri_state(status: str, *, matched: str = "matched", failed: set[str]) -> bool | None:
    if status == matched:
        return True
    if status in failed:
        return False
    return None


def main() -> None:
    args = parse_args()
    payload = load_payload(args.input)
    expected = object_or_none(payload.get("expected"), "expected")
    if expected is None:
        fail("expected is required")
    validate_expected(expected)

    native = normalize_observation(object_or_none(payload.get("native"), "native"))
    local = normalize_observation(object_or_none(payload.get("local"), "local"))

    violations: list[str] = []
    if native is not None:
        violations.extend(compare_expected(expected, native, "native"))
    if local is not None:
        violations.extend(compare_expected(expected, local, "local"))
    if native is not None and local is not None:
        violations.extend(compare_sources(native, local))

    route, native_complete, local_complete = build_route_evidence(native, local, violations)
    ancestry = build_ancestry_evidence(expected, native, local, violations)
    permission = build_permission_evidence(expected, native, local, violations)

    if permission["status"] == "not_observed":
        violations.append("permission:read_only_native_unobserved")
    elif permission["status"] == "broader_than_required":
        violations.append("permission:read_only_not_enforced")

    identity_conflict = any(
        item.endswith("thread_id_mismatch") or item.startswith("source_conflict:thread_id")
        for item in violations
    )
    conflict = (
        route["status"] == "conflict"
        or ancestry["status"] == "conflict"
        or permission["status"] in {"broader_than_required", "conflict"}
        or identity_conflict
        or any(item.startswith("source_conflict:") for item in violations)
    )

    runtime_required = expected.get("runtime_observation_required", False)
    if conflict:
        status, decision = "mismatch", "quarantine"
    elif permission["status"] == "not_observed":
        status, decision = "not_exposed", "return_to_main_session"
    elif runtime_required and not native_complete:
        status, decision = "not_exposed", "return_to_main_session"
    elif not native_complete and not local_complete:
        status, decision = "not_exposed", "continue_configuration_only"
    else:
        status, decision = "matched", "continue"

    result = {
        "status": status,
        "decision": decision,
        "evidence_grade": compact_grade(native_complete, local_complete, conflict),
        "route_evidence": route,
        "ancestry_evidence": ancestry,
        "permission_evidence": permission,
        "configuration_match": tri_state(route["status"], failed={"conflict"}),
        "runtime_reported": native_complete,
        "local_record_observed": local_complete,
        "source_agreement": source_agreement(native, local, violations),
        "permission_match": tri_state(
            permission["status"], failed={"broader_than_required", "conflict"}
        ),
        "ancestry_match": tri_state(ancestry["status"], failed={"conflict"}),
        "violations": sorted(set(violations)),
    }
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
