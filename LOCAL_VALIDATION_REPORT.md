# codex delegate Local Validation Report

This file is the maintainer evidence ledger. `HEADOFF.md` owns the finite remaining execution plan. Public users and AI Agents should use README/README_AI instead.

## Current candidate baseline

```text
Product: codex delegate
Repository: R-jed/codex-delegate
Marketplace id: codex-delegate
Plugin id: codex-delegate
Canonical command: /codex-delegate
Plugin version: 0.8.0
Current roles: codex_delegate_reader / codex_delegate_worker / codex_delegate_solver / codex_delegate_investigator / codex_delegate_advisor
Current ownership manifest: .codex-delegate-agents.json
Routing contract: policy schema 2 / routing-eval schema 4.0
Architecture posture: ROUTING V4 IMPLEMENTED / VALIDATION PENDING
Release posture: HOLD FOR RELEASE / DETERMINISTIC + LIVE V4 VALIDATION PENDING
Known open reproducible PROJECT P0/P1 on exact current tree: none established yet
```

The current repository tree has one project identity and one current managed Agent generation. Routing V4 implementation changes the role set, dependency classifier, main-session judgment coverage, recovery semantics, Final Review semantics, and behavioral-evaluation contract. Therefore older green test or live-runtime evidence cannot prove the exact current candidate unless its declared dependencies are unchanged.

Static validation for the exact current tree is pending. No statement in this ledger should be interpreted as `pytest passed`, `Plugin validator passed`, or `Routing V4 is behaviorally proven` until exact commands and outputs are recorded here.

## Repository facts established during the 2026-08-04 Routing V4 refactor

Current source inspection establishes:

- public/AI/plugin metadata identifies version `0.8.0` and the current `codex-delegate` identity;
- `policy-contract.json` schema `2` defines five dependency kinds and five semantic child roles;
- current managed roles are Reader, Worker, Solver, Investigator, and Advisor;
- `codex_delegate_solver` is a Sol High workspace-write role for judgment-coupled execution;
- Luna Worker is restricted to standardized `bounded_execution` where material behavior decisions are already resolved;
- Terra Investigator is restricted to narrow `technical_investigation` after semantic intent is stable;
- Sol Advisor covers material judgment uplift and fresh independent Final Review;
- main-session judgment coverage is a routing input only when material judgment exists;
- complete trusted native Sol main metadata can establish `covered`; complete native non-Sol metadata can establish `uncovered`; missing/partial/local-only/conflicted metadata remains `unknown`;
- a covered Sol main suppresses redundant ordinary Sol capability-uplift children but does not satisfy required independent Final Review;
- execution failure is handled through evidence-driven dependency reclassification rather than a fixed model ladder;
- standard reclassification signals are `CONTRACT_GAP`, `JUDGMENT_REQUIRED`, `TECHNICAL_GAP`, and `EXECUTION_STALL`;
- Final Review direct triggers are consequence-driven; Terra use, Solver use, recovery, or diff size alone is not a trigger;
- Worker and Solver share the one-active-project-writer-per-canonical-checkout safety domain;
- installer code provisions the five current profiles and preserves unrelated Agent profiles;
- current-generation installer logic can add a newly shipped Solver profile to an exact proven current receipt without rewriting unchanged managed profiles;
- behavioral eval schema/workloads/scorer have been refactored around Routing V4 strategy comparisons rather than a universal Luna-first execution baseline.

These are repository implementation facts only. They require deterministic execution and live runtime evidence before stronger release/product claims are allowed.

## Evidence classes

- **Repository fact**: inspected source/manifest/policy/test state.
- **Deterministic evidence**: reproducible test, validator, installer/verifier/digest/filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/runtime.
- **Upstream source fact**: behavior established from a specific official source revision/documentation.
- **Model judgment**: advisory only.
- **Carried forward**: older evidence whose declared dependencies did not change.
- **Pending revalidation**: implementation exists but exact-current-tree proof is absent.

