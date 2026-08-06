from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
ROUTER = SKILL / "references" / "router-core.md"
GUARDRAILS = SKILL / "references" / "guardrails.md"
COORDINATION_CASES = ROOT / "evals" / "coordination-cases.json"


def cases() -> dict[str, dict]:
    payload = json.loads(COORDINATION_CASES.read_text())
    assert payload["schema_version"] == "1.0"
    assert payload["suite"] == "codex-delegate-coordination-contract"
    return {case["id"]: case for case in payload["cases"]}


def test_upstream_workflow_ownership_is_preserved():
    router = ROUTER.read_text().lower()
    for phrase in [
        "preserve upstream workflow ownership",
        "treat those definitions as task truth",
        "does not silently create a competing domain plan",
        "reuse it as the coordination source of truth",
        "do not create a second persistent state source",
    ]:
        assert phrase in router

    case = cases()["upstream-workflow-remains-authoritative"]
    expected = case["expected"]
    assert expected["preserve_upstream_workflow"] is True
    assert set(expected["delegate_may_assign"]) == {
        "owner",
        "role",
        "concurrency",
        "write_isolation",
        "integration_timing",
    }
    assert {
        "goal",
        "decomposition",
        "stage_order",
        "dependencies",
        "required_outputs",
        "business_acceptance",
        "quality_gates",
    } <= set(expected["delegate_must_not_redefine"])
