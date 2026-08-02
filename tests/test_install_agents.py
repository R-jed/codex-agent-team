from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-agents.py"
PROFILE_SOURCE = ROOT / "examples" / "agents"
PROFILE_FILES = (
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


def test_companion_installer_installs_only_agent_profiles(tmp_path: Path):
    home = tmp_path / "codex-home"
    result = run_installer(home)
    assert result.returncode == 0, result.stderr
    assert not (home / "skills").exists()
    for filename in PROFILE_FILES:
        assert (home / "agents" / filename).read_bytes() == (PROFILE_SOURCE / filename).read_bytes()
    manifest = json.loads((home / MANIFEST).read_text())
    assert manifest["schema_version"] == 1
    assert set(manifest["profile_hashes"]) == set(PROFILE_FILES)


def test_companion_check_is_non_mutating(tmp_path: Path):
    home = tmp_path / "codex-home"
    install = run_installer(home)
    assert install.returncode == 0, install.stderr
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


def test_user_modified_profile_is_never_overwritten(tmp_path: Path):
    home = tmp_path / "codex-home"
    first = run_installer(home)
    assert first.returncode == 0, first.stderr
    profile = home / "agents" / "luna-worker.toml"
    profile.write_bytes(profile.read_bytes() + b"\n# user change\n")
    before = profile.read_bytes()

    result = run_installer(home)

    assert result.returncode != 0
    assert "not proven unchanged" in result.stderr
    assert profile.read_bytes() == before


def test_previous_companion_managed_profile_can_upgrade(tmp_path: Path):
    home = tmp_path / "codex-home"
    first = run_installer(home)
    assert first.returncode == 0, first.stderr
    profile = home / "agents" / "luna-worker.toml"
    old = profile.read_bytes() + b"\n# simulated previous package\n"
    profile.write_bytes(old)
    manifest_path = home / MANIFEST
    manifest = json.loads(manifest_path.read_text())
    manifest["profile_hashes"]["luna-worker.toml"] = sha(old)
    manifest_path.write_text(json.dumps(manifest))

    result = run_installer(home)

    assert result.returncode == 0, result.stderr
    assert profile.read_bytes() == (PROFILE_SOURCE / "luna-worker.toml").read_bytes()


def test_full_installer_manifest_can_seed_companion_upgrade_ownership(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)
    old_hashes: dict[str, str] = {}
    for filename in PROFILE_FILES:
        current = (PROFILE_SOURCE / filename).read_bytes()
        installed = current
        if filename == "terra-reviewer.toml":
            installed = current + b"\n# simulated previous standalone package\n"
        (agents / filename).write_bytes(installed)
        old_hashes[filename] = sha(installed)
    (home / FULL_MANIFEST).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "mode": "profile",
                "skill_hash": "placeholder",
                "profile_hashes": old_hashes,
            }
        )
    )

    result = run_installer(home)

    assert result.returncode == 0, result.stderr
    assert (agents / "terra-reviewer.toml").read_bytes() == (
        PROFILE_SOURCE / "terra-reviewer.toml"
    ).read_bytes()
    assert (home / MANIFEST).is_file()


def test_exact_profiles_can_be_adopted_without_overwrite(tmp_path: Path):
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
