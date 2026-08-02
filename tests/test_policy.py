from pathlib import Path
import json
import re
import tomllib

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
SKILL_DIR = PLUGIN_ROOT / "skills" / "codex-agent-team"
PROFILE_DIR = PLUGIN_ROOT / "agent-profiles"


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
    assert match
    frontmatter = yaml.safe_load(match.group(1))
    assert set(frontmatter) == {"name", "description"}
    assert frontmatter["name"] == "codex-agent-team"
    assert "Luna Max" in frontmatter["description"]
    assert "distinct dependency" in frontmatter["description"]


def test_openai_yaml_matches_skill():
    data = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text())
    assert data["interface"]["display_name"] == "Codex Agent Team"
    assert "/codex-agent-team" in data["interface"]["default_prompt"]
    assert "evidence" in data["interface"]["default_prompt"].lower()
    assert data["policy"]["allow_implicit_invocation"] is True


def test_core_references_exist_and_are_linked():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    for name in [
        "delegation-contract.md",
        "routing-policy.md",
        "runtime-assurance.md",
        "consent-policy.md",
        "safety-policy.md",
        "orchestration-receipt.md",
    ]:
        assert (SKILL_DIR / "references" / name).exists()
        assert f"references/{name}" in skill
    assert not (SKILL_DIR / "references" / "task-packet.md").exists()


def test_semantic_profiles_are_namespaced_and_route_locked():
    expected = {
        "codex-agent-team-reader.toml": ("codex_agent_team_reader", "gpt-5.6-luna", "max", "read-only"),
        "codex-agent-team-worker.toml": ("codex_agent_team_worker", "gpt-5.6-luna", "max", "workspace-write"),
        "codex-agent-team-investigator.toml": ("codex_agent_team_investigator", "gpt-5.6-terra", "xhigh", "read-only"),
        "codex-agent-team-advisor.toml": ("codex_agent_team_advisor", "gpt-5.6-sol", "high", "read-only"),
    }
    assert sorted(path.name for path in PROFILE_DIR.glob("*.toml")) == sorted(expected)
    for filename, values in expected.items():
        data = tomllib.loads((PROFILE_DIR / filename).read_text())
        actual = (data["name"], data["model"], data["model_reasoning_effort"], data["sandbox_mode"])
        assert actual == values
        assert data["developer_instructions"].strip()
        assert data["name"].startswith("codex_agent_team_")


def test_static_cases_use_semantic_roles_and_profile_only_routing():
    allowed = {
        "reader": ("gpt-5.6-luna", "max", "codex_agent_team_reader"),
        "worker": ("gpt-5.6-luna", "max", "codex_agent_team_worker"),
        "investigator": ("gpt-5.6-terra", "xhigh", "codex_agent_team_investigator"),
        "advisor": ("gpt-5.6-sol", "high", "codex_agent_team_advisor"),
    }
    for case in load_evals()["evals"]:
        for node in case["expected"].get("nodes", []):
            model, effort, agent_type = allowed[node["responsibility"]]
            assert (node["model"], node["effort"], node["agent_type"]) == (model, effort, agent_type)
            assert node["route_assurance"] == "profile_locked"
            assert node["fork_turns"] == "none" or re.fullmatch(r"[1-9][0-9]*", node["fork_turns"])


def test_no_fixed_three_model_pipeline():
    ids = {case["id"] for case in load_evals()["evals"]}
    assert "luna-sol-short-path" in ids
    assert "luna-capability-gap-terra-delta" in ids
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "Luna -> Terra -> Sol" in routing
    assert "never required" in routing
    assert "main -> Luna -> Sol -> main" in routing


def test_contractability_is_upstream_of_model_selection():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    assert skill.index("## 3. Contractability Gate") < skill.index("## 5. Agent Profile Readiness")
    contract = (SKILL_DIR / "references" / "delegation-contract.md").read_text()
    for field in ["OUTCOME", "SCOPE", "INVARIANTS", "DECISION RIGHTS", "ACCEPTANCE ORACLE", "VERIFICATION", "STOP / ESCALATE"]:
        assert field in contract
    assert "do not create a writing Worker" in contract


