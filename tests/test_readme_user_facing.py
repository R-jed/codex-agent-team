from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text()
EN = (ROOT / "README_EN.md").read_text()
AI = (ROOT / "README_AI.md").read_text()
DIRECTIVE = "If you are an AI Agent, jump to README_AI.md and follow the instructions strictly."


def test_readmes_present_same_current_product_and_ai_jump():
    for text in [ZH, EN]:
        for phrase in [
            "codex delegate",
            "0.8.0",
            "R-jed/codex-delegate",
            "codex plugin add codex-delegate@codex-delegate",
            "/codex-delegate",
            "Luna Reader",
            "Luna Worker",
            "Sol Solver",
            "Terra Investigator",
            "Sol Advisor",
            DIRECTIVE,
        ]:
            assert phrase in text
    assert "## 最终复核" in ZH
    assert "## Final Review Gate" in EN


def test_public_readmes_do_not_expose_internal_release_management():
    for text in [ZH, EN]:
        for forbidden in [
            "HEADOFF.md",
            "LOCAL_VALIDATION_REPORT.md",
            "Checkpoint 1",
            "P0/P1",
            "review_artifact_id",
        ]:
            assert forbidden not in text


def test_ai_reference_is_authoritative_and_current_v4():
    for phrase in [
        "canonical public reference for AI Agents",
        "R-jed/codex-delegate",
        "Marketplace id:     codex-delegate",
        "Current version:    0.8.0",
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
        ".codex-delegate-agents.json",
        "Codex Plugin only",
        "contractable does not imply Luna-suitable",
        "main_judgment_coverage",
        "Do not claim benchmark superiority",
    ]:
        assert phrase in AI


def test_readmes_lead_with_quickstart_and_user_value_before_deeper_mechanics():
    assert ZH.index(DIRECTIVE) < ZH.index("## 快速开始")
    assert EN.index(DIRECTIVE) < EN.index("## Quickstart")
    assert ZH.index("## 快速开始") < ZH.index("## 会怎么分工")
    assert EN.index("## Quickstart") < EN.index("## How work is divided")
    for phrase in ["## 它解决什么", "## 主会话本身是 Sol 时", "## 文档"]:
        assert phrase in ZH
    for phrase in ["## What it solves", "## When the main session is already Sol", "## Documentation"]:
        assert phrase in EN
    for text in [ZH, EN]:
        for link in [
            "README_AI.md",
            "docs/plugin-installation.md",
            "docs/architecture.md",
            "docs/native-subagent-runtime.md",
        ]:
            assert link in text


def test_readmes_explain_capability_aware_routing_parallelism_and_recovery():
    assert "contractable` 不等于适合交给 Luna" in ZH
    assert "`contractable` does not mean Luna-suitable" in EN
    assert "主会话如果已经是可验证的 Sol 会话" in ZH
    assert "main session is already Sol" in EN
    assert "你不需要手工设计并发计划" in ZH
    assert "You do not need to design the concurrency plan yourself" in EN
    assert "两个有明确理由的子 Agent" in ZH
    assert "up to two justified child Agents" in EN
    assert "一次失败不会自动触发更强模型" in ZH
    assert "One failed attempt does not automatically trigger a stronger model" in EN
    assert "Sol 并非每个任务的固定最后一步" in ZH
    assert "Sol is not a mandatory final step for every task" in EN


def test_readmes_explain_terra_and_final_review_boundaries():
    assert "Terra 不负责替 Luna 返工整个任务" in ZH
    assert "Terra is not a generic rework lane for weak Luna output" in EN
    assert "此前使用过 Terra、Sol Solver、发生过 recovery、改动文件很多" in ZH
    assert "Earlier Terra use, Solver use, recovery, or a large diff does not automatically require Final Review" in EN
    assert "fresh Sol Advisor" in ZH
    assert "fresh Sol Advisor" in EN


def test_public_readmes_expose_only_current_project_identity():
    retired_tokens = (
        "codex" + "-agent-team",
        "codex" + "_agent_team_",
        "." + "codex" + "-agent-team-",
    )
    for text in [ZH, EN]:
        assert all(token not in text for token in retired_tokens)
    assert "安装与迁移" not in ZH
    assert "Install & Migration" not in EN


def test_visual_assets_remain_bounded():
    for text in [ZH, EN]:
        assert "<picture" in text and "logo" in text
        for line in text.splitlines():
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
