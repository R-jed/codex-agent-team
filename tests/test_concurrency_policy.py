from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-agent-team"
SKILL = PLUGIN / "skills" / "codex-agent-team" / "SKILL.md"
ROUTING = PLUGIN / "skills" / "codex-agent-team" / "references" / "routing-policy.md"
CONSENT = PLUGIN / "skills" / "codex-agent-team" / "references" / "consent-policy.md"
SAFETY = PLUGIN / "skills" / "codex-agent-team" / "references" / "safety-policy.md"
CONTRACT = PLUGIN / "skills" / "codex-agent-team" / "references" / "delegation-contract.md"
PROGRESS = PLUGIN / "skills" / "codex-agent-team" / "references" / "execution-progress.md"
POLICY = PLUGIN / "policy-contract.json"


def policy() -> dict:
    return json.loads(POLICY.read_text())


def test_scheduler_has_no_product_hard_child_count():
    combined = SKILL.read_text() + ROUTING.read_text()
    for phrase in [
        "no product-level hard child count",
        "Dependency Ledger",
        "ready frontier",
        "smallest useful scheduling wave",
        "native runtime capacity",
    ]:
        assert phrase.lower() in combined.lower()
    for forbidden in ["hard maximum is 4", "hard max 4", "default child count is 1"]:
        assert forbidden.lower() not in combined.lower()


def test_two_children_is_consent_boundary_not_scheduler_ceiling():
    contract = policy()["delegation"]
    consent = CONSENT.read_text()
    routing = ROUTING.read_text()
    assert contract["baseline_concurrent_children"] == 2
    assert "consent boundary" in (consent + routing).lower()
    assert "not a total child lifetime limit" in routing.lower()
    assert "does not add another numerical hard ceiling" in consent.lower()
    assert "material compute expansion" in consent.lower()


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
    combined = SKILL.read_text() + CONTRACT.read_text()
    for phrase in [
        "Preserve unrelated existing edits",
        "Re-read affected files",
        "concurrent workspace drift",
        "File-level ownership promises do not authorize a second writing Worker",
    ]:
        assert phrase.lower() in combined.lower()


def test_same_checkout_writer_rule_is_workspace_scoped_not_global():
    contract = policy()["delegation"]
    combined = SKILL.read_text() + ROUTING.read_text() + SAFETY.read_text()
    assert contract["max_active_writers_per_workspace"] == 1
    assert "same physical checkout" in combined.lower()
    assert "independent workspaces may have independent writers" in combined.lower()
    assert "machine-wide" in combined.lower()
    assert "file-list promises inside one checkout are insufficient" in combined.lower()


def test_progress_recovery_has_no_universal_retry_count():
    combined = PROGRESS.read_text() + CONTRACT.read_text()
    for phrase in [
        "same failure signature",
        "clean restart",
        "Capability takes precedence over retry",
        "There is no universal retry count",
        "Do not repeat an unchanged contract after failure",
    ]:
        assert phrase.lower() in combined.lower()


def test_codex_home_concurrency_is_fail_closed_and_not_overclaimed():
    combined = SKILL.read_text() + ROUTING.read_text() + SAFETY.read_text()
    assert "mixed concurrent managed-profile generations are unsupported for v1.0.0" in combined.lower()
    assert "fails closed" in combined.lower()
    assert "concurrent same-codex-home installation remains a live release-validation gate" in combined.lower()
    assert "do not claim cross-session writer exclusion or multi-process installer safety" in combined.lower()
