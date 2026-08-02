from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "readme"

ZH_ASSETS = ["hero-zh.svg", "workflow-zh.svg", "roles-zh.svg"]
EN_ASSETS = ["hero.svg", "workflow.svg", "roles.svg"]


def load_svg(name: str) -> str:
    return (ASSET_DIR / name).read_text()


def test_readme_svgs_are_valid_indigo_porcelain_editorial_assets():
    for name in ZH_ASSETS + EN_ASSETS:
        path = ASSET_DIR / name
        ET.parse(path)
        svg = path.read_text()
        assert svg.lstrip().startswith("<svg")
        assert 'width="1200"' in svg
        assert "#0a1f3d" in svg
        assert "#f1f3f5" in svg
        assert "Playfair Display" in svg or "Noto Serif SC" in svg
        assert "Noto Sans SC" in svg or "Inter" in svg
        assert "<linearGradient" not in svg
        assert "<radialGradient" not in svg
        assert "<filter" not in svg
        assert "<foreignObject" not in svg


def test_readme_svg_text_is_large_enough_for_github_scaling():
    for name in ZH_ASSETS + EN_ASSETS:
        sizes = [int(value) for value in re.findall(r'font-size="(\d+)"', load_svg(name))]
        assert sizes
        assert min(sizes) >= 20, f"{name} contains text smaller than 20px: {min(sizes)}px"


def test_chinese_readme_svgs_are_localized():
    banned = [
        "ACT II",
        "ACT III",
        "TASK FLOW",
        "OPTIONAL JUDGMENT",
        "DECIDE",
        "EXECUTE",
        "REVIEW",
        "DELIVER",
        "FAIL CLOSED",
        "BOUNDED DELEGATION",
        "ROOT STAYS IN CONTROL",
    ]
    for name in ZH_ASSETS:
        svg = load_svg(name)
        assert re.search(r"[\u4e00-\u9fff]", svg)
        for phrase in banned:
            assert phrase not in svg, f"{name} contains English explanatory label: {phrase}"


def test_english_readme_svgs_remain_english_only():
    for name in EN_ASSETS:
        assert not re.search(r"[\u4e00-\u9fff]", load_svg(name))


def test_role_spread_preserves_control_hierarchy():
    for name in ["roles-zh.svg", "roles.svg"]:
        svg = load_svg(name)
        root_x = svg.index(">ROOT<")
        luna_x = svg.index(">LUNA<")
        terra_x = svg.index(">TERRA<")
        sol_x = svg.index(">SOL<")
        assert root_x < luna_x < terra_x < sol_x
        assert 'x="478" y="118" width="666" height="172"' in svg
