#!/usr/bin/env python3
"""Normalize Codex main-session or child runtime route evidence.

Child mode reconciles an expected exact project route with supplied observations.
Main-session mode observes model/effort without inventing an expected role and derives
only the conservative judgment-coverage state used by Routing V4.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
POLICY_CONTRACT_PATH = ROOT / "policy-contract.json"
CHILD_ROUTE_FIELDS = ("agent_role", "model", "effort")
MAIN_ROUTE_FIELDS = ("model", "effort")
IDENTITY_FIELDS = ("thread_id", "parent_thread_id")
PERMISSION_FIELDS = ("sandbox_policy_type", "permission_profile_type")
OBSERVED_FIELDS = (*CHILD_ROUTE_FIELDS, *IDENTITY_FIELDS, *PERMISSION_FIELDS)
READ_ONLY_SANDBOXES = {"read-only", "read_only", "readonly"}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"ERROR: {message}")


def load_judgment_reference_model() -> str:
    try:
        payload = json.loads(POLICY_CONTRACT_PATH.read_text(encoding="utf-8"))
        classification = payload["classification"]
        role = classification["main_coverage_reference_role"]
        model = payload["roles"][role]["model"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        fail(f"invalid Routing V4 policy contract for main coverage: {exc}")
    if payload.get("schema_version") != 2:
        fail("main coverage requires policy contract schema 2")
    if not isinstance(role, str) or not isinstance(model, str) or not model.strip():
        fail("main coverage reference role/model is invalid")
    return model.strip().lower()


JUDGMENT_REFERENCE_MODEL = load_judgment_reference_model()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize Codex main-session or child runtime route evidence."
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


def observed_fields(
    observation: dict[str, str | None] | None, fields: tuple[str, ...]
) -> list[str]:
    if observation is None:
        return []
    return [field for field in fields if observation.get(field) is not None]


def evidence_source(native: bool, local: bool) -> str:
    if native and local:
        return "both"
    if native:
        return "native"
    if local:
        return "local"
    return "none"


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


def source_conflicts(
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    fields: tuple[str, ...],
) -> list[str]:
    if native is None or local is None:
        return []
    return [
        f"source_conflict:{field}"
        for field in fields
        if native.get(field) is not None
        and local.get(field) is not None
        and native[field] != local[field]
    ]


def main_session_result(payload: dict[str, Any]) -> dict[str, Any]:
    native = normalize_observation(object_or_none(payload.get("native"), "native"))
    local = normalize_observation(object_or_none(payload.get("local"), "local"))
    violations = source_conflicts(native, local, MAIN_ROUTE_FIELDS)
    native_seen = observed_fields(native, MAIN_ROUTE_FIELDS)
    local_seen = observed_fields(local, MAIN_ROUTE_FIELDS)
    seen = sorted(set(native_seen + local_seen))
    native_complete = native is not None and all(native.get(field) for field in MAIN_ROUTE_FIELDS)
    local_complete = local is not None and all(local.get(field) for field in MAIN_ROUTE_FIELDS)
    conflict = bool(violations)

    if conflict:
        status = "conflict"
    elif native_complete or local_complete:
        status = "observed"
    elif seen:
        status = "partial"
    else:
        status = "not_observed"

    if conflict or not native_complete:
        coverage = "unknown"
    else:
        model = str(native.get("model") or "").lower()
        coverage = (
            "covered"
            if model == JUDGMENT_REFERENCE_MODEL
            or model.startswith(JUDGMENT_REFERENCE_MODEL + "-")
            else "uncovered"
        )

    return {
        "subject": "main_session",
        "status": status,
        "decision": "quarantine_main_route_claim" if conflict else "use_observed_coverage",
        "evidence_grade": compact_grade(native_complete, local_complete, conflict),
        "route_evidence": {
            "status": status,
            "source": evidence_source(native_complete, local_complete),
            "observed_fields": seen,
            "native_observed_fields": native_seen,
            "local_observed_fields": local_seen,
        },
        "main_judgment_coverage": coverage,
        "coverage_source": "trusted_session_metadata" if native_complete and not conflict else "not_observed",
        "coverage_reference_model": JUDGMENT_REFERENCE_MODEL,
        "observed_main_model": native.get("model") if native_complete and native is not None else None,
        "observed_main_effort": native.get("effort") if native_complete and native is not None else None,
        "violations": sorted(set(violations)),
    }


def validate_child_expected(expected: dict[str, Any]) -> None:
    missing = [field for field in CHILD_ROUTE_FIELDS if string_or_none(expected.get(field)) is None]
    if missing:
        fail("expected exact route is incomplete; missing: " + ", ".join(missing))
    for flag in ("runtime_observation_required", "requires_enforced_read_only"):
        value = expected.get(flag, False)
        if not isinstance(value, bool):
            fail(f"expected.{flag} must be boolean when present")


def compare_expected(
    expected: dict[str, Any], observed: dict[str, str | None], source: str
) -> list[str]:
    violations: list[str] = []
    for field in (*IDENTITY_FIELDS, *CHILD_ROUTE_FIELDS):
        wanted = string_or_none(expected.get(field))
        got = observed.get(field)
        if wanted is not None and got is not None and wanted != got:
            violations.append(f"{source}:{field}_mismatch")
    return violations


def route_complete(
    observation: dict[str, str | None] | None, source: str, violations: list[str]
) -> bool:
    if observation is None:
        return False
    return all(observation.get(field) is not None for field in CHILD_ROUTE_FIELDS) and not any(
        f"{source}:{field}_mismatch" in violations for field in CHILD_ROUTE_FIELDS
    )


def build_route_evidence(
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> tuple[dict[str, Any], bool, bool]:
    native_complete = route_complete(native, "native", violations)
    local_complete = route_complete(local, "local", violations)
    native_seen = observed_fields(native, CHILD_ROUTE_FIELDS)
    local_seen = observed_fields(local, CHILD_ROUTE_FIELDS)
    seen = sorted(set(native_seen + local_seen))
    conflict = any(item.startswith("source_conflict:") for item in violations) or any(
        f"{source}:{field}_mismatch" in violations
        for source in ("native", "local")
        for field in CHILD_ROUTE_FIELDS
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
    if "source_conflict:parent_thread_id" in violations:
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
    if any(
        item in violations
        for item in (
            "source_conflict:sandbox_policy_type",
            "source_conflict:permission_profile_type",
        )
    ):
        return {"status": "conflict", "source": "both"}
    if not expected.get("requires_enforced_read_only", False):
        return {"status": "not_required", "source": "none"}
    if native is None or native.get("sandbox_policy_type") is None:
        return {"status": "not_observed", "source": "none"}
    sandbox = native["sandbox_policy_type"]
    if sandbox is not None and sandbox.lower() in READ_ONLY_SANDBOXES:
        return {"status": "matched", "source": "native"}
    return {"status": "broader_than_required", "source": "native"}


def tri_state(status: str, *, matched: str = "matched", failed: set[str]) -> bool | None:
    if status == matched:
        return True
    if status in failed:
        return False
    return None


def child_result(payload: dict[str, Any]) -> dict[str, Any]:
    expected = object_or_none(payload.get("expected"), "expected")
    if expected is None:
        fail("expected is required for child evidence")
    validate_child_expected(expected)
    native = normalize_observation(object_or_none(payload.get("native"), "native"))
    local = normalize_observation(object_or_none(payload.get("local"), "local"))

    violations: list[str] = []
    if native is not None:
        violations.extend(compare_expected(expected, native, "native"))
    if local is not None:
        violations.extend(compare_expected(expected, local, "local"))
    violations.extend(source_conflicts(native, local, OBSERVED_FIELDS))

    route, native_complete, local_complete = build_route_evidence(native, local, violations)
    ancestry = build_ancestry_evidence(expected, native, local, violations)
    permission = build_permission_evidence(expected, native, local, violations)

    if permission["status"] == "not_observed":
        violations.append("permission:read_only_native_unobserved")
    elif permission["status"] == "broader_than_required":
        violations.append("permission:read_only_not_enforced")

    identity_conflict = any(
        item.endswith("thread_id_mismatch")
        or item.startswith("source_conflict:thread_id")
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

    source_agreement = None
    if native is not None and local is not None:
        overlap = any(
            native.get(field) is not None and local.get(field) is not None
            for field in OBSERVED_FIELDS
        )
        if overlap:
            source_agreement = not any(
                item.startswith("source_conflict:") for item in violations
            )

    return {
        "subject": "child",
        "status": status,
        "decision": decision,
        "evidence_grade": compact_grade(native_complete, local_complete, conflict),
        "route_evidence": route,
        "ancestry_evidence": ancestry,
        "permission_evidence": permission,
        "configuration_match": tri_state(route["status"], failed={"conflict"}),
        "runtime_reported": native_complete,
        "local_record_observed": local_complete,
        "source_agreement": source_agreement,
        "permission_match": tri_state(
            permission["status"], failed={"broader_than_required", "conflict"}
        ),
        "ancestry_match": tri_state(ancestry["status"], failed={"conflict"}),
        "violations": sorted(set(violations)),
    }


def main() -> None:
    args = parse_args()
    payload = load_payload(args.input)
    subject = payload.get("subject", "child")
    if subject == "main_session":
        result = main_session_result(payload)
    elif subject == "child":
        result = child_result(payload)
    else:
        fail("subject must be 'main_session' or 'child'")
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
