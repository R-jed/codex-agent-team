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
    assert payload["skills"] == "./skills/"
    assert payload["license"] == "MIT"
    assert payload["interface"]["displayName"] == "Codex Agent Team"
    assert {"Read", "Write"} <= set(payload["interface"]["capabilities"])
    assert "/codex-agent-team" in payload["interface"]["longDescription"]
    assert MAIN_SKILL.is_dir()
    assert sorted(path.name for path in (PLUGIN_ROOT / "skills").iterdir() if path.is_dir()) == [
        "codex-agent-team"
    ]
    assert (PLUGIN_ROOT / "scripts" / "install-agents.py").is_file()
    assert (PLUGIN_ROOT / "agent-profiles" / "luna-worker.toml").is_file()


def test_repository_marketplace_points_at_nested_plugin_root():
    payload = json.loads(MARKETPLACE.read_text())
    assert payload["name"] == "codex-agent-team"
    assert len(payload["plugins"]) == 1
    plugin = payload["plugins"][0]
    assert plugin["name"] == "codex-agent-team"
    assert plugin["source"] == {
        "source": "local",
        "path": "./plugins/codex-agent-team",
    }
    assert plugin["policy"]["installation"] == "AVAILABLE"
    assert not (ROOT / ".codex-plugin" / "plugin.json").exists()


def test_main_skill_owns_first_run_profile_setup_and_receipts():
    text = (MAIN_SKILL / "SKILL.md").read_text()
    assert "Agent Profile Readiness Gate" in text
    assert "../../scripts/install-agents.py" in text
    assert 'python "$installer" --check' in text
    assert "/codex-agent-team" in text
    assert "codex-agent-team-setup" not in text
    assert "references/orchestration-receipt.md" in text
    receipt = (MAIN_SKILL / "references" / "orchestration-receipt.md").read_text()
    assert "/codex-agent-team" in receipt
    assert "$codex-agent-team" not in receipt
    assert "Agent Team: Main session only" in receipt
    assert "Root only" not in receipt
    assert "Do not claim runtime evidence that was not observed" in receipt


def test_repository_has_no_standalone_or_setup_install_surface():
    assert not (ROOT / "scripts" / "install.py").exists()
    assert not (ROOT / "scripts" / "doctor.py").exists()
    assert not (ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team-setup").exists()
    assert not (ROOT / "skill" / "codex-agent-team").exists()
    assert not (ROOT / "examples" / "agents").exists()


def test_readmes_expose_plugin_only_single_command_path():
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text()
        assert "codex plugin marketplace add R-jed/codex-agent-team --ref main" in text
        assert "Plugins Directory" in text
        assert "/codex-agent-team" in text
        assert "codex-agent-team-setup" not in text
        assert "python scripts/install.py" not in text
        assert "--skill-only" not in text
        assert "Agent Team: Main session only" in text
