#!/usr/bin/env python3
"""Legacy migration contract for codex-delegate -> subagents-dispatch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import NamedTuple

LEGACY_MANAGED_BY = "codex-delegate"
LEGACY_MANIFEST_NAME = ".codex-delegate-agents.json"
LEGACY_LOCK_NAME = ".codex-delegate-agents.lock"
LEGACY_ROLE_PREFIX = "codex-delegate"
LEGACY_AGENT_TYPE_PREFIX = "codex_delegate"

CURRENT_MANAGED_BY = "subagents-dispatch"
CURRENT_MANIFEST_NAME = ".subagents-dispatch-agents.json"
CURRENT_LOCK_NAME = ".subagents-dispatch-agents.lock"

LEGACY_PROFILE_FILES = (
    "codex-delegate-reader.toml",
    "codex-delegate-worker.toml",
    "codex-delegate-solver.toml",
    "codex-delegate-investigator.toml",
    "codex-delegate-advisor.toml",
)


class LegacyMigrationError(RuntimeError):
    """Raised when legacy state changes or cannot be mutated safely."""


class LegacyManifest(NamedTuple):
    schema_version: int
    managed_by: str
    profile_hashes: dict[str, str]


class MigrationState(NamedTuple):
    legacy_only: bool
    current_only: bool
    mixed: bool
    legacy_modified: bool
    legacy_ownership_unknown: bool
    preserved_legacy: bool
    migration_complete: bool


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def artifact_exists(path: Path) -> bool:
    """Return True for normal paths and symlink artifacts, including broken symlinks."""
    return path.is_symlink() or path.exists()


def load_legacy_manifest(path: Path) -> LegacyManifest | None:
    """Load a valid legacy manifest, otherwise return None without trusting it."""
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
    profile_hashes = payload.get("profile_hashes", {})
    if not isinstance(profile_hashes, dict):
        return None
    return LegacyManifest(
        schema_version=payload.get("schema_version", 0),
        managed_by=payload["managed_by"],
        profile_hashes={
            str(k): str(v)
            for k, v in profile_hashes.items()
            if isinstance(k, str) and isinstance(v, str)
        },
    )


def detect_legacy_state(codex_home: Path) -> MigrationState:
    """Detect migration state while keeping unknown ownership distinct from absence."""
    agents_dir = codex_home / "agents"
    legacy_manifest_path = codex_home / LEGACY_MANIFEST_NAME
    current_manifest_path = codex_home / CURRENT_MANIFEST_NAME

    legacy_manifest = load_legacy_manifest(legacy_manifest_path)
    legacy_manifest_artifact = artifact_exists(legacy_manifest_path)
    legacy_manifest_invalid = legacy_manifest_artifact and legacy_manifest is None

    legacy_profiles: list[str] = []
    if agents_dir.is_dir():
        for filename in LEGACY_PROFILE_FILES:
            profile_path = agents_dir / filename
            if artifact_exists(profile_path):
                legacy_profiles.append(filename)

    current_manifest = None
    if current_manifest_path.is_file() and not current_manifest_path.is_symlink():
        try:
            payload = json.loads(current_manifest_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and payload.get("managed_by") == CURRENT_MANAGED_BY:
                current_manifest = payload
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass

    legacy_modified = False
    ownership_unknown = legacy_manifest_invalid
    if legacy_profiles:
        if legacy_manifest is None:
            ownership_unknown = True
        else:
            for filename in legacy_profiles:
                profile_path = agents_dir / filename
                expected_hash = legacy_manifest.profile_hashes.get(filename)
                if expected_hash is None or profile_path.is_symlink() or not profile_path.is_file():
                    ownership_unknown = True
                    continue
                try:
                    actual_hash = sha256_bytes(profile_path.read_bytes())
                except OSError:
                    ownership_unknown = True
                    continue
                if actual_hash != expected_hash:
                    legacy_modified = True

    has_legacy = legacy_manifest_artifact or bool(legacy_profiles)
    has_current = current_manifest is not None
    preserved_legacy = has_current and has_legacy and (legacy_modified or ownership_unknown)

    return MigrationState(
        legacy_only=has_legacy and not has_current,
        current_only=has_current and not has_legacy,
        mixed=has_legacy and has_current,
        legacy_modified=legacy_modified,
        legacy_ownership_unknown=ownership_unknown,
        preserved_legacy=preserved_legacy,
        migration_complete=not has_legacy and has_current,
    )


def collect_legacy_files(codex_home: Path) -> dict[str, bytes]:
    """Snapshot mutable legacy data for rollback and drift checks.

    The legacy lock is deliberately excluded. Migration holds that lock while this
    function runs, Windows may deny a second read handle, and the lock is never a
    cleanup target or rollback payload.
    """
    agents_dir = codex_home / "agents"
    files: dict[str, bytes] = {}

    legacy_manifest_path = codex_home / LEGACY_MANIFEST_NAME
    if legacy_manifest_path.is_file() and not legacy_manifest_path.is_symlink():
        files[LEGACY_MANIFEST_NAME] = legacy_manifest_path.read_bytes()

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
    """Return removal decisions proven by the legacy ownership receipt.

    Unknown, modified, symlinked, or unowned files are always preserved. The legacy
    lock is intentionally retained as the cross-generation coordination primitive.
    The manifest is removed only when every active legacy profile can also be removed.
    """
    agents_dir = codex_home / "agents"
    result: dict[str, bool] = {}
    profile_decisions: list[bool] = []

    for filename in LEGACY_PROFILE_FILES:
        profile_path = agents_dir / filename
        if not artifact_exists(profile_path):
            continue
        relative = f"agents/{filename}"
        can_remove = False
        if (
            legacy_manifest is not None
            and not profile_path.is_symlink()
            and profile_path.is_file()
        ):
            expected_hash = legacy_manifest.profile_hashes.get(filename)
            if expected_hash is not None:
                try:
                    can_remove = sha256_bytes(profile_path.read_bytes()) == expected_hash
                except OSError:
                    can_remove = False
        result[relative] = can_remove
        profile_decisions.append(can_remove)

    manifest_path = codex_home / LEGACY_MANIFEST_NAME
    if artifact_exists(manifest_path):
        result[LEGACY_MANIFEST_NAME] = legacy_manifest is not None and all(profile_decisions)

    lock_path = codex_home / LEGACY_LOCK_NAME
    if artifact_exists(lock_path):
        result[LEGACY_LOCK_NAME] = False

    return result


class LegacyBackup(NamedTuple):
    """Snapshot and ownership decisions captured before migration mutation."""

    files: dict[str, bytes]
    removal_map: dict[str, bool]


def backup_legacy_files(codex_home: Path) -> tuple[LegacyBackup, list[str]]:
    """Snapshot legacy files and compute fail-closed removal decisions."""
    legacy_manifest_path = codex_home / LEGACY_MANIFEST_NAME
    legacy_manifest = load_legacy_manifest(legacy_manifest_path)
    removal_map = can_safely_remove_legacy(codex_home, legacy_manifest)
    files = collect_legacy_files(codex_home)

    warnings: list[str] = []
    if artifact_exists(legacy_manifest_path) and legacy_manifest is None:
        warnings.append("Legacy manifest is invalid or unsafe; ownership is unknown and legacy state will be preserved.")
    for relative_path, can_remove in removal_map.items():
        if relative_path == LEGACY_LOCK_NAME:
            continue
        if not can_remove and artifact_exists(codex_home / relative_path):
            warnings.append(f"Will preserve legacy file with modified or unproven ownership: {relative_path}")

    return LegacyBackup(files=files, removal_map=removal_map), warnings


def commit_legacy_cleanup(
    codex_home: Path,
    backup: LegacyBackup,
) -> tuple[list[str], list[str]]:
    """Remove only unchanged files that were proven removable at snapshot time.

    Any drift aborts the transaction. The caller owns rollback of earlier removals.
    """
    messages: list[str] = []
    warnings: list[str] = []
    agents_dir = codex_home / "agents"

    for relative_path, can_remove in backup.removal_map.items():
        target = codex_home / relative_path
        if not can_remove:
            if relative_path != LEGACY_LOCK_NAME and artifact_exists(target):
                warnings.append(f"Preserved legacy file: {relative_path}")
            continue

        expected = backup.files.get(relative_path)
        if expected is None:
            raise LegacyMigrationError(f"Legacy snapshot missing removable file: {relative_path}")
        if target.is_symlink() or not target.is_file():
            raise LegacyMigrationError(f"Legacy state changed before cleanup: {relative_path}")
        try:
            current = target.read_bytes()
        except OSError as exc:
            raise LegacyMigrationError(f"Could not re-read legacy file before cleanup {relative_path}: {exc}") from exc
        if current != expected:
            raise LegacyMigrationError(f"Legacy file changed after snapshot; refusing removal: {relative_path}")
        target.unlink()
        messages.append(f"Removed legacy file: {relative_path}")

    if agents_dir.is_dir() and not any(agents_dir.iterdir()):
        agents_dir.rmdir()
        messages.append("Removed empty agents directory")

    return messages, warnings


def rollback_legacy_cleanup(codex_home: Path, backup: LegacyBackup) -> list[str]:
    """Restore snapshot files that this migration removed without overwriting drift."""
    errors: list[str] = []

    for relative_path, data in backup.files.items():
        target = codex_home / relative_path
        if artifact_exists(target):
            if target.is_symlink() or not target.is_file():
                errors.append(f"refusing to overwrite changed legacy artifact {relative_path}")
                continue
            try:
                if target.read_bytes() != data:
                    errors.append(f"refusing to overwrite drifted legacy file {relative_path}")
            except OSError as exc:
                errors.append(f"could not verify existing legacy file {relative_path}: {exc}")
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
    """Legacy cleanup helper retained for compatibility with direct callers."""
    del current_profile_source, current_profile_files
    backup, warnings = backup_legacy_files(codex_home)
    if dry_run:
        messages = [
            f"Would remove: {path}"
            for path, can_remove in backup.removal_map.items()
            if can_remove
        ]
        return messages, warnings
    messages, commit_warnings = commit_legacy_cleanup(codex_home, backup)
    warnings.extend(commit_warnings)
    return messages, warnings


def format_migration_state(state: MigrationState) -> str:
    """Format migration state with preserved/unknown ownership as terminal evidence."""
    if state.migration_complete:
        return "migration_complete"
    if state.preserved_legacy:
        if state.legacy_ownership_unknown:
            return "current_with_preserved_legacy_ownership_unknown"
        if state.legacy_modified:
            return "current_with_preserved_legacy_modified"
        return "current_with_preserved_legacy"
    if state.mixed:
        if state.legacy_ownership_unknown:
            return "mixed_legacy_ownership_unknown"
        if state.legacy_modified:
            return "mixed_legacy_modified"
        return "mixed"
    if state.legacy_only:
        if state.legacy_ownership_unknown:
            return "legacy_only_ownership_unknown"
        if state.legacy_modified:
            return "legacy_only_modified"
        return "legacy_only"
    if state.current_only:
        return "current_only"
    return "unknown"
