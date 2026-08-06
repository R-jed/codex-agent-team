from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
ROUTER = SKILL / "references" / "router-core.md"
GUARDRAILS = SKILL / "references" / "guardrails.md"
COORDINATION_CASES = ROOT / "evals" / "coordination-cases.json"


def cases() -> dict[str, dict]:
    payload = json.loads(COORDINATION_CASES.read_text())
    assert payload["schema_version"] == "1.0"
    assert payload["suite"] == "codex-delegate-coordination-contract"
    return {case["id"]: case for case in payload["cases"]}


def test_upstream_workflow_ownership_is_preserved():
    router = ROUTER.read_text().lower()
    for phrase in [
        "preserve upstream workflow ownership",
        "treat those definitions as task truth",
        "does not silently create a competing domain plan",
        "reuse it as the coordination source of truth",
        "do not create a second persistent state source",
    ]:
        assert phrase in router

    case = cases()["upstream-workflow-remains-authoritative"]
    expected = case["expected"]
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


def test_parallel_writers_require_semantic_independence_not_only_isolation():
    router = ROUTER.read_text().lower()
    guardrails = GUARDRAILS.read_text().lower()
    for phrase in [
        "filesystem isolation is necessary for simultaneous writers, but it is not sufficient",
        "semantic independence",
        "shared api or schema",
        "migration order",
        "generated artifact",
        "explicit dependency and integration order",
    ]:
        assert phrase in router
    for phrase in [
        "filesystem isolation alone does not establish semantic independence",
        "shared apis",
        "schemas",
        "migrations",
        "lockfiles",
        "generated artifacts",
        "explicit dependency or integration order",
    ]:
        assert phrase in guardrails

    case = cases()["isolated-files-shared-api-are-not-independent"]
    expected = case["expected"]
    assert expected["parallel_writes_allowed"] is False
    assert expected["filesystem_isolation_sufficient"] is False
    assert expected["reason"] == "semantic_dependency"
    assert expected["required_resolution"] == "explicit_dependency_or_integration_order"


def test_child_intent_and_mutation_authority_are_separate_contracts():
    router = ROUTER.read_text().lower()
    guardrails = GUARDRAILS.read_text().lower()
    for phrase in [
        "intent: inspect | implement | verify | review",
        "mutation authority: none | declared-output-only | bounded-source-write",
        "a writable filesystem or broad sandbox never creates mutation authority by itself",
        "children do not widen scope, permission, mutation authority",
    ]:
        assert phrase in router
    for phrase in [
        "mutation authority is explicit",
        "filesystem permission is capability, not authorization",
        "declared-output-only",
        "bounded-source-write",
        "children do not self-upgrade mutation authority",
    ]:
        assert phrase in guardrails

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


def test_optional_integration_dependencies_do_not_become_fake_execution_readiness():
    router = ROUTER.read_text().lower()
    for phrase in [
        "integration after, when needed",
        "it expresses integration order, not permission to execute through an unresolved semantic dependency",
        "keep it off the ready frontier instead of using `integration after` as a shortcut",
        "main remains the integration owner",
        "do not integrate by completion time when dependency order says otherwise",
        "verifies the resulting combined artifact",
    ]:
        assert phrase in router

    ordered = cases()["independent-execution-ordered-integration"]["expected"]
    assert ordered["execution_can_overlap"] is True
    assert ordered["consumer_integration_after"] == ["producer"]
    assert ordered["main_is_integration_owner"] is True
    assert ordered["integrate_by_completion_time"] is False

    blocked = cases()["unresolved-semantics-cannot-hide-behind-integration-order"]["expected"]
    assert blocked["ready_to_execute"] is False
    assert blocked["integration_after_is_sufficient"] is False
    assert blocked["reason"] == "semantic_truth_not_ready"


def test_requested_accepted_and_observed_truth_layers_are_not_collapsed():
    guardrails = GUARDRAILS.read_text().lower()
    for phrase in [
        "keep three truth layers separate",
        "requested is not accepted",
        "accepted is not observed",
        "does not prove that the runtime actually executed that route",
        "not_reported",
        "not_observed",
    ]:
        assert phrase in guardrails

    expected = cases()["accepted-route-is-not-runtime-observation"]["expected"]
    assert expected == {
        "requested_status": "declared",
        "accepted_status": "matched",
        "observed_status": "not_observed",
        "may_claim_observed_route": False,
    }
