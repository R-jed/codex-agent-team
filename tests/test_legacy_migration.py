"""Tests for legacy codex-delegate -> subagents-dispatch migration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-agents.py"
DOCTOR = ROOT / "scripts" / "doctor.py"
PROFILE_SOURCE = ROOT / "agent-profiles"
POLICY = json.loads((ROOT / "policy-contract.json").read_text())
CURRENT_FILES = tuple(spec["profile_file"] for spec in POLICY["roles"].values())
CURRENT_MANIFEST = ".subagents-dispatch-agents.json"
CURRENT_LOCK = ".subagents-dispatch-agents.lock"
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


def snapshot(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }


def legacy_content_for(index: int) -> bytes:
    source = PROFILE_SOURCE / CURRENT_FILES[index]
    return source.read_bytes().replace(b"subagents_dispatch_", b"codex_delegate_")


def create_legacy_installation(home: Path) -> dict[str, bytes]:
    agents_dir = home / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    contents: dict[str, bytes] = {}
    profile_hashes: dict[str, str] = {}
    for index, legacy_name in enumerate(LEGACY_PROFILE_FILES):
        content = legacy_content_for(index)
        (agents_dir / legacy_name).write_bytes(content)
        contents[legacy_name] = content
        profile_hashes[legacy_name] = sha(content)

    manifest = {
        "schema_version": 1,
        "managed_by": LEGACY_MANAGED_BY,
        "profile_hashes": profile_hashes,
    }
    (home / LEGACY_MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (home / LEGACY_LOCK).write_bytes(b"\0")
    return contents


def assert_current_installation(home: Path) -> None:
    assert (home / CURRENT_MANIFEST).is_file()
    assert (home / CURRENT_LOCK).is_file()
    for filename in CURRENT_FILES:
        assert (home / "agents" / filename).is_file()
    check = run_installer(home, "--check")
    assert check.returncode == 0, check.stdout + check.stderr


def test_clean_v1_migration(tmp_path: Path):
    home = tmp_path / "codex-home"
    create_legacy_installation(home)

    before = run_doctor(home, "--legacy")
    assert before.returncode == 0
    assert "legacy_only" in before.stdout

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Legacy state detected" in result.stdout
    assert not (home / LEGACY_MANIFEST).exists()
    assert (home / LEGACY_LOCK).exists()
    for filename in LEGACY_PROFILE_FILES:
        assert not (home / "agents" / filename).exists()
    assert_current_installation(home)

    after = run_doctor(home, "--legacy")
    assert after.returncode == 0
    assert "migration_complete" in after.stdout


def test_modified_legacy_profile_is_preserved_with_ownership_receipt(tmp_path: Path):
    home = tmp_path / "codex-home"
    originals = create_legacy_installation(home)
    modified_name = LEGACY_PROFILE_FILES[0]
    modified = originals[modified_name] + b"\n# user modification\n"
    (home / "agents" / modified_name).write_bytes(modified)

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "WARNING" in result.stdout
    assert (home / "agents" / modified_name).read_bytes() == modified
    assert (home / LEGACY_MANIFEST).is_file(), "ownership receipt must remain while modified legacy state remains"
    for filename in LEGACY_PROFILE_FILES[1:]:
        assert not (home / "agents" / filename).exists()
    assert_current_installation(home)

    doctor = run_doctor(home, "--legacy")
    assert "current_with_preserved_legacy_modified" in doctor.stdout
    assert "Do not repeat automatic migration" in doctor.stdout

    state_after_first = snapshot(home)
    rerun = run_installer(home, "--migrate-legacy")
    assert rerun.returncode == 0, rerun.stdout + rerun.stderr
    assert snapshot(home) == state_after_first


def test_old_new_clean_mixed_state_converges(tmp_path: Path):
    home = tmp_path / "codex-home"
    assert run_installer(home).returncode == 0
    create_legacy_installation(home)

    before = run_doctor(home, "--legacy")
    assert "mixed" in before.stdout

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (home / LEGACY_MANIFEST).exists()
    assert (home / LEGACY_LOCK).exists()
    for filename in LEGACY_PROFILE_FILES:
        assert not (home / "agents" / filename).exists()
    assert_current_installation(home)


def test_partial_legacy_state_migrates_owned_files(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    content = legacy_content_for(0)
    manifest = {
        "schema_version": 1,
        "managed_by": LEGACY_MANAGED_BY,
        "profile_hashes": {LEGACY_PROFILE_FILES[0]: sha(content)},
    }
    (home / LEGACY_MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    (agents / LEGACY_PROFILE_FILES[0]).write_bytes(content)

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (home / LEGACY_MANIFEST).exists()
    assert not (agents / LEGACY_PROFILE_FILES[0]).exists()
    assert_current_installation(home)


def test_clean_migration_rerun_is_idempotent(tmp_path: Path):
    home = tmp_path / "codex-home"
    create_legacy_installation(home)
    first = run_installer(home, "--migrate-legacy")
    assert first.returncode == 0
    state_after_first = snapshot(home)

    second = run_installer(home, "--migrate-legacy")
    assert second.returncode == 0
    assert "Legacy migration already complete" in second.stdout
    assert snapshot(home) == state_after_first


def test_unowned_legacy_profile_preserves_manifest_and_reaches_explicit_terminal_state(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)

    known_hashes: dict[str, str] = {}
    for index, legacy_name in enumerate(LEGACY_PROFILE_FILES[:2]):
        content = legacy_content_for(index)
        (agents / legacy_name).write_bytes(content)
        known_hashes[legacy_name] = sha(content)

    unowned = LEGACY_PROFILE_FILES[4]
    (agents / unowned).write_bytes(b'name = "custom_legacy_agent"\n')
    (home / LEGACY_MANIFEST).write_text(
        json.dumps({"schema_version": 1, "managed_by": LEGACY_MANAGED_BY, "profile_hashes": known_hashes}),
        encoding="utf-8",
    )

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    for filename in LEGACY_PROFILE_FILES[:2]:
        assert not (agents / filename).exists()
    assert (agents / unowned).exists()
    assert (home / LEGACY_MANIFEST).exists()
    assert_current_installation(home)

    doctor = run_doctor(home, "--legacy")
    assert "current_with_preserved_legacy_ownership_unknown" in doctor.stdout
    assert "explicitly" in doctor.stdout.lower()


def test_corrupt_legacy_manifest_is_preserved_and_never_authorizes_deletion(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    legacy_profile = agents / LEGACY_PROFILE_FILES[0]
    legacy_profile.write_bytes(legacy_content_for(0))
    corrupt = b'{"managed_by":"codex-delegate","profile_hashes":'
    (home / LEGACY_MANIFEST).write_bytes(corrupt)

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    assert legacy_profile.exists()
    assert (home / LEGACY_MANIFEST).read_bytes() == corrupt
    assert "ownership is unknown" in result.stdout
    assert_current_installation(home)

    doctor = run_doctor(home, "--legacy")
    assert "current_with_preserved_legacy_ownership_unknown" in doctor.stdout
    assert "invalid or unreadable" in doctor.stdout


def test_preserved_legacy_reserved_role_collision_fails_before_mutation(tmp_path: Path):
    home = tmp_path / "codex-home"
    originals = create_legacy_installation(home)
    conflict = LEGACY_PROFILE_FILES[0]
    current_role = POLICY["roles"]["reader"]["agent_type"]
    modified = originals[conflict].replace(b"codex_delegate_reader", current_role.encode()) + b"\n# changed\n"
    (home / "agents" / conflict).write_bytes(modified)
    state_before = snapshot(home)

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode != 0
    assert "reserved current role name" in (result.stdout + result.stderr)
    assert not (home / CURRENT_MANIFEST).exists()
    # Lock files may be initialized by the attempted migration, but owned legacy data must be unchanged.
    assert (home / "agents" / conflict).read_bytes() == modified
    assert (home / LEGACY_MANIFEST).read_bytes() == state_before[LEGACY_MANIFEST]
    for filename in LEGACY_PROFILE_FILES[1:]:
        assert (home / "agents" / filename).read_bytes() == state_before[f"agents/{filename}"]


def test_legacy_manifest_symlink_is_never_removed(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    (agents / LEGACY_PROFILE_FILES[0]).write_bytes(legacy_content_for(0))
    target = tmp_path / "external-manifest.json"
    target.write_text("external", encoding="utf-8")
    manifest_path = home / LEGACY_MANIFEST
    try:
        manifest_path.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable")

    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    assert manifest_path.is_symlink()
    assert target.read_text(encoding="utf-8") == "external"
    assert (agents / LEGACY_PROFILE_FILES[0]).exists()
    assert_current_installation(home)


def test_doctor_check_is_read_only_for_legacy_only_state(tmp_path: Path):
    home = tmp_path / "codex-home"
    create_legacy_installation(home)
    before = snapshot(home)

    result = run_doctor(home, "--check")
    assert result.returncode == 1
    assert snapshot(home) == before


def test_doctor_legacy_diagnostics_for_empty_and_clean_states(tmp_path: Path):
    home = tmp_path / "codex-home"
    empty = run_doctor(home, "--legacy")
    assert empty.returncode == 0
    assert "unknown" in empty.stdout

    create_legacy_installation(home)
    legacy = run_doctor(home, "--legacy")
    assert "legacy_only" in legacy.stdout
    assert "Manifest:" in legacy.stdout

    assert run_installer(home, "--migrate-legacy").returncode == 0
    current = run_doctor(home, "--legacy")
    assert "migration_complete" in current.stdout
