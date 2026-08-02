#!/usr/bin/env python3
"""Read allowlisted routing metadata for one native Codex Subagent rollout.

This helper is intentionally read-only. It locates one rollout whose filename ends in
an exact child thread UUID, streams only metadata needed for runtime evidence, and
emits a compact JSON object. Prompts, messages, instructions, environment variables,
tokens, tool arguments, arbitrary rollout payloads, and local paths are excluded by
default.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, NoReturn

THREAD_ID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Emit allowlisted runtime metadata for one native Subagent thread."
    )
    parser.add_argument("thread_id", help="Canonical lowercase native Subagent thread UUID.")
    parser.add_argument(
        "--sessions-dir",
        type=Path,
        help=(
            "Codex sessions root. Defaults to $CODEX_HOME/sessions when CODEX_HOME "
            "is set, otherwise ~/.codex/sessions."
        ),
    )
    parser.add_argument(
        "--include-location",
        action="store_true",
        help="Also emit agent_path and cwd. Off by default to minimize local path disclosure.",
    )
    return parser.parse_args()


def default_sessions_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "sessions"
    return Path.home() / ".codex" / "sessions"


def resolve_sessions_root(path: Path) -> Path:
    expanded = path.expanduser()
    if not expanded.is_dir():
        fail(f"sessions directory is unavailable: {expanded}")
    try:
        return expanded.resolve(strict=True)
    except OSError as exc:
        fail(f"could not resolve sessions directory: {exc}")


def locate_rollout(sessions_root: Path, thread_id: str) -> Path:
    suffix = f"-{thread_id}.jsonl"
    matches: list[Path] = []
    try:
        for candidate in sessions_root.rglob(f"rollout-*{suffix}"):
            if candidate.name.startswith("rollout-") and candidate.name.endswith(suffix):
                matches.append(candidate)
    except OSError as exc:
        fail(f"could not enumerate rollout files: {exc}")

    if not matches:
        fail("no rollout filename matched the requested thread id")
    if len(matches) != 1:
        fail("multiple rollout filenames matched the requested thread id")

    rollout = matches[0]
    if rollout.is_symlink() or not rollout.is_file():
        fail("matched rollout is not a regular non-symlink file")

    try:
        resolved = rollout.resolve(strict=True)
        resolved.relative_to(sessions_root)
    except (OSError, ValueError):
        fail("matched rollout resolves outside the sessions root")
    return resolved


def string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def stable_value(values: list[str | None], field: str, *, required: bool) -> str | None:
    non_null = {value for value in values if value is not None}
    if required and not non_null:
        fail(f"missing {field}")
    if len(non_null) > 1:
        fail(f"conflicting {field} values")
    return next(iter(non_null), None)


def parse_rollout(
    rollout: Path, expected_thread_id: str, *, include_location: bool
) -> dict[str, str | None]:
    session_records: list[dict[str, Any]] = []
    turn_records: list[dict[str, Any]] = []

    try:
        with rollout.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                if not raw_line.strip():
                    continue
                try:
                    record = json.loads(raw_line)
                except json.JSONDecodeError as exc:
                    fail(f"invalid JSON at rollout line {line_number}: {exc.msg}")
                if not isinstance(record, dict):
                    continue
                record_type = record.get("type")
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                if record_type == "session_meta":
                    session_records.append(payload)
                elif record_type == "turn_context":
                    turn_records.append(payload)
    except (OSError, UnicodeError) as exc:
        fail(f"could not read rollout: {exc}")

    if len(session_records) != 1:
        fail("missing or ambiguous session metadata")
    if not turn_records:
        fail("missing turn context")

    session = session_records[0]
    session_thread_id = string_or_none(session.get("id"))
    if session_thread_id != expected_thread_id:
        fail("session metadata does not identify the requested thread")

    agent_role = string_or_none(session.get("agent_role"))
    if agent_role is None:
        fail("missing agent role")

    models = [string_or_none(turn.get("model")) for turn in turn_records]
    efforts = [string_or_none(turn.get("effort")) for turn in turn_records]
    sandboxes = [
        string_or_none((turn.get("sandbox_policy") or {}).get("type"))
        if isinstance(turn.get("sandbox_policy") or {}, dict)
        else None
        for turn in turn_records
    ]
    permissions = [
        string_or_none((turn.get("permission_profile") or {}).get("type"))
        if isinstance(turn.get("permission_profile") or {}, dict)
        else None
        for turn in turn_records
    ]
    cwds = [string_or_none(turn.get("cwd")) for turn in turn_records]

    result: dict[str, str | None] = {
        "thread_id": session_thread_id,
        "parent_thread_id": string_or_none(session.get("parent_thread_id")),
        "agent_role": agent_role,
        "model_provider": string_or_none(session.get("model_provider")),
        "model": stable_value(models, "model", required=True),
        "effort": stable_value(efforts, "effort", required=True),
        "sandbox_policy_type": stable_value(
            sandboxes, "sandbox policy type", required=False
        ),
        "permission_profile_type": stable_value(
            permissions, "permission profile type", required=False
        ),
        "runtime_version": string_or_none(
            session.get("cli_version") or session.get("runtime_version") or session.get("version")
        ),
        "record_format_version": string_or_none(session.get("record_format_version")),
    }
    if include_location:
        result["agent_path"] = string_or_none(session.get("agent_path"))
        result["cwd"] = stable_value(cwds, "working directory", required=False)
    return result


def main() -> None:
    args = parse_args()
    if not THREAD_ID_RE.fullmatch(args.thread_id):
        fail("thread_id must be a canonical lowercase UUID")

    sessions_root = resolve_sessions_root(args.sessions_dir or default_sessions_dir())
    rollout = locate_rollout(sessions_root, args.thread_id)
    result = parse_rollout(rollout, args.thread_id, include_location=args.include_location)
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
