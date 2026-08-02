from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team"


def read(path: str) -> str:
    return (ROOT / path).read_text()


def load_cases() -> dict:
    return json.loads((ROOT / "evals" / "runtime-assurance-cases.json").read_text())


def test_runtime_assurance_reference_and_inspector_remain_installed():
    runtime = SKILL / "references" / "runtime-assurance.md"
    inspector = SKILL / "scripts" / "inspect-runtime.py"
    skill = (SKILL / "SKILL.md").read_text()
    assert runtime.exists()
    assert inspector.exists()
    assert "references/runtime-assurance.md" in skill
    assert "scripts/inspect-runtime.py" in runtime.read_text()


def test_three_compute_tiers_have_distinct_responsibilities_not_fixed_order():
    skill = (SKILL / "SKILL.md").read_text()
    routing = (SKILL / "references" / "routing-policy.md").read_text()
    assert "Luna Max is the default execution tier" in skill
    assert "Terra is an exception lane for unresolved complex technical deltas" in skill
    assert "Sol High is a selective judgment or review tier" in skill
    assert "main -> Luna -> Sol -> main" in routing
    assert "never required" in routing


def test_runtime_observation_is_demand_driven_not_universal_overhead():
    routing = (SKILL / "references" / "routing-policy.md").read_text()
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    assert "Runtime observation is demand-driven" in routing
    assert "Do not inspect rollout data for every routine child" in runtime


def test_delegation_contract_records_decision_rights_and_evidence_state():
    contract = (SKILL / "references" / "delegation-contract.md").read_text()
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    for section in ["OUTCOME", "SCOPE", "INVARIANTS", "DECISION RIGHTS", "ACCEPTANCE ORACLE", "VERIFICATION"]:
        assert section in contract
    assert "Shared Evidence State" in contract
    assert "unresolved_delta" in contract
    assert "Child reports are claims" in safety
    assert "independently inspectable artifacts and evidence" in safety


def test_sol_review_is_selective_and_terra_is_delta_investigation():
    routing = (SKILL / "references" / "routing-policy.md").read_text()
    receipt = (SKILL / "references" / "orchestration-receipt.md").read_text()
    assert "Terra is not a mandatory reviewer" in routing
    assert "Sol is the high-value judgment resource" in routing
    assert "Luna + Sol example" in receipt
    assert "Delta-escalation example" in receipt


def test_behavioral_read_only_never_claims_runtime_enforcement():
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    assert "Behavioral read-only is allowed only when all of these conditions hold" in safety
    assert "permission_guarantee = instruction_enforced" in safety
    assert "Do not upgrade behavioral read-only to `runtime_enforced`" in safety


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
