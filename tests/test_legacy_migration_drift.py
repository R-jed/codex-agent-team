from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-agents.py"
LEGACY_MANIFEST = ".codex-delegate-agents.json"
LEGACY_PROFILES = (
    "codex-delegate-reader.toml",
    "codex-delegate-worker.toml",
)


def load_installer():
    scripts_dir = str(INSTALLER.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("subagents_dispatch_installer_drift", INSTALLER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_snapshot_drift_aborts_and_does_not_overwrite_external_change(tmp_path: Path):
    home = tmp_path / "codex-home"
    agents = home / "agents"
    agents.mkdir(parents=True)

    original = {
        LEGACY_PROFILES[0]: b'name = "codex_delegate_reader"\n',
        LEGACY_PROFILES[1]: b'name = "codex_delegate_worker"\n',
    }
    for filename, data in original.items():
        (agents / filename).write_bytes(data)
    manifest = {
        "schema_version": 1,
        "managed_by": "codex-delegate",
        "profile_hashes": {
            filename: hashlib.sha256(data).hexdigest()
            for filename, data in original.items()
        },
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
    (home / LEGACY_MANIFEST).write_bytes(manifest_bytes)

    installer = load_installer()
    real_backup = installer.backup_legacy_files
    externally_changed = original[LEGACY_PROFILES[1]] + b"# external edit after snapshot\n"

    def backup_then_drift(codex_home):
        backup, warnings = real_backup(codex_home)
        (codex_home / "agents" / LEGACY_PROFILES[1]).write_bytes(externally_changed)
        return backup, warnings

    installer.backup_legacy_files = backup_then_drift

    with pytest.raises(SystemExit, match="ROLLBACK INCOMPLETE"):
        installer.install(home, False, True)

    # The first owned profile may have been removed before drift was detected, but
    # transaction rollback must restore it. The externally changed file must remain
    # exactly as changed and must never be overwritten from the snapshot.
    assert (agents / LEGACY_PROFILES[0]).read_bytes() == original[LEGACY_PROFILES[0]]
    assert (agents / LEGACY_PROFILES[1]).read_bytes() == externally_changed
    assert (home / LEGACY_MANIFEST).read_bytes() == manifest_bytes
    assert not (home / ".subagents-dispatch-agents.json").exists()
