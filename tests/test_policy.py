from pathlib import Path
import json
import re
import tomllib

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "codex-agent-team"


def load_evals():
    return json.loads((ROOT / "evals" / "routing-cases.json").read_text())


def read(name):
    return (ROOT / name).read_text()


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
    assert 25 <= len(data["interface"]["short_description"]) <= 64
    assert data["policy"]["allow_implicit_invocation"] is True


def test_core_references_exist_and_are_linked():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    for name in ["routing-policy.md", "task-packet.md", "consent-policy.md", "safety-policy.md"]:
        assert (SKILL_DIR / "references" / name).exists()
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


def test_every_worker_has_exact_route_metadata():
    for case in load_evals()["evals"]:
        for worker in case["expected"].get("workers", []):
            assert worker["fork_turns"] == "none" or re.fullmatch(r"[1-9][0-9]*", worker["fork_turns"])
            assert worker["route_mode"] in {"portable", "profile"}
            assert worker["route_assurance"] in {"native_explicit_validated", "profile_locked"}
            assert worker["agent_type"]


def test_route_assurance_matches_route_mode():
    expected = {"portable": "native_explicit_validated", "profile": "profile_locked"}
    for case in load_evals()["evals"]:
        for worker in case["expected"].get("workers", []):
            assert worker["route_assurance"] == expected[worker["route_mode"]]


def test_inheritance_is_not_an_exact_assurance_mode():
    schema = json.loads((ROOT / "evals" / "routing-case.schema.json").read_text())
    props = schema["properties"]["evals"]["items"]["properties"]["expected"]["properties"]["workers"]["items"]["properties"]
    assert "inheritance" not in props["route_mode"]["enum"]
    assert "inherited_exact" not in props["route_assurance"]["enum"]
    ids = {case["id"] for case in load_evals()["evals"]}
    assert "luna-root-hidden-overrides-no-exact-inheritance" in ids


def test_route_assurance_failure_cases_present():
    ids = {case["id"] for case in load_evals()["evals"]}
    assert {
        "profile-route-lock-not-provable",
        "portable-role-conflicts-with-explicit-route",
        "luna-root-hidden-overrides-no-exact-inheritance",
        "required-role-surface-unavailable",
    } <= ids


def test_profile_mode_uses_project_specific_agent_types():
    profile_workers = [
        worker
        for case in load_evals()["evals"]
        for worker in case["expected"].get("workers", [])
        if worker["route_mode"] == "profile"
    ]
    assert profile_workers
    assert all(worker["agent_type"] not in {"explorer", "worker", "default"} for worker in profile_workers)
    assert any(worker["agent_type"] == "sol_judge" for worker in profile_workers)


def test_optional_profiles_parse_and_lock_expected_routes():
    expected = {
        "luna-explorer.toml": ("luna_explorer", "gpt-5.6-luna", "max"),
        "luna-worker.toml": ("luna_worker", "gpt-5.6-luna", "max"),
        "terra-reviewer.toml": ("terra_reviewer", "gpt-5.6-terra", "xhigh"),
        "sol-judge.toml": ("sol_judge", "gpt-5.6-sol", "high"),
    }
    for filename, values in expected.items():
        data = tomllib.loads((ROOT / "examples" / "agents" / filename).read_text())
        assert (data["name"], data["model"], data["model_reasoning_effort"]) == values
        assert data["developer_instructions"].strip()


def test_team_limits_and_large_fanout_consent():
    for case in load_evals()["evals"]:
        expected = case["expected"]
        workers = expected.get("workers", [])
        assert len(workers) <= 4
        assert sum(worker["responsibility"] == "independent_critic" for worker in workers) <= 1
        assert sum(worker["responsibility"] == "senior_judge" for worker in workers) <= 1
        if len(workers) > 2:
            assert expected["action"] == "ask_consent"


def test_senior_judge_always_requires_consent():
    for case in load_evals()["evals"]:
        workers = case["expected"].get("workers", [])
        if any(worker["responsibility"] == "senior_judge" for worker in workers):
            assert case["expected"]["action"] == "ask_consent"
            assert case["expected"].get("consent_reason")


def test_luna_is_only_default_execution_route():
    for case in load_evals()["evals"]:
        for worker in case["expected"].get("workers", []):
            if worker["responsibility"] in {"explorer", "execution_worker"}:
                assert (worker["model"], worker["effort"]) == ("gpt-5.6-luna", "max")


