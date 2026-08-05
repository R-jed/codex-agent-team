from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL = PLUGIN / "skills" / "codex-delegate"
ROUTER = SKILL / "references" / "router-core.md"
GUARDRAILS = SKILL / "references" / "guardrails.md"
POLICY = PLUGIN / "policy-contract.json"


def policy():
    return json.loads(POLICY.read_text())


def test_scheduler_is_completion_driven_without_product_hard_child_count():
    text = (ROUTER.read_text() + (SKILL / "SKILL.md").read_text()).lower()
    for phrase in ["smallest useful safe set", "completion", "native capacity", "without waiting"]:
        assert phrase in text
    assert "fixed team" not in text


def test_two_children_is_consent_envelope_not_scheduler_target():
    assert policy()["delegation"]["baseline_concurrent_children"] == 2
    text = (GUARDRAILS.read_text() + ROUTER.read_text()).lower()
    assert "up to 2 concurrently active justified children" in text
    assert "envelope, not a target" in text


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
    guardrails = GUARDRAILS.read_text().lower()
    assert delegation["max_active_writers_per_workspace"] == 1
    assert delegation["max_depth"] == 1
    assert "one canonical physical checkout has at most one active writing actor" in guardrails
    assert "main session when mutating the checkout" in guardrails
    assert "luna worker" in guardrails
    assert "sol solver" in guardrails
    assert "genuine filesystem isolation" in guardrails
    assert "delegation depth is one" in guardrails


def test_stalled_lane_has_one_clean_retry_not_universal_retry_loop():
    router = ROUTER.read_text().lower()
    assert "stalled" in router
    assert "at most one clean retry" in router
    assert "materially improved packet" in router
    assert "failed luna attempt never directly means" in router


def test_codex_home_concurrency_remains_release_validation_boundary():
    guardrails = GUARDRAILS.read_text().lower()
    installation = (ROOT / "docs" / "plugin-installation.md").read_text().lower()
    assert "cross-session locking" in guardrails
    assert "concurrent same-codex-home multi-process behavior remains a release-validation concern" in installation
