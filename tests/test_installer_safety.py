from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "plugins" / "codex-delegate" / "scripts" / "install-agents.py"


def run_installer(target: Path, *extra: str):
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(target), *extra],
        capture_output=True,
        text=True,
    )


def test_installer_refuses_different_same_filename_profile(tmp_path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "codex-agent-team-worker.toml").write_text(
        'name = "codex_agent_team_worker"\nmodel = "gpt-5.6-terra"\ndeveloper_instructions = "custom"\n'
    )
    result = run_installer(target)
    assert result.returncode != 0
    assert "Refusing to overwrite" in result.stdout + result.stderr


def test_installer_refuses_same_reserved_role_name_in_different_file(tmp_path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "my-custom-worker.toml").write_text(
        'name = "codex_agent_team_worker"\nmodel = "gpt-5.6-terra"\ndeveloper_instructions = "custom"\n'
    )
    result = run_installer(target)
    assert result.returncode != 0
    assert "reserved role name" in result.stdout + result.stderr


def test_installer_is_idempotent_for_identical_profiles(tmp_path):
    target = tmp_path / "codex-home"
    first = run_installer(target)
    second = run_installer(target)
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert "no changes made" in second.stdout


def test_check_mode_is_non_mutating_and_verifies_current_profiles(tmp_path):
    target = tmp_path / "codex-home"
    assert run_installer(target).returncode == 0
    before = {path.name: path.read_bytes() for path in (target / "agents").glob("*.toml")}
    result = run_installer(target, "--check")
    after = {path.name: path.read_bytes() for path in (target / "agents").glob("*.toml")}
    assert result.returncode == 0, result.stderr
    assert before == after
    assert "CHECK PASSED" in result.stdout
