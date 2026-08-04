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
            "$CODEX_HOME/agents",
            "Luna Reader",
            "Luna Worker",
            "Terra Investigator",
            "Sol Advisor",
            "Final Review Gate",
            "review_artifact_id",
        ]:
            assert phrase in text


def test_readmes_keep_user_facing_product_positioning():
    assert "Codex Native Subagents 之上的委派策略层" in ZH
    assert "a delegation policy layer over Codex Native Subagents" in EN
    assert "委派框架" not in ZH
    assert "delegation framework" not in EN.lower()

    for forbidden in [
        "HEADOFF.md",
        "LOCAL_VALIDATION_REPORT.md",
        "Checkpoint 1",
        "Checkpoint 5",
        "P0/P1",
        "CAT-LOCAL-001",
        "branch audit",
        "本地真测交接",
        "远端分支清理",
        "静态收口",
    ]:
        assert forbidden not in ZH
        assert forbidden not in EN


def test_readmes_explain_user_does_not_manually_schedule_agents():
    assert "用户不需要手工告诉 Codex" in ZH
    assert "Users should not have to manually tell Codex" in EN
    assert "目标、不能破坏的约束和成功标准" in ZH
    assert "outcome, constraints that must remain true, and observable success criteria" in EN


def test_readmes_explain_completion_driven_concurrency_without_hard_team_size():
    assert "没有固定 Agent 数量" in ZH
    assert "No fixed Agent count" in EN
    assert "completion-driven" in ZH
    assert "completion-driven" in EN
    assert "立即补位" in ZH
    assert "refill immediately" in EN
    assert "join dependency" in ZH
    assert "join dependency" in EN
    assert "最多两个同时活跃" in ZH
    assert "up to two concurrently active" in EN
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


def test_readmes_do_not_shift_performance_responsibility_to_prompt_wording():
    assert "性能主要取决于怎么写 prompt" in ZH
    assert "说法不够完整" in ZH
    assert "performance is not determined mainly by prompt wording" in EN
    assert "任务本身是否存在独立依赖" in ZH
    assert "whether the task actually contains independent dependencies" in EN
    assert "Native Codex" in ZH and "native Codex runtime" in EN


def test_readmes_keep_recovery_and_risk_triggered_final_review_semantics():
    assert "未通过验收和需要改变执行方式是两个不同判断" in ZH
    assert "Failing acceptance and needing to change execution are separate decisions" in EN
    assert "Recovery Ledger" in ZH and "Recovery Ledger" in EN
    assert "固定重试次数" in ZH
    assert "fixed retry count" in EN

    for text in [ZH, EN]:
        for phrase in [
            "Candidate Ready",
            "ship",
            "fix-first",
            "rethink",
            "INSUFFICIENT_EVIDENCE",
            "review_artifact_id",
        ]:
            assert phrase in text
    assert "Sol 不是所有任务的固定阶段" in ZH
    assert "Sol is not a fixed stage for every task" in EN


def test_readmes_explain_plugin_and_custom_agent_boundary():
    assert "Plugin manifest 不声明不存在的 `agents` 组件" in ZH
    assert "Plugin manifest does not invent an `agents` component" in EN


def test_readme_visual_assets_remain_intentional_and_bounded():
    for text in [ZH, EN]:
        assert "<picture" in text
        assert "logo" in text
        for line in text.splitlines():
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
