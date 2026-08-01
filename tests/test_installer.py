from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_default_installer_installs_skill_and_all_locked_profiles(tmp_path):
    target = tmp_path / "codex-home"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "install.py"), "--codex-home", str(target)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (target / "skills" / "codex-agent-team" / "SKILL.md").exists()
    for filename in [
        "luna-explorer.toml",
        "luna-worker.toml",
        "terra-reviewer.toml",
        "sol-judge.toml",
    ]:
        assert (target / "agents" / filename).exists()


def test_skill_only_installer_does_not_install_profiles(tmp_path):
    target = tmp_path / "codex-home"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "install.py"),
            "--codex-home",
            str(target),
            "--skill-only",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (target / "skills" / "codex-agent-team" / "SKILL.md").exists()
    assert not (target / "agents").exists()


def test_readmes_make_locked_profiles_the_default_install_path():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "python scripts/install.py" in zh
    assert "默认安装器会一次完成两件事" in zh
    assert "--skill-only" in zh
    assert "python scripts/install.py" in en
    assert "default installer places the Skill" in en
    assert "--skill-only" in en
