#!/usr/bin/env python3
"""Install Codex Agent Team companion custom-agent profiles safely.

This installer is intended for Plugin users. Plugin installation provides the Skill,
while these role-pinned Agent TOML files live under Codex home and require a separate,
explicit setup step. The installer is transactional, refuses user-modified profiles,
and keeps its ownership manifest separate from the standalone Skill installer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import tomllib
from typing import NoReturn
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROFILE_SOURCE = ROOT / "examples" / "agents"
PROFILE_FILES = (
    "luna-explorer.toml",
    "luna-worker.toml",
    "terra-reviewer.toml",
    "sol-judge.toml",
)
EXPECTED_PROFILES = {
    "luna-explorer.toml": ("luna_explorer", "gpt-5.6-luna", "max"),
    "luna-worker.toml": ("luna_worker", "gpt-5.6-luna", "max"),
    "terra-reviewer.toml": ("terra_reviewer", "gpt-5.6-terra", "xhigh"),
    "sol-judge.toml": ("sol_judge", "gpt-5.6-sol", "high"),
}
MANIFEST_NAME = ".codex-agent-team-agents.json"
FULL_MANIFEST_NAME = ".codex-agent-team-install.json"
MANIFEST_SCHEMA = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Codex Agent Team companion custom-agent profiles."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex home directory (default: $CODEX_HOME or ~/.codex).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify all companion Agent profiles exactly; make no changes.",
    )
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json_manifest(path: Path, *, required_schema: bool) -> dict | None:
    if path.is_symlink():
        fail(f"Refusing symlinked install manifest: {path}")
    if not path.exists():
        return None
    if not path.is_file():
        fail(f"Install manifest is not a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"Invalid install manifest {path}: {exc}")
    if not isinstance(payload, dict):
        fail(f"Invalid install manifest object: {path}")
    if required_schema and payload.get("schema_version") != MANIFEST_SCHEMA:
        fail(f"Unsupported companion install manifest: {path}")
    profile_hashes = payload.get("profile_hashes", {})
    if not isinstance(profile_hashes, dict):
        fail(f"Invalid profile hashes in install manifest: {path}")
    return payload


def desired_manifest() -> dict:
    return {
        "schema_version": MANIFEST_SCHEMA,
        "profile_hashes": {
            filename: file_hash(PROFILE_SOURCE / filename) for filename in PROFILE_FILES
        },
    }


def validate_sources() -> None:
    seen_names: set[str] = set()
    for filename, expected in EXPECTED_PROFILES.items():
        path = PROFILE_SOURCE / filename
        if path.is_symlink() or not path.is_file():
            fail(f"Agent profile must be a regular non-symlink file: {path}")
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            fail(f"Invalid Agent profile {path}: {exc}")
        actual = (
            str(data.get("name", "")).strip(),
            str(data.get("model", "")).strip(),
            str(data.get("model_reasoning_effort", "")).strip(),
        )
        if actual != expected:
            fail(f"Agent profile {filename} pins {actual!r}; expected {expected!r}")
        if not str(data.get("description", "")).strip():
            fail(f"Agent profile has no description: {filename}")
        if not str(data.get("developer_instructions", "")).strip():
            fail(f"Agent profile has no developer_instructions: {filename}")
        if expected[0] in seen_names:
            fail(f"Duplicate shipped Agent role name: {expected[0]}")
        seen_names.add(expected[0])


def preflight_agents_dir(path: Path, *, check_only: bool) -> None:
    if path.is_symlink():
        fail(f"Refusing symlinked agents directory: {path}")
    if path.exists() and not path.is_dir():
        fail(f"Agents destination is not a directory: {path}")
    if check_only and not path.is_dir():
        fail(f"Required agents directory is missing: {path}")


def previous_managed_hashes(
    companion_manifest: dict | None, full_manifest: dict | None
) -> dict[str, str]:
    if companion_manifest is not None:
        return {
            str(key): str(value)
            for key, value in companion_manifest.get("profile_hashes", {}).items()
            if isinstance(key, str) and isinstance(value, str)
        }
    if full_manifest is not None:
        return {
            str(key): str(value)
            for key, value in full_manifest.get("profile_hashes", {}).items()
            if isinstance(key, str) and isinstance(value, str)
        }
    return {}


def preflight_profiles(
    agents_dir: Path,
    *,
    check_only: bool,
    old_hashes: dict[str, str],
) -> set[str]:
    upgrades: set[str] = set()

    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.is_symlink():
            fail(f"Refusing symlinked Agent profile destination: {target}")
        if not target.exists():
            if check_only:
                fail(f"Required installed Agent profile is missing: {target}")
            continue
        if not target.is_file():
            fail(f"Agent profile destination is not a regular file: {target}")
        if target.read_bytes() == source.read_bytes():
            continue
        actual_hash = file_hash(target)
        if not check_only and old_hashes.get(filename) == actual_hash:
            upgrades.add(filename)
            continue
        fail(
            "Refusing to overwrite an Agent profile that differs from the current package "
            f"and is not proven unchanged from a previous managed install: {target}"
        )

    reserved_names = {values[0] for values in EXPECTED_PROFILES.values()}
    if agents_dir.exists():
        for existing in agents_dir.glob("*.toml"):
            if existing.name in PROFILE_FILES or existing.is_symlink() or not existing.is_file():
                continue
            try:
                data = tomllib.loads(existing.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, tomllib.TOMLDecodeError):
                continue
            existing_name = str(data.get("name", "")).strip()
            if existing_name in reserved_names:
                fail(
                    "Refusing to install because another Agent file uses the reserved role name "
                    f"{existing_name!r}: {existing}"
                )
    return upgrades


def verify_profiles(agents_dir: Path) -> None:
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.is_symlink() or not target.is_file():
            fail(f"Installed Agent profile is missing or unsafe: {target}")
        if target.read_bytes() != source.read_bytes():
            fail(f"Installed Agent profile differs from shipped template: {target}")


def stage_file(directory: Path, data: bytes) -> Path:
    fd, name = tempfile.mkstemp(prefix=".codex-agent-team-agent-", dir=directory)
    staged = Path(name)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    return staged


def write_manifest(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    staged = stage_file(path.parent, data)
    try:
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def install_profiles(
    agents_dir: Path, upgrades: set[str]
) -> tuple[list[Path], dict[Path, Path]]:
    created: list[Path] = []
    backups: dict[Path, Path] = {}
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.exists() and filename not in upgrades:
            continue
        staged = stage_file(agents_dir, source.read_bytes())
        try:
            if target.exists():
                backup = agents_dir / f".{filename}.backup-{uuid.uuid4().hex}"
                target.rename(backup)
                backups[target] = backup
            staged.rename(target)
            if target not in backups:
                created.append(target)
        except BaseException:
            staged.unlink(missing_ok=True)
            raise
    return created, backups


def rollback_profiles(created: list[Path], backups: dict[Path, Path]) -> list[str]:
    errors: list[str] = []
    for path in reversed(created):
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            errors.append(f"could not remove created profile {path}: {exc}")
    for target, backup in reversed(list(backups.items())):
        try:
            target.unlink(missing_ok=True)
            backup.rename(target)
        except OSError as exc:
            errors.append(f"could not restore profile {target}: {exc}")
    return errors


def restore_manifest(path: Path, previous: bytes | None) -> list[str]:
    try:
        if previous is None:
            path.unlink(missing_ok=True)
        else:
            staged = stage_file(path.parent, previous)
            try:
                os.replace(staged, path)
            finally:
                staged.unlink(missing_ok=True)
    except OSError as exc:
        return [f"could not restore companion manifest {path}: {exc}"]
    return []


def install(codex_home: Path, check_only: bool) -> None:
    codex_home = codex_home.expanduser().resolve()
    agents_dir = codex_home / "agents"
    manifest_path = codex_home / MANIFEST_NAME
    full_manifest_path = codex_home / FULL_MANIFEST_NAME

    validate_sources()
    preflight_agents_dir(agents_dir, check_only=check_only)
    companion_manifest = load_json_manifest(manifest_path, required_schema=True)
    full_manifest = load_json_manifest(full_manifest_path, required_schema=False)
    old_hashes = previous_managed_hashes(companion_manifest, full_manifest)
    upgrades = preflight_profiles(
        agents_dir, check_only=check_only, old_hashes=old_hashes
    )

    if check_only:
        verify_profiles(agents_dir)
        print("CHECK PASSED: companion Agent profiles match shipped templates exactly.")
        return

    profiles_exact = agents_dir.is_dir() and all(
        (agents_dir / filename).is_file()
        and not (agents_dir / filename).is_symlink()
        and (agents_dir / filename).read_bytes() == (PROFILE_SOURCE / filename).read_bytes()
        for filename in PROFILE_FILES
    )
    if profiles_exact and companion_manifest == desired_manifest():
        print("Companion Agent profiles already installed exactly; no changes made.")
        return

    codex_home.mkdir(parents=True, exist_ok=True)
    agents_dir.mkdir(parents=True, exist_ok=True)
    previous_manifest = manifest_path.read_bytes() if manifest_path.is_file() else None
    created: list[Path] = []
    backups: dict[Path, Path] = {}

    try:
        created, backups = install_profiles(agents_dir, upgrades)
        verify_profiles(agents_dir)
        write_manifest(manifest_path, desired_manifest())
        verify_profiles(agents_dir)
    except BaseException as exc:
        rollback_errors = rollback_profiles(created, backups)
        rollback_errors.extend(restore_manifest(manifest_path, previous_manifest))
        if rollback_errors:
            fail(
                f"INSTALL FAILED: {exc}\nROLLBACK INCOMPLETE:\n- "
                + "\n- ".join(rollback_errors)
            )
        raise
    else:
        for backup in backups.values():
            backup.unlink(missing_ok=True)

    print(f"Companion Agent profiles installed under: {agents_dir}")
    print(f"Managed companion manifest: {manifest_path}")
    print("Verified roles: luna_explorer, luna_worker, terra_reviewer, sol_judge")
    print("Start a new Codex task so the native spawn surface discovers the Agent profiles.")


def main() -> None:
    args = parse_args()
    install(args.codex_home, args.check)


if __name__ == "__main__":
    main()
