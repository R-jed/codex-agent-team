from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "subagents-dispatch"
SKILL = PLUGIN / "skills" / "dispatch"
ROUTER = SKILL / "references" / "router-core.md"
GUARDRAILS = SKILL / "references" / "guardrails.md"
TEAM_PLAN = SKILL / "references" / "team-plan.md"
COORDINATION_CASES = ROOT / "evals" / "coordination-cases.json"


def cases() -> dict[str, dict]:
    payload = json.loads(COORDINATION_CASES.read_text())
    assert payload["schema_version"] == "1.0"
    assert payload["suite"] == "subagents-dispatch-coordination-contract"
    return {case["id"]: case for case in payload["cases"]}


def test_upstream_workflow_truth_remains_authoritative():
    router = ROUTER.read_text().lower()
    assert "upstream workflow" in router
    assert "task truth" in router
    assert "competing" in router

    expected = cases()["upstream-workflow-remains-authoritative"]["expected"]
    assert expected["preserve_upstream_workflow"] is True
    assert set(expected["delegate_may_assign"]) == {
        "owner",
        "role",
        "concurrency",
        "write_isolation",
        "integration_timing",
    }
    assert {
        "goal",
        "decomposition",
        "stage_order",
        "dependencies",
        "required_outputs",
        "business_acceptance",
        "quality_gates",
    } <= set(expected["delegate_must_not_redefine"])


def test_parallel_writers_require_semantic_independence():
    router = ROUTER.read_text().lower()
    guardrails = GUARDRAILS.read_text().lower()
    team_plan = TEAM_PLAN.read_text().lower()
    assert "semantic independence" in router
    assert "semantic independence" in guardrails
    assert "different files" in team_plan

    expected = cases()["isolated-files-shared-api-are-not-independent"]["expected"]
    assert expected == {
        "parallel_writes_allowed": False,
        "filesystem_isolation_sufficient": False,
        "reason": "semantic_dependency",
        "required_resolution": "explicit_dependency_or_integration_order",
    }


def test_intent_and_mutation_authority_stay_separate():
    router = ROUTER.read_text().lower()
    guardrails = GUARDRAILS.read_text().lower()
    assert "intent: inspect | implement | verify | review" in router
    assert "mutation authority: none | declared-output-only | bounded-source-write" in router
    assert "filesystem permission is capability, not authorization" in guardrails

    verify_case = cases()["verify-child-cannot-fix-source"]["expected"]
    assert verify_case == {
        "intent": "verify",
        "mutation_authority": "none",
        "source_write_allowed": False,
        "on_required_source_change": "return_to_main_for_authority",
    }

    output_case = cases()["declared-output-does-not-grant-source-write"]["expected"]
    assert output_case["mutation_authority"] == "declared-output-only"
    assert output_case["source_write_allowed"] is False
    assert output_case["declared_output_write_allowed"] is True


def test_execution_dependency_and_integration_order_are_distinct():
    team_plan = TEAM_PLAN.read_text().lower()
    assert "dependency" in team_plan
    assert "integration_order" in team_plan
    assert "integration_owner" in team_plan

    ordered = cases()["independent-execution-ordered-integration"]["expected"]
    assert ordered["execution_can_overlap"] is True
    assert ordered["consumer_integration_after"] == ["producer"]
    assert ordered["main_is_integration_owner"] is True
    assert ordered["integrate_by_completion_time"] is False

    blocked = cases()["unresolved-semantics-cannot-hide-behind-integration-order"]["expected"]
    assert blocked["ready_to_execute"] is False
    assert blocked["integration_after_is_sufficient"] is False
    assert blocked["reason"] == "semantic_truth_not_ready"


def test_requested_accepted_and_observed_truth_layers_are_distinct():
    guardrails = GUARDRAILS.read_text().lower()
    for concept in ["requested", "accepted", "observed"]:
        assert concept in guardrails

    expected = cases()["accepted-route-is-not-runtime-observation"]["expected"]
    assert expected == {
        "requested_status": "declared",
        "accepted_status": "matched",
        "observed_status": "not_observed",
        "may_claim_observed_route": False,
    }
