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
CANONICAL_MARKETPLACE = "codex plugin marketplace add R-jed/codex-delegate@main"
PLUGIN_ADD = "codex plugin add codex-delegate@codex-delegate"
UPGRADE = "codex plugin marketplace upgrade codex-delegate"


def test_plugin_manifest_and_marketplace_use_canonical_identity():
    payload = json.loads(PLUGIN.read_text())
    assert payload["name"] == "codex-delegate"
    assert payload["version"] == "1.1.0"
    assert payload["skills"] == "./skills/"
    assert payload["repository"] == "https://github.com/R-jed/codex-delegate"
    assert payload["homepage"] == "https://github.com/R-jed/codex-delegate#readme"
    assert payload["interface"]["displayName"] == "Codex Delegate"
    assert payload["interface"]["websiteURL"] == "https://github.com/R-jed/codex-delegate"
    assert SKILL.is_dir()

    market = json.loads(MARKETPLACE.read_text())
    assert market["name"] == "codex-delegate"
    assert market["plugins"] == [
        {
            "name": "codex-delegate",
            "source": {"source": "local", "path": "./plugins/codex-delegate"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }
    ]


def test_plugin_brand_assets_and_supported_components():
    payload = json.loads(PLUGIN.read_text())
    interface = payload["interface"]
    assert interface["brandColor"] == "#2563EB"
    for field in ["composerIcon", "logo", "logoDark"]:
        asset = PLUGIN_ROOT / interface[field].removeprefix("./")
        assert asset.is_file() and "<svg" in asset.read_text()
    for unsupported in ["agents", "hooks", "mcpServers", "apps"]:
        assert unsupported not in payload
    for field in ["homepage", "repository"]:
        parsed = urlparse(payload[field])
        assert parsed.scheme == "https" and parsed.netloc


def test_only_current_five_profiles_are_packaged():
    policy = json.loads(POLICY.read_text())
    assert policy["schema_version"] == 4
    assert set(policy["roles"]) == {"reader", "worker", "solver", "investigator", "advisor"}
    expected = {spec["profile_file"] for spec in policy["roles"].values()}
    assert len(expected) == 5
    assert {p.name for p in (PLUGIN_ROOT / "agent-profiles").glob("*.toml")} == expected
    assert all(name.startswith("codex-delegate-") for name in expected)
    assert all(spec["agent_type"].startswith("codex_delegate_") for spec in policy["roles"].values())
    assert policy["roles"]["solver"]["profile_file"] == "codex-delegate-solver.toml"


def test_third_party_mit_notice_is_packaged_without_source_pointer():
    notice = PLUGIN_ROOT / "THIRD_PARTY_NOTICES.md"
    assert notice.is_file()
    text = notice.read_text()
    for phrase in [
        "MIT-licensed third-party material",
        "Copyright (c) 2026 Zhijian AI / Dapeng",
        "Permission is hereby granted",
        "THE SOFTWARE IS PROVIDED \"AS IS\"",
    ]:
        assert phrase in text
    assert "github.com/" not in text
    assert "upstream revision" not in text


def test_skill_owns_current_profile_setup_before_delegated_execution():
    text = (SKILL / "SKILL.md").read_text()
    assert "../../scripts/install-agents.py" in text
    assert 'python "$installer" --check' in text
    assert ".codex-delegate-agents.json" in text
    assert "$codex-delegate:codex-delegate" in text
    assert "native custom-Agent TOML mechanism" in text
    assert "Complete readiness before delegated execution" in text
    assert "stop before delegated code execution" in text
    assert not (ROOT / "scripts" / "install.py").exists()
    assert not (ROOT / "scripts" / "doctor.py").exists()


def test_install_doc_locks_canonical_git_marketplace_fingerprint():
    text = INSTALL_DOC.read_text()
    for phrase in [
        "Normal installation",
        CANONICAL_MARKETPLACE,
        "--sparse .agents/plugins",
        "--sparse plugins/codex-delegate",
        PLUGIN_ADD,
        UPGRADE,
        "Canonical marketplace source",
        "Codex treats the Git source, ref, and sparse paths as part of marketplace source identity",
        "Source conflict repair",
        "codex plugin marketplace list --json",
        "codex plugin marketplace remove codex-delegate",
        "New users and users already on the canonical source do not need the remove step",
        "$codex-delegate:codex-delegate",
        "Repo marketplace id: codex-delegate",
        "codex_delegate_reader",
        "codex_delegate_solver",
        ".codex-delegate-agents.json",
        "First-use Agent readiness",
        "Implicit invocation is disabled",
        "public directory listing exists",
    ]:
        assert phrase in text
    assert "Version:" in text and "1.1.0" in text
    assert "--ref main" not in text


def test_readmes_and_ai_reference_share_streamlined_install_path():
    directive = "If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly."
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text()
        assert directive in text
        assert "1.1.0" in text
        assert "Sol Solver" in text
        assert "$codex-delegate:codex-delegate" in text
        assert CANONICAL_MARKETPLACE in text
        assert "--sparse .agents/plugins" in text
        assert "--sparse plugins/codex-delegate" in text
        assert PLUGIN_ADD in text
        assert UPGRADE in text
        assert "codex plugin marketplace remove codex-delegate" not in text

    ai = (ROOT / "README_AI.md").read_text()
    assert "Current version:     1.1.0" in ai
    assert "Repo marketplace id: codex-delegate" in ai
    assert "Explicit invocation: $codex-delegate:codex-delegate" in ai
    assert "Distribution:        Codex Plugin via canonical Git marketplace" in ai
    assert "codex_delegate_solver" in ai
    assert "codex-delegate-solver.toml" in ai
    assert "codex_delegate_advisor" in ai
    assert CANONICAL_MARKETPLACE in ai
    assert "Do not ask a normal user to remove the marketplace first" in ai
    assert "no project-level ordinary numeric child ceiling" in ai
