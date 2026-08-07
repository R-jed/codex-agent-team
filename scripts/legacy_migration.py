#!/usr/bin/env python3
"""Legacy migration contract for codex-delegate → subagents-dispatch."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tomllib
from typing import NamedTuple

# Legacy plugin identity
LEGACY_MANAGED_BY = "codex-delegate"
LEGACY_MANIFEST_NAME = ".codex-delegate-agents.json"
LEGACY_LOCK_NAME = ".codex-delegate-agents.lock"
LEGACY_ROLE_PREFIX = "codex-delegate"
LEGACY_AGENT_TYPE_PREFIX = "codex_delegate"

# Current plugin identity
CURRENT_MANAGED_BY = "subagents-dispatch"
CURRENT_MANIFEST_NAME = ".subagents-dispatch-agents.json"
CURRENT_LOCK_NAME = ".subagents-dispatch-agents.lock"

# Legacy profile file names (5 roles)
LEGACY_PROFILE_FILES = (
    "codex-delegate-reader.toml",
    "codex-delegate-worker.toml",
    "codex-delegate-solver.toml",
    "codex-delegate-investigator.toml",
    "codex-delegate-advisor.toml",
)


class LegacyManifest(NamedTuple):
    schema_version: int
    managed_by: str
    profile_hashes: dict[str, str]


class MigrationState(NamedTuple):
    legacy_only: bool
    current_only: bool
    mixed: bool
    legacy_modified: bool
    migration_complete: bool


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_legacy_manifest(path: Path) -> LegacyManifest | None:
    """Load legacy manifest if it exists and is valid."""
    if path.is_symlink() or not path.exists() or not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    if payload.get("managed_by") != LEGACY_MANAGED_BY:
        return None
    return LegacyManifest(
        schema_version=payload.get("schema_version", 0),
        managed_by=payload["managed_by"],
        profile_hashes={
            str(k): str(v)
            for k, v in payload.get("profile_hashes", {}).items()
            if isinstance(k, str) and isinstance(v, str)
        },
    )


def detect_legacy_state(codex_home: Path) -> MigrationState:
    """Detect the current migration state."""
    agents_dir = codex_home / "agents"
    legacy_manifest_path = codex_home / LEGACY_MANIFEST_NAME
    current_manifest_path = codex_home / CURRENT_MANIFEST_NAME

    legacy_manifest = load_legacy_manifest(legacy_manifest_path)

    # Check for legacy profiles
    legacy_profiles_exist = []
    if agents_dir.is_dir():
        for filename in LEGACY_PROFILE_FILES:
            profile_path = agents_dir / filename
            if profile_path.is_file() and not profile_path.is_symlink():
                legacy_profiles_exist.append(filename)

    # Check for current profiles
    current_manifest = None
    if current_manifest_path.is_file() and not current_manifest_path.is_symlink():
        try:
            payload = json.loads(current_manifest_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and payload.get("managed_by") == CURRENT_MANAGED_BY:
                current_manifest = payload
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass

    has_legacy = legacy_manifest is not None or len(legacy_profiles_exist) > 0
    has_current = current_manifest is not None

    # Check if legacy profiles were modified
    legacy_modified = False
    if legacy_manifest and agents_dir.is_dir():
        for filename, expected_hash in legacy_manifest.profile_hashes.items():
            profile_path = agents_dir / filename
            if profile_path.is_file():
                actual_hash = sha256_bytes(profile_path.read_bytes())
                if actual_hash != expected_hash:
                    legacy_modified = True
                    break

    return MigrationState(
        legacy_only=has_legacy and not has_current,
        current_only=has_current and not has_legacy,
        mixed=has_legacy and has_current,
        legacy_modified=legacy_modified,
        migration_complete=not has_legacy and has_current,
    )


def collect_legacy_files(codex_home: Path) -> dict[str, bytes]:
    """Collect all legacy-managed files for potential cleanup."""
    agents_dir = codex_home / "agents"
    files: dict[str, bytes] = {}

    # Legacy manifest
    legacy_manifest_path = codex_home / LEGACY_MANIFEST_NAME
    if legacy_manifest_path.is_file() and not legacy_manifest_path.is_symlink():
        files[LEGACY_MANIFEST_NAME] = legacy_manifest_path.read_bytes()

    # Legacy lock
    legacy_lock_path = codex_home / LEGACY_LOCK_NAME
    if legacy_lock_path.is_file() and not legacy_lock_path.is_symlink():
        files[LEGACY_LOCK_NAME] = legacy_lock_path.read_bytes()

    # Legacy profiles
    if agents_dir.is_dir():
        for filename in LEGACY_PROFILE_FILES:
            profile_path = agents_dir / filename
            if profile_path.is_file() and not profile_path.is_symlink():
                files[f"agents/{filename}"] = profile_path.read_bytes()

    return files


def can_safely_remove_legacy(
    codex_home: Path,
    legacy_manifest: LegacyManifest | None,
) -> dict[str, bool]:
    """Determine which legacy files can be safely removed.

    Returns dict of relative_path -> can_remove.
    Only files whose hash matches the legacy manifest ownership can be removed.
    """
    agents_dir = codex_home / "agents"
    result: dict[str, bool] = {}

    # Legacy manifest itself can be removed if we're migrating
    result[LEGACY_MANIFEST_NAME] = True

    # Legacy lock: preserved during compatibility period
    # Cross-generation contention tests depend on both lock files coexisting
    result[LEGACY_LOCK_NAME] = False

    # Legacy profiles: only if hash matches manifest ownership
    if legacy_manifest and agents_dir.is_dir():
        for filename in LEGACY_PROFILE_FILES:
            profile_path = agents_dir / filename
            if not profile_path.is_file() or profile_path.is_symlink():
                continue
            expected_hash = legacy_manifest.profile_hashes.get(filename)
            if expected_hash is None:
                # Not in legacy manifest, don't touch
                result[f"agents/{filename}"] = False
            else:
                actual_hash = sha256_bytes(profile_path.read_bytes())
                result[f"agents/{filename}"] = actual_hash == expected_hash
    else:
        # No legacy manifest, don't remove any profiles
        for filename in LEGACY_PROFILE_FILES:
            result[f"agents/{filename}"] = False

    return result


class LegacyBackup(NamedTuple):
    """Snapshot of legacy files before destructive migration."""
    files: dict[str, bytes]
    removal_map: dict[str, bool]


def backup_legacy_files(
    codex_home: Path,
) -> tuple[LegacyBackup, list[str]]:
    """Phase 1: Snapshot all legacy files without mutation.

    Returns (backup, warnings).
    """
    agents_dir = codex_home / "agents"
    legacy_manifest_path = codex_home / LEGACY_MANIFEST_NAME
    legacy_manifest = load_legacy_manifest(legacy_manifest_path)

    removal_map = can_safely_remove_legacy(codex_home, legacy_manifest)
    files = collect_legacy_files(codex_home)

    warnings: list[str] = []
    for relative_path, can_remove in removal_map.items():
        if not can_remove and (codex_home / relative_path).exists():
            warnings.append(f"Will preserve modified legacy file: {relative_path}")

    return LegacyBackup(files=files, removal_map=removal_map), warnings


def commit_legacy_cleanup(
    codex_home: Path,
    backup: LegacyBackup,
) -> tuple[list[str], list[str]]:
    """Phase 2: Remove legacy files. Returns (messages, warnings).

    Only files marked removable AND present in the backup snapshot are touched.
    """
    messages: list[str] = []
    warnings: list[str] = []
    agents_dir = codex_home / "agents"

    for relative_path, can_remove in backup.removal_map.items():
        if relative_path not in backup.files:
            continue
        target = codex_home / relative_path
        if not target.exists():
            continue
        if can_remove:
            target.unlink(missing_ok=True)
            messages.append(f"Removed legacy file: {relative_path}")
        else:
            warnings.append(f"Preserved modified legacy file: {relative_path}")

    if agents_dir.is_dir() and not any(agents_dir.iterdir()):
        agents_dir.rmdir()
        messages.append("Removed empty agents directory")

    return messages, warnings


def rollback_legacy_cleanup(
    codex_home: Path,
    backup: LegacyBackup,
) -> list[str]:
    """Restore legacy files from backup snapshot. Returns errors."""
    errors: list[str] = []

    for relative_path, data in backup.files.items():
        target = codex_home / relative_path
        if target.exists():
            continue
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        except OSError as exc:
            errors.append(f"could not restore {relative_path}: {exc}")

    return errors


def migrate_legacy_to_current(
    codex_home: Path,
    current_profile_source: Path,
    current_profile_files: tuple[str, ...],
    *,
    dry_run: bool = False,
) -> tuple[list[str], list[str]]:
    """Migrate from legacy codex-delegate to current subagents-dispatch.

    Returns (messages, warnings).
    """
    if dry_run:
        backup, warnings = backup_legacy_files(codex_home)
        messages = [f"Would remove: {p}" for p in backup.files if backup.removal_map.get(p, False)]
        return messages, warnings

    backup, warnings = backup_legacy_files(codex_home)
    messages, commit_warnings = commit_legacy_cleanup(codex_home, backup)
    warnings.extend(commit_warnings)
    return messages, warnings


def format_migration_state(state: MigrationState) -> str:
    """Format migration state for display."""
    if state.migration_complete:
        return "migration_complete"
    if state.mixed:
        if state.legacy_modified:
            return "mixed_legacy_modified"
        return "mixed"
    if state.legacy_only:
        if state.legacy_modified:
            return "legacy_only_modified"
        return "legacy_only"
    if state.current_only:
        return "current_only"
    return "unknown"
