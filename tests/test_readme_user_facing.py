from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text()
EN = (ROOT / "README_EN.md").read_text()
AI = (ROOT / "README_AI.md").read_text()
EVALS = (ROOT / "evals" / "README.md").read_text()
ALL_READMES = [path.read_text() for path in ROOT.rglob("README*.md")]
DIRECTIVE = "If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly."
CANONICAL_MARKETPLACE = "codex plugin marketplace add R-jed/codex-delegate@main"
PLUGIN_ADD = "codex plugin add codex-delegate@codex-delegate"
UPGRADE = "codex plugin marketplace upgrade codex-delegate"


def test_public_readmes_keep_current_identity_roles_and_entrypoint():
    for text in [ZH, EN]:
        for phrase in [
            "codex delegate",
            "1.1.0",
            "$codex-delegate:codex-delegate",
            "Luna Reader",
            "Luna Worker",
            "Sol Solver",
            "Terra Investigator",
            "Sol Advisor",
            DIRECTIVE,
        ]:
            assert phrase in text


def test_public_readmes_distinguish_marketplace_and_command_line_installation():
    for text in [ZH, EN]:
        assert CANONICAL_MARKETPLACE in text
        assert "--sparse .agents/plugins" in text
        assert "--sparse plugins/codex-delegate" in text
        assert "&& \\\n" in text
        assert PLUGIN_ADD in text
        assert UPGRADE in text
        assert "$codex-delegate:codex-delegate" in text
        assert "/plugins" in text
        assert "/skills" in text
        assert "--ref main" not in text
        assert "codex-delegate" in text

    for phrase in [
        "## 安装",
        "### 方式一：Codex 插件市场",
        "搜索 `codex-delegate`",
        "### 方式二：命令行安装",
        "## 更新",
        "### 插件市场",
        "### 命令行",
    ]:
        assert phrase in ZH

    for phrase in [
        "## Installation",
        "### Option 1: Codex Plugin Marketplace",
        "Search for `codex-delegate`",
        "### Option 2: Command-line installation",
        "## Update",
        "### Plugin Marketplace",
        "### Command line",
    ]:
        assert phrase in EN


def test_public_install_docs_do_not_expose_legacy_source_migration():
    for text in [ZH, EN, AI]:
        lowered = text.lower()
        for phrase in [
            "already added from a different source",
            "source conflict repair",
            "source mismatch",
            "marketplace remove codex-delegate",
            "old source",
            "historical installation",
        ]:
            assert phrase not in lowered

    assert "旧来源" not in ZH
    assert "旧来源修复" not in ZH


def test_public_readmes_use_plain_language_and_leader_model():
    forbidden = [
        "material judgment",
        "judgment-coupled",
        "bounded read-heavy",
        "capability dedup",
        "orchestration receipt",
        "runtime ontology",
        "consent envelope",
        "dependency ledger",
        "shared evidence state",
        "recovery ledger",
    ]
    for text in [ZH, EN]:
        lowered = text.lower()
        for phrase in forbidden:
            assert phrase not in lowered

    assert "给主会话的一套带团队规则" in ZH
    assert "small set of team-leading rules" in EN
    assert "你不需要自己挑模型" in ZH
    assert "You do not need to choose models" in EN
    assert "不预设固定 Agent 数量" in ZH
    assert "does not choose a fixed Agent count" in EN
    assert "不是需要填满的目标" in ZH
    assert "not a target to fill" in EN


def test_all_readmes_are_product_or_reference_docs_not_release_status_ledgers():
    forbidden = [
        "HEADOFF.md",
        "LOCAL_VALIDATION_REPORT.md",
        "validation pending",
        "hold for release",
        "pre-release",
        "pre release",
        "release candidate",
        "release posture:",
        "ready for checkpoint",
        "checkpoint 1",
        "checkpoint 2",
        "checkpoint 3",
        "checkpoint 4",
        "checkpoint 5",
        "checkpoint 6",
        "known open reproducible project",
        "P0/P1",
        "review_artifact_id",
    ]
    for text in ALL_READMES:
        lowered = text.lower()
        for phrase in forbidden:
            assert phrase.lower() not in lowered


