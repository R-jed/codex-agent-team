from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-agent-team"
SKILL = PLUGIN / "skills" / "codex-agent-team"
RUNTIME_REFERENCE = SKILL / "references" / "runtime-assurance.md"
RUNTIME_VERIFIER = PLUGIN / "scripts" / "runtime-evidence.py"
LEGACY_INSPECTOR = SKILL / "scripts" / "inspect-runtime.py"
LEGACY_VERIFIER = SKILL / "scripts" / "verify-runtime.py"


def test_runtime_assurance_uses_one_normalized_verifier():
    assert RUNTIME_VERIFIER.is_file()
    assert not LEGACY_INSPECTOR.exists()
    assert not LEGACY_VERIFIER.exists()
    reference = RUNTIME_REFERENCE.read_text()
    assert "runtime-evidence.py" in reference
    assert "normalized" in reference.lower()


def test_project_does_not_scrape_rollout_files_for_runtime_proof():
    reference = RUNTIME_REFERENCE.read_text()
    skill = (SKILL / "SKILL.md").read_text()
    combined = reference + skill
    assert "does not scrape Codex rollout internals" in combined
    assert "no longer ships a rollout-file inspector" in reference
    assert "sessions root" not in combined.lower()
    assert "--sessions-dir" not in combined
    assert "rollout-2026-" not in combined


def test_missing_native_permission_evidence_remains_fail_closed():
    reference = RUNTIME_REFERENCE.read_text()
    assert "required read-only but native sandbox missing" in reference
    assert "return to main session" in reference
    assert "local/reconstructed" not in reference or "cannot establish host enforcement" in reference


def test_runtime_evidence_keeps_route_ancestry_and_permission_typed():
    reference = RUNTIME_REFERENCE.read_text()
    for field in ["route_evidence", "ancestry_evidence", "permission_evidence"]:
        assert field in reference
    for status in ["not_observed", "partial", "matched", "conflict"]:
        assert status in reference
    for grade in [
        "C1_configuration_only",
        "L1_local_record_observed",
        "R1_runtime_reported",
        "R2_runtime_reported_and_local_record_agree",
        "X0_conflicted",
    ]:
        assert grade in reference
