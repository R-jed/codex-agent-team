# codex delegate Local Validation Report

This file is the maintainer evidence ledger. `HEADOFF.md` owns the finite remaining execution plan. Public users and AI Agents should use README/README_AI instead.

## Current accepted/candidate baseline

```text
Product: codex delegate
Repository: R-jed/codex-delegate
Marketplace id: codex-delegate
Plugin id: codex-delegate
Canonical command: /codex-delegate
Plugin version: 0.7.0
Current roles: codex_delegate_reader / codex_delegate_worker / codex_delegate_investigator / codex_delegate_advisor
Current profile files: codex-delegate-*.toml
Current ownership manifest: .codex-delegate-agents.json
Architecture posture: FROZEN
Release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
Known open reproducible PROJECT P0/P1: none
```

The 0.7.0 identity closure removes the old project Agent namespace from current runtime/profile/ownership state. Historical `codex_agent_team_*`, `codex-agent-team-*.toml`, and `.codex-agent-team-*.json` values are recognized only by the bounded migration path and migration tests. Successful migration must leave no active old project generation.

Static validation for this exact 0.7.0 tree is pending the direct-main CI run. Do not convert the previous 0.6.0 green run into evidence for changed profile/installer identity.

## Evidence classes

- **Repository fact**: inspected source/manifest/policy/test state.
- **Deterministic evidence**: reproducible test, validator, installer/verifier/digest/filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/runtime.
- **Upstream source fact**: behavior established from a specific official source revision/documentation.
- **Model judgment**: advisory only.
- **Carried forward**: older evidence whose declared dependencies did not change.
- **Pending revalidation**: implementation exists but current-runtime proof is absent.

## Current evidence matrix

| Claim | Status | Boundary |
| --- | --- | --- |
| public repo/marketplace/Plugin identity is `codex-delegate` | repository fact | current tree |
| current role namespace is exclusively `codex_delegate_*` | pending deterministic validation | policy/profile/test tree changed in 0.7.0 |
| current ownership receipt is `.codex-delegate-agents.json` | pending deterministic validation | installer changed in 0.7.0 |
| proven 0.6.x project state migrates one-way and old project state is removed | pending deterministic + live validation | static migration tests then Checkpoint 6 |
| unproven old project profile fails closed | pending deterministic + live validation | no silent overwrite/delete |
| Plugin structure/current official validator | pending 0.7.0 CI | RC reruns then-current validator |
| exact current Reader/Worker/Investigator/Advisor routes | live pending | Checkpoint 1 |
| host-enforced read-only | live pending | configuration intent is not proof |
| completion-driven refill/wait surface | live pending | Checkpoint 3 |
| same-checkout multi-session writer safety | live pending | Checkpoint 5 |
| installer multi-process safety | live pending | Checkpoint 6 I1-I3 |
| Final Review lifecycle and product value | live pending | Checkpoint 4 |

## Last accepted real Codex runtime baseline

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

That evidence predates the 0.7.0 Agent identity migration and cannot prove current role discovery.

## Live validation record format

```text
TEST_ID
CHECKPOINT
TESTED_REVISION
RUNTIME_VERSION / PLATFORM
WORKLOAD / FIXTURE
EXPECTED INVARIANT
CONFIGURED ROUTE / RESOURCE STATE
OBSERVED RUNTIME EVIDENCE
COMMANDS / VERIFICATION
RESULT: PASS | FAIL | PARTIAL | NOT_EXPOSED
EVIDENCE CLASS
DEPENDENCIES
UNRESOLVED
```

For completion/concurrency also record child ids, start/completion times, wait surface, slot-refill timing, and model-mediated polling. For Final Review also record requirement, triggers, artifact id, Advisor route evidence, verdict, post-review mutation, and gate status.

## Adversarial consultation

Use `/gpt56-sol-pro-consult` with exact target conversation `分支 · 分支 · 项目对比分析`. Exact-title unique-match is fail-closed. Consultation is model judgment only and never runtime/install evidence.
