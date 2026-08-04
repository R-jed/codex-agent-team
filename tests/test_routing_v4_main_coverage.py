from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
POLICY = PLUGIN / "policy-contract.json"
VERIFIER = PLUGIN / "scripts" / "runtime-evidence.py"


def run_main(model: str | None = None, effort: str | None = None) -> dict:
    native = {}
    if model is not None:
        native["model"] = model
    if effort is not None:
        native["effort"] = effort
    payload = {"subject": "main_session", "native": native or None}
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_policy_owns_main_coverage_reference_model_and_effort_order():
    policy = json.loads(POLICY.read_text())
    classification = policy["classification"]
    role = classification["main_coverage_reference_role"]
    reference = policy["roles"][role]
    order = classification["reasoning_effort_order"]

    assert role == "solver"
    assert reference["model"] == "gpt-5.6-sol"
    assert reference["effort"] == "high"
    assert order.index("medium") < order.index("high") < order.index("xhigh") < order.index("max")


def test_main_coverage_requires_reference_model_and_sufficient_effort():
    assert run_main("gpt-5.6-sol", "high")["main_judgment_coverage"] == "covered"
    assert run_main("gpt-5.6-sol", "xhigh")["main_judgment_coverage"] == "covered"
    assert run_main("gpt-5.6-sol", "max")["main_judgment_coverage"] == "covered"

    assert run_main("gpt-5.6-sol", "medium")["main_judgment_coverage"] == "uncovered"
    assert run_main("gpt-5.6-sol", "low")["main_judgment_coverage"] == "uncovered"
    assert run_main("gpt-5.6-luna", "max")["main_judgment_coverage"] == "uncovered"


def test_unknown_effort_on_matching_model_does_not_suppress_sol_uplift():
    data = run_main("gpt-5.6-sol", "future-effort")
    assert data["main_judgment_coverage"] == "unknown"
    assert data["coverage_reference_model"] == "gpt-5.6-sol"
    assert data["coverage_reference_effort"] == "high"


def test_partial_main_route_remains_unknown():
    assert run_main("gpt-5.6-sol", None)["main_judgment_coverage"] == "unknown"