def test_failure_classification_prevents_whole_task_terra_rework():
    contract = (SKILL_DIR / "references" / "delegation-contract.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    for phrase in ["mechanical defect", "contract gap", "capability gap", "judgment gap"]:
        assert phrase in contract
    assert "Low quality alone is not a Terra trigger" in contract
    assert "Terra is not a mandatory reviewer and not a generic second implementation attempt" in routing
    assert "unresolved delta" in routing
    terra = tomllib.loads((PROFILE_DIR / "codex-agent-team-investigator.toml").read_text())
    assert "unresolved technical delta" in terra["developer_instructions"]
    assert "do not restart repository discovery" in terra["developer_instructions"]


def test_shared_evidence_state_and_invalidation_are_explicit():
    contract = (SKILL_DIR / "references" / "delegation-contract.md").read_text()
    skill = (SKILL_DIR / "SKILL.md").read_text()
    for text in [contract, skill]:
        assert "Shared Evidence State" in text
        assert "invalidated" in text.lower()
    assert "deterministic | repository_fact | model_judgment" in contract
    assert "A file or artifact change invalidates only evidence that depends on the changed input" in contract


def test_useful_parallelism_requires_distinct_dependencies():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assert "outputs satisfy different dependencies" in skill
    assert "Parallel execution is useful when concurrent outputs satisfy different dependencies" in routing
    assert "Do not launch Luna, Terra, and Sol over the same question" in routing


def test_one_writer_and_depth_one_remain_invariants():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    safety = (SKILL_DIR / "references" / "safety-policy.md").read_text()
    assert "one active writing Worker" in skill
    assert "Children must not spawn further Subagents" in safety
    assert "Every Delegation Contract carries the no-further-delegation rule" in safety


def test_consent_is_resource_based_and_explicit_sol_can_fit_baseline():
    consent = (SKILL_DIR / "references" / "consent-policy.md").read_text()
    assert "0-2 justified child Agents" in consent
    assert "at most 1 active writer" in consent
    assert "Luna + Sol selective review" in consent
    assert "For implicit Skill invocation, ask before adding Sol" in consent


def test_route_assurance_has_no_portable_mode():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    assurance = read("docs/model-route-assurance.md")
    for text in [skill, routing, assurance]:
        assert "profile_locked" in text
        assert "native_explicit_validated" not in text
    assert "There is no Portable Mode" in skill
    assert "There is no Portable Mode" in routing
    assert "## No Portable Mode" in assurance


def test_readmes_are_text_first_and_explain_incremental_orchestration():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "README_EN.md" in zh and "README.md" in en
    for text in [zh, en]:
        assert "<img" not in text
        assert "```mermaid" not in text
        assert len(text.splitlines()) <= 190
        assert "/codex-agent-team" in text
        assert "codex plugin marketplace add R-jed/codex-agent-team --ref main" in text
        assert "codex_agent_team_worker" in text
        assert "codex_agent_team_investigator" in text
        assert "codex_agent_team_advisor" in text
    assert "Luna + Sol 是一条正常的短路径" in zh
    assert "已经算过的东西尽量不再算一遍" in zh
    assert "Luna + Sol is a normal short path" in en
    assert "Reuse work that has already been established" in en


def test_readmes_use_main_session_without_user_facing_root_vocabulary():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "主会话" in zh
    assert "main session" in en.lower()
    assert not re.search(r"\broot\b", zh, re.I)
    assert not re.search(r"\broot\b", en, re.I)


def test_chinese_readme_avoids_em_dash_and_basic_spacing_regressions():
    text = read("README.md")
    assert "—" not in text
    stripped = re.sub(r"```.*?```", "", text, flags=re.S)
    stripped = re.sub(r"`[^`]*`", "", stripped)
    bad = []
    for line in stripped.splitlines():
        if "http" in line or "<" in line or "|" in line:
            continue
        if re.search(r"[\u4e00-\u9fff][A-Za-z0-9]|[A-Za-z0-9][\u4e00-\u9fff]", line):
            bad.append(line)
    assert not bad, f"Chinese/English spacing regressions: {bad}"


def test_architecture_and_model_docs_match_semantic_role_design():
    architecture = read("docs/architecture.md")
    assurance = read("docs/model-route-assurance.md")
    assert "Role identity is intentionally separate from model identity" in architecture
    assert "No Portable Mode" in assurance
    assert "codex_agent_team_investigator" in architecture
    assert "route_evidence" in architecture


def test_official_runtime_reference_still_documented():
    refs = read("docs/openai-references.md")
    runtime = read("docs/native-subagent-runtime.md")
    assert "https://developers.openai.com/codex/subagents" in refs
    assert "spawn_agent" in runtime
    assert "delegation depth at 1" in runtime
