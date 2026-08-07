import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text(encoding="utf-8")
EN = (ROOT / "README_EN.md").read_text(encoding="utf-8")
AI = (ROOT / "README_AI.md").read_text(encoding="utf-8")
EVALS = (ROOT / "evals" / "README.md").read_text(encoding="utf-8")
MANIFEST = json.loads((ROOT / "plugins" / "codex-delegate" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
VERSION = MANIFEST["version"]
DIRECTIVE = "If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly."
CANONICAL_MARKETPLACE = "codex plugin marketplace add R-jed/codex-delegate@main"
PLUGIN_ADD = "codex plugin add codex-delegate@codex-delegate"
UPGRADE = "codex plugin marketplace upgrade codex-delegate"
ROLE_LABELS = ["Luna Reader", "Luna Worker", "Sol Solver", "Terra Investigator", "Sol Advisor"]
LIGHT_LOGO = "plugins/codex-delegate/assets/codex-delegate-logo.svg#gh-light-mode-only"
DARK_LOGO = "plugins/codex-delegate/assets/codex-delegate-logo-dark.svg#gh-dark-mode-only"


def test_public_readmes_keep_product_identity_install_use_and_update():
    for text in [ZH, EN]:
        assert "codex delegate" in text
        assert VERSION in text
        assert DIRECTIVE in text
        assert "$codex-delegate:codex-delegate" in text
        assert "/plugins" in text
        assert "/skills" in text
        assert CANONICAL_MARKETPLACE in text
        assert "--sparse .agents/plugins" in text
        assert "--sparse plugins/codex-delegate" in text
        assert PLUGIN_ADD in text
        assert UPGRADE in text
        assert "--ref main" not in text
        for role in ROLE_LABELS:
            assert role in text

    assert "## 安装" in ZH and "## 开始使用" in ZH and "## 更新" in ZH
    assert "### 方式一：Codex 插件市场" in ZH
    assert "### 方式二：命令行" in ZH
    assert "## Install" in EN and "## Quick start" in EN and "## Update" in EN
    assert "### Option 1: Codex Plugin Marketplace" in EN
    assert "### Option 2: Command line" in EN


def test_public_readmes_explain_the_current_repository_layout():
    assert "## 项目结构" in ZH
    assert "## Repository layout" in EN
    for text in [ZH, EN]:
        for path in [
            ".agents/plugins/",
            "plugins/codex-delegate/",
            "agent-profiles/",
            "policy-contract.json",
            "skills/codex-delegate/",
            "docs/",
            "evals/",
            "scripts/",
            "tests/",
        ]:
            assert path in text


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
        "R-jed/codex-delegate",
        "Repo marketplace id: codex-delegate",
        "Explicit invocation: $codex-delegate:codex-delegate",
        f"Current version:     {VERSION}",
        "Distribution:        Codex Plugin",
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
        "router-core.md",
        "team-plan.md",
        "recovery.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json",
        CANONICAL_MARKETPLACE,
        "--sparse .agents/plugins",
        "--sparse plugins/codex-delegate",
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
    plugin_assets = ROOT / "plugins" / "codex-delegate" / "assets"
    assert (plugin_assets / "codex-delegate-logo.svg").is_file()
    assert (plugin_assets / "codex-delegate-logo-dark.svg").is_file()
    assert not (ROOT / "docs" / "logo-light.svg").exists()
    assert not (ROOT / "docs" / "logo-dark.svg").exists()

    for text in [ZH, EN]:
        assert "<picture" not in text
        assert LIGHT_LOGO in text
        assert DARK_LOGO in text
        assert "docs/logo-" not in text
        for line in text.splitlines():
            if "<img" in line and "codex-delegate-logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
