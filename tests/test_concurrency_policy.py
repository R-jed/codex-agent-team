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
    for phrase in [
        "smallest useful active set",
        "ready frontier",
        "progressive fan-out",
        "native codex capacity",
        "process an exposed child completion",
        "artificial wave barrier",
    ]:
        assert phrase in text
    assert "fixed team size" in text
    assert "ordinary numeric child ceiling" in text


def test_machine_contract_keeps_only_hard_delegation_limits():
    delegation = policy()["delegation"]
    assert delegation == {
        "max_depth": 1,
        "max_active_writers_per_workspace": 1,
    }
    assert "baseline_concurrent_children" not in delegation
    assert "max_concurrent_children" not in delegation


def test_static_eval_allows_parallel_readers_and_cost_based_consent():
    payload = json.loads((ROOT / "evals" / "routing-cases.json").read_text())
    by_id = {case["id"]: case for case in payload["evals"]}

    parallel = by_id["three-independent-readers-can-fanout"]
    assert parallel["expected"]["action"] == "delegate"
    assert len(parallel["expected"]["nodes"]) == 3
    assert all(node["agent_type"] == "codex_delegate_reader" for node in parallel["expected"]["nodes"])

    consent = by_id["material-compute-expansion-needs-consent"]
    assert consent["expected"]["action"] == "ask_consent"
    assert consent["expected"]["consent_reason"] == "material_compute_expansion"


def test_guardrails_prevent_agent_sprawl_without_count_threshold():
    text = GUARDRAILS.read_text().lower()
    for phrase in [
        "native capacity is a ceiling, never a reason to fill slots",
        "another active owner already covers the same unchanged responsibility",
        "the work is speculative",
        "child count by itself is not a consent trigger",
        "materially expanding",
    ]:
        assert phrase in text
    assert "more than two simultaneous children" not in text


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


def test_installer_lock_is_separate_from_session_level_scheduler_claims():
    guardrails = GUARDRAILS.read_text().lower()
    installation = (ROOT / "docs" / "plugin-installation.md").read_text().lower()
    assert "cross-session locking" in guardrails
    assert "persistent installer lock serializes installers targeting the same codex home" in installation
    assert "one failed rollback cannot erase a successful peer" in installation
