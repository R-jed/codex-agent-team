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
            "codex_agent_team_reader",
            "codex_agent_team_worker",
            "codex_agent_team_investigator",
            "codex_agent_team_advisor",
            "one" if path.name == "README_EN.md" else "一个",
        ]:
            assert phrase in text


def test_readmes_explain_compatibility_ids_without_reverting_brand():
    zh = (ROOT / "README.md").read_text()
    en = (ROOT / "README_EN.md").read_text()
    assert "compatibility identifier" in en
    assert "兼容标识" in zh
    assert zh.startswith("# Codex Delegate")
    assert en.startswith("# Codex Delegate")


def test_readmes_do_not_expose_internal_release_handoff_as_user_guidance():
    forbidden = [
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
