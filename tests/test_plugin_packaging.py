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


def test_plugin_manifest_and_marketplace_use_canonical_identity():
    payload = json.loads(PLUGIN.read_text())
    assert payload["name"] == "codex-delegate"
    assert payload["version"] == "0.8.0"
    assert payload["skills"] == "./skills/"
    assert payload["repository"] == "https://github.com/R-jed/codex-delegate"
    assert payload["homepage"] == "https://github.com/R-jed/codex-delegate#readme"
    assert payload["interface"]["displayName"] == "Codex Delegate"
    assert payload["interface"]["websiteURL"] == "https://github.com/R-jed/codex-delegate"
    assert "judgment-coupled execution" in payload["interface"]["longDescription"]
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
    for unsupported in ["agents", "hooks"]:
        assert unsupported not in payload
    for field in ["homepage", "repository"]:
        parsed = urlparse(payload[field])
        assert parsed.scheme == "https" and parsed.netloc


def test_only_current_five_profiles_are_packaged():
    policy = json.loads(POLICY.read_text())
    assert policy["schema_version"] == 2
    assert set(policy["roles"]) == {"reader", "worker", "solver", "investigator", "advisor"}
    expected = {spec["profile_file"] for spec in policy["roles"].values()}
    assert len(expected) == 5
    assert {p.name for p in (PLUGIN_ROOT / "agent-profiles").glob("*.toml")} == expected
    assert all(name.startswith("codex-delegate-") for name in expected)
    assert all(spec["agent_type"].startswith("codex_delegate_") for spec in policy["roles"].values())
    assert policy["roles"]["solver"]["profile_file"] == "codex-delegate-solver.toml"


def test_skill_owns_current_profile_setup_and_no_standalone_installer_surface():
    text = (SKILL / "SKILL.md").read_text()
    assert "../../scripts/install-agents.py" in text
    assert 'python "$installer" --check' in text
    assert ".codex-delegate-agents.json" in text
    assert "/codex-delegate" in text
    assert "It manages only the current project profiles" in text
    assert not (ROOT / "scripts" / "install.py").exists()
    assert not (ROOT / "scripts" / "doctor.py").exists()


def test_install_doc_explains_current_install_and_five_profile_lifecycle():
    text = INSTALL_DOC.read_text()
    for phrase in [
        "codex plugin marketplace add R-jed/codex-delegate --ref main",
        "--sparse plugins/codex-delegate",
        "codex plugin marketplace upgrade codex-delegate",
        "codex plugin add codex-delegate@codex-delegate",
        "codex_delegate_reader",
        "codex_delegate_solver",
        ".codex-delegate-agents.json",
        "Version:         0.8.0",
        "leaves unrelated Agent profiles untouched",
        "five current profiles",
    ]:
        assert phrase in text


def test_readmes_and_ai_reference_share_current_install_path():
    directive = "If you are an AI Agent, jump to README_AI.md and follow the instructions strictly."
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text()
        assert directive in text
        assert "0.8.0" in text
        assert "Sol Solver" in text
        assert "codex plugin add codex-delegate@codex-delegate" in text
        assert "/codex-delegate" in text
    ai = (ROOT / "README_AI.md").read_text()
    assert "Current version:    0.8.0" in ai
    assert "codex_delegate_solver" in ai
    assert "codex-delegate-solver.toml" in ai
    assert "codex_delegate_advisor" in ai
