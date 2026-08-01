from pathlib import Path
import json
import re

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "codex-agent-team"


def load_evals():
    return json.loads((ROOT / "evals" / "routing-cases.json").read_text())


def test_eval_schema():
    schema = json.loads((ROOT / "evals" / "routing-case.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(load_evals())


def test_skill_frontmatter_and_name():
    text = (SKILL_DIR / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, "SKILL.md must start with YAML frontmatter"
    frontmatter = yaml.safe_load(match.group(1))
    assert set(frontmatter) == {"name", "description"}
    assert frontmatter["name"] == "codex-agent-team"
    assert "Luna Max" in frontmatter["description"]
    assert "Terra XHigh" in frontmatter["description"]


def test_openai_yaml_matches_skill():
    data = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text())
    assert data["interface"]["display_name"] == "Codex Agent Team"
    assert "$codex-agent-team" in data["interface"]["default_prompt"]
    desc = data["interface"]["short_description"]
    assert 25 <= len(desc) <= 64
    assert data["policy"]["allow_implicit_invocation"] is True


def test_core_references_exist_and_are_linked():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    for name in ["routing-policy.md", "task-packet.md", "consent-policy.md", "safety-policy.md"]:
        path = SKILL_DIR / "references" / name
        assert path.exists()
        assert f"references/{name}" in skill


def test_role_routes_are_stable():
    allowed = {
        "explorer": ("gpt-5.6-luna", "max"),
        "execution_worker": ("gpt-5.6-luna", "max"),
        "independent_critic": ("gpt-5.6-terra", "xhigh"),
        "senior_judge": ("gpt-5.6-sol", "high"),
    }
    for case in load_evals()["evals"]:
        for worker in case["expected"].get("workers", []):
            assert (worker["model"], worker["effort"]) == allowed[worker["responsibility"]]


def test_team_limits_and_large_fanout_consent():
    for case in load_evals()["evals"]:
        expected = case["expected"]
        workers = expected.get("workers", [])
        assert len(workers) <= 4
        terra = sum(w["responsibility"] == "independent_critic" for w in workers)
        sol = sum(w["responsibility"] == "senior_judge" for w in workers)
        assert terra <= 1
        assert sol <= 1
        if len(workers) > 2:
            assert expected["action"] == "ask_consent"


def test_senior_judge_always_requires_consent():
    for case in load_evals()["evals"]:
        workers = case["expected"].get("workers", [])
        if any(w["responsibility"] == "senior_judge" for w in workers):
            assert case["expected"]["action"] == "ask_consent"
            assert case["expected"].get("consent_reason")


def test_no_non_luna_execution_worker():
    for case in load_evals()["evals"]:
        for worker in case["expected"].get("workers", []):
            if worker["responsibility"] in {"explorer", "execution_worker"}:
                assert worker["model"] == "gpt-5.6-luna"
                assert worker["effort"] == "max"


def test_one_writer_per_workspace_in_expected_delegate_plans():
    for case in load_evals()["evals"]:
        if case["expected"]["action"] not in {"delegate", "ask_consent"}:
            continue
        counts = {}
        for worker in case["expected"].get("workers", []):
            if worker["write_intent"]:
                counts[worker["workspace"]] = counts.get(worker["workspace"], 0) + 1
        assert all(count <= 1 for count in counts.values())


def test_required_safety_evals_present():
    ids = {case["id"] for case in load_evals()["evals"]}
    required = {
        "strict-read-only-unavailable",
        "prompt-injection-scope-expansion",
        "nested-delegation-observed",
        "two-shared-writing-workers",
        "production-deploy-from-worker",
    }
    assert required <= ids


def test_skill_contains_no_model_escalation_ladder():
    text = (SKILL_DIR / "SKILL.md").read_text().lower()
    forbidden = ["luna medium", "luna high", "terra high", "sol xhigh"]
    for phrase in forbidden:
        assert phrase not in text


def test_installable_skill_has_no_repo_only_docs():
    forbidden = {"README.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"}
    present = {p.name for p in SKILL_DIR.iterdir() if p.is_file()}
    assert not (present & forbidden)
