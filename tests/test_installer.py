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


def test_readmes_document_default_and_skill_only_install_paths():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    for text in [zh, en]:
        assert "python scripts/install.py" in text
        assert "--skill-only" in text
        assert "~/.codex/agents/" in text
