from __future__ import annotations

import json
import tomllib
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-delegate"
MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "codex-delegate"
OPENAI_YAML = SKILL_ROOT / "agents" / "openai.yaml"
POLICY = PLUGIN_ROOT / "policy-contract.json"
CANONICAL_INVOCATION = "$codex-delegate:codex-delegate"


def test_plugin_manifest_has_public_legal_links_and_stays_skills_only():
    payload = json.loads(MANIFEST.read_text())
    interface = payload["interface"]
    assert payload["name"] == "codex-delegate"
    assert payload["skills"] == "./skills/"
    for unsupported_component in ["mcpServers", "apps", "hooks"]:
        assert unsupported_component not in payload
    for field, suffix in [
        ("privacyPolicyURL", "/PRIVACY.md"),
        ("termsOfServiceURL", "/TERMS.md"),
    ]:
        parsed = urlparse(interface[field])
        assert parsed.scheme == "https" and parsed.netloc
        assert parsed.path.endswith(suffix)
    assert (ROOT / "PRIVACY.md").is_file()
    assert (ROOT / "TERMS.md").is_file()


def test_plugin_starter_prompts_use_the_current_explicit_invocation():
    prompts = json.loads(MANIFEST.read_text())["interface"]["defaultPrompt"]
    assert 1 <= len(prompts) <= 3
    assert all(CANONICAL_INVOCATION in prompt for prompt in prompts)
    assert all(len(prompt) <= 128 for prompt in prompts)


def test_openai_skill_metadata_uses_the_current_explicit_invocation():
    payload = yaml.safe_load(OPENAI_YAML.read_text())
    interface = payload["interface"]
    assert 25 <= len(interface["short_description"]) <= 64
    assert CANONICAL_INVOCATION in interface["default_prompt"]
    assert payload["policy"]["allow_implicit_invocation"] is False


def test_managed_agent_profiles_follow_policy_owned_native_shape():
    policy = json.loads(POLICY.read_text())
    profile_dir = PLUGIN_ROOT / "agent-profiles"
    for role in policy["roles"].values():
        payload = tomllib.loads((profile_dir / role["profile_file"]).read_text())
        assert payload["name"] == role["agent_type"]
        assert isinstance(payload["description"], str) and payload["description"].strip()
        assert isinstance(payload["developer_instructions"], str) and payload["developer_instructions"].strip()
        assert payload["model"] == role["model"]
        assert payload["model_reasoning_effort"] == role["effort"]
        assert payload["sandbox_mode"] == role["sandbox_intent"]
