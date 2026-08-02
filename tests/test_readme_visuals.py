from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "readme"

ZH_ASSETS = ["hero-zh.svg", "example-zh.svg", "operating-model-zh.svg"]
EN_ASSETS = ["hero.svg", "example.svg", "operating-model.svg"]
ALL_ASSETS = ZH_ASSETS + EN_ASSETS


def load_svg(name: str) -> str:
    return (ASSET_DIR / name).read_text()


def test_readme_svgs_are_valid_local_assets_without_effect_filters():
    for name in ALL_ASSETS:
        path = ASSET_DIR / name
        ET.parse(path)
        svg = path.read_text()
        assert svg.lstrip().startswith("<svg")
        assert 'width="1200"' in svg
        assert "<linearGradient" not in svg
        assert "<radialGradient" not in svg
        assert "<filter" not in svg
        assert "<foreignObject" not in svg
        assert not re.search(r"\broot\b", svg, re.I)


def test_readme_svgs_share_one_codex_agent_team_brand_system():
    retired_palette = ["#29473a", "#17251f", "#f2ede3"]
    retired_type = ["Playfair Display", "Noto Serif SC", "Songti SC"]
    for name in ALL_ASSETS:
        svg = load_svg(name)
        assert "#002FA7" in svg
        assert "#0a0a0a" in svg
        for value in retired_palette + retired_type:
            assert value not in svg, f"{name} still carries the retired mixed visual system: {value}"


def test_readme_svg_text_is_large_and_sparse_enough_for_github_scaling():
    for name in ALL_ASSETS:
        svg = load_svg(name)
        sizes = [int(value) for value in re.findall(r'font-size="(\d+)"', svg)]
        assert sizes
        assert min(sizes) >= 28, f"{name} contains text smaller than 28px: {min(sizes)}px"
        assert svg.count("<text ") <= 24, f"{name} is too text-dense for a README visual"


def test_chinese_readme_svgs_are_localized():
    for name in ZH_ASSETS:
        svg = load_svg(name)
        assert re.search(r"[\u4e00-\u9fff]", svg)
        assert "MAIN SESSION" not in svg
        assert "OPERATING MODEL" not in svg


def test_english_readme_svgs_remain_english_only():
    for name in EN_ASSETS:
        assert not re.search(r"[\u4e00-\u9fff]", load_svg(name))


def test_hero_keeps_only_product_relationship_not_low_level_policy():
    zh = load_svg("hero-zh.svg")
    en = load_svg("hero.svg")
    assert "主会话负责全局" in zh
    assert "子代理只接局部任务" in zh
    assert "The main session owns the task." in en
    assert "Subagents own bounded work." in en
    for svg in [zh, en]:
        for term in ["Writing Worker", "reasoning effort", "runtime evidence", "GPT-5.6"]:
            assert term not in svg


def test_task_example_is_concrete_without_pinning_model_configuration():
    zh = load_svg("example-zh.svg")
    en = load_svg("example.svg")
    assert "支付回调" in zh
    assert "LUNA" in zh and "TERRA" in zh
    assert "PAYMENT CALLBACK" in en
    assert "LUNA" in en and "TERRA" in en
    assert "GPT-5.6" not in zh
    assert "GPT-5.6" not in en


def test_operating_model_shows_one_main_session_and_optional_specialists():
    zh = load_svg("operating-model-zh.svg")
    en = load_svg("operating-model.svg")

    assert zh.count("主会话") >= 3
    assert "LUNA" in zh and "TERRA" in zh and "SOL" in zh
    assert "没有触发，就留在主会话" in zh
    assert "小而明确的任务：主会话直接完成" in zh

    assert en.count("MAIN SESSION") >= 2
    assert "LUNA" in en and "TERRA" in en and "SOL" in en
    assert "Without one, the work stays in the main session." in en
    assert "Small, isolated work stays in the main session." in en
