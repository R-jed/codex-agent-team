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
        "main_session_route": "gpt-5.6-sol/high",
        "success": success,
        "decision": "complete",
        "agent_count": 1 if mode != "main_session_only" else 0,
        "roles": ["worker"] if mode != "main_session_only" else [],
        "policy_violations": [],
        "scope_violations": 0,
        "wrong_edits": 0,
        "regressions": 0,
        "correction_turns": 0,
        "review_findings": 0,
        "review_false_positives": 0,
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
                "schema_version": "2.0",
                "suite": "codex-agent-team-live-behavior",
                "runtime": {"codex_version": "fixture", "date": "2026-08-02"},
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


def test_behavioral_workloads_cover_contract_and_resource_coordination():
    payload = json.loads(WORKLOADS.read_text())
    assert payload["schema_version"] == "2.0"
    ids = {item["id"] for item in payload["workloads"]}
    assert {
        "simple-main-session-fix",
        "bounded-implementation",
        "ambiguous-product-decision",
        "context-heavy-read",
        "luna-capability-gap",
        "selective-sol-review",
        "two-independent-readers",
        "runtime-route-partial",
    } <= ids
    assert "no claimed benchmark results" in payload["note"]


def test_behavioral_result_schema_accepts_paired_runs():
    schema = json.loads(SCHEMA.read_text())
    payload = {
        "schema_version": "2.0",
        "suite": "codex-agent-team-live-behavior",
        "runtime": {"codex_version": "fixture", "date": "2026-08-02"},
        "runs": [base_run("raw_prompt_luna"), base_run("contract_luna")],
    }
    jsonschema.Draft202012Validator(schema).validate(payload)


def test_scorer_reports_paired_delta_and_keeps_global_modes_descriptive_only(tmp_path: Path):
    raw = base_run("raw_prompt_luna")
    raw.update({"acceptance_score": 7, "correction_turns": 2, "input_tokens": 1000})
    contract = base_run("contract_luna")
    contract.update({"acceptance_score": 9, "correction_turns": 0, "input_tokens": 800})

    result = run_score(tmp_path, [raw, contract])

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["pair_count"] == 1
    pair = summary["pairs"]["bounded-1"]
    assert pair["modes"] == ["contract_luna", "raw_prompt_luna"]
    assert pair["comparison"]["baseline_mode"] == "raw_prompt_luna"
    assert pair["comparison"]["candidate_mode"] == "contract_luna"
    assert pair["comparison"]["metric_deltas"]["acceptance_score"] == 2
    assert pair["comparison"]["metric_deltas"]["correction_turns"] == -2
    assert pair["comparison"]["metric_deltas"]["input_tokens"] == -200
    comparison = summary["comparisons"]["bounded-implementation:raw_prompt_luna->contract_luna"]
    assert comparison["pair_count"] == 1
    assert comparison["mean_metric_deltas"]["acceptance_score"] == 2
    assert summary["mode_aggregates_are_descriptive_only"] is True
    assert "bounded-implementation" in summary["workloads"]


def test_scorer_does_not_invent_missing_telemetry(tmp_path: Path):
    result = run_score(tmp_path, [base_run("raw_prompt_luna"), base_run("contract_luna")])
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    comparison = summary["pairs"]["bounded-1"]["comparison"]
    assert comparison["metric_deltas"]["input_tokens"] is None
    assert comparison["metric_deltas"]["main_session_correction_tokens"] is None
    assert summary["modes"]["contract_luna"]["mean_input_tokens"] is None


def test_scorer_rejects_unpaired_run(tmp_path: Path):
    result = run_score(tmp_path, [base_run("contract_luna")])
    assert result.returncode != 0
    assert "fewer than two runs" in result.stderr


def test_scorer_rejects_wrong_modes_for_declared_primary_comparison(tmp_path: Path):
    result = run_score(
        tmp_path,
        [base_run("raw_prompt_luna"), base_run("contract_luna_selective_sol")],
    )
    assert result.returncode != 0
    assert "must contain declared primary comparison modes" in result.stderr


def test_scorer_rejects_mixed_main_session_routes_inside_pair(tmp_path: Path):
    raw = base_run("raw_prompt_luna")
    contract = base_run("contract_luna")
    contract["main_session_route"] = "gpt-5.6-terra/high"
    result = run_score(tmp_path, [raw, contract])
    assert result.returncode != 0
    assert "mixes main-session routes" in result.stderr
