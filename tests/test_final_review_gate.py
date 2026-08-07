from pathlib import Path
import json
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
REFS = SKILL / "references"
PROFILES = PLUGIN / "agent-profiles"
POLICY = PLUGIN / "policy-contract.json"


def contract():
    return json.loads(POLICY.read_text())


def test_final_review_is_linked_and_semantically_triggered():
    skill = (SKILL / "SKILL.md").read_text()
    review = (REFS / "final-review.md").read_text()
    assert "references/final-review.md" in skill
    assert "Candidate Ready" in review
    assert "Process history" in review
    for trigger in contract()["final_review"]["trigger_codes"]:
        assert trigger in review


def test_current_advisor_route_matches_policy_and_is_fresh():
    spec = contract()["roles"]["advisor"]
    advisor = tomllib.loads((PROFILES / spec["profile_file"]).read_text())
    review = (REFS / "final-review.md").read_text()
    assert "agent_type: codex_delegate_advisor" in review
    assert "fork_turns: none" in review
    assert advisor["name"] == spec["agent_type"]
    assert advisor["model"] == spec["model"]
    assert advisor["model_reasoning_effort"] == spec["effort"]
    assert advisor["sandbox_mode"] == spec["sandbox_intent"]


def test_review_lifecycle_remains_fail_closed_and_artifact_bound():
    review = (REFS / "final-review.md").read_text()
    for phrase in [
        "review_artifact_id",
        "review-artifact.py",
        "ship",
        "fix-first",
        "rethink",
        "INSUFFICIENT_EVIDENCE",
        "Any deliverable mutation after review invalidates the old verdict",
    ]:
        assert phrase in review
    final_review = contract()["final_review"]
    assert final_review["ship_verdict"] == "ship"
    assert final_review["correction_verdicts"] == ["fix-first", "rethink"]
    assert final_review["unresolved_verdict"] == "insufficient_evidence"


def test_sol_review_is_selective_outside_required_assurance():
    router = (REFS / "router-core.md").read_text().lower()
    review = (REFS / "final-review.md").read_text().lower()
    assert "final review" in router
    assert "candidate" in router and "independent second judgment" in router
    assert "process history" in review
    assert "not a trigger by itself" in review
