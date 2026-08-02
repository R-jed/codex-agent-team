from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
SKILL_SOURCE = PLUGIN_ROOT / "skills" / "codex-agent-team"
PROFILE_SOURCE = PLUGIN_ROOT / "agent-profiles"
MANIFEST_NAME = ".codex-agent-team-install.json"
PROFILE_FILES = (
    "luna-explorer.toml",
    "luna-worker.toml",
    "terra-reviewer.toml",
    "sol-judge.toml",
)


def run_installer(codex_home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(codex_home), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }


def installed_file_state(root: Path) -> dict[str, tuple[int, bytes]]:
    return {
        path.relative_to(root).as_posix(): (path.stat().st_mtime_ns, path.read_bytes())
        for path in root.rglob("*")
        if path.is_file()
    }


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_hash(root: Path) -> str:
    snapshot = {
        path.relative_to(root).as_posix(): sha(path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    return sha(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode())


def test_default_installer_installs_skill_profiles_and_manifest(tmp_path: Path):
    target = tmp_path / "codex-home"
    result = run_installer(target)
    assert result.returncode == 0, result.stderr
    assert tree_bytes(target / "skills" / "codex-agent-team") == tree_bytes(SKILL_SOURCE)
    for filename in PROFILE_FILES:
        assert (target / "agents" / filename).read_bytes() == (PROFILE_SOURCE / filename).read_bytes()
    manifest = json.loads((target / MANIFEST_NAME).read_text())
    assert manifest["schema_version"] == 1
    assert manifest["mode"] == "profile"
    assert manifest["skill_hash"] == tree_hash(SKILL_SOURCE)
    assert set(manifest["profile_hashes"]) == set(PROFILE_FILES)


def test_skill_only_installer_does_not_install_profiles(tmp_path: Path):
    target = tmp_path / "codex-home"
    result = run_installer(target, "--skill-only")
    assert result.returncode == 0, result.stderr
    assert (target / "skills" / "codex-agent-team" / "SKILL.md").exists()
    assert not (target / "agents").exists()
    manifest = json.loads((target / MANIFEST_NAME).read_text())
    assert manifest["mode"] == "skill_only"
    assert manifest["profile_hashes"] == {}


def test_check_is_exact_and_non_mutating(tmp_path: Path):
    target = tmp_path / "codex-home"
    install = run_installer(target)
    assert install.returncode == 0, install.stderr
    before = installed_file_state(target)
    check = run_installer(target, "--check")
    after = installed_file_state(target)
    assert check.returncode == 0, check.stderr
    assert "CHECK PASSED" in check.stdout
    assert before == after


def test_repeat_install_is_a_true_no_op(tmp_path: Path):
    target = tmp_path / "codex-home"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr
    before = installed_file_state(target)
    second = run_installer(target)
    after = installed_file_state(target)
    assert second.returncode == 0, second.stderr
    assert "no changes made" in second.stdout
    assert before == after


def test_managed_previous_profile_can_upgrade(tmp_path: Path):
    target = tmp_path / "codex-home"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr

    profile = target / "agents" / "luna-worker.toml"
    old_managed = profile.read_bytes() + b"\n# simulated previous package version\n"
    profile.write_bytes(old_managed)
    manifest_path = target / MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text())
    manifest["profile_hashes"]["luna-worker.toml"] = sha(old_managed)
    manifest_path.write_text(json.dumps(manifest))

    upgrade = run_installer(target)
    assert upgrade.returncode == 0, upgrade.stderr
    assert profile.read_bytes() == (PROFILE_SOURCE / "luna-worker.toml").read_bytes()
    updated = json.loads(manifest_path.read_text())
    assert updated["profile_hashes"]["luna-worker.toml"] == sha(profile.read_bytes())


def test_user_modified_managed_profile_is_not_overwritten(tmp_path: Path):
    target = tmp_path / "codex-home"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr
    profile = target / "agents" / "luna-worker.toml"
    profile.write_bytes(profile.read_bytes() + b"\n# user modification\n")
    before = profile.read_bytes()

    result = run_installer(target)

    assert result.returncode != 0
    assert "not proven unchanged" in result.stderr
    assert profile.read_bytes() == before


def test_managed_previous_skill_can_upgrade(tmp_path: Path):
    target = tmp_path / "codex-home"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr
    skill = target / "skills" / "codex-agent-team"
    skill_md = skill / "SKILL.md"
    skill_md.write_text(skill_md.read_text() + "\n<!-- previous managed package -->\n")
    manifest_path = target / MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text())
    manifest["skill_hash"] = tree_hash(skill)
    manifest_path.write_text(json.dumps(manifest))

    upgrade = run_installer(target)

    assert upgrade.returncode == 0, upgrade.stderr
    assert tree_bytes(skill) == tree_bytes(SKILL_SOURCE)
    assert json.loads(manifest_path.read_text())["skill_hash"] == tree_hash(SKILL_SOURCE)


