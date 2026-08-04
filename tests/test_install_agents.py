from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
INSTALLER = PLUGIN / "scripts" / "install-agents.py"
PROFILE_SOURCE = PLUGIN / "agent-profiles"
CURRENT_FILES = (
    "codex-delegate-reader.toml",
    "codex-delegate-worker.toml",
    "codex-delegate-investigator.toml",
    "codex-delegate-advisor.toml",
)
LEGACY_TEAM_FILES = (
    "codex-agent-team-reader.toml",
    "codex-agent-team-worker.toml",
    "codex-agent-team-investigator.toml",
    "codex-agent-team-advisor.toml",
)
LEGACY_MODEL_FILES = ("luna-explorer.toml", "luna-worker.toml", "terra-reviewer.toml", "sol-judge.toml")
CURRENT_MANIFEST = ".codex-delegate-agents.json"
LEGACY_TEAM_MANIFEST = ".codex-agent-team-agents.json"
LEGACY_FULL_MANIFEST = ".codex-agent-team-install.json"


def run(home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(home), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def state(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def test_fresh_install_creates_only_current_generation(tmp_path: Path):
    home = tmp_path / "codex-home"
    result = run(home)
    assert result.returncode == 0, result.stderr
    assert {p.name for p in (home / "agents").glob("*.toml")} == set(CURRENT_FILES)
    for filename in CURRENT_FILES:
        assert (home / "agents" / filename).read_bytes() == (PROFILE_SOURCE / filename).read_bytes()
    manifest = json.loads((home / CURRENT_MANIFEST).read_text())
    assert manifest["schema_version"] == 1
    assert manifest["managed_by"] == "codex-delegate"
    assert set(manifest["profile_hashes"]) == set(CURRENT_FILES)
    assert not (home / LEGACY_TEAM_MANIFEST).exists()
    assert not (home / LEGACY_FULL_MANIFEST).exists()


def test_symlinked_codex_home_is_rejected_without_writing_target(tmp_path: Path):
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    before = state(real)
    result = run(link)
    assert result.returncode != 0
    assert "Refusing symlinked Codex home" in result.stderr
    assert state(real) == before


def test_check_is_non_mutating_and_repeat_install_is_noop(tmp_path: Path):
    home = tmp_path / "codex-home"
    assert run(home).returncode == 0
    before = state(home)
    check = run(home, "--check")
    assert check.returncode == 0, check.stderr
    assert "CHECK PASSED" in check.stdout
    assert state(home) == before
    repeat = run(home)
    assert repeat.returncode == 0, repeat.stderr
    assert "no changes made" in repeat.stdout
    assert state(home) == before


def test_modified_current_profile_is_not_overwritten_without_current_ownership(tmp_path: Path):
    home = tmp_path / "codex-home"
    assert run(home).returncode == 0
    profile = home / "agents" / "codex-delegate-worker.toml"
    profile.write_bytes(profile.read_bytes() + b"\n# user change\n")
    manifest = home / CURRENT_MANIFEST
    manifest.unlink()
    before = profile.read_bytes()
    result = run(home)
    assert result.returncode != 0
    assert "not proven unchanged" in result.stderr
    assert profile.read_bytes() == before


def test_previous_current_profile_can_upgrade_with_exact_current_manifest(tmp_path: Path):
    home = tmp_path / "codex-home"
    assert run(home).returncode == 0
    profile = home / "agents" / "codex-delegate-worker.toml"
    previous = profile.read_bytes() + b"\n# previous managed generation\n"
    profile.write_bytes(previous)
    manifest_path = home / CURRENT_MANIFEST
    manifest = json.loads(manifest_path.read_text())
    manifest["profile_hashes"][profile.name] = sha(previous)
    manifest_path.write_text(json.dumps(manifest))
    result = run(home)
    assert result.returncode == 0, result.stderr
    assert profile.read_bytes() == (PROFILE_SOURCE / profile.name).read_bytes()


def test_proven_06_team_generation_migrates_and_is_removed(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    hashes = {}
    for filename in LEGACY_TEAM_FILES:
        data = f'name = "{filename.removeprefix("codex-agent-team-").removesuffix(".toml")}"\n# managed 0.6\n'.encode()
        (agents / filename).write_bytes(data)
        hashes[filename] = sha(data)
    (home / LEGACY_TEAM_MANIFEST).write_text(json.dumps({"schema_version": 2, "profile_hashes": hashes}))

    result = run(home)

    assert result.returncode == 0, result.stderr
    assert all(not (agents / filename).exists() for filename in LEGACY_TEAM_FILES)
    assert all((agents / filename).is_file() for filename in CURRENT_FILES)
    assert not (home / LEGACY_TEAM_MANIFEST).exists()
    assert (home / CURRENT_MANIFEST).is_file()
    assert run(home, "--check").returncode == 0


def test_two_legacy_receipts_merge_disjoint_proven_ownership(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    team_file = agents / "codex-agent-team-reader.toml"
    team_data = b'name = "codex_agent_team_reader"\n# team-owned\n'
    team_file.write_bytes(team_data)
    model_file = agents / "luna-worker.toml"
    model_data = b"# older project-owned model profile\n"
    model_file.write_bytes(model_data)
    (home / LEGACY_TEAM_MANIFEST).write_text(
        json.dumps({"schema_version": 2, "profile_hashes": {team_file.name: sha(team_data)}})
    )
    (home / LEGACY_FULL_MANIFEST).write_text(
        json.dumps({"schema_version": 1, "mode": "profile", "profile_hashes": {model_file.name: sha(model_data)}})
    )

    result = run(home)

    assert result.returncode == 0, result.stderr
    assert not team_file.exists()
    assert not model_file.exists()
    assert not (home / LEGACY_TEAM_MANIFEST).exists()
    assert not (home / LEGACY_FULL_MANIFEST).exists()
    assert run(home, "--check").returncode == 0


def test_conflicting_legacy_receipts_fail_closed_before_mutation(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    old = agents / "codex-agent-team-worker.toml"
    old_data = b'name = "codex_agent_team_worker"\n# old\n'
    old.write_bytes(old_data)
    (home / LEGACY_TEAM_MANIFEST).write_text(
        json.dumps({"schema_version": 2, "profile_hashes": {old.name: sha(old_data)}})
    )
    (home / LEGACY_FULL_MANIFEST).write_text(
        json.dumps({"schema_version": 1, "mode": "profile", "profile_hashes": {old.name: "0" * 64}})
    )
    before = state(home)

    result = run(home)

    assert result.returncode != 0
    assert "Conflicting legacy ownership hashes" in result.stderr
    assert state(home) == before


def test_unproven_old_team_profile_fails_closed_and_is_untouched(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    old = agents / "codex-agent-team-worker.toml"
    old.write_text('name = "codex_agent_team_worker"\n# user modified\n')
    before = state(home)
    result = run(home)
    assert result.returncode != 0
    assert "ownership cannot be proven" in result.stderr
    assert state(home) == before


def test_legacy_team_role_in_unowned_filename_fails_closed(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    foreign = agents / "my-worker.toml"
    foreign.write_text('name = "codex_agent_team_worker"\nmodel = "gpt-5.6-luna"\n')
    before = foreign.read_bytes()
    result = run(home)
    assert result.returncode != 0
    assert "legacy codex_agent_team_* role remains" in result.stderr
    assert foreign.read_bytes() == before


def test_recognized_full_manifest_can_migrate_proven_model_named_files(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    hashes = {}
    for filename in LEGACY_MODEL_FILES:
        data = f"# previous project-owned {filename}\n".encode()
        (agents / filename).write_bytes(data)
        hashes[filename] = sha(data)
    (home / LEGACY_FULL_MANIFEST).write_text(
        json.dumps({"schema_version": 1, "mode": "profile", "profile_hashes": hashes})
    )
    result = run(home)
    assert result.returncode == 0, result.stderr
    assert all(not (agents / filename).exists() for filename in LEGACY_MODEL_FILES)
    assert not (home / LEGACY_FULL_MANIFEST).exists()
    assert (home / CURRENT_MANIFEST).exists()


def test_unrecognized_full_manifest_fails_closed_without_mutation(tmp_path: Path):
    home = tmp_path / "codex-home"
    home.mkdir()
    (home / LEGACY_FULL_MANIFEST).write_text(json.dumps({"schema_version": 999, "profile_hashes": {}}))
    before = state(home)
    result = run(home)
    assert result.returncode != 0
    assert "not a recognized profile-ownership manifest" in result.stderr
    assert state(home) == before


def test_exact_current_profiles_can_be_adopted(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    for filename in CURRENT_FILES:
        (agents / filename).write_bytes((PROFILE_SOURCE / filename).read_bytes())
    result = run(home)
    assert result.returncode == 0, result.stderr
    assert (home / CURRENT_MANIFEST).exists()
    assert run(home, "--check").returncode == 0


def test_check_missing_home_does_not_create_it(tmp_path: Path):
    home = tmp_path / "missing"
    result = run(home, "--check")
    assert result.returncode != 0
    assert not home.exists()
