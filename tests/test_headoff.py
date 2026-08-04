from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "HEADOFF.md"
REPORT = ROOT / "LOCAL_VALIDATION_REPORT.md"


def test_local_runtime_handoff_is_an_internal_release_contract():
    assert HANDOFF.is_file()
    assert REPORT.is_file()
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text()
        assert "HEADOFF.md" not in text
        assert "LOCAL_VALIDATION_REPORT.md" not in text


def test_handoff_protects_release_critical_live_validation_scope():
    text = HANDOFF.read_text()
    for phrase in [
        "# Codex Delegate Local Runtime Validation Handoff",
        "## Current checkpoint",
        "Accepted v0.6.0 static product baseline",
        "## v0.6.0 control model",
        "## Stop line",
        "# Completed repository work",
        "## E. Final Review Gate static closure",
        "# Pending live validation",
        "## Checkpoint 1: exact roles and Runtime Truth",
        "incomplete expected route -> fail closed",
        "## Checkpoint 3: dependency scheduling, evidence reuse, intervention, and recovery",
        "### 7. Intervention Gate and recovery",
        "### 8. Child progress observability",
        "## Checkpoint 4: product-value and final-review experiments",
        "### 9. Raw prompt versus compiled contract",
        "### 11. Selective and mandatory fresh-context Sol experiments",
        "## Checkpoint 5: adaptive resources, consent, multi-session safety, and lifecycle",
        "### 14. Workspace-scoped one-writer and multi-session matrix",
        "## Checkpoint 6: official Plugin install, migration, and installer concurrency",
        "### 15. Current official Plugin contract validation",
        "### 17. Filesystem and concurrent installer matrix",
        "# Defect triage",
        "# Definition of Done for v1.0.0",
        "# v1.0.0 release execution plan",
        "# Required validation artifact",
        "# Feedback protocol for continued adversarial review",
        "# Completion condition",
        "LOCAL_VALIDATION_REPORT.md",
        "RELEASE CANDIDATE",
        "HOLD FOR RELEASE / LIVE VALIDATION PENDING",
    ]:
        assert phrase in text

    assert "[x]" in text
    assert "[ ]" in text
    assert "CAT-LOCAL-001" in text
    assert "Do not add a Checkpoint 7" in text


def test_handoff_keeps_adaptive_fanout_without_product_hard_ceiling():
    text = HANDOFF.read_text()
    for phrase in [
        "no fixed Agent count and no product-level hard child ceiling",
        "up to 2 concurrently active justified children without another prompt",
        "larger simultaneous fan-out -> consent unless already authorized",
        "native slot shortage -> queue/serialize ready work",
        "F4 >=5 authorized independent read-only dependencies",
        "no product hard 4 ceiling",
        "observed native capacity",
        "runtime slot waits",
    ]:
        assert phrase in text

    for forbidden in [
        "normal max 2, v1 hard max 4",
        "main-session child envelope = normal max 2",
        "v1 hard maximum of four children",
    ]:
        assert forbidden not in text


def test_handoff_requires_intervention_recovery_and_observability_validation():
    text = HANDOFF.read_text()
    for phrase in [
        "Dependency Ledger and ready frontier",
        "A running dependency does not receive duplicate inference",
        "Healthy incomplete case",
        "False-progress case",
        "Same failure signature with no new evidence -> execution stall",
        "Clean same-lane restart uses fresh context",
        "Semantic cycle case `hypothesis A -> B -> A`",
        "Evidence-supported capability gap -> Terra receives unresolved delta before repeated same-lane retry",
        "Proposed recovery action remains separate from effective action and decision source",
        "child-progress observability",
        "intervention_gate_evaluations",
        "recovery_ledger_entries",
        "attempt_cycle_detected",
        "same_failure_without_new_evidence",
        "material Terra escalation or material recovery dynamically promotes Final Review Gate state",
    ]:
        assert phrase in text


def test_handoff_requires_final_review_gate_live_validation():
    text = HANDOFF.read_text()
    for phrase in [
        "Final Review Gate required -> main-session acceptance creates Candidate Ready only",
        "required gate completion -> fresh Sol ship + unchanged review_artifact_id",
        "fix-first -> correction + re-verification + new artifact + new fresh review",
        "rethink -> invalidate affected architecture/contract assumptions",
        "INSUFFICIENT_EVIDENCE -> gate unresolved",
        "Post-review deliverable mutation makes `--verify` fail",
        "A declined additional required review keeps `Candidate Ready`",
        "FINAL REVIEW REQUIREMENT / REASONS / ARTIFACT / VERDICT",
        "FINAL_REVIEW_STATE",
        "Final Review Gate smoke covering required trigger",
    ]:
        assert phrase in text

    assert "no universal Sol review stage for low-risk work" in text
    assert "no required Final Review Gate silently downgraded" in text
    assert "no old `ship` retained after any deliverable mutation" in text
    assert "no `INSUFFICIENT_EVIDENCE` converted into `ship` or `fix-first`" in text


