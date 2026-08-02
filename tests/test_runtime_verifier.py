from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "skill" / "codex-agent-team" / "scripts" / "verify-runtime.py"
THREAD = "11111111-1111-7111-8111-111111111111"
PARENT = "00000000-0000-7000-8000-000000000000"


def run_verifier(payload: dict) -> tuple[subprocess.CompletedProcess[str], dict | None]:
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    data = json.loads(result.stdout) if result.returncode == 0 else None
    return result, data


def expected(**overrides):
    value = {
        "thread_id": THREAD,
        "parent_thread_id": PARENT,
        "agent_role": "luna_worker",
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
        "agent_role": "luna_worker",
        "model": "gpt-5.6-luna",
        "effort": "max",
        "sandbox_policy_type": "workspace-write",
        "permission_profile_type": "default",
    }
    value.update(overrides)
    return value


def test_configuration_only_is_explicitly_c1():
    result, data = run_verifier({"expected": expected(), "native": None, "local": None})
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "continue_configuration_only"
    assert data["status"] == "not_exposed"
    assert data["evidence_grade"] == "C1_configuration_only"


def test_native_report_is_r1():
    result, data = run_verifier({"expected": expected(), "native": observation(), "local": None})
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "continue"
    assert data["evidence_grade"] == "R1_runtime_reported"
    assert data["runtime_reported"] is True


def test_local_record_alone_is_not_promoted_to_runtime_report():
    result, data = run_verifier({"expected": expected(), "native": None, "local": observation()})
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "continue"
    assert data["evidence_grade"] == "L1_local_record_observed"
    assert data["runtime_reported"] is False


def test_native_and_local_agreement_is_r2():
    result, data = run_verifier(
        {"expected": expected(), "native": observation(), "local": observation()}
    )
    assert result.returncode == 0, result.stderr
    assert data["evidence_grade"] == "R2_runtime_reported_and_local_record_agree"
    assert data["source_agreement"] is True


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
    assert "source_conflict:model" in data["violations"]


def test_wrong_parent_is_a_depth_one_violation():
    result, data = run_verifier(
        {
            "expected": expected(),
            "native": observation(parent_thread_id="22222222-2222-7222-8222-222222222222"),
        }
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "quarantine"
    assert data["ancestry_match"] is False
    assert "native:parent_thread_id_mismatch" in data["violations"]


def test_required_runtime_observation_cannot_be_satisfied_by_local_record_only():
    result, data = run_verifier(
        {
            "expected": expected(runtime_observation_required=True),
            "native": None,
            "local": observation(),
        }
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "return_to_root"
    assert data["status"] == "not_exposed"
    assert data["evidence_grade"] == "L1_local_record_observed"


def test_required_read_only_requires_observed_read_only():
    result, data = run_verifier(
        {
            "expected": expected(requires_enforced_read_only=True),
            "native": observation(sandbox_policy_type="workspace-write"),
        }
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "quarantine"
    assert data["permission_match"] is False
    assert "permission:read_only_not_enforced" in data["violations"]


def test_required_read_only_unobserved_returns_to_root():
    obs = observation()
    obs["sandbox_policy_type"] = None
    result, data = run_verifier(
        {
            "expected": expected(requires_enforced_read_only=True),
            "native": obs,
        }
    )
    assert result.returncode == 0, result.stderr
    assert data["decision"] == "return_to_root"
    assert data["status"] == "not_exposed"
