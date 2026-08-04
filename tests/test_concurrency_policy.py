from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-delegate"
SKILL_ROOT = PLUGIN / "skills" / "codex-delegate"
SKILL = SKILL_ROOT / "SKILL.md"
ROUTING = SKILL_ROOT / "references" / "routing-policy.md"
CONSENT = SKILL_ROOT / "references" / "consent-policy.md"
SAFETY = SKILL_ROOT / "references" / "safety-policy.md"
CONTRACT = SKILL_ROOT / "references" / "delegation-contract.md"
PROGRESS = SKILL_ROOT / "references" / "execution-progress.md"
POLICY = PLUGIN / "policy-contract.json"


def policy() -> dict:
    return json.loads(POLICY.read_text())


def test_scheduler_has_no_product_hard_child_count_and_is_completion_driven():
    routing = ROUTING.read_text().lower()
    skill = SKILL.read_text().lower()
    for phrase in [
        "no product-level hard child count",
        "dependency ledger",
        "ready frontier",
        "completion-driven",
        "native capacity",
        "refill",
    ]:
        assert phrase in routing + skill
    for forbidden in ["hard maximum is 4", "hard max 4", "default child count is 1"]:
        assert forbidden not in routing + skill


def test_two_children_is_consent_boundary_not_scheduler_ceiling():
    delegation = policy()["delegation"]
    consent = CONSENT.read_text().lower()
    routing = ROUTING.read_text().lower()
    assert delegation["baseline_concurrent_children"] == 2
    assert "consent boundary" in consent + routing
    assert "lifetime child limit" in routing
    assert "does not add another numerical hard ceiling" in consent
    assert "material compute expansion" in consent


def test_authorized_static_eval_can_exceed_four_readers():
    payload = json.loads((ROOT / "evals/routing-cases.json").read_text())
    case = next(item for item in payload["evals"] if item["id"] == "five-independent-readers-authorized")
    assert case["expected"]["action"] == "delegate"
    assert len(case["expected"]["nodes"]) == 5
    assert len({node["dependency_id"] for node in case["expected"]["nodes"]}) == 5
    assert all(node["write_intent"] is False for node in case["expected"]["nodes"])


def test_runtime_slot_pressure_queues_without_cross_routing():
    payload = json.loads((ROOT / "evals/routing-cases.json").read_text())
    case = next(item for item in payload["evals"] if item["id"] == "runtime-slot-pressure-queues-ready-work")
    assert case["expected"]["action"] == "queue"
    assert len(case["expected"]["nodes"]) == 3
    assert case["expected"]["queued_dependencies"] == ["D04", "D05"]
    assert all(node["model"] == policy()["roles"]["reader"]["model"] for node in case["expected"]["nodes"])


def test_worker_contract_is_concurrent_change_aware():
    contract = CONTRACT.read_text().lower()
    for phrase in [
        "preserve unrelated existing edits",
        "re-read affected state",
        "workspace drift",
        "file-level ownership promises do not authorize a second writing worker",
    ]:
        assert phrase in contract


def test_same_checkout_writer_rule_is_workspace_scoped_not_global():
    delegation = policy()["delegation"]
    safety = SAFETY.read_text().lower()
    routing = ROUTING.read_text().lower()
    assert delegation["max_active_writers_per_workspace"] == 1
    assert "one canonical shared workspace has at most one active writing worker" in safety
    assert "multiple writers require actual filesystem isolation" in safety
    assert "isolated runtime-backed worktrees/workspaces/repositories" in routing
    assert "machine-wide" not in routing


def test_progress_recovery_has_no_universal_retry_count():
    progress = PROGRESS.read_text().lower()
    contract = CONTRACT.read_text().lower()
    assert "same failure signature" in progress
    assert "clean restart" in progress
    assert "capability takes precedence over retry" in progress
    assert "does not define a universal retry count" in progress
    assert "do not resend an unchanged contract after failure" in contract


def test_codex_home_and_cross_session_claims_remain_evidence_bounded():
    skill = SKILL.read_text().lower()
    safety = SAFETY.read_text().lower()
    assert "mixed concurrent managed-profile generations are unsupported for v1" in skill
    assert "concurrent same-codex-home installation remains a live release-validation gate" in safety
    assert "current session-local orchestration must not be presented as cross-session exclusion" in safety
    assert "add inter-process locking only after a reproducible failure" in safety
