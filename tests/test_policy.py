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
    assert {"profile-route-lock-not-provable", "portable-role-conflicts-with-explicit-route", "luna-root-hidden-overrides-no-exact-inheritance", "required-role-surface-unavailable"} <= ids


def test_profile_mode_uses_project_specific_agent_types():
    profile_workers = [w for case in load_evals()["evals"] for w in case["expected"].get("workers", []) if w["route_mode"] == "profile"]
    assert profile_workers
    assert all(w["agent_type"] not in {"explorer", "worker", "default"} for w in profile_workers)
    assert any(w["agent_type"] == "sol_judge" for w in profile_workers)


def test_optional_profiles_parse_and_lock_expected_routes():
    expected = {
        "luna-explorer.toml": ("luna_explorer", "gpt-5.6-luna", "max"),
        "luna-worker.toml": ("luna_worker", "gpt-5.6-luna", "max"),
        "terra-reviewer.toml": ("terra_reviewer", "gpt-5.6-terra", "xhigh"),
        "sol-judge.toml": ("sol_judge", "gpt-5.6-sol", "high"),
    }
    for filename, values in expected.items():
        path = ROOT / "examples" / "agents" / filename
        assert path.exists()
        data = tomllib.loads(path.read_text())
        assert (data["name"], data["model"], data["model_reasoning_effort"]) == values
        assert data["developer_instructions"].strip()


def test_team_limits_and_large_fanout_consent():
    for case in load_evals()["evals"]:
        expected = case["expected"]
        workers = expected.get("workers", [])
        assert len(workers) <= 4
        assert sum(w["responsibility"] == "independent_critic" for w in workers) <= 1
        assert sum(w["responsibility"] == "senior_judge" for w in workers) <= 1
        if len(workers) > 2:
            assert expected["action"] == "ask_consent"


def test_senior_judge_always_requires_consent():
    for case in load_evals()["evals"]:
        workers = case["expected"].get("workers", [])
        if any(w["responsibility"] == "senior_judge" for w in workers):
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
    assert {"strict-read-only-unavailable", "prompt-injection-scope-expansion", "nested-delegation-observed", "two-shared-writing-workers", "production-deploy-from-worker", "role-specific-fork-turns-must-be-explicit"} <= ids


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
    texts = [(SKILL_DIR / "SKILL.md").read_text(), (SKILL_DIR / "references" / "routing-policy.md").read_text(), read("docs/model-route-assurance.md"), read("docs/architecture.md")]
    for text in texts:
        assert "profile_locked" in text
        assert "native_explicit_validated" in text
    assert "Do not use omitted `model` or `reasoning_effort` as proof" in texts[0]
    assert "agents.default_subagent_model" in texts[2]


def test_requested_configured_and_observed_routes_are_separate():
    texts = [(SKILL_DIR / "SKILL.md").read_text(), (SKILL_DIR / "references" / "routing-policy.md").read_text(), (SKILL_DIR / "references" / "task-packet.md").read_text(), read("docs/model-route-assurance.md")]
    for text in texts:
        assert "route_assurance" in text
        assert "observed_route" in text
    task_packet = texts[2]
    assert "preferred_route" in task_packet
    assert "configured_route" in task_packet
    assert "observed_route = not_exposed" in task_packet


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


def test_bilingual_readmes_and_visuals_exist():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "README_EN.md" in zh
    assert "README.md" in en
    assert zh.count("```mermaid") >= 3
    assert en.count("```mermaid") >= 3
    assert "img.shields.io" in zh and "img.shields.io" in en


def test_readmes_explain_native_subagent_vs_policy_layer():
    zh = read("README.md")
    en = read("README_EN.md")
    for text in [zh, en]:
        assert "spawn_agent" in text
        assert "SubAgent / ThreadSpawn" in text
        assert "Route Assurance" in text
        assert "App Thread" in text
    assert "和 Codex 自己调用 Subagents 有什么区别" in zh
    assert "How does this differ from Codex using Subagents by itself" in en


def test_readmes_explain_exact_model_and_effort_assurance():
    for text in [read("README.md"), read("README_EN.md")]:
        assert "profile_locked" in text
        assert "native_explicit_validated" in text
        assert "gpt-5.6-luna" in text and "max" in text
        assert "gpt-5.6-terra" in text and "xhigh" in text
        assert "gpt-5.6-sol" in text and "high" in text
        assert "not_exposed" in text


def test_profile_installation_is_documented_with_all_roles():
    for text in [read("README.md"), read("README_EN.md")]:
        assert "~/.codex/agents" in text
        for role in ["luna_explorer", "luna_worker", "terra_reviewer", "sol_judge"]:
            assert role in text


