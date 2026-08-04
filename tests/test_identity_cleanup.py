from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETIRED_TOKENS = (
    "codex" + "-agent-team",
    "codex" + "_agent_team",
    "codex" + " agent team",
)
SCAN_ROOTS = ("plugins", "docs", "evals", "tests", ".agents", ".github")
ROOT_FILES = ("README.md", "README_EN.md", "README_AI.md", "HEADOFF.md", "LOCAL_VALIDATION_REPORT.md")


def iter_text_files():
    for root_name in SCAN_ROOTS:
        root = ROOT / root_name
        if root.exists():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".py", ".md", ".json", ".toml", ".yaml", ".yml"}:
                    yield path
    for name in ROOT_FILES:
        path = ROOT / name
        if path.exists():
            yield path


def iter_project_paths():
    for root_name in SCAN_ROOTS:
        root = ROOT / root_name
        if root.exists():
            yield root
            yield from root.rglob("*")
    for name in ROOT_FILES:
        path = ROOT / name
        if path.exists():
            yield path


def test_retired_identity_tokens_are_absent_from_current_tree_content():
    violations = []
    for path in iter_text_files():
        text = path.read_text(errors="replace").lower()
        matches = [token for token in RETIRED_TOKENS if token in text]
        if matches:
            violations.append((path.relative_to(ROOT).as_posix(), matches))
    assert not violations, f"Retired project identity remains in current tree content: {violations}"


def test_retired_identity_tokens_are_absent_from_current_tree_paths():
    violations = []
    for path in iter_project_paths():
        rel = path.relative_to(ROOT).as_posix().lower()
        if any(token in rel for token in RETIRED_TOKENS):
            violations.append(rel)
    assert not violations, f"Retired project identity remains in current tree paths: {violations}"


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
