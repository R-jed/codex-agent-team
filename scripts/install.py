#!/usr/bin/env python3
"""Install the canonical Codex Agent Team Skill and role-pinned Agent profiles safely."""

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
PLUGIN_ROOT = ROOT / "plugins" / "codex-agent-team"
SKILL_SOURCE = PLUGIN_ROOT / "skills" / "codex-agent-team"
PROFILE_SOURCE = PLUGIN_ROOT / "agent-profiles"
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
    parser = argparse.ArgumentParser(description="Install Codex Agent Team into Codex home.")
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
    parser.add_argument(
        "--adopt-legacy-install",
        action="store_true",
        help=(
            "Explicitly allow one migration of a differing pre-manifest Skill after "
            "confirming local Skill edits may be replaced."
        ),
    )
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def tree_snapshot(root: Path) -> dict[str, str]:
    if root.is_symlink() or not root.is_dir():
        fail(f"Expected a real directory: {root}")
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


def skill_is_exact(target: Path) -> bool:
    return target.is_dir() and not target.is_symlink() and tree_snapshot(target) == tree_snapshot(SKILL_SOURCE)


def validate_sources() -> None:
    if PLUGIN_ROOT.is_symlink() or not PLUGIN_ROOT.is_dir():
        fail(f"Plugin package is missing or unsafe: {PLUGIN_ROOT}")
    tree_snapshot(SKILL_SOURCE)
    seen: set[str] = set()
    for filename, expected in EXPECTED_PROFILES.items():
        path = PROFILE_SOURCE / filename
        if path.is_symlink() or not path.is_file():
            fail(f"Agent profile must be a regular non-symlink file: {path}")
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            fail(f"Invalid Agent profile {path}: {exc}")
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
        if expected[0] in seen:
            fail(f"Duplicate shipped Agent role name: {expected[0]}")
        seen.add(expected[0])


