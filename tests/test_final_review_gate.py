from pathlib import Path
import json
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
SKILL_DIR = PLUGIN_ROOT / "skills" / "codex-agent-team"
REFERENCES = SKILL_DIR / "references"
PROFILE_DIR = PLUGIN_ROOT / "agent-profiles"
ARTIFACT_HELPER = PLUGIN_ROOT / "scripts" / "review-artifact.py"
POLICY_CONTRACT = PLUGIN_ROOT / "policy-contract.json"


def read(path: Path) -> str:
    return path.read_text()


def policy_contract() -> dict:
    return json.loads(POLICY_CONTRACT.read_text())


def test_final_review_reference_is_linked_from_main_skill():
    skill = read(SKILL_DIR / "SKILL.md")
    gate = REFERENCES / "final-review-gate.md"
    assert gate.is_file()
    assert "references/final-review-gate.md" in skill
    assert "Final Review Gate" in skill
    assert "Candidate Ready" in skill


def test_review_gate_matches_machine_readable_semantic_triggers():
    gate = read(REFERENCES / "final-review-gate.md")
    final_review = policy_contract()["final_review"]
    for reason in final_review["trigger_codes"]:
        assert reason in gate
    assert final_review["completion_verdicts"] == ["ship", "fix-first", "rethink"]
    assert final_review["unresolved_verdict"] == "insufficient_evidence"
    assert "Do not use a numeric risk score" in gate
    assert "diff-line threshold" in gate
    assert "file-count threshold" in gate


def test_mandatory_review_reuses_existing_fresh_sol_route():
    gate = read(REFERENCES / "final-review-gate.md")
    advisor_spec = policy_contract()["roles"]["advisor"]
    advisor = tomllib.loads((PROFILE_DIR / advisor_spec["profile_file"]).read_text())
    assert "agent_type: codex_agent_team_advisor" in gate
    assert "fork_turns: none" in gate
    assert advisor["name"] == advisor_spec["agent_type"]
    assert advisor["model"] == advisor_spec["model"]
    assert advisor["model_reasoning_effort"] == advisor_spec["effort"]
    assert advisor["sandbox_mode"] == advisor_spec["sandbox_intent"]


def test_review_verdict_is_bound_to_exact_artifact_with_bundled_helper():
    gate = read(REFERENCES / "final-review-gate.md")
    assert ARTIFACT_HELPER.is_file()
    for phrase in [
        "review_artifact_id",
        "review-artifact.py",
        "tracked_diff_sha256",
        "--verify '<review_artifact_id>'",
        "Any deliverable mutation after a `ship` verdict invalidates that verdict",
        "REVIEWED_ARTIFACT_ID",
        "reviewed artifact unchanged",
    ]:
        assert phrase in gate
    assert "branch name" in gate
    assert "alone is not an artifact identity" in gate


def test_fix_first_requires_fresh_reverification_and_rereview():
    gate = read(REFERENCES / "final-review-gate.md")
    assert "capture a new artifact identity, and launch a new fresh Sol review" in gate
    assert "The old verdict is invalid after any fix" in gate
    assert "must not repair the code and report completion without re-review" in gate


def test_rethink_invalidates_plan_instead_of_becoming_local_fix():
    gate = read(REFERENCES / "final-review-gate.md")
    assert "Invalidate the affected Dependency Ledger and Shared Evidence entries" in gate
    assert "Do not downgrade `rethink` into a local bug-fix ticket" in gate


def test_routing_policy_makes_sol_selective_with_mandatory_high_risk_gate():
    routing = read(REFERENCES / "routing-policy.md")
    gate = read(REFERENCES / "final-review-gate.md")
    assert "Sol is not globally mandatory" in routing
    assert "final-review-gate.md" in routing
    assert "fresh Sol `ship` verdict" in gate
    assert "semantic trigger" in gate.lower()


def test_receipt_can_report_required_final_review_without_claiming_unobserved_runtime():
    receipt = read(REFERENCES / "orchestration-receipt.md")
    assert "Final Review Gate" in receipt
    assert "Review requirement: required" in receipt
    assert "Verdict: ship" in receipt
    assert "Artifact unchanged after review" in receipt
    assert "Do not claim a mandatory final review succeeded" in receipt