def test_handoff_requires_official_plugin_validation_and_v060_upgrade():
    text = HANDOFF.read_text()
    for phrase in [
        "plugin-creator/scripts/validate_plugin.py",
        "codex plugin marketplace add R-jed/codex-agent-team --ref main",
        "--sparse .agents/plugins",
        "--sparse plugins/codex-agent-team",
        "codex plugin add codex-agent-team@codex-agent-team",
        "Start a new Codex thread after install/reinstall",
        "$CODEX_HOME/agents",
        "Starting from real v0.3.x Codex Agent Team",
        "Starting from real v0.4.x Codex Delegate",
        "Starting from v0.5.0/v0.5.1, update/reinstall v0.6.0",
        "metadata reports `0.6.0`",
        "scripts/review-artifact.py",
        "Cosmetic alignment cannot block v1",
    ]:
        assert phrase in text


def test_handoff_requires_paired_control_fingerprints_and_review_metrics():
    text = HANDOFF.read_text()
    for field in [
        "workload_definition_hash",
        "main_session_route",
        "worker_route",
        "permissions_fingerprint",
        "tool_surface_fingerprint",
        "acceptance_rubric_id",
        "final_review_requirement",
        "final_review_trigger_reasons",
        "final_review_attempts",
        "final_review_verdict",
        "final_review_gate_satisfied",
        "review_artifact_verify_failures",
        "post_review_mutations",
        "review_yield",
    ]:
        assert field in text


def test_handoff_defines_adversarial_feedback_packets():
    text = HANDOFF.read_text()
    for phrase in [
        "`gpt56-sol-pro-consult` is the required adversarial consultation mechanism",
        "Review Checkpoints A-E",
        "immediately after any P0/P1 candidate",
        "Codex remains the local executor",
        "must not be counted as evidence that Codex Delegate itself routed correctly",
        "Do not replace this consultation with an ad hoc generic Sol call",
    ]:
        assert phrase in text

    for field in [
        "COMPLETED_HEADOFF_ITEMS",
        "NEW_EVIDENCE",
        "DEPENDENCY_STATE",
        "EXECUTION_PROGRESS",
        "RECOVERY_STATE",
        "FINAL_REVIEW_STATE",
        "RESOURCE_STATE",
        "PLUGIN_STATE",
        "DEFECTS",
        "TESTS",
        "CHANGES",
        "UNRESOLVED",
        "LOCAL_JUDGMENT",
        "ASK",
    ]:
        assert field in text


def test_handoff_targets_existing_project_chatgpt_conversation_fail_closed():
    text = HANDOFF.read_text()
    for phrase in [
        "/gpt56-sol-pro-consult",
        "## Project consultation target",
        "TARGET_CHATGPT_CONVERSATION_TITLE",
        "分支 · 分支 · 项目对比分析",
        "continue_existing_conversation",
        "exact_title_unique_match",
        "CONSULTATION_TARGET_UNRESOLVED",
        "Do not create a replacement ChatGPT conversation",
        "Do not silently fall back to an isolated consultation conversation",
        "project discussion",
        "The target contract does not replace any transport-level `task_id`, sentinel, safety scan",
    ]:
        assert phrase in text

    lines = text.splitlines()
    assert "conversation_title: 分支 · 项目对比分析" not in lines
    assert "分支 · 项目对比分析" not in lines
    assert "fuzzy match" in text
    assert "model_judgment" in text


def test_handoff_has_a_finite_release_finish_line():
    text = HANDOFF.read_text()
    assert "The remaining job is finite" in text
    assert "When items 1-12 are satisfied, the required action is **release v1.0.0**" in text
    assert "remaining P2/P3 work moves post-v1" in text
    assert "Luna Max / Terra XHigh / Sol High remain the frozen v1 routing baseline" in text
    assert "Cosmetic alignment cannot block v1" in text
    for stage in ["## Stage R1", "## Stage R2", "## Stage R3", "## Stage R4"]:
        assert stage in text


def test_handoff_requires_cross_session_workspace_validation_without_global_locking():
    text = HANDOFF.read_text()
    for phrase in [
        "M1 different sessions, different projects/checkouts",
        "M2 different sessions, same repository, isolated worktrees",
        "M3 different sessions, same canonical physical checkout",
        "M4 one writing session + one read-only session same checkout",
        "Do not implement a workspace lock before M3 establishes a reproducible failure",
    ]:
        assert phrase in text


def test_handoff_requires_concurrent_installer_validation_before_locking():
    text = HANDOFF.read_text()
    for phrase in [
        "I1 same clean CODEX_HOME",
        "I2 one installer forced to fail after mutation begins while peer succeeds",
        "peer-success state",
        "I3 different managed profile generations compete in one CODEX_HOME",
        "Do not add an inter-process installer lock merely because races are theoretically possible",
    ]:
        assert phrase in text


def test_validation_report_separates_v060_static_evidence_from_historical_live_evidence():
    text = REPORT.read_text()
    for phrase in [
        "Plugin version: 0.6.0",
        "Validated workflow: 30876233050",
        "pytest: 164 passed",
        "Accepted v0.6.0 static evidence",
        "Accepted v0.5.1 historical static evidence",
        "That live baseline predates v0.6.0",
        "review_artifact_id",
        "contract_luna_final_review_gate",
        "HOLD FOR RELEASE / LIVE VALIDATION PENDING",
        "ARCHITECTURE FROZEN AT v0.6.0",
    ]:
        assert phrase in text

    assert "No live result yet proves that mandatory Final Review Gate use improves product outcomes" in text
