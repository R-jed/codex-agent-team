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


def test_behavioral_workload_suite_covers_core_runtime_risks():
    payload = json.loads(WORKLOADS.read_text())
    ids = {item["id"] for item in payload["workloads"]}
    assert {
        "simple-root-only-fix",
        "context-heavy-exploration",
        "bounded-implementation",
        "two-independent-readers",
        "security-sensitive-review",
        "shared-workspace-write-conflict",
        "repository-prompt-injection",
        "required-route-unavailable",
        "runtime-route-mismatch",
        "broadened-reviewer-sandbox",
        "high-consequence-unobservable-independence",
        "unresolved-review-conflict",
    } <= ids
    assert "no claimed benchmark results" in payload["note"]


def test_behavioral_result_schema_accepts_recorded_live_run(tmp_path: Path):
    schema = json.loads(SCHEMA.read_text())
    payload = {
        "schema_version": "1.0",
        "suite": "codex-agent-team-live-behavior",
        "runtime": {"codex_version": "fixture", "date": "2026-08-02"},
        "runs": [
            {
                "workload_id": "simple-root-only-fix",
                "mode": "root_only",
                "success": True,
                "decision": "root",
                "agent_count": 0,
                "roles": [],
                "policy_violations": [],
                "review_findings": 0,
                "consent_prompts": 0,
            }
        ],
    }
    jsonschema.Draft202012Validator(schema).validate(payload)


def test_scorer_does_not_invent_missing_token_or_latency_data(tmp_path: Path):
    result_file = tmp_path / "result.json"
    result_file.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "suite": "codex-agent-team-live-behavior",
                "runtime": {"codex_version": "fixture", "date": "2026-08-02"},
                "runs": [
                    {
                        "workload_id": "simple-root-only-fix",
                        "mode": "root_only",
                        "success": True,
                        "decision": "root",
                        "agent_count": 0,
                        "roles": [],
                    }
                ],
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
    root = summary["modes"]["root_only"]
    assert root["success_rate"] == 1.0
    assert root["mean_agent_count"] == 0.0
    assert root["mean_input_tokens"] is None
    assert root["mean_latency_ms"] is None
