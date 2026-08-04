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


def test_handoff_adversarial_review_is_transport_agnostic():
    text = HANDOFF.read_text()
    assert "Review Checkpoints A-E" in text
    assert "Codex remains the local executor" in text
    assert "model_judgment" in text
    assert "must not be counted as evidence that Codex Delegate itself routed correctly" in text
    assert "Do not bind release correctness to the title or existence of one specific external ChatGPT conversation" in text
    for forbidden in [
        "TARGET_CHATGPT_CONVERSATION_TITLE",
        "分支 · 分支 · 项目对比分析",
        "continue_existing_conversation",
    ]:
        assert forbidden not in text


def test_validation_report_reflects_merged_v060_baseline_and_provenance():
    text = REPORT.read_text()
    for phrase in [
        "Plugin version: 0.6.0",
        "Accepted v0.6.0 feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed",
        "workflow: 30879802677",
        "pytest: 167 passed",
        "Accepted v0.6.0 static evidence",
        "Accepted v0.5.1 historical static evidence",
        "That live baseline predates v0.6.0",
        "review_artifact_id",
        "contract_luna_final_review_gate",
        "HOLD FOR RELEASE / LIVE VALIDATION PENDING",
        "ARCHITECTURE FROZEN AT v0.6.0",
        "Current engineering-consolidation candidate",
    ]:
        assert phrase in text
    assert "Current feature PR: #27" not in text
    assert "final documentation/version closure must also pass CI before PR #27 is merged" not in text.lower()
