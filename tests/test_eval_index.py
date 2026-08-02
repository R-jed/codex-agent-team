from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "evals" / "README.md"


def test_eval_index_links_reproducible_live_artifacts():
    text = INDEX.read_text()
    for name in [
        "behavioral-workloads.json",
        "behavioral-result.schema.json",
        "LOCAL_EVAL_FIXTURE_TEMPLATE.md",
        "routing-cases.json",
        "runtime-assurance-cases.json",
        "../HEADOFF.md",
    ]:
        assert name in text
