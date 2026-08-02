from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "plugins" / "codex-agent-team" / "scripts" / "install-agents.py"


def run_installer(target: Path):
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(target)],
        capture_output=True,
        text=True,
    )


def test_installer_refuses_different_same_filename_profile(tmp_path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "luna-worker.toml").write_text(
        'name = "luna_worker"\nmodel = "gpt-5.6-terra"\ndeveloper_instructions = "custom"\n'
    )

    result = run_installer(target)

    assert result.returncode != 0
    assert "Refusing to overwrite" in result.stdout + result.stderr
    assert not (target / "skills").exists()


def test_installer_refuses_same_role_name_in_different_file(tmp_path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "my-custom-worker.toml").write_text(
        'name = "luna_worker"\nmodel = "gpt-5.6-terra"\ndeveloper_instructions = "custom"\n'
    )

    result = run_installer(target)

    assert result.returncode != 0
    assert "reserved role name" in result.stdout + result.stderr
    assert not (target / "skills").exists()


def test_installer_is_idempotent_for_identical_profiles(tmp_path):
    target = tmp_path / "codex-home"

    first = run_installer(target)
    second = run_installer(target)

    assert first.returncode == 0
    assert second.returncode == 0
    assert "no changes made" in second.stdout
