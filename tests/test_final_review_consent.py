from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "plugins" / "codex-delegate" / "skills" / "codex-delegate" / "references"


def test_explicit_invocation_can_cover_first_required_final_review():
    final_review = (REFERENCES / "final-review.md").read_text()
    guardrails = (REFERENCES / "guardrails.md").read_text()
    assert "first ordinary fresh review after explicit `/codex-delegate` use" in final_review
    assert "up to 2 concurrently active justified children" in guardrails


def test_implicit_invocation_is_disabled_instead_of_needing_extra_consent_policy():
    openai = (
        ROOT
        / "plugins"
        / "codex-delegate"
        / "skills"
        / "codex-delegate"
        / "agents"
        / "openai.yaml"
    ).read_text()
    guardrails = (REFERENCES / "guardrails.md").read_text()
    assert "allow_implicit_invocation: false" in openai
    assert "Explicit invocation only" in guardrails


def test_declined_required_review_remains_incomplete():
    final_review = (REFERENCES / "final-review.md").read_text()
    assert "the user declines it" in final_review
    assert "independent assurance remains incomplete" in final_review
    assert "Do not silently downgrade the review requirement" in final_review


def test_repeated_final_review_cycles_remain_compute_consent_bounded():
    final_review = (REFERENCES / "final-review.md").read_text()
    guardrails = (REFERENCES / "guardrails.md").read_text()
    assert "Repeated correction/re-review loops" in final_review
    assert "repeated expensive Solver, Advisor, Investigator, or correction/re-review loops" in guardrails
