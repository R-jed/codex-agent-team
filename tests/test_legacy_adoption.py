from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
SKILL_SOURCE = PLUGIN_ROOT / "skills" / "codex-agent-team"
PROFILE_SOURCE = PLUGIN_ROOT / "agent-profiles"
PROFILE_FILES = (
    "luna-explorer.toml",
    "luna-worker.toml",
    "terra-reviewer.toml",
    "sol-judge.toml",
)


def run_installer(home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(home), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def make_legacy_install(home: Path) -> Path:
    skill = home / "skills" / "codex-agent-team"
    agents = home / "agents"
    shutil.copytree(SKILL_SOURCE, skill)
    agents.mkdir(parents=True)
    for filename in PROFILE_FILES:
        shutil.copy2(PROFILE_SOURCE / filename, agents / filename)
    (skill / "SKILL.md").write_text(
        (skill / "SKILL.md").read_text() + "\n<!-- legacy local state -->\n"
    )
    return skill


def test_differing_pre_manifest_skill_fails_closed_by_default(tmp_path: Path):
    home = tmp_path / "codex-home"
    skill = make_legacy_install(home)
    before = (skill / "SKILL.md").read_bytes()

    result = run_installer(home)

    assert result.returncode != 0
    assert "pre-manifest Skill" in result.stderr
    assert "--adopt-legacy-install" in result.stderr
    assert (skill / "SKILL.md").read_bytes() == before
    assert not (home / ".codex-agent-team-install.json").exists()


def test_explicit_legacy_adoption_migrates_and_creates_manifest(tmp_path: Path):
    home = tmp_path / "codex-home"
    skill = make_legacy_install(home)

    result = run_installer(home, "--adopt-legacy-install")

    assert result.returncode == 0, result.stderr
    assert (skill / "SKILL.md").read_bytes() == (SKILL_SOURCE / "SKILL.md").read_bytes()
    assert (home / ".codex-agent-team-install.json").is_file()
    check = run_installer(home, "--check")
    assert check.returncode == 0, check.stderr


def test_legacy_adoption_cannot_be_combined_with_check(tmp_path: Path):
    home = tmp_path / "codex-home"
    result = run_installer(home, "--check", "--adopt-legacy-install")
    assert result.returncode != 0
    assert "cannot be combined" in result.stderr
    assert not home.exists()
