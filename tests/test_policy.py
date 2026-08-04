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
    assert load_cases()["schema_version"] == "4.0"
    assert load_cases()["skill_name"] == "codex-delegate"

    text = (SKILL / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match
    frontmatter = yaml.safe_load(match.group(1))
    assert frontmatter["name"] == "codex-delegate"
    assert "classifying unresolved dependencies" in frontmatter["description"]

    data = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text())
    assert data["interface"]["display_name"] == "Codex Delegate"
    assert "/codex-delegate" in data["interface"]["default_prompt"]
    assert "judgment-coupled execution to Sol" in data["interface"]["default_prompt"]


def test_policy_contract_declares_routing_v4_and_exact_profiles():
    payload = contract()
    assert payload["schema_version"] == 2
    assert payload["delegation"] == {
        "max_depth": 1,
        "baseline_concurrent_children": 2,
        "max_active_writers_per_workspace": 1,
    }
    assert payload["classification"]["dependency_kinds"] == [
        "evidence",
        "bounded_execution",
        "judgment",
        "judgment_coupled_execution",
        "technical_investigation",
    ]
    assert payload["classification"]["main_judgment_coverage"] == [
        "covered",
        "uncovered",
        "unknown",
    ]
    assert set(payload["roles"]) == {"reader", "worker", "solver", "investigator", "advisor"}
    assert {p.name for p in PROFILES.glob("*.toml")} == {
        spec["profile_file"] for spec in payload["roles"].values()
    }

    for spec in payload["roles"].values():
        assert spec["profile_file"].startswith("codex-delegate-")
        assert spec["agent_type"].startswith("codex_delegate_")
        profile = tomllib.loads((PROFILES / spec["profile_file"]).read_text())
        assert profile["name"] == spec["agent_type"]
        assert profile["model"] == spec["model"]
        assert profile["model_reasoning_effort"] == spec["effort"]
        assert profile["sandbox_mode"] == spec["sandbox_intent"]
        assert profile["developer_instructions"].strip()

    assert payload["roles"]["worker"]["model"] == "gpt-5.6-luna"
    assert payload["roles"]["solver"]["model"] == "gpt-5.6-sol"
    assert payload["roles"]["solver"]["sandbox_intent"] == "workspace-write"


def test_final_review_contract_is_consequence_driven():
    triggers = set(contract()["final_review"]["trigger_codes"])
    assert triggers == {
        "user_requested",
        "public_contract_change",
        "persistent_state_change",
        "security_boundary",
        "authorization_boundary",
        "data_integrity",
        "concurrency_semantics",
        "migration",
        "verification_gap",
    }
    assert "terra_escalation" not in triggers
    assert "material_recovery" not in triggers
    assert "wide_blast_radius" not in triggers


def test_static_cases_use_current_policy_routes_and_unique_dependencies():
    roles = contract()["roles"]
    cases = load_cases()["evals"]
    assert any(case["expected"].get("dependency_kind") == "judgment_coupled_execution" for case in cases)
    assert any(case["expected"].get("main_judgment_coverage") == "covered" for case in cases)
    assert any(case["expected"].get("main_judgment_coverage") == "unknown" for case in cases)

    for case in cases:
        ids = []
        for node in case["expected"].get("nodes", []):
            spec = roles[node["responsibility"]]
            assert node["model"] == spec["model"]
            assert node["effort"] == spec["effort"]
            assert node["agent_type"] == spec["agent_type"]
            assert node["route_assurance"] == "profile_locked"
            ids.append(node["dependency_id"])
        assert len(ids) == len(set(ids))


def test_routing_v4_has_one_classifier_and_no_model_ladder():
    routing = (REFS / "routing-policy.md").read_text()
    skill = (SKILL / "SKILL.md").read_text()
    progress = (REFS / "execution-progress.md").read_text()

    for phrase in [
        "contractable does not imply Luna-suitable",
        "main-session authority is independent of model identity",
        "main-session judgment coverage is not",
        "judgment_coupled_execution",
        "Reclassification replaces model escalation",
        "process history",
    ]:
        assert phrase.lower() in routing.lower()

    for signal in ["CONTRACT_GAP", "JUDGMENT_REQUIRED", "TECHNICAL_GAP", "EXECUTION_STALL"]:
        assert signal in skill
        assert signal in progress

    assert "capability gap" not in routing.lower()
    assert "mandatory luna -> terra -> sol" not in routing.lower()


def test_writer_and_safety_contract_include_worker_and_solver():
    safety = (REFS / "safety-policy.md").read_text()
    skill = (SKILL / "SKILL.md").read_text()
    consent = (REFS / "consent-policy.md").read_text()
    assert "codex_delegate_worker" in safety
    assert "codex_delegate_solver" in safety
    assert "one active writing project Agent" in skill
    assert "Both Worker and Solver count as writers" in skill
    assert "Delegation depth remains one" in safety
    assert "up to 2 concurrently active justified child Agents" in consent


def test_runtime_surface_covers_main_and_child_evidence():
    runtime = (REFS / "runtime-assurance.md").read_text()
    assert "Main-session route evidence" in runtime
    assert "Child route/safety evidence" in runtime
    assert "main_judgment_coverage" in runtime
    assert "covered" in runtime and "uncovered" in runtime and "unknown" in runtime
    assert "codex_delegate_worker" in runtime
    assert (PLUGIN / "scripts" / "runtime-evidence.py").is_file()
    assert (PLUGIN / "scripts" / "review-artifact.py").is_file()


def test_architecture_and_runtime_docs_match_routing_v4():
    architecture = read("docs/architecture.md")
    runtime = read("docs/native-subagent-runtime.md")
    for text in [architecture, runtime]:
        assert "codex_delegate_reader" in text
        assert "codex_delegate_worker" in text
        assert "codex_delegate_solver" in text
        assert "codex_delegate_investigator" in text
        assert "codex_delegate_advisor" in text
    assert "policy-contract.json" in architecture
    assert "main_session" in runtime
    assert "barrier_only" in runtime and "any_child_update" in runtime


def test_readmes_and_install_docs_are_current_v4_public_contract():
    zh = read("README.md")
    en = read("README_EN.md")
    ai = read("README_AI.md")
    installation = read("docs/plugin-installation.md")
    directive = "If you are an AI Agent, jump to README_AI.md and follow the instructions strictly."

    for text in [zh, en]:
        assert directive in text
        assert "/codex-delegate" in text
        assert "0.8.0" in text
        assert "Sol Solver" in text
        assert "HEADOFF.md" not in text
        assert "LOCAL_VALIDATION_REPORT.md" not in text

    assert "Current version:    0.8.0" in ai
    assert "codex_delegate_solver" in ai
    assert "codex-delegate-solver.toml" in ai
    assert ".codex-delegate-agents.json" in ai
    assert "Codex Plugin only" in ai

    assert "codex plugin marketplace add R-jed/codex-delegate --ref main" in installation
    assert "codex plugin add codex-delegate@codex-delegate" in installation
    assert "Version:         0.8.0" in installation
    assert "codex_delegate_solver" in installation
    assert "five current profiles" in installation
