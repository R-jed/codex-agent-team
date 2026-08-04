from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = (ROOT / "HEADOFF.md").read_text()
REPORT = (ROOT / "LOCAL_VALIDATION_REPORT.md").read_text()


def test_handoff_is_finite_six_checkpoint_release_contract():
    assert "finite live-validation" in HANDOFF
    for n in range(1, 7):
        assert f"## Checkpoint {n}:" in HANDOFF
    assert "Do not add Checkpoint 7" in HANDOFF
    assert "Definition of Done for v1.0.0" in HANDOFF
    assert "tag `v1.0.0`" in HANDOFF


def test_handoff_uses_only_current_roles_as_runtime_targets():
    for role in ["codex_delegate_reader", "codex_delegate_worker", "codex_delegate_investigator", "codex_delegate_advisor"]:
        assert role in HANDOFF
    assert ".codex-delegate-agents.json" in HANDOFF
    assert "old `codex_agent_team_*`" in HANDOFF
    assert "migration inputs only" in HANDOFF
    assert "Do not restore them as current fallback roles" in HANDOFF


def test_handoff_keeps_core_live_gates():
    for phrase in ["barrier_only | per_child_terminal | any_child_update", "A = slow independent dependency", "M3 different sessions, same canonical physical checkout", "I1 two installers target the same clean CODEX_HOME", "INSUFFICIENT_EVIDENCE", "review_artifact_id", "no product hard four-child ceiling"]:
        assert phrase in HANDOFF


def test_handoff_keeps_exact_adversarial_consultation_target():
    for phrase in ["/gpt56-sol-pro-consult", "TARGET_CHATGPT_CONVERSATION_TITLE: 分支 · 分支 · 项目对比分析", "TARGET_MODE: continue_existing_conversation", "MATCH_POLICY: exact_title_unique_match", "CONSULTATION_TARGET_UNRESOLVED"]:
        assert phrase in HANDOFF


def test_report_is_evidence_ledger_for_07_identity_closure():
    for phrase in ["Plugin version: 0.7.0", "codex_delegate_reader", ".codex-delegate-agents.json", "HOLD FOR RELEASE / LIVE VALIDATION PENDING", "Static validation for this exact 0.7.0 tree is pending", "分支 · 分支 · 项目对比分析"]:
        assert phrase in REPORT
    assert "public users and ai agents should use readme/readme_ai" in REPORT.lower()
