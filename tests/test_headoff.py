from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "HEADOFF.md"
REPORT = ROOT / "LOCAL_VALIDATION_REPORT.md"


def test_local_runtime_handoff_is_internal_release_contract():
    assert HANDOFF.is_file()
    assert REPORT.is_file()
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text()
        assert "HEADOFF.md" not in text
        assert "LOCAL_VALIDATION_REPORT.md" not in text


def test_handoff_has_finite_six_checkpoint_release_plan():
    text = HANDOFF.read_text()
    assert "# Codex Delegate Local Runtime Validation Handoff" in text
    assert "Accepted v0.6.0 static product baseline" in text
    for checkpoint in range(1, 7):
        assert f"## Checkpoint {checkpoint}:" in text
    assert "Checkpoint 7" in text and "Do not add a Checkpoint 7" in text
    for stage in ["## Stage R1", "## Stage R2", "## Stage R3", "## Stage R4"]:
        assert stage in text
    assert "# Definition of Done for v1.0.0" in text
    assert "When items 1-12 are satisfied, the required action is **release v1.0.0**" in text
    assert "remaining job is finite" in text.lower()


def test_handoff_keeps_adaptive_resource_model():
    text = HANDOFF.read_text()
    for phrase in [
        "no fixed Agent count",
        "up to 2 concurrently active justified children without another prompt",
        "larger fan-out authorized",
        "no product hard 4 ceiling",
        "observed native capacity",
        "runtime slot waits",
        "one active writer per canonical physical checkout",
    ]:
        assert phrase in text
    for forbidden in [
        "normal max 2, v1 hard max 4",
        "v1 hard maximum of four children",
    ]:
        assert forbidden not in text


def test_handoff_runtime_evidence_uses_shipped_normalized_verifier():
    text = HANDOFF.read_text()
    assert "plugins/codex-agent-team/scripts/runtime-evidence.py" in text
    assert "incomplete expected route -> fail closed" in text
    assert "complete matching native route -> R1" in text
    assert "hard read-only required + native sandbox absent -> return to main session" in text
    assert "Do not introduce a project rollout-file scraper" in text
    assert "inspect-runtime.py" not in text
    assert "verify-runtime.py" not in text


def test_handoff_requires_completion_driven_frontier_refill_characterization():
    text = HANDOFF.read_text()
    for phrase in [
        "Completion-driven frontier refill",
        "A = slow independent dependency",
        "B = fast independent dependency",
        "C = depends only on B",
        "start C before A finishes",
        "barrier serialization",
        "barrier_only",
        "per_child_terminal",
        "any_child_update",
        "model-mediated polling",
        "independent main-session work",
    ]:
        assert phrase in text


def test_handoff_requires_intervention_recovery_and_observability_validation():
    text = HANDOFF.read_text()
    for phrase in [
        "Dependency scheduling",
        "Evidence reuse",
        "Intervention Gate and recovery",
        "Healthy incomplete case",
        "False-progress case",
        "same failure signature with no new evidence",
        "hypothesis A -> B -> A",
        "Capability gap",
        "proposed recovery action remains separate from effective action",
        "none",
        "terminal_only",
        "periodic_summary",
        "structured_live",
    ]:
        assert phrase in text


def test_handoff_requires_final_review_gate_live_lifecycle():
    text = HANDOFF.read_text()
    for phrase in [
        "Candidate Ready",
        "fresh Advisor route",
        "exact review_artifact_id handoff",
        "ship | fix-first | rethink",
        "INSUFFICIENT_EVIDENCE -> gate unresolved",
        "fix-first -> correction + re-verification + new artifact + new fresh review",
        "rethink -> invalidate affected architecture/contract assumptions",
        "post-review deliverable mutation",
        "required Final Review Gate is never silently downgraded",
        "no old `ship` is retained after any deliverable mutation",
    ]:
        assert phrase in text


def test_handoff_requires_real_plugin_install_upgrade_and_installer_concurrency():
    text = HANDOFF.read_text()
    for phrase in [
        "plugin-creator/scripts/validate_plugin.py",
        "codex plugin marketplace add R-jed/codex-agent-team --ref main",
        "--sparse .agents/plugins",
        "--sparse plugins/codex-agent-team",
        "codex plugin marketplace upgrade codex-agent-team",
        "codex plugin add codex-agent-team@codex-agent-team",
        "start a new Codex thread",
        "marketplace upgrade` followed by explicit `plugin add` refreshes the installed Plugin bytes",
        "I1 two installers target the same clean CODEX_HOME",
        "I2 one installer fails after mutation begins while a peer succeeds",
        "I3 two different managed profile generations compete in one CODEX_HOME",
        "Do not add an inter-process installer lock",
    ]:
        assert phrase in text


def test_handoff_multi_session_writer_matrix_is_evidence_driven():
    text = HANDOFF.read_text()
    for phrase in [
        "M1 different sessions, different projects/checkouts",
        "M2 different sessions, same repository, isolated worktrees",
        "M3 different sessions, same canonical physical checkout",
        "M4 one writing session + one read-only session same checkout",
        "Do not implement a workspace lock before M3 establishes a reproducible failure",
    ]:
        assert phrase in text


def test_handoff_targets_existing_project_chatgpt_conversation_fail_closed():
    text = HANDOFF.read_text()
    for phrase in [
        "Review Checkpoints A-E",
        "Codex remains the local executor",
        "model_judgment",
        "/gpt56-sol-pro-consult",
        "## Project consultation target",
        "TARGET_CHATGPT_CONVERSATION_TITLE: 分支 · 分支 · 项目对比分析",
        "TARGET_MODE: continue_existing_conversation",
        "MATCH_POLICY: exact_title_unique_match",
        "CONSULTATION_TARGET_UNRESOLVED",
        "do not fuzzy match",
        "do not create a replacement ChatGPT conversation",
        "do not silently fall back to an isolated consultation conversation",
        "The target contract does not replace any transport-level `task_id`, sentinel, safety scan",
        "must not be counted as evidence that Codex Delegate itself routed correctly",
    ]:
        assert phrase in text
    lines = text.splitlines()
    assert "conversation_title: 分支 · 项目对比分析" not in lines
    assert "分支 · 项目对比分析" not in lines


def test_validation_report_reflects_merged_v060_baseline_and_consolidation():
    text = REPORT.read_text()
    for phrase in [
        "Plugin version: 0.6.0",
        "Accepted v0.6.0 feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed",
        "workflow: 30879802677",
        "pytest: 167 passed",
        "Accepted v0.6.0 static evidence",
        "Accepted engineering-consolidation static evidence",
        "Accepted engineering-consolidation merge: 6ae52d47f6416087f4a7c7e314bef6d0204a129f",
        "Exact tested consolidation head: ac5976d41e44a7ffddb3dad94686c2729c4b6687",
        "Consolidation workflow: 30886554206",
        "pytest: 157 passed",
        "Accepted v0.5.1 historical static evidence",
        "That live baseline predates v0.6.0",
        "review_artifact_id",
        "contract_luna_final_review_gate",
        "HOLD FOR RELEASE / LIVE VALIDATION PENDING",
        "ARCHITECTURE FROZEN AT v0.6.0",
        "ENGINEERING CONSOLIDATION COMPLETE",
    ]:
        assert phrase in text
    assert "Current engineering-consolidation candidate" not in text
    assert "Current feature PR: #27" not in text
