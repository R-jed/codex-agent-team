from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
POLICY = PLUGIN / "policy-contract.json"


def test_runtime_evidence_is_diagnostic_not_default_hot_path():
    guardrails = (SKILL / "references" / "guardrails.md").read_text()
    router = (SKILL / "references" / "router-core.md").read_text()
    assert "Runtime evidence is on demand" in guardrails
    assert "Do not run runtime-evidence diagnostics for every ordinary child" in guardrails
    assert "Main-session Sol dedup is an optimization" in router
    assert "Missing telemetry is allowed to remain missing" in router


def test_runtime_verifier_supports_main_and_child_subjects_and_policy_reference():
    verifier = (PLUGIN / "scripts" / "runtime-evidence.py").read_text()
    policy = json.loads(POLICY.read_text())
    assert 'subject == "main_session"' in verifier
    assert 'subject == "child"' in verifier
    assert "load_main_coverage_policy" in verifier
    assert policy["capability_dedup"]["reference_role"] == "solver"
    assert 'coverage = "unknown"' in verifier
    assert "quarantine_main_route_claim" in verifier


def test_exact_project_roles_have_no_cross_role_fallback():
    policy = json.loads(POLICY.read_text())
    skill = (SKILL / "SKILL.md").read_text()
    assert "Exact role mismatch fails closed" in skill
    assert set(spec["agent_type"] for spec in policy["roles"].values()) == {
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
    }


def test_consent_writer_and_explicit_invocation_are_guardrail_owned():
    guardrails = (SKILL / "references" / "guardrails.md").read_text()
    for phrase in [
        "Project policy does not impose an ordinary numeric child ceiling",
        "Child count by itself is not a consent trigger",
        "One writer per canonical checkout",
        "main session when mutating the checkout",
        "Explicit invocation only",
    ]:
        assert phrase in guardrails

    openai = (SKILL / "agents" / "openai.yaml").read_text()
    assert "allow_implicit_invocation: false" in openai


def test_first_use_readiness_occurs_before_delegated_execution():
    guardrails = (SKILL / "references" / "guardrails.md").read_text()
    skill = (SKILL / "SKILL.md").read_text()
    assert "First-use readiness before delegated execution" in guardrails
    assert "stop before delegated code execution" in skill
    assert "ensure required native roles are ready before delegated execution" in skill.lower()


def test_profile_lifecycle_comes_from_policy_and_installer_not_user_docs():
    policy = json.loads(POLICY.read_text())
    profiles = PLUGIN / "agent-profiles"
    installer = (PLUGIN / "scripts" / "install-agents.py").read_text()
    expected_files = {spec["profile_file"] for spec in policy["roles"].values()}
    assert {path.name for path in profiles.glob("*.toml")} == expected_files
    assert 'MANIFEST_NAME = ".codex-delegate-agents.json"' in installer
    assert 'LOCK_NAME = ".codex-delegate-agents.lock"' in installer
    assert "policy-contract.json" in installer


def test_process_history_is_not_a_final_review_trigger():
    final_review = (SKILL / "references" / "final-review.md").read_text()
    for phrase in ["Terra use", "Solver use", "recovery", "a large diff"]:
        assert phrase in final_review
    assert "is not a trigger by itself" in final_review


def test_behavioral_evals_remain_measurement_not_runtime_policy():
    docs = (ROOT / "docs" / "behavioral-evals.md").read_text().lower()
    for phrase in [
        "controlled paired workloads",
        "measurement surface",
        "experiment labels only",
    ]:
        assert phrase in docs
