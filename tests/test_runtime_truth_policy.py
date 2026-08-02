from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "codex-agent-team"


def test_evidence_grades_are_explicit_and_local_record_is_not_runtime_proof():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    for grade in [
        "C1_configuration_only",
        "L1_local_record_observed",
        "R1_runtime_reported",
        "R2_runtime_reported_and_local_record_agree",
        "X0_conflicted",
    ]:
        assert grade in runtime
    assert "mutable local Codex rollout record" in runtime
    assert "Reserve stronger terminology such as `runtime_attested`" in runtime


def test_profile_locked_is_documented_as_configuration_only():
    skill = (SKILL / "SKILL.md").read_text().lower()
    route = (ROOT / "docs" / "model-route-assurance.md").read_text().lower()
    assert "profile_locked" in skill
    assert "configuration assurance only" in skill
    assert "profile_locked" in route
    assert "configuration lock" in route
    assert "post-spawn" in route


def test_verifier_is_wired_into_skill_and_policy():
    verifier = SKILL / "scripts" / "verify-runtime.py"
    assert verifier.exists()
    for path in [
        SKILL / "SKILL.md",
        SKILL / "references" / "runtime-assurance.md",
        SKILL / "references" / "routing-policy.md",
        SKILL / "references" / "task-packet.md",
    ]:
        assert "verify-runtime.py" in path.read_text()


def test_depth_one_has_parent_thread_runtime_check():
    skill = (SKILL / "SKILL.md").read_text()
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    packet = (SKILL / "references" / "task-packet.md").read_text()
    assert "parent_thread_id" in skill
    assert "parent_thread_id" in safety
    assert "expected_parent_thread_id" in packet


def test_consent_policy_defines_baseline_envelope():
    consent = (SKILL / "references" / "consent-policy.md").read_text().lower()
    assert "baseline orchestration envelope" in consent
    assert "luna" in consent and "0-1" in consent
    assert "terra" in consent and "at most 1" in consent
    assert "sol senior judge" in consent
    assert "outside the baseline envelope" in consent


def test_live_evals_are_separate_from_static_tests():
    docs = (ROOT / "docs" / "behavioral-evals.md").read_text().lower()
    workloads = (ROOT / "evals" / "behavioral-workloads.json").read_text().lower()
    assert "static repository tests" in docs
    assert "do not prove" in docs and "real" in docs
    assert "no claimed benchmark results" in workloads


def test_doctor_and_compatibility_docs_exist():
    assert (ROOT / "scripts" / "doctor.py").exists()
    compatibility = (ROOT / "docs" / "compatibility.md").read_text().lower()
    assert "requires active codex runtime" in compatibility
    assert "r1_runtime_reported" in compatibility
