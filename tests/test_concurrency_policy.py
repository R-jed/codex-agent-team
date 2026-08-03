from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/SKILL.md"
ROUTING = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/routing-policy.md"
CONSENT = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/consent-policy.md"
SAFETY = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/safety-policy.md"
CONTRACT = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/delegation-contract.md"
PROGRESS = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/execution-progress.md"


def test_scheduler_has_no_product_hard_child_count():
    skill = SKILL.read_text()
    routing = ROUTING.read_text()
    combined = skill + routing

    for phrase in [
        "no product-level hard child count",
        "Dependency Ledger",
        "ready frontier",
        "smallest useful scheduling wave",
        "native runtime capacity",
    ]:
        assert phrase.lower() in combined.lower()

    for forbidden in [
        "hard maximum is 4",
        "hard maximum: 4",
        "hard max 4",
        "default child count is 1",
    ]:
        assert forbidden.lower() not in combined.lower()


def test_two_children_is_consent_boundary_not_scheduler_ceiling():
    consent = CONSENT.read_text()
    routing = ROUTING.read_text()
    combined = consent + routing

    for phrase in [
        "up to 2 concurrently active justified child Agents",
        "consent boundary",
        "not a total child lifetime limit",
        "does not add another numerical hard ceiling",
        "material compute expansion",
    ]:
        assert phrase.lower() in combined.lower()


def test_authorized_static_eval_can_exceed_four_readers():
    import json

    payload = json.loads((ROOT / "evals/routing-cases.json").read_text())
    case = next(item for item in payload["evals"] if item["id"] == "five-independent-readers-authorized")
    assert case["expected"]["action"] == "delegate"
    assert len(case["expected"]["nodes"]) == 5
    assert len({node["dependency_id"] for node in case["expected"]["nodes"]}) == 5
    assert all(node["write_intent"] is False for node in case["expected"]["nodes"])


def test_runtime_slot_pressure_queues_without_cross_routing():
    import json

    payload = json.loads((ROOT / "evals/routing-cases.json").read_text())
    case = next(item for item in payload["evals"] if item["id"] == "runtime-slot-pressure-queues-ready-work")
    assert case["expected"]["action"] == "queue"
    assert len(case["expected"]["nodes"]) == 3
    assert case["expected"]["queued_dependencies"] == ["D04", "D05"]
    assert all(node["model"] == "gpt-5.6-luna" for node in case["expected"]["nodes"])


def test_worker_contract_is_concurrent_change_aware():
    skill = SKILL.read_text()
    contract = CONTRACT.read_text()

    for phrase in [
        "Preserve unrelated existing edits",
        "Re-read affected files",
        "concurrent workspace drift",
        "File-level ownership promises do not authorize a second writing Worker",
    ]:
        assert phrase.lower() in (skill + contract).lower()


def test_same_checkout_writer_rule_does_not_create_a_global_writer_mutex():
    skill = SKILL.read_text()
    routing = ROUTING.read_text()
    safety = SAFETY.read_text()
    combined = skill + routing + safety

    for phrase in [
        "same physical checkout",
        "independent workspaces may have independent writers",
        "machine-wide",
        "File-level promises inside one shared checkout are insufficient",
    ]:
        assert phrase.lower() in combined.lower()


def test_progress_recovery_has_no_universal_retry_count():
    progress = PROGRESS.read_text()
    contract = CONTRACT.read_text()
    combined = progress + contract

    for phrase in [
        "same failure signature",
        "clean restart",
        "Capability takes precedence over retry",
        "There is no universal retry count",
        "Do not repeat an unchanged contract after failure",
    ]:
        assert phrase.lower() in combined.lower()


def test_codex_home_concurrency_is_fail_closed_and_not_overclaimed():
    skill = SKILL.read_text()
    routing = ROUTING.read_text()
    safety = SAFETY.read_text()

    combined = skill + routing + safety
    for phrase in [
        "Mixed concurrent profile generations are unsupported for v1.0.0",
        "fails closed",
        "Concurrent same-Codex-home install behavior is a release-validation gate",
        "Do not claim cross-session writer exclusion or multi-process installer safety",
    ]:
        assert phrase.lower() in combined.lower()
