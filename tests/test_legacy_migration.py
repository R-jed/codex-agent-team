"""Tests for legacy codex-delegate → subagents-dispatch migration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT
INSTALLER = PLUGIN / "scripts" / "install-agents.py"
DOCTOR = PLUGIN / "scripts" / "doctor.py"
PROFILE_SOURCE = PLUGIN / "agent-profiles"
POLICY = json.loads((PLUGIN / "policy-contract.json").read_text())
CURRENT_FILES = tuple(spec["profile_file"] for spec in POLICY["roles"].values())
CURRENT_MANIFEST = ".subagents-dispatch-agents.json"
CURRENT_LOCK = ".subagents-dispatch-agents.lock"

# Legacy constants
LEGACY_MANIFEST = ".codex-delegate-agents.json"
LEGACY_LOCK = ".codex-delegate-agents.lock"
LEGACY_PROFILE_FILES = (
    "codex-delegate-reader.toml",
    "codex-delegate-worker.toml",
    "codex-delegate-solver.toml",
    "codex-delegate-investigator.toml",
    "codex-delegate-advisor.toml",
)
LEGACY_MANAGED_BY = "codex-delegate"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_installer(home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(home), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def run_doctor(home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DOCTOR), "--codex-home", str(home), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def state(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def create_legacy_profile_content(original_content: bytes, role_name: str) -> bytes:
    """Create legacy profile content with codex-delegate role names."""
    content = original_content.decode("utf-8")
    # Replace subagents_dispatch_ with codex_delegate_
    content = content.replace("subagents_dispatch_", "codex_delegate_")
    return content.encode("utf-8")


def create_legacy_installation(home: Path, *, modified: bool = False) -> None:
    """Create a legacy codex-delegate installation."""
    agents_dir = home / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Create legacy profiles with codex-delegate role names
    profile_hashes = {}
    for i, legacy_name in enumerate(LEGACY_PROFILE_FILES):
        source = PROFILE_SOURCE / CURRENT_FILES[i]
        target = agents_dir / legacy_name
        content = create_legacy_profile_content(source.read_bytes(), legacy_name)
        if modified and i == 0:  # Modify first profile
            content += b"\n# user modification\n"
        target.write_bytes(content)
        profile_hashes[legacy_name] = sha(content)

    # Create legacy manifest
    manifest = {
        "schema_version": 1,
        "managed_by": LEGACY_MANAGED_BY,
        "profile_hashes": profile_hashes,
    }
    (home / LEGACY_MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")

    # Create legacy lock
    (home / LEGACY_LOCK).write_bytes(b"\0")


def test_clean_v1_migration(tmp_path: Path):
    """Test clean migration from legacy v1 installation."""
    home = tmp_path / "codex-home"
    create_legacy_installation(home)

    # Verify legacy state before migration
    doctor_result = run_doctor(home, "--legacy")
    assert doctor_result.returncode == 0
    assert "legacy_only" in doctor_result.stdout

    # Run migration
    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0
    assert "Legacy state detected" in result.stdout
    assert "Removed legacy file" in result.stdout

    # Verify legacy files removed
    assert not (home / LEGACY_MANIFEST).exists()
    assert (home / LEGACY_LOCK).exists()  # preserved for cross-generation safety
    for filename in LEGACY_PROFILE_FILES:
        assert not (home / "agents" / filename).exists()

    # Verify current installation
    assert (home / CURRENT_MANIFEST).exists()
    for filename in CURRENT_FILES:
        assert (home / "agents" / filename).exists()

    # Verify migration complete state
    doctor_result = run_doctor(home, "--legacy")
    assert doctor_result.returncode == 0
    assert "migration_complete" in doctor_result.stdout


def test_modified_legacy_profile_preserved(tmp_path: Path):
    """Test that modified legacy profiles are preserved during migration.

    Correct scenario:
    1. Legacy install writes file + manifest hash
    2. User modifies file afterwards
    3. Migration sees current hash != ownership hash
    4. Modified legacy file is preserved
    5. Warning is emitted
    6. Current profiles are installed safely
    7. Rerun remains idempotent
    """
    home = tmp_path / "codex-home"
    agents_dir = home / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Create legacy installation with ORIGINAL content
    profile_hashes = {}
    original_contents = {}
    for i, legacy_name in enumerate(LEGACY_PROFILE_FILES):
        source = PROFILE_SOURCE / CURRENT_FILES[i]
        target = agents_dir / legacy_name
        content = create_legacy_profile_content(source.read_bytes(), legacy_name)
        target.write_bytes(content)
        original_contents[legacy_name] = content
        profile_hashes[legacy_name] = sha(content)

    # Record original hash in manifest
    manifest = {
        "schema_version": 1,
        "managed_by": LEGACY_MANAGED_BY,
        "profile_hashes": profile_hashes,
    }
    (home / LEGACY_MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")
    (home / LEGACY_LOCK).write_bytes(b"\0")

    # Step 2: User modifies first profile AFTER installation
    modified_profile = LEGACY_PROFILE_FILES[0]
    modified_content = original_contents[modified_profile] + b"\n# user modification\n"
    (agents_dir / modified_profile).write_bytes(modified_content)

    # Step 3-5: Run migration - should preserve modified file and emit warning
    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0

    # Modified profile should be PRESERVED (not deleted)
    assert (agents_dir / modified_profile).exists()
    assert (agents_dir / modified_profile).read_bytes() == modified_content

    # Unmodified profiles should be removed
    for filename in LEGACY_PROFILE_FILES[1:]:
        assert not (agents_dir / filename).exists()

    # Warning should be emitted
    assert "Preserved modified legacy file" in result.stdout or "WARNING" in result.stdout

    # Step 6: Current profiles installed safely
    assert (home / CURRENT_MANIFEST).exists()
    for filename in CURRENT_FILES:
        assert (home / "agents" / filename).exists()

    # Step 7: Rerun is idempotent
    result2 = run_installer(home, "--migrate-legacy")
    assert result2.returncode == 0
    # Modified legacy file still preserved
    assert (agents_dir / modified_profile).exists()


def test_old_new_mixed_state(tmp_path: Path):
    """Test migration from mixed legacy and current state."""
    home = tmp_path / "codex-home"

    # Install current first
    result = run_installer(home)
    assert result.returncode == 0

    # Add legacy files on top
    create_legacy_installation(home)

    # Verify mixed state
    doctor_result = run_doctor(home, "--legacy")
    assert doctor_result.returncode == 0
    assert "mixed" in doctor_result.stdout

    # Run migration
    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0

    # Verify legacy files removed
    assert not (home / LEGACY_MANIFEST).exists()
    assert (home / LEGACY_LOCK).exists()  # preserved for cross-generation safety
    for filename in LEGACY_PROFILE_FILES:
        assert not (home / "agents" / filename).exists()

    # Verify current installation intact
    assert (home / CURRENT_MANIFEST).exists()
    for filename in CURRENT_FILES:
        assert (home / "agents" / filename).exists()


def test_legacy_lock_contention(tmp_path: Path):
    """Test that legacy lock doesn't block migration."""
    home = tmp_path / "codex-home"
    create_legacy_installation(home)

    # Verify legacy lock exists
    assert (home / LEGACY_LOCK).exists()

    # Run migration - should succeed
    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0

    # Verify legacy lock preserved for cross-generation safety
    assert (home / LEGACY_LOCK).exists()


