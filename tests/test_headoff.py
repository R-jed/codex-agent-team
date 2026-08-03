from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "HEADOFF.md"


def test_local_runtime_handoff_is_an_internal_release_contract():
    assert HANDOFF.is_file()
    for name in ["README.md", "README_EN.md"]:
        assert "HEADOFF.md" not in (ROOT / name).read_text()


def test_handoff_protects_release_critical_live_validation_scope():
    text = HANDOFF.read_text()
    for phrase in [
        "# Codex Delegate Local Runtime Validation Handoff",
        "## Current checkpoint",
        "## v0.5.0 control model",
        "## Stop line",
        "# Completed repository work",
        "# Pending live validation",
        "## Checkpoint 1: exact roles and Runtime Truth",
        "incomplete expected route -> fail closed",
        "## Checkpoint 3: dependency scheduling, evidence reuse, and execution recovery",
        "### 7. Execution-progress and stall recovery",
        "## Checkpoint 4: product-value experiments",
        "### 8. Raw prompt versus compiled contract",
        "### 10. Selective fresh-context Sol experiment",
        "## Checkpoint 5: adaptive resources, multi-session safety, and lifecycle",
        "### 13. Workspace-scoped one-writer and multi-session matrix",
        "## Checkpoint 6: installer and version migration",
        "### 15. Filesystem and concurrent installer matrix",
        "# Defect triage",
        "# Definition of Done for v1.0.0",
        "# v1.0.0 release execution plan",
        "# Required validation artifact",
        "# Feedback protocol for continued adversarial review",
        "# Completion condition",
        "LOCAL_VALIDATION_REPORT.md",
        "RELEASE CANDIDATE",
        "HOLD FOR RELEASE / VALIDATION INCOMPLETE",
    ]:
        assert phrase in text

    assert "[x]" in text
    assert "[ ]" in text
    assert "CAT-LOCAL-001" in text


def test_handoff_removes_fixed_child_ceiling_and_defines_adaptive_fanout():
    text = HANDOFF.read_text()
    for phrase in [
        "no fixed Agent count and no product-level hard child ceiling",
        "up to 2 concurrently active justified children without another prompt",
        "larger simultaneous fan-out -> consent unless already authorized",
        "native slot shortage -> queue/serialize ready work",
        "F4 at least five independent read-only ready dependencies",
        "Codex Delegate imposes no hard 4 ceiling",
        "observed_child_capacity",
        "runtime_slot_waits",
    ]:
        assert phrase in text

    for forbidden in [
        "normal max 2, v1 hard max 4",
        "main-session child envelope = normal max 2",
        "v1 hard maximum of four children",
    ]:
        assert forbidden not in text


def test_handoff_requires_dependency_and_execution_progress_validation():
    text = HANDOFF.read_text()
    for phrase in [
        "Dependency Ledger and ready frontier",
        "A running dependency does not receive duplicate inference",
        "Same failure signature with no new evidence -> execution stall",
        "Clean same-lane restart uses fresh context",
        "Evidence-supported capability gap -> Terra receives the unresolved delta before repeated same-lane retry",
        "execution_stall_events",
        "clean_same_lane_restarts",
        "unjustified_retry_calls",
        "same_failure_without_new_evidence",
    ]:
        assert phrase in text


def test_handoff_requires_v05_upgrade_and_entrypoint_validation():
    text = HANDOFF.read_text()
    for phrase in [
        "Starting from real v0.3.x Codex Agent Team",
        "Starting from real v0.4.x Codex Delegate",
        "update to v0.5.0",
        "fresh v0.5.0 install presents `Codex Delegate`",
        "Characterize old `/codex-agent-team` invocation after upgrade",
        "metadata reports `0.5.0`",
        "Cosmetic alignment cannot block v1",
    ]:
        assert phrase in text


def test_handoff_requires_paired_control_fingerprints():
    text = HANDOFF.read_text()
    for field in [
        "workload_definition_hash",
        "main_session_route",
        "worker_route",
        "permissions_fingerprint",
        "tool_surface_fingerprint",
        "acceptance_rubric_id",
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
        "RESOURCE_STATE",
        "DEFECTS",
        "TESTS",
        "CHANGES",
        "UNRESOLVED",
        "LOCAL_JUDGMENT",
        "ASK",
    ]:
        assert field in text


def test_handoff_has_a_finite_release_finish_line():
    text = HANDOFF.read_text()
    assert "The remaining job is finite" in text
    assert "When items 1-12 are satisfied, the required action is **release v1.0.0**" in text
    assert "remaining P2/P3 work is moved post-v1" in text
    assert "Luna Max / Terra XHigh / Sol High remain the frozen v1 routing baseline" in text
    assert "Cosmetic alignment cannot block v1" in text
    for stage in ["## Stage R1", "## Stage R2", "## Stage R3", "## Stage R4"]:
        assert stage in text


def test_handoff_requires_cross_session_workspace_validation_without_global_locking():
    text = HANDOFF.read_text()
    for phrase in [
        "M1 different sessions, different projects/checkouts",
        "M2 different sessions, same repository, different runtime-backed isolated worktrees",
        "M3 different sessions, same canonical physical checkout",
        "M4 one writing session plus one read-only session on the same checkout",
        "Do not implement a workspace lock before M3 establishes a reproducible failure",
    ]:
        assert phrase in text


def test_handoff_requires_concurrent_installer_validation_before_locking():
    text = HANDOFF.read_text()
    for phrase in [
        "I1 same clean CODEX_HOME",
        "I2 one installer is forced to fail after mutation begins",
        "peer-success state",
        "I3 different managed profile generations",
        "Do not add an inter-process installer lock merely because races are theoretically possible",
    ]:
        assert phrase in text
