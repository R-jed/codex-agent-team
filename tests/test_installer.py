from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"
SKILL_SOURCE = ROOT / "skill" / "codex-agent-team"
PROFILE_SOURCE = ROOT / "examples" / "agents"
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


def test_default_installer_installs_skill_and_all_locked_profiles(tmp_path: Path):
    target = tmp_path / "codex-home"
    result = run_installer(target)
    assert result.returncode == 0, result.stderr
    assert tree_bytes(target / "skills" / "codex-agent-team") == tree_bytes(SKILL_SOURCE)
    for filename in PROFILE_FILES:
        assert (target / "agents" / filename).read_bytes() == (
            PROFILE_SOURCE / filename
        ).read_bytes()


def test_skill_only_installer_does_not_install_profiles(tmp_path: Path):
    target = tmp_path / "codex-home"
    result = run_installer(target, "--skill-only")
    assert result.returncode == 0, result.stderr
    assert (target / "skills" / "codex-agent-team" / "SKILL.md").exists()
    assert not (target / "agents").exists()


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
    assert before == after
    assert tree_bytes(target / "skills" / "codex-agent-team") == tree_bytes(SKILL_SOURCE)


def test_profile_conflict_causes_zero_partial_install(tmp_path: Path):
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
    for filename in PROFILE_FILES:
        if filename != "luna-worker.toml":
            assert not (agents / filename).exists()


def test_reserved_role_name_collision_is_rejected_before_mutation(tmp_path: Path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "custom.toml").write_text(
        "name = \"terra_reviewer\"\n"
        "model = \"gpt-5.6-terra\"\n"
        "model_reasoning_effort = \"xhigh\"\n"
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


def test_readmes_document_default_skill_only_and_check_paths():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    for text in [zh, en]:
        assert "python scripts/install.py" in text
        assert "--skill-only" in text
        assert "--check" in text
        assert "~/.codex/agents/" in text
