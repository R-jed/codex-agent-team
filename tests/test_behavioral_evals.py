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


def test_scorer_requires_pair_integrity_and_does_not_invent_missing_telemetry(tmp_path: Path):
    result_file = tmp_path / "result.json"
    result_file.write_text(
        json.dumps(
            {
                "schema_version": "2.0",
                "suite": "codex-agent-team-live-behavior",
                "runtime": {"codex_version": "fixture", "date": "2026-08-02"},
                "runs": [base_run("raw_prompt_luna"), base_run("contract_luna")],
            }
        )
    )
    result = subprocess.run(
        [sys.executable, str(SCORER), str(result_file), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["pair_count"] == 1
    assert summary["pairs"]["bounded-1"]["modes"] == ["contract_luna", "raw_prompt_luna"]
    assert summary["modes"]["contract_luna"]["mean_input_tokens"] is None
    assert summary["modes"]["contract_luna"]["mean_main_session_correction_tokens"] is None


def test_scorer_rejects_unpaired_run(tmp_path: Path):
    result_file = tmp_path / "result.json"
    result_file.write_text(
        json.dumps(
            {
                "schema_version": "2.0",
                "suite": "codex-agent-team-live-behavior",
                "runtime": {"codex_version": "fixture", "date": "2026-08-02"},
                "runs": [base_run("contract_luna")],
            }
        )
    )
    result = subprocess.run(
        [sys.executable, str(SCORER), str(result_file), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "fewer than two runs" in result.stderr
