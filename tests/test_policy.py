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


def test_every_planned_worker_has_explicit_fork_and_route_mode():
    for case in load_evals()["evals"]:
        for worker in case["expected"].get("workers", []):
            assert worker["fork_turns"] == "none" or re.fullmatch(r"[1-9][0-9]*", worker["fork_turns"])
            assert worker["route_mode"] in {"portable", "profile"}
            assert worker["agent_type"]


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


def test_profile_mode_uses_custom_agent_type():
    profile_cases = [
        c for c in load_evals()["evals"]
        if any(w.get("route_mode") == "profile" for w in c["expected"].get("workers", []))
    ]
    assert profile_cases, "At least one Profile Mode eval is required"
    for case in profile_cases:
        for worker in case["expected"].get("workers", []):
            if worker.get("route_mode") == "profile":
                assert worker["agent_type"] not in {"explorer", "worker", "default"}


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
        "role-specific-fork-turns-must-be-explicit",
        "required-role-surface-unavailable",
    }
    assert required <= ids


def test_terra_root_behavior_is_covered():
    ids = {case["id"] for case in load_evals()["evals"]}
    assert "terra-root-detached-review" in ids
    assert "terra-root-needs-sol-judge" in ids
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "### Terra XHigh Root" in routing
    assert "Do not create another Terra Critic solely to claim model diversity" in routing


def test_skill_contains_no_model_escalation_ladder():
    text = (SKILL_DIR / "SKILL.md").read_text().lower()
    forbidden = ["luna medium", "luna high", "terra high", "sol xhigh"]
    for phrase in forbidden:
        assert phrase not in text


def test_context_fork_contract_is_explicit():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    for text in [skill, routing]:
        assert 'fork_turns = "none"' in text
        assert 'fork_turns = "all"' in text
        assert "Never omit `fork_turns`" in text
    assert "MultiAgentV2 defaults `fork_turns` to full history when omitted" in routing


def test_portable_and_profile_modes_do_not_compete():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    architecture = (ROOT / "docs" / "architecture.md").read_text()
    for text in [skill, routing, architecture]:
        assert "Portable Mode" in text
        assert "Profile Mode" in text
    assert "live `agent_type` and `fork_turns` surface" in architecture
    assert "omit explicit `model` and `reasoning_effort`" in skill
    assert "Do not combine a route-pinning custom profile with competing explicit model/effort overrides" in skill


def test_permission_docs_do_not_overclaim_profile_sandbox():
    safety = (SKILL_DIR / "references" / "safety-policy.md").read_text()
    architecture = (ROOT / "docs" / "architecture.md").read_text()
    readme = (ROOT / "README.md").read_text()
    assert "profile declaring `sandbox_mode = \"read-only\"`" in safety
    assert "not sufficient evidence for `permission_guarantee = runtime_enforced`" in architecture
    assert "实际 child 权限仍以当前 Codex runtime 的有效权限为准" in readme


def test_bilingual_readmes_and_visuals_exist():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "README_EN.md" in zh
    assert "README.md" in en
    assert zh.count("```mermaid") >= 2
    assert en.count("```mermaid") >= 2
    assert "img.shields.io" in zh
    assert "img.shields.io" in en


def test_openai_reference_doc_records_price_change_and_sources():
    refs = (ROOT / "docs" / "openai-references.md").read_text()
    required_urls = [
        "https://openai.com/index/gpt-5-6/",
        "https://developers.openai.com/api/docs/pricing",
        "https://developers.openai.com/api/docs/guides/latest-model",
        "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs",
        "https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md",
    ]
    for url in required_urls:
        assert url in refs
    assert "$1.00" in refs and "$6.00" in refs
    assert "$0.20" in refs and "$1.20" in refs
    assert "80% lower" in refs


def test_readme_one_writer_requires_runtime_isolation():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "runtime-backed 隔离 workspace/worktree/filesystem" in zh
    assert "runtime-backed workspace/worktree/filesystem isolation" in en
    assert "互不重叠的写边界" not in zh


def test_installable_skill_has_no_repo_only_docs():
    forbidden = {"README.md", "README_EN.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"}
    present = {p.name for p in SKILL_DIR.iterdir() if p.is_file()}
    assert not (present & forbidden)


def test_mermaid_uses_github_safe_line_breaks():
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text()
        assert "\\n" not in text
        assert "<br/>" in text


def test_profile_installation_and_agent_role_sources_are_documented():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    refs = (ROOT / "docs" / "openai-references.md").read_text()
    for text in [zh, en]:
        assert "~/.codex/agents" in text
        assert "luna_explorer" in text
        assert "luna_worker" in text
        assert "terra_reviewer" in text
    assert "codex-rs/core/src/config/agent_roles.rs" in refs
    assert "codex-rs/core/src/agent/role_tests.rs" in refs


def test_bilingual_readmes_share_published_model_evidence():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    for text in [zh, en]:
        for value in ["64.6%", "63.4%", "62.7%", "88.8%", "87.4%", "84.7%"]:
            assert value in text
        assert "$0.20" in text and "$1.20" in text
    refs = (ROOT / "docs" / "openai-references.md").read_text()
    assert "These are OpenAI model-family evaluations, not Codex Agent Team benchmarks" in refs


def test_capability_gate_requires_role_and_fork_surface():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "required `agent_type` and `fork_turns` surface" in skill
    assert "required `agent_type` or `fork_turns` surface is unavailable" in routing
    ids = {case["id"] for case in load_evals()["evals"]}
    assert "required-role-surface-unavailable" in ids
