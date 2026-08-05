from __future__ import annotations

import json
import os
import re
import subprocess
import tomllib
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-delegate"
MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "codex-delegate"
OPENAI_YAML = SKILL_ROOT / "agents" / "openai.yaml"
OFFICIAL_INVOCATION = "$codex-delegate"
RETIRED_SLASH_INVOCATION = "/" + "codex-delegate"
RETIRED_SLASH_PATTERN = re.compile(r"(?<![A-Za-z0-9_./-])/codex-delegate(?=\s|<|`|[\"']|$)")


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / os.fsdecode(raw) for raw in result.stdout.split(b"\0") if raw]


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


def test_plugin_starter_prompts_use_official_skill_invocation():
    prompts = json.loads(MANIFEST.read_text())["interface"]["defaultPrompt"]
    assert 1 <= len(prompts) <= 3
    assert all(OFFICIAL_INVOCATION in prompt for prompt in prompts)
    assert all(RETIRED_SLASH_INVOCATION not in prompt for prompt in prompts)
    assert all(len(prompt) <= 128 for prompt in prompts)


def test_openai_skill_metadata_uses_explicit_dollar_invocation():
    payload = yaml.safe_load(OPENAI_YAML.read_text())
    interface = payload["interface"]
    assert 25 <= len(interface["short_description"]) <= 64
    assert OFFICIAL_INVOCATION in interface["default_prompt"]
    assert payload["policy"]["allow_implicit_invocation"] is False


def test_retired_custom_slash_invocation_is_absent_from_tracked_tree():
    violations = []
    for path in tracked_paths():
        if path.is_symlink():
            text = os.readlink(path)
        else:
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
        if RETIRED_SLASH_PATTERN.search(text):
            violations.append(path.relative_to(ROOT).as_posix())
    assert not violations, f"Retired custom slash invocation remains: {violations}"


def test_managed_agent_profiles_follow_native_custom_agent_shape():
    policy = json.loads((PLUGIN_ROOT / "policy-contract.json").read_text())
    profile_dir = PLUGIN_ROOT / "agent-profiles"
    for role in policy["roles"].values():
        payload = tomllib.loads((profile_dir / role["profile_file"]).read_text())
        assert payload["name"] == role["agent_type"]
        assert isinstance(payload["description"], str) and payload["description"].strip()
        assert isinstance(payload["developer_instructions"], str) and payload["developer_instructions"].strip()
        assert payload["model"] == role["model"]
        assert payload["model_reasoning_effort"] == role["effort"]
        assert payload["sandbox_mode"] == role["sandbox_intent"]
