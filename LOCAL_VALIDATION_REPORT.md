# codex delegate Local Validation Report

This file is the maintainer evidence ledger. `HEADOFF.md` owns the finite remaining execution plan. Public users and AI Agents should use README/README_AI.

## Current candidate baseline

```text
Product: codex delegate
Repository: R-jed/codex-delegate
Marketplace id: codex-delegate
Plugin id: codex-delegate
Skill: codex-delegate
Canonical explicit invocation: $codex-delegate
Plugin version: 0.9.1
Current roles: codex_delegate_reader / codex_delegate_worker / codex_delegate_solver / codex_delegate_investigator / codex_delegate_advisor
Current ownership manifest: .codex-delegate-agents.json
Machine policy: policy-contract.json schema 3
Runtime policy surface: router-core.md / guardrails.md / final-review.md
Invocation: explicit only
Plugin shape: skills-only
Architecture posture: MECHANISM COMPRESSION + OFFICIAL CODEX ALIGNMENT IMPLEMENTED / VALIDATION PENDING
Release posture: HOLD FOR RELEASE / DETERMINISTIC + LIVE VALIDATION PENDING
Known open reproducible PROJECT P0/P1 on exact current tree: none established yet
```

Static validation for the exact current tree is pending. Nothing in this ledger means `pytest passed`, `Plugin validator passed`, or product behavior is proven until exact commands and outputs are recorded for the exact candidate SHA.

## Repository facts established during the 2026-08-05 refactor and official-compliance review

Current source inspection establishes:

- the product keeps five exact role profiles: Reader, Worker, Solver, Investigator, Advisor;
- runtime policy is compressed from eight model-facing reference documents to three;
- `router-core.md` owns delegation benefit, direct capability selection, child packet, blocker handling, scheduling, and acceptance;
- `guardrails.md` owns user authority, official explicit Skill invocation, provisioning readiness, consent, writer ownership, permissions, trust boundaries, and on-demand runtime evidence;
- `final-review.md` owns independent artifact-bound assurance;
- `policy-contract.json` schema `3` contains stable machine constants only: delegation limits, capability-dedup reference, role routes, and Final Review reason codes;
- the former runtime dependency ontology is no longer encoded in the machine policy;
- Skill state is one compact work-item state rather than separate dependency/evidence/recovery ledgers;
- normal routing diagnoses only `contract | judgment | investigation | stalled` blockers;
- stalled same-role work permits at most one clean retry when the role remains correct and the packet materially improves;
- Luna Worker is restricted to clear, repeatable bounded implementation where material behavior decisions are already resolved;
- Sol Solver is the write-capable lane when demanding/material judgment is coupled to implementation;
- Sol Advisor is the read-only demanding/material-judgment and fresh-review lane;
- Terra Investigator is a bounded read-heavy technical investigation/evidence-synthesis lane after semantics are stable and material judgment is absent;
- Terra is not an escalation rung; demanding, ambiguous, multi-step technical judgment belongs to capable Main/Sol;
- main-session model/effort awareness is a Sol capability-dedup optimization, not authority or runtime task taxonomy;
- `runtime-evidence.py` reads the policy-owned reference model + effort order and is explicitly diagnostic/on-demand;
- complete trusted Sol `high`, `xhigh`, or `max` metadata can cover the current Sol `high` reference; Sol `medium`/`low` is insufficient; unknown/unranked/partial/local-only/conflicted evidence remains conservative;
- one canonical checkout has one writing actor inside the current orchestration; Main writes, Worker, and Solver share that domain;
- implicit Skill invocation is disabled;
- official explicit Skill invocation is `$codex-delegate`; `/skills` is the Skill picker; no invented custom slash command is part of the current product contract;
- first-use role provisioning is required before delegated code execution, avoiding mid-implementation setup/restart;
- the five managed role files use Codex's native custom-Agent TOML mechanism under the active Codex home; the bundled installer is a project-specific lifecycle/ownership safety layer, not another Agent runtime;
- ordinary successful tasks no longer require a separate orchestration receipt;
- Final Review remains consequence-driven and fresh when required;
- the Plugin intentionally remains skills-only and does not declare unused MCP/apps/hooks surfaces;
- public Plugin metadata now includes website, privacy policy, terms of use, category, brand assets, and `$codex-delegate` starter prompts;
- root `PRIVACY.md` and `TERMS.md` are current public legal documents for Plugin submission metadata;
- `main` remains a moving pre-release development ref; final v1.0.0 installation evidence must be bound to one immutable RC/tag.

These are repository facts only. Deterministic and live validation remain required.

## Official upstream facts used by this review

The current review is grounded in current OpenAI Codex documentation for:

```text
Codex Skills explicit invocation: $skill-name
Codex Skill picker: /skills
Plugin minimum shape and skills-only Plugins
Plugin manifest and marketplace metadata
public Plugin submission/listing/legal URL requirements
native custom Agents under Codex agent configuration directories
Subagent token/concurrency cautions
model guidance: Luna for clear repeatable high-volume work, Terra for intelligence/cost-balanced read-heavy exploration, Sol for demanding ambiguous multi-step reasoning
```

