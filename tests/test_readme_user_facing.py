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
            "0.9.1",
            "$codex-delegate",
            "Luna Reader",
            "Luna Worker",
            "Sol Solver",
            "Terra Investigator",
            "Sol Advisor",
            DIRECTIVE,
        ]:
            assert phrase in text
    assert "## 最终复核" in ZH
    assert "## Final Review" in EN


def test_public_readmes_use_marketplace_first_installation_and_official_skill_invocation():
    assert "Codex 中打开**插件市场**" in ZH
    assert "搜索 `codex-delegate`" in ZH
    assert "Open the **Codex Plugin Marketplace**" in EN
    assert "search for `codex-delegate`" in EN
    assert "$codex-delegate" in ZH and "/skills" in ZH
    assert "$codex-delegate" in EN and "/skills" in EN
    for text in [ZH, EN]:
        assert "codex plugin marketplace add" not in text
        assert "codex plugin add codex-delegate@codex-delegate" not in text
    assert "开发安装、手动安装或排障" in ZH
    assert "development installs, manual installs, or troubleshooting" in EN


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


def test_ai_reference_is_authoritative_and_mechanism_compressed():
    for phrase in [
        "canonical public reference for AI Agents",
        "R-jed/codex-delegate",
        "Marketplace id:     codex-delegate",
        "Explicit invocation: $codex-delegate",
        "Current version:    0.9.1",
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
        ".codex-delegate-agents.json",
        "Codex Plugin only",
        "router-core.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json` schema `3`",
        "Implicit invocation is disabled",
        "Do not claim benchmark superiority",
        "search for `codex-delegate` in the Codex Plugin Marketplace",
        "Tell them to invoke the Skill with `$codex-delegate`",
        "Provide CLI installation commands only for explicit manual/development/troubleshooting requests",
    ]:
        assert phrase in AI


def test_readmes_lead_with_quickstart_and_user_value_before_deeper_mechanics():
    assert ZH.index(DIRECTIVE) < ZH.index("## 快速开始")
    assert EN.index(DIRECTIVE) < EN.index("## Quickstart")
    assert ZH.index("## 快速开始") < ZH.index("## 会怎么分工")
    assert EN.index("## Quickstart") < EN.index("## How work is divided")
    for phrase in ["## 它解决什么", "## 主会话本身已经有足够 Sol 能力时", "## 文档"]:
        assert phrase in ZH
    for phrase in ["## What it solves", "## When the main session already has sufficient Sol capability", "## Documentation"]:
        assert phrase in EN
    for text in [ZH, EN]:
        for link in [
            "README_AI.md",
            "docs/plugin-installation.md",
            "docs/architecture.md",
            "docs/native-subagent-runtime.md",
        ]:
            assert link in text


def test_readmes_explain_explicit_capability_aware_routing_and_recovery():
    assert "插件不会隐式介入普通任务" in ZH
    assert "does not implicitly enter ordinary tasks" in EN
    assert "一个任务能够写出 contract，并不代表适合交给 Luna" in ZH
    assert "A task being contractable does not make it Luna-suitable" in EN
    assert "你不需要手工设计并发计划" in ZH
    assert "You do not need to design the concurrency plan yourself" in EN
    assert "两个有明确理由的子 Agent" in ZH
    assert "up to two justified child Agents" in EN
    assert "一次失败不会自动触发更强模型" in ZH
    assert "One failed attempt does not automatically trigger a stronger model" in EN
    assert "Sol 并非每个任务的固定最后一步" in ZH
    assert "Sol is not a mandatory final step for every task" in EN


def test_readmes_explain_first_use_and_no_default_receipt():
    assert "## 首次使用体验" in ZH
    assert "## First-use experience" in EN
    assert "任何子 Agent 写代码之前" in ZH
    assert "before any child starts writing" in EN
    assert "不会默认追加一份内部 orchestration receipt" in ZH
    assert "do not receive a separate orchestration receipt by default" in EN


def test_readmes_explain_official_model_boundaries_and_final_review():
    assert "Luna 做得不好不会自动触发 Terra" in ZH
    assert "Weak Luna output does not automatically trigger Terra" in EN
    assert "bounded read-heavy" in ZH
    assert "bounded read-heavy" in EN
    assert "真正困难、模糊或需要复杂技术判断的问题进入 Sol 路径" in ZH
    assert "Demanding, ambiguous, or judgment-heavy technical work belongs on the Sol path" in EN
    assert "这些事实本身不会自动触发 Final Review" in ZH
    assert "does not automatically require review" in EN
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
