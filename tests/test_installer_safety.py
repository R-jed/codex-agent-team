from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-agents.py"


def run_installer(target: Path, *extra: str):
    return subprocess.run([sys.executable, str(INSTALLER), "--codex-home", str(target), *extra], capture_output=True, text=True)


def test_installer_refuses_different_same_filename_profile(tmp_path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "subagents-dispatch-worker.toml").write_text(
        'name = "subagents_dispatch_worker"\nmodel = "gpt-5.6-terra"\ndeveloper_instructions = "custom"\n'
    )
    result = run_installer(target)
    assert result.returncode != 0
    assert "Refusing to overwrite" in result.stdout + result.stderr


def test_installer_refuses_same_current_reserved_role_name_in_different_file(tmp_path):
    target = tmp_path / "codex-home"
    agents = target / "agents"
    agents.mkdir(parents=True)
    (agents / "my-custom-worker.toml").write_text(
        'name = "subagents_dispatch_worker"\nmodel = "gpt-5.6-terra"\ndeveloper_instructions = "custom"\n'
    )
    result = run_installer(target)
    assert result.returncode != 0
    assert "reserved current role name" in result.stdout + result.stderr


def test_installer_refuses_symlinked_lock(tmp_path):
    target = tmp_path / "codex-home"
    target.mkdir()
    external = tmp_path / "external-lock"
    external.write_bytes(b"\0")
    (target / ".subagents-dispatch-agents.lock").symlink_to(external)
    result = run_installer(target)
    assert result.returncode != 0
    assert "Refusing symlinked installer lock" in result.stdout + result.stderr


def test_installer_is_idempotent_and_check_is_non_mutating(tmp_path):
    target = tmp_path / "codex-home"
    first = run_installer(target)
    assert first.returncode == 0, first.stderr
    before = {path.name: path.read_bytes() for path in target.rglob("*") if path.is_file()}
    check = run_installer(target, "--check")
    second = run_installer(target)
    after = {path.name: path.read_bytes() for path in target.rglob("*") if path.is_file()}
    assert check.returncode == 0, check.stderr
    assert second.returncode == 0, second.stderr
    assert before == after
