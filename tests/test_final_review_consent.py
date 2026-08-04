from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = (
    ROOT
    / "plugins"
    / "codex-agent-team"
    / "skills"
    / "codex-agent-team"
    / "references"
)


def test_explicit_invocation_can_cover_first_required_final_review():
    consent = (REFERENCES / "consent-policy.md").read_text()
    assert "first risk-triggered Final Review Gate pass" in consent
    assert "explicit `/codex-delegate` baseline" in consent
    assert "single read-only Sol advisor" in consent


def test_implicit_invocation_does_not_silently_expand_sol_compute():
    consent = (REFERENCES / "consent-policy.md").read_text()
    assert "For implicit Skill invocation, ask before adding Sol" in consent
    assert "does not silently expand implicit-call compute authorization" in consent


def test_declined_review_keeps_quality_gate_unsatisfied():
    consent = (REFERENCES / "consent-policy.md").read_text()
    receipt = (REFERENCES / "orchestration-receipt.md").read_text()
    assert "keep the candidate at **Candidate Ready**" in consent
    assert "do not downgrade `review_requirement`" in consent
    assert "do not fabricate `ship`" in consent
    assert "additional Sol review declined by user" in receipt
    assert "independent final review not satisfied" in receipt


def test_repeated_final_review_cycles_remain_compute_consent_bounded():
    consent = (REFERENCES / "consent-policy.md").read_text()
    assert "final review gate does not authorize unlimited reviewer retries" in consent.lower()
    assert "Approval for one additional Sol pass does not authorize repeated Sol retries" in consent
