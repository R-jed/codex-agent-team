#!/usr/bin/env python3
"""Validate and summarize recorded live behavioral runs.

This scorer never executes Codex. It consumes results produced by real runs and emits
aggregate metrics without inventing missing token/latency data.
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
    parser = argparse.ArgumentParser(description="Score recorded Codex Agent Team live evals.")
    parser.add_argument("result", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def mean_present(runs: list[dict[str, Any]], field: str) -> float | None:
    values = [run[field] for run in runs if isinstance(run.get(field), int)]
    return statistics.fmean(values) if values else None


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

    by_mode: dict[str, list[dict[str, Any]]] = {}
    for run in payload["runs"]:
        by_mode.setdefault(run["mode"], []).append(run)

    summary: dict[str, Any] = {"runtime": payload["runtime"], "modes": {}}
    for mode, runs in sorted(by_mode.items()):
        violations = sum(len(run.get("policy_violations", [])) for run in runs)
        summary["modes"][mode] = {
            "runs": len(runs),
            "success_rate": sum(bool(run["success"]) for run in runs) / len(runs),
            "mean_agent_count": statistics.fmean(run["agent_count"] for run in runs),
            "policy_violations": violations,
            "mean_input_tokens": mean_present(runs, "input_tokens"),
            "mean_output_tokens": mean_present(runs, "output_tokens"),
            "mean_reasoning_tokens": mean_present(runs, "reasoning_tokens"),
            "mean_latency_ms": mean_present(runs, "latency_ms"),
            "review_material_catches": sum(
                run.get("review_caught_material_issue") is True for run in runs
            ),
            "consent_prompts": sum(run.get("consent_prompts", 0) for run in runs),
        }

    if args.json:
        json.dump(summary, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return

    print(f"Runtime: {payload['runtime']['codex_version']} ({payload['runtime']['date']})")
    for mode, stats in summary["modes"].items():
        print(f"\n{mode}")
        print(f"  runs: {stats['runs']}")
        print(f"  success_rate: {stats['success_rate']:.3f}")
        print(f"  mean_agent_count: {stats['mean_agent_count']:.2f}")
        print(f"  policy_violations: {stats['policy_violations']}")
        for field in ["mean_input_tokens", "mean_output_tokens", "mean_reasoning_tokens", "mean_latency_ms"]:
            value = stats[field]
            print(f"  {field}: {'not_recorded' if value is None else round(value, 2)}")


if __name__ == "__main__":
    main()
