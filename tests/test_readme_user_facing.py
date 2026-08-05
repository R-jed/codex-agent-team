from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text()
EN = (ROOT / "README_EN.md").read_text()
AI = (ROOT / "README_AI.md").read_text()
EVALS = (ROOT / "evals" / "README.md").read_text()
ALL_READMES = [path.read_text() for path in ROOT.rglob("README*.md")]
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


def test_public_readmes_use_marketplace_first_installation_update_and_official_skill_invocation():
    assert "Codex 中打开**插件市场**" in ZH
    assert "搜索 `codex-delegate`" in ZH
    assert "Open the **Codex Plugin Marketplace**" in EN
    assert "search for `codex-delegate`" in EN
    assert "$codex-delegate" in ZH and "/skills" in ZH
    assert "$codex-delegate" in EN and "/skills" in EN
    assert "后续更新同样直接通过 Codex 插件市场完成" in ZH
    assert "Future updates are handled through the Codex Plugin Marketplace as well" in EN
    for text in [ZH, EN]:
        assert "codex plugin marketplace add" not in text
        assert "codex plugin add codex-delegate@codex-delegate" not in text
    assert "开发安装、手动安装或排障" in ZH
    assert "development installs, manual installs, or troubleshooting" in EN


def test_all_readmes_are_release_ready_product_surfaces_not_status_ledgers():
    forbidden = [
        "HEADOFF.md",
        "LOCAL_VALIDATION_REPORT.md",
        "validation pending",
        "hold for release",
        "pre-release",
        "pre release",
        "release candidate",
        "release posture:",
        "ready for checkpoint",
        "checkpoint 1",
        "checkpoint 2",
        "checkpoint 3",
        "checkpoint 4",
        "checkpoint 5",
        "checkpoint 6",
        "known open reproducible project",
        "P0/P1",
        "review_artifact_id",
    ]
    for text in ALL_READMES:
        lowered = text.lower()
        for phrase in forbidden:
            assert phrase.lower() not in lowered


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
        "For ordinary users, updates should be handled through the Codex Plugin Marketplace",
    ]:
        assert phrase in AI


def test_evals_readme_stays_measurement_only_and_does_not_expose_release_status():
    for phrase in [
        "maintainer-facing measurement and regression surface",
        "does not define the runtime router",
        "router-core.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json",
        "../docs/behavioral-evals.md",
    ]:
        assert phrase in EVALS


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
    for text in ALL_READMES:
        assert all(token not in text for token in retired_tokens)
    assert "安装与迁移" not in ZH
    assert "Install & Migration" not in EN


def test_visual_assets_remain_bounded():
    for text in [ZH, EN]:
        assert "<picture" in text and "logo" in text
        for line in text.splitlines():
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
