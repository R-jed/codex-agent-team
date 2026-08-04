#!/usr/bin/env python3
"""Validate and summarize recorded paired Codex Delegate live runs.

The scorer validates controlled pairs before computing candidate-minus-baseline deltas.
Metric definitions are declarative so adding telemetry does not require independent
field lists for deltas, summaries, and CLI rendering.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import statistics
import sys
from typing import Any, Literal, NoReturn

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"
WORKLOADS = ROOT / "evals" / "behavioral-workloads.json"

PAIR_CONTROL_FIELDS = (
    "workload_definition_hash",
    "main_session_route",
    "permissions_fingerprint",
    "tool_surface_fingerprint",
    "acceptance_rubric_id",
)


@dataclass(frozen=True)
class Metric:
    field: str
    summary_key: str
    aggregate: Literal["mean", "sum"]
    delta: bool = True


METRICS = (
    Metric("acceptance_score", "mean_acceptance_score", "mean"),
    Metric("agent_count", "mean_agent_count", "mean"),
    Metric("peak_active_children", "mean_peak_active_children", "mean"),
    Metric("ready_dependencies", "mean_ready_dependencies", "mean"),
    Metric("runtime_slot_waits", "runtime_slot_waits", "sum"),
    Metric("scope_violations", "scope_violations", "sum"),
    Metric("wrong_edits", "wrong_edits", "sum"),
    Metric("regressions", "regressions", "sum"),
    Metric("correction_turns", "mean_correction_turns", "mean"),
    Metric("execution_stall_events", "execution_stall_events", "sum"),
    Metric("clean_same_lane_restarts", "clean_same_lane_restarts", "sum"),
    Metric("unjustified_retry_calls", "unjustified_retry_calls", "sum"),
    Metric("same_failure_without_new_evidence", "same_failure_without_new_evidence", "sum"),
    Metric("main_session_correction_tokens", "mean_main_session_correction_tokens", "mean"),
    Metric("main_session_correction_ms", "mean_main_session_correction_ms", "mean"),
    Metric("review_findings", "review_findings", "sum"),
    Metric("review_false_positives", "review_false_positives", "sum"),
    Metric("final_review_attempts", "final_review_attempts", "sum"),
    Metric("review_artifact_verify_failures", "review_artifact_verify_failures", "sum"),
    Metric("post_review_mutations", "post_review_mutations", "sum"),
    Metric("consent_prompts", "consent_prompts", "sum"),
    Metric("input_tokens", "mean_input_tokens", "mean"),
    Metric("output_tokens", "mean_output_tokens", "mean"),
    Metric("reasoning_tokens", "mean_reasoning_tokens", "mean"),
    Metric("latency_ms", "mean_latency_ms", "mean"),
    Metric("evidence_established", "evidence_established", "sum"),
    Metric("evidence_invalidated", "evidence_invalidated", "sum"),
    Metric("unjustified_repeated_commands", "unjustified_repeated_commands", "sum"),
    Metric("unjustified_repeated_discovery", "unjustified_repeated_discovery", "sum"),
    Metric("duplicate_dependency_calls", "duplicate_dependency_calls", "sum"),
)

DELTA_FIELDS = tuple(metric.field for metric in METRICS if metric.delta)
METRIC_BY_FIELD = {metric.field: metric for metric in METRICS}

COMPARISON_CLI_FIELDS = (
    "acceptance_score",
    "correction_turns",
    "main_session_correction_tokens",
    "input_tokens",
    "reasoning_tokens",
    "latency_ms",
    "unjustified_retry_calls",
    "review_findings",
    "review_false_positives",
    "final_review_attempts",
    "review_artifact_verify_failures",
    "post_review_mutations",
    "unjustified_repeated_commands",
    "unjustified_repeated_discovery",
    "duplicate_dependency_calls",
)

MODE_MEAN_CLI_KEYS = (
    "mean_peak_active_children",
    "mean_ready_dependencies",
    "mean_acceptance_score",
    "mean_correction_turns",
    "mean_main_session_correction_tokens",
    "mean_input_tokens",
    "mean_reasoning_tokens",
    "mean_latency_ms",
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score recorded paired Codex Delegate live evals.")
    parser.add_argument("result", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def number_or_none(value: Any) -> float | int | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    return None


def mean_values(values: list[float | int | None]) -> float | None:
    present = [value for value in values if value is not None]
    return statistics.fmean(present) if present else None


def metric_summary(runs: list[dict[str, Any]], metric: Metric) -> float | int | None:
    values = [number_or_none(run.get(metric.field)) for run in runs]
    if metric.aggregate == "mean":
        return mean_values(values)
    return sum(value for value in values if value is not None)


def workload_specs(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in payload["workloads"]}


def declared_primary_modes(spec: dict[str, Any]) -> list[str] | None:
    comparison = spec.get("expected", {}).get("primary_comparison")
    if comparison is None:
        return None
    if (
        not isinstance(comparison, list)
        or len(comparison) != 2
        or not all(isinstance(item, str) for item in comparison)
    ):
        fail(f"workload {spec['id']!r} has invalid primary_comparison metadata")
    return comparison


def validate_pairs(
    runs: list[dict[str, Any]], specs: dict[str, dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
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

        for field in PAIR_CONTROL_FIELDS:
            if len({run[field] for run in pair_runs}) != 1:
                fail(f"pair {pair_id!r} mixes controlled field {field!r}")

        worker_routes = {
            run.get("worker_route")
            for run in pair_runs
            if isinstance(run.get("worker_route"), str) and run.get("worker_route")
        }
        if len(worker_routes) > 1:
            fail(f"pair {pair_id!r} mixes worker routes")

        workload_id = pair_runs[0]["workload_id"]
        primary = declared_primary_modes(specs[workload_id])
        if primary is not None and set(modes) != set(primary):
            fail(
                f"pair {pair_id!r} for workload {workload_id!r} must contain declared "
                f"primary comparison modes {primary!r}; got {sorted(modes)!r}"
            )
    return pairs


def mode_summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "runs": len(runs),
        "success_rate": sum(bool(run["success"]) for run in runs) / len(runs),
        "policy_violations": sum(len(run.get("policy_violations", [])) for run in runs),
    }
    for metric in METRICS:
        summary[metric.summary_key] = metric_summary(runs, metric)

    final_review_attempts = int(summary["final_review_attempts"] or 0)
    review_material_catches = sum(run.get("review_caught_material_issue") is True for run in runs)
    required_review_runs = sum(run.get("final_review_requirement") == "required" for run in runs)
    satisfied_review_runs = sum(run.get("final_review_gate_satisfied") is True for run in runs)
    unsatisfied_required_review_runs = sum(
        run.get("final_review_requirement") == "required"
        and run.get("final_review_gate_satisfied") is not True
        for run in runs
    )
    summary.update(
        {
            "review_material_catches": review_material_catches,
            "final_review_required_runs": required_review_runs,
            "final_review_satisfied_runs": satisfied_review_runs,
            "final_review_unsatisfied_required_runs": unsatisfied_required_review_runs,
            "final_review_yield": (
                review_material_catches / final_review_attempts
                if final_review_attempts > 0
                else None
            ),
        }
    )
    return summary


def delta(baseline: dict[str, Any], candidate: dict[str, Any], field: str) -> float | int | None:
    left = number_or_none(baseline.get(field))
    right = number_or_none(candidate.get(field))
    if left is None or right is None:
        return None
    return right - left


def pair_comparison(
    pair_runs: list[dict[str, Any]], primary_modes: list[str]
) -> dict[str, Any]:
    by_mode = {run["mode"]: run for run in pair_runs}
    baseline_mode, candidate_mode = primary_modes
    baseline = by_mode[baseline_mode]
    candidate = by_mode[candidate_mode]
    return {
        "baseline_mode": baseline_mode,
        "candidate_mode": candidate_mode,
        "success_delta": int(bool(candidate["success"])) - int(bool(baseline["success"])),
        "metric_deltas": {
            field: delta(baseline, candidate, field)
            for field in DELTA_FIELDS
        },
    }


def aggregate_comparisons(items: list[dict[str, Any]]) -> dict[str, Any]:
    first = items[0]
    return {
        "pair_count": len(items),
        "baseline_mode": first["baseline_mode"],
        "candidate_mode": first["candidate_mode"],
        "mean_success_delta": statistics.fmean(item["success_delta"] for item in items),
        "mean_metric_deltas": {
            field: mean_values([item["metric_deltas"][field] for item in items])
            for field in DELTA_FIELDS
        },
    }


def build_summary(payload: dict[str, Any], specs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pairs = validate_pairs(payload["runs"], specs)
    by_mode: dict[str, list[dict[str, Any]]] = {}
    by_workload_mode: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for run in payload["runs"]:
        by_mode.setdefault(run["mode"], []).append(run)
        by_workload_mode.setdefault(run["workload_id"], {}).setdefault(run["mode"], []).append(run)

    summary: dict[str, Any] = {
        "runtime": payload["runtime"],
        "pair_count": len(pairs),
        "pairs": {},
        "comparisons": {},
        "workloads": {},
        "modes": {},
        "mode_aggregates_are_descriptive_only": True,
    }

    comparison_groups: dict[str, list[dict[str, Any]]] = {}
    for pair_id, pair_runs in sorted(pairs.items()):
        first = pair_runs[0]
        primary = declared_primary_modes(specs[first["workload_id"]])
        comparison = pair_comparison(pair_runs, primary) if primary is not None else None
        summary["pairs"][pair_id] = {
            "workload_id": first["workload_id"],
            "repo_revision": first["repo_revision"],
            "repeat_index": first["repeat_index"],
            "modes": sorted(run["mode"] for run in pair_runs),
            "controls": {field: first[field] for field in PAIR_CONTROL_FIELDS},
            "comparison": comparison,
        }
        if comparison is not None:
            key = f"{first['workload_id']}:{comparison['baseline_mode']}->{comparison['candidate_mode']}"
            comparison_groups.setdefault(key, []).append(comparison)

    summary["comparisons"] = {
        key: aggregate_comparisons(items)
        for key, items in sorted(comparison_groups.items())
    }
    summary["workloads"] = {
        workload_id: {
            mode: mode_summary(runs)
            for mode, runs in sorted(mode_runs.items())
        }
        for workload_id, mode_runs in sorted(by_workload_mode.items())
    }
    summary["modes"] = {
        mode: mode_summary(runs)
        for mode, runs in sorted(by_mode.items())
    }
    return summary


def print_human(summary: dict[str, Any]) -> None:
    runtime = summary["runtime"]
    print(f"Runtime: {runtime['codex_version']} ({runtime['date']})")
    if runtime.get("observed_child_capacity") is not None:
        print(f"Observed child capacity: {runtime['observed_child_capacity']}")
    print(f"Pairs: {summary['pair_count']}")

    if summary["comparisons"]:
        print("\nPaired primary comparisons")
        for key, stats in summary["comparisons"].items():
            print(f"  {key}")
            print(f"    pairs: {stats['pair_count']}")
            print(f"    mean_success_delta: {stats['mean_success_delta']:.3f}")
            for field in COMPARISON_CLI_FIELDS:
                value = stats["mean_metric_deltas"][field]
                print(f"    delta_{field}: {'not_recorded' if value is None else round(value, 2)}")

    print("\nDescriptive mode aggregates (do not compare across workload mixes)")
    for mode, stats in summary["modes"].items():
        print(f"\n{mode}")
        print(f"  runs: {stats['runs']}")
        print(f"  success_rate: {stats['success_rate']:.3f}")
        mean_agent_count = stats["mean_agent_count"]
        print(f"  mean_agent_count: {'not_recorded' if mean_agent_count is None else f'{mean_agent_count:.2f}'}")
        for field in MODE_MEAN_CLI_KEYS:
            value = stats[field]
            print(f"  {field}: {'not_recorded' if value is None else round(value, 2)}")
        for field in [
            "runtime_slot_waits",
            "execution_stall_events",
            "clean_same_lane_restarts",
            "unjustified_retry_calls",
            "final_review_required_runs",
            "final_review_satisfied_runs",
            "final_review_unsatisfied_required_runs",
            "final_review_attempts",
            "review_artifact_verify_failures",
            "post_review_mutations",
        ]:
            print(f"  {field}: {stats[field]}")
        review_yield = stats["final_review_yield"]
        print(
            "  final_review_yield: "
            + ("not_recorded" if review_yield is None else f"{review_yield:.3f}")
        )


def main() -> None:
    args = parse_args()
    try:
        payload = json.loads(args.result.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        workloads = json.loads(WORKLOADS.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(str(exc))

    jsonschema.Draft202012Validator(schema).validate(payload)
    specs = workload_specs(workloads)
    unknown = sorted({run["workload_id"] for run in payload["runs"]} - set(specs))
    if unknown:
        fail(f"unknown workload ids: {', '.join(unknown)}")

    summary = build_summary(payload, specs)
    if args.json:
        json.dump(summary, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print_human(summary)


if __name__ == "__main__":
    main()