def test_user_modified_managed_skill_is_not_overwritten(tmp_path: Path):
    target = tmp_path / "codex-home"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr
    skill_md = target / "skills" / "codex-agent-team" / "SKILL.md"
    skill_md.write_text(skill_md.read_text() + "\n<!-- user modification -->\n")
    before = skill_md.read_bytes()

    result = run_installer(target)

    assert result.returncode != 0
    assert "not proven unchanged" in result.stderr
    assert skill_md.read_bytes() == before


def test_profile_conflict_without_manifest_causes_zero_partial_install(tmp_path: Path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    conflict = agents / "luna-worker.toml"
    original = "name = \"luna_worker\"\nmodel = \"wrong-model\"\n"
    conflict.write_text(original)
    result = run_installer(target)
    assert result.returncode != 0
    assert conflict.read_text() == original
    assert not (target / "skills" / "codex-agent-team").exists()
    assert not (target / MANIFEST_NAME).exists()


def test_reserved_role_name_collision_is_rejected_before_mutation(tmp_path: Path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "custom.toml").write_text(
        "name = \"terra_reviewer\"\nmodel = \"gpt-5.6-terra\"\nmodel_reasoning_effort = \"xhigh\"\n"
    )
    result = run_installer(target)
    assert result.returncode != 0
    assert "reserved role name" in result.stderr
    assert not (target / "skills" / "codex-agent-team").exists()


def test_check_refuses_missing_install_without_creating_directories(tmp_path: Path):
    target = tmp_path / "missing-home"
    result = run_installer(target, "--check")
    assert result.returncode != 0
    assert not target.exists()


def test_check_requires_managed_manifest(tmp_path: Path):
    target = tmp_path / "codex-home"
    install = run_installer(target)
    assert install.returncode == 0, install.stderr
    (target / MANIFEST_NAME).unlink()
    check = run_installer(target, "--check")
    assert check.returncode != 0
    assert "manifest" in check.stderr.lower()


def test_skill_only_check_does_not_require_profiles(tmp_path: Path):
    target = tmp_path / "codex-home"
    install = run_installer(target, "--skill-only")
    check = run_installer(target, "--skill-only", "--check")
    assert install.returncode == 0, install.stderr
    assert check.returncode == 0, check.stderr
    assert not (target / "agents").exists()


def test_symlinked_profile_destination_is_rejected(tmp_path: Path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    outside = tmp_path / "outside.toml"
    outside.write_text((PROFILE_SOURCE / "luna-worker.toml").read_text())
    link = agents / "luna-worker.toml"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks are unavailable in this environment")
    result = run_installer(target)
    assert result.returncode != 0
    assert "symlinked Agent profile" in result.stderr
    assert not (target / "skills" / "codex-agent-team").exists()


def test_readmes_document_default_skill_only_check_and_doctor_paths():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    for text in [zh, en]:
        assert "python scripts/install.py" in text
        assert "--skill-only" in text
        assert "--check" in text
        assert "python scripts/doctor.py" in text
        assert "~/.codex/agents/" in text
