from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-agent-team"
SKILL = PLUGIN / "skills" / "codex-agent-team"
RUNTIME_VERIFIER = PLUGIN / "scripts" / "runtime-evidence.py"


def load_cases() -> dict:
    return json.loads((ROOT / "evals" / "runtime-assurance-cases.json").read_text())


def test_runtime_assurance_reference_and_normalized_verifier_are_installed():
    runtime = SKILL / "references" / "runtime-assurance.md"
    skill = (SKILL / "SKILL.md").read_text()
    assert runtime.is_file()
    assert RUNTIME_VERIFIER.is_file()
    assert "references/runtime-assurance.md" in skill
    assert "runtime-evidence.py" in runtime.read_text()
    assert "runtime-evidence.py" in skill
    assert not (SKILL / "scripts" / "inspect-runtime.py").exists()


def test_compute_lanes_have_distinct_responsibilities_not_fixed_order():
    skill = (SKILL / "SKILL.md").read_text()
    routing = (SKILL / "references" / "routing-policy.md").read_text()
    combined = skill + routing
    assert "Luna" in combined and "bounded" in combined
    assert "Terra" in combined and "unresolved" in combined and "technical delta" in combined
    assert "Sol" in combined and "selective" in combined and "judgment" in combined
    assert "main -> Luna -> Sol -> main" in routing
    assert "never required" in routing
    assert "no product-level hard child count" in routing.lower()


def test_runtime_observation_is_demand_driven_not_universal_overhead():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    assert "Do not demand runtime telemetry for every routine child" in runtime
    assert "Ordinary bounded work may proceed" in runtime
    assert "when post-spawn route identity" in (SKILL / "references" / "routing-policy.md").read_text().lower()


def test_delegation_contract_records_decision_rights_and_evidence_schema():
    contract = (SKILL / "references" / "delegation-contract.md").read_text()
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    for section in [
        "DEPENDENCY",
        "OUTCOME",
        "SCOPE",
        "INVARIANTS",
        "DECISION RIGHTS",
        "ACCEPTANCE ORACLE",
        "VERIFICATION",
    ]:
        assert section in contract
    assert "type: deterministic | repository_fact | model_judgment" in contract
    assert "unresolved_delta" in contract
    assert "Child reports are claims" in safety
    assert "inspectable artifacts and evidence" in safety


def test_sol_is_selective_and_terra_is_delta_investigation():
    routing = (SKILL / "references" / "routing-policy.md").read_text()
    receipt = (SKILL / "references" / "orchestration-receipt.md").read_text()
    assert "Terra is not a mandatory reviewer" in routing
    assert "Sol handles bounded consequential judgment or independent review" in routing
    assert "Sol is not globally mandatory" in routing
    assert "Luna + Sol example" in receipt
    assert "Delta-escalation example" in receipt


def test_behavioral_read_only_never_claims_runtime_enforcement():
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    assert "Behavioral read-only is allowed only when hard host isolation is not required" in safety
    assert "permission_guarantee = instruction_enforced" in safety
    assert "Do not relabel behavioral read-only as `runtime_enforced`" in safety


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