def test_openai_reference_doc_records_price_and_runtime_sources():
    refs = read("docs/openai-references.md")
    required_urls = ["https://openai.com/index/gpt-5-6/", "https://developers.openai.com/api/docs/pricing", "https://developers.openai.com/api/docs/guides/latest-model", "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs", "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_common.rs", "https://github.com/openai/codex/blob/main/codex-rs/core/src/agent/role.rs", "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs", "https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md"]
    for url in required_urls:
        assert url in refs
    assert "$1.00" in refs and "$6.00" in refs
    assert "$0.20" in refs and "$1.20" in refs
    assert "80% lower" in refs
    assert "[agents].default_subagent_model" in refs


def test_readmes_keep_price_as_context_not_route_invariant():
    zh = read("README.md")
    en = read("README_EN.md")
    for text in [zh, en]:
        assert "$0.20" in text and "$1.20" in text
        assert "62.7%" in text and "63.4%" in text
        assert "84.7%" in text and "87.4%" in text
    assert "没有被硬编码成路由规则" in zh
    assert "not routing invariants" in en


def test_readme_one_writer_requires_runtime_backed_isolation():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "一个共享 Workspace 同时最多 1 个 Writing Worker" in zh
    assert "One active writing Worker per shared workspace" in en


def test_installable_skill_has_no_repo_only_docs():
    forbidden = {"README.md", "README_EN.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"}
    present = {p.name for p in SKILL_DIR.iterdir() if p.is_file()}
    assert not (present & forbidden)


def test_mermaid_uses_github_safe_line_breaks():
    for name in ["README.md", "README_EN.md"]:
        text = read(name)
        assert "\\n" not in text
        assert "<br/>" in text


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


def test_readmes_distinguish_native_subagent_child_thread_from_other_sessions():
    zh = read("README.md")
    en = read("README_EN.md")
    for text in [zh, en]:
        assert "Native Subagent child thread" in text
        assert "App Thread" in text
        assert "spawn_agent" in text
    assert "独立用户会话" in zh
    assert "Separate user session" in en


def test_route_assurance_is_configuration_level_when_runtime_receipt_is_absent():
    zh = read("README.md")
    en = read("README_EN.md")
    skill = (SKILL_DIR / "SKILL.md").read_text()
    for text in [zh, en, skill]:
        assert "observed_route" in text
        assert "not_exposed" in text
    assert "配置级 Route Assurance" in zh
    assert "configuration-level Route Assurance" in en


def test_chinese_readme_credits_requested_documentation_style():
    zh = read("README.md")
    assert "chinese-documentation" in zh
    assert "自然中文" in zh


def test_model_route_docs_use_four_fact_assurance_model():
    assurance = read("docs/model-route-assurance.md")
    runtime = read("docs/native-subagent-runtime.md")
    architecture = read("docs/architecture.md")
    assert "separates four facts" in assurance
    assert "live `spawn_agent` surface exposes `agent_type`" in assurance
    assert "configuration-level" in runtime
    assert "configuration-level assured route" in architecture


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


def test_route_binding_is_fixed_while_team_selection_is_dynamic():
    zh = read("README.md")
    en = read("README_EN.md")
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "固化的是 Route，动态的是 Team" in zh
    assert "route binding is fixed; team composition is dynamic" in en
    assert "Role-to-route bindings are fixed; team composition is dynamic" in skill
    assert "never silently changes the current Root model or reasoning effort" in routing


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


def test_readme_explains_subagent_vs_agent_thread_as_same_native_mechanism():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "Subagent 是角色" in zh
    assert "Agent thread 是它的运行线程" in zh
    assert "Subagent is the delegated agent" in en
    assert "Agent thread is its runtime thread" in en
    for text in [zh, en]:
        assert "https://developers.openai.com/codex/subagents" in text


def test_readme_does_not_duplicate_fixed_vs_dynamic_route_section():
    zh = read("README.md")
    assert zh.count("固化的是 Route，动态的是 Team") == 1
    assert "固定的部分和智能判断的部分" not in zh


def test_user_facing_default_subagent_config_names_match_official_docs():
    zh = read("README.md")
    assurance = read("docs/model-route-assurance.md")
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    for text in [zh, assurance, routing]:
        assert "default_subagent_model" in text
        assert "default_subagent_reasoning_effort" in text
    assert "agent_default_subagent_model" not in zh


def test_readmes_scope_route_assurance_to_children_only():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "Route Assurance 只约束 Skill 创建的 model-specific Subagent" in zh
    assert "Skill 不会暗中切换 Root" in zh
    assert "Route Assurance applies to model-specific Subagents" in en
    assert "never silently switches the Root" in en


def test_readmes_recommend_profiles_for_strongest_route_assurance():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "推荐：同时安装锁定模型的 Agent profiles" in zh
    assert "Route Assurance 可以优先走 `profile_locked`" in zh
    assert "Recommended: install the model-locked Agent profiles" in en
    assert "Route Assurance can prefer `profile_locked`" in en
