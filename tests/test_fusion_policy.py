from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "codex-agent-team"


def read(path: str) -> str:
    return (ROOT / path).read_text()


def load_cases() -> dict:
    return json.loads((ROOT / "evals" / "runtime-assurance-cases.json").read_text())


def test_runtime_assurance_reference_is_installed_and_linked():
    runtime = SKILL / "references" / "runtime-assurance.md"
    inspector = SKILL / "scripts" / "inspect-runtime.py"
    skill = (SKILL / "SKILL.md").read_text()

    assert runtime.exists()
    assert inspector.exists()
    assert "references/runtime-assurance.md" in skill
    assert "scripts/inspect-runtime.py" in runtime.read_text()


def test_fusion_keeps_existing_role_separation():
    skill = (SKILL / "SKILL.md").read_text()
    routing = (SKILL / "references" / "routing-policy.md").read_text()

    assert "Luna Max is the default execution route" in skill
    assert "Terra XHigh is the selective independent-judgment route" in skill
    assert "Do not use Terra as a generic difficulty escalation or implementation lane" in routing
    assert "Sol High is a consent-gated Senior Judge" in skill
    assert "Sol is not a mandatory final reviewer" in read("docs/architecture.md")
    assert "The Skill never requires a Sol Root" in routing


def test_runtime_observation_does_not_become_universal_dependency():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    routing = (SKILL / "references" / "routing-policy.md").read_text()

    assert "For ordinary bounded work" in runtime
    assert "missing runtime telemetry may stay `not_exposed`" in routing
    assert "Runtime assurance and review must not increase Agent count by themselves" in routing


def test_worker_report_is_claim_and_implementation_preset_records_judgment_calls():
    packet = (SKILL / "references" / "task-packet.md").read_text()
    safety = (SKILL / "references" / "safety-policy.md").read_text()

    for section in ["OBJECTIVE", "OWNERSHIP", "INTERFACES", "CONSTRAINTS", "VERIFICATION"]:
        assert section in packet
    assert "judgment_calls" in packet
    assert "The Worker report is a claim" in packet
    assert "Worker reports are claims" in safety


def test_review_gate_is_selective_and_root_retains_acceptance():
    skill = (SKILL / "SKILL.md").read_text()
    routing = (SKILL / "references" / "routing-policy.md").read_text()

    assert "Detached review is risk-triggered, not mandatory for every implementation" in skill
    assert "Root still owns acceptance" in skill
    assert "review_status: clear | findings | insufficient_evidence" in routing
    assert "Consent Gate" in routing and "Sol Senior Judge" in routing


def test_behavioral_read_only_never_claims_runtime_enforcement():
    safety = (SKILL / "references" / "safety-policy.md").read_text()

    assert "Behavioral read-only is allowed only when all of these conditions hold" in safety
    assert "permission_guarantee = instruction_enforced" in safety
    assert "Do not upgrade behavioral read-only to `runtime_enforced`" in safety


def test_runtime_and_review_cases_cover_required_regressions():
    payload = load_cases()
    assert payload["schema_version"] == "1.0"
    assert payload["skill_name"] == "codex-agent-team"

    cases = {case["id"]: case for case in payload["cases"]}
    required = {
        "ordinary-route-observation-unavailable",
        "high-consequence-model-independence-unobservable",
        "native-runtime-route-match",
        "native-local-attestation-conflict",
        "required-read-only-unobservable",
        "broadened-reviewer-sandbox-behavioral-readonly",
        "unused-role-unavailable-does-not-block-team",
        "small-mechanical-change-no-detached-review",
        "material-worker-judgment-triggers-review-gate",
        "unresolved-high-consequence-terra-conflict-needs-sol-consent",
    }
    assert required <= set(cases)

    assert cases["ordinary-route-observation-unavailable"]["expected"]["decision"] == "continue"
    assert cases["high-consequence-model-independence-unobservable"]["expected"]["decision"] == "return_to_root"
    assert cases["native-local-attestation-conflict"]["expected"]["decision"] == "quarantine"
    assert cases["unused-role-unavailable-does-not-block-team"]["expected"]["workers"] == ["execution_worker"]
    assert cases["small-mechanical-change-no-detached-review"]["expected"]["independent_critic"] is False
    assert cases["material-worker-judgment-triggers-review-gate"]["expected"]["review_route"] == "gpt-5.6-terra/xhigh"
    assert cases["unresolved-high-consequence-terra-conflict-needs-sol-consent"]["expected"]["decision"] == "ask_consent"
