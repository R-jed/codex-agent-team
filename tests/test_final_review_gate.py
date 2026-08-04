from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team"
REFERENCES = SKILL_DIR / "references"
PROFILE_DIR = ROOT / "plugins" / "codex-agent-team" / "agent-profiles"


def read(path: Path) -> str:
    return path.read_text()


def test_final_review_reference_is_linked_from_main_skill():
    skill = read(SKILL_DIR / "SKILL.md")
    gate = REFERENCES / "final-review-gate.md"
    assert gate.is_file()
    assert "references/final-review-gate.md" in skill
    assert "Final Review Gate" in skill
    assert "Candidate Ready" in skill


def test_review_gate_is_semantic_not_numeric():
    gate = read(REFERENCES / "final-review-gate.md")
    for reason in [
        "user_requested",
        "public_contract_change",
        "persistent_state_change",
        "security_boundary",
        "authorization_boundary",
        "data_integrity",
        "concurrency_semantics",
        "migration",
        "wide_blast_radius",
        "terra_escalation",
        "material_recovery",
        "verification_gap",
    ]:
        assert reason in gate
    assert "Do not use a numeric risk score" in gate
    assert "diff-line threshold" in gate
    assert "file-count threshold" in gate


def test_mandatory_review_reuses_existing_fresh_sol_route():
    gate = read(REFERENCES / "final-review-gate.md")
    advisor = tomllib.loads((PROFILE_DIR / "codex-agent-team-advisor.toml").read_text())
    assert "agent_type: codex_agent_team_advisor" in gate
    assert "fork_turns: none" in gate
    assert advisor["name"] == "codex_agent_team_advisor"
    assert advisor["model"] == "gpt-5.6-sol"
    assert advisor["model_reasoning_effort"] == "high"
    assert advisor["sandbox_mode"] == "read-only"


def test_review_verdict_is_bound_to_exact_artifact():
    gate = read(REFERENCES / "final-review-gate.md")
    for phrase in [
        "review_artifact_id",
        "complete accumulated diff digest",
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


def test_routing_policy_makes_sol_conditionally_mandatory_not_global():
    routing = read(REFERENCES / "routing-policy.md")
    assert "Sol is not a globally mandatory stage" in routing
    assert "Final Review Gate" in routing
    assert "fresh Sol `ship` verdict" in routing
    assert "risk-triggered" in routing.lower()


def test_receipt_can_report_required_final_review_without_claiming_unobserved_runtime():
    receipt = read(REFERENCES / "orchestration-receipt.md")
    assert "Final Review Gate" in receipt
    assert "Review requirement: required" in receipt
    assert "Verdict: ship" in receipt
    assert "Artifact unchanged after review" in receipt
    assert "Do not claim a mandatory final review succeeded" in receipt
