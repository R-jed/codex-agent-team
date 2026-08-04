from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"


def test_runtime_evidence_is_typed_and_main_coverage_is_conservative():
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
    for phrase in [
        "main_judgment_coverage",
        "covered",
        "uncovered",
        "unknown",
        "local-only",
        "Main-session coverage is used only to avoid redundant capability-uplift Sol calls",
    ]:
        assert phrase in runtime


def test_runtime_verifier_supports_main_and_child_subjects_and_policy_reference():
    verifier = (PLUGIN / "scripts" / "runtime-evidence.py").read_text()
    policy = (PLUGIN / "policy-contract.json").read_text()
    assert 'subject == "main_session"' in verifier
    assert 'subject == "child"' in verifier
    assert "JUDGMENT_REFERENCE_MODEL = load_judgment_reference_model()" in verifier
    assert "main_coverage_reference_role" in verifier
    assert '"main_coverage_reference_role": "solver"' in policy
    assert 'coverage = "unknown"' in verifier
    assert "quarantine_main_route_claim" in verifier
    assert 'SOL_MODEL_PREFIX = "gpt-5.6-sol"' not in verifier


def test_exact_project_roles_have_no_cross_role_fallback():
    routing = (SKILL / "references" / "routing-policy.md").read_text()
    skill = (SKILL / "SKILL.md").read_text()
    for role in [
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
    ]:
        assert role in skill or role in routing
    assert "Exact-route mismatch fails closed" in skill
    assert "Do not cross-route" in skill
    assert (PLUGIN / "scripts" / "runtime-evidence.py").is_file()


def test_consent_and_live_eval_boundaries_remain_distinct():
    consent = (SKILL / "references" / "consent-policy.md").read_text()
    for phrase in [
        "up to 2 concurrently active justified child Agents",
        "at most 1 active writing project Agent",
        "Material compute expansion",
        "Do not spend Sol merely because the baseline permits it",
    ]:
        assert phrase in consent

    docs = (ROOT / "docs" / "behavioral-evals.md").read_text()
    for phrase in [
        "paired live workloads",
        "raw_prompt_luna",
        "bounded_luna",
        "advisor_then_luna",
        "sol_solver",
        "Process-history negative control",
    ]:
        assert phrase.lower() in docs.lower()


def test_writer_safety_covers_worker_and_solver():
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    assert "codex_delegate_worker" in safety
    assert "codex_delegate_solver" in safety
    assert "one active writing project Agent" in safety
    assert "Multiple writing Agents require genuine filesystem isolation" in safety


def test_profile_lifecycle_is_current_only_and_five_role():
    installation = (ROOT / "docs" / "plugin-installation.md").read_text()
    ai = (ROOT / "README_AI.md").read_text()
    for role in [
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
    ]:
        assert role in installation
        assert role in ai
    assert ".codex-delegate-agents.json" in installation
    assert "leaves unrelated Agent profiles untouched" in installation


def test_process_history_is_not_a_final_review_trigger():
    final_review = (SKILL / "references" / "final-review-gate.md").read_text()
    for phrase in [
        "Terra was used",
        "Sol Solver was used",
        "a clean restart happened",
        "material recovery happened",
        "the diff is large",
    ]:
        assert phrase in final_review
    assert "do **not** make review mandatory by themselves" in final_review
