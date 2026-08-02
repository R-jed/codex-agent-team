from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "codex-agent-team" / "skills" / "codex-agent-team"
PLUGIN = ROOT / "plugins" / "codex-agent-team"


def test_runtime_evidence_is_typed_and_partial_observation_is_not_proof():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    for field in ["route_evidence", "ancestry_evidence", "permission_evidence"]:
        assert field in runtime
    assert "partial" in runtime
    assert "never earns `R1`, `L1`, or `R2`" in runtime
    assert "mutable implementation-coupled telemetry" in runtime


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
    assert "derived from complete route evidence" in runtime


def test_profile_locked_is_the_only_route_assurance_path():
    skill = (SKILL / "SKILL.md").read_text()
    route = (ROOT / "docs" / "model-route-assurance.md").read_text()
    assert "profile_locked" in skill and "profile_locked" in route
    assert "native_explicit_validated" not in skill
    assert "native_explicit_validated" not in route
    assert "No Portable Mode" in route


def test_verifier_is_wired_into_skill_and_runtime_reference():
    verifier = SKILL / "scripts" / "verify-runtime.py"
    assert verifier.exists()
    for path in [SKILL / "SKILL.md", SKILL / "references" / "runtime-assurance.md"]:
        assert "verify-runtime.py" in path.read_text()


def test_depth_one_preserves_not_observed_state():
    runtime = (SKILL / "references" / "runtime-assurance.md").read_text()
    safety = (SKILL / "references" / "safety-policy.md").read_text()
    assert "missing observed parent -> not_observed" in runtime
    assert "parent_thread_id" in safety


def test_consent_policy_defines_resource_envelope_not_fixed_team_shape():
    consent = (SKILL / "references" / "consent-policy.md").read_text()
    assert "0-2 justified child Agents" in consent
    assert "at most 1 active writer" in consent
    assert "Luna + Sol selective review" in consent
    assert "team shape is dynamic" in consent.lower()


def test_live_evals_are_paired_and_track_correction_cost():
    docs = (ROOT / "docs" / "behavioral-evals.md").read_text()
    workloads = (ROOT / "evals" / "behavioral-workloads.json").read_text()
    assert "paired live runs" in docs
    assert "Main-session correction cost" in docs
    assert "raw_prompt_luna" in docs
    assert "contract_luna_selective_sol" in docs
    assert "no claimed benchmark results" in workloads


def test_plugin_profile_lifecycle_remains_present():
    assert (PLUGIN / "scripts" / "install-agents.py").exists()
    installation = (ROOT / "docs" / "plugin-installation.md").read_text()
    assert "codex_agent_team_worker" in installation
    assert "Migration from older model-named profiles" in installation
