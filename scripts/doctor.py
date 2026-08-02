#!/usr/bin/env python3
"""Inspect local Codex Agent Team installation and runtime prerequisites.

The doctor is intentionally non-mutating. It checks local package integrity and the
availability of runtime evidence surfaces that can be inspected without spawning a
model. Live child routing still has to be verified inside an active Codex session.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / "skill" / "codex-agent-team"
PROFILE_SOURCE = ROOT / "examples" / "agents"
PROFILE_FILES = (
    "luna-explorer.toml",
    "luna-worker.toml",
    "terra-reviewer.toml",
    "sol-judge.toml",
)
MANIFEST_NAME = ".codex-agent-team-install.json"
MANIFEST_SCHEMA = 1


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def tree_hash(root: Path) -> str:
    snapshot = {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    return digest_bytes(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode())


def expected_manifest(mode: str) -> dict[str, Any]:
    return {
        "schema_version": MANIFEST_SCHEMA,
        "mode": mode,
        "skill_hash": tree_hash(SKILL_SOURCE),
        "profile_hashes": (
            {}
            if mode == "skill_only"
            else {filename: digest(PROFILE_SOURCE / filename) for filename in PROFILE_FILES}
        ),
    }


def manifest_status(path: Path) -> str:
    if path.is_symlink():
        return "unsafe_symlink"
    if not path.is_file():
        return "missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return "invalid"
    if not isinstance(payload, dict) or payload.get("schema_version") != MANIFEST_SCHEMA:
        return "invalid"
    mode = payload.get("mode")
    if mode not in {"profile", "skill_only"}:
        return "invalid"
    return "exact" if payload == expected_manifest(mode) else "stale"


def codex_version() -> str | None:
    binary = shutil.which("codex")
    if not binary:
        return None
    try:
        result = subprocess.run(
            [binary, "--version"], text=True, capture_output=True, check=False, timeout=5
        )
    except (OSError, subprocess.SubprocessError):
        return None
    text = (result.stdout or result.stderr).strip()
    return text or None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose Codex Agent Team installation.")
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    home = args.codex_home.expanduser().resolve()
    installed_skill = home / "skills" / "codex-agent-team"
    agents_dir = home / "agents"
    sessions_dir = home / "sessions"
    manifest = home / MANIFEST_NAME

    profile_status: dict[str, str] = {}
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.is_symlink():
            profile_status[filename] = "unsafe_symlink"
        elif not target.is_file():
            profile_status[filename] = "missing"
        elif target.read_bytes() == source.read_bytes():
            profile_status[filename] = "exact"
        else:
            profile_status[filename] = "different"

    if installed_skill.is_symlink():
        skill_status = "unsafe_symlink"
    elif not installed_skill.is_dir():
        skill_status = "missing"
    else:
        try:
            skill_status = "exact" if tree_hash(installed_skill) == tree_hash(SKILL_SOURCE) else "different"
        except OSError:
            skill_status = "unreadable"

    managed_manifest = manifest_status(manifest)
    profile_exact = all(v == "exact" for v in profile_status.values())
    result: dict[str, Any] = {
        "python": sys.version.split()[0],
        "codex_version": codex_version(),
        "codex_home": str(home),
        "skill_integrity": skill_status,
        "profiles": profile_status,
        "managed_manifest": managed_manifest,
        "local_sessions_store": "available" if sessions_dir.is_dir() else "unavailable",
        "local_rollout_adapter": "available" if (SKILL_SOURCE / "scripts" / "inspect-runtime.py").is_file() else "missing",
        "runtime_verifier": "available" if (SKILL_SOURCE / "scripts" / "verify-runtime.py").is_file() else "missing",
        "live_spawn_surface": "requires_in_session_check",
        "native_runtime_metadata": "requires_in_session_check",
        "recommended_mode": (
            "profile_mode"
            if skill_status == "exact" and profile_exact and managed_manifest == "exact"
            else "repair_or_portable_mode"
        ),
    }

    if args.json:
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return

    print("Codex Agent Team doctor")
    print(f"Python:                  {result['python']}")
    print(f"Codex:                   {result['codex_version'] or 'not found'}")
    print(f"Skill integrity:         {skill_status}")
    for filename, status in profile_status.items():
        print(f"Profile {filename:<21} {status}")
    print(f"Managed manifest:        {managed_manifest}")
    print(f"Local sessions store:    {result['local_sessions_store']}")
    print(f"Runtime verifier:        {result['runtime_verifier']}")
    print("Live spawn/model/effort: requires an active Codex session")
    print(f"Recommended mode:        {result['recommended_mode']}")


if __name__ == "__main__":
    main()
