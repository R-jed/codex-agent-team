from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
GUARDRAILS = SKILL / "references" / "guardrails.md"
RUNTIME_DOC = ROOT / "docs" / "native-subagent-runtime.md"
RUNTIME_VERIFIER = PLUGIN / "scripts" / "runtime-evidence.py"
LEGACY_INSPECTOR = SKILL / "scripts" / "inspect-runtime.py"
LEGACY_VERIFIER = SKILL / "scripts" / "verify-runtime.py"


def test_runtime_assurance_uses_one_optional_normalized_verifier():
    assert RUNTIME_VERIFIER.is_file()
    assert not LEGACY_INSPECTOR.exists()
    assert not LEGACY_VERIFIER.exists()
    guardrails = GUARDRAILS.read_text()
    runtime = RUNTIME_DOC.read_text()
    assert "runtime-evidence.py" in guardrails
    assert "runtime-evidence.py" in runtime
    assert "diagnostic" in runtime.lower()
    assert "on demand" in runtime.lower()


def test_project_does_not_scrape_runtime_internals_for_proof():
    runtime = RUNTIME_DOC.read_text().lower()
    assert "configured values never become observed values by assumption" in runtime
    for forbidden in ["--sessions-dir", "rollout-2026-", "sessions root"]:
        assert forbidden not in runtime


def test_missing_native_permission_evidence_remains_fail_closed():
    guardrails = GUARDRAILS.read_text()
    assert "When hard read-only isolation is required, demand native evidence" in guardrails
    assert "keep the responsibility in the main session/blocked" in guardrails
    assert "configured read-only profile is intent, not proof" in guardrails


def test_runtime_evidence_keeps_route_ancestry_and_permission_typed():
    runtime = RUNTIME_DOC.read_text()
    verifier = RUNTIME_VERIFIER.read_text()
    for field in ["route_evidence", "ancestry_evidence", "permission_evidence"]:
        assert field in runtime
        assert field in verifier
    for grade in [
        "C1_configuration_only",
        "L1_local_record_observed",
        "R1_runtime_reported",
        "R2_runtime_reported_and_local_record_agree",
        "X0_conflicted",
    ]:
        assert grade in verifier
