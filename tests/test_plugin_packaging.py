from __future__ import annotations

import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
MAIN_SKILL = ROOT / "skill" / "codex-agent-team"
SETUP_SKILL = ROOT / "skill" / "codex-agent-team-setup"


def test_plugin_manifest_packages_repo_skill_tree_without_copying_policy():
    payload = json.loads(PLUGIN.read_text())
    assert payload["name"] == "codex-agent-team"
    assert payload["skills"] == "./skill/"
    assert payload["license"] == "MIT"
    assert payload["interface"]["displayName"] == "Codex Agent Team"
    assert {"Interactive", "Write"} <= set(payload["interface"]["capabilities"])
    assert MAIN_SKILL.is_dir()
    assert SETUP_SKILL.is_dir()
    assert not (ROOT / "plugins" / "codex-agent-team" / "skills").exists()


def test_repository_marketplace_points_at_repo_plugin_root():
    payload = json.loads(MARKETPLACE.read_text())
    assert payload["name"] == "codex-agent-team"
    assert len(payload["plugins"]) == 1
    plugin = payload["plugins"][0]
    assert plugin["name"] == "codex-agent-team"
    assert plugin["source"] == {"source": "local", "path": "./"}
    assert plugin["policy"]["installation"] == "AVAILABLE"


def test_setup_skill_is_explicit_and_uses_companion_installer():
    text = (SETUP_SKILL / "SKILL.md").read_text()
    metadata = yaml.safe_load((SETUP_SKILL / "agents" / "openai.yaml").read_text())
    assert "../../scripts/install-agents.py" in text
    assert "python \"$installer\" --check" in text
    assert "~/.codex/agents" not in text  # installer owns destination resolution
    assert metadata["policy"]["allow_implicit_invocation"] is False
    assert "$codex-agent-team-setup" in metadata["interface"]["default_prompt"]


def test_main_skill_explains_plugin_agent_setup_and_receipts():
    text = (MAIN_SKILL / "SKILL.md").read_text()
    assert "$codex-agent-team-setup" in text
    assert "Plugin installation alone" in text
    assert "references/orchestration-receipt.md" in text
    receipt = (MAIN_SKILL / "references" / "orchestration-receipt.md").read_text()
    assert "Agent Team: Root only" in receipt
    assert "Do not claim runtime evidence that was not observed" in receipt


def test_readmes_make_plugin_primary_and_keep_standalone_path():
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text()
        assert "codex plugin marketplace add R-jed/codex-agent-team --ref main" in text
        assert "codex plugin add codex-agent-team@codex-agent-team" in text
        assert "$codex-agent-team-setup" in text
        assert "python scripts/install.py" in text
        assert "python scripts/install.py --check" in text
        assert "python scripts/install.py --skill-only" in text
        assert "Agent Team: Root only" in text


def test_setup_skill_frontmatter_is_minimal_and_valid():
    text = (SETUP_SKILL / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match
    frontmatter = yaml.safe_load(match.group(1))
    assert set(frontmatter) == {"name", "description"}
    assert frontmatter["name"] == "codex-agent-team-setup"
