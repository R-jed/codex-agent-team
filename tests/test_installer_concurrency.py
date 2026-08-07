from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-agents.py"
LEGACY_LOCK = ".codex-delegate-agents.lock"
CURRENT_LOCK = ".subagents-dispatch-agents.lock"


def load_installer():
    scripts_dir = str(INSTALLER.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("subagents_dispatch_installer", INSTALLER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_installer(home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(home), *extra],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def create_minimal_legacy_state(home: Path) -> None:
    home.mkdir(parents=True, exist_ok=True)
    (home / ".codex-delegate-agents.json").write_text(
        json.dumps({"schema_version": 1, "managed_by": "codex-delegate", "profile_hashes": {}}),
        encoding="utf-8",
    )
    (home / LEGACY_LOCK).write_bytes(b"\0")


def start_real_lock_holder(lock_path: Path) -> subprocess.Popen[str]:
    code = r'''
import os
from pathlib import Path
import sys
path = Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)
fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
if os.fstat(fd).st_size == 0:
    os.write(fd, b"\0")
    os.fsync(fd)
if os.name == "nt":
    import msvcrt
    os.lseek(fd, 0, os.SEEK_SET)
    msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
else:
    import fcntl
    fcntl.flock(fd, fcntl.LOCK_EX)
print("LOCKED", flush=True)
sys.stdin.readline()
if os.name == "nt":
    os.lseek(fd, 0, os.SEEK_SET)
    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
else:
    fcntl.flock(fd, fcntl.LOCK_UN)
os.close(fd)
'''
    proc = subprocess.Popen(
        [sys.executable, "-c", code, str(lock_path)],
        cwd=ROOT,
        text=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdout is not None
    assert proc.stdout.readline().strip() == "LOCKED"
    return proc


def test_real_legacy_lock_holder_blocks_new_migrator(tmp_path: Path):
    """Old-generation lock ownership must serialize the new migrator."""
    home = tmp_path / "codex-home"
    create_minimal_legacy_state(home)
    holder = start_real_lock_holder(home / LEGACY_LOCK)
    migrator = subprocess.Popen(
        [sys.executable, str(INSTALLER), "--codex-home", str(home), "--migrate-legacy"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        time.sleep(0.4)
        assert migrator.poll() is None, "migrator bypassed the held legacy OS lock"
        assert holder.stdin is not None
        holder.stdin.write("release\n")
        holder.stdin.flush()
        holder_out, holder_err = holder.communicate(timeout=10)
        assert holder.returncode == 0, holder_out + holder_err
        out, err = migrator.communicate(timeout=30)
        assert migrator.returncode == 0, out + err
    finally:
        if holder.poll() is None:
            holder.kill()
        if migrator.poll() is None:
            migrator.kill()


def test_both_generation_lock_files_remain_after_migration(tmp_path: Path):
    home = tmp_path / "codex-home"
    create_minimal_legacy_state(home)
    result = run_installer(home, "--migrate-legacy")
    assert result.returncode == 0, result.stdout + result.stderr
    assert (home / LEGACY_LOCK).exists()
    assert (home / CURRENT_LOCK).exists()
    check = run_installer(home, "--check")
    assert check.returncode == 0, check.stdout + check.stderr


@pytest.mark.skipif(not hasattr(os, "fork"), reason="fault-injection harness requires fork")
def test_failed_installer_cannot_rollback_a_successful_peer(tmp_path: Path):
    home = tmp_path / "codex-home"
    installer = load_installer()
    ready_read, ready_write = os.pipe()
    release_read, release_write = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(ready_read)
        os.close(release_write)
        def fail_after_profile_mutation(path, payload):
            os.write(ready_write, b"1")
            os.read(release_read, 1)
            raise RuntimeError("injected failure after profile mutation")
        installer.write_manifest = fail_after_profile_mutation
        try:
            installer.install(home, False)
        except RuntimeError:
            os._exit(23)
        os._exit(24)

    os.close(ready_write)
    os.close(release_read)
    os.read(ready_read, 1)
    peer = subprocess.Popen(
        [sys.executable, str(INSTALLER), "--codex-home", str(home)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(0.2)
    assert peer.poll() is None
    os.write(release_write, b"1")
    _, fault_status = os.waitpid(pid, 0)
    peer_stdout, peer_stderr = peer.communicate(timeout=10)
    assert os.waitstatus_to_exitcode(fault_status) == 23
    assert peer.returncode == 0, peer_stdout + peer_stderr
    check = run_installer(home, "--check")
    assert check.returncode == 0, check.stdout + check.stderr
