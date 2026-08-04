from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text()
EN = (ROOT / "README_EN.md").read_text()
AI = (ROOT / "README_AI.md").read_text()
DIRECTIVE = "If you are an AI Agent, jump to README_AI.md and follow the instructions strictly."


def test_readmes_present_same_current_product_and_ai_jump():
    for text in [ZH, EN]:
        for phrase in ["codex delegate", "0.7.0", "R-jed/codex-delegate", "codex plugin add codex-delegate@codex-delegate", "/codex-delegate", "Luna Reader", "Luna Worker", "Terra Investigator", "Sol Advisor", DIRECTIVE]:
            assert phrase in text
    assert "## 最终复核" in ZH
    assert "## Final Review Gate" in EN


def test_public_readmes_do_not_expose_internal_release_management():
    for text in [ZH, EN]:
        for forbidden in ["HEADOFF.md", "LOCAL_VALIDATION_REPORT.md", "Checkpoint 1", "P0/P1", "review_artifact_id"]:
            assert forbidden not in text


def test_ai_reference_is_authoritative_and_current():
    for phrase in [
        "canonical public reference for AI Agents",
        "R-jed/codex-delegate",
        "Marketplace id:     codex-delegate",
        "Current version:    0.7.0",
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
        ".codex-delegate-agents.json",
        "Codex Plugin only",
        "Do not claim benchmark superiority",
    ]:
        assert phrase in AI
    assert "Do not present `codex-agent-team`" in AI
    assert "historical migration inputs only" in AI


def test_readmes_explain_adaptive_parallelism_and_recovery():
    assert "你不需要手工设计并发计划" in ZH
    assert "You do not need to design the concurrency plan yourself" in EN
    assert "两个有明确理由的子 Agent" in ZH
    assert "up to two justified child Agents" in EN
    assert "一次失败不会自动触发更强模型" in ZH
    assert "One failed attempt does not automatically trigger a stronger model" in EN
    assert "Sol 并非每个任务的固定最后一步" in ZH
    assert "Sol is not a mandatory final step for every task" in EN


def test_legacy_public_id_is_migration_context_only_in_public_readmes():
    for text in [ZH, EN]:
        assert "codex-agent-team" in text
        assert "codex plugin add codex-agent-team@codex-agent-team" not in text
        assert "--sparse plugins/codex-agent-team" not in text
        assert "codex_agent_team_" not in text
        assert ".codex-agent-team-" not in text


def test_visual_assets_remain_bounded():
    for text in [ZH, EN]:
        assert "<picture" in text and "logo" in text
        for line in text.splitlines():
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
