import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text(encoding="utf-8")
EN = (ROOT / "README_EN.md").read_text(encoding="utf-8")
AI = (ROOT / "README_AI.md").read_text(encoding="utf-8")
EVALS = (ROOT / "evals" / "README.md").read_text(encoding="utf-8")
MANIFEST = json.loads((ROOT / "plugins" / "subagents-dispatch" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
VERSION = MANIFEST["version"]
DIRECTIVE_EN = "If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly."
DIRECTIVE_ZH = "如果你是 AI Agent，请跳转到 [README_AI.md](README_AI.md) 并严格按照说明操作。"
CANONICAL_MARKETPLACE = "codex plugin marketplace add R-jed/subagents-dispatch"
PLUGIN_ADD = "codex plugin add subagents-dispatch@subagents-dispatch"
UPGRADE = "codex plugin marketplace upgrade subagents-dispatch"
MAIN_SKILL = "/subagents-dispatch:dispatch"
DOCTOR_SKILL = "/subagents-dispatch:doctor"
ROLE_LABELS = ["Luna Reader", "Luna Worker", "Sol Solver", "Terra Investigator", "Sol Advisor"]
LIGHT_LOGO = "plugins/subagents-dispatch/assets/subagents-dispatch-logo.svg#gh-light-mode-only"
DARK_LOGO = "plugins/subagents-dispatch/assets/subagents-dispatch-logo-dark.svg#gh-dark-mode-only"


def test_public_readmes_keep_product_identity_install_use_and_update():
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

    assert "## 安装" in ZH and "## 使用" in ZH and "## 更新" in ZH
    assert "## Install" in EN and "## Quick start" in EN and "## Update" in EN


def test_public_readmes_explain_the_current_repository_layout():
    assert "## 项目结构" in ZH
    assert "## Repository layout" in EN
    for text in [ZH, EN]:
        for path in [
            ".agents/plugins/",
            "plugins/subagents-dispatch/",
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
        assert "│       ├── dispatch/" in text
        assert "│       └── doctor/" in text


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


def test_ai_reference_is_an_index_to_canonical_policy_owners():
    for phrase in [
        "R-jed/subagents-dispatch",
        "Repo marketplace id: subagents-dispatch",
        "Main invocation:     /subagents-dispatch:dispatch",
        "Doctor invocation:   /subagents-dispatch:doctor",
        f"Current version:     {VERSION}",
        "Distribution:        Codex Plugin",
        "subagents_dispatch_reader",
        "subagents_dispatch_worker",
        "subagents_dispatch_solver",
        "subagents_dispatch_investigator",
        "subagents_dispatch_advisor",
        "router-core.md",
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
        "runtime-assurance-cases.json",
        "do not control how the plugin routes or coordinates work",
        "router-core.md",
        "team-plan.md",
        "recovery.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json",
    ]:
        assert phrase in EVALS


def test_public_readme_visual_surface_uses_canonical_plugin_assets():
    plugin_assets = ROOT / "plugins" / "subagents-dispatch" / "assets"
    assert (plugin_assets / "subagents-dispatch-logo.svg").is_file()
    assert (plugin_assets / "subagents-dispatch-logo-dark.svg").is_file()
    assert not (ROOT / "docs" / "logo-light.svg").exists()
    assert not (ROOT / "docs" / "logo-dark.svg").exists()

    for text in [ZH, EN]:
        assert "<picture" not in text
        assert LIGHT_LOGO in text
        assert DARK_LOGO in text
        assert "docs/logo-" not in text
        for line in text.splitlines():
            if "<img" in line and "subagents-dispatch-logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
