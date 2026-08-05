from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = (ROOT / "HEADOFF.md").read_text()
REPORT = (ROOT / "LOCAL_VALIDATION_REPORT.md").read_text()
CONSULTATION_TARGET = "R-jed/codex-delegate"


def test_handoff_is_finite_six_checkpoint_release_contract():
    assert "finite deterministic/live-validation" in HANDOFF
    for n in range(1, 7):
        assert f"## Checkpoint {n}:" in HANDOFF
    assert "Do not add Checkpoint 7" in HANDOFF
    assert "Definition of Done for v1.0.0" in HANDOFF
    assert "tag `v1.0.0`" in HANDOFF


def test_handoff_requires_official_compliance_and_deterministic_execution_before_live_evidence():
    for phrase in [
        "## Deterministic execution preflight",
        "tests/test_official_plugin_compliance.py",
        "python -m pytest tests/test_identity_cleanup.py -q",
        "tests/test_runtime_evidence.py",
        "tests/test_capability_dedup.py",
        "tests/test_behavioral_evals.py",
        "python -m pytest -q",
        "complete pytest suite has no failures or errors",
        "both required Plugin validator runs pass",
        "tested SHA remains unchanged after validation",
        "$codex-delegate",
        "/skills",
        "privacy policy",
        "skills-only",
        "LOCAL_VALIDATION_REPORT.md",
    ]:
        assert phrase in HANDOFF
    assert HANDOFF.index("## Deterministic execution preflight") < HANDOFF.index("## Checkpoint 1:")


def test_handoff_uses_five_roles_and_compact_policy_surface():
    for role in [
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
    ]:
        assert role in HANDOFF
    for phrase in [
        "version: 0.9.1",
        "router-core.md / guardrails.md / final-review.md",
        "policy-contract.json schema 3",
        "invocation: explicit only",
        "contract | judgment | investigation | stalled",
        "ordinary successful tasks do not need a separate orchestration receipt",
        ".codex-delegate-agents.json",
    ]:
        assert phrase in HANDOFF


def test_handoff_terra_is_read_heavy_lane_and_sol_keeps_demanding_judgment():
    for phrase in [
        "Terra is a bounded read-heavy investigation/evidence-synthesis lane",
        "difficult, ambiguous, multi-step technical judgment belongs to capable main/Sol",
        "Terra is not an escalation rung",
        "Luna Reader vs Terra Investigator",
        "demanding/ambiguous technical judgment must go to Sol",
    ]:
        assert phrase.lower() in HANDOFF.lower()


def test_handoff_keeps_daily_runtime_and_behavioral_gates():
    for phrase in [
        "A = slow independent read-only work",
        "M3 different sessions, same canonical physical checkout",
        "M5 Worker + Solver proposed concurrently in same checkout",
        "M6 Main writer + Worker/Solver proposed concurrently in same checkout",
        "I1 two installers target the same clean CODEX_HOME",
        "INSUFFICIENT_EVIDENCE",
        "review_artifact_id",
        "Advisor + Luna handoff vs one Sol Solver",
        "Sol-main direct execution vs redundant Sol Solver",
        "first-use five-profile native custom-Agent provisioning/readiness behavior",
    ]:
        assert phrase.lower() in HANDOFF.lower()


def test_handoff_requires_immutable_release_candidate_for_release_evidence():
    for phrase in [
        "`main` is a moving development ref",
        "fixed immutable RC/tag",
        "immutable candidate SHA/ref",
        "make the immutable release ref the recommended stable user-install channel",
    ]:
        assert phrase in HANDOFF


def test_handoff_keeps_exact_adversarial_consultation_target():
    for phrase in [
        "/gpt56-sol-pro-consult",
        f"TARGET_CHATGPT_CONVERSATION_TITLE: {CONSULTATION_TARGET}",
        "TARGET_MODE: continue_existing_conversation",
        "MATCH_POLICY: exact_title_unique_match",
        "CONSULTATION_TARGET_UNRESOLVED",
    ]:
        assert phrase in HANDOFF


def test_report_is_pending_evidence_ledger_for_officially_aligned_candidate():
    for phrase in [
        "Plugin version: 0.9.1",
        "Canonical explicit invocation: $codex-delegate",
        "codex_delegate_reader",
        "codex_delegate_solver",
        ".codex-delegate-agents.json",
        "policy-contract.json schema 3",
        "MECHANISM COMPRESSION + OFFICIAL CODEX ALIGNMENT IMPLEMENTED / VALIDATION PENDING",
        "DETERMINISTIC + LIVE VALIDATION PENDING",
        "Static validation for the exact current tree is pending",
        "exactly three model-facing runtime references remain",
        "Sol Solver reduces handoff/rework on judgment-coupled implementation | hypothesis only",
        "Terra improves read-heavy stable-semantics investigation at useful cost/quality | hypothesis only",
        CONSULTATION_TARGET,
    ]:
        assert phrase in REPORT
    assert "public users and ai agents should use readme/readme_ai" in REPORT.lower()
    assert "pytest passed" in REPORT
