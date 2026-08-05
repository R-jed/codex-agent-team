from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"
WORKLOADS = ROOT / "evals" / "behavioral-workloads.json"
SCORER = ROOT / "scripts" / "score-behavioral-evals.py"


def base_run(mode: str, *, success: bool = True) -> dict:
    return {
        "workload_id": "bounded-implementation",
        "mode": mode,
        "pair_id": "bounded-1",
        "repeat_index": 1,
        "repo_revision": "abc123",
        "workload_definition_hash": "sha256:workload-fixture",
        "main_session_route": "gpt-5.6-sol/high",
        "main_judgment_coverage": "covered",
        "dependency_kind": "bounded_execution",
        "execution_route": "gpt-5.6-luna/max" if mode != "main_session_only" else None,
        "permissions_fingerprint": "workspace-write+default-approval",
        "tool_surface_fingerprint": "spawn-agent-v2+shell+git",
        "acceptance_rubric_id": "bounded-fix-v1",
        "success": success,
        "decision": "complete",
        "agent_count": 1 if mode != "main_session_only" else 0,
        "peak_active_children": 1 if mode != "main_session_only" else 0,
        "ready_dependencies": 1,
        "runtime_slot_waits": 0,
        "roles": ["worker"] if mode != "main_session_only" else [],
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
        "consent_prompts": 0,
        "evidence_established": 3,
        "evidence_invalidated": 0,
        "unjustified_repeated_commands": 0,
        "unjustified_repeated_discovery": 0,
        "duplicate_dependency_calls": 0,
    }


