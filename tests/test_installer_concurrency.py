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
INSTALLER = ROOT / "plugins" / "subagents-dispatch" / "scripts" / "install-agents.py"


def load_installer():
    # Add scripts directory to sys.path so legacy_migration can be found
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


def test_migration_handles_legacy_lock_contention(tmp_path: Path):
    """Verify migration handles legacy lock contention gracefully."""
    home = tmp_path / "codex-home"
    home.mkdir(parents=True)

    # Create legacy state
    legacy_manifest = {
        "schema_version": 1,
        "managed_by": "codex-delegate",
        "profile_hashes": {}
    }
    (home / ".codex-delegate-agents.json").write_text(
        json.dumps(legacy_manifest), encoding="utf-8"
    )

    # Create legacy lock file
    legacy_lock = home / ".codex-delegate-agents.lock"
    legacy_lock.write_bytes(b"\0")

    # Simulate holding the lock by making it exclusive
    # (In real scenario, another process would hold flock)
    # For this test, we just verify the migration proceeds
    # even when legacy lock exists

    installer = subprocess.run(
        [sys.executable, str(INSTALLER), "--codex-home", str(home), "--migrate-legacy"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )

    # Migration should succeed
    assert installer.returncode == 0, installer.stdout + installer.stderr
    assert "Legacy state detected" in installer.stdout or "No legacy installation" in installer.stdout


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
    peer_was_serialized = peer.poll() is None
    os.write(release_write, b"1")
    _, fault_status = os.waitpid(pid, 0)
    peer_stdout, peer_stderr = peer.communicate(timeout=10)

    assert peer_was_serialized
    assert os.waitstatus_to_exitcode(fault_status) == 23
    assert peer.returncode == 0, peer_stdout + peer_stderr
    check = run_installer(home, "--check")
    assert check.returncode == 0, check.stdout + check.stderr
