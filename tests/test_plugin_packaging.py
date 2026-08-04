from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
PLUGIN = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
MAIN_SKILL = PLUGIN_ROOT / "skills" / "codex-agent-team"
INSTALL_DOC = ROOT / "docs" / "plugin-installation.md"
POLICY_CONTRACT = PLUGIN_ROOT / "policy-contract.json"


def test_plugin_manifest_packages_single_canonical_skill_tree():
    payload = json.loads(PLUGIN.read_text())
    assert payload["name"] == "codex-agent-team"
    assert PLUGIN_ROOT.name == payload["name"]
    assert payload["version"] == "0.6.0"
    assert payload["skills"] == "./skills/"
    assert payload["license"] == "MIT"
    assert payload["author"]["name"] == "R-jed"
    assert payload["interface"]["displayName"] == "Codex Delegate"
    assert {"Read", "Write"} <= set(payload["interface"]["capabilities"])
    assert "Codex Delegate" in payload["description"]
    assert "dependency-driven" in payload["description"]
    assert "intervention gate" in payload["description"].lower()
    assert "final review" in payload["description"].lower()
    assert MAIN_SKILL.is_dir()
    assert sorted(path.name for path in (PLUGIN_ROOT / "skills").iterdir() if path.is_dir()) == ["codex-agent-team"]
    assert POLICY_CONTRACT.is_file()
    assert (PLUGIN_ROOT / "scripts" / "install-agents.py").is_file()
    assert (PLUGIN_ROOT / "scripts" / "review-artifact.py").is_file()
    assert (PLUGIN_ROOT / "scripts" / "runtime-evidence.py").is_file()


def test_machine_readable_policy_contract_is_bundled_and_versioned():
    payload = json.loads(POLICY_CONTRACT.read_text())
    assert payload["schema_version"] == 1
    assert set(payload["roles"]) == {"reader", "worker", "investigator", "advisor"}
    assert payload["delegation"]["max_depth"] == 1
    assert payload["delegation"]["baseline_concurrent_children"] == 2
    assert payload["delegation"]["max_active_writers_per_workspace"] == 1
    assert payload["final_review"]["completion_verdicts"] == ["ship", "fix-first", "rethink"]


def test_plugin_manifest_default_prompts_are_bounded_and_use_canonical_entrypoint():
    payload = json.loads(PLUGIN.read_text())
    prompts = payload["interface"]["defaultPrompt"]
    assert 1 <= len(prompts) <= 3
    for prompt in prompts:
        assert "/codex-delegate" in prompt
        assert len(prompt) <= 128


def test_plugin_manifest_urls_are_https_and_unsupported_components_are_absent():
    payload = json.loads(PLUGIN.read_text())
    for field in ["homepage", "repository"]:
        parsed = urlparse(payload[field])
        assert parsed.scheme == "https"
        assert parsed.netloc
    for field in ["websiteURL", "privacyPolicyURL", "termsOfServiceURL"]:
        value = payload.get("interface", {}).get(field) or payload.get(field)
        if value:
            parsed = urlparse(value)
            assert parsed.scheme == "https"
            assert parsed.netloc
    for unsupported in ["agents", "hooks"]:
        assert unsupported not in payload


def test_plugin_packages_only_current_semantic_profiles():
    expected = {spec["profile_file"] for spec in json.loads(POLICY_CONTRACT.read_text())["roles"].values()}
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
    assert plugin["policy"]["authentication"] == "ON_INSTALL"
    assert plugin["category"] == "Productivity"
    assert plugin["source"]["path"].startswith("./")


def test_main_skill_owns_first_run_profile_setup_and_receipts():
    text = (MAIN_SKILL / "SKILL.md").read_text()
    assert "## 3. Ensure the exact role is available" in text
    assert "Custom Agent profiles are a Codex configuration surface" in text
    assert "active Codex-home `agents` directory" in text
    assert "../../scripts/install-agents.py" in text
    assert 'python "$installer" --check' in text
    assert "/codex-delegate" in text
    assert "codex-agent-team-setup" not in text
    assert "references/orchestration-receipt.md" in text
    assert "references/execution-progress.md" in text
    assert "references/final-review-gate.md" in text
    assert "runtime-evidence.py" in text
    receipt = (MAIN_SKILL / "references" / "orchestration-receipt.md").read_text()
    assert "Codex Delegate: Main session only" in receipt
    assert "Adaptive parallel example" in receipt
    assert "Clean-restart example" in receipt
    assert "Policy-transform example" in receipt
    assert "Required Final Review Gate example" in receipt


def test_repository_has_no_standalone_or_setup_install_surface():
    assert not (ROOT / "scripts" / "install.py").exists()
    assert not (ROOT / "scripts" / "doctor.py").exists()
    assert not (ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team-setup").exists()
    assert not (ROOT / "skill" / "codex-agent-team").exists()


def test_install_docs_use_cli_marketplace_and_plugin_lifecycle_without_manual_config_edits():
    text = INSTALL_DOC.read_text()
    assert "codex plugin marketplace add R-jed/codex-agent-team --ref main" in text
    assert "--sparse .agents/plugins" in text
    assert "--sparse plugins/codex-agent-team" in text
    assert "codex plugin marketplace upgrade codex-agent-team" in text
    assert "codex plugin add codex-agent-team@codex-agent-team" in text
    assert "new Codex thread" in text
    assert "~/.codex/agents" in text
    assert "active Codex-home `agents` directory" in text
    assert "does not claim a native `agents` component" in text
    assert "manually editing `config.toml`" in text
    assert "scripts/validate_plugin.py" in text
    assert "Version 0.6.0" in text
    assert "Final Review Gate" in text
    assert "review_artifact_id" in text


def test_readmes_expose_plugin_only_single_command_path():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    for text in [zh, en]:
        assert "codex plugin marketplace add R-jed/codex-agent-team --ref main" in text
        assert "--sparse .agents/plugins" in text
        assert "--sparse plugins/codex-agent-team" in text
        assert "codex plugin add codex-agent-team@codex-agent-team" in text
        assert "/codex-delegate" in text
        assert "Codex Delegate" in text
        assert "docs/plugin-installation.md" in text
        assert "0.6.0" in text
        assert "Final Review Gate" in text
        assert "codex-agent-team-setup" not in text
        assert "python scripts/install.py" not in text
    assert "Plugin" in zh
    assert "new Codex thread" in en