def desired_manifest(skill_only: bool) -> dict:
    return {
        "schema_version": MANIFEST_SCHEMA,
        "mode": "skill_only" if skill_only else "profile",
        "skill_hash": tree_hash(SKILL_SOURCE),
        "profile_hashes": (
            {}
            if skill_only
            else {name: file_hash(PROFILE_SOURCE / name) for name in PROFILE_FILES}
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
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"Invalid install manifest {path}: {exc}")
    if not isinstance(payload, dict) or payload.get("schema_version") != MANIFEST_SCHEMA:
        fail(f"Unsupported install manifest: {path}")
    if not isinstance(payload.get("profile_hashes", {}), dict):
        fail(f"Invalid profile hashes in install manifest: {path}")
    return payload


def preflight_parent(path: Path) -> None:
    if path.is_symlink():
        fail(f"Refusing symlinked destination directory: {path}")
    if path.exists() and not path.is_dir():
        fail(f"Destination parent is not a directory: {path}")


def preflight_skill(
    target: Path,
    *,
    check_only: bool,
    manifest: dict | None,
    adopt_legacy: bool,
) -> bool:
    """Return whether the existing Skill may be replaced."""
    if target.is_symlink():
        fail(f"Refusing symlinked installed Skill: {target}")
    if not target.exists():
        if check_only:
            fail(f"Installed Skill is missing: {target}")
        return True
    if not target.is_dir():
        fail(f"Installed Skill path is not a directory: {target}")
    if skill_is_exact(target):
        return False
    if check_only:
        fail(f"Installed Skill does not exactly match shipped source: {target}")
    actual = tree_hash(target)
    if manifest is None:
        if adopt_legacy:
            return True
        fail(
            "Refusing to overwrite a differing pre-manifest Skill because prior package ownership "
            "cannot be proven. Review local edits, then rerun with --adopt-legacy-install only if "
            f"the current package may replace that Skill: {target}"
        )
    if manifest.get("skill_hash") == actual:
        return True
    fail(
        "Refusing to overwrite an installed Skill that differs from the current package "
        f"and is not proven unchanged from the previous managed install: {target}"
    )


def preflight_profiles(
    agents_dir: Path, *, check_only: bool, manifest: dict | None
) -> set[str]:
    upgrades: set[str] = set()
    if not agents_dir.exists():
        if check_only:
            fail(f"Required agents directory is missing: {agents_dir}")
        return upgrades
    old_hashes = (manifest or {}).get("profile_hashes", {})
    for filename in PROFILE_FILES:
        target = agents_dir / filename
        source = PROFILE_SOURCE / filename
        if target.is_symlink():
            fail(f"Refusing symlinked Agent profile destination: {target}")
        if not target.exists():
            if check_only:
                fail(f"Required installed Agent profile is missing: {target}")
            continue
        if not target.is_file():
            fail(f"Agent profile destination is not a regular file: {target}")
        if target.read_bytes() == source.read_bytes():
            continue
        if not check_only and old_hashes.get(filename) == file_hash(target):
            upgrades.add(filename)
            continue
        fail(
            "Refusing to overwrite an Agent profile that differs from the current package "
            f"and is not proven unchanged from the previous managed install: {target}"
        )

    reserved = {values[0] for values in EXPECTED_PROFILES.values()}
    for existing in agents_dir.glob("*.toml"):
        if existing.name in PROFILE_FILES or existing.is_symlink() or not existing.is_file():
            continue
        try:
            data = tomllib.loads(existing.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            continue
        role = str(data.get("name", "")).strip()
        if role in reserved:
            fail(
                "Refusing to install because another Agent file uses the reserved role name "
                f"{role!r}: {existing}"
            )
    return upgrades


def stage_bytes(directory: Path, data: bytes, prefix: str) -> Path:
    fd, name = tempfile.mkstemp(prefix=prefix, dir=directory)
    staged = Path(name)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    return staged


def write_manifest(path: Path, payload: dict) -> None:
    data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    staged = stage_bytes(path.parent, data, ".codex-agent-team-manifest-")
    try:
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def verify_installed(target_skill: Path, agents_dir: Path, manifest_path: Path, skill_only: bool) -> None:
    if not skill_is_exact(target_skill):
        fail(f"Installed Skill does not exactly match shipped source: {target_skill}")
    if not skill_only:
        for filename in PROFILE_FILES:
            target = agents_dir / filename
            source = PROFILE_SOURCE / filename
            if target.is_symlink() or not target.is_file():
                fail(f"Installed Agent profile is missing or unsafe: {target}")
            if target.read_bytes() != source.read_bytes():
                fail(f"Installed Agent profile differs from shipped template: {target}")
    manifest = load_manifest(manifest_path)
    if manifest is None:
        fail(f"Managed install manifest is missing: {manifest_path}")
    if manifest != desired_manifest(skill_only):
        fail(f"Managed install manifest does not match installed artifacts: {manifest_path}")


def install(codex_home: Path, skill_only: bool, check_only: bool, adopt_legacy: bool) -> None:
    if check_only and adopt_legacy:
        fail("--adopt-legacy-install cannot be combined with --check")

    codex_home = codex_home.expanduser().resolve()
    skills_dir = codex_home / "skills"
    agents_dir = codex_home / "agents"
    target_skill = skills_dir / "codex-agent-team"
    manifest_path = codex_home / MANIFEST_NAME

    validate_sources()
    manifest = load_manifest(manifest_path)
    preflight_parent(skills_dir)
    if not skill_only:
        preflight_parent(agents_dir)
    replace_skill = preflight_skill(
        target_skill,
        check_only=check_only,
        manifest=manifest,
        adopt_legacy=adopt_legacy,
    )
    profile_upgrades = (
        set()
        if skill_only
        else preflight_profiles(agents_dir, check_only=check_only, manifest=manifest)
    )

    if check_only:
        if not skills_dir.is_dir():
            fail(f"Required skills directory is missing: {skills_dir}")
        verify_installed(target_skill, agents_dir, manifest_path, skill_only)
        print("CHECK PASSED: installed Codex Agent Team matches managed artifacts exactly.")
        return

    desired = desired_manifest(skill_only)
    profiles_exact = skill_only or (
        agents_dir.is_dir()
        and all(
            (agents_dir / filename).is_file()
            and not (agents_dir / filename).is_symlink()
            and (agents_dir / filename).read_bytes() == (PROFILE_SOURCE / filename).read_bytes()
            for filename in PROFILE_FILES
        )
    )
    if not replace_skill and profiles_exact and manifest == desired:
        print("Already installed exactly; no changes made.")
        return

    codex_home.mkdir(parents=True, exist_ok=True)
    skills_dir.mkdir(parents=True, exist_ok=True)
    if not skill_only:
        agents_dir.mkdir(parents=True, exist_ok=True)

    previous_manifest = manifest_path.read_bytes() if manifest_path.is_file() else None
    skill_backup: Path | None = None
    profile_backups: dict[Path, Path] = {}
    created_profiles: list[Path] = []
    new_skill = not target_skill.exists()
    staged_skill_root: Path | None = None

    try:
        if replace_skill:
            staged_skill_root = Path(tempfile.mkdtemp(prefix=".codex-agent-team-stage-", dir=skills_dir))
            staged_skill = staged_skill_root / "codex-agent-team"
            shutil.copytree(SKILL_SOURCE, staged_skill)
            if not skill_is_exact(staged_skill):
                fail("Staged Skill failed exactness verification")
            if target_skill.exists():
                skill_backup = skills_dir / f".codex-agent-team-backup-{uuid.uuid4().hex}"
                target_skill.rename(skill_backup)
            staged_skill.rename(target_skill)

        if not skill_only:
            for filename in PROFILE_FILES:
                source = PROFILE_SOURCE / filename
                target = agents_dir / filename
                if target.exists() and filename not in profile_upgrades:
                    continue
                staged = stage_bytes(agents_dir, source.read_bytes(), ".codex-agent-profile-")
                try:
                    if target.exists():
                        backup = agents_dir / f".{filename}.backup-{uuid.uuid4().hex}"
                        target.rename(backup)
                        profile_backups[target] = backup
                    staged.rename(target)
                    if target not in profile_backups:
                        created_profiles.append(target)
                finally:
                    staged.unlink(missing_ok=True)

        write_manifest(manifest_path, desired)
        verify_installed(target_skill, agents_dir, manifest_path, skill_only)
    except BaseException as exc:
        rollback_errors: list[str] = []
        for path in reversed(created_profiles):
            try:
                path.unlink(missing_ok=True)
            except OSError as rollback_exc:
                rollback_errors.append(f"could not remove created profile {path}: {rollback_exc}")
        for target, backup in reversed(list(profile_backups.items())):
            try:
                target.unlink(missing_ok=True)
                backup.rename(target)
            except OSError as rollback_exc:
                rollback_errors.append(f"could not restore profile {target}: {rollback_exc}")
        try:
            if skill_backup is not None and skill_backup.exists():
                shutil.rmtree(target_skill, ignore_errors=True)
                skill_backup.rename(target_skill)
            elif new_skill:
                shutil.rmtree(target_skill, ignore_errors=True)
        except OSError as rollback_exc:
            rollback_errors.append(f"could not restore Skill: {rollback_exc}")
        try:
            if previous_manifest is None:
                manifest_path.unlink(missing_ok=True)
            else:
                staged = stage_bytes(codex_home, previous_manifest, ".codex-agent-team-manifest-restore-")
                try:
                    os.replace(staged, manifest_path)
                finally:
                    staged.unlink(missing_ok=True)
        except OSError as rollback_exc:
            rollback_errors.append(f"could not restore install manifest: {rollback_exc}")
        if rollback_errors:
            fail(f"INSTALL FAILED: {exc}\nROLLBACK INCOMPLETE:\n- " + "\n- ".join(rollback_errors))
        raise
    else:
        for backup in profile_backups.values():
            backup.unlink(missing_ok=True)
        if skill_backup is not None:
            shutil.rmtree(skill_backup, ignore_errors=True)
    finally:
        if staged_skill_root is not None:
            shutil.rmtree(staged_skill_root, ignore_errors=True)

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
    install(args.codex_home, args.skill_only, args.check, args.adopt_legacy_install)


if __name__ == "__main__":
    main()
