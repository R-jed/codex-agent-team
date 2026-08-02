#!/usr/bin/env python3
"""Install Codex Agent Team and its locked Agent profiles.

The installer validates all shipped sources and destination conflicts before mutation.
A normal install stages the Skill when an update is needed, creates only missing exact
Agent profiles, swaps the Skill within the destination filesystem, and verifies the
final state. An already exact install is a no-op. `--check` is strictly non-mutating.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import tomllib
from typing import NoReturn
import uuid

ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / "skill" / "codex-agent-team"
PROFILE_SOURCE = ROOT / "examples" / "agents"
PROFILE_FILES = (
    "luna-explorer.toml",
    "luna-worker.toml",
    "terra-reviewer.toml",
    "sol-judge.toml",
)
EXPECTED_PROFILES = {
    "luna-explorer.toml": ("luna_explorer", "gpt-5.6-luna", "max"),
    "luna-worker.toml": ("luna_worker", "gpt-5.6-luna", "max"),
    "terra-reviewer.toml": ("terra_reviewer", "gpt-5.6-terra", "xhigh"),
    "sol-judge.toml": ("sol_judge", "gpt-5.6-sol", "high"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Codex Agent Team into a Codex home directory."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex home directory (default: $CODEX_HOME or ~/.codex).",
    )
    parser.add_argument(
        "--skill-only",
        action="store_true",
        help="Install only the Skill. Exact profile_locked routes will not be available.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the installed Skill and requested profiles exactly; make no changes.",
    )
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def validate_source_tree(root: Path) -> None:
    if root.is_symlink() or not root.is_dir():
        fail(f"Skill source must be a real directory: {root}")
    for path in root.rglob("*"):
        if path.is_symlink():
            fail(f"Refusing symlink in shipped Skill source: {path}")
        if not path.is_file() and not path.is_dir():
            fail(f"Refusing unsupported entry in shipped Skill source: {path}")


def profile_data(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        fail(f"Agent profile must be a regular non-symlink file: {path}")
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        fail(f"Invalid Agent profile {path}: {exc}")


def validate_sources() -> None:
    validate_source_tree(SKILL_SOURCE)
    seen_names: set[str] = set()
    for filename, expected in EXPECTED_PROFILES.items():
        data = profile_data(PROFILE_SOURCE / filename)
        name, model, effort = expected
        actual = (
            str(data.get("name", "")).strip(),
            str(data.get("model", "")).strip(),
            str(data.get("model_reasoning_effort", "")).strip(),
        )
        if actual != expected:
            fail(
                f"Agent profile {filename} pins {actual!r}; expected {(name, model, effort)!r}"
            )
        if not str(data.get("description", "")).strip():
            fail(f"Agent profile has no description: {filename}")
        if not str(data.get("developer_instructions", "")).strip():
            fail(f"Agent profile has no developer_instructions: {filename}")
        if name in seen_names:
            fail(f"Duplicate shipped Agent role name: {name}")
        seen_names.add(name)


def tree_snapshot(root: Path) -> dict[str, str]:
    if root.is_symlink() or not root.is_dir():
        fail(f"Expected a real Skill directory: {root}")
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            fail(f"Refusing symlink in Skill tree: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            fail(f"Refusing unsupported Skill tree entry: {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        snapshot[path.relative_to(root).as_posix()] = digest
    return snapshot


def skill_is_exact(target_skill: Path) -> bool:
    return tree_snapshot(SKILL_SOURCE) == tree_snapshot(target_skill)


def preflight_parent(path: Path) -> None:
    if path.is_symlink():
        fail(f"Refusing symlinked destination directory: {path}")
    if path.exists() and not path.is_dir():
        fail(f"Destination parent is not a directory: {path}")


def preflight_skill(target_skill: Path) -> None:
    if target_skill.is_symlink():
        fail(f"Refusing symlinked installed Skill: {target_skill}")
    if target_skill.exists() and not target_skill.is_dir():
        fail(f"Installed Skill path is not a directory: {target_skill}")


def preflight_profiles(agents_dir: Path, *, check_only: bool) -> None:
    desired_by_name = {
        EXPECTED_PROFILES[filename][0]: PROFILE_SOURCE / filename
        for filename in PROFILE_FILES
    }
    desired_targets = {
        name: agents_dir / source.name for name, source in desired_by_name.items()
    }

    if not agents_dir.exists():
        if check_only:
            fail(f"Required agents directory is missing: {agents_dir}")
        return

    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.is_symlink():
            fail(f"Refusing symlinked Agent profile destination: {target}")
        if target.exists():
            if not target.is_file():
                fail(f"Agent profile destination is not a regular file: {target}")
            if target.read_bytes() != source.read_bytes():
                fail(
                    "Refusing to overwrite an existing Agent profile with different content: "
                    f"{target}"
                )
        elif check_only:
            fail(f"Required installed Agent profile is missing: {target}")

    for existing in agents_dir.glob("*.toml"):
        if existing.name in PROFILE_FILES or existing.is_symlink() or not existing.is_file():
            continue
        try:
            data = tomllib.loads(existing.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            continue
        existing_name = str(data.get("name", "")).strip()
        if existing_name not in desired_by_name:
            continue
        expected_target = desired_targets[existing_name]
        fail(
            "Refusing to install because another Agent file uses the reserved role name "
            f"{existing_name!r}; expected only {expected_target}, found {existing}"
        )


def verify_installed(target_skill: Path, agents_dir: Path, skill_only: bool) -> None:
    if not target_skill.exists():
        fail(f"Installed Skill is missing: {target_skill}")
    if not skill_is_exact(target_skill):
        fail(f"Installed Skill does not exactly match shipped source: {target_skill}")

    if skill_only:
        return
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.is_symlink() or not target.is_file():
            fail(f"Installed Agent profile is missing or unsafe: {target}")
        if target.read_bytes() != source.read_bytes():
            fail(f"Installed Agent profile differs from shipped template: {target}")


def stage_skill(skills_dir: Path) -> tuple[Path, Path]:
    stage_root = Path(tempfile.mkdtemp(prefix=".codex-agent-team-stage-", dir=skills_dir))
    staged_skill = stage_root / "codex-agent-team"
    try:
        shutil.copytree(SKILL_SOURCE, staged_skill)
        if not skill_is_exact(staged_skill):
            fail("Staged Skill failed exactness verification")
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return stage_root, staged_skill


def install_missing_profiles(agents_dir: Path) -> list[Path]:
    created: list[Path] = []
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        destination = agents_dir / filename
        if destination.exists():
            continue

        fd, staged_name = tempfile.mkstemp(prefix=".codex-agent-profile-", dir=agents_dir)
        staged = Path(staged_name)
        try:
            with os.fdopen(fd, "wb") as handle:
                data = source.read_bytes()
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(staged, destination)
            except FileExistsError:
                if destination.is_symlink() or not destination.is_file():
                    fail(f"Agent profile destination changed during install: {destination}")
                if destination.read_bytes() != source.read_bytes():
                    fail(f"Agent profile destination changed during install: {destination}")
            else:
                created.append(destination)
        finally:
            staged.unlink(missing_ok=True)
    return created


def rollback_profiles(created: list[Path]) -> None:
    for path in reversed(created):
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


def install(codex_home: Path, skill_only: bool, check_only: bool) -> None:
    codex_home = codex_home.expanduser().resolve()
    skills_dir = codex_home / "skills"
    agents_dir = codex_home / "agents"
    target_skill = skills_dir / "codex-agent-team"

    validate_sources()
    preflight_parent(skills_dir)
    if not skill_only:
        preflight_parent(agents_dir)
    preflight_skill(target_skill)
    if not skill_only:
        preflight_profiles(agents_dir, check_only=check_only)

    if check_only:
        if not skills_dir.is_dir():
            fail(f"Required skills directory is missing: {skills_dir}")
        verify_installed(target_skill, agents_dir, skill_only)
        print("CHECK PASSED: installed Codex Agent Team matches shipped artifacts exactly.")
        return

    skill_already_exact = target_skill.exists() and skill_is_exact(target_skill)

    codex_home.mkdir(parents=True, exist_ok=True)
    skills_dir.mkdir(parents=True, exist_ok=True)
    if not skill_only:
        agents_dir.mkdir(parents=True, exist_ok=True)

    stage_root: Path | None = None
    staged_skill: Path | None = None
    if not skill_already_exact:
        stage_root, staged_skill = stage_skill(skills_dir)

    created_profiles: list[Path] = []
    backup: Path | None = None
    installed_new_skill = not target_skill.exists()

    try:
        if not skill_only:
            created_profiles = install_missing_profiles(agents_dir)

        if not skill_already_exact:
            assert staged_skill is not None
            if target_skill.exists():
                backup = skills_dir / f".codex-agent-team-backup-{uuid.uuid4().hex}"
                target_skill.rename(backup)
            try:
                staged_skill.rename(target_skill)
            except BaseException:
                if backup is not None and backup.exists() and not target_skill.exists():
                    backup.rename(target_skill)
                raise

        verify_installed(target_skill, agents_dir, skill_only)
    except BaseException:
        rollback_profiles(created_profiles)
        if backup is not None and backup.exists():
            shutil.rmtree(target_skill, ignore_errors=True)
            try:
                backup.rename(target_skill)
            except OSError:
                pass
        elif installed_new_skill:
            shutil.rmtree(target_skill, ignore_errors=True)
        raise
    else:
        if backup is not None:
            shutil.rmtree(backup, ignore_errors=True)
    finally:
        if stage_root is not None:
            shutil.rmtree(stage_root, ignore_errors=True)

    print(f"Installed Skill: {target_skill}")
    if skill_only:
        print("Skipped Agent profiles (--skill-only).")
        print("Portable Mode will require live spawn_agent model/effort overrides.")
        return

    for filename in PROFILE_FILES:
        print(f"Verified Agent profile: {agents_dir / filename}")
    print("Installed exact route profiles: luna_explorer, luna_worker, terra_reviewer, sol_judge")
    print("Restart or reopen Codex so newly installed Agent profiles are discovered.")


def main() -> None:
    args = parse_args()
    install(args.codex_home, args.skill_only, args.check)


if __name__ == "__main__":
    main()
