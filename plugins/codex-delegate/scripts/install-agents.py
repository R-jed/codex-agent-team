#!/usr/bin/env python3
"""Provision codex delegate custom-Agent profiles safely."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import tomllib
from typing import NoReturn
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROFILE_SOURCE = ROOT / "agent-profiles"
POLICY_CONTRACT_PATH = ROOT / "policy-contract.json"
MANIFEST_NAME = ".codex-delegate-agents.json"
MANIFEST_SCHEMA = 1
MANAGED_BY = "codex-delegate"
POLICY_SCHEMA = 3
ROLE_KEYS = {"reader", "worker", "solver", "investigator", "advisor"}


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_policy_contract() -> dict:
    try:
        payload = json.loads(POLICY_CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"Invalid codex delegate policy contract {POLICY_CONTRACT_PATH}: {exc}")
    if not isinstance(payload, dict) or payload.get("schema_version") != POLICY_SCHEMA:
        fail(f"Unsupported codex delegate policy contract: {POLICY_CONTRACT_PATH}")
    roles = payload.get("roles")
    if not isinstance(roles, dict) or set(roles) != ROLE_KEYS:
        fail("Policy contract must define reader, worker, solver, investigator, and advisor roles")
    required = {"profile_file", "agent_type", "model", "effort", "sandbox_intent"}
    seen_files: set[str] = set()
    seen_names: set[str] = set()
    for role, spec in roles.items():
        if not isinstance(spec, dict) or not required <= set(spec):
            fail(f"Policy contract role {role!r} is incomplete")
        values = [spec.get(key) for key in required]
        if not all(isinstance(value, str) and value.strip() for value in values):
            fail(f"Policy contract role {role!r} contains an empty/non-string constant")
        if spec["profile_file"] in seen_files or spec["agent_type"] in seen_names:
            fail(f"Duplicate profile or Agent role in policy contract: {role}")
        seen_files.add(spec["profile_file"])
        seen_names.add(spec["agent_type"])
    return payload


POLICY_CONTRACT = load_policy_contract()
ROLE_SPECS = POLICY_CONTRACT["roles"]
PROFILE_FILES = tuple(spec["profile_file"] for spec in ROLE_SPECS.values())
EXPECTED_PROFILES = {
    spec["profile_file"]: (
        spec["agent_type"], spec["model"], spec["effort"], spec["sandbox_intent"]
    )
    for spec in ROLE_SPECS.values()
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Provision codex delegate managed custom-Agent profiles.")
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex home directory (default: $CODEX_HOME or ~/.codex).",
    )
    parser.add_argument("--check", action="store_true", help="Verify current managed state without mutation.")
    return parser.parse_args()


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
    if not isinstance(payload, dict) or not isinstance(payload.get("profile_hashes", {}), dict):
        fail(f"Invalid install manifest object: {path}")
    if payload.get("schema_version") != MANIFEST_SCHEMA or payload.get("managed_by") != MANAGED_BY:
        fail(f"Unsupported codex delegate managed-profile manifest: {path}")
    return payload


def manifest_hashes(manifest: dict | None) -> dict[str, str]:
    if manifest is None:
        return {}
    return {
        str(key): str(value)
        for key, value in manifest.get("profile_hashes", {}).items()
        if isinstance(key, str) and isinstance(value, str)
    }


def desired_manifest() -> dict:
    return {
        "schema_version": MANIFEST_SCHEMA,
        "managed_by": MANAGED_BY,
        "profile_hashes": {
            filename: file_hash(PROFILE_SOURCE / filename) for filename in PROFILE_FILES
        },
    }


def validate_sources() -> None:
    seen_names: set[str] = set()
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
            str(data.get("sandbox_mode", "")).strip(),
        )
        if actual != expected:
            fail(f"Agent profile {filename} pins {actual!r}; expected {expected!r}")
        if not str(data.get("description", "")).strip() or not str(data.get("developer_instructions", "")).strip():
            fail(f"Agent profile is incomplete: {filename}")
        if expected[0] in seen_names:
            fail(f"Duplicate shipped Agent role name: {expected[0]}")
        seen_names.add(expected[0])


def preflight_agents_dir(path: Path, *, check_only: bool) -> None:
    if path.is_symlink():
        fail(f"Refusing symlinked agents directory: {path}")
    if path.exists() and not path.is_dir():
        fail(f"Agents destination is not a directory: {path}")
    if check_only and not path.is_dir():
        fail(f"Required agents directory is missing: {path}")


def parse_profile_name(path: Path) -> str | None:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return None
    return str(data.get("name", "")).strip() or None


def preflight_profiles(
    agents_dir: Path,
    *,
    check_only: bool,
    managed_hashes: dict[str, str],
) -> set[str]:
    upgrades: set[str] = set()

    for filename in PROFILE_FILES:
        source = PROFILE_SOURCE / filename
        target = agents_dir / filename
        if target.is_symlink():
            fail(f"Refusing symlinked Agent profile destination: {target}")
        if not target.exists():
            if check_only:
                fail(f"Missing managed Agent profile: {target}")
            continue
        if not target.is_file():
            fail(f"Agent profile destination is not a regular file: {target}")
        if target.read_bytes() == source.read_bytes():
            continue
        prior_hash = managed_hashes.get(filename)
        if prior_hash is None or file_hash(target) != prior_hash:
            fail(f"Refusing to overwrite unowned or modified Agent profile: {target}")
        if check_only:
            fail(f"Managed Agent profile is stale: {target}")
        upgrades.add(filename)

    reserved_names = {spec["agent_type"] for spec in ROLE_SPECS.values()}
    managed_files = set(PROFILE_FILES)
    if agents_dir.exists():
        for path in agents_dir.glob("*.toml"):
            if path.name in managed_files:
                continue
            if path.is_symlink():
                continue
            name = parse_profile_name(path)
            if name in reserved_names:
                fail(f"Another Agent profile claims reserved current role name {name!r}: {path}")
    return upgrades


def build_plan(agents_dir: Path, upgrades: set[str]) -> dict[str, bytes]:
    plan: dict[str, bytes] = {}
    for filename in PROFILE_FILES:
        target = agents_dir / filename
        if not target.exists() or filename in upgrades:
            plan[str(target)] = (PROFILE_SOURCE / filename).read_bytes()
    return plan


def preflight_manifest(path: Path, *, check_only: bool, desired: dict, current: dict | None) -> None:
    if path.is_symlink():
        fail(f"Refusing symlinked install manifest: {path}")
    if path.exists() and not path.is_file():
        fail(f"Install manifest is not a regular file: {path}")
    if check_only and current != desired:
        fail(f"Managed Agent manifest is stale: {path}")


def write_transaction(files: dict[str, bytes], manifest_path: Path, manifest_bytes: bytes) -> None:
    backups: dict[Path, bytes | None] = {}
    staged: dict[Path, Path] = {}
    try:
        for raw_target, data in files.items():
            target = Path(raw_target)
            target.parent.mkdir(parents=True, exist_ok=True)
            backups[target] = target.read_bytes() if target.exists() else None
            fd, raw_stage = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
            os.close(fd)
            stage = Path(raw_stage)
            stage.write_bytes(data)
            staged[target] = stage
        backups[manifest_path] = manifest_path.read_bytes() if manifest_path.exists() else None
        fd, raw_stage = tempfile.mkstemp(prefix=f".{manifest_path.name}.", suffix=".tmp", dir=manifest_path.parent)
        os.close(fd)
        manifest_stage = Path(raw_stage)
        manifest_stage.write_bytes(manifest_bytes)
        staged[manifest_path] = manifest_stage

        for target, stage in staged.items():
            os.replace(stage, target)
    except BaseException:
        for stage in staged.values():
            if stage.exists():
                stage.unlink()
        for target, previous in backups.items():
            try:
                if previous is None:
                    if target.exists() and not target.is_symlink():
                        target.unlink()
                else:
                    target.write_bytes(previous)
            except OSError:
                pass
        raise


def verify_current_state(codex_home: Path) -> None:
    agents_dir = codex_home / "agents"
    manifest_path = codex_home / MANIFEST_NAME
    if not agents_dir.is_dir() or agents_dir.is_symlink():
        fail(f"Managed agents directory missing or unsafe: {agents_dir}")
    manifest = load_manifest(manifest_path)
    desired = desired_manifest()
    if manifest != desired:
        fail(f"Managed Agent manifest does not match current project generation: {manifest_path}")
    for filename, expected in EXPECTED_PROFILES.items():
        target = agents_dir / filename
        if target.is_symlink() or not target.is_file():
            fail(f"Managed Agent profile missing or unsafe: {target}")
        if target.read_bytes() != (PROFILE_SOURCE / filename).read_bytes():
            fail(f"Managed Agent profile differs from current project generation: {target}")
        data = tomllib.loads(target.read_text(encoding="utf-8"))
        actual = (
            str(data.get("name", "")).strip(),
            str(data.get("model", "")).strip(),
            str(data.get("model_reasoning_effort", "")).strip(),
            str(data.get("sandbox_mode", "")).strip(),
        )
        if actual != expected:
            fail(f"Managed Agent profile tuple mismatch: {target}")


def main() -> None:
    args = parse_args()
    codex_home = args.codex_home.expanduser()
    if codex_home.is_symlink():
        fail(f"Refusing symlinked Codex home: {codex_home}")
    if codex_home.exists() and not codex_home.is_dir():
        fail(f"Codex home is not a directory: {codex_home}")
    if not args.check:
        codex_home.mkdir(parents=True, exist_ok=True)

    validate_sources()
    agents_dir = codex_home / "agents"
    preflight_agents_dir(agents_dir, check_only=args.check)
    manifest_path = codex_home / MANIFEST_NAME
    current_manifest = load_manifest(manifest_path)
    managed_hashes = manifest_hashes(current_manifest)
    upgrades = preflight_profiles(
        agents_dir,
        check_only=args.check,
        managed_hashes=managed_hashes,
    )
    desired = desired_manifest()
    preflight_manifest(
        manifest_path,
        check_only=args.check,
        desired=desired,
        current=current_manifest,
    )

    if args.check:
        verify_current_state(codex_home)
        print(f"codex delegate managed Agent profiles verified under {codex_home}")
        return

    agents_dir.mkdir(parents=True, exist_ok=True)
    plan = build_plan(agents_dir, upgrades)
    manifest_bytes = (json.dumps(desired, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if plan or current_manifest != desired:
        write_transaction(plan, manifest_path, manifest_bytes)
    verify_current_state(codex_home)
    print(f"codex delegate managed Agent profiles installed under {codex_home}")


if __name__ == "__main__":
    main()
