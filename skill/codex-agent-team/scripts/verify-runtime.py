#!/usr/bin/env python3
"""Deterministically reconcile expected and observed native Subagent runtime facts.

Input is a JSON object on stdin or via --input. Observation objects must already be
normalized to the allowlisted shape emitted by inspect-runtime.py or an equivalent
native-metadata adapter. This verifier never reads rollout files itself.

Evidence grades deliberately distinguish configuration, runtime reports, and mutable
local records. Local rollout data is corroborating telemetry, not authoritative or
cryptographic attestation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, NoReturn

ROUTE_FIELDS = ("agent_role", "model", "effort")
OPTIONAL_IDENTITY_FIELDS = ("thread_id", "parent_thread_id")
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
    mapping = {
        "thread_id": "thread_id",
        "parent_thread_id": "parent_thread_id",
        "agent_role": "agent_role",
        "model": "model",
        "effort": "effort",
    }
    for expected_key, observed_key in mapping.items():
        wanted = string_or_none(expected.get(expected_key))
        got = observed.get(observed_key)
        if wanted is not None and got is not None and wanted != got:
            violations.append(f"{source}:{expected_key}_mismatch")
    return violations


def compare_sources(
    native: dict[str, str | None],
    local: dict[str, str | None],
) -> list[str]:
    violations: list[str] = []
    for field in (*ROUTE_FIELDS, *OPTIONAL_IDENTITY_FIELDS, *PERMISSION_FIELDS):
        left = native.get(field)
        right = local.get(field)
        if left is not None and right is not None and left != right:
            violations.append(f"source_conflict:{field}")
    return violations


def read_only_observed(observation: dict[str, str | None] | None) -> bool | None:
    if observation is None:
        return None
    sandbox = observation.get("sandbox_policy_type")
    if sandbox is None:
        return None
    return sandbox.lower() in READ_ONLY_SANDBOXES


def choose_permission_observation(
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
) -> bool | None:
    native_read_only = read_only_observed(native)
    if native_read_only is not None:
        return native_read_only
    return read_only_observed(local)


def evidence_grade(
    native: dict[str, str | None] | None,
    local: dict[str, str | None] | None,
    violations: list[str],
) -> str:
    if violations:
        return "X0_conflicted"
    if native is not None and local is not None:
        return "R2_runtime_reported_and_local_record_agree"
    if native is not None:
        return "R1_runtime_reported"
    if local is not None:
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

    requires_read_only = bool(expected.get("requires_enforced_read_only", False))
    observed_read_only = choose_permission_observation(native, local)
    if requires_read_only:
        if observed_read_only is None:
            violations.append("permission:read_only_unobserved")
        elif not observed_read_only:
            violations.append("permission:read_only_not_enforced")

    grade = evidence_grade(native, local, violations)
    runtime_observation_required = bool(expected.get("runtime_observation_required", False))

    if violations:
        status = "mismatch"
        decision = "quarantine"
        if violations == ["permission:read_only_unobserved"]:
            status = "not_exposed"
            decision = "return_to_root"
    elif runtime_observation_required and native is None:
        status = "not_exposed"
        decision = "return_to_root"
    elif native is None and local is None:
        status = "not_exposed"
        decision = "continue_configuration_only"
    else:
        status = "matched"
        decision = "continue"

    result = {
        "status": status,
        "decision": decision,
        "evidence_grade": grade,
        "configuration_match": not any(
            item.startswith("native:") or item.startswith("local:") for item in violations
        ),
        "runtime_reported": native is not None,
        "local_record_observed": local is not None,
        "source_agreement": not any(item.startswith("source_conflict:") for item in violations),
        "permission_match": not any(item.startswith("permission:") for item in violations),
        "ancestry_match": not any("parent_thread_id_mismatch" in item for item in violations),
        "violations": sorted(set(violations)),
    }
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
