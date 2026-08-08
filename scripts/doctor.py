#!/usr/bin/env python3
"""Doctor script for subagents-dispatch installation diagnostics."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from legacy_migration import (
    LEGACY_LOCK_NAME,
    LEGACY_MANIFEST_NAME,
    LEGACY_PROFILE_FILES,
    MigrationState,
    detect_legacy_state,
    format_migration_state,
    legacy_manifest_status,
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
    """Use install-agents.py --check as the canonical managed-profile verifier."""
    installer_path = Path(__file__).parent / "install-agents.py"
    if not installer_path.is_file():
        return False, ["Installer not found"]
    try:
        result = subprocess.run(
            [sys.executable, str(installer_path), "--codex-home", str(codex_home), "--check"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return False, ["Installer --check timed out"]
    except OSError as exc:
        return False, [f"Installer --check error: {exc}"]
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        return False, [f"Installer --check failed: {detail}"]
    return True, []


def print_legacy_recommendation(state: MigrationState) -> None:
    if state.migration_complete or state.current_only:
        print("  ✓ Migration complete. No legacy cleanup is needed.")
    elif state.preserved_legacy:
        print("  ⚠ Current profiles are installed and user-owned legacy state was preserved. Do not repeat automatic migration; review the preserved files explicitly.")
    elif state.ownership_unknown:
        print("  ⚠ Legacy ownership metadata is missing, invalid, or unsafe. Automatic migration is blocked until the legacy state is resolved explicitly.")
    elif state.legacy_only:
        print("  → Run the installer with --migrate-legacy to migrate the owned legacy state.")
    elif state.mixed:
        print("  → Run the installer with --migrate-legacy to clean up proven-owned legacy state.")
    else:
        print("  → No actionable legacy installation was detected.")


def show_legacy_diagnostics(codex_home: Path) -> None:
    state = detect_legacy_state(codex_home)
    print("=== Legacy Migration Diagnostics ===")
    print(f"State: {format_migration_state(state)}")
    print()
    print("State flags:")
    print(f"  Legacy only: {state.legacy_only}")
    print(f"  Current only: {state.current_only}")
    print(f"  Mixed: {state.mixed}")
    print(f"  Legacy modified: {state.legacy_modified}")
    print(f"  Ownership unknown: {state.ownership_unknown}")
    print(f"  Preserved legacy: {state.preserved_legacy}")
    print(f"  Migration complete: {state.migration_complete}")
    print()

    agents_dir = codex_home / "agents"
    manifest_path = codex_home / LEGACY_MANIFEST_NAME
    lock_path = codex_home / LEGACY_LOCK_NAME
    manifest_status, manifest = legacy_manifest_status(manifest_path)
    print("Legacy files:")
    if manifest_path.exists() or manifest_path.is_symlink():
        print(f"  Manifest: {manifest_path} ({manifest_status})")
        if manifest:
            print(f"    Schema version: {manifest.schema_version}")
            print(f"    Managed by: {manifest.managed_by}")
            print(f"    Owned profiles: {', '.join(manifest.profile_hashes.keys())}")
    else:
        print("  Manifest: not found")
    print(f"  Lock: {lock_path}" if lock_path.exists() else "  Lock: not found")
    if agents_dir.is_dir() and not agents_dir.is_symlink():
        profiles = [name for name in LEGACY_PROFILE_FILES if (agents_dir / name).is_file() and not (agents_dir / name).is_symlink()]
        print(f"  Active legacy profiles: {', '.join(profiles) if profiles else 'none'}")
    else:
        print("  Active legacy profiles: agents directory not available")
    print()
    print("Recommendations:")
    print_legacy_recommendation(state)


def main() -> None:
    args = parse_args()
    codex_home = args.codex_home.expanduser()
    if codex_home.is_symlink():
        fail(f"Refusing symlinked Codex home: {codex_home}")
    codex_home = codex_home.resolve()

    if args.legacy:
        show_legacy_diagnostics(codex_home)
        return

    current_ok, current_issues = check_current_installation(codex_home)
    legacy_state = detect_legacy_state(codex_home)
    print("=== Installation Diagnostics ===" if args.check else "=== subagents-dispatch Doctor ===")
    print()
    print("Current installation:")
    if current_ok:
        print("  ✓ All checks passed" if args.check else "  ✓ Healthy")
    else:
        for issue in current_issues:
            print(f"  ✗ {issue}")
    print()
    print("Legacy state:")
    print(f"  {format_migration_state(legacy_state)}")
    if legacy_state.preserved_legacy:
        print("  ⚠ User-owned legacy state is preserved and requires explicit review.")
    elif legacy_state.ownership_unknown:
        print("  ⚠ Legacy ownership is unknown; automatic migration is blocked.")
    elif legacy_state.mixed:
        print("  ⚠ Mixed current/legacy state is present.")
    print()

    if not current_ok:
        fail("Installation has issues. Run with --legacy for migration diagnostics.")
    if legacy_state.legacy_only or (legacy_state.mixed and not legacy_state.preserved_legacy and not legacy_state.ownership_unknown):
        print("  → Consider running installer with --migrate-legacy")
    elif legacy_state.preserved_legacy or legacy_state.ownership_unknown:
        print("  → Run with --legacy for the exact preserved-state guidance.")


if __name__ == "__main__":
    main()
