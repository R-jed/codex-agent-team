from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "HEADOFF.md"

HISTORICAL_BRANCHES = {
    "docs/readme-community-v2",
    "docs/readme-native-zh-v3",
    "docs/readme-visual-system-v4",
    "feat/community-plugin-v1",
    "feat/runtime-assurance-v1",
    "feat/runtime-truth-v1",
    "feat/single-command-plugin-v1",
    "fix/legacy-install-adoption",
    "fix/readme-layout-v5",
    "incremental-orchestration-v1",
}


def test_local_runtime_handoff_is_linked_from_both_readmes():
    assert HANDOFF.is_file()
    for name in ["README.md", "README_EN.md"]:
        assert "HEADOFF.md" in (ROOT / name).read_text()


def test_handoff_protects_release_critical_live_validation_scope():
    text = HANDOFF.read_text()
    for phrase in [
        "## 2. Stop line",
        "## 5. Remote branch cleanup",
        "## 8. Runtime Truth adversarial matrix",
        "## 11. Shared Evidence State and invalidation",
        "## 13. Terra delta-escalation experiment",
        "## 14. Luna + selective Sol experiment",
        "## 15. Primary product experiment",
        "## 16. Parallelism and stress tests",
        "## 17. Installer migration and fault injection",
        "## 19. Current unknown technical debt register",
        "## 20. Release acceptance gate",
        "## 21. Required local deliverables",
        "LOCAL_VALIDATION_REPORT.md",
        "behavioral-result.schema.json",
    ]:
        assert phrase in text

    for branch in HISTORICAL_BRANCHES:
        assert branch in text


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
