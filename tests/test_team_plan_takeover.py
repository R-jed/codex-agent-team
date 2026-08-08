from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SCRIPT = SCRIPTS / "validate_team_plan.py"


def load_validator():
    scripts_dir = str(SCRIPTS)
    sys.path.insert(0, scripts_dir)
    try:
        spec = importlib.util.spec_from_file_location("subagents_dispatch_team_plan_takeover", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(scripts_dir)


VALIDATOR = load_validator()


def test_teamplan_role_main_is_rejected_because_takeover_is_recovery_state():
    payload = {
        "schema_version": "1.0",
        "revision": 1,
        "supersedes_revision": None,
        "planning_source": "ad_hoc",
        "source_refs": [],
        "root_goal": "deliver the verified requested result",
        "units": [
            {
                "unit_id": "U1",
                "role": "reader",
                "goal": "trace contract",
                "output": "evidence",
                "depends_on": [],
                "ownership": {"write": [], "forbidden": []},
                "done_when": "contract evidenced",
            },
            {
                "unit_id": "U2",
                "role": "main",
                "goal": "implement change",
                "output": "source change",
                "depends_on": ["U1"],
                "ownership": {"write": ["src/example.py"], "forbidden": []},
                "done_when": "acceptance passes",
            },
        ],
        "integration_owner": "main",
        "integration_order": ["U1", "U2"],
        "final_verification": "Main verifies the combined artifact",
        "revision_reason": "initial",
    }
    result = VALIDATOR.validate_team_plan_payload(payload)
    assert result["team_plan_valid"] is False
    assert "U2 has unsupported role" in result["errors"]
