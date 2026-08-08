import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text(encoding="utf-8")
EN = (ROOT / "README_EN.md").read_text(encoding="utf-8")
AI = (ROOT / "README_AI.md").read_text(encoding="utf-8")
EVALS = (ROOT / "evals" / "README.md").read_text(encoding="utf-8")
MANIFEST = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
VERSION = MANIFEST["version"]
DIRECTIVE_EN = "If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly."
DIRECTIVE_ZH = "如果你是 AI Agent，请跳转到 [README_AI.md](README_AI.md) 并严格按照说明操作。"
CANONICAL_MARKETPLACE = "codex plugin marketplace add R-jed/subagents-dispatch"
PLUGIN_ADD = "codex plugin add subagents-dispatch@subagents-dispatch"
UPGRADE = "codex plugin marketplace upgrade subagents-dispatch"
MAIN_SKILL = "/dispatch"
DOCTOR_SKILL = "/doctor"
MAIN_SKILL_NAMESPACED = "/subagents-dispatch:dispatch"
DOCTOR_SKILL_NAMESPACED = "/subagents-dispatch:doctor"
ROLE_LABELS = ["Luna Reader", "Luna Worker", "Sol Solver", "Terra Investigator", "Sol Advisor"]
CONTROL_FORMS = ["/dispatch preview", "/dispatch status", "/dispatch steer", "/dispatch takeover"]
README_LOGO = "assets/subagents-dispatch-logo.png"


def test_public_readmes_keep_product_identity_install_use_update_and_controls():
    assert "subagents-dispatch" in ZH
    assert VERSION in ZH
    assert DIRECTIVE_ZH in ZH
    assert MAIN_SKILL in ZH
    assert DOCTOR_SKILL in ZH
    assert CANONICAL_MARKETPLACE in ZH
    assert PLUGIN_ADD in ZH
    assert UPGRADE in ZH
    for role in ROLE_LABELS:
        assert role in ZH
    for form in CONTROL_FORMS:
        assert form in ZH

    assert "subagents-dispatch" in EN
    assert VERSION in EN
    assert DIRECTIVE_EN in EN
    assert MAIN_SKILL in EN
    assert DOCTOR_SKILL in EN
    assert CANONICAL_MARKETPLACE in EN
    assert PLUGIN_ADD in EN
    assert UPGRADE in EN
    for role in ROLE_LABELS:
        assert role in EN
    for form in CONTROL_FORMS:
        assert form in EN

    assert "## 安装" in ZH and "## 快速开始" in ZH and "## 更新" in ZH
    assert "## 运行中控制" in ZH and "## 执行摘要" in ZH and "## 减少重复扫描" in ZH
    assert "## Install" in EN and "## Quick start" in EN and "## Update" in EN
    assert "## Control active work" in EN and "## Compact execution receipt" in EN and "## Evidence-bound handoffs" in EN


def test_public_readmes_explain_the_current_repository_layout():
    assert "## 项目结构" in ZH
    assert "## Repository layout" in EN
    for text in [ZH, EN]:
        for path in [
            ".agents/plugins/",
            ".codex-plugin/",
            "agent-profiles/",
            "policy-contract.json",
            "skills/",
            "dispatch/",
            "doctor/",
            "docs/",
            "evals/",
            "scripts/",
            "tests/",
        ]:
            assert path in text
        assert "├── dispatch/" in text
        assert "└── doctor/" in text


def test_public_readmes_keep_runtime_detail_bounded_and_link_deeper_docs():
    for text in [ZH, EN]:
        for link in [
            "README_AI.md",
            "docs/plugin-installation.md",
            "docs/architecture.md",
            "docs/native-subagent-runtime.md",
        ]:
            assert link in text
        assert "review_artifact_id" not in text
        assert "TeamPlan revision" not in text
        assert "failure_origin" not in text
        assert "task_blocker" not in text
        assert "chain-of-thought" not in text.lower()


def test_public_readmes_describe_safe_takeover_receipt_handoff_writer_and_first_run_boundaries():
    for text in [ZH, EN]:
        assert "UNKNOWN" in text
        assert "Handoff Capsule" in text
        assert "Token" in text or "token" in text
    assert "原写入者没有确认停止前" in ZH
    assert "不会根据模型名称或运行时长猜 Token 和费用" in ZH
    assert "同一次 subagents-dispatch 调度内" in ZH
    assert "其他 Codex 会话、编辑器、hook 和外部进程不在这个保证范围内" in ZH
    assert "五个项目 Agent profiles" in ZH
    assert "再开启一次新的 Codex 会话" in ZH
    assert "previous writer is confirmed stopped or terminal" in EN
    assert "does not estimate token usage or currency cost" in EN
    assert "Within one subagents-dispatch orchestration" in EN
    assert "other Codex sessions, editors, hooks, and external processes are outside this guarantee" in EN
    assert "five managed Agent profiles" in EN
    assert "one additional fresh Codex session" in EN


def test_ai_reference_is_an_index_to_canonical_policy_owners():
    for phrase in [
        "R-jed/subagents-dispatch",
        "Repo marketplace id: subagents-dispatch",
        f"User command:        {MAIN_SKILL}",
        f"Internal identity:   {MAIN_SKILL_NAMESPACED}",
        f"Doctor command:      {DOCTOR_SKILL}",
        f"Internal identity:   {DOCTOR_SKILL_NAMESPACED}",
        f"Current version:     {VERSION}",
        "Distribution:        Codex Plugin",
        "subagents_dispatch_reader",
        "subagents_dispatch_worker",
        "subagents_dispatch_solver",
        "subagents_dispatch_investigator",
        "subagents_dispatch_advisor",
        "interaction.md",
        "router-core.md",
        "handoff-capsule.md",
        "team-plan.md",
        "recovery.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json",
        "doctor/SKILL.md",
        CANONICAL_MARKETPLACE,
        PLUGIN_ADD,
        UPGRADE,
    ]:
        assert phrase in AI
    assert "not a second copy of runtime policy" in AI


def test_evals_readme_identifies_measurement_boundary_and_canonical_owners():
    for phrase in [
        "not part of the normal user setup",
        "behavioral-workloads.json",
        "behavioral-result.schema.json",
        "routing-cases.json",
        "coordination-cases.json",
        "interaction-cases.json",
        "runtime-assurance-cases.json",
        "do not control how the plugin routes or coordinates work",
        "interaction.md",
        "router-core.md",
        "handoff-capsule.md",
        "team-plan.md",
        "recovery.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json",
    ]:
        assert phrase in EVALS


def test_public_readme_visual_surface_uses_canonical_plugin_assets():
    plugin_assets = ROOT / "assets"
    assert (plugin_assets / "subagents-dispatch-logo.png").is_file()
    assert (plugin_assets / "subagents-dispatch-logo.svg").is_file()
    assert (plugin_assets / "subagents-dispatch-logo-dark.svg").is_file()
    assert not (ROOT / "docs" / "logo-light.svg").exists()
    assert not (ROOT / "docs" / "logo-dark.svg").exists()

    for text in [ZH, EN]:
        assert "<picture" not in text
        assert README_LOGO in text
        assert "#gh-light-mode-only" not in text
        assert "#gh-dark-mode-only" not in text
        assert "docs/logo-" not in text
        for line in text.splitlines():
            if "<img" in line and "subagents-dispatch-logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
