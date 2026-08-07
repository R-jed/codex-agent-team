from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"
SCORER = ROOT / "scripts" / "score-behavioral-evals.py"


def run(mode: str) -> dict:
    return {
        "workload_id": "bounded-implementation",
        "mode": mode,
        "pair_id": "final-review-metrics-1",
        "repeat_index": 1,
        "repo_revision": "candidate-sha",
        "workload_definition_hash": "sha256:workload-fixture",
        "main_session_route": "gpt-5.6-sol/high",
        "main_judgment_coverage": "covered",
        "dependency_kind": "bounded_execution",
        "execution_route": "gpt-5.6-luna/max",
        "permissions_fingerprint": "workspace-write+default-approval",
        "tool_surface_fingerprint": "spawn-agent-v2+shell+git",
        "acceptance_rubric_id": "final-review-metrics-v1",
        "success": True,
        "decision": "complete",
        "agent_count": 1,
        "peak_active_children": 1,
        "ready_dependencies": 1,
        "runtime_slot_waits": 0,
        "roles": ["worker"],
        "policy_violations": [],
        "scope_violations": 0,
        "wrong_edits": 0,
        "regressions": 0,
        "material_judgment_violations": 0,
        "correction_turns": 0,
        "reclassification_events": 0,
        "execution_stall_events": 0,
        "clean_same_lane_restarts": 0,
        "unjustified_retry_calls": 0,
        "same_failure_without_new_evidence": 0,
        "judgment_uplift_calls": 0,
        "solver_calls": 0,
        "advisor_calls": 0,
        "terra_calls": 0,
        "redundant_sol_calls": 0,
        "review_findings": 0,
        "review_false_positives": 0,
        "final_review_attempts": 0,
        "review_artifact_verify_failures": 0,
        "post_review_mutations": 0,
        "consent_prompts": 0,
        "evidence_established": 1,
        "evidence_invalidated": 0,
        "unjustified_repeated_commands": 0,
        "unjustified_repeated_discovery": 0,
        "duplicate_dependency_calls": 0,
    }


def score_process(tmp_path: Path, runs: list[dict]) -> subprocess.CompletedProcess[str]:
    result_path = tmp_path / "result.json"
    result_path.write_text(
        json.dumps(
            {
                "schema_version": "4.0",
                "suite": "subagents-dispatch-live-behavior",
                "runtime": {"codex_version": "fixture", "date": "2026-08-05"},
                "runs": runs,
            }
        ),
        encoding="utf-8",
    )
    return subprocess.run(
        [sys.executable, str(SCORER), str(result_path), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def score(tmp_path: Path, runs: list[dict]) -> dict:
    result = score_process(tmp_path, runs)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_schema_accepts_complete_final_review_telemetry():
    schema = json.loads(SCHEMA.read_text())
    candidate = run("bounded_luna")
    candidate.update(
        {
            "final_review_requirement": "required",
            "final_review_trigger_reasons": ["public_contract_change"],
            "final_review_attempts": 1,
            "final_review_verdict": "ship",
            "final_review_gate_satisfied": True,
            "review_caught_material_issue": False,
        }
    )
    payload = {
        "schema_version": "4.0",
        "suite": "subagents-dispatch-live-behavior",
        "runtime": {"codex_version": "fixture", "date": "2026-08-05"},
        "runs": [candidate],
    }
    jsonschema.Draft202012Validator(schema).validate(payload)


def test_scorer_reports_final_review_cost_and_artifact_deltas(tmp_path: Path):
    baseline = run("raw_prompt_luna")
    candidate = run("bounded_luna")
    candidate.update(
        {
            "final_review_requirement": "required",
            "final_review_trigger_reasons": ["public_contract_change"],
            "final_review_attempts": 2,
            "final_review_verdict": "ship",
            "final_review_gate_satisfied": True,
            "review_findings": 1,
            "review_caught_material_issue": True,
            "review_artifact_verify_failures": 1,
            "post_review_mutations": 1,
        }
    )

    summary = score(tmp_path, [baseline, candidate])
    comparison = summary["pairs"]["final-review-metrics-1"]["comparison"]
    assert comparison["metric_deltas"]["final_review_attempts"] == 2
    assert comparison["metric_deltas"]["review_artifact_verify_failures"] == 1
    assert comparison["metric_deltas"]["post_review_mutations"] == 1
    assert comparison["metric_deltas"]["review_findings"] == 1

    mode = summary["modes"]["bounded_luna"]
    assert mode["final_review_required_runs"] == 1
    assert mode["final_review_satisfied_runs"] == 1
    assert mode["final_review_unsatisfied_required_runs"] == 0
    assert mode["final_review_attempts"] == 2
    assert mode["final_review_yield"] == 0.5
    assert mode["review_artifact_verify_failures"] == 1
    assert mode["post_review_mutations"] == 1


def test_scorer_rejects_satisfied_gate_without_ship_verdict(tmp_path: Path):
    baseline = run("raw_prompt_luna")
    candidate = run("bounded_luna")
    candidate.update(
        {
            "final_review_requirement": "required",
            "final_review_trigger_reasons": ["public_contract_change"],
            "final_review_attempts": 1,
            "final_review_verdict": "fix-first",
            "final_review_gate_satisfied": True,
        }
    )
    result = score_process(tmp_path, [baseline, candidate])
    assert result.returncode != 0
    assert "without the ship verdict" in result.stderr


def test_scorer_rejects_required_review_without_trigger_reason(tmp_path: Path):
    baseline = run("raw_prompt_luna")
    candidate = run("bounded_luna")
    candidate.update(
        {
            "final_review_requirement": "required",
            "final_review_trigger_reasons": [],
            "final_review_attempts": 1,
            "final_review_verdict": "ship",
            "final_review_gate_satisfied": True,
        }
    )
    result = score_process(tmp_path, [baseline, candidate])
    assert result.returncode != 0
    assert "without a trigger reason" in result.stderr


def test_scorer_rejects_verdict_without_review_attempt(tmp_path: Path):
    baseline = run("raw_prompt_luna")
    candidate = run("bounded_luna")
    candidate["final_review_verdict"] = "ship"
    result = score_process(tmp_path, [baseline, candidate])
    assert result.returncode != 0
    assert "without a review attempt" in result.stderr


def test_scorer_keeps_missing_final_review_telemetry_explicitly_empty(tmp_path: Path):
    baseline = run("raw_prompt_luna")
    candidate = run("bounded_luna")
    for item in [baseline, candidate]:
        for field in [
            "final_review_attempts",
            "review_artifact_verify_failures",
            "post_review_mutations",
        ]:
            item.pop(field)

    summary = score(tmp_path, [baseline, candidate])
    comparison = summary["pairs"]["final-review-metrics-1"]["comparison"]
    assert comparison["metric_deltas"]["final_review_attempts"] is None
    assert comparison["metric_deltas"]["review_artifact_verify_failures"] is None
    assert comparison["metric_deltas"]["post_review_mutations"] is None
    assert summary["modes"]["bounded_luna"]["final_review_attempts"] is None
    assert summary["modes"]["bounded_luna"]["final_review_yield"] is None
