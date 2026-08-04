import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
WORKLOADS = ROOT / "evals" / "behavioral-workloads.json"
RESULT_SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"


def cases() -> dict[str, dict]:
    payload = json.loads(WORKLOADS.read_text())
    assert payload["schema_version"] == "3.0"
    return {item["id"]: item for item in payload["workloads"]}


def test_behavioral_suite_distinguishes_optional_and_required_final_review():
    by_id = cases()
    assert by_id["selective-sol-review"]["expected"]["review_requirement"] == "not_required"

    public = by_id["public-contract-final-review-required"]["expected"]
    assert public["review_requirement"] == "required"
    assert public["review_reason"] == "public_contract_change"
    assert public["fresh_sol_required"] is True
    assert public["ship_required"] is True


def test_behavioral_suite_covers_dynamic_review_escalation():
    by_id = cases()
    terra = by_id["terra-escalation-final-review-required"]["expected"]
    recovery = by_id["material-recovery-final-review-required"]["expected"]
    assert terra["review_reason"] == "terra_escalation"
    assert terra["artifact_binding_required"] is True
    assert recovery["review_reason"] == "material_recovery"
    assert recovery["fresh_sol_required"] is True


def test_behavioral_suite_covers_verdict_invalidation_lifecycle():
    by_id = cases()
    fix_first = by_id["fix-first-invalidates-old-review"]["expected"]
    mutation = by_id["post-review-mutation-invalidates-ship"]["expected"]
    rethink = by_id["rethink-invalidates-plan"]["expected"]

    assert fix_first["old_verdict_valid"] is False
    assert fix_first["fresh_rereview_required"] is True
    assert fix_first["completion_before_rereview"] is False

    assert mutation["old_verdict_valid"] is False
    assert mutation["artifact_verify_must_fail"] is True
    assert mutation["completion_allowed"] is False

    assert rethink["local_patch_only_forbidden"] is True
    assert rethink["dependency_invalidation_required"] is True
    assert rethink["shared_evidence_invalidation_required"] is True


def test_behavioral_suite_covers_declined_required_review():
    expected = cases()["implicit-required-review-declined"]["expected"]
    assert expected["review_requirement"] == "required"
    assert expected["sol_spawned"] is False
    assert expected["gate_satisfied"] is False
    assert expected["candidate_ready"] is True
    assert expected["ship_must_not_be_claimed"] is True


def test_behavioral_result_schema_supports_final_review_metrics():
    schema = json.loads(RESULT_SCHEMA.read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    props = schema["properties"]["runs"]["items"]["properties"]

    for field in [
        "final_review_requirement",
        "final_review_trigger_reasons",
        "final_review_attempts",
        "final_review_verdict",
        "final_review_gate_satisfied",
        "review_artifact_verify_failures",
        "post_review_mutations",
    ]:
        assert field in props

    assert props["final_review_requirement"]["enum"] == [None, "not_required", "required"]
    assert props["final_review_verdict"]["enum"] == [
        None,
        "ship",
        "fix-first",
        "rethink",
        "incomplete",
        "declined",
    ]
