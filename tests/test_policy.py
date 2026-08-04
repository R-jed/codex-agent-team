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
POLICY_CONTRACT = PLUGIN_ROOT / "policy-contract.json"
RUNTIME_VERIFIER = PLUGIN_ROOT / "scripts" / "runtime-evidence.py"


def load_evals():
    return json.loads((ROOT / "evals" / "routing-cases.json").read_text())


def load_policy_contract():
    return json.loads(POLICY_CONTRACT.read_text())


def read(name):
    return (ROOT / name).read_text()


def test_eval_schema():
    schema = json.loads((ROOT / "evals" / "routing-case.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(load_evals())
    assert load_evals()["schema_version"] == "3.0"
    assert load_evals()["skill_name"] == "codex-delegate"


def test_skill_frontmatter_and_name():
    text = (SKILL_DIR / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match
    frontmatter = yaml.safe_load(match.group(1))
    assert set(frontmatter) == {"name", "description"}
    assert frontmatter["name"] == "codex-delegate"
    assert "distinct unresolved dependencies" in frontmatter["description"]
    assert "fixed Agent counts" in frontmatter["description"]
    assert "intervention gate" in frontmatter["description"].lower()


def test_openai_yaml_matches_skill():
    data = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text())
    assert data["interface"]["display_name"] == "Codex Delegate"
    assert "/codex-delegate" in data["interface"]["default_prompt"]
    assert "unresolved dependencies" in data["interface"]["default_prompt"].lower()
    assert "execution progress" in data["interface"]["default_prompt"].lower()
    assert data["policy"]["allow_implicit_invocation"] is True


def test_core_references_and_executable_helpers_exist():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    for name in [
        "delegation-contract.md",
        "execution-progress.md",
        "routing-policy.md",
        "runtime-assurance.md",
        "consent-policy.md",
        "safety-policy.md",
        "orchestration-receipt.md",
        "final-review-gate.md",
    ]:
        assert (SKILL_DIR / "references" / name).is_file()
        assert f"references/{name}" in skill
    assert not (SKILL_DIR / "references" / "task-packet.md").exists()
    assert RUNTIME_VERIFIER.is_file()
    assert (PLUGIN_ROOT / "scripts" / "review-artifact.py").is_file()


def test_runtime_docs_reference_only_shipped_verifier():
    assurance = (SKILL_DIR / "references" / "runtime-assurance.md").read_text()
    route_doc = read("docs/model-route-assurance.md")
    combined = assurance + route_doc
    assert "runtime-evidence.py" in combined
    assert "inspect-runtime.py" not in combined
    assert "verify-runtime.py" not in combined
    assert "does not scrape Codex rollout internals" in combined


def test_policy_contract_is_small_stable_constant_source():
    contract = load_policy_contract()
    assert contract["schema_version"] == 1
    assert contract["delegation"] == {
        "max_depth": 1,
        "baseline_concurrent_children": 2,
        "max_active_writers_per_workspace": 1,
    }
    assert set(contract["roles"]) == {"reader", "worker", "investigator", "advisor"}
    assert contract["final_review"]["completion_verdicts"] == ["ship", "fix-first", "rethink"]
    assert contract["final_review"]["unresolved_verdict"] == "insufficient_evidence"
    assert len(contract["final_review"]["trigger_codes"]) == len(
        set(contract["final_review"]["trigger_codes"])
    )


def test_semantic_profiles_match_policy_contract_exactly():
    contract = load_policy_contract()
    expected_files = {spec["profile_file"] for spec in contract["roles"].values()}
    assert {path.name for path in PROFILE_DIR.glob("*.toml")} == expected_files

    for spec in contract["roles"].values():
        data = tomllib.loads((PROFILE_DIR / spec["profile_file"]).read_text())
        assert data["name"] == spec["agent_type"]
        assert data["model"] == spec["model"]
        assert data["model_reasoning_effort"] == spec["effort"]
        assert data["sandbox_mode"] == spec["sandbox_intent"]
        assert data["developer_instructions"].strip()
        assert data["name"].startswith("codex_agent_team_")


def test_static_cases_use_policy_contract_routes_and_dependency_ids():
    roles = load_policy_contract()["roles"]
    for case in load_evals()["evals"]:
        dependency_ids = []
        for node in case["expected"].get("nodes", []):
            spec = roles[node["responsibility"]]
            assert node["model"] == spec["model"]
            assert node["effort"] == spec["effort"]
            assert node["agent_type"] == spec["agent_type"]
            assert node["route_assurance"] == "profile_locked"
            assert node["fork_turns"] == "none" or re.fullmatch(r"[1-9][0-9]*", node["fork_turns"])
            assert node["dependency_id"]
            dependency_ids.append(node["dependency_id"])
        assert len(dependency_ids) == len(set(dependency_ids))


def test_no_fixed_three_model_pipeline_or_hard_agent_count():
    ids = {case["id"] for case in load_evals()["evals"]}
    assert {"luna-sol-short-path", "luna-capability-gap-terra-delta", "five-independent-readers-authorized"} <= ids
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    schema = (ROOT / "evals" / "routing-case.schema.json").read_text()
    assert "Luna -> Terra -> Sol" in routing
    assert "never required" in routing
    assert "main -> Luna -> Sol -> main" in routing
    assert "no product-level hard child count" in routing.lower()
    assert '"maxItems": 4' not in schema


def test_contractability_is_upstream_of_model_selection():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    assert skill.index("## 4. Contractability Gate") < skill.index("## 6. Official Plugin boundary")
    contract = (SKILL_DIR / "references" / "delegation-contract.md").read_text()
    for field in [
        "DEPENDENCY",
        "OUTCOME",
        "SCOPE",
        "INTERFACES / DEPENDENCIES",
        "INVARIANTS",
        "DECISION RIGHTS",
        "ACCEPTANCE ORACLE",
        "VERIFICATION",
        "STOP / ESCALATE",
    ]:
        assert field in contract
    assert "do not create a writing Worker" in contract


def test_failure_classification_prevents_blind_retry_and_whole_task_terra_rework():
    contract = (SKILL_DIR / "references" / "delegation-contract.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    progress = (SKILL_DIR / "references" / "execution-progress.md").read_text()
    for phrase in ["mechanical defect", "contract gap", "execution stall", "capability gap", "judgment gap"]:
        assert phrase in (contract + routing).lower()
    assert "Low quality alone is not a Terra trigger" in contract
    assert "Terra is not a mandatory reviewer and not a generic second implementation attempt" in routing
    assert "does not define a universal retry count" in progress
    assert "Capability takes precedence over retry" in progress
    assert "Intervention Gate" in progress


def test_shared_evidence_dependency_and_recovery_state_are_explicit():
    contract = (SKILL_DIR / "references" / "delegation-contract.md").read_text()
    skill = (SKILL_DIR / "SKILL.md").read_text()
    for text in [contract, skill]:
        assert "Dependency Ledger" in text
        assert "Shared Evidence State" in text
        assert "Recovery Ledger" in text
        assert "invalidated" in text.lower()
    assert "deterministic | repository_fact | model_judgment" in contract
    assert "A file or artifact change invalidates only evidence that depends on the changed input" in contract
    assert "already `running` or `satisfied` must not receive a duplicate Agent call" in skill


def test_parallelism_consent_writer_and_depth_invariants():
    contract = load_policy_contract()["delegation"]
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (SKILL_DIR / "references" / "routing-policy.md").read_text()
    safety = (SKILL_DIR / "references" / "safety-policy.md").read_text()
    consent = (SKILL_DIR / "references" / "consent-policy.md").read_text()
    assert contract["max_depth"] == 1
    assert contract["baseline_concurrent_children"] == 2
    assert contract["max_active_writers_per_workspace"] == 1
    assert "outputs satisfy different ready dependencies" in routing
    assert "smallest useful scheduling wave" in skill
    assert "Children must not spawn further Subagents" in safety
    assert "up to 2 concurrently active justified child Agents" in consent
    assert "at most 1 active writer" in consent
    assert "does not add another numerical hard ceiling" in consent


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


def test_readmes_are_user_facing_without_arbitrary_line_budget():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "README_EN.md" in zh and "README.md" in en
    for text in [zh, en]:
        assert "```mermaid" not in text
        assert "/codex-delegate" in text
        assert "codex plugin marketplace add R-jed/codex-agent-team --ref main" in text
        assert "codex plugin add codex-agent-team@codex-agent-team" in text
        assert "Luna Reader" in text
        assert "Luna Worker" in text
        assert "Terra Investigator" in text
        assert "Sol Advisor" in text
        assert "Final Review Gate" in text
    for heading in [
        "## 1. 这个项目是什么",
        "## 2. 怎么安装",
        "## 3. 它能干什么",
        "## 4. 架构是怎么设计的",
        "## 5. 安全性怎么样",
        "## 6. 使用前需要注意什么",
    ]:
        assert heading in zh


def test_readmes_use_main_session_without_old_root_role_vocabulary():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "主会话" in zh
    assert "main session" in en.lower()
    assert "Root session" not in en
    assert "Root agent" not in en
    assert "Root" not in zh


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


def test_architecture_matches_current_final_review_and_runtime_design():
    architecture = read("docs/architecture.md")
    assurance = read("docs/model-route-assurance.md")
    native = read("docs/native-subagent-runtime.md")
    for phrase in [
        "Role identity is intentionally separate from model identity",
        "Dependency Ledger",
        "Recovery Ledger",
        "Intervention Gate",
        "no second numerical hard ceiling",
        "codex_agent_team_investigator",
        "route_evidence",
        "Final Review Gate",
        "review_artifact_id",
        "fresh Sol ship verdict",
    ]:
        assert phrase in architecture
    assert "Final Sol review remains selective, not mandatory" not in architecture
    assert "No Portable Mode" in assurance
    assert "does not define a product hard child count" in native
    assert "child progress observability" in native.lower()


def test_official_runtime_and_plugin_references_are_documented():
    refs = read("docs/openai-references.md")
    runtime = read("docs/native-subagent-runtime.md")
    installation = read("docs/plugin-installation.md")
    assert "https://developers.openai.com/codex/subagents" in refs
    assert "plugin-creator/SKILL.md" in refs
    assert "installing-and-updating.md" in refs
    assert "scripts/validate_plugin.py" in refs
    assert "spawn_agent" in runtime
    assert "delegation depth" in runtime
    assert "~/.codex/agents" in installation
    assert "active Codex-home `agents` directory" in installation
    assert "codex plugin add codex-agent-team@codex-agent-team" in installation
