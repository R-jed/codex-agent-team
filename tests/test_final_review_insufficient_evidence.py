from pathlib import Path
import json
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
ADVISOR = PLUGIN / "agent-profiles" / "codex-delegate-advisor.toml"
GATE = PLUGIN / "skills" / "codex-delegate" / "references" / "final-review-gate.md"
SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"


def test_advisor_can_fail_closed_on_missing_evidence():
    instructions = tomllib.loads(ADVISOR.read_text())["developer_instructions"]
    assert "INSUFFICIENT_EVIDENCE" in instructions
    assert "missing dependency" in instructions


def test_gate_keeps_insufficient_evidence_unresolved():
    gate = GATE.read_text()
    assert "INSUFFICIENT_EVIDENCE" in gate
    assert "unresolved" in gate.lower()
    assert "not `fix-first`" in gate
    assert "current artifact receives `ship`" in gate


def test_behavioral_schema_records_insufficient_evidence():
    schema = json.loads(SCHEMA.read_text())
    verdicts = schema["properties"]["runs"]["items"]["properties"]["final_review_verdict"]["enum"]
    assert "insufficient_evidence" in verdicts
