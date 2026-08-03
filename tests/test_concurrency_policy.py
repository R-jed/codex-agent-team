from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/SKILL.md"
ROUTING = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/routing-policy.md"
SAFETY = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/safety-policy.md"
CONTRACT = ROOT / "plugins/codex-agent-team/skills/codex-agent-team/references/delegation-contract.md"


def test_concurrency_scopes_are_distinct_and_v1_limits_stay_frozen():
    skill = SKILL.read_text()
    routing = ROUTING.read_text()

    for phrase in [
        "normal maximum is 2, hard maximum is 4",
        "Child-count limits are per main session",
        "workspace scope",
        "Codex-home scope",
        "not a machine-wide or account-wide concurrency limit",
        "one active writing Worker per canonical workspace",
    ]:
        assert phrase in skill or phrase in routing


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
        "Do not create a global Agent cap that blocks independent projects",
        "File-level promises inside one shared checkout are insufficient",
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