def test_one_writer_per_workspace_in_delegate_plans():
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
    assert {
        "strict-read-only-unavailable",
        "prompt-injection-scope-expansion",
        "nested-delegation-observed",
        "two-shared-writing-workers",
        "production-deploy-from-worker",
        "role-specific-fork-turns-must-be-explicit",
    } <= ids


def test_terra_root_behavior_is_covered():
    ids = {case["id"] for case in load_evals()["evals"]}
    assert {"terra-root-detached-review", "terra-root-needs-sol-judge"} <= ids
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "### Terra XHigh Root" in routing
    assert "Do not create another Terra solely to claim model diversity" in routing


def test_skill_contains_no_old_effort_ladder():
    text = (SKILL_DIR / "SKILL.md").read_text().lower()
    for phrase in ["luna medium", "luna high", "terra high", "sol xhigh"]:
        assert phrase not in text


def test_context_fork_contract_is_explicit():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    for text in [skill, routing]:
        assert 'fork_turns = "none"' in text
        assert 'fork_turns = "all"' in text
    assert "defaults `fork_turns` to full history when omitted" in routing


def test_route_assurance_docs_reject_implicit_inheritance():
    texts = [
        (SKILL_DIR / "SKILL.md").read_text(),
        (SKILL_DIR / "references" / "routing-policy.md").read_text(),
        read("docs/model-route-assurance.md"),
        read("docs/architecture.md"),
    ]
    for text in texts:
        assert "profile_locked" in text
        assert "native_explicit_validated" in text
    assert "Do not use omitted `model` or `reasoning_effort` as proof" in texts[0]
    assert "agents.default_subagent_model" in texts[2]


def test_requested_configured_and_observed_routes_are_separate():
    texts = [
        (SKILL_DIR / "SKILL.md").read_text(),
        (SKILL_DIR / "references" / "routing-policy.md").read_text(),
        (SKILL_DIR / "references" / "task-packet.md").read_text(),
        read("docs/model-route-assurance.md"),
    ]
    for text in texts:
        assert "route_assurance" in text
        assert "observed_route" in text
    assert "preferred_route" in texts[2]
    assert "configured_route" in texts[2]
    assert "observed_route = not_exposed" in texts[2]


def test_native_subagent_runtime_doc_explains_actual_primitive():
    text = read("docs/native-subagent-runtime.md")
    assert "SubAgent / ThreadSpawn" in text
    assert "child Codex thread/session" in text
    assert "spawn_agent" in text
    assert "does not create an App Thread" in text
    assert "does not replace Codex Subagents" in text
    assert "delegation depth at 1" in text


def test_architecture_links_runtime_and_assurance_docs():
    text = read("docs/architecture.md")
    assert "native-subagent-runtime.md" in text
    assert "model-route-assurance.md" in text
    assert "Native `spawn_agent`" in text


def test_permission_docs_do_not_overclaim_profile_sandbox():
    safety = (SKILL_DIR / "references" / "safety-policy.md").read_text()
    architecture = read("docs/architecture.md")
    assert 'profile declaring `sandbox_mode = "read-only"`' in safety
    assert "not proof of effective runtime enforcement" in architecture


def test_openai_reference_doc_records_price_and_runtime_sources():
    refs = read("docs/openai-references.md")
    required_urls = [
        "https://openai.com/index/gpt-5-6/",
        "https://developers.openai.com/api/docs/pricing",
        "https://developers.openai.com/api/docs/guides/latest-model",
        "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs",
        "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_common.rs",
        "https://github.com/openai/codex/blob/main/codex-rs/core/src/agent/role.rs",
        "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs",
        "https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md",
    ]
    for url in required_urls:
        assert url in refs
    assert "$1.00" in refs and "$6.00" in refs
    assert "$0.20" in refs and "$1.20" in refs
    assert "80% lower" in refs
    assert "[agents].default_subagent_model" in refs


def test_installable_skill_has_no_repo_only_docs():
    forbidden = {"README.md", "README_EN.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"}
    present = {path.name for path in SKILL_DIR.iterdir() if path.is_file()}
    assert not (present & forbidden)


def test_no_silent_cross_role_fallback():
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "Luna execution unavailable does not turn Terra into an implementation Worker" in routing
    assert "Terra critic unavailable means Root reviews" in routing
    assert "Sol Senior Judge unavailable means Root keeps control" in routing


