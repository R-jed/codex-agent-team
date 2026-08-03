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
            "0.4.0",
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


def test_readmes_explain_current_delegation_and_concurrency_contract():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()

    for text in [zh, en]:
        assert "default: 1" in text or "默认：1 个" in text
        assert "normal maximum: 2" in text or "一般最多：2 个" in text
        assert "hard maximum: 4" in text or "硬上限：4 个" in text
        assert "physical checkout" in text
        assert "0.3.x" in text and "0.4.x" in text

    assert "跨独立主会话" in zh
    assert "independent main sessions" in en
    assert "机器或账号的全局 Agent 上限" in zh
    assert "machine-wide or account-wide Agent cap" in en


def test_readmes_explain_compatibility_ids_without_reverting_brand():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "compatibility identifiers" in en
    assert "兼容标识" in zh
    assert zh.startswith("# Codex Delegate")
    assert en.startswith("# Codex Delegate")


def test_readmes_remain_text_first_and_user_facing():
    forbidden = [
        "<img",
        "<picture",
        "shields.io",
        "```mermaid",
        "HEADOFF.md",
        "LOCAL_VALIDATION_REPORT.md",
        "Checkpoint 1",
        "Checkpoint 5",
        "P0/P1",
        "CAT-LOCAL-001",
        "branch audit",
        "static closure",
        "本地真测交接",
        "远端分支清理",
        "静态收口",
    ]
    for path in READMES:
        text = path.read_text()
        for phrase in forbidden:
            assert phrase not in text
