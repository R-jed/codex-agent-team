from pathlib import Path
import json
import re
import tomllib

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
SKILL_DIR = PLUGIN_ROOT / "skills" / "codex-agent-team"
REF_DIR = SKILL_DIR / "references"
PROFILE_DIR = PLUGIN_ROOT / "agent-profiles"
POLICY_CONTRACT = PLUGIN_ROOT / "policy-contract.json"
RUNTIME_VERIFIER = PLUGIN_ROOT / "scripts" / "runtime-evidence.py"


def read(path: str) -> str:
    return (ROOT / path).read_text()


def load_evals():
    return json.loads((ROOT / "evals" / "routing-cases.json").read_text())


def load_policy_contract():
    return json.loads(POLICY_CONTRACT.read_text())


def test_eval_schema_and_skill_identity():
    schema = json.loads((ROOT / "evals" / "routing-case.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(load_evals())
    assert load_evals()["schema_version"] == "3.0"
    assert load_evals()["skill_name"] == "codex-delegate"

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
    assert data["policy"]["allow_implicit_invocation"] is True


def test_policy_has_one_normative_owner_per_boundary():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    expected = {
        "delegation-contract.md": "contract",
        "routing-policy.md": "routing",
        "execution-progress.md": "progress",
        "consent-policy.md": "consent",
        "safety-policy.md": "safety",
        "runtime-assurance.md": "runtime",
        "final-review-gate.md": "review",
        "orchestration-receipt.md": "receipt",
    }
    for name in expected:
        assert (REF_DIR / name).is_file()
        assert f"references/{name}" in skill

    contract = (REF_DIR / "delegation-contract.md").read_text()
    for duplicated_heading in [
        "## Dependency Ledger",
        "## Shared Evidence State",
        "## Recovery Ledger",
        "## Intervention Gate",
        "## Failure classification",
        "## Safety rules",
    ]:
        assert duplicated_heading not in contract

    assert "This file owns the responsibility contract and return packet" in contract
    assert "This file owns dependency readiness, completion-driven dispatch" in (
        REF_DIR / "routing-policy.md"
    ).read_text()


def test_only_shipped_runtime_verifier_is_referenced():
    assert RUNTIME_VERIFIER.is_file()
    assert (PLUGIN_ROOT / "scripts" / "review-artifact.py").is_file()
    assert not (SKILL_DIR / "scripts" / "inspect-runtime.py").exists()
    assert not (SKILL_DIR / "scripts" / "verify-runtime.py").exists()

    policy_surface = [SKILL_DIR / "SKILL.md", *REF_DIR.glob("*.md")]
    policy_surface += [ROOT / "docs" / "architecture.md", ROOT / "docs" / "native-subagent-runtime.md"]
    for path in policy_surface:
        text = path.read_text()
        assert "inspect-runtime.py" not in text
        assert "verify-runtime.py" not in text

    assert "runtime-evidence.py" in (REF_DIR / "runtime-assurance.md").read_text()


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
    assert len(contract["final_review"]["trigger_codes"]) == len(set(contract["final_review"]["trigger_codes"]))


def test_semantic_profiles_match_policy_contract_exactly():
    roles = load_policy_contract()["roles"]
    assert {path.name for path in PROFILE_DIR.glob("*.toml")} == {spec["profile_file"] for spec in roles.values()}

    for spec in roles.values():
        data = tomllib.loads((PROFILE_DIR / spec["profile_file"]).read_text())
        assert data["name"] == spec["agent_type"]
        assert data["model"] == spec["model"]
        assert data["model_reasoning_effort"] == spec["effort"]
        assert data["sandbox_mode"] == spec["sandbox_intent"]
        assert data["developer_instructions"].strip()
        assert data["name"].startswith("codex_agent_team_")


def test_static_cases_use_policy_contract_routes_and_unique_dependencies():
    roles = load_policy_contract()["roles"]
    for case in load_evals()["evals"]:
        ids = []
        for node in case["expected"].get("nodes", []):
            spec = roles[node["responsibility"]]
            assert node["model"] == spec["model"]
            assert node["effort"] == spec["effort"]
            assert node["agent_type"] == spec["agent_type"]
            assert node["route_assurance"] == "profile_locked"
            assert node["fork_turns"] == "none" or re.fullmatch(r"[1-9][0-9]*", node["fork_turns"])
            ids.append(node["dependency_id"])
        assert len(ids) == len(set(ids))


def test_no_fixed_pipeline_or_product_child_ceiling():
    ids = {case["id"] for case in load_evals()["evals"]}
    assert {"luna-sol-short-path", "luna-capability-gap-terra-delta", "five-independent-readers-authorized"} <= ids
    routing = (REF_DIR / "routing-policy.md").read_text()
    schema = read("evals/routing-case.schema.json")
    assert "`Luna -> Terra -> Sol` is never required" in routing
    assert "no product-level hard child count" in routing.lower()
    assert '"maxItems": 4' not in schema


def test_completion_driven_ready_frontier_is_explicit_across_kernel_and_docs():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (REF_DIR / "routing-policy.md").read_text()
    architecture = read("docs/architecture.md")
    runtime = read("docs/native-subagent-runtime.md")

    for text in [skill, routing, architecture, runtime]:
        assert "completion-driven" in text.lower()
        assert "ready frontier" in text.lower()
        assert "join dependency" in text.lower()

    assert "refill newly free capacity" in skill
    assert "start C while A is still running" in routing
    assert "Avoid model-mediated busy polling" in routing
    assert "barrier_only" in runtime
    assert "any_child_update" in runtime


def test_contractability_is_upstream_of_writing_delegation():
    contract = (REF_DIR / "delegation-contract.md").read_text()
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
        "RETURN",
    ]:
        assert field in contract
    assert "do not create a writing Worker" in contract
    assert "Do not resend an unchanged contract after failure" in contract


def test_recovery_is_owned_by_execution_progress_and_prevents_blind_retry():
    progress = (REF_DIR / "execution-progress.md").read_text()
    routing = (REF_DIR / "routing-policy.md").read_text()
    for phrase in ["mechanical defect", "contract gap", "execution stall", "capability gap", "judgment gap"]:
        assert phrase in progress.lower()
    assert "does not define a universal retry count" in progress
    assert "Capability takes precedence over retry" in progress
    assert "Intervention Gate" in progress
    assert "Low quality alone is not a Terra trigger" in routing


def test_evidence_and_recovery_state_are_explicit_without_duplicate_policy_owners():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    contract = (REF_DIR / "delegation-contract.md").read_text()
    progress = (REF_DIR / "execution-progress.md").read_text()
    assert "Dependency Ledger" in skill
    assert "Shared Evidence State" in skill
    assert "Recovery Ledger" in skill
    assert "type: deterministic | repository_fact | model_judgment" in contract
    assert "Recovery Ledger" in progress
    assert "already `running` or `satisfied` must not receive duplicate inference" in skill


def test_parallelism_consent_writer_and_depth_invariants():
    delegation = load_policy_contract()["delegation"]
    routing = (REF_DIR / "routing-policy.md").read_text()
    safety = (REF_DIR / "safety-policy.md").read_text()
    consent = (REF_DIR / "consent-policy.md").read_text()
    assert delegation["max_depth"] == 1
    assert delegation["baseline_concurrent_children"] == 2
    assert delegation["max_active_writers_per_workspace"] == 1
    assert "Completion-driven dispatch" in routing
    assert "Children must not spawn further Subagents" in safety
    assert "up to 2 concurrently active justified child Agents" in consent
    assert "at most 1 active writer" in consent
    assert "does not add another numerical hard ceiling" in consent


def test_route_assurance_has_no_portable_mode():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    routing = (REF_DIR / "routing-policy.md").read_text()
    runtime = (REF_DIR / "runtime-assurance.md").read_text()
    for text in [routing, runtime]:
        assert "profile_locked" in text
        assert "native_explicit_validated" not in text
    assert "There is no Portable Mode" in routing
    assert "Portable Mode" in skill


def test_readmes_are_release_ready_user_product_docs():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "README_EN.md" in zh and "README.md" in en

    for text in [zh, en]:
        lower = text.lower()
        assert "```mermaid" not in text
        assert "/codex-delegate" in text
        assert "HEADOFF.md" not in text
        assert "LOCAL_VALIDATION_REPORT.md" not in text
        assert "Final Review" in text
        assert "Native Subagents" in text
        assert "status-pre--v1" not in text
        assert "pre-v1" not in lower
        assert "release validation" not in lower
        assert "live pending" not in lower
        assert "ready frontier" not in lower
        assert "intervention gate" not in lower
        assert "recovery ledger" not in lower
        assert "review_artifact_id" not in lower

    for heading in [
        "## 为什么用 Codex Delegate",
        "## 安装",
        "## 模型分工",
        "## 并行工作",
        "## 失败时怎么处理",
        "## Final Review",
        "## 安全边界",
    ]:
        assert heading in zh

    for heading in [
        "## Why Codex Delegate",
        "## Installation",
        "## Models and roles",
        "## Parallel work",
        "## When work goes wrong",
        "## Final Review",
        "## Safety",
    ]:
        assert heading in en


def test_readmes_use_main_session_without_old_root_role_vocabulary():
    zh = read("README.md")
    en = read("README_EN.md")
    assert "主会话" in zh
    assert "main session" in en.lower()
    assert "Root session" not in en
    assert "Root agent" not in en
    assert "Root" not in zh


def test_chinese_readme_avoids_em_dash_and_spacing_regressions():
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


def test_architecture_matches_current_runtime_and_final_review_design():
    architecture = read("docs/architecture.md")
    runtime = read("docs/native-subagent-runtime.md")
    for phrase in [
        "smallest useful compute graph on the shortest safe critical path",
        "Completion-driven scheduling",
        "Dependency Ledger",
        "Recovery Ledger",
        "Final Review Gate",
        "review_artifact_id",
        "route_evidence",
    ]:
        assert phrase in architecture
    assert "Completion-driven scheduling contract" in runtime
    assert "child-progress observability" in runtime.lower()


def test_official_runtime_and_plugin_references_are_documented():
    refs = read("docs/openai-references.md")
    installation = read("docs/plugin-installation.md")
    assert "https://developers.openai.com/codex/subagents" in refs
    assert "plugin-creator/SKILL.md" in refs
    assert "installing-and-updating.md" in refs
    assert "scripts/validate_plugin.py" in refs
    assert "~/.codex/agents" in installation
    assert "active Codex-home `agents` directory" in installation
    assert "codex plugin add codex-agent-team@codex-agent-team" in installation
