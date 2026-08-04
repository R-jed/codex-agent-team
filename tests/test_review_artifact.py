from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "codex-agent-team" / "scripts" / "review-artifact.py"


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=True,
    )


def init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "codex-delegate@example.invalid")
    git(repo, "config", "user.name", "Codex Delegate Test")
    (repo / ".gitignore").write_text("ignored-cache/\n", encoding="utf-8")
    (repo / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", ".gitignore", "app.py")
    git(repo, "commit", "-m", "base")
    return repo


def artifact(repo: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), *extra],
        text=True,
        capture_output=True,
        check=False,
    )


def artifact_id(repo: Path) -> str:
    result = artifact(repo)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == 1
    assert payload["review_artifact_id"].startswith("sha256:")
    return payload["review_artifact_id"]


def test_review_artifact_is_stable_and_verify_accepts_exact_state(tmp_path: Path):
    repo = init_repo(tmp_path)
    first = artifact_id(repo)
    second = artifact_id(repo)
    assert first == second

    verified = artifact(repo, "--verify", first)
    assert verified.returncode == 0
    assert json.loads(verified.stdout)["review_artifact_id"] == first


def test_tracked_mutation_invalidates_review_artifact(tmp_path: Path):
    repo = init_repo(tmp_path)
    before = artifact_id(repo)

    (repo / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
    after = artifact_id(repo)
    assert after != before

    verified = artifact(repo, "--verify", before)
    assert verified.returncode == 2
    assert "review artifact changed" in verified.stderr


def test_staged_mutation_is_bound_without_requiring_commit(tmp_path: Path):
    repo = init_repo(tmp_path)
    before = artifact_id(repo)

    (repo / "app.py").write_text("VALUE = 3\n", encoding="utf-8")
    git(repo, "add", "app.py")
    after = artifact_id(repo)
    assert after != before


def test_untracked_deliverable_is_bound_and_content_changes_invalidate(tmp_path: Path):
    repo = init_repo(tmp_path)
    clean = artifact_id(repo)

    untracked = repo / "new_module.py"
    untracked.write_text("FLAG = 'a'\n", encoding="utf-8")
    first = artifact_id(repo)
    assert first != clean

    untracked.write_text("FLAG = 'b'\n", encoding="utf-8")
    second = artifact_id(repo)
    assert second != first

    payload = json.loads(artifact(repo).stdout)
    assert payload["untracked"][0]["path"] == "new_module.py"
    assert payload["untracked"][0]["kind"] == "file"


def test_ignored_cache_artifacts_do_not_change_source_deliverable_identity(tmp_path: Path):
    repo = init_repo(tmp_path)
    before = artifact_id(repo)

    cache = repo / "ignored-cache"
    cache.mkdir()
    (cache / "result.bin").write_bytes(b"not a source deliverable")
    after = artifact_id(repo)
    assert after == before


def test_head_change_invalidates_artifact_even_with_clean_worktree(tmp_path: Path):
    repo = init_repo(tmp_path)
    before = artifact_id(repo)

    (repo / "app.py").write_text("VALUE = 4\n", encoding="utf-8")
    git(repo, "add", "app.py")
    git(repo, "commit", "-m", "change head")
    after = artifact_id(repo)
    assert after != before
