from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "evals" / "README.md"


def test_eval_index_links_current_measurement_artifacts():
    text = INDEX.read_text()
    for name in [
        "behavioral-workloads.json",
        "behavioral-result.schema.json",
        "LOCAL_EVAL_FIXTURE_TEMPLATE.md",
        "routing-cases.json",
        "coordination-cases.json",
        "runtime-assurance-cases.json",
        "../docs/behavioral-evals.md",
    ]:
        assert name in text
