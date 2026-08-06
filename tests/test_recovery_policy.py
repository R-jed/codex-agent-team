from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SCRIPTS = PLUGIN / "scripts"
SKILL_ROOT = PLUGIN / "skills" / "codex-delegate"
ROUTER = SKILL_ROOT / "references" / "router-core.md"
RECOVERY = SKILL_ROOT / "references" / "recovery.md"
LEDGER_SCRIPT = SCRIPTS / "validate_team_ledger.py"


def load_ledger_validator():
    sys.path.insert(0, str(SCRIPTS))
    try:
        spec = importlib.util.spec_from_file_location("codex_delegate_team_ledger", LEDGER_SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(SCRIPTS))


VALIDATOR = load_ledger_validator()


def attempt(
    *,
    unit_id="U1",
    revision=None,
    task_id="task-1",
    attempt_no=1,
    agent_type="codex_delegate_reader",
    agent_id="agent-1",
    state="COMPLETED",
    followups=0,
    adopted=True,
    failure_origin="none",
    task_blocker="none",
):
    return {
        "unit_id": unit_id,
        "team_plan_revision": revision,
        "task_id": task_id,
        "attempt": attempt_no,
        "agent_type": agent_type,
        "agent_id": agent_id,
        "control_state": state,
        "followup_count": followups,
        "adopted": adopted,
        "failure_origin": failure_origin,
        "task_blocker": task_blocker,
    }


def plan():
    return {
        "schema_version": "1.0",
        "revision": 1,
        "supersedes_revision": None,
        "planning_source": "ad_hoc",
        "source_refs": [],
        "root_goal": "deliver result",
        "units": [
            {
                "unit_id": "U1",
                "role": "reader",
                "goal": "read",
                "output": "evidence",
                "depends_on": [],
                "ownership": {"write": [], "forbidden": []},
                "done_when": "evidence complete",
            },
            {
                "unit_id": "U2",
                "role": "worker",
                "goal": "write",
                "output": "change",
                "depends_on": ["U1"],
                "ownership": {"write": ["src/example.py"], "forbidden": []},
                "done_when": "verified",
            },
        ],
        "integration_owner": "main",
        "integration_order": ["U1", "U2"],
        "final_verification": "Main verifies combined artifact",
        "revision_reason": "initial",
    }


def validate(payload):
    return VALIDATOR.validate_team_ledger_payload(payload)


def test_recovery_is_blocker_diagnosis_not_model_escalation():
    skill = (SKILL_ROOT / "SKILL.md").read_text()
    router = ROUTER.read_text()
    assert "Verify, then diagnose blockers" in skill
    for blocker in ["contract", "judgment", "investigation", "stalled"]:
        assert blocker in skill
        assert blocker in router
    assert "A failed Luna attempt never directly means" in router
    assert "model ladder" in router.lower()


def test_recovery_contract_adds_native_lifecycle_and_bounded_actions():
    text = RECOVERY.read_text()
    for phrase in [
        "UNKNOWN is not failure",
        "2 Agent attempts",
        "1 focused follow-up",
        "failure_origin",
        "task_blocker",
        "same_agent_followup",
        "same_role_retry",
        "semantic_reroute",
        "main_takeover",
        "Failure itself never means Luna -> Terra -> Sol",
    ]:
        assert phrase in text
    for state in [
        "PLANNED",
        "SPAWN_PENDING",
        "RUNNING",
        "COMPLETED",
        "FAILED",
        "UNKNOWN",
        "CLOSED",
    ]:
        assert state in text


def test_single_child_ledger_does_not_require_team_plan():
    payload = {
        "schema_version": "1.0",
        "team_plans": [],
        "active_team_plan_revision": None,
        "attempts": [attempt()],
    }
    result = validate(payload)
    assert result["ledger_valid"] is True
    assert result["unit_count"] == 1


def test_multiple_units_require_team_plan_and_role_binding():
    payload = {
        "schema_version": "1.0",
        "team_plans": [],
        "active_team_plan_revision": None,
        "attempts": [
            attempt(),
            attempt(unit_id="U2", task_id="task-2", agent_id="agent-2"),
        ],
    }
    assert "multiple delegated units require TeamPlan binding" in validate(payload)["errors"]

    payload = {
        "schema_version": "1.0",
        "team_plans": [plan()],
        "active_team_plan_revision": 1,
        "attempts": [
            attempt(revision=1),
            attempt(
                unit_id="U2",
                revision=1,
                task_id="task-2",
                agent_type="codex_delegate_worker",
                agent_id="agent-2",
            ),
        ],
    }
    assert validate(payload)["ledger_valid"] is True

    payload["attempts"][1]["agent_type"] = "codex_delegate_reader"
    assert any("does not match TeamPlan role" in error for error in validate(payload)["errors"])


