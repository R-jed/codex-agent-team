from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-delegate"
PLUGIN = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SKILL = PLUGIN_ROOT / "skills" / "codex-delegate"
INSTALL_DOC = ROOT / "docs" / "plugin-installation.md"
POLICY = PLUGIN_ROOT / "policy-contract.json"
EXPECTED_VERSION = "1.2.0"
CANONICAL_MARKETPLACE = "codex plugin marketplace add R-jed/codex-delegate@main"
PLUGIN_ADD = "codex plugin add codex-delegate@codex-delegate"
UPGRADE = "codex plugin marketplace upgrade codex-delegate"


def test_plugin_manifest_and_marketplace_use_canonical_identity():
    payload = json.loads(PLUGIN.read_text(encoding="utf-8"))
    assert payload["name"] == "codex-delegate"
    assert payload["version"] == EXPECTED_VERSION
    assert payload["skills"] == "./skills/"
    assert payload["repository"] == "https://github.com/R-jed/codex-delegate"
    assert payload["homepage"] == "https://github.com/R-jed/codex-delegate#readme"
    assert payload["interface"]["displayName"] == "Codex Delegate"
    assert payload["interface"]["websiteURL"] == "https://github.com/R-jed/codex-delegate"
    assert SKILL.is_dir()

    market = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    assert market == {
        "name": "codex-delegate",
        "interface": {"displayName": "Codex Delegate"},
        "plugins": [
            {
                "name": "codex-delegate",
                "source": {"source": "local", "path": "./plugins/codex-delegate"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }
        ],
    }


def test_plugin_brand_assets_and_supported_components():
    payload = json.loads(PLUGIN.read_text(encoding="utf-8"))
    interface = payload["interface"]
    assert interface["brandColor"] == "#2563EB"
    for field in ["composerIcon", "logo", "logoDark"]:
        asset = PLUGIN_ROOT / interface[field].removeprefix("./")
        assert asset.is_file() and "<svg" in asset.read_text(encoding="utf-8")
    for unsupported in ["agents", "hooks", "mcpServers", "apps"]:
        assert unsupported not in payload
    for field in ["homepage", "repository"]:
        parsed = urlparse(payload[field])
        assert parsed.scheme == "https" and parsed.netloc


def test_policy_contract_owns_the_five_packaged_profiles():
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    assert policy["schema_version"] == 5
    assert set(policy["roles"]) == {"reader", "worker", "solver", "investigator", "advisor"}
    expected = {spec["profile_file"] for spec in policy["roles"].values()}
    assert len(expected) == 5
    assert {p.name for p in (PLUGIN_ROOT / "agent-profiles").glob("*.toml")} == expected
    assert all(name.startswith("codex-delegate-") for name in expected)
    assert all(spec["agent_type"].startswith("codex_delegate_") for spec in policy["roles"].values())


def test_third_party_mit_notice_is_packaged_without_repository_pointer():
    notice = PLUGIN_ROOT / "THIRD_PARTY_NOTICES.md"
    assert notice.is_file()
    text = notice.read_text(encoding="utf-8")
    for phrase in [
        "MIT-licensed third-party material",
        "Copyright (c) 2026 Zhijian AI / Dapeng",
        "Permission is hereby granted",
        "THE SOFTWARE IS PROVIDED \"AS IS\"",
    ]:
        assert phrase in text
    assert "github.com/" not in text


def test_skill_owns_profile_readiness_before_delegated_execution():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "../../scripts/install-agents.py" in text
    assert 'python "$installer"' in text
    assert 'python "$installer" --check' in text
    assert "Exact role mismatch fails closed" in text
    assert "stop before delegated code execution" in text


def test_install_doc_contains_the_two_current_install_and_update_paths():
    text = INSTALL_DOC.read_text(encoding="utf-8")
    for phrase in [
        "Option 1: Codex Plugin Marketplace",
        "Search for `codex-delegate`",
        "/plugins",
        "Option 2: Command-line installation",
        CANONICAL_MARKETPLACE,
        "--sparse .agents/plugins",
        "--sparse plugins/codex-delegate",
        PLUGIN_ADD,
        "## Update",
        UPGRADE,
        "$codex-delegate:codex-delegate",
        "/skills",
    ]:
        assert phrase in text
    assert "--ref main" not in text


def test_readmes_and_ai_reference_share_the_current_install_contract():
    payload = json.loads(PLUGIN.read_text(encoding="utf-8"))
    version = payload["version"]
    for name in ["README.md", "README_EN.md", "README_AI.md"]:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert version in text
        assert "$codex-delegate:codex-delegate" in text
        assert "/plugins" in text
        assert CANONICAL_MARKETPLACE in text
        assert "--sparse .agents/plugins" in text
        assert "--sparse plugins/codex-delegate" in text
        assert PLUGIN_ADD in text
        assert UPGRADE in text