## Current evidence matrix

| Claim | Status | Boundary |
| --- | --- | --- |
| repo/marketplace/Plugin identity is `codex-delegate` | repository fact | current tree |
| Plugin version is `0.8.0` | repository fact | current Plugin/public docs |
| current managed role set is Reader/Worker/Solver/Investigator/Advisor | repository fact, deterministic revalidation pending | policy/profile/installer/tests |
| current ownership receipt is `.codex-delegate-agents.json` | repository fact, deterministic revalidation pending | installer lifecycle |
| retired project identity is absent from current tree | guard implementation fact, deterministic rerun pending | identity test |
| Routing V4 dependency classification contracts are internally consistent | implementation fact, deterministic suite pending | policy/schema/static evals |
| main-session coverage verifier returns covered/uncovered/unknown correctly | implementation + fixture-test code present, deterministic execution pending | runtime-evidence helper |
| installer safely adds Solver to a proven current-generation receipt | test implementation present, deterministic execution pending | installer lifecycle |
| official Plugin structure/validation passes | pending | deterministic preflight + Checkpoint 6 |
| exact five child routes are discoverable/routed on current Codex runtime | live pending | Checkpoint 1 |
| main-session model/effort is exposed sufficiently for coverage decisions | live pending | Checkpoint 1 |
| Luna bounded-execution quality hypothesis | live pending | Checkpoint 2/4 |
| Sol Solver improves or simplifies non-Sol judgment-coupled execution | hypothesis only | Checkpoint 4 controlled pair |
| Sol main can avoid redundant Sol child calls without quality loss | hypothesis only | Checkpoint 2/4 controlled pair |
| Terra delta routing reduces rework for real technical uncertainty | hypothesis only | Checkpoint 3/4 |
| process-history negative control reduces decorative Final Review | hypothesis only | Checkpoint 4 |
| host-enforced read-only | live pending | runtime evidence when material |
| completion-driven refill/wait surface | live pending | Checkpoint 3 |
| same-checkout multi-session writer safety including Worker/Solver | live pending | Checkpoint 5 |
| installer multi-process safety | live pending | Checkpoint 6 I1-I3 |
| required Final Review lifecycle and yield | live pending | Checkpoint 4 |

## Previous real Codex runtime evidence

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

This evidence predates Routing V4, Sol Solver, policy schema `2`, and current eval schema `4.0`. It cannot establish current role discovery, main-session coverage, Routing V4 behavior, installer five-profile lifecycle, or release readiness.

## Deterministic execution record

Pending for exact current Routing V4 SHA.

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

Do not mark the deterministic gate passed until the complete required preflight in `HEADOFF.md` succeeds on one unchanged SHA, including both required Plugin validator runs.

## Live validation record format

```text
TEST_ID
CHECKPOINT
TESTED_REVISION
RUNTIME_VERSION / PLATFORM
WORKLOAD / FIXTURE
MAIN_SESSION_ROUTE / MAIN_JUDGMENT_COVERAGE
DEPENDENCY KIND
EXPECTED ACTOR / INVARIANT
CONFIGURED ROUTE / RESOURCE STATE
OBSERVED RUNTIME EVIDENCE
COMMANDS / VERIFICATION
RESULT: PASS | FAIL | PARTIAL | NOT_EXPOSED
EVIDENCE CLASS
DEPENDENCIES
UNRESOLVED
```

For concurrency also record child ids, start/completion times, wait surface, slot-refill timing, and model-mediated polling. For reclassification record original kind, new evidence, stop signal, resulting kind, and effective actor. For Final Review record semantic triggers, artifact id, Advisor route evidence, verdict, post-review mutation, and gate status.

## Adversarial consultation

Use `/gpt56-sol-pro-consult` with exact target conversation `R-jed/codex-delegate`. Exact-title unique-match is fail-closed. Consultation is `model_judgment` only and never counts as deterministic, runtime, install, or behavioral product evidence.
