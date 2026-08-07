#!/usr/bin/env python3
"""Doctor script for subagents-dispatch installation diagnostics."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tomllib

# Windows compatibility: force UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from legacy_migration import (
    LEGACY_MANIFEST_NAME,
    LEGACY_LOCK_NAME,
    LEGACY_PROFILE_FILES,
    MigrationState,
    detect_legacy_state,
    format_migration_state,
    load_legacy_manifest,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose subagents-dispatch installation state.")
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex home directory (default: $CODEX_HOME or ~/.codex).",
    )
    parser.add_argument("--check", action="store_true", help="Run all diagnostics and exit with status.")
    parser.add_argument("--legacy", action="store_true", help="Show legacy migration diagnostics.")
    return parser.parse_args()


def check_current_installation(codex_home: Path) -> tuple[bool, list[str]]:
    """Check current subagents-dispatch installation.

    Uses install-agents.py --check as the canonical verifier for managed profiles.
    """
    issues: list[str] = []
    agents_dir = codex_home / "agents"
    manifest_path = codex_home / ".subagents-dispatch-agents.json"

    # Check agents directory
    if not agents_dir.is_dir():
        issues.append("Agents directory missing")
    elif agents_dir.is_symlink():
        issues.append("Agents directory is a symlink")

    # Check manifest
    if not manifest_path.is_file():
        issues.append("Managed-profile manifest missing")
    elif manifest_path.is_symlink():
        issues.append("Managed-profile manifest is a symlink")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("managed_by") != "subagents-dispatch":
                issues.append(f"Manifest managed_by is {manifest.get('managed_by')!r}, expected 'subagents-dispatch'")
            if manifest.get("schema_version") != 1:
                issues.append(f"Manifest schema_version is {manifest.get('schema_version')}, expected 1")
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            issues.append(f"Invalid manifest: {exc}")

    # Check lock file
    lock_path = codex_home / ".subagents-dispatch-agents.lock"
    if lock_path.exists() and lock_path.is_symlink():
        issues.append("Installer lock is a symlink")

    # Use canonical installer for profile verification
    # This ensures Doctor and installer have consistent health definitions
    installer_path = Path(__file__).parent / "install-agents.py"
    if installer_path.is_file():
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(installer_path), "--codex-home", str(codex_home), "--check"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                detail = (result.stderr.strip() or result.stdout.strip() or "unknown error")
                issues.append(f"Installer --check failed: {detail}")
        except subprocess.TimeoutExpired:
            issues.append("Installer --check timed out")
        except Exception as exc:
            issues.append(f"Installer --check error: {exc}")
    else:
        issues.append("Installer not found")

    return len(issues) == 0, issues


def check_legacy_state(codex_home: Path) -> MigrationState:
    """Check legacy migration state."""
    return detect_legacy_state(codex_home)


def show_legacy_diagnostics(codex_home: Path) -> None:
    """Show detailed legacy migration diagnostics."""
    legacy_state = detect_legacy_state(codex_home)
    state_name = format_migration_state(legacy_state)

    print("=== Legacy Migration Diagnostics ===")
    print(f"State: {state_name}")
    print()

    print("State flags:")
    print(f"  Legacy only: {legacy_state.legacy_only}")
    print(f"  Current only: {legacy_state.current_only}")
    print(f"  Mixed: {legacy_state.mixed}")
    print(f"  Legacy modified: {legacy_state.legacy_modified}")
    print(f"  Migration complete: {legacy_state.migration_complete}")
    print()

    # Show legacy files if present
    agents_dir = codex_home / "agents"
    legacy_manifest_path = codex_home / LEGACY_MANIFEST_NAME
    legacy_lock_path = codex_home / LEGACY_LOCK_NAME

    print("Legacy files:")
    if legacy_manifest_path.exists():
        print(f"  Manifest: {legacy_manifest_path}")
        legacy_manifest = load_legacy_manifest(legacy_manifest_path)
        if legacy_manifest:
            print(f"    Schema version: {legacy_manifest.schema_version}")
            print(f"    Managed by: {legacy_manifest.managed_by}")
            print(f"    Profiles: {', '.join(legacy_manifest.profile_hashes.keys())}")
    else:
        print("  Manifest: not found")

    if legacy_lock_path.exists():
        print(f"  Lock: {legacy_lock_path}")
    else:
        print("  Lock: not found")

    if agents_dir.is_dir():
        legacy_profiles = [f for f in LEGACY_PROFILE_FILES if (agents_dir / f).is_file()]
        if legacy_profiles:
            print(f"  Profiles: {', '.join(legacy_profiles)}")
        else:
            print("  Profiles: none found")
    else:
        print("  Profiles: agents directory not found")

    print()

    # Recommendations
    print("Recommendations:")
    if legacy_state.migration_complete:
        print("  ✓ Migration complete. No action needed.")
    elif legacy_state.legacy_only:
        print("  → Run with --migrate-legacy to migrate to current installation.")
    elif legacy_state.mixed:
        print("  → Mixed state detected. Run with --migrate-legacy to clean up legacy files.")
        if legacy_state.legacy_modified:
            print("  ⚠ Some legacy profiles were modified. They will be preserved during migration.")
    elif legacy_state.current_only:
        print("  ✓ Current installation only. No legacy files found.")


def main() -> None:
    args = parse_args()
    codex_home = args.codex_home.expanduser()
    if codex_home.is_symlink():
        fail(f"Refusing symlinked Codex home: {codex_home}")
    codex_home = codex_home.resolve()

    if args.legacy:
        show_legacy_diagnostics(codex_home)
        return

    if args.check:
        current_ok, current_issues = check_current_installation(codex_home)
        legacy_state = check_legacy_state(codex_home)

        print("=== Installation Diagnostics ===")
        print()

        print("Current installation:")
        if current_ok:
            print("  ✓ All checks passed")
        else:
            for issue in current_issues:
                print(f"  ✗ {issue}")
        print()

        print("Legacy state:")
        state_name = format_migration_state(legacy_state)
        print(f"  {state_name}")
        if legacy_state.mixed:
            print("  ⚠ Mixed state: both legacy and current files present")
        if legacy_state.legacy_modified:
            print("  ⚠ Legacy profiles were modified")
        print()

        if not current_ok:
            fail("Installation has issues. Run with --legacy for migration diagnostics.")

        if legacy_state.mixed or legacy_state.legacy_only:
            print("  → Consider running installer with --migrate-legacy")

        return

    # Default: show both current and legacy status
    current_ok, current_issues = check_current_installation(codex_home)
    legacy_state = check_legacy_state(codex_home)

    print("=== subagents-dispatch Doctor ===")
    print()

    print("Current installation:")
    if current_ok:
        print("  ✓ Healthy")
    else:
        for issue in current_issues:
            print(f"  ✗ {issue}")
    print()

    print("Legacy migration:")
    state_name = format_migration_state(legacy_state)
    print(f"  {state_name}")
    print()

    if not current_ok or legacy_state.mixed or legacy_state.legacy_only:
        print("Run with --check for full diagnostics, --legacy for migration details.")


if __name__ == "__main__":
    main()
