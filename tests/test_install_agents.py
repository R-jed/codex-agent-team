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
CURRENT_MANIFEST = ".codex-delegate-agents.json"


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


def test_fresh_install_creates_only_current_managed_generation(tmp_path: Path):
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
    (home / CURRENT_MANIFEST).unlink()
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


def test_unrelated_agent_profiles_are_preserved(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    unrelated = agents / "my-custom-agent.toml"
    unrelated.write_text('name = "my_custom_agent"\nmodel = "custom"\n')
    before = unrelated.read_bytes()

    result = run(home)

    assert result.returncode == 0, result.stderr
    assert unrelated.read_bytes() == before
    assert all((agents / filename).is_file() for filename in CURRENT_FILES)
    assert (home / CURRENT_MANIFEST).is_file()


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
