from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETIRED_TOKENS = (
    "codex" + "-agent-team",
    "codex" + "_agent_team",
    "codex" + " agent team",
)


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        paths.append(ROOT / os.fsdecode(raw))
    return paths


def tracked_bytes(path: Path) -> bytes:
    if path.is_symlink():
        return os.fsencode(os.readlink(path))
    return path.read_bytes()


def test_retired_identity_tokens_are_absent_from_all_tracked_content():
    retired = tuple(token.encode("utf-8") for token in RETIRED_TOKENS)
    violations = []
    for path in tracked_paths():
        data = tracked_bytes(path).lower()
        matches = [token.decode("utf-8") for token in retired if token in data]
        if matches:
            violations.append((path.relative_to(ROOT).as_posix(), matches))
    assert not violations, f"Retired project identity remains in tracked content: {violations}"


def test_retired_identity_tokens_are_absent_from_all_tracked_paths():
    violations = []
    for path in tracked_paths():
        rel = path.relative_to(ROOT).as_posix().lower()
        if any(token in rel for token in RETIRED_TOKENS):
            violations.append(rel)
    assert not violations, f"Retired project identity remains in tracked paths: {violations}"


def test_current_profile_filenames_and_roles_are_single_generation():
    profile_dir = ROOT / "plugins" / "codex-delegate" / "agent-profiles"
    names = {path.name for path in profile_dir.glob("*.toml")}
    assert names == {
        "codex-delegate-reader.toml",
        "codex-delegate-worker.toml",
        "codex-delegate-solver.toml",
        "codex-delegate-investigator.toml",
        "codex-delegate-advisor.toml",
    }
    for path in profile_dir.glob("*.toml"):
        assert 'name = "codex_delegate_' in path.read_text()


def test_current_plugin_directory_exists():
    assert (ROOT / "plugins" / "codex-delegate").is_dir()
