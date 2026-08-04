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
            "Final Review Gate",
        ]:
            assert phrase in text


def test_readmes_are_release_copy_not_internal_release_notes():
    assert "Codex Delegate 让 Codex 在复杂开发任务里更会分工" in ZH
    assert "Codex Delegate helps Codex divide complex development work more effectively" in EN
    assert "Codex Native Subagents" in ZH and "Codex Native Subagents" in EN

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


def test_readmes_explain_that_users_do_not_manually_orchestrate_agents():
    assert "你不需要自己决定“这里开几个 Agent”或“这个问题该交给哪一个模型”" in ZH
    assert "You should not have to decide how many Agents to start or which model should own each step" in EN
    assert "目标、不能破坏的约束和完成标准" in ZH
    assert "outcome, the constraints that must remain true, and the completion criteria" in EN


def test_readmes_explain_adaptive_parallel_work_without_fixed_team_shape():
    assert "不要求固定的 Agent 队伍" in ZH
    assert "does not force every task into a fixed Agent team" in EN
    assert "B 解锁了 C" in ZH
    assert "B unlocks C" in EN
    assert "最多两个有明确理由的 child" in ZH
    assert "up to two justified child Agents" in EN
    assert "physical checkout" in ZH and "physical checkout" in EN

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
    assert "不会因为一次失败就机械地换更强模型或从头重跑" in ZH
    assert "does not switch to a stronger model or restart the whole task just because one attempt fails" in EN
    assert "Sol 不是每个任务的固定最后一步" in ZH
    assert "Sol is not a mandatory final step for every task" in EN

    for text in [ZH, EN]:
        for phrase in ["ship", "fix-first", "rethink"]:
            assert phrase in text


def test_readmes_keep_custom_agent_install_scope_user_facing():
    assert "Installer 只管理 Codex Delegate 自己的四个 profile" in ZH
    assert "installer manages only the four Codex Delegate profiles" in EN
    assert "不修改凭据、MCP、仓库、`config.toml` 或其他 Agent profile" in ZH
    assert "does not modify credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles" in EN


def test_readme_visual_assets_remain_intentional_and_bounded():
    for text in [ZH, EN]:
        assert "<picture" in text
        assert "logo" in text
        for line in text.splitlines():
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
