from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = (ROOT / "README.md").read_text()
EN = (ROOT / "README_EN.md").read_text()
AI = (ROOT / "README_AI.md").read_text()
EVALS = (ROOT / "evals" / "README.md").read_text()
ALL_READMES = [path.read_text() for path in ROOT.rglob("README*.md")]
DIRECTIVE = "If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly."


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


def test_public_readmes_use_repo_marketplace_until_public_listing_is_verified():
    assert "当前可靠的安装方式" in ZH
    assert "GitHub 仓库注册为 Codex repo marketplace" in ZH
    assert "The current reliable installation path" in EN
    assert "register this GitHub repository as a Codex repo marketplace" in EN

    for text in [ZH, EN]:
        assert "codex plugin marketplace add R-jed/codex-delegate --ref main" in text
        assert "codex plugin add codex-delegate@codex-delegate" in text
        assert "$codex-delegate:codex-delegate" in text
        assert "/skills" in text
        assert "Plugins Directory" in text

    assert "OpenAI Platform 提交、审核并由开发者 Publish" in ZH
    assert "submitted through the OpenAI Platform, approved, and published by the developer" in EN
    assert "在 Codex 中打开**插件市场**，搜索 `codex-delegate`" not in ZH
    assert "Open the **Codex Plugin Marketplace**, search for `codex-delegate`" not in EN


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

    assert "给主会话的一套“带团队规则”" in ZH
    assert "small set of team-leading rules" in EN
    assert "你不需要自己挑模型" in ZH
    assert "You do not need to pick models yourself" in EN
    assert "没有固定的子 Agent 数量" in ZH
    assert "does not have a fixed child-Agent count" in EN
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


def test_ai_reference_keeps_exact_machine_facts_without_false_public_listing_claims():
    for phrase in [
        "R-jed/codex-delegate",
        "Repo marketplace id:    codex-delegate",
        "Explicit invocation:    $codex-delegate:codex-delegate",
        "Current version:        1.1.0",
        "Public directory state: do not assume published; verify a current OpenAI listing first",
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
        "Repo/local marketplace packaging does not prove public Plugins Directory publication",
        "verify the current public listing first",
    ]:
        assert phrase in AI

    assert "search for `codex-delegate` in the Codex Plugin Marketplace" not in AI


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
        "必须再找一个新的 Sol Advisor 做独立复核",
        "实质验证缺口",
        "Luna 做得不好不会自动升级到 Terra",
    ]:
        assert phrase in ZH
    for phrase in [
        "First time a child Agent is needed",
        "only one actor writes to the same physical Git checkout at a time",
        "When it asks for one more review",
        "A fresh Sol Advisor is required",
        "a meaningful verification gap",
        "Weak Luna output does not automatically send the task to Terra",
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
