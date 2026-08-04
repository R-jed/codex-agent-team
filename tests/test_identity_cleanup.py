from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_PUBLIC = "codex-agent-team"
LEGACY_INTERNAL_TOKENS = ("codex_agent_team_", "codex-agent-team-", ".codex-agent-team-")
ALLOWED_MIGRATION_SURFACES = {
    "plugins/codex-delegate/scripts/install-agents.py",
    "docs/plugin-installation.md",
    "README.md",
    "README_EN.md",
    "README_AI.md",
    "HEADOFF.md",
    "LOCAL_VALIDATION_REPORT.md",
    "tests/test_install_agents.py",
    "tests/test_installer_safety.py",
    "tests/test_plugin_packaging.py",
    "tests/test_readme_user_facing.py",
    "tests/test_policy.py",
    "tests/test_runtime_truth_policy.py",
    "tests/test_headoff.py",
    "tests/test_identity_cleanup.py",
}


def iter_text_files():
    for root_name in ["plugins", "docs", "evals", "tests"]:
        root = ROOT / root_name
        if root.exists():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".py", ".md", ".json", ".toml", ".yaml", ".yml"}:
                    yield path
    for name in ["README.md", "README_EN.md", "README_AI.md", "HEADOFF.md", "LOCAL_VALIDATION_REPORT.md"]:
        yield ROOT / name


def test_legacy_identity_is_confined_to_one_way_migration_surfaces():
    violations = []
    for path in iter_text_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(errors="replace")
        has_legacy = LEGACY_PUBLIC in text or any(token in text for token in LEGACY_INTERNAL_TOKENS)
        if has_legacy and rel not in ALLOWED_MIGRATION_SURFACES:
            violations.append(rel)
    assert not violations, f"Legacy identity escaped migration boundary: {violations}"


def test_current_runtime_surfaces_have_no_legacy_identity():
    current_surfaces = [
        ROOT / "plugins" / "codex-delegate" / "policy-contract.json",
        ROOT / "plugins" / "codex-delegate" / "agent-profiles",
        ROOT / "plugins" / "codex-delegate" / "skills" / "codex-delegate" / "SKILL.md",
        ROOT / "plugins" / "codex-delegate" / "skills" / "codex-delegate" / "references" / "routing-policy.md",
        ROOT / "plugins" / "codex-delegate" / "skills" / "codex-delegate" / "references" / "runtime-assurance.md",
        ROOT / "plugins" / "codex-delegate" / "skills" / "codex-delegate" / "references" / "final-review-gate.md",
        ROOT / "evals" / "routing-cases.json",
        ROOT / "evals" / "routing-case.schema.json",
    ]
    for surface in current_surfaces:
        paths = list(surface.rglob("*")) if surface.is_dir() else [surface]
        for path in paths:
            if path.is_file():
                text = path.read_text(errors="replace")
                assert LEGACY_PUBLIC not in text, path
                assert not any(token in text for token in LEGACY_INTERNAL_TOKENS), path


def test_current_profile_filenames_and_roles_are_single_generation():
    profile_dir = ROOT / "plugins" / "codex-delegate" / "agent-profiles"
    names = {path.name for path in profile_dir.glob("*.toml")}
    assert names == {"codex-delegate-reader.toml", "codex-delegate-worker.toml", "codex-delegate-investigator.toml", "codex-delegate-advisor.toml"}
    for path in profile_dir.glob("*.toml"):
        assert 'name = "codex_delegate_' in path.read_text()
