from pathlib import Path
import json
import re
import tomllib

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
REFS = SKILL / "references"
PROFILES = PLUGIN / "agent-profiles"
POLICY = PLUGIN / "policy-contract.json"


def read(path: str) -> str:
    return (ROOT / path).read_text()


def load_cases():
    return json.loads((ROOT / "evals" / "routing-cases.json").read_text())


def contract():
    return json.loads(POLICY.read_text())


def test_eval_schema_skill_and_openai_interface():
    schema = json.loads((ROOT / "evals" / "routing-case.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(load_cases())
    assert load_cases()["schema_version"] == "3.0"
    assert load_cases()["skill_name"] == "codex-delegate"
    text = (SKILL / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match
    frontmatter = yaml.safe_load(match.group(1))
    assert frontmatter["name"] == "codex-delegate"
    assert "distinct unresolved dependencies" in frontmatter["description"]
    data = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text())
    assert data["interface"]["display_name"] == "Codex Delegate"
    assert "/codex-delegate" in data["interface"]["default_prompt"]


def test_policy_contract_and_profiles_use_only_current_namespace():
    payload = contract()
    assert payload["schema_version"] == 1
    assert payload["delegation"] == {"max_depth": 1, "baseline_concurrent_children": 2, "max_active_writers_per_workspace": 1}
    assert set(payload["roles"]) == {"reader", "worker", "investigator", "advisor"}
    assert {p.name for p in PROFILES.glob("*.toml")} == {spec["profile_file"] for spec in payload["roles"].values()}
    for spec in payload["roles"].values():
        assert spec["profile_file"].startswith("codex-delegate-")
        assert spec["agent_type"].startswith("codex_delegate_")
        profile = tomllib.loads((PROFILES / spec["profile_file"]).read_text())
        assert profile["name"] == spec["agent_type"]
        assert profile["model"] == spec["model"]
        assert profile["model_reasoning_effort"] == spec["effort"]
        assert profile["sandbox_mode"] == spec["sandbox_intent"]
        assert profile["developer_instructions"].strip()


def test_static_cases_use_current_policy_routes_and_unique_dependencies():
    roles = contract()["roles"]
    for case in load_cases()["evals"]:
        ids = []
        for node in case["expected"].get("nodes", []):
            spec = roles[node["responsibility"]]
            assert node["model"] == spec["model"]
            assert node["effort"] == spec["effort"]
            assert node["agent_type"] == spec["agent_type"]
            assert node["route_assurance"] == "profile_locked"
            ids.append(node["dependency_id"])
        assert len(ids) == len(set(ids))


def test_adaptive_orchestration_invariants_remain_explicit():
    routing = (REFS / "routing-policy.md").read_text()
    skill = (SKILL / "SKILL.md").read_text()
    safety = (REFS / "safety-policy.md").read_text()
    consent = (REFS / "consent-policy.md").read_text()
    assert "no product-level hard child count" in routing.lower()
    assert "Luna -> Terra -> Sol" in routing and "never required" in routing
    assert "completion-driven" in routing.lower() and "ready frontier" in routing.lower()
    assert "one active writing Worker" in skill
    assert "Delegation depth" in skill
    assert "Children must not spawn further Subagents" in safety
    assert "up to 2 concurrently active justified child Agents" in consent


def test_runtime_and_final_review_helpers_are_single_current_surface():
    assert (PLUGIN / "scripts" / "runtime-evidence.py").is_file()
    assert (PLUGIN / "scripts" / "review-artifact.py").is_file()
    assert not (SKILL / "scripts" / "inspect-runtime.py").exists()
    runtime = (REFS / "runtime-assurance.md").read_text()
    gate = (REFS / "final-review-gate.md").read_text()
    assert "codex_delegate_worker" in runtime
    assert "codex_delegate_advisor" in gate
    assert "review_artifact_id" in gate
    assert "INSUFFICIENT_EVIDENCE" in gate


def test_architecture_and_runtime_docs_match_current_namespace():
    architecture = read("docs/architecture.md")
    runtime = read("docs/native-subagent-runtime.md")
    for text in [architecture, runtime]:
        assert "codex_delegate_reader" in text
        assert "codex_delegate_worker" in text
        assert "codex_agent_team_" not in text
    assert "plugins/codex-delegate/policy-contract.json" in architecture
    assert "plugins/codex-delegate/scripts/runtime-evidence.py" in architecture
    assert "barrier_only" in runtime and "any_child_update" in runtime


def test_readmes_are_public_docs_and_ai_reference_is_explicit():
    zh = read("README.md")
    en = read("README_EN.md")
    ai = read("README_AI.md")
    directive = "If you are an AI Agent, jump to README_AI.md and follow the instructions strictly."
    for text in [zh, en]:
        assert directive in text
        assert "/codex-delegate" in text
        assert "0.7.0" in text
        assert "HEADOFF.md" not in text
        assert "LOCAL_VALIDATION_REPORT.md" not in text
    assert "codex_delegate_reader" in ai
    assert "codex-delegate-reader.toml" in ai
    assert ".codex-delegate-agents.json" in ai
    assert "Codex Plugin only" in ai


def test_official_install_docs_keep_supported_cli_path_and_migration_boundary():
    installation = read("docs/plugin-installation.md")
    assert "codex plugin marketplace add R-jed/codex-delegate --ref main" in installation
    assert "codex plugin add codex-delegate@codex-delegate" in installation
    assert "codex plugin marketplace upgrade codex-delegate" in installation
    assert "codex plugin remove codex-agent-team@codex-agent-team" in installation
    assert "codex plugin marketplace remove codex-agent-team" in installation
    assert ".codex-delegate-agents.json" in installation
    assert "codex_delegate_worker" in installation
    assert "0.7.0" in installation
