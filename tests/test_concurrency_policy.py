from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
ROUTING = SKILL / "references" / "routing-policy.md"
CONSENT = SKILL / "references" / "consent-policy.md"
SAFETY = SKILL / "references" / "safety-policy.md"
PROGRESS = SKILL / "references" / "execution-progress.md"
POLICY = PLUGIN / "policy-contract.json"


def policy():
    return json.loads(POLICY.read_text())


def test_scheduler_is_completion_driven_without_product_hard_child_count():
    text = (ROUTING.read_text() + (SKILL / "SKILL.md").read_text()).lower()
    for phrase in ["no product-level hard child count", "ready frontier", "completion-driven", "native capacity", "refill"]:
        assert phrase in text


def test_two_children_is_consent_envelope_not_scheduler_ceiling():
    assert policy()["delegation"]["baseline_concurrent_children"] == 2
    combined = (CONSENT.read_text() + ROUTING.read_text()).lower()
    assert "up to 2 concurrently active justified" in combined
    assert "consent envelope" in combined
    assert "no second product numerical ceiling" in combined or "does not add another numerical hard ceiling" in combined


def test_authorized_static_eval_can_exceed_four_readers_and_slot_pressure_queues():
    payload = json.loads((ROOT / "evals" / "routing-cases.json").read_text())
    by_id = {case["id"]: case for case in payload["evals"]}
    fanout = by_id["five-independent-readers-authorized"]
    assert len(fanout["expected"]["nodes"]) == 5
    assert all(node["agent_type"] == "codex_delegate_reader" for node in fanout["expected"]["nodes"])
    queued = by_id["runtime-slot-pressure-queues-ready-work"]
    assert queued["expected"]["action"] == "queue"
    assert queued["expected"]["queued_dependencies"] == ["D04", "D05"]


def test_writer_safety_is_workspace_scoped_and_depth_one():
    delegation = policy()["delegation"]
    safety = SAFETY.read_text().lower()
    routing = ROUTING.read_text().lower()
    assert delegation["max_active_writers_per_workspace"] == 1
    assert delegation["max_depth"] == 1
    assert "one canonical shared workspace has at most one active writing worker" in safety
    assert "filesystem isolation" in safety
    assert "isolated runtime-backed worktrees/workspaces/repositories" in routing
    assert "delegation depth remains one" in routing


def test_progress_recovery_has_no_universal_retry_count():
    progress = PROGRESS.read_text().lower()
    assert "same failure signature" in progress
    assert "clean restart" in progress
    assert "capability takes precedence over retry" in progress
    assert "does not define a universal retry count" in progress


def test_codex_home_generation_and_installer_concurrency_remain_fail_closed():
    skill = (SKILL / "SKILL.md").read_text().lower()
    safety = SAFETY.read_text().lower()
    assert "mixed concurrent managed-profile generations are unsupported for v1" in skill
    assert "concurrent same-codex-home installer behavior remains a live release-validation gate" in safety
    assert "historical `codex_agent_team_*` names are migration inputs only" in safety
