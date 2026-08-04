from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "evals" / "LOCAL_EVAL_FIXTURE_TEMPLATE.md"
EVAL_DOC = ROOT / "docs" / "behavioral-evals.md"


def test_local_eval_fixture_freezes_causal_controls():
    text = TEMPLATE.read_text()
    for field in [
        "workload_definition_hash",
        "base_revision",
        "exact_user_prompt",
        "starting_state",
        "acceptance_rubric_id",
        "allowed_verification",
        "main_session_route",
        "worker_route",
        "permissions_fingerprint",
        "tool_surface_fingerprint",
        "codex_runtime_version",
    ]:
        assert field in text
    assert "Freeze this definition before the first run in a pair" in text
    assert "create a new fixture version, pair id, and workload-definition hash" in text


def test_behavioral_eval_protocol_requires_frozen_executable_fixture():
    text = EVAL_DOC.read_text()
    assert "Freeze the executable workload" in text
    assert "exact user prompt bytes" in text
    assert "workload_definition_hash" in text
    assert "worker_route" in text
    assert "If a controlled input changes, create a new pair id and hash" in text