def run_score(tmp_path: Path, runs: list[dict]) -> subprocess.CompletedProcess[str]:
    result_file = tmp_path / "result.json"
    result_file.write_text(
        json.dumps(
            {
                "schema_version": "4.0",
                "suite": "codex-delegate-live-behavior",
                "runtime": {
                    "codex_version": "fixture",
                    "date": "2026-08-05",
                    "observed_child_capacity": 3,
                },
                "runs": runs,
            }
        )
    )
    return subprocess.run(
        [sys.executable, str(SCORER), str(result_file), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_behavioral_workloads_cover_current_product_questions():
    payload = json.loads(WORKLOADS.read_text())
    assert payload["schema_version"] == "4.0"
    assert payload["suite"] == "codex-delegate-live-behavior"
    ids = {item["id"] for item in payload["workloads"]}
    assert {
        "simple-main-session-fix",
        "bounded-implementation",
        "judgment-coupled-nonsol",
        "judgment-coupled-sol-main",
        "unknown-main-routine-bounded",
        "luna-semantic-emergence",
        "technical-delta-after-semantics",
        "claimed-technical-gap-is-actually-judgment",
        "process-history-does-not-force-review",
        "public-contract-final-review-required",
        "verification-gap-final-review-required",
        "sol-main-still-needs-independent-review",
        "shared-workspace-worker-solver-conflict",
        "main-route-observability",
    } <= ids
    assert "no claimed benchmark results" in payload["note"]


def test_behavioral_result_schema_keeps_historical_measurement_controls():
    schema = json.loads(SCHEMA.read_text())
    payload = {
        "schema_version": "4.0",
        "suite": "codex-delegate-live-behavior",
        "runtime": {"codex_version": "fixture", "date": "2026-08-05"},
        "runs": [base_run("raw_prompt_luna"), base_run("bounded_luna")],
    }
    jsonschema.Draft202012Validator(schema).validate(payload)

    for missing_field in ["main_judgment_coverage", "dependency_kind", "execution_route"]:
        incomplete = base_run("bounded_luna")
        incomplete.pop(missing_field)
        invalid = {**payload, "runs": [base_run("raw_prompt_luna"), incomplete]}
        assert list(jsonschema.Draft202012Validator(schema).iter_errors(invalid))


def test_behavioral_schema_accepts_solver_and_routing_metrics():
    schema = json.loads(SCHEMA.read_text())
    run = base_run("sol_solver")
    run.update(
        {
            "workload_id": "judgment-coupled-nonsol",
            "pair_id": "solver-1",
            "main_session_route": "gpt-5.6-luna/max",
            "main_judgment_coverage": "uncovered",
            "dependency_kind": "judgment_coupled_execution",
            "execution_route": "gpt-5.6-sol/high",
            "roles": ["solver"],
            "solver_calls": 1,
            "judgment_uplift_calls": 1,
            "reclassification_events": 1,
        }
    )
    payload = {
        "schema_version": "4.0",
        "suite": "codex-delegate-live-behavior",
        "runtime": {"codex_version": "fixture", "date": "2026-08-05"},
        "runs": [run],
    }
    assert not list(jsonschema.Draft202012Validator(schema).iter_errors(payload))


def test_scorer_reports_paired_delta_and_strategy_routes(tmp_path: Path):
    raw = base_run("raw_prompt_luna")
    raw.update(
        {
            "acceptance_score": 7,
            "correction_turns": 2,
            "material_judgment_violations": 1,
            "input_tokens": 1000,
            "unjustified_retry_calls": 1,
        }
    )
    bounded = base_run("bounded_luna")
    bounded.update(
        {
            "acceptance_score": 9,
            "correction_turns": 0,
            "material_judgment_violations": 0,
            "input_tokens": 800,
            "unjustified_retry_calls": 0,
        }
    )

    result = run_score(tmp_path, [raw, bounded])
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    pair = summary["pairs"]["bounded-1"]
    assert summary["pair_count"] == 1
    assert pair["modes"] == ["bounded_luna", "raw_prompt_luna"]
    assert pair["comparison"]["baseline_mode"] == "raw_prompt_luna"
    assert pair["comparison"]["candidate_mode"] == "bounded_luna"
    assert pair["comparison"]["metric_deltas"]["acceptance_score"] == 2
    assert pair["comparison"]["metric_deltas"]["correction_turns"] == -2
    assert pair["comparison"]["metric_deltas"]["material_judgment_violations"] == -1
    assert pair["comparison"]["metric_deltas"]["input_tokens"] == -200
    assert pair["controls"]["main_judgment_coverage"] == "covered"
    assert pair["execution_routes"]["bounded_luna"] == "gpt-5.6-luna/max"
    assert summary["mode_aggregates_are_descriptive_only"] is True


def test_scorer_allows_execution_route_to_be_the_experimental_variable(tmp_path: Path):
    advisor_luna = base_run("advisor_then_luna")
    advisor_luna.update(
        {
            "workload_id": "judgment-coupled-nonsol",
            "pair_id": "judgment-1",
            "main_session_route": "gpt-5.6-luna/max",
            "main_judgment_coverage": "uncovered",
            "dependency_kind": "judgment_coupled_execution",
            "execution_route": "gpt-5.6-sol/high -> gpt-5.6-luna/max",
            "roles": ["advisor", "worker"],
            "agent_count": 2,
            "advisor_calls": 1,
            "judgment_uplift_calls": 1,
        }
    )
    solver = dict(advisor_luna)
    solver.update(
        {
            "mode": "sol_solver",
            "execution_route": "gpt-5.6-sol/high",
            "roles": ["solver"],
            "agent_count": 1,
            "advisor_calls": 0,
            "solver_calls": 1,
        }
    )

    result = run_score(tmp_path, [advisor_luna, solver])
    assert result.returncode == 0, result.stderr
    pair = json.loads(result.stdout)["pairs"]["judgment-1"]
    assert pair["comparison"]["baseline_execution_route"] != pair["comparison"]["candidate_execution_route"]


def test_scorer_does_not_invent_missing_telemetry(tmp_path: Path):
    result = run_score(tmp_path, [base_run("raw_prompt_luna"), base_run("bounded_luna")])
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    comparison = summary["pairs"]["bounded-1"]["comparison"]
    assert comparison["metric_deltas"]["input_tokens"] is None
    assert comparison["metric_deltas"]["main_session_correction_tokens"] is None
    assert summary["modes"]["bounded_luna"]["mean_input_tokens"] is None


def test_scorer_rejects_unpaired_run(tmp_path: Path):
    result = run_score(tmp_path, [base_run("bounded_luna")])
    assert result.returncode != 0
    assert "fewer than two runs" in result.stderr


def test_scorer_rejects_wrong_modes_for_declared_primary_comparison(tmp_path: Path):
    result = run_score(tmp_path, [base_run("raw_prompt_luna"), base_run("adaptive_routing_v4")])
    assert result.returncode != 0
    assert "must contain declared primary comparison modes" in result.stderr


def test_scorer_rejects_mixed_pair_control_fields(tmp_path: Path):
    for field, changed in [
        ("main_session_route", "gpt-5.6-terra/xhigh"),
        ("main_judgment_coverage", "unknown"),
        ("workload_definition_hash", "sha256:other-workload"),
        ("permissions_fingerprint", "read-only+default-approval"),
        ("tool_surface_fingerprint", "spawn-agent-v3+shell+git"),
        ("acceptance_rubric_id", "bounded-fix-v2"),
    ]:
        raw = base_run("raw_prompt_luna")
        bounded = base_run("bounded_luna")
        bounded[field] = changed
        result = run_score(tmp_path, [raw, bounded])
        assert result.returncode != 0
        assert f"controlled field '{field}'" in result.stderr


def test_behavioral_docs_state_measurement_labels_are_not_runtime_ontology():
    docs = (ROOT / "docs" / "behavioral-evals.md").read_text()
    for phrase in [
        "paired workloads",
        "advisor_then_luna",
        "sol_solver",
        "main_judgment_coverage",
        "execution_route",
        "measurement surface",
        "not runtime ontology",
        "historical measurement labels",
    ]:
        assert phrase.lower() in docs.lower()
