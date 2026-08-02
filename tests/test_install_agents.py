from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
INSTALLER = PLUGIN_ROOT / "scripts" / "install-agents.py"
PROFILE_SOURCE = PLUGIN_ROOT / "agent-profiles"
PROFILE_FILES = (
    "codex-agent-team-reader.toml",
    "codex-agent-team-worker.toml",
    "codex-agent-team-investigator.toml",
    "codex-agent-team-advisor.toml",
)
LEGACY_PROFILE_FILES = (
    "luna-explorer.toml",
    "luna-worker.toml",
    "terra-reviewer.toml",
    "sol-judge.toml",
)
MANIFEST = ".codex-agent-team-agents.json"
FULL_MANIFEST = ".codex-agent-team-install.json"


def run_installer(home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(home), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def installed_state(root: Path) -> dict[str, tuple[int, bytes]]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): (path.stat().st_mtime_ns, path.read_bytes())
        for path in root.rglob("*")
        if path.is_file()
    }


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_companion_installer_installs_only_current_agent_profiles(tmp_path: Path):
    home = tmp_path / "codex-home"
    result = run_installer(home)
    assert result.returncode == 0, result.stderr
    assert not (home / "skills").exists()
    for filename in PROFILE_FILES:
        assert (home / "agents" / filename).read_bytes() == (PROFILE_SOURCE / filename).read_bytes()
    manifest = json.loads((home / MANIFEST).read_text())
    assert manifest["schema_version"] == 2
    assert set(manifest["profile_hashes"]) == set(PROFILE_FILES)


def test_companion_check_is_non_mutating(tmp_path: Path):
    home = tmp_path / "codex-home"
    assert run_installer(home).returncode == 0
    before = installed_state(home)
    check = run_installer(home, "--check")
    after = installed_state(home)
    assert check.returncode == 0, check.stderr
    assert "CHECK PASSED" in check.stdout
    assert before == after


def test_repeat_companion_install_is_true_no_op(tmp_path: Path):
    home = tmp_path / "codex-home"
    first = run_installer(home)
    assert first.returncode == 0, first.stderr
    before = installed_state(home)
    second = run_installer(home)
    after = installed_state(home)
    assert second.returncode == 0, second.stderr
    assert "no changes made" in second.stdout
    assert before == after


def test_user_modified_current_profile_is_never_overwritten(tmp_path: Path):
    home = tmp_path / "codex-home"
    assert run_installer(home).returncode == 0
    profile = home / "agents" / "codex-agent-team-worker.toml"
    profile.write_bytes(profile.read_bytes() + b"\n# user change\n")
    before = profile.read_bytes()
    result = run_installer(home)
    assert result.returncode != 0
    assert "not proven unchanged" in result.stderr
    assert profile.read_bytes() == before


def test_previous_current_managed_profile_can_upgrade(tmp_path: Path):
    home = tmp_path / "codex-home"
    assert run_installer(home).returncode == 0
    profile = home / "agents" / "codex-agent-team-worker.toml"
    old = profile.read_bytes() + b"\n# simulated previous package\n"
    profile.write_bytes(old)
    manifest_path = home / MANIFEST
    manifest = json.loads(manifest_path.read_text())
    manifest["profile_hashes"]["codex-agent-team-worker.toml"] = sha(old)
    manifest_path.write_text(json.dumps(manifest))
    result = run_installer(home)
    assert result.returncode == 0, result.stderr
    assert profile.read_bytes() == (PROFILE_SOURCE / "codex-agent-team-worker.toml").read_bytes()


