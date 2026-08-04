from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team"


def read(path: Path) -> str:
    return path.read_text()


def test_recovery_is_two_stage_and_not_failure_triggered():
    skill = read(SKILL_ROOT / "SKILL.md")
    progress = read(SKILL_ROOT / "references" / "execution-progress.md")
    routing = read(SKILL_ROOT / "references" / "routing-policy.md")

    for text in [skill, progress, routing]:
        assert "Intervention Gate" in text
        assert "acceptance" in text.lower()
        assert "forward progress" in text.lower()

    assert "Failure to satisfy acceptance and need for intervention are different facts" in progress
    assert "Stage A: Intervention Gate" in routing
    assert "Stage B: Recovery classification" in routing
    assert "successful command" in progress.lower()


def test_recovery_has_no_numeric_stall_or_retry_threshold():
    progress = read(SKILL_ROOT / "references" / "execution-progress.md")
    assert "does not define a universal retry count" in progress
    assert '"three repeats means Terra"' in progress
    assert "fixed numerical thresholds" in progress
    assert "Do not convert this principle into hard retry counts" in progress


def test_recovery_ledger_is_bounded_semantic_state_not_transcript():
    contract = read(SKILL_ROOT / "references" / "delegation-contract.md")
    progress = read(SKILL_ROOT / "references" / "execution-progress.md")

    for field in [
        "ATTEMPT ID",
        "LANE",
        "CORRECTION HYPOTHESIS",
        "FAILURE SIGNATURE",
        "PROGRESS SIGNAL",
        "NEW EVIDENCE IDS",
        "UNRESOLVED DELTA",
        "RECOVERY ACTION",
        "DECISION SOURCE",
    ]:
        assert field in progress

    assert "bounded semantic history" in contract
    assert "not a transcript" in contract
    assert "never store private chain-of-thought" in contract
    assert "MATERIAL RECOVERY HISTORY" in contract


def test_proposed_action_is_not_orchestration_authority():
    progress = read(SKILL_ROOT / "references" / "execution-progress.md")
    contract = read(SKILL_ROOT / "references" / "delegation-contract.md")
    receipt = read(SKILL_ROOT / "references" / "orchestration-receipt.md")

    for field in ["PROPOSED ACTION", "EFFECTIVE ACTION", "DECISION SOURCE", "POLICY TRANSFORM"]:
        assert field in progress

    assert "main session owns `effective_action`" in contract
    assert "suggested_next_action" in contract
    assert "Proposed action" in receipt
    assert "Effective action" in receipt
    assert "model_judgment" in receipt


def test_recovery_evaluation_is_event_driven_and_observability_fail_closed():
    progress = read(SKILL_ROOT / "references" / "execution-progress.md")
    routing = read(SKILL_ROOT / "references" / "routing-policy.md")

    assert "Event-driven recovery evaluation" in progress
    assert "not after every ordinary tool call" in progress
    for level in ["none", "terminal_only", "periodic_summary", "structured_live"]:
        assert level in routing
    assert "Do not claim structured live mid-run anti-thrashing without evidence" in routing


def test_behavioral_workloads_cover_intervention_counterexamples():
    payload = json.loads((ROOT / "evals" / "behavioral-workloads.json").read_text())
    by_id = {item["id"]: item for item in payload["workloads"]}

    required = {
        "healthy-failure-no-intervention",
        "successful-command-no-progress",
        "recovery-ledger-oscillation",
        "proposed-action-policy-transform",
        "child-progress-observability",
    }
    assert required <= set(by_id)
    assert by_id["healthy-failure-no-intervention"]["expected"]["intervention_required"] is False
    assert by_id["successful-command-no-progress"]["expected"]["successful_command_alone_is_progress"] is False
    assert by_id["recovery-ledger-oscillation"]["expected"]["attempt_cycle_detected"] is True


def test_behavioral_schema_supports_recovery_provenance_and_observability():
    schema = json.loads((ROOT / "evals" / "behavioral-result.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    props = schema["properties"]["runs"]["items"]["properties"]
    for field in [
        "intervention_gate_evaluations",
        "interventions_taken",
        "recovery_ledger_entries",
        "attempt_cycle_detected",
        "proposed_recovery_action",
        "effective_recovery_action",
        "recovery_decision_source",
        "policy_transform",
        "child_progress_observability",
    ]:
        assert field in props

    allowed = props["child_progress_observability"]["enum"]
    assert allowed == [None, "none", "terminal_only", "periodic_summary", "structured_live"]
