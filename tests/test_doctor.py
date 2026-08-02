from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCTOR = ROOT / "scripts" / "doctor.py"
INSTALLER = ROOT / "scripts" / "install.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False
    )


def test_doctor_reports_exact_profile_mode_after_install(tmp_path: Path):
    home = tmp_path / "codex-home"
    install = run(str(INSTALLER), "--codex-home", str(home))
    assert install.returncode == 0, install.stderr

    result = run(str(DOCTOR), "--codex-home", str(home), "--json")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["skill_integrity"] == "exact"
    assert set(payload["profiles"].values()) == {"exact"}
    assert payload["runtime_verifier"] == "available"
    assert payload["live_spawn_surface"] == "requires_in_session_check"
    assert payload["recommended_mode"] == "profile_mode"


def test_doctor_reports_modified_profile_without_mutation(tmp_path: Path):
    home = tmp_path / "codex-home"
    install = run(str(INSTALLER), "--codex-home", str(home))
    assert install.returncode == 0, install.stderr
    profile = home / "agents" / "luna-worker.toml"
    profile.write_text(profile.read_text() + "\n# user change\n")
    before = profile.read_bytes()

    result = run(str(DOCTOR), "--codex-home", str(home), "--json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["profiles"]["luna-worker.toml"] == "different"
    assert payload["recommended_mode"] == "repair_or_portable_mode"
    assert profile.read_bytes() == before


def test_doctor_reports_missing_install(tmp_path: Path):
    home = tmp_path / "missing"
    result = run(str(DOCTOR), "--codex-home", str(home), "--json")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["skill_integrity"] == "missing"
    assert set(payload["profiles"].values()) == {"missing"}
