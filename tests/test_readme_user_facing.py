from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text()
EN = (ROOT / "README_EN.md").read_text()


def test_readmes_present_the_same_product_and_install_path():
    for text in [ZH, EN]:
        for phrase in [
            "Codex Delegate",
            "0.6.0",
            "codex plugin marketplace add R-jed/codex-agent-team --ref main",
            "codex plugin marketplace upgrade codex-agent-team",
            "codex plugin add codex-agent-team@codex-agent-team",
            "/codex-delegate",
            "Luna Reader",
            "Luna Worker",
            "Terra Investigator",
            "Sol Advisor",
        ]:
            assert phrase in text
    assert "## 最终复核" in ZH
    assert "## Final Review Gate" in EN


def test_readmes_are_release_copy_not_internal_release_notes():
    assert "启动 Subagent 很容易，难的是判断什么时候值得用" in ZH
    assert "Starting a Subagent is easy. Knowing when one will actually help is harder" in EN
    assert "Codex 原生 Subagents" in ZH
    assert "Codex Native Subagents" in EN

    for text in [ZH, EN]:
        lower = text.lower()
        for forbidden in [
            "HEADOFF.md",
            "LOCAL_VALIDATION_REPORT.md",
            "Checkpoint 1",
            "Checkpoint 5",
            "P0/P1",
            "CAT-LOCAL-001",
            "status-pre--v1",
            "review_artifact_id",
        ]:
            assert forbidden not in text
        for forbidden in [
            "pre-v1",
            "release validation",
            "live pending",
            "ready frontier",
            "intervention gate",
            "recovery ledger",
        ]:
            assert forbidden not in lower


def test_chinese_readme_localizes_generic_engineering_terms():
    for forbidden in [
        "Codex Native Subagents",
        "Codex thread",
        " child",
        "physical checkout",
        "worktree",
        "workspace",
        "routing proxy",
        "Installer",
        "Agent profile",
        "Final Review Gate",
        "Agent runtime",
        "actual diff",
    ]:
        assert forbidden not in ZH

    for required in [
        "Codex 原生 Subagents",
        "Codex 会话",
        "子 Agent",
        "实际 Git 工作副本",
        "工作区",
        "路由代理",
        "安装程序",
        "Agent 配置文件",
        "最终复核",
        "Agent 运行时",
        "实际改动",
    ]:
        assert required in ZH


def test_readmes_explain_that_users_do_not_manually_orchestrate_agents():
    assert "你不需要手工设计并发计划" in ZH
    assert "You do not need to design the concurrency plan yourself" in EN
    assert "目标、不能破坏的约束和完成标准" in ZH
    assert "outcome, the constraints that must remain true, and the completion criteria" in EN


def test_readmes_explain_adaptive_parallel_work_without_fixed_team_shape():
    assert "不要求固定的 Agent 队伍" in ZH
    assert "does not force every task into a fixed Agent team" in EN
    assert "B 解锁了 C" in ZH
    assert "B unlocks C" in EN
    assert "两个有明确理由的子 Agent" in ZH
    assert "up to two justified child Agents" in EN
    assert "实际 Git 工作副本" in ZH
    assert "physical checkout" in EN

    for forbidden in [
        "默认：1 个",
        "一般最多：2 个",
        "硬上限：4 个",
        "default: 1",
        "normal maximum: 2",
        "hard maximum: 4",
    ]:
        assert forbidden not in ZH
        assert forbidden not in EN


def test_readmes_keep_local_recovery_and_risk_triggered_final_review():
    assert "一次失败不会自动触发更强模型，也不会让整个任务从头再来" in ZH
    assert "One failed attempt does not automatically trigger a stronger model or restart the whole task" in EN
    assert "Sol 并非每个任务的固定最后一步" in ZH
    assert "Sol is not a mandatory final step for every task" in EN

    for text in [ZH, EN]:
        for phrase in ["ship", "fix-first", "rethink"]:
            assert phrase in text


def test_readmes_keep_custom_agent_install_scope_user_facing():
    assert "安装程序只管理 Codex Delegate 自己的四个配置文件" in ZH
    assert "installer manages only the four Codex Delegate profiles" in EN
    assert "不修改凭据、MCP、仓库、`config.toml` 或其他 Agent 配置文件" in ZH
    assert "does not modify credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles" in EN


def test_readme_visual_assets_remain_intentional_and_bounded():
    for text in [ZH, EN]:
        assert "<picture" in text
        assert "logo" in text
        for line in text.splitlines():
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