def test_managed_legacy_profiles_are_removed_during_semantic_migration(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    legacy_hashes: dict[str, str] = {}
    for filename in LEGACY_PROFILE_FILES:
        data = f"# legacy managed {filename}\n".encode()
        (agents / filename).write_bytes(data)
        legacy_hashes[filename] = sha(data)
    (home / MANIFEST).write_text(json.dumps({"schema_version": 1, "profile_hashes": legacy_hashes}))

    result = run_installer(home)

    assert result.returncode == 0, result.stderr
    assert all(not (agents / filename).exists() for filename in LEGACY_PROFILE_FILES)
    assert all((agents / filename).is_file() for filename in PROFILE_FILES)
    manifest = json.loads((home / MANIFEST).read_text())
    assert manifest["schema_version"] == 2
    assert set(manifest["profile_hashes"]) == set(PROFILE_FILES)


def test_unproven_legacy_profile_is_left_untouched(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    legacy = agents / "luna-worker.toml"
    legacy.write_text('name = "luna_worker"\n# user-owned legacy file\n')
    before = legacy.read_bytes()

    result = run_installer(home)

    assert result.returncode == 0, result.stderr
    assert legacy.read_bytes() == before
    assert (agents / "codex-agent-team-worker.toml").is_file()


def test_full_installer_manifest_can_seed_legacy_ownership(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    old_hashes: dict[str, str] = {}
    for filename in LEGACY_PROFILE_FILES:
        data = f"# old standalone {filename}\n".encode()
        (agents / filename).write_bytes(data)
        old_hashes[filename] = sha(data)
    (home / FULL_MANIFEST).write_text(
        json.dumps({"schema_version": 1, "mode": "profile", "skill_hash": "placeholder", "profile_hashes": old_hashes})
    )

    result = run_installer(home)

    assert result.returncode == 0, result.stderr
    assert all(not (agents / filename).exists() for filename in LEGACY_PROFILE_FILES)
    assert (home / MANIFEST).is_file()


def test_unrecognized_full_manifest_schema_cannot_seed_legacy_deletion(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    legacy = agents / "luna-worker.toml"
    legacy_data = b"# user data that happens to match a supplied hash\n"
    legacy.write_bytes(legacy_data)
    (home / FULL_MANIFEST).write_text(
        json.dumps(
            {
                "schema_version": 999,
                "mode": "profile",
                "profile_hashes": {legacy.name: sha(legacy_data)},
            }
        )
    )

    result = run_installer(home)

    assert result.returncode == 0, result.stderr
    assert legacy.read_bytes() == legacy_data
    assert (agents / "codex-agent-team-worker.toml").is_file()


def test_non_profile_full_manifest_cannot_seed_legacy_deletion(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    legacy = agents / "luna-worker.toml"
    legacy_data = b"# legacy filename under a non-profile manifest\n"
    legacy.write_bytes(legacy_data)
    (home / FULL_MANIFEST).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "mode": "skill_only",
                "profile_hashes": {legacy.name: sha(legacy_data)},
            }
        )
    )

    result = run_installer(home)

    assert result.returncode == 0, result.stderr
    assert legacy.read_bytes() == legacy_data
    assert (agents / "codex-agent-team-worker.toml").is_file()


def test_full_manifest_legacy_ownership_is_consumed_after_migration(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    legacy_name = "luna-worker.toml"
    legacy_data = b"# old standalone luna-worker.toml\n"
    (agents / legacy_name).write_bytes(legacy_data)
    (home / FULL_MANIFEST).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "mode": "profile",
                "skill_hash": "placeholder",
                "profile_hashes": {legacy_name: sha(legacy_data)},
            }
        )
    )

    first = run_installer(home)
    assert first.returncode == 0, first.stderr
    assert not (agents / legacy_name).exists()
    assert json.loads((home / MANIFEST).read_text())["schema_version"] == 2

    # A user may intentionally recreate the old filename later. A stale standalone
    # manifest must not retain deletion authority after the companion ownership epoch
    # has been established.
    (agents / legacy_name).write_bytes(legacy_data)
    second = run_installer(home)

    assert second.returncode == 0, second.stderr
    assert (agents / legacy_name).read_bytes() == legacy_data
    assert "no changes made" in second.stdout


def test_exact_current_profiles_can_be_adopted_without_overwrite(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    for filename in PROFILE_FILES:
        (agents / filename).write_bytes((PROFILE_SOURCE / filename).read_bytes())
    before = {filename: (agents / filename).read_bytes() for filename in PROFILE_FILES}
    result = run_installer(home)
    assert result.returncode == 0, result.stderr
    assert (home / MANIFEST).is_file()
    assert all((agents / filename).read_bytes() == before[filename] for filename in PROFILE_FILES)


def test_check_missing_profiles_does_not_create_codex_home(tmp_path: Path):
    home = tmp_path / "missing-home"
    result = run_installer(home, "--check")
    assert result.returncode != 0
    assert not home.exists()
