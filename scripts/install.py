#!/usr/bin/env python3
"""Install Codex Agent Team and its locked Agent profiles safely.

The installer validates shipped sources and destination conflicts before mutation.
It records hashes of package-managed artifacts so future releases can upgrade files
that are still unchanged from the previous managed install while refusing to overwrite
user modifications. `--check` is strictly non-mutating.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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
MANIFEST_NAME = ".codex-agent-team-install.json"
MANIFEST_SCHEMA = 1


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
        help="Verify installed package-managed artifacts exactly; make no changes.",
    )
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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
        actual = (
            str(data.get("name", "")).strip(),
            str(data.get("model", "")).strip(),
            str(data.get("model_reasoning_effort", "")).strip(),
        )
        if actual != expected:
            fail(f"Agent profile {filename} pins {actual!r}; expected {expected!r}")
        if not str(data.get("description", "")).strip():
            fail(f"Agent profile has no description: {filename}")
        if not str(data.get("developer_instructions", "")).strip():
            fail(f"Agent profile has no developer_instructions: {filename}")
        if expected[0] in seen_names:
            fail(f"Duplicate shipped Agent role name: {expected[0]}")
        seen_names.add(expected[0])


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
        snapshot[path.relative_to(root).as_posix()] = file_hash(path)
    return snapshot


def tree_hash(root: Path) -> str:
    encoded = json.dumps(tree_snapshot(root), sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(encoded)


def skill_is_exact(target_skill: Path) -> bool:
    return tree_snapshot(SKILL_SOURCE) == tree_snapshot(target_skill)


def desired_manifest(skill_only: bool) -> dict:
    return {
        "schema_version": MANIFEST_SCHEMA,
        "mode": "skill_only" if skill_only else "profile",
        "skill_hash": tree_hash(SKILL_SOURCE),
        "profile_hashes": (
            {}
            if skill_only
            else {filename: file_hash(PROFILE_SOURCE / filename) for filename in PROFILE_FILES}
        ),
    }


def load_manifest(path: Path) -> dict | None:
    if path.is_symlink():
        fail(f"Refusing symlinked install manifest: {path}")
    if not path.exists():
        return None
    if not path.is_file():
        fail(f"Install manifest is not a regular file: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"Invalid install manifest {path}: {exc}")
    if not isinstance(data, dict) or data.get("schema_version") != MANIFEST_SCHEMA:
        fail(f"Unsupported install manifest: {path}")
    if not isinstance(data.get("profile_hashes", {}), dict):
        fail(f"Invalid profile hashes in install manifest: {path}")
    return data


def preflight_parent(path: Path) -> None:
    if path.is_symlink():
        fail(f"Refusing symlinked destination directory: {path}")
    if path.exists() and not path.is_dir():
        fail(f"Destination parent is not a directory: {path}")


def preflight_skill(
    target_skill: Path, *, check_only: bool, manifest: dict | None
) -> bool:
    """Return True when an existing differing Skill is a safe managed/legacy upgrade."""
    if target_skill.is_symlink():
        fail(f"Refusing symlinked installed Skill: {target_skill}")
    if not target_skill.exists():
        return False
    if not target_skill.is_dir():
        fail(f"Installed Skill path is not a directory: {target_skill}")
    if skill_is_exact(target_skill):
        return False
    if check_only:
        fail(f"Installed Skill does not exactly match shipped source: {target_skill}")

    actual_hash = tree_hash(target_skill)
    if manifest is None:
        # One-time migration path from installer versions that predate the manifest.
        return True
    previous_managed_hash = manifest.get("skill_hash")
    if previous_managed_hash == actual_hash:
        return True
    fail(
        "Refusing to overwrite an installed Skill that differs from the current package "
        f"and is not proven unchanged from the previous managed install: {target_skill}"
    )


def preflight_profiles(
    agents_dir: Path, *, check_only: bool, manifest: dict | None
) -> set[str]:
    desired_by_name = {
        EXPECTED_PROFILES[filename][0]: PROFILE_SOURCE / filename
        for filename in PROFILE_FILES
    }
    managed_upgrades: set[str] = set()

    if not agents_dir.exists():
        if check_only:
            fail(f"Required agents directory is missing: {agents_dir}")
        return managed_upgrades

    old_hashes = (manifest or {}).get("profile_hashes", {})
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.is_symlink():
            fail(f"Refusing symlinked Agent profile destination: {target}")
        if target.exists():
            if not target.is_file():
                fail(f"Agent profile destination is not a regular file: {target}")
            if target.read_bytes() != source.read_bytes():
                actual_hash = file_hash(target)
                previous_managed_hash = old_hashes.get(filename)
                if not check_only and previous_managed_hash == actual_hash:
                    managed_upgrades.add(filename)
                else:
                    fail(
                        "Refusing to overwrite an Agent profile that differs from the current "
                        f"package and is not proven unchanged from the previous managed install: {target}"
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
        if existing_name in desired_by_name:
            fail(
                "Refusing to install because another Agent file uses the reserved role name "
                f"{existing_name!r}: {existing}"
            )
    return managed_upgrades


def verify_installed(
    target_skill: Path, agents_dir: Path, manifest_path: Path, skill_only: bool
) -> None:
    if not target_skill.exists():
        fail(f"Installed Skill is missing: {target_skill}")
    if not skill_is_exact(target_skill):
        fail(f"Installed Skill does not exactly match shipped source: {target_skill}")

    if not skill_only:
        for filename in PROFILE_FILES:
            source = PROFILE_SOURCE / filename
            target = agents_dir / filename
            if target.is_symlink() or not target.is_file():
                fail(f"Installed Agent profile is missing or unsafe: {target}")
            if target.read_bytes() != source.read_bytes():
                fail(f"Installed Agent profile differs from shipped template: {target}")

    manifest = load_manifest(manifest_path)
    if manifest is None:
        fail(f"Managed install manifest is missing: {manifest_path}")
    if manifest != desired_manifest(skill_only):
        fail(f"Managed install manifest does not match installed artifacts: {manifest_path}")


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


def stage_file(directory: Path, data: bytes, prefix: str) -> Path:
    fd, staged_name = tempfile.mkstemp(prefix=prefix, dir=directory)
    staged = Path(staged_name)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    return staged


def install_profiles(
    agents_dir: Path, managed_upgrades: set[str]
) -> tuple[list[Path], dict[Path, Path]]:
    created: list[Path] = []
    backups: dict[Path, Path] = {}
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        destination = agents_dir / filename
        if destination.exists() and filename not in managed_upgrades:
            continue
        staged = stage_file(agents_dir, source.read_bytes(), ".codex-agent-profile-")
        try:
            if destination.exists():
                backup = agents_dir / f".{filename}.backup-{uuid.uuid4().hex}"
                destination.rename(backup)
                backups[destination] = backup
            staged.rename(destination)
            if destination not in backups:
                created.append(destination)
        except BaseException:
            staged.unlink(missing_ok=True)
            raise
    return created, backups


def rollback_profiles(created: list[Path], backups: dict[Path, Path]) -> list[str]:
    errors: list[str] = []
    for path in reversed(created):
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            errors.append(f"could not remove created profile {path}: {exc}")
    for destination, backup in reversed(list(backups.items())):
        try:
            destination.unlink(missing_ok=True)
            backup.rename(destination)
        except OSError as exc:
            errors.append(f"could not restore profile {destination}: {exc}")
    return errors


def discard_profile_backups(backups: dict[Path, Path]) -> None:
    for backup in backups.values():
        backup.unlink(missing_ok=True)


def write_bytes_atomically(path: Path, data: bytes, prefix: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = stage_file(path.parent, data, prefix)
    try:
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def write_manifest(path: Path, payload: dict) -> None:
    write_bytes_atomically(
        path,
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode(),
        ".codex-agent-team-manifest-",
    )


def restore_manifest(path: Path, previous: bytes | None) -> list[str]:
    try:
        if previous is None:
            path.unlink(missing_ok=True)
        else:
            write_bytes_atomically(path, previous, ".codex-agent-team-manifest-restore-")
    except OSError as exc:
        return [f"could not restore install manifest {path}: {exc}"]
    return []


def install(codex_home: Path, skill_only: bool, check_only: bool) -> None:
    codex_home = codex_home.expanduser().resolve()
    skills_dir = codex_home / "skills"
    agents_dir = codex_home / "agents"
    target_skill = skills_dir / "codex-agent-team"
    manifest_path = codex_home / MANIFEST_NAME

    validate_sources()
    manifest = load_manifest(manifest_path)
    previous_manifest_bytes = manifest_path.read_bytes() if manifest_path.is_file() else None
    preflight_parent(skills_dir)
    if not skill_only:
        preflight_parent(agents_dir)
    preflight_skill(target_skill, check_only=check_only, manifest=manifest)
    managed_upgrades: set[str] = set()
    if not skill_only:
        managed_upgrades = preflight_profiles(
            agents_dir, check_only=check_only, manifest=manifest
        )

    if check_only:
        if not skills_dir.is_dir():
            fail(f"Required skills directory is missing: {skills_dir}")
        verify_installed(target_skill, agents_dir, manifest_path, skill_only)
        print("CHECK PASSED: installed Codex Agent Team matches managed artifacts exactly.")
        return

    skill_already_exact = target_skill.exists() and skill_is_exact(target_skill)
    manifest_already_exact = manifest == desired_manifest(skill_only)
    profiles_already_exact = skill_only or all(
        (agents_dir / filename).is_file()
        and not (agents_dir / filename).is_symlink()
        and (agents_dir / filename).read_bytes() == (PROFILE_SOURCE / filename).read_bytes()
        for filename in PROFILE_FILES
    )
    if skill_already_exact and profiles_already_exact and manifest_already_exact:
        print("Already installed exactly; no changes made.")
        return

    codex_home.mkdir(parents=True, exist_ok=True)
    skills_dir.mkdir(parents=True, exist_ok=True)
    if not skill_only:
        agents_dir.mkdir(parents=True, exist_ok=True)

    stage_root: Path | None = None
    staged_skill: Path | None = None
    if not skill_already_exact:
        stage_root, staged_skill = stage_skill(skills_dir)

    created_profiles: list[Path] = []
    profile_backups: dict[Path, Path] = {}
    skill_backup: Path | None = None
    installed_new_skill = not target_skill.exists()

    try:
        if not skill_only:
            created_profiles, profile_backups = install_profiles(agents_dir, managed_upgrades)

        if not skill_already_exact:
            assert staged_skill is not None
            if target_skill.exists():
                skill_backup = skills_dir / f".codex-agent-team-backup-{uuid.uuid4().hex}"
                target_skill.rename(skill_backup)
            staged_skill.rename(target_skill)

        if not skill_is_exact(target_skill):
            fail("Installed Skill failed exactness verification")
        if not skill_only:
            for filename in PROFILE_FILES:
                if (agents_dir / filename).read_bytes() != (PROFILE_SOURCE / filename).read_bytes():
                    fail(f"Installed profile failed exactness verification: {filename}")

        write_manifest(manifest_path, desired_manifest(skill_only))
        verify_installed(target_skill, agents_dir, manifest_path, skill_only)
    except BaseException as exc:
        rollback_errors = rollback_profiles(created_profiles, profile_backups)
        if skill_backup is not None and skill_backup.exists():
            try:
                shutil.rmtree(target_skill, ignore_errors=True)
                skill_backup.rename(target_skill)
            except OSError as rollback_exc:
                rollback_errors.append(f"could not restore Skill: {rollback_exc}")
        elif installed_new_skill:
            try:
                shutil.rmtree(target_skill, ignore_errors=True)
            except OSError as rollback_exc:
                rollback_errors.append(f"could not remove new Skill: {rollback_exc}")
        rollback_errors.extend(restore_manifest(manifest_path, previous_manifest_bytes))
        if rollback_errors:
            fail(
                f"INSTALL FAILED: {exc}\nROLLBACK INCOMPLETE:\n- "
                + "\n- ".join(rollback_errors)
            )
        raise
    else:
        discard_profile_backups(profile_backups)
        if skill_backup is not None:
            shutil.rmtree(skill_backup, ignore_errors=True)
    finally:
        if stage_root is not None:
            shutil.rmtree(stage_root, ignore_errors=True)

    print(f"Installed Skill: {target_skill}")
    print(f"Managed manifest: {manifest_path}")
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
