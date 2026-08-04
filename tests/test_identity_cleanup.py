from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETIRED_TOKENS = (
    "codex" + "-agent-team",
    "codex" + "_agent_team_",
    "." + "codex" + "-agent-team-",
)


def iter_text_files():
    for root_name in ["plugins", "docs", "evals", "tests", ".agents", ".github"]:
        root = ROOT / root_name
        if root.exists():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".py", ".md", ".json", ".toml", ".yaml", ".yml"}:
                    yield path
    for name in ["README.md", "README_EN.md", "README_AI.md", "HEADOFF.md", "LOCAL_VALIDATION_REPORT.md"]:
        path = ROOT / name
        if path.exists():
            yield path


def test_retired_identity_tokens_are_absent_from_current_tree():
    violations = []
    for path in iter_text_files():
        text = path.read_text(errors="replace")
        matches = [token for token in RETIRED_TOKENS if token in text]
        if matches:
            violations.append((path.relative_to(ROOT).as_posix(), matches))
    assert not violations, f"Retired project identity remains in current tree: {violations}"


def test_current_profile_filenames_and_roles_are_single_generation():
    profile_dir = ROOT / "plugins" / "codex-delegate" / "agent-profiles"
    names = {path.name for path in profile_dir.glob("*.toml")}
    assert names == {
        "codex-delegate-reader.toml",
        "codex-delegate-worker.toml",
        "codex-delegate-investigator.toml",
        "codex-delegate-advisor.toml",
    }
    for path in profile_dir.glob("*.toml"):
        assert 'name = "codex_delegate_' in path.read_text()


def test_only_current_plugin_directory_exists():
    retired_plugin = ROOT / "plugins" / ("codex" + "-agent-team")
    assert not retired_plugin.exists()
    assert (ROOT / "plugins" / "codex-delegate").is_dir()
