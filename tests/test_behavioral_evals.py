from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"
WORKLOADS = ROOT / "evals" / "behavioral-workloads.json"
SCRIPTS = ROOT / "scripts"
SCORER = SCRIPTS / "score-behavioral-evals.py"


def load_scorer_module():
    scripts_dir = str(SCRIPTS)
    sys.path.insert(0, scripts_dir)
    try:
        spec = importlib.util.spec_from_file_location("subagents_dispatch_behavioral_scorer", SCORER)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(scripts_dir)


SCORER_MODULE = load_scorer_module()


def base_run(mode: str) -> dict:
    return {
        "workload_id": "bounded-implementation",
        "mode": mode,
        "pair_id": "bounded-1",
        "repeat_index": 1,
        "repo_revision": "abc123",
        "workload_definition_hash": "sha256:fixture",
        "main_session_route": "gpt-5.6-sol/high",
        "main_judgment_coverage": "covered",
        "dependency_kind": "bounded_execution",
        "execution_route": "gpt-5.6-luna/max",
        "permissions_fingerprint": "workspace-write+default-approval",
        "tool_surface_fingerprint": "spawn-agent-v2+shell+git",
        "acceptance_rubric_id": "bounded-v1",
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
        "consent_prompts": 0,
        "evidence_established": 1,
        "evidence_invalidated": 0,
        "unjustified_repeated_commands": 0,
        "unjustified_repeated_discovery": 0,
        "duplicate_dependency_calls": 0,
    }


def score(tmp_path: Path, runs: list[dict]) -> subprocess.CompletedProcess[str]:
    payload = {
        "schema_version": "4.0",
        "runtime": {
            "codex_version": "fixture",
            "date": "2026-08-08",
            "observed_child_capacity": 4,
        },
        "runs": runs,
    }
    path = tmp_path / "result.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCORER), str(path), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_behavioral_schema_and_workload_registry_are_current():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    workloads = json.loads(WORKLOADS.read_text(encoding="utf-8"))
    assert schema["properties"]["schema_version"]["const"] == "4.0"
    assert workloads["schema_version"] == "4.0"
    assert workloads["workloads"]


def test_score_rejects_incomplete_pair(tmp_path: Path):
    result = score(tmp_path, [base_run("baseline")])
    assert result.returncode != 0
    assert "fewer than two runs" in result.stderr


def test_score_rejects_mixed_control_fields(tmp_path: Path):
    baseline = base_run("baseline")
    candidate = base_run("candidate")
    candidate["tool_surface_fingerprint"] = "different"
    result = score(tmp_path, [baseline, candidate])
    assert result.returncode != 0
    assert "mixes controlled field" in result.stderr


def test_mode_summary_keeps_metric_contract_without_cli_metadata_duplication():
    run = base_run("baseline")
    summary = SCORER_MODULE.mode_summary([run])
    assert summary["mean_acceptance_score"] is None
    assert summary["mean_agent_count"] == 1
    assert summary["scope_violations"] == 0
    assert summary["evidence_established"] == 1


def test_metric_mean_helper_ignores_missing_values():
    metric = next(metric for metric in SCORER_MODULE.METRICS if metric.field == "acceptance_score")
    first = base_run("baseline")
    second = base_run("candidate")
    first["acceptance_score"] = 0.8
    second["acceptance_score"] = None
    assert SCORER_MODULE.metric_summary([first, second], metric) == pytest.approx(0.8)


def test_score_accepts_controlled_pair_when_modes_match_workload_contract(tmp_path: Path):
    workloads = json.loads(WORKLOADS.read_text(encoding="utf-8"))
    spec = next(item for item in workloads["workloads"] if item["id"] == "bounded-implementation")
    primary = spec["expected"]["primary_comparison"]
    baseline = base_run(primary[0])
    candidate = base_run(primary[1])
    result = score(tmp_path, [baseline, candidate])
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["pair_count"] == 1
    assert summary["comparisons"]