def test_ai_reference_keeps_exact_machine_facts_and_clean_install_contract():
    for phrase in [
        "R-jed/codex-delegate",
        "Repo marketplace id: codex-delegate",
        "Explicit invocation: $codex-delegate:codex-delegate",
        "Current version:     1.1.0",
        "Distribution:        Codex Plugin",
        "codex_delegate_reader",
        "codex_delegate_worker",
        "codex_delegate_solver",
        "codex_delegate_investigator",
        "codex_delegate_advisor",
        ".codex-delegate-agents.json",
        "router-core.md",
        "team-plan.md",
        "recovery.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json` schema `4`",
        "Implicit invocation is disabled",
        CANONICAL_MARKETPLACE,
        "--sparse .agents/plugins",
        "--sparse plugins/codex-delegate",
        "Explain two installation methods clearly",
        "Plugin Marketplace",
        "Command line",
        "search for `codex-delegate`",
        "/plugins",
        "For update questions",
        "Do not claim benchmark wins",
    ]:
        assert phrase in AI

    for phrase in [
        "Treat the current Codex main session as the team leader",
        "Do not ask the user to design the Agent team",
        "Main manages a ready frontier and uses progressive fan-out",
        "Spare capacity is never a reason to spawn",
        "Child count alone is not a consent trigger",
        "preserve that workflow as task truth",
        "Filesystem isolation is necessary for simultaneous writers and does not by itself prove semantic independence",
        "MUTATION AUTHORITY: none | declared-output-only | bounded-source-write",
        "INTEGRATION AFTER",
        "Requested is not accepted. Accepted is not observed",
        "UNKNOWN is not FAILED",
        "two Agent attempts",
        "validate_team_plan.py",
        "validate_team_ledger.py",
        "evals/coordination-cases.json",
    ]:
        assert phrase in AI


def test_evals_readme_is_short_maintainer_reference_and_not_runtime_policy():
    for phrase in [
        "test data used to check routing, coordination, recovery, and runtime behavior",
        "not part of the normal user setup",
        "behavioral-workloads.json",
        "behavioral-result.schema.json",
        "LOCAL_EVAL_FIXTURE_TEMPLATE.md",
        "routing-cases.json",
        "coordination-cases.json",
        "runtime-assurance-cases.json",
        "adaptive multi-Agent fan-out",
        "does not use a fixed ordinary child-Agent count",
        "upstream workflow ownership",
        "semantic independence",
        "mutation authority",
        "integration ordering",
        "requested/accepted/observed route truth",
        "do not control how the plugin routes or coordinates work",
        "router-core.md",
        "team-plan.md",
        "recovery.md",
        "guardrails.md",
        "final-review.md",
        "policy-contract.json",
        "tests/test_team_plan.py",
        "tests/test_recovery_policy.py",
        "../docs/behavioral-evals.md",
    ]:
        assert phrase in EVALS


def test_public_readmes_cover_first_use_parallel_writing_and_independent_review():
    for phrase in [
        "第一次需要子 Agent 时",
        "同一个实际 Git checkout 里，同一时间只允许一个写入者",
        "什么时候会再做一次独立复核",
        "新的 Sol Advisor 做独立复核",
        "实质验证缺口",
    ]:
        assert phrase in ZH
    for phrase in [
        "First time a child Agent is needed",
        "Only one actor writes to the same physical Git checkout at a time",
        "When it asks for one more review",
        "A fresh Sol Advisor is required",
        "a meaningful verification gap",
    ]:
        assert phrase in EN


def test_public_readmes_link_to_deeper_docs_without_exposing_maintainer_ledgers():
    for text in [ZH, EN]:
        for link in [
            "README_AI.md",
            "docs/plugin-installation.md",
            "docs/architecture.md",
            "docs/native-subagent-runtime.md",
        ]:
            assert link in text
        assert "[README_AI.md](README_AI.md)" in text
        assert "HEADOFF.md" not in text
        assert "LOCAL_VALIDATION_REPORT.md" not in text


def test_all_readmes_expose_only_current_project_identity():
    retired_tokens = (
        "codex" + "-agent-team",
        "codex" + "_agent_team_",
        "." + "codex" + "-agent-team-",
    )
    for text in ALL_READMES:
        assert all(token not in text for token in retired_tokens)


def test_visual_assets_remain_bounded():
    for text in [ZH, EN]:
        assert "<picture" in text and "logo" in text
        for line in text.splitlines():
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                raise AssertionError(f"Unexpected README image: {line}")
