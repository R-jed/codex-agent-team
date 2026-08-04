#!/usr/bin/env python3
"""Create or verify a deterministic identity for the current Git deliverable.

The identity binds the current HEAD, the complete tracked working-tree diff against
HEAD, and every non-ignored untracked file. It intentionally does not hash ignored
build/cache artifacts because they are not normally part of a source deliverable.

This helper is read-only. It does not update the index, create commits, or mutate the
working tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import NoReturn

SCHEMA_VERSION = 1


def fail(message: str, *, code: int = 1) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or verify a deterministic Codex Delegate review artifact identity."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Path inside the Git working tree (default: current directory).",
    )
    parser.add_argument(
        "--verify",
        metavar="ARTIFACT_ID",
        help="Exit nonzero unless the current artifact exactly matches this id.",
    )
    return parser.parse_args()


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", os.fspath(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode(errors="replace").strip()
        fail(f"git {' '.join(args)} failed: {detail or f'exit {result.returncode}'}")
    return result.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repository_root(repo: Path) -> Path:
    raw = git(repo, "rev-parse", "--show-toplevel").rstrip(b"\n")
    if not raw:
        fail("Git returned an empty repository root")
    return Path(os.fsdecode(raw)).resolve()


def head_identity(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", os.fspath(root), "rev-parse", "--verify", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        value = result.stdout.decode("ascii", errors="strict").strip()
        if not value:
            fail("Git returned an empty HEAD identity")
        return value
    return "UNBORN"


def tracked_diff_digest(root: Path, head: str) -> str:
    if head == "UNBORN":
        # In an unborn repository every staged tracked file is part of the candidate.
        diff = git(root, "diff", "--binary", "--no-ext-diff", "--cached", "--")
    else:
        # `git diff HEAD` binds both staged and unstaged tracked changes.
        diff = git(root, "diff", "--binary", "--no-ext-diff", "HEAD", "--")
    return sha256(diff)


def untracked_paths(root: Path) -> list[bytes]:
    raw = git(root, "ls-files", "--others", "--exclude-standard", "-z")
    paths = [item for item in raw.split(b"\0") if item]
    return sorted(paths)


def digest_untracked(root: Path, raw_path: bytes) -> dict[str, str]:
    relative = os.fsdecode(raw_path)
    path = root / relative
    try:
        info = path.lstat()
    except OSError as exc:
        fail(f"could not stat untracked path {relative!r}: {exc}")

    mode = stat.S_IFMT(info.st_mode)
    if stat.S_ISREG(mode):
        kind = "file"
        try:
            digest = sha256(path.read_bytes())
        except OSError as exc:
            fail(f"could not read untracked file {relative!r}: {exc}")
    elif stat.S_ISLNK(mode):
        kind = "symlink"
        try:
            target = os.readlink(path)
        except OSError as exc:
            fail(f"could not read untracked symlink {relative!r}: {exc}")
        digest = sha256(os.fsencode(target))
    else:
        fail(f"unsupported untracked file type for review artifact: {relative!r}")

    return {
        "path": os.fsdecode(raw_path),
        "kind": kind,
        "sha256": digest,
    }


def build_receipt(repo: Path) -> dict:
    root = repository_root(repo.expanduser().resolve())
    head = head_identity(root)
    diff_sha = tracked_diff_digest(root, head)
    untracked = [digest_untracked(root, path) for path in untracked_paths(root)]

    canonical_state = {
        "schema_version": SCHEMA_VERSION,
        "head": head,
        "tracked_diff_sha256": diff_sha,
        "untracked": untracked,
    }
    canonical_bytes = json.dumps(
        canonical_state,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return {
        **canonical_state,
        "review_artifact_id": f"sha256:{sha256(canonical_bytes)}",
    }


def main() -> None:
    args = parse_args()
    receipt = build_receipt(args.repo)
    current = receipt["review_artifact_id"]

    if args.verify is not None and current != args.verify:
        print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
        fail(
            f"review artifact changed: expected {args.verify}, current {current}",
            code=2,
        )

    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
