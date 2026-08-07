from __future__ import annotations

import hashlib
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
LEGACY_PROFILE = "codex-delegate-reader.toml"
LEGACY_MANIFEST = ".codex-delegate-agents.json"
LEGACY_LOCK = ".codex-delegate-agents.lock"
CURRENT_MANIFEST = ".subagents-dispatch-agents.json"


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


def create_minimal_legacy(home: Path) -> bytes:
    agents = home / "agents"
    agents.mkdir(parents=True, exist_ok=True)
    content = b'name = "codex_delegate_reader"\n'
    (agents / LEGACY_PROFILE).write_bytes(content)
    manifest = {
        "schema_version": 1,
        "managed_by": "codex-delegate",
        "profile_hashes": {LEGACY_PROFILE: hashlib.sha256(content).hexdigest()},
    }
    (home / LEGACY_MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    (home / LEGACY_LOCK).write_bytes(b"\0")
    return content


def wait_for_path(path: Path, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists():
            return
        time.sleep(0.02)
    raise AssertionError(f"Timed out waiting for {path}")


LOCK_HOLDER = r'''
import os
from pathlib import Path
import sys
import time

lock_path = Path(sys.argv[1])
ready_path = Path(sys.argv[2])
release_path = Path(sys.argv[3])
lock_path.parent.mkdir(parents=True, exist_ok=True)
fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
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
ready_path.write_text("ready", encoding="utf-8")
while not release_path.exists():
    time.sleep(0.02)
if os.name == "nt":
    os.lseek(fd, 0, os.SEEK_SET)
    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
else:
    fcntl.flock(fd, fcntl.LOCK_UN)
os.close(fd)
'''


def test_migration_waits_for_real_legacy_os_lock(tmp_path: Path):
    """An old-generation lock holder must serialize the new migrator."""
    home = tmp_path / "codex-home"
    create_minimal_legacy(home)
    ready = tmp_path / "legacy-lock-ready"
    release = tmp_path / "legacy-lock-release"

    holder = subprocess.Popen(
        [sys.executable, "-c", LOCK_HOLDER, str(home / LEGACY_LOCK), str(ready), str(release)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        wait_for_path(ready)
        migrator = subprocess.Popen(
            [sys.executable, str(INSTALLER), "--codex-home", str(home), "--migrate-legacy"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(0.3)
        assert migrator.poll() is None, "migration should wait while the legacy OS lock is held"
        assert (home / LEGACY_MANIFEST).exists(), "migration mutated legacy state before acquiring legacy lock"
        assert not (home / CURRENT_MANIFEST).exists(), "migration installed current state before acquiring legacy lock"

        release.write_text("release", encoding="utf-8")
        holder_stdout, holder_stderr = holder.communicate(timeout=10)
        migrate_stdout, migrate_stderr = migrator.communicate(timeout=30)
        assert holder.returncode == 0, holder_stdout + holder_stderr
        assert migrator.returncode == 0, migrate_stdout + migrate_stderr
        assert (home / LEGACY_LOCK).exists(), "legacy compatibility lock must be preserved"
        assert (home / CURRENT_MANIFEST).exists()
    finally:
        if holder.poll() is None:
            release.write_text("release", encoding="utf-8")
            holder.kill()
            holder.wait(timeout=5)


def test_partial_legacy_cleanup_failure_rolls_back_snapshot(tmp_path: Path):
    """A failure inside legacy cleanup must restore earlier destructive steps."""
    home = tmp_path / "codex-home"
    original_profile = create_minimal_legacy(home)
    original_manifest = (home / LEGACY_MANIFEST).read_bytes()
    installer = load_installer()

    def fail_mid_cleanup(codex_home, backup):
        (codex_home / "agents" / LEGACY_PROFILE).unlink()
        raise RuntimeError("injected partial legacy cleanup failure")

    installer.commit_legacy_cleanup = fail_mid_cleanup
    with pytest.raises(RuntimeError, match="partial legacy cleanup"):
        installer.install(home, False, True)

    assert (home / "agents" / LEGACY_PROFILE).read_bytes() == original_profile
    assert (home / LEGACY_MANIFEST).read_bytes() == original_manifest
    assert not (home / CURRENT_MANIFEST).exists()


def test_failed_installer_cannot_rollback_a_successful_peer(tmp_path: Path):
    """Current-generation lock serializes a faulting installer and a successful peer."""
    if not hasattr(os, "fork"):
        pytest.skip("fault-injection harness requires fork")

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
    peer_was_serialized = peer.poll() is None
    os.write(release_write, b"1")
    _, fault_status = os.waitpid(pid, 0)
    peer_stdout, peer_stderr = peer.communicate(timeout=10)

    assert peer_was_serialized
    assert os.waitstatus_to_exitcode(fault_status) == 23
    assert peer.returncode == 0, peer_stdout + peer_stderr
    check = run_installer(home, "--check")
    assert check.returncode == 0, check.stdout + check.stderr
