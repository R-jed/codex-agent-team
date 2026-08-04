from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "codex-delegate" / "scripts" / "review-artifact.py"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def artifact_id(repo: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["review_artifact_id"]


def test_unborn_staged_file_then_unstaged_edit_changes_artifact(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")

    tracked = repo / "tracked.txt"
    tracked.write_text("staged-version\n", encoding="utf-8")
    git(repo, "add", "tracked.txt")
    staged_id = artifact_id(repo)

    tracked.write_text("working-tree-version\n", encoding="utf-8")
    working_id = artifact_id(repo)

    assert working_id != staged_id