def test_partial_migration(tmp_path: Path):
    """Test migration with partial legacy state (only some files)."""
    home = tmp_path / "codex-home"
    agents_dir = home / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Create only manifest and one profile
    source_content = (PROFILE_SOURCE / CURRENT_FILES[0]).read_bytes()
    legacy_content = create_legacy_profile_content(source_content, LEGACY_PROFILE_FILES[0])
    manifest = {
        "schema_version": 1,
        "managed_by": LEGACY_MANAGED_BY,
        "profile_hashes": {
            LEGACY_PROFILE_FILES[0]: sha(legacy_content),
        },
    }
    (home / LEGACY_MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")
    (agents_dir / LEGACY_PROFILE_FILES[0]).write_bytes(legacy_content)

    # Run migration
    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0

    # Verify partial legacy removed
    assert not (home / LEGACY_MANIFEST).exists()
    assert not (agents_dir / LEGACY_PROFILE_FILES[0]).exists()

    # Verify current installation created
    assert (home / CURRENT_MANIFEST).exists()
    for filename in CURRENT_FILES:
        assert (home / "agents" / filename).exists()


def test_migration_rerun_idempotent(tmp_path: Path):
    """Test that migration is idempotent."""
    home = tmp_path / "codex-home"
    create_legacy_installation(home)

    # Run migration first time
    result1 = run_installer(home, "--migrate-legacy")
    assert result1.returncode == 0
    assert "Legacy state detected" in result1.stdout

    # Record state after first migration
    state_after_first = state(home)

    # Run migration again - should be noop
    result2 = run_installer(home, "--migrate-legacy")
    assert result2.returncode == 0
    assert "Legacy migration already complete" in result2.stdout

    # State should be unchanged
    assert state(home) == state_after_first


def test_doctor_legacy_diagnostics(tmp_path: Path):
    """Test doctor legacy diagnostics output."""
    home = tmp_path / "codex-home"

    # Test with no installation - state is unknown
    result = run_doctor(home, "--legacy")
    assert result.returncode == 0
    assert "unknown" in result.stdout

    # Test with legacy only
    create_legacy_installation(home)
    result = run_doctor(home, "--legacy")
    assert result.returncode == 0
    assert "legacy_only" in result.stdout
    assert "Manifest:" in result.stdout

    # Test with current only (after migration)
    run_installer(home, "--migrate-legacy")
    result = run_doctor(home, "--legacy")
    assert result.returncode == 0
    assert "migration_complete" in result.stdout


def test_doctor_check_excludes_migration(tmp_path: Path):
    """Test that --check doesn't trigger migration."""
    home = tmp_path / "codex-home"
    create_legacy_installation(home)

    # Record state before
    state_before = state(home)

    # Run check - should not mutate, but will fail because current installation missing
    result = run_doctor(home, "--check")
    assert result.returncode == 1  # Fails because current installation missing
    assert state(home) == state_before  # But no mutation occurred


def test_ownership_hash_verification(tmp_path: Path):
    """Test that only files with matching ownership hash are removed."""
    home = tmp_path / "codex-home"
    agents_dir = home / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Create legacy manifest with only some profiles
    profile_hashes = {}
    for i, legacy_name in enumerate(LEGACY_PROFILE_FILES[:3]):
        source = PROFILE_SOURCE / CURRENT_FILES[i]
        target = agents_dir / legacy_name
        target.write_bytes(source.read_bytes())
        profile_hashes[legacy_name] = sha(source.read_bytes())

    # Add extra profile NOT in manifest
    extra_profile = agents_dir / LEGACY_PROFILE_FILES[4]
    extra_profile.write_bytes(b"extra content not in manifest")

    manifest = {
        "schema_version": 1,
        "managed_by": LEGACY_MANAGED_BY,
        "profile_hashes": profile_hashes,
    }
    (home / LEGACY_MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")

    # Run migration
    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0

    # Verify profiles in manifest were removed
    for filename in LEGACY_PROFILE_FILES[:3]:
        assert not (agents_dir / filename).exists()

    # Verify profile NOT in manifest was preserved
    assert extra_profile.exists()
    assert extra_profile.read_bytes() == b"extra content not in manifest"
