from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "evals" / "LOCAL_EVAL_FIXTURE_TEMPLATE.md"
EVAL_DOC = ROOT / "docs" / "behavioral-evals.md"


def test_local_eval_fixture_freezes_causal_controls_and_strategy_variable():
    text = TEMPLATE.read_text(encoding="utf-8")
    for field in [
        "workload_definition_hash",
        "base_revision",
        "exact_user_prompt",
        "starting_state",
        "acceptance_rubric_id",
        "allowed_verification",
        "main_session_route",
        "main_judgment_coverage",
        "permissions_fingerprint",
        "tool_surface_fingerprint",
        "codex_runtime_version",
        "baseline_mode",
        "baseline_execution_route",
        "candidate_mode",
        "candidate_execution_route",
    ]:
        assert field in text
    assert "Freeze this definition before the first run in a pair" in text
    assert "create a new fixture version, pair id, and workload-definition hash" in text
    assert "Missing runtime telemetry remains missing" in text


def test_behavioral_eval_protocol_keeps_controls_distinct_from_execution_strategy():
    text = EVAL_DOC.read_text(encoding="utf-8")
    assert "Freeze controlled inputs" in text
    assert "exact user prompt bytes" in text
    assert "workload_definition_hash" in text
    assert "execution_route" in text
    assert "experimental variable" in text
    assert "measurement surface" in text
