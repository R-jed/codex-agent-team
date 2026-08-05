#!/usr/bin/env python3
"""Normalize optional runtime route evidence for codex delegate.

This helper is diagnostic. Ordinary task routing must not depend on telemetry that the
runtime did not expose. Main-session evidence is used only to suppress a redundant Sol
capability-uplift call when the current main route is already at least as capable as the
policy reference. Child evidence verifies exact route, ancestry, and permission claims
when those facts are material.
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


def load_main_coverage_policy() -> tuple[str, str, tuple[str, ...]]:
    try:
        payload = json.loads(POLICY_CONTRACT_PATH.read_text(encoding="utf-8"))
        classification = payload["classification"]
        role = classification["main_coverage_reference_role"]
        order = classification["reasoning_effort_order"]
        reference = payload["roles"][role]
        model = reference["model"]
        effort = reference["effort"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        fail(f"invalid policy contract for main coverage: {exc}")
    if payload.get("schema_version") != 2:
        fail("main coverage requires policy contract schema 2")
    if not isinstance(role, str) or not isinstance(model, str) or not model.strip():
        fail("main coverage reference role/model is invalid")
    if not isinstance(effort, str) or not effort.strip():
        fail("main coverage reference effort is invalid")
    if not isinstance(order, list) or not order or not all(isinstance(x, str) and x for x in order):
        fail("reasoning_effort_order must be a non-empty string list")
    normalized_order = tuple(x.strip().lower() for x in order)
    if effort.strip().lower() not in normalized_order or len(set(normalized_order)) != len(normalized_order):
        fail("reasoning_effort_order does not contain a unique reference effort")
    return model.strip().lower(), effort.strip().lower(), normalized_order


JUDGMENT_REFERENCE_MODEL, JUDGMENT_REFERENCE_EFFORT, REASONING_EFFORT_ORDER = load_main_coverage_policy()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize codex delegate runtime evidence.")
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


def text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def normalize(value: dict[str, Any] | None) -> dict[str, str | None] | None:
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
    return {key: text(value.get(key)) for key in allowed}


def observed(observation: dict[str, str | None] | None, fields: tuple[str, ...]) -> list[str]:
    if observation is None:
        return []
    return [field for field in fields if observation.get(field) is not None]


def source(native: bool, local: bool) -> str:
    if native and local:
        return "both"
    if native:
        return "native"
    if local:
        return "local"
    return "none"


def grade(native_complete: bool, local_complete: bool, conflict: bool) -> str:
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


def model_matches_reference(model: str) -> bool:
    model = model.lower()
    return model == JUDGMENT_REFERENCE_MODEL or model.startswith(JUDGMENT_REFERENCE_MODEL + "-")


def effort_coverage(effort: str) -> str:
    normalized = effort.lower()
    if normalized not in REASONING_EFFORT_ORDER:
        return "unknown"
    return (
        "covered"
        if REASONING_EFFORT_ORDER.index(normalized)
        >= REASONING_EFFORT_ORDER.index(JUDGMENT_REFERENCE_EFFORT)
        else "uncovered"
    )


def main_session_result(payload: dict[str, Any]) -> dict[str, Any]:
    native = normalize(object_or_none(payload.get("native"), "native"))
    local = normalize(object_or_none(payload.get("local"), "local"))
    violations = source_conflicts(native, local, MAIN_ROUTE_FIELDS)
    native_seen = observed(native, MAIN_ROUTE_FIELDS)
    local_seen = observed(local, MAIN_ROUTE_FIELDS)
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

    coverage = "unknown"
    if native_complete and not conflict and native is not None:
        model = str(native.get("model") or "")
        effort = str(native.get("effort") or "")
        if not model_matches_reference(model):
            coverage = "uncovered"
        else:
            coverage = effort_coverage(effort)

    trusted = native_complete and not conflict
    return {
        "subject": "main_session",
        "status": status,
        "decision": "quarantine_main_route_claim" if conflict else "use_observed_coverage",
        "evidence_grade": grade(native_complete, local_complete, conflict),
        "route_evidence": {
            "status": status,
            "source": source(native_complete, local_complete),
            "observed_fields": seen,
            "native_observed_fields": native_seen,
            "local_observed_fields": local_seen,
        },
        "main_judgment_coverage": coverage,
        "coverage_source": "trusted_session_metadata" if trusted else "not_observed",
        "coverage_reference_model": JUDGMENT_REFERENCE_MODEL,
        "coverage_reference_effort": JUDGMENT_REFERENCE_EFFORT,
        "observed_main_model": native.get("model") if trusted and native is not None else None,
        "observed_main_effort": native.get("effort") if trusted and native is not None else None,
        "violations": sorted(set(violations)),
    }


def validate_expected(expected: dict[str, Any]) -> None:
    missing = [field for field in CHILD_ROUTE_FIELDS if text(expected.get(field)) is None]
    if missing:
        fail("expected exact route is incomplete; missing: " + ", ".join(missing))
    for flag in ("runtime_observation_required", "requires_enforced_read_only"):
        if not isinstance(expected.get(flag, False), bool):
            fail(f"expected.{flag} must be boolean when present")


def compare_expected(expected: dict[str, Any], obs: dict[str, str | None], label: str) -> list[str]:
    out: list[str] = []
    for field in (*IDENTITY_FIELDS, *CHILD_ROUTE_FIELDS):
        wanted, got = text(expected.get(field)), obs.get(field)
        if wanted is not None and got is not None and wanted != got:
            out.append(f"{label}:{field}_mismatch")
    return out


def route_complete(obs: dict[str, str | None] | None, label: str, violations: list[str]) -> bool:
    if obs is None:
        return False
    return all(obs.get(field) is not None for field in CHILD_ROUTE_FIELDS) and not any(
        f"{label}:{field}_mismatch" in violations for field in CHILD_ROUTE_FIELDS
    )


def child_result(payload: dict[str, Any]) -> dict[str, Any]:
    expected = object_or_none(payload.get("expected"), "expected")
    if expected is None:
        fail("expected is required for child evidence")
    validate_expected(expected)
    native = normalize(object_or_none(payload.get("native"), "native"))
    local = normalize(object_or_none(payload.get("local"), "local"))

    violations: list[str] = []
    if native is not None:
        violations.extend(compare_expected(expected, native, "native"))
    if local is not None:
        violations.extend(compare_expected(expected, local, "local"))
    violations.extend(source_conflicts(native, local, OBSERVED_FIELDS))

    native_complete = route_complete(native, "native", violations)
    local_complete = route_complete(local, "local", violations)
    native_seen = observed(native, CHILD_ROUTE_FIELDS)
    local_seen = observed(local, CHILD_ROUTE_FIELDS)
    route_conflict = any(item.startswith("source_conflict:") for item in violations) or any(
        f"{label}:{field}_mismatch" in violations
        for label in ("native", "local")
        for field in CHILD_ROUTE_FIELDS
    )
    if route_conflict:
        route_status = "conflict"
    elif native_complete or local_complete:
        route_status = "matched"
    elif native_seen or local_seen:
        route_status = "partial"
    else:
        route_status = "not_observed"
    route = {
        "status": route_status,
        "source": source(native_complete, local_complete),
        "observed_fields": sorted(set(native_seen + local_seen)),
        "native_observed_fields": native_seen,
        "local_observed_fields": local_seen,
    }

    wanted_parent = text(expected.get("parent_thread_id"))
    parent_conflict = "source_conflict:parent_thread_id" in violations or any(
        "parent_thread_id_mismatch" in item for item in violations
    )
    if parent_conflict:
        ancestry = {"status": "conflict", "source": source(bool(native), bool(local))}
    elif wanted_parent is None:
        ancestry = {"status": "not_required", "source": "none"}
    elif not ((native and native.get("parent_thread_id")) or (local and local.get("parent_thread_id"))):
        ancestry = {"status": "not_observed", "source": "none"}
    else:
        ancestry = {"status": "matched", "source": source(bool(native), bool(local))}

    if not expected.get("requires_enforced_read_only", False):
        permission = {"status": "not_required", "source": "none"}
    elif "source_conflict:sandbox_policy_type" in violations or "source_conflict:permission_profile_type" in violations:
        permission = {"status": "conflict", "source": "both"}
    elif native is None or native.get("sandbox_policy_type") is None:
        permission = {"status": "not_observed", "source": "none"}
        violations.append("permission:read_only_native_unobserved")
    elif str(native["sandbox_policy_type"]).lower() in READ_ONLY_SANDBOXES:
        permission = {"status": "matched", "source": "native"}
    else:
        permission = {"status": "broader_than_required", "source": "native"}
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
        overlap = any(native.get(field) is not None and local.get(field) is not None for field in OBSERVED_FIELDS)
        if overlap:
            source_agreement = not any(item.startswith("source_conflict:") for item in violations)

    def tri(value: str, failed: set[str]) -> bool | None:
        if value == "matched":
            return True
        if value in failed:
            return False
        return None

    return {
        "subject": "child",
        "status": status,
        "decision": decision,
        "evidence_grade": grade(native_complete, local_complete, conflict),
        "route_evidence": route,
        "ancestry_evidence": ancestry,
        "permission_evidence": permission,
        "configuration_match": tri(route["status"], {"conflict"}),
        "runtime_reported": native_complete,
        "local_record_observed": local_complete,
        "source_agreement": source_agreement,
        "permission_match": tri(permission["status"], {"broader_than_required", "conflict"}),
        "ancestry_match": tri(ancestry["status"], {"conflict"}),
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
