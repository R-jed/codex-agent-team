from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
INSPECTOR = (
    ROOT
    / "plugins"
    / "codex-agent-team"
    / "skills"
    / "codex-agent-team"
    / "scripts"
    / "inspect-runtime.py"
)
THREAD_ID = "11111111-1111-7111-8111-111111111111"


def run_inspector(
    sessions_dir: Path, thread_id: str = THREAD_ID, *extra: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(INSPECTOR),
            "--sessions-dir",
            str(sessions_dir),
            *extra,
            thread_id,
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def write_rollout(sessions_dir: Path, thread_id: str, records: list[dict]) -> Path:
    day = sessions_dir / "2026" / "08" / "02"
    day.mkdir(parents=True, exist_ok=True)
    path = day / f"rollout-2026-08-02T00-00-00-{thread_id}.jsonl"
    path.write_text("".join(json.dumps(record) + "\n" for record in records))
    return path


def valid_records(thread_id: str = THREAD_ID) -> list[dict]:
    return [
        {
            "type": "response_item",
            "payload": {"prompt": "DO_NOT_LEAK_PROMPT", "token": "DO_NOT_LEAK_TOKEN"},
        },
        {
            "type": "event_msg",
            "payload": {
                "environment": {"SECRET_ENV": "DO_NOT_LEAK_ENV"},
                "config": {"api_key": "DO_NOT_LEAK_CONFIG"},
            },
        },
        {
            "type": "session_meta",
            "payload": {
                "id": thread_id,
                "parent_thread_id": "00000000-0000-7000-8000-000000000000",
                "agent_role": "codex_agent_team_worker",
                "agent_path": "/root/fixture",
                "model_provider": "openai",
                "cli_version": "0.145.0",
                "record_format_version": "1",
                "base_instructions": "DO_NOT_LEAK_INSTRUCTIONS",
            },
        },
        {
            "type": "turn_context",
            "payload": {
                "model": "gpt-5.6-luna",
                "effort": "max",
                "sandbox_policy": {"type": "workspace-write", "hidden": "DO_NOT_LEAK_SANDBOX"},
                "permission_profile": {"type": "default", "hidden": "DO_NOT_LEAK_PERMISSION"},
                "cwd": "/fixture/cwd",
                "summary": "DO_NOT_LEAK_SUMMARY",
            },
        },
    ]


def test_runtime_inspector_emits_only_minimal_allowlisted_metadata(tmp_path: Path):
    sessions = tmp_path / "sessions"
    write_rollout(sessions, THREAD_ID, valid_records())

    result = run_inspector(sessions)

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "agent_role": "codex_agent_team_worker",
        "effort": "max",
        "model": "gpt-5.6-luna",
        "model_provider": "openai",
        "parent_thread_id": "00000000-0000-7000-8000-000000000000",
        "permission_profile_type": "default",
        "record_format_version": "1",
        "runtime_version": "0.145.0",
        "sandbox_policy_type": "workspace-write",
        "thread_id": THREAD_ID,
    }
    assert "agent_path" not in payload
    assert "cwd" not in payload
    assert "DO_NOT_LEAK" not in result.stdout


def test_runtime_inspector_location_is_explicit_opt_in(tmp_path: Path):
    sessions = tmp_path / "sessions"
    write_rollout(sessions, THREAD_ID, valid_records())

    result = run_inspector(sessions, THREAD_ID, "--include-location")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["agent_path"] == "/root/fixture"
    assert payload["cwd"] == "/fixture/cwd"


def test_runtime_inspector_rejects_invalid_thread_id_without_scanning(tmp_path: Path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    result = run_inspector(sessions, "not-a-thread-id")
    assert result.returncode != 0
    assert "canonical lowercase UUID" in result.stderr


def test_runtime_inspector_rejects_zero_and_duplicate_matches(tmp_path: Path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    missing = run_inspector(sessions)
    assert missing.returncode != 0
    assert "no rollout filename" in missing.stderr

    write_rollout(sessions, THREAD_ID, valid_records())
    other_day = sessions / "2026" / "08" / "03"
    other_day.mkdir(parents=True)
    duplicate = other_day / f"rollout-2026-08-03T00-00-00-{THREAD_ID}.jsonl"
    duplicate.write_text("{}\n")

    result = run_inspector(sessions)
    assert result.returncode != 0
    assert "multiple rollout filenames" in result.stderr


def test_runtime_inspector_rejects_missing_or_conflicting_route_metadata(tmp_path: Path):
    sessions = tmp_path / "sessions"
    records = valid_records()
    records[-1]["payload"].pop("effort")
    write_rollout(sessions, THREAD_ID, records)

    missing = run_inspector(sessions)
    assert missing.returncode != 0
    assert "missing effort" in missing.stderr

    rollout = next(sessions.rglob("*.jsonl"))
    records = valid_records() + [
        {
            "type": "turn_context",
            "payload": {
                "model": "gpt-5.6-terra",
                "effort": "max",
                "sandbox_policy": {"type": "workspace-write"},
                "permission_profile": {"type": "default"},
                "cwd": "/fixture/cwd",
            },
        }
    ]
    rollout.write_text("".join(json.dumps(record) + "\n" for record in records))

    conflicting = run_inspector(sessions)
    assert conflicting.returncode != 0
    assert "conflicting model values" in conflicting.stderr


def test_runtime_inspector_allows_unexposed_optional_permission_fields(tmp_path: Path):
    sessions = tmp_path / "sessions"
    records = valid_records()
    records[-1]["payload"].pop("sandbox_policy")
    records[-1]["payload"].pop("permission_profile")
    records[-1]["payload"].pop("cwd")
    write_rollout(sessions, THREAD_ID, records)

    result = run_inspector(sessions)

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["sandbox_policy_type"] is None
    assert payload["permission_profile_type"] is None
    assert "cwd" not in payload


def test_runtime_inspector_rejects_symlinked_rollout(tmp_path: Path):
    sessions = tmp_path / "sessions"
    outside = tmp_path / "outside.jsonl"
    outside.write_text("".join(json.dumps(record) + "\n" for record in valid_records()))
    day = sessions / "2026" / "08" / "02"
    day.mkdir(parents=True)
    link = day / f"rollout-2026-08-02T00-00-00-{THREAD_ID}.jsonl"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks are unavailable in this environment")

    result = run_inspector(sessions)
    assert result.returncode != 0
    assert "non-symlink" in result.stderr or "outside the sessions root" in result.stderr
