from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_transient_local_agent_review_and_handoff_artifacts_are_not_packaged():
    forbidden_markers = {
        "deep-review-report",
        "release-candidate-closure",
        "local-validation",
        "handoff-progress",
        "headoff",
    }
    candidates = [ROOT, ROOT / "docs"]
    offenders: list[str] = []
    for base in candidates:
        for path in base.iterdir():
            if not path.is_file():
                continue
            lowered = path.name.lower()
            if any(marker in lowered for marker in forbidden_markers):
                offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], f"transient local-agent artifacts must stay out of the repository: {offenders}"
