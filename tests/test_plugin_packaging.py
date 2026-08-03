from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
PLUGIN = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
MAIN_SKILL = PLUGIN_ROOT / "skills" / "codex-agent-team"


def test_plugin_manifest_packages_single_canonical_skill_tree():
    payload = json.loads(PLUGIN.read_text())
    assert payload["name"] == "codex-agent-team"
    assert payload["version"] == "0.5.0"
    assert payload["skills"] == "./skills/"
    assert payload["license"] == "MIT"
    assert payload["interface"]["displayName"] == "Codex Delegate"
    assert {"Read", "Write"} <= set(payload["interface"]["capabilities"])
    assert "Codex Delegate" in payload["description"]
    assert "dependency-driven" in payload["description"]
    assert "fixed Agent counts" in payload["description"]
    assert all("/codex-delegate" in prompt for prompt in payload["interface"]["defaultPrompt"])
    assert MAIN_SKILL.is_dir()
    assert sorted(path.name for path in (PLUGIN_ROOT / "skills").iterdir() if path.is_dir()) == ["codex-agent-team"]
    assert (PLUGIN_ROOT / "scripts" / "install-agents.py").is_file()


def test_plugin_packages_only_current_semantic_profiles():
    expected = {
        "codex-agent-team-reader.toml",
        "codex-agent-team-worker.toml",
        "codex-agent-team-investigator.toml",
        "codex-agent-team-advisor.toml",
    }
    assert {path.name for path in (PLUGIN_ROOT / "agent-profiles").glob("*.toml")} == expected


def test_repository_marketplace_points_at_nested_plugin_root():
    payload = json.loads(MARKETPLACE.read_text())
    assert payload["name"] == "codex-agent-team"
    assert payload["interface"]["displayName"] == "Codex Delegate"
    assert len(payload["plugins"]) == 1
    plugin = payload["plugins"][0]
    assert plugin["name"] == "codex-agent-team"
    assert plugin["source"] == {"source": "local", "path": "./plugins/codex-agent-team"}
    assert plugin["policy"]["installation"] == "AVAILABLE"


def test_main_skill_owns_first_run_profile_setup_and_receipts():
    text = (MAIN_SKILL / "SKILL.md").read_text()
    assert "Agent Profile Readiness" in text
    assert "../../scripts/install-agents.py" in text
    assert 'python "$installer" --check' in text
    assert "/codex-delegate" in text
    assert "codex-agent-team-setup" not in text
    assert "references/orchestration-receipt.md" in text
    assert "references/execution-progress.md" in text
    receipt = (MAIN_SKILL / "references" / "orchestration-receipt.md").read_text()
    assert "Codex Delegate: Main session only" in receipt
    assert "Adaptive parallel example" in receipt
    assert "Clean-restart example" in receipt


def test_repository_has_no_standalone_or_setup_install_surface():
    assert not (ROOT / "scripts" / "install.py").exists()
    assert not (ROOT / "scripts" / "doctor.py").exists()
    assert not (ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team-setup").exists()
    assert not (ROOT / "skill" / "codex-agent-team").exists()


def test_readmes_expose_plugin_only_single_command_path():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    for text in [zh, en]:
        assert "codex plugin marketplace add R-jed/codex-agent-team --ref main" in text
        assert "/codex-delegate" in text
        assert "Codex Delegate" in text
        assert "docs/plugin-installation.md" in text
        assert "codex-agent-team-setup" not in text
        assert "python scripts/install.py" not in text
    assert "插件市场" in zh
    assert "Plugins Directory" in en
