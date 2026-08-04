from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"


def test_runtime_evidence_is_typed_and_partial_is_not_proof():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    for field in ["route_evidence", "ancestry_evidence", "permission_evidence"]:
        assert field in runtime
    for grade in [
        "C1_configuration_only",
        "L1_local_record_observed",
        "R1_runtime_reported",
        "R2_runtime_reported_and_local_record_agree",
        "X0_conflicted",
    ]:
        assert grade in runtime
    assert "partial record never earns" in runtime


def test_profile_locked_is_only_route_assurance_and_verifier_is_current():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    routing = (SKILL / "references" / "routing-policy.md").read_text()
    assert "profile_locked" in runtime and "profile_locked" in routing
    assert "native_explicit_validated" not in runtime + routing
    assert "There is no Portable Mode" in routing
    assert (PLUGIN / "scripts" / "runtime-evidence.py").is_file()
    assert "codex_delegate_worker" in runtime


def test_consent_and_live_eval_boundaries_remain():
    consent = (SKILL / "references" / "consent-policy.md").read_text()
    for phrase in [
        "up to 2 concurrently active justified child Agents",
        "at most 1 active writer",
        "The exact team shape is dynamic",
        "does not add another numerical hard ceiling",
    ]:
        assert phrase in consent
    docs = (ROOT / "docs" / "behavioral-evals.md").read_text()
    assert "controlled live runs" in docs
    assert "raw_prompt_luna" in docs
    assert "contract_luna_final_review_gate" in docs


def test_profile_lifecycle_is_current_only():
    installation = (ROOT / "docs" / "plugin-installation.md").read_text()
    skill = (SKILL / "SKILL.md").read_text()
    assert "codex_delegate_worker" in installation
    assert ".codex-delegate-agents.json" in installation
    assert "leaves unrelated Agent profiles untouched" in installation
    assert "Other Agent profiles are user-owned and must remain untouched" in skill
