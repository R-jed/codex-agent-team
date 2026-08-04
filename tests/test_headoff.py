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


def test_handoff_requires_deterministic_execution_preflight_before_live_evidence():
    for phrase in [
        "## Deterministic execution preflight",
        "python -m pytest tests/test_identity_cleanup.py -q",
        "tests/test_runtime_evidence.py",
        "tests/test_behavioral_evals.py",
        "python -m pytest -q",
        "complete pytest suite has no failures or errors",
        "both required Plugin validator runs pass",
        "tested SHA remains unchanged after validation",
        "Do not carry forward a green result from an earlier SHA",
        "LOCAL_VALIDATION_REPORT.md",
    ]:
        assert phrase in HANDOFF
    assert HANDOFF.index("## Deterministic execution preflight") < HANDOFF.index("## Checkpoint 1:")


def test_handoff_uses_five_current_roles_and_routing_v4():
    for role in [
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
    ]:
        assert role in HANDOFF
    for phrase in [
        "version: 0.8.0",
        "Routing V4",
        "contractable` does not imply Luna-suitable",
        "JUDGMENT_REQUIRED",
        "TECHNICAL_GAP",
        "unknown main-session model does not automatically route routine work to Sol",
        ".codex-delegate-agents.json",
    ]:
        assert phrase in HANDOFF


def test_handoff_keeps_core_runtime_and_behavioral_gates():
    for phrase in [
        "barrier_only | per_child_terminal | any_child_update",
        "A = slow independent dependency",
        "M3 different sessions, same canonical physical checkout",
        "M5 Worker + Solver proposed concurrently in same checkout",
        "I1 two installers target the same clean CODEX_HOME",
        "INSUFFICIENT_EVIDENCE",
        "review_artifact_id",
        "advisor_then_luna vs sol_solver",
        "main_session_only vs sol_solver",
        "process-history negative control",
    ]:
        assert phrase.lower() in HANDOFF.lower()


def test_handoff_keeps_exact_adversarial_consultation_target():
    for phrase in [
        "/gpt56-sol-pro-consult",
        f"TARGET_CHATGPT_CONVERSATION_TITLE: {CONSULTATION_TARGET}",
        "TARGET_MODE: continue_existing_conversation",
        "MATCH_POLICY: exact_title_unique_match",
        "CONSULTATION_TARGET_UNRESOLVED",
    ]:
        assert phrase in HANDOFF


def test_report_is_pending_evidence_ledger_for_routing_v4():
    for phrase in [
        "Plugin version: 0.8.0",
        "codex_delegate_reader",
        "codex_delegate_solver",
        ".codex-delegate-agents.json",
        "ROUTING V4 IMPLEMENTED / VALIDATION PENDING",
        "DETERMINISTIC + LIVE V4 VALIDATION PENDING",
        "Static validation for the exact current tree is pending",
        "policy schema 2 / routing-eval schema 4.0",
        "Sol Solver improves or simplifies non-Sol judgment-coupled execution | hypothesis only",
        CONSULTATION_TARGET,
    ]:
        assert phrase in REPORT
    assert "public users and ai agents should use readme/readme_ai" in REPORT.lower()
    assert "pytest passed" in REPORT
    assert "should be interpreted as `pytest passed`" in REPORT
