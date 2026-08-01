from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "readme"

ZH_ASSETS = ["hero-zh.svg", "workflow-zh.svg", "roles-zh.svg"]
EN_ASSETS = ["hero.svg", "workflow.svg", "roles.svg"]
ALLOWED_COLORS = {
    "#fafaf8",
    "#0a0a0a",
    "#f0f0ee",
    "#d4d4d2",
    "#737373",
    "#002fa7",
    "#ffffff",
}


def load_svg(name):
    return (ASSET_DIR / name).read_text()


def test_readme_svg_style_b_contract():
    for name in ZH_ASSETS + EN_ASSETS:
        svg = load_svg(name)
        assert svg.lstrip().startswith("<svg")
        assert 'width="1600"' in svg
        assert "#002FA7" in svg

        forbidden = [
            "<linearGradient",
            "<radialGradient",
            "<filter",
            "<foreignObject",
            ' rx="',
            ' ry="',
        ]
        for token in forbidden:
            assert token not in svg

        colors = {value.lower() for value in re.findall(r"#[0-9A-Fa-f]{6}", svg)}
        assert colors <= ALLOWED_COLORS

        font_sizes = [int(value) for value in re.findall(r'font-size="(\d+)"', svg)]
        assert font_sizes
        assert min(font_sizes) >= 22


def test_readme_svg_language_localization():
    for name in ZH_ASSETS:
        svg = load_svg(name)
        assert re.search(r"[\u4e00-\u9fff]", svg)

    for name in EN_ASSETS:
        svg = load_svg(name)
        assert not re.search(r"[\u4e00-\u9fff]", svg)


def test_workflow_keeps_sol_as_optional_consultation():
    zh = load_svg("workflow-zh.svg")
    en = load_svg("workflow.svg")
    assert "可选 · 经用户授权" in zh
    assert "OPTIONAL · WITH CONSENT" in en
    assert 'stroke-dasharray="10 10"' in zh
    assert 'stroke-dasharray="10 10"' in en


def test_roles_visualizes_root_as_control_plane():
    zh = load_svg("roles-zh.svg")
    en = load_svg("roles.svg")
    assert "控制平面 + 委派角色" in zh
    assert "CONTROL PLANE + DELEGATED ROLES" in en
    assert 'x="80" y="144" width="439" height="396"' in zh
    assert 'x="80" y="144" width="439" height="396"' in en
