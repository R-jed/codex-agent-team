#!/usr/bin/env python3
"""Validate and summarize recorded paired Codex Agent Team live runs.

The scorer never executes Codex and never invents missing telemetry. Pair integrity is
checked before aggregate mode statistics are reported.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
from typing import Any, NoReturn

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"
WORKLOADS = ROOT / "evals" / "behavioral-workloads.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score recorded paired Codex Agent Team live evals.")
    parser.add_argument("result", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def mean_present(runs: list[dict[str, Any]], field: str) -> float | None:
    values = [run[field] for run in runs if isinstance(run.get(field), (int, float)) and not isinstance(run.get(field), bool)]
    return statistics.fmean(values) if values else None


def validate_pairs(runs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    pairs: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        pairs.setdefault(run["pair_id"], []).append(run)
    for pair_id, pair_runs in pairs.items():
        if len(pair_runs) < 2:
            fail(f"pair {pair_id!r} has fewer than two runs")
        keys = {
            (run["workload_id"], run["repo_revision"], run["repeat_index"])
            for run in pair_runs
        }
        if len(keys) != 1:
            fail(f"pair {pair_id!r} mixes workload, revision, or repeat index")
        modes = [run["mode"] for run in pair_runs]
        if len(modes) != len(set(modes)):
            fail(f"pair {pair_id!r} contains duplicate modes")
    return pairs


def mode_summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "runs": len(runs),
        "success_rate": sum(bool(run["success"]) for run in runs) / len(runs),
        "mean_acceptance_score": mean_present(runs, "acceptance_score"),
        "mean_agent_count": statistics.fmean(run["agent_count"] for run in runs),
        "policy_violations": sum(len(run.get("policy_violations", [])) for run in runs),
        "scope_violations": sum(run.get("scope_violations", 0) for run in runs),
        "wrong_edits": sum(run.get("wrong_edits", 0) for run in runs),
        "regressions": sum(run.get("regressions", 0) for run in runs),
        "mean_correction_turns": mean_present(runs, "correction_turns"),
        "mean_main_session_correction_tokens": mean_present(runs, "main_session_correction_tokens"),
        "mean_main_session_correction_ms": mean_present(runs, "main_session_correction_ms"),
        "mean_input_tokens": mean_present(runs, "input_tokens"),
        "mean_output_tokens": mean_present(runs, "output_tokens"),
        "mean_reasoning_tokens": mean_present(runs, "reasoning_tokens"),
        "mean_latency_ms": mean_present(runs, "latency_ms"),
        "review_material_catches": sum(run.get("review_caught_material_issue") is True for run in runs),
        "review_false_positives": sum(run.get("review_false_positives", 0) for run in runs),
        "unjustified_repeated_commands": sum(run.get("unjustified_repeated_commands", 0) for run in runs),
        "unjustified_repeated_discovery": sum(run.get("unjustified_repeated_discovery", 0) for run in runs),
        "duplicate_dependency_calls": sum(run.get("duplicate_dependency_calls", 0) for run in runs),
    }


def main() -> None:
    args = parse_args()
    try:
        payload = json.loads(args.result.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        workloads = json.loads(WORKLOADS.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(str(exc))

    jsonschema.Draft202012Validator(schema).validate(payload)
    known = {item["id"] for item in workloads["workloads"]}
    unknown = sorted({run["workload_id"] for run in payload["runs"]} - known)
    if unknown:
        fail(f"unknown workload ids: {', '.join(unknown)}")

    pairs = validate_pairs(payload["runs"])
    by_mode: dict[str, list[dict[str, Any]]] = {}
    for run in payload["runs"]:
        by_mode.setdefault(run["mode"], []).append(run)

    summary: dict[str, Any] = {
        "runtime": payload["runtime"],
        "pair_count": len(pairs),
        "pairs": {},
        "modes": {},
    }
    for pair_id, pair_runs in sorted(pairs.items()):
        first = pair_runs[0]
        summary["pairs"][pair_id] = {
            "workload_id": first["workload_id"],
            "repo_revision": first["repo_revision"],
            "repeat_index": first["repeat_index"],
            "modes": sorted(run["mode"] for run in pair_runs),
        }
    for mode, runs in sorted(by_mode.items()):
        summary["modes"][mode] = mode_summary(runs)

    if args.json:
        json.dump(summary, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return

    print(f"Runtime: {payload['runtime']['codex_version']} ({payload['runtime']['date']})")
    print(f"Pairs: {summary['pair_count']}")
    for mode, stats in summary["modes"].items():
        print(f"\n{mode}")
        print(f"  runs: {stats['runs']}")
        print(f"  success_rate: {stats['success_rate']:.3f}")
        print(f"  mean_agent_count: {stats['mean_agent_count']:.2f}")
        for field in [
            "mean_acceptance_score",
            "mean_correction_turns",
            "mean_main_session_correction_tokens",
            "mean_input_tokens",
            "mean_reasoning_tokens",
            "mean_latency_ms",
        ]:
            value = stats[field]
            print(f"  {field}: {'not_recorded' if value is None else round(value, 2)}")
        print(f"  unjustified_repeated_commands: {stats['unjustified_repeated_commands']}")
        print(f"  unjustified_repeated_discovery: {stats['unjustified_repeated_discovery']}")
        print(f"  duplicate_dependency_calls: {stats['duplicate_dependency_calls']}")


if __name__ == "__main__":
    main()
