from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "HEADOFF.md"


def test_local_runtime_handoff_is_linked_from_both_readmes():
    assert HANDOFF.is_file()
    for name in ["README.md", "README_EN.md"]:
        assert "HEADOFF.md" in (ROOT / name).read_text()


def test_handoff_protects_release_critical_live_validation_scope():
    text = HANDOFF.read_text()
    for phrase in [
        "## Current checkpoint",
        "## Stop line",
        "# Completed work",
        "# Pending live validation",
        "## Checkpoint 1: complete exact-role and Runtime Truth coverage",
        "incomplete expected route -> fail closed",
        "### 5. Shared Evidence State and invalidation",
        "### 7. Terra delta-escalation experiment",
        "### 8. Primary raw-prompt versus compiled-contract experiment",
        "### 9. Luna + selective Sol experiment",
        "## Checkpoint 5: resource governance and lifecycle stress",
        "## Checkpoint 6: installer migration and fault injection",
        "# Version-scoped unknowns and technical debt",
        "# Defect triage",
        "# Release acceptance gate",
        "# Required validation artifact",
        "# Feedback protocol for continued adversarial review",
        "# Completion condition",
        "LOCAL_VALIDATION_REPORT.md",
        "behavioral-result.schema.json",
        "RELEASE CANDIDATE",
        "HOLD",
    ]:
        assert phrase in text

    assert "[x]" in text
    assert "[ ]" in text
    assert "origin/main only" in text
    assert "CAT-LOCAL-001" in text
    assert "PROJECT TAKEOVER: CODEX AGENT TEAM LOCAL RUNTIME VALIDATION" not in text


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


def test_handoff_defines_incremental_feedback_packets():
    text = HANDOFF.read_text()
    for field in [
        "COMPLETED_HEADOFF_ITEMS",
        "NEW_EVIDENCE",
        "DEFECTS",
        "TESTS",
        "CHANGES",
        "UNRESOLVED",
        "LOCAL_JUDGMENT",
        "ASK",
    ]:
        assert field in text
