#!/usr/bin/env python3
"""Create or verify a deterministic identity for the current Git deliverable.

The identity binds the current HEAD, the complete tracked working-tree diff against
HEAD (or the repository's empty tree before the first commit), and every non-ignored
untracked file. It intentionally does not hash ignored build/cache artifacts because
they are not normally part of a source deliverable.

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


def git(repo: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", os.fspath(repo), *args],
        input=input_bytes,
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

    symbolic = subprocess.run(
        ["git", "-C", os.fspath(root), "symbolic-ref", "-q", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if symbolic.returncode == 0 and symbolic.stdout.strip():
        return "UNBORN"

    detail = result.stderr.decode(errors="replace").strip()
    fail(f"could not resolve HEAD: {detail or f'exit {result.returncode}'}")


def empty_tree_identity(root: Path) -> str:
    raw = git(root, "hash-object", "-t", "tree", "--stdin", input_bytes=b"").strip()
    try:
        value = raw.decode("ascii", errors="strict")
    except UnicodeDecodeError as exc:
        fail(f"Git returned a non-ASCII empty-tree identity: {exc}")
    if not value:
        fail("Git returned an empty empty-tree identity")
    return value


def tracked_diff_digest(root: Path, head: str) -> str:
    common = (
        "diff",
        "--binary",
        "--full-index",
        "--no-color",
        "--no-ext-diff",
        "--no-textconv",
        "--no-renames",
        "--ignore-submodules=none",
        "--src-prefix=a/",
        "--dst-prefix=b/",
    )
    base = empty_tree_identity(root) if head == "UNBORN" else "HEAD"
    # `git diff <tree>` compares the current tracked working-tree content with the
    # named tree, so staged + unstaged edits are both bound without making staging
    # arrangement itself part of the deliverable identity.
    diff = git(root, *common, base, "--")
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

    if stat.S_ISREG(info.st_mode):
        kind = "file"
        git_mode = "100755" if info.st_mode & 0o111 else "100644"
        try:
            digest = sha256(path.read_bytes())
        except OSError as exc:
            fail(f"could not read untracked file {relative!r}: {exc}")
    elif stat.S_ISLNK(info.st_mode):
        kind = "symlink"
        git_mode = "120000"
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
        "mode": git_mode,
        "sha256": digest,
    }


def build_receipt_once(root: Path) -> dict:
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
        ensure_ascii=True,
    ).encode("ascii")

    return {
        **canonical_state,
        "review_artifact_id": f"sha256:{sha256(canonical_bytes)}",
    }


def build_receipt(repo: Path) -> dict:
    root = repository_root(repo.expanduser().resolve())
    first = build_receipt_once(root)
    second = build_receipt_once(root)
    if first != second:
        fail("workspace changed while review artifact identity was being captured; retry from a quiescent state")
    return second


def emit(receipt: dict) -> None:
    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=True))


def main() -> None:
    args = parse_args()
    receipt = build_receipt(args.repo)
    current = receipt["review_artifact_id"]

    if args.verify is not None and current != args.verify:
        emit(receipt)
        fail(
            f"review artifact changed: expected {args.verify}, current {current}",
            code=2,
        )

    emit(receipt)


if __name__ == "__main__":
    main()
