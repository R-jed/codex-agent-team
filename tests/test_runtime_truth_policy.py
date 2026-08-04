from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-agent-team"
SKILL = PLUGIN / "skills" / "codex-agent-team"


def test_runtime_evidence_is_typed_and_partial_observation_is_not_proof():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    for field in ["route_evidence", "ancestry_evidence", "permission_evidence"]:
        assert field in runtime
    assert "partial" in runtime
    assert "A partial record never earns `L1`, `R1`, or `R2`" in runtime
    assert "corroborating evidence" in runtime


def test_compact_grades_remain_derived_compatibility_summaries():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    for grade in [
        "C1_configuration_only",
        "L1_local_record_observed",
        "R1_runtime_reported",
        "R2_runtime_reported_and_local_record_agree",
        "X0_conflicted",
    ]:
        assert grade in runtime
    assert "compact compatibility grade" in runtime


def test_profile_locked_is_the_only_route_assurance_path():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    route = (ROOT / "docs" / "model-route-assurance.md").read_text()
    assert "profile_locked" in runtime and "profile_locked" in route
    assert "native_explicit_validated" not in runtime
    assert "native_explicit_validated" not in route
    assert "No Portable Mode" in route


def test_normalized_verifier_is_wired_into_skill_and_runtime_reference():
    verifier = PLUGIN / "scripts" / "runtime-evidence.py"
    assert verifier.is_file()
    for path in [SKILL / "SKILL.md", SKILL / "references" / "runtime-assurance.md"]:
        text = path.read_text()
        assert "runtime-evidence.py" in text
        assert "verify-runtime.py" not in text
    assert not (SKILL / "scripts" / "inspect-runtime.py").exists()


def test_depth_one_preserves_not_observed_state():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    assert "absence remains `not_observed`" in runtime
    assert "parent_thread_id" in safety


def test_consent_policy_defines_resource_envelope_not_fixed_team_shape():
    consent = (SKILL / "references" / "consent-policy.md").read_text()
    assert "up to 2 concurrently active justified child Agents" in consent
    assert "at most 1 active writer" in consent
    assert "The exact team shape is dynamic" in consent
    assert "lifetime number of child calls" in consent
    assert "does not add another numerical hard ceiling" in consent


def test_live_evals_are_controlled_paired_runs_and_track_correction_cost():
    docs = (ROOT / "docs" / "behavioral-evals.md").read_text()
    workloads = (ROOT / "evals" / "behavioral-workloads.json").read_text()
    assert "controlled live runs" in docs
    assert "Pairing rules" in docs
    assert "Main-session correction cost" in docs
    assert "raw_prompt_luna" in docs
    assert "contract_luna_selective_sol" in docs
    assert "contract_luna_final_review_gate" in docs
    assert "Adaptive scheduling experiment" in docs
    assert "Intervention / clean-restart experiment" in docs
    assert "no claimed benchmark results" in workloads


def test_plugin_profile_lifecycle_remains_present():
    assert (PLUGIN / "scripts" / "install-agents.py").exists()
    installation = (ROOT / "docs" / "plugin-installation.md").read_text()
    assert "codex_agent_team_worker" in installation
    assert "Migration from Codex Agent Team 0.3.x" in installation
    assert "0.4.x" in installation
    assert "0.5.0" in installation
    assert "luna_explorer" in installation
    assert ".codex-agent-team-agents.json" in installation
