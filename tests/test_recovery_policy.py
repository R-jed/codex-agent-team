from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "plugins" / "codex-delegate" / "skills" / "codex-delegate"
ROUTER = SKILL_ROOT / "references" / "router-core.md"


def test_recovery_is_blocker_diagnosis_not_model_escalation():
    skill = (SKILL_ROOT / "SKILL.md").read_text()
    router = ROUTER.read_text()
    assert "Verify, then diagnose blockers" in skill
    for blocker in ["contract", "judgment", "specialist", "stalled"]:
        assert blocker in skill
        assert blocker in router
    assert "A failed Luna attempt never directly means" in router
    assert "model ladder" in router.lower()


def test_stalled_work_has_one_clean_retry_not_numeric_retry_state_machine():
    router = ROUTER.read_text()
    assert "at most one clean retry" in router
    assert "same role remains correct" in router
    assert "materially improved packet" in router
    assert "unbounded" not in router.lower()


def test_runtime_state_is_one_compact_work_item_not_three_ledgers():
    skill = (SKILL_ROOT / "SKILL.md").read_text()
    router = ROUTER.read_text()
    for field in [
        "outcome",
        "owner",
        "write: yes | no",
        "material_judgment: none | separable | coupled",
        "acceptance",
        "valid_evidence",
        "current_failure",
        "blocked_by: none | contract | judgment | specialist | stalled",
    ]:
        assert field in router
    for retired in ["Dependency Ledger", "Shared Evidence State", "Recovery Ledger"]:
        assert retired not in skill
        assert retired not in router


def test_child_proposal_never_becomes_orchestration_authority():
    router = ROUTER.read_text()
    guardrails = (SKILL_ROOT / "references" / "guardrails.md").read_text()
    assert "Children do not widen scope, permission, user intent, external impact, or their own role" in router
    assert "main session always owns" in guardrails.lower()
    assert "Child completion, confidence, model agreement" in guardrails


def test_progress_observability_remains_runtime_fact_not_recovery_ceremony():
    runtime = (ROOT / "docs" / "native-subagent-runtime.md").read_text()
    for level in ["none", "terminal_only", "periodic_summary", "structured_live"]:
        assert level in runtime
    assert "A wake-up event does not imply deterministic insight into child progress" in runtime
    assert "does not simulate event-driven behavior with model-mediated busy polling" in runtime


def test_behavioral_schema_can_keep_legacy_recovery_measurements_without_owning_runtime_policy():
    schema = json.loads((ROOT / "evals" / "behavioral-result.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    props = schema["properties"]["runs"]["items"]["properties"]
    for field in [
        "recovery_ledger_entries",
        "attempt_cycle_detected",
        "proposed_recovery_action",
        "effective_recovery_action",
        "recovery_decision_source",
        "child_progress_observability",
    ]:
        assert field in props

    docs = (ROOT / "docs" / "behavioral-evals.md").read_text().lower()
    assert "measurement surface" in docs
    assert "historical measurement labels" in docs
    assert "do not make the skill maintain an ontology" in docs
