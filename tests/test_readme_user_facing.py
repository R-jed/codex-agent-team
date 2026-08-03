from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READMES = [ROOT / "README.md", ROOT / "README_EN.md"]


def test_readmes_present_the_product_to_users():
    for path in READMES:
        text = path.read_text()
        for phrase in [
            "Codex Delegate",
            "codex plugin marketplace add R-jed/codex-agent-team --ref main",
            "/codex-delegate",
            "0.5.0",
            "Luna Reader",
            "Luna Worker",
            "Terra Investigator",
            "Sol Advisor",
        ]:
            assert phrase in text


def test_readmes_position_codex_delegate_as_a_native_delegation_layer():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "Codex Native Subagents 之上的委派策略层" in zh
    assert "A delegation policy layer over Codex Native Subagents" in en
    assert "委派框架" not in zh
    assert "delegation framework" not in en.lower()


def test_readmes_explain_adaptive_concurrency_without_hard_agent_count():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()

    for text in [zh, en]:
        assert "physical checkout" in text
        assert "0.5.0" in text
        assert "0.3.x" not in text or "0.5" in text

    assert "没有固定 Agent 数量" in zh
    assert "No fixed Agent count" in en
    assert "最多两个同时活跃" in zh
    assert "up to two concurrently active" in en
    assert "runtime" in zh.lower() and "runtime" in en.lower()

    for forbidden in [
        "默认：1 个",
        "一般最多：2 个",
        "硬上限：4 个",
        "default: 1",
        "normal maximum: 2",
        "hard maximum: 4",
    ]:
        assert forbidden not in zh
        assert forbidden not in en


def test_readmes_explain_evidence_guided_recovery():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "卡住时如何处理" in zh
    assert "What happens when execution stalls" in en
    assert "固定重试次数" in zh
    assert "fixed retry count" in en
    assert "Terra" in zh and "Terra" in en


def test_readmes_explain_compatibility_ids_without_reverting_brand():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "兼容标识" in zh
    assert "compatibility identifiers" in en
    zh_lines = zh.split("\n")[0:15]
    en_lines = en.split("\n")[0:15]
    assert any("Codex Delegate" in line for line in zh_lines)
    assert any("Codex Delegate" in line for line in en_lines)


def test_readmes_remain_user_facing():
    forbidden = [
        "```mermaid",
        "HEADOFF.md",
        "LOCAL_VALIDATION_REPORT.md",
        "Checkpoint 1",
        "Checkpoint 5",
        "P0/P1",
        "CAT-LOCAL-001",
        "branch audit",
        "static closure",
        "Dependency Ledger status",
        "本地真测交接",
        "远端分支清理",
        "静态收口",
    ]
    for path in READMES:
        text = path.read_text()
        for phrase in forbidden:
            assert phrase not in text
        lines = text.splitlines()
        for line in lines:
            if "<img" in line and "logo" not in line and "shields.io" not in line:
                assert False, f"Non-logo/shields <img> found: {line}"
        if "<picture" in text:
            assert "logo" in text
