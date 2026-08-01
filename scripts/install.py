#!/usr/bin/env python3
"""Install Codex Agent Team and its locked Agent profiles.

Default behavior installs both the Skill and the four project-specific Agent profiles.
Use --skill-only only when you intentionally want Portable Mode without profile locks.
The installer fails closed on Agent-profile filename or role-name conflicts.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / "skill" / "codex-agent-team"
PROFILE_SOURCE = ROOT / "examples" / "agents"
PROFILE_FILES = (
    "luna-explorer.toml",
    "luna-worker.toml",
    "terra-reviewer.toml",
    "sol-judge.toml",
)


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
    return parser.parse_args()


def profile_name(path: Path) -> str:
    data = tomllib.loads(path.read_text())
    name = str(data.get("name", "")).strip()
    if not name:
        raise SystemExit(f"Agent profile has no valid name: {path}")
    return name


def preflight_profiles(agents_dir: Path) -> None:
    desired_by_name = {
        profile_name(PROFILE_SOURCE / filename): PROFILE_SOURCE / filename
        for filename in PROFILE_FILES
    }
    desired_targets = {
        name: agents_dir / source.name for name, source in desired_by_name.items()
    }

    if not agents_dir.exists():
        return

    for existing in agents_dir.glob("*.toml"):
        target_source = PROFILE_SOURCE / existing.name
        if existing.name in PROFILE_FILES:
            if existing.read_bytes() != target_source.read_bytes():
                raise SystemExit(
                    "Refusing to overwrite an existing Agent profile with different content: "
                    f"{existing}"
                )

        try:
            existing_name = profile_name(existing)
        except (tomllib.TOMLDecodeError, UnicodeDecodeError):
            continue

        if existing_name not in desired_by_name:
            continue

        expected_target = desired_targets[existing_name]
        source = desired_by_name[existing_name]
        if existing != expected_target or existing.read_bytes() != source.read_bytes():
            raise SystemExit(
                "Refusing to install because an existing Agent uses the reserved role name "
                f"{existing_name!r}: {existing}"
            )


def install(codex_home: Path, skill_only: bool) -> None:
    codex_home = codex_home.expanduser().resolve()
    skills_dir = codex_home / "skills"
    agents_dir = codex_home / "agents"
    target_skill = skills_dir / "codex-agent-team"

    if not skill_only:
        preflight_profiles(agents_dir)

    skills_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL_SOURCE, target_skill, dirs_exist_ok=True)
    print(f"Installed Skill: {target_skill}")

    if skill_only:
        print("Skipped Agent profiles (--skill-only).")
        print("Portable Mode will require live spawn_agent model/effort overrides.")
        return

    agents_dir.mkdir(parents=True, exist_ok=True)
    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        shutil.copy2(source, target)
        print(f"Installed Agent profile: {target}")

    print("Installed exact route profiles: luna_explorer, luna_worker, terra_reviewer, sol_judge")
    print("Restart or reopen Codex so the newly installed Agent profiles are discovered.")


def main() -> None:
    args = parse_args()
    install(args.codex_home, args.skill_only)


if __name__ == "__main__":
    main()
