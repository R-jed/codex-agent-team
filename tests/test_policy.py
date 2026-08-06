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


def contract():
    return json.loads(POLICY.read_text())


def test_skill_and_openai_interface_keep_one_explicit_product_entrypoint():
    text = (SKILL / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match
    frontmatter = yaml.safe_load(match.group(1))
    assert frontmatter["name"] == "codex-delegate"
    assert "Delegate only when it improves the task" in frontmatter["description"]

    data = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text())
    assert data["interface"]["display_name"] == "Codex Delegate"
    assert "$codex-delegate:codex-delegate" in data["interface"]["default_prompt"]
    assert data["policy"]["allow_implicit_invocation"] is False


def test_policy_contract_is_machine_constants_not_runtime_ontology():
    payload = contract()
    assert payload["schema_version"] == 4
    assert set(payload) == {
        "schema_version",
        "delegation",
        "capability_dedup",
        "roles",
        "final_review",
    }
    assert payload["delegation"] == {
        "max_depth": 1,
        "max_active_writers_per_workspace": 1,
    }
    assert "baseline_concurrent_children" not in payload["delegation"]
    assert "max_concurrent_children" not in payload["delegation"]
    assert "classification" not in payload
    assert "dependency_kinds" not in json.dumps(payload)

    dedup = payload["capability_dedup"]
    assert dedup["reference_role"] == "solver"
    assert dedup["reasoning_effort_order"].index("medium") < dedup["reasoning_effort_order"].index("high")

    assert set(payload["roles"]) == {"reader", "worker", "solver", "investigator", "advisor"}
    assert {p.name for p in PROFILES.glob("*.toml")} == {
        spec["profile_file"] for spec in payload["roles"].values()
    }
    for spec in payload["roles"].values():
        profile = tomllib.loads((PROFILES / spec["profile_file"]).read_text())
        assert profile["name"] == spec["agent_type"]
        assert profile["model"] == spec["model"]
        assert profile["model_reasoning_effort"] == spec["effort"]
        assert profile["sandbox_mode"] == spec["sandbox_intent"]


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
    for process_proxy in ["terra_escalation", "material_recovery", "wide_blast_radius"]:
        assert process_proxy not in triggers


def test_model_facing_policy_surface_has_five_focused_owners():
    assert {path.name for path in REFS.glob("*.md")} == {
        "router-core.md",
        "team-plan.md",
        "recovery.md",
        "guardrails.md",
        "final-review.md",
    }
    skill = (SKILL / "SKILL.md").read_text()
    for name in ["router-core.md", "team-plan.md", "recovery.md", "guardrails.md", "final-review.md"]:
        assert f"references/{name}" in skill
    assert "five focused owners" in skill
    for retired in [
        "routing-policy.md",
        "delegation-contract.md",
        "execution-progress.md",
        "consent-policy.md",
        "safety-policy.md",
        "runtime-assurance.md",
        "final-review-gate.md",
        "orchestration-receipt.md",
    ]:
        assert retired not in skill
        assert not (REFS / retired).exists()


def test_router_core_uses_direct_capability_questions_and_delegates_stateful_coordination():
    router = (REFS / "router-core.md").read_text()
    skill = (SKILL / "SKILL.md").read_text()
    for phrase in [
        "Minimal task state",
        "does delegation help",
        "Writing with behavior already decided",
        "Writing with judgment coupled to implementation",
        "Bounded read-heavy technical investigation",
        "Main-session Sol dedup is an optimization",
        "blocked_by: none | contract | judgment | investigation | stalled",
        "at most one clean retry",
        "ready frontier",
        "progressive fan-out",
        "Native Codex capacity is the upper bound on concurrency, not a target",
        "team-plan.md",
        "recovery.md",
    ]:
        assert phrase.lower() in router.lower()
    assert "Dependency Ledger" not in skill
    assert "Shared Evidence State" not in skill
    assert "Recovery Ledger" not in skill


def test_terra_is_investigation_lane_not_hard_work_escalation():
    router = (REFS / "router-core.md").read_text()
    investigator = (PROFILES / "codex-delegate-investigator.toml").read_text()
    assert "read-heavy technical investigation" in router
    assert "not an escalation rung" in router
    assert "Demanding, ambiguous, multi-step technical reasoning" in router
    assert "read-heavy technical investigation" in investigator
    assert "blocker=judgment" in investigator


def test_guardrails_keep_safety_without_hot_path_runtime_ceremony():
    guardrails = (REFS / "guardrails.md").read_text()
    for phrase in [
        "One writer per canonical checkout",
        "main session when mutating the checkout",
        "Adaptive fan-out still requires discipline",
        "Child count by itself is not a consent trigger",
        "Explicit invocation only",
        "$codex-delegate:codex-delegate <task>",
        "First-use readiness before delegated execution",
        "Runtime evidence is on demand",
        "Do not emit a separate orchestration receipt",
    ]:
        assert phrase in guardrails
    for script in [
        "runtime-evidence.py",
        "review-artifact.py",
        "validate_team_plan.py",
        "validate_team_ledger.py",
    ]:
        assert (PLUGIN / "scripts" / script).is_file()


def test_team_plan_and_recovery_do_not_reintroduce_numeric_fanout_policy():
    team_plan = (REFS / "team-plan.md").read_text().lower()
    recovery = (REFS / "recovery.md").read_text().lower()
    validator = (PLUGIN / "scripts" / "validate_team_plan.py").read_text().lower()
    assert "native codex capacity remains the concurrency ceiling" in team_plan
    assert "fixed waves" in team_plan
    assert "two-attempt bound is a recovery limit, not a team-size or concurrency limit" in recovery
    for retired in ["max_planned_workers", "max_worker_attempts", "max_new_workers_per_wave", "scale_profile"]:
        assert retired not in validator


def test_static_eval_files_remain_valid_but_are_not_runtime_policy_owners():
    schema = json.loads((ROOT / "evals" / "routing-case.schema.json").read_text())
    cases = json.loads((ROOT / "evals" / "routing-cases.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(cases)
    assert cases["skill_name"] == "codex-delegate"
    roles = contract()["roles"]
    for case in cases["evals"]:
        for node in case["expected"].get("nodes", []):
            spec = roles[node["responsibility"]]
            assert node["model"] == spec["model"]
            assert node["effort"] == spec["effort"]
            assert node["agent_type"] == spec["agent_type"]


def test_public_docs_keep_product_identity_and_ai_reference_owns_profile_details():
    zh = read("README.md")
    en = read("README_EN.md")
    ai = read("README_AI.md")
    directive = "If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly."

    for text in [zh, en]:
        assert directive in text
        assert "$codex-delegate:codex-delegate" in text
        assert "1.1.0" in text
        assert "Sol Solver" in text
        assert "HEADOFF.md" not in text
        assert "LOCAL_VALIDATION_REPORT.md" not in text

    for role in [
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
    ]:
        assert role in ai