Exact source URLs/revisions should be captured in `docs/openai-references.md` and release evidence. Upstream guidance remains distinct from live runtime proof.

## Evidence classes

- **Repository fact**: inspected current source/manifest/policy/test state.
- **Deterministic evidence**: reproducible test, validator, installer/verifier/digest/filesystem result.
- **Live runtime evidence**: behavior observed in a real Codex task/runtime.
- **Upstream source fact**: behavior established from a specific official source revision/documentation.
- **Model judgment**: advisory only.
- **Carried forward**: older evidence whose declared dependencies did not change.
- **Pending revalidation**: implementation exists but exact-current-tree proof is absent.

## Current evidence matrix

| Claim | Status | Boundary |
| --- | --- | --- |
| repo/marketplace/Plugin identity is `codex-delegate` | repository fact | current tree |
| Plugin version is `0.9.1` | repository fact | current Plugin/public docs |
| canonical explicit Skill invocation is `$codex-delegate` | implementation fact, exact-tree regression/live validation pending | manifest/openai metadata/docs/tests |
| public privacy/terms URLs exist in Plugin manifest | implementation fact, current validator/live listing revalidation pending | manifest + root legal docs |
| Plugin remains skills-only | repository fact, official validator revalidation pending | manifest/package |
| current role set is Reader/Worker/Solver/Investigator/Advisor | repository fact, deterministic revalidation pending | policy/profile/installer/tests |
| current ownership receipt is `.codex-delegate-agents.json` | repository fact, deterministic revalidation pending | installer lifecycle |
| custom profiles use native Codex Agent TOML shape | implementation fact, live discovery pending | profiles/compliance tests |
| policy schema 3 is internally valid | implementation fact, deterministic suite pending | policy/runtime/tests |
| exactly three model-facing runtime references remain | implementation fact, deterministic suite pending | Skill references/tests |
| implicit invocation is disabled | implementation fact, runtime validation pending | openai interface/live invocation |
| first-use provisioning happens before delegated execution | policy fact, live validation pending | Skill/guardrails/Checkpoint 1 |
| capability dedup is model + effort aware | implementation + fixture tests present, deterministic execution pending | runtime-evidence helper |
| runtime evidence is absent from ordinary hot path | policy fact, live observation pending | Skill/guardrails/Checkpoint 2 |
| one compact task state replaces three runtime ledgers | policy fact, behavioral validation pending | Skill/router-core |
| Luna bounded implementation quality | hypothesis only | Checkpoint 2/4 |
| Sol Solver reduces handoff/rework on judgment-coupled implementation | hypothesis only | Checkpoint 2/4 |
| covered Sol main avoids redundant Sol calls without quality loss | hypothesis only | Checkpoint 2/4 |
| Terra improves read-heavy stable-semantics investigation at useful cost/quality | hypothesis only | Checkpoint 2/4 |
| demanding technical judgment routes to Sol rather than Terra | policy fact, behavioral validation pending | Checkpoint 2/3/4 |
| no default orchestration receipt improves completion clarity | product hypothesis | Checkpoint 5 |
| consequence-driven Final Review preserves quality at lower frequency | hypothesis only | Checkpoint 4 |
| same-checkout cross-session safety | live pending | Checkpoint 5 |
| same-Codex-home installer multi-process safety | live pending | Checkpoint 6 |
| immutable RC install/release path works | pending | Checkpoint 6 |

## Previous real Codex runtime evidence

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

This evidence predates Sol Solver, mechanism compression, official `$skill` invocation alignment, and current Terra placement. It cannot establish current routing, onboarding, profile lifecycle, capability dedup, or release readiness.

## Deterministic execution record

Pending for exact current candidate SHA.

Record each run as:

```text
TEST_ID
TESTED_REVISION
PYTHON / TOOL VERSION
COMMAND
EXIT CODE
RESULT: PASS | FAIL | PARTIAL | NOT_RUN
WARNINGS / SKIPS / XFAILS
DEPENDENCIES
NOTES
```

Do not mark the deterministic gate passed until the complete preflight in `HEADOFF.md` succeeds on one unchanged SHA, including official compliance tests and both required Plugin validator runs.

## Live validation record format

```text
TEST_ID
CHECKPOINT
TESTED_REVISION
RUNTIME_VERSION / PLATFORM
WORKLOAD / FIXTURE
EXPECTED USER OUTCOME
EXPECTED ACTOR / INVARIANT
OBSERVED ROUTING / RESOURCE STATE
OBSERVED RUNTIME EVIDENCE, when material
COMMANDS / VERIFICATION
RESULT: PASS | FAIL | PARTIAL | NOT_EXPOSED
EVIDENCE CLASS
UNRESOLVED
```

For writer/concurrency cases record workspace identity, active writer, child ids, start/completion timing, wait surface, and relevant external drift. For Final Review record semantic reason, artifact id, Advisor evidence, verdict, post-review mutation, and gate status.

## Adversarial consultation

Use `/gpt56-sol-pro-consult` with exact target conversation `R-jed/codex-delegate`. Exact-title unique-match is fail-closed. Consultation is model judgment only and never counts as deterministic, runtime, install, or behavioral product evidence.