def test_task_and_agent_identity_are_unique():
    payload = {
        "schema_version": "1.0",
        "team_plans": [plan()],
        "active_team_plan_revision": 1,
        "attempts": [
            attempt(revision=1),
            attempt(
                unit_id="U2",
                revision=1,
                task_id="task-1",
                agent_type="codex_delegate_worker",
                agent_id="agent-1",
            ),
        ],
    }
    errors = validate(payload)["errors"]
    assert any("duplicates task_id" in error for error in errors)
    assert any("duplicates agent_id" in error for error in errors)


def test_second_agent_attempt_requires_confirmed_failed_first_attempt():
    first = attempt(
        state="FAILED",
        adopted=False,
        failure_origin="quality_failure",
        task_blocker="stalled",
    )
    second = attempt(
        task_id="task-2",
        attempt_no=2,
        agent_id="agent-2",
        state="RUNNING",
        adopted=False,
    )
    payload = {
        "schema_version": "1.0",
        "team_plans": [],
        "active_team_plan_revision": None,
        "attempts": [first, second],
    }
    assert validate(payload)["ledger_valid"] is True

    payload["attempts"][0] = attempt(state="COMPLETED", adopted=False)
    assert any("second attempt requires the first attempt to be FAILED" in error for error in validate(payload)["errors"])


def test_unknown_attempt_blocks_replacement_and_requires_runtime_ambiguous_origin():
    unknown = attempt(
        agent_id=None,
        state="UNKNOWN",
        adopted=False,
        failure_origin="runtime_ambiguous",
    )
    payload = {
        "schema_version": "1.0",
        "team_plans": [],
        "active_team_plan_revision": None,
        "attempts": [unknown],
    }
    assert validate(payload)["ledger_valid"] is True

    replacement = attempt(
        task_id="task-2",
        attempt_no=2,
        agent_id="agent-2",
        state="RUNNING",
        adopted=False,
    )
    payload["attempts"].append(replacement)
    assert any("UNKNOWN attempt forbids a replacement attempt" in error for error in validate(payload)["errors"])

    payload["attempts"] = [unknown]
    payload["attempts"][0]["failure_origin"] = "timeout"
    assert any("UNKNOWN requires failure_origin=runtime_ambiguous" in error for error in validate(payload)["errors"])


def test_followup_and_attempt_bounds_are_machine_enforced():
    payload = {
        "schema_version": "1.0",
        "team_plans": [],
        "active_team_plan_revision": None,
        "attempts": [attempt(followups=2)],
    }
    assert any("followup_count must be 0 or 1" in error for error in validate(payload)["errors"])

    payload["attempts"] = [attempt(attempt_no=3)]
    assert any("attempt must be 1 or 2" in error for error in validate(payload)["errors"])


def test_failure_state_and_adoption_consistency_fail_closed():
    failed = attempt(state="FAILED", adopted=False, failure_origin="none")
    payload = {
        "schema_version": "1.0",
        "team_plans": [],
        "active_team_plan_revision": None,
        "attempts": [failed],
    }
    assert any("FAILED requires a failure_origin" in error for error in validate(payload)["errors"])

    closed = attempt(state="CLOSED", adopted=False)
    payload["attempts"] = [closed]
    assert any("CLOSED requires adopted=true" in error for error in validate(payload)["errors"])


def test_team_plan_revision_binding_does_not_reset_unit_attempt_budget():
    first_plan = plan()
    second_plan = plan()
    second_plan["revision"] = 2
    second_plan["supersedes_revision"] = 1
    second_plan["revision_reason"] = "scope changed"

    payload = {
        "schema_version": "1.0",
        "team_plans": [first_plan, second_plan],
        "active_team_plan_revision": 2,
        "attempts": [
            attempt(
                revision=1,
                state="FAILED",
                adopted=False,
                failure_origin="quality_failure",
                task_blocker="stalled",
            ),
            attempt(
                revision=2,
                task_id="task-2",
                attempt_no=2,
                agent_id="agent-2",
                state="RUNNING",
                adopted=False,
            ),
        ],
    }
    assert validate(payload)["ledger_valid"] is True

    payload["attempts"].append(
        attempt(
            revision=2,
            task_id="task-3",
            attempt_no=3,
            agent_id="agent-3",
            state="RUNNING",
            adopted=False,
        )
    )
    errors = validate(payload)["errors"]
    assert any("attempt must be 1 or 2" in error for error in errors)
    assert any("exceeds the two-Agent-attempt recovery bound" in error for error in errors)


def test_behavioral_schema_remains_measurement_surface_not_runtime_state_source():
    schema = json.loads((ROOT / "evals" / "behavioral-result.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    props = schema["properties"]["runs"]["items"]["properties"]
    for field in [
        "reclassification_events",
        "execution_stall_events",
        "clean_same_lane_restarts",
        "same_failure_without_new_evidence",
        "duplicate_dependency_calls",
    ]:
        assert field in props

    docs = (ROOT / "docs" / "behavioral-evals.md").read_text().lower()
    assert "measurement surface" in docs
    assert "historical" in docs and "experiment labels" in docs
