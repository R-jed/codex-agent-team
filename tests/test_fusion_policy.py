from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
RUNTIME_VERIFIER = PLUGIN / "scripts" / "runtime-evidence.py"


def load_cases() -> dict:
    return json.loads((ROOT / "evals" / "runtime-assurance-cases.json").read_text())


def test_compact_runtime_references_and_verifier_are_installed():
    refs = SKILL / "references"
    assert {path.name for path in refs.glob("*.md")} == {
        "router-core.md",
        "guardrails.md",
        "final-review.md",
    }
    assert RUNTIME_VERIFIER.is_file()
    skill = (SKILL / "SKILL.md").read_text()
    assert "runtime-evidence.py" in skill
    assert not (SKILL / "scripts" / "inspect-runtime.py").exists()


def test_compute_lanes_have_distinct_responsibilities_without_fixed_order():
    combined = (SKILL / "SKILL.md").read_text() + (SKILL / "references" / "router-core.md").read_text()
    lower = combined.lower()
    assert "luna" in lower and "clear" in lower and "repeatable" in lower and "bounded" in lower
    assert "terra" in lower and "read-heavy" in lower and "investigation" in lower
    assert "sol" in lower and "material judgment" in lower
    assert "model ladder" in lower
    assert "zero children is normal" in lower


def test_runtime_observation_is_demand_driven_not_universal_overhead():
    guardrails = (SKILL / "references" / "guardrails.md").read_text()
    router = (SKILL / "references" / "router-core.md").read_text()
    assert "Do not run runtime-evidence diagnostics for every ordinary child" in guardrails
    assert "routine bounded" in guardrails.lower()
    assert "Main-session Sol dedup is an optimization" in router


def test_compact_child_packet_keeps_decision_rights_acceptance_and_evidence_reuse():
    router = (SKILL / "references" / "router-core.md").read_text()
    for section in [
        "OUTCOME",
        "READ / WRITE SCOPE",
        "INTERFACES AND INVARIANTS",
        "DECISION RIGHTS",
        "ACCEPTANCE",
        "VALID EVIDENCE / DO NOT REDO",
        "STOP WHEN",
    ]:
        assert section in router
    assert "child report is a claim" in router.lower()
    assert "actual artifact state" in router


def test_sol_is_high_leverage_and_terra_is_investigation_value_lane():
    router = (SKILL / "references" / "router-core.md").read_text()
    lower = router.lower()
    assert "demanding or material judgment before writing" in lower
    assert "writing with judgment coupled to implementation" in lower
    assert "bounded read-heavy technical investigation" in lower
    assert "terra is an investigation/value lane" in lower
    assert "demanding, ambiguous, multi-step technical reasoning" in lower
    assert "failed luna attempt never directly means" in lower


def test_behavioral_read_only_never_claims_runtime_enforcement():
    guardrails = (SKILL / "references" / "guardrails.md").read_text()
    assert "configured read-only profile is intent, not proof" in guardrails
    assert "behavioral read-only" in guardrails
    assert "broader effective permission remains recorded as residual risk" in guardrails


def test_runtime_truth_cases_cover_partial_and_typed_evidence_regressions():
    payload = load_cases()
    assert payload["schema_version"] == "2.0"
    cases = {case["id"]: case for case in payload["cases"]}
    required = {
        "ordinary-route-observation-unavailable",
        "native-runtime-route-complete",
        "native-runtime-route-partial",
        "two-partial-sources-do-not-form-r2",
        "native-local-route-conflict",
        "expected-parent-unobserved",
        "required-readonly-native-unobserved",
    }
    assert required <= set(cases)
    assert cases["native-runtime-route-partial"]["expected"]["evidence_grade"] == "C1_configuration_only"
    assert cases["two-partial-sources-do-not-form-r2"]["expected"]["evidence_grade"] == "C1_configuration_only"
    assert cases["expected-parent-unobserved"]["expected"]["ancestry_status"] == "not_observed"
