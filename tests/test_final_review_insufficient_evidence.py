from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-agent-team"
GATE = PLUGIN / "skills" / "codex-agent-team" / "references" / "final-review-gate.md"
ADVISOR = PLUGIN / "agent-profiles" / "codex-agent-team-advisor.toml"
SCHEMA = ROOT / "evals" / "behavioral-result.schema.json"


def test_existing_advisor_can_fail_closed_on_missing_evidence():
    advisor = tomllib.loads(ADVISOR.read_text())
    instructions = advisor["developer_instructions"]
    assert "INSUFFICIENT_EVIDENCE" in instructions
    assert "missing dependency" in instructions


def test_final_review_gate_treats_insufficient_evidence_as_unresolved_not_ship():
    gate = GATE.read_text()
    assert "### `INSUFFICIENT_EVIDENCE`" in gate
    assert "not a successful final verdict" in gate
    assert "review_verdict = insufficient_evidence" in gate
    assert "launch a new fresh Sol review" in gate
    assert "do not report the Final Review Gate satisfied until the current artifact receives `ship`" in gate
    assert "Do not silently map missing evidence to `fix-first`" in gate


def test_behavioral_schema_can_record_insufficient_evidence_without_profile_migration():
    import json

    schema = json.loads(SCHEMA.read_text())
    verdicts = schema["properties"]["runs"]["items"]["properties"]["final_review_verdict"]["enum"]
    assert "insufficient_evidence" in verdicts
