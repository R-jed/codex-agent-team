from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team" / "scripts" / "verify-runtime.py"
THREAD = "11111111-1111-7111-8111-111111111111"
PARENT = "00000000-0000-7000-8000-000000000000"


def run_verifier(payload: dict):
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    return result, json.loads(result.stdout) if result.returncode == 0 else None


def expected(**overrides):
    value = {
        "thread_id": THREAD,
        "parent_thread_id": PARENT,
        "agent_role": "codex_agent_team_worker",
        "model": "gpt-5.6-luna",
        "effort": "max",
        "runtime_observation_required": False,
        "requires_enforced_read_only": False,
    }
    value.update(overrides)
    return value


def observation(**overrides):
    value = {
        "thread_id": THREAD,
        "parent_thread_id": PARENT,
        "agent_role": "codex_agent_team_worker",
        "model": "gpt-5.6-luna",
        "effort": "max",
        "sandbox_policy_type": "workspace-write",
        "permission_profile_type": "default",
    }
    value.update(overrides)
    return value


def test_configuration_only_is_c1_with_typed_not_observed_states():
    result, data = run_verifier({"expected": expected(), "native": None, "local": None})
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "continue_configuration_only"
    assert data["evidence_grade"] == "C1_configuration_only"
    assert data["route_evidence"]["status"] == "not_observed"
    assert data["ancestry_evidence"]["status"] == "not_observed"
    assert data["ancestry_match"] is None


def test_complete_native_route_is_r1():
    result, data = run_verifier({"expected": expected(), "native": observation(), "local": None})
    assert result.returncode == 0, result.stderr
    assert data["evidence_grade"] == "R1_runtime_reported"
    assert data["route_evidence"]["status"] == "matched"
    assert data["route_evidence"]["source"] == "native"
    assert data["runtime_reported"] is True
    assert data["ancestry_evidence"]["status"] == "matched"


def test_empty_native_object_never_counts_as_r1():
    result, data = run_verifier({"expected": expected(), "native": {}, "local": None})
    assert result.returncode == 0, result.stderr
    assert data["evidence_grade"] == "C1_configuration_only"
    assert data["runtime_reported"] is False
    assert data["route_evidence"]["status"] == "not_observed"


def test_partial_native_route_never_counts_as_r1():
    result, data = run_verifier(
        {"expected": expected(), "native": {"thread_id": THREAD, "agent_role": "codex_agent_team_worker"}, "local": None}
    )
    assert result.returncode == 0, result.stderr
    assert data["evidence_grade"] == "C1_configuration_only"
    assert data["route_evidence"]["status"] == "partial"
    assert data["route_evidence"]["observed_fields"] == ["agent_role"]


def test_runtime_required_rejects_partial_native_route():
    result, data = run_verifier(
        {
            "expected": expected(runtime_observation_required=True),
            "native": {"thread_id": THREAD, "agent_role": "codex_agent_team_worker", "model": "gpt-5.6-luna"},
            "local": None,
        }
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "return_to_root"
    assert data["evidence_grade"] == "C1_configuration_only"
    assert data["route_evidence"]["status"] == "partial"


def test_complete_local_route_is_l1_not_runtime_proof():
    result, data = run_verifier({"expected": expected(), "native": None, "local": observation()})
    assert result.returncode == 0, result.stderr
    assert data["evidence_grade"] == "L1_local_record_observed"
    assert data["runtime_reported"] is False
    assert data["local_record_observed"] is True


def test_two_partial_observations_never_count_as_r2():
    partial = {"agent_role": "codex_agent_team_worker"}
    result, data = run_verifier({"expected": expected(), "native": partial, "local": partial})
    assert result.returncode == 0, result.stderr
    assert data["evidence_grade"] == "C1_configuration_only"
    assert data["route_evidence"]["status"] == "partial"
    assert data["route_evidence"]["source"] == "none"


def test_complete_native_and_local_agreement_is_r2():
    result, data = run_verifier({"expected": expected(), "native": observation(), "local": observation()})
    assert result.returncode == 0, result.stderr
    assert data["evidence_grade"] == "R2_runtime_reported_and_local_record_agree"
    assert data["route_evidence"]["source"] == "both"


def test_cross_source_conflict_is_quarantined():
    result, data = run_verifier(
        {
            "expected": expected(),
            "native": observation(),
            "local": observation(model="gpt-5.6-terra", effort="xhigh"),
        }
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "quarantine"
    assert data["evidence_grade"] == "X0_conflicted"
    assert data["route_evidence"]["status"] == "conflict"


def test_missing_parent_is_not_reported_as_ancestry_match():
    obs = observation(parent_thread_id=None)
    result, data = run_verifier({"expected": expected(), "native": obs})
    assert result.returncode == 0, result.stderr
    assert data["ancestry_evidence"]["status"] == "not_observed"
    assert data["ancestry_match"] is None


def test_wrong_parent_is_quarantined():
    result, data = run_verifier(
        {"expected": expected(), "native": observation(parent_thread_id="22222222-2222-7222-8222-222222222222")}
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "quarantine"
    assert data["ancestry_evidence"]["status"] == "conflict"
    assert data["ancestry_match"] is False


def test_required_read_only_needs_native_effective_sandbox():
    result, data = run_verifier(
        {
            "expected": expected(requires_enforced_read_only=True),
            "native": observation(sandbox_policy_type=None),
            "local": observation(sandbox_policy_type="read-only"),
        }
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "return_to_root"
    assert data["permission_evidence"]["status"] == "not_observed"
    assert data["permission_match"] is None


def test_broader_than_required_read_only_is_quarantined():
    result, data = run_verifier(
        {"expected": expected(requires_enforced_read_only=True), "native": observation(sandbox_policy_type="workspace-write")}
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "quarantine"
    assert data["permission_evidence"]["status"] == "broader_than_required"
    assert data["permission_match"] is False