def test_installable_skill_does_not_depend_on_repo_level_docs():
    for path in SKILL_DIR.rglob("*.md"):
        text = path.read_text()
        assert "../../docs/" not in text
        assert "../docs/" not in text


def test_model_route_docs_use_four_fact_assurance_model():
    assurance = read("docs/model-route-assurance.md")
    runtime = read("docs/native-subagent-runtime.md")
    architecture = read("docs/architecture.md")
    assert "separates four facts" in assurance
    assert "live `spawn_agent` surface exposes `agent_type`" in assurance
    assert "configuration-level" in runtime
    assert "configuration-level assured route" in architecture


def test_official_subagent_terms_and_precedence_are_documented():
    refs = read("docs/openai-references.md")
    runtime = read("docs/native-subagent-runtime.md")
    assurance = read("docs/model-route-assurance.md")
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "https://developers.openai.com/codex/subagents" in refs
    assert "Subagent" in runtime and "Agent thread" in runtime
    for text in [assurance, skill, routing]:
        assert "custom Agent file value" in text
        assert "explicit spawn value" in text
        assert "[agents] default" in text
        assert "parent value" in text


def test_readmes_are_concise_skill_overviews_with_localized_svg_visuals():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "README_EN.md" in zh
    assert "README.md" in en

    zh_assets = ["hero-zh.svg", "workflow-zh.svg", "roles-zh.svg"]
    en_assets = ["hero.svg", "workflow.svg", "roles.svg"]

    for asset in zh_assets:
        path = ROOT / "assets" / "readme" / asset
        svg = path.read_text()
        assert svg.lstrip().startswith("<svg")
        assert re.search(r"[\u4e00-\u9fff]", svg)
        assert f"assets/readme/{asset}" in zh
        assert f"assets/readme/{asset}" not in en

    for asset in en_assets:
        path = ROOT / "assets" / "readme" / asset
        svg = path.read_text()
        assert svg.lstrip().startswith("<svg")
        assert not re.search(r"[\u4e00-\u9fff]", svg)
        assert f"assets/readme/{asset}" in en
        assert f"assets/readme/{asset}" not in zh

    for text in [zh, en]:
        assert "```mermaid" not in text
        assert not re.search(r"assets/readme/[^)\"']+\.(png|jpe?g|webp|gif)", text, re.I)
        assert len(text.splitlines()) <= 180


def test_readmes_keep_quick_start_and_role_identity():
    zh = read("README.md")
    en = read("README_EN.md")
    for text in [zh, en]:
        assert "python scripts/install.py" in text
        assert "--skill-only" in text
        assert "$codex-agent-team" in text
        assert "GPT-5.6 Luna" in text
        assert "GPT-5.6 Terra" in text
        assert "GPT-5.6 Sol" in text
        for role in ["luna_explorer", "luna_worker", "terra_reviewer", "sol_judge"]:
            assert role in text


def test_readmes_keep_public_safety_boundaries():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "一个共享 Workspace 同时最多 1 个 Writing Worker" in zh
    assert "Worker 不继续创建新的 Subagent 团队" in zh
    assert "Skill 不会暗中切换当前 Root" in zh
    assert "one active writing Worker per shared workspace" in en
    assert "Workers do not create another Subagent team" in en
    assert "never silently switches the active Root" in en


def test_readmes_point_technical_details_to_docs():
    for text in [read("README.md"), read("README_EN.md")]:
        for path in [
            "docs/architecture.md",
            "docs/native-subagent-runtime.md",
            "docs/model-route-assurance.md",
            "docs/openai-references.md",
            "skill/codex-agent-team/references/routing-policy.md",
            "skill/codex-agent-team/references/safety-policy.md",
            "skill/codex-agent-team/references/consent-policy.md",
        ]:
            assert path in text
        assert "spawn_agent" in text


def test_chinese_readme_has_basic_cn_en_spacing():
    text = read("README.md")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    bad = []
    for line in text.splitlines():
        if "http" in line or "<" in line or "|" in line:
            continue
        if re.search(r"[\u4e00-\u9fff][A-Za-z0-9]|[A-Za-z0-9][\u4e00-\u9fff]", line):
            bad.append(line)
    assert not bad, f"Chinese/English spacing regressions: {bad}"


def test_chinese_readme_avoids_em_dash_prose():
    assert "—" not in read("README.md")
