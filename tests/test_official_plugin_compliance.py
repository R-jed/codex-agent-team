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
CANONICAL_INVOCATION = "$codex-delegate:codex-delegate"
RETIRED_SLASH_INVOCATION = r"(?<![A-Za-z0-9_-])" + "/" + "codex-delegate"
RETIRED_SHORT_DOLLAR_INVOCATION = r"\$" + "codex-delegate" + r"(?!:)"
RETIRED_INVOCATION = re.compile(f"(?:{RETIRED_SLASH_INVOCATION}|{RETIRED_SHORT_DOLLAR_INVOCATION})")
EVIDENCE_LEDGERS = {"HEADOFF.md", "LOCAL_VALIDATION_REPORT.md"}


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


def test_plugin_starter_prompts_use_canonical_invocation():
    prompts = json.loads(MANIFEST.read_text())["interface"]["defaultPrompt"]
    assert 1 <= len(prompts) <= 3
    assert all(CANONICAL_INVOCATION in prompt for prompt in prompts)
    assert all(not RETIRED_INVOCATION.search(prompt) for prompt in prompts)
    assert all(len(prompt) <= 128 for prompt in prompts)


def test_openai_skill_metadata_uses_canonical_invocation():
    payload = yaml.safe_load(OPENAI_YAML.read_text())
    interface = payload["interface"]
    assert 25 <= len(interface["short_description"]) <= 64
    assert CANONICAL_INVOCATION in interface["default_prompt"]
    assert not RETIRED_INVOCATION.search(interface["default_prompt"])
    assert payload["policy"]["allow_implicit_invocation"] is False


def test_retired_invocations_are_absent_from_tracked_tree():
    violations = []
    for path in tracked_paths():
        relative = path.relative_to(ROOT).as_posix()
        if relative in EVIDENCE_LEDGERS:
            continue
        if path.is_symlink():
            text = os.readlink(path)
        else:
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
        if RETIRED_INVOCATION.search(text):
            violations.append(relative)
    assert not violations, f"Retired invocation remains: {violations}"


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
