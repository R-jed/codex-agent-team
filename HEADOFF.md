# codex delegate v1.0 Validation Handoff

This is the finite deterministic/live-validation and v1.0.0 release checklist for the current codex delegate candidate.

The product model is settled: the user gives one strong Main session the goal, Main acts as the team leader, and `$codex-delegate:codex-delegate` gives that leader the rules for deciding what to keep, what to delegate, which specialist role fits, how much useful parallelism to use, and when to stop adding Agents.

The project should trust a capable Main model to lead. Policy provides coordination and safety boundaries without replacing Main's judgment with a fixed Agent count, rigid model pipeline, or second workflow planner.

## Current candidate baseline

```text
product: codex delegate
repository: R-jed/codex-delegate
marketplace/plugin id: codex-delegate
skill: codex-delegate
explicit invocation: $codex-delegate:codex-delegate
version: 1.0.0
current roles: codex_delegate_reader / worker / solver / investigator / advisor
current ownership manifest: .codex-delegate-agents.json
current installer lock: .codex-delegate-agents.lock
runtime policy surface: router-core.md / guardrails.md / final-review.md
machine policy: policy-contract.json schema 4
invocation: explicit only
plugin shape: skills-only
custom roles: native Codex custom-Agent TOML profiles + project lifecycle installer
parallelism policy: main-led ready frontier + progressive fan-out, no project ordinary numeric child ceiling
coordination policy: preserve upstream workflow truth + semantic independence + explicit mutation authority + optional integration order
runtime evidence: requested / accepted / observed are separate truth layers
known open reproducible PROJECT P0/P1: none established on current coordination-hardening tree; exact-SHA local/live validation pending
release posture: HOLD FOR RELEASE / OFFICIAL COMPLIANCE + DETERMINISTIC + LIVE VALIDATION PENDING
```

Before every checkpoint, fetch current `origin/main`, record the exact SHA and runtime, and invalidate evidence whose declared dependencies changed.

## Architecture decision to preserve

These are product decisions, not tuning suggestions:

- main session always owns user intent, authorization, team composition, integration, acceptance, and final response;
- zero children is a normal outcome;
- delegation requires a concrete benefit;
- project policy does not target or cap an ordinary fixed child count;
- Main manages a ready frontier and uses progressive fan-out;
- every child needs a distinct, ready, non-duplicative responsibility;
- native Agent capacity is an upper bound, never a target to fill;
- spare native capacity alone does not create another child;
- three or more distinct ready read-only responsibilities may run together when the task and native capacity justify it;
- child count alone is not a consent trigger; material compute expansion is;
- an upstream Skill or accepted plan remains authoritative for its goal, decomposition, stage order, dependencies, outputs, acceptance, and quality gates;
- codex delegate may coordinate ownership, role selection, useful concurrency, write isolation, and integration timing around that upstream workflow without creating a competing domain plan;
- one canonical physical checkout has one active writer inside one orchestration;
- filesystem isolation alone does not prove semantic independence for concurrent writers;
- child intent and mutation authority are separate; filesystem capability never grants extra mutation authority;
- `INTEGRATION AFTER` may order accepted outputs only when work is already safe to execute; it cannot hide unresolved semantics;
- Main integrates delegated outputs in dependency-respecting order and verifies the combined artifact;
- requested, platform-accepted, and runtime-observed route facts stay separate; accepted/configured values never become observed facts by inference;
- delegation depth remains one;
- children do not widen scope, permissions, mutation authority, external impact, or user intent;
- there is no fixed Luna → Terra → Sol ladder;
- failure does not imply model escalation;
- exact role mismatch fails closed;
- independent Final Review is triggered by the final artifact's consequences, not process ceremony.

The five specialist roles remain:

```text
codex_delegate_reader       -> Luna Reader, narrow read-only evidence
codex_delegate_worker       -> Luna Worker, clear repeatable writing after behavior is decided
codex_delegate_solver       -> Sol Solver, judgment-coupled implementation
codex_delegate_investigator -> Terra Investigator, broader read-only investigation after semantics are stable
codex_delegate_advisor      -> Sol Advisor, important read-only judgment or fresh independent review
```

Terra is a bounded read-heavy investigation/evidence-synthesis lane. Terra is not an escalation rung. Difficult, ambiguous, multi-step technical judgment belongs to capable main/Sol.

## Repository maintenance workflow

For clear, bounded, owner-authorized maintenance, inspect current `main` first and preserve unrelated work. Direct-main work is allowed when isolation adds no concrete value.

Use a separate physical checkout when multiple independent writers, risky experimentation, or external review genuinely requires isolation. Filesystem isolation does not remove semantic dependencies. Never overwrite concurrent work.

During pre-release development, `main` is a moving development ref. The final v1.0.0 installation and release proof must use one fixed immutable RC/tag. A green earlier `main` SHA is not release evidence for a later SHA.

## Deterministic execution preflight

Complete this gate on one exact current SHA before treating live-runtime results as release evidence. Record commands, outputs, exit codes, Python version, validator revision, relevant warnings/skips, and the exact SHA in `LOCAL_VALIDATION_REPORT.md`.

Required deterministic execution:

```bash
python -m pytest tests/test_identity_cleanup.py -q
python -m pytest tests/test_official_plugin_compliance.py tests/test_install_agents.py tests/test_installer_safety.py tests/test_plugin_packaging.py tests/test_policy.py tests/test_concurrency_policy.py tests/test_coordination_policy.py tests/test_runtime_evidence.py tests/test_capability_dedup.py tests/test_runtime_truth_policy.py tests/test_behavioral_evals.py tests/test_headoff.py tests/test_readme_user_facing.py -q
python -m pytest -q
```

Also run:

1. the repository-pinned official Plugin validator used by maintained CI;
2. the then-current official OpenAI Plugin validator against `plugins/codex-delegate`, recording its exact revision.

The deterministic gate passes only when:

- every required command exits successfully;
- the complete pytest suite has no failures or errors;
- release-relevant skips, xfails, and warnings are reviewed;
- canonical `$codex-delegate:codex-delegate` and `/skills` behavior remains the documented project entry surface;
- no stale slash command or unnamespaced dollar invocation remains;
- public Plugin metadata still includes website, privacy policy, terms, category, brand assets, and valid starter prompts;
- the Plugin remains the smallest useful skills-only shape;
- policy-contract.json schema 4 defines exactly five managed profiles and no ordinary numeric child ceiling;
- `router-core.md / guardrails.md / final-review.md` remain the only model-facing runtime references;
- upstream workflow ownership, semantic independence, mutation authority, optional integration order, and route truth layering stay covered by deterministic coordination regressions;
- implicit invocation remains disabled;
- installer fresh/update/idempotent/non-mutating/safety tests pass;
- runtime evidence and Sol capability dedup preserve unknown when native truth is missing;
- platform acceptance alone never counts as observed runtime route proof;
- both required Plugin validator runs pass;
- the tested SHA remains unchanged after validation.

If any deterministic check fails, stop release validation, fix the evidence-backed defect, rerun focused checks, then rerun the full deterministic gate on the new exact SHA.

Static checks do not prove model quality, native concurrent capacity, adaptive team-size quality, semantic-independence judgment quality, cross-session safety, onboarding quality, Sol Solver value, Terra investigation value, or Final Review yield.

## Product stop line

Do not reintroduce a fixed child count, role ladder, mandatory final Sol pass, competing workflow planner, global TeamPlan, or orchestration ceremony merely to make one workload easier to describe.

Blocked work stays compact:

```text
contract | judgment | investigation | stalled
```

A stall permits at most one clean same-role retry when the role remains correct and the packet materially improves. Ordinary successful tasks do not need a separate orchestration receipt.

Do not add Checkpoint 7.

## Checkpoint 1: Plugin discovery, command invocation, and exact five-role readiness

```text
Status: REOPENED — deterministic gate passes on bd159e4; live rerun pending
Prior runtime product bytes exercised: 55728b41592058575a6e35632adc6af75a355016
Prior Checkpoint 1 closure SHA: cfd5f17cf18e19b5ed3afe4992fe5b8cbb45be97
Deterministic revalidation SHA: bd159e417bde9db2b95e612e1d6154a8f75a5a9f
Evidence reference: LOCAL_VALIDATION_REPORT.md#checkpoint-1-plugin-discovery-command-invocation-and-five-role-readiness
Remaining blocker: rerun the live Checkpoint 1 path (Plugin discovery, $codex-delegate:codex-delegate invocation, /skills, implicit-off, five-profile lifecycle) on bd159e4 in a fresh Codex thread.
Prior evidence: Codex 0.146.0 `/skills` displayed and selected `Codex Delegate`, inserting `@Codex-Delegate`; unrelated and Skill-affine ordinary-task controls completed without observed Codex Delegate activation. Prior live evidence also exposed that Codex 0.146.0 rejected the documented `/codex-delegate` command, and the source contract was corrected to `$codex-delegate:codex-delegate`.
Deterministic revalidation: 151 tests pass, no warnings/skips/xfails, pinned + current Plugin validators pass, policy-contract.json schema 4 with 5 roles, 7 coordination cases covered.
Reopen reason: current Skill/router/guardrails/runtime-evidence bytes changed during coordination hardening, so earlier runtime evidence is useful historical evidence but is not exact-candidate release proof.
```

Validate a fresh user path:

- Plugin is discoverable from the Codex Plugin Marketplace;
- a new thread exposes `$codex-delegate:codex-delegate` and `/skills` can discover/select the Skill;
- ordinary tasks do not implicitly invoke codex delegate;
- first delegated use detects missing project roles before delegated implementation starts;
- provisioning requests permission and writes only the five managed native custom-Agent profiles, `.codex-delegate-agents.json`, and `.codex-delegate-agents.lock`;
- if a fresh thread is required to see new roles, stop before child writing;
- exact role/profile tuples come from policy-contract.json schema 4;
- missing or mismatched exact roles do not cross-route.

### Review Checkpoint A

```text
Status: SUPERSEDED
Result: REVIEW_COMPLETED
Request-ID: wgpt-a508773eef17481d
Evidence reference: LOCAL_VALIDATION_REPORT.md#adversarial-consultation
Finding: retained as historical review evidence. Current invocation and coordination-hardened exact candidate require the later consolidated post-push review packet before release closure.
```

## Checkpoint 2: everyday routing quality and Sol dedup

Exercise representative tasks:

```text
T1 trivial isolated fix
-> main only

T2 narrow independent factual trace
-> Luna Reader when delegation helps

T3 fully specified implementation
-> Luna Worker when delegation helps

T4 demanding/material design judgment
-> capable main or Sol Advisor

T5 implementation with continuing material judgment
-> capable main or Sol Solver

T6 stable semantics + broader read-only investigation
-> Terra Investigator

T7 large task with no delegation benefit
-> main only

T8 ambiguous task truth
-> main repairs the contract before child writing

T9 upstream Skill already defines goal/stages/dependencies/outputs/acceptance
-> preserve upstream workflow; codex delegate assigns owners/roles/concurrency without redefining domain semantics

T10 host accepts a requested route but exposes no native route observation
-> accepted is recorded separately; observed stays not_observed and Sol coverage stays unknown
```

Verify trusted observed Sol-main capability can suppress redundant Sol delegation when appropriate. Accepted/configured route data without native observation must stay unknown and must not add routine cost.

### Review Checkpoint B

Review repeated unnecessary Agent calls, Luna semantic overreach, upstream workflow takeover, Terra used as an escalation rung, missed Sol judgment placement, false observed-route claims, and unjustified fan-out before changing policy.

Record the sanitized evidence and unresolved consequential judgment in the consolidated review packet. Do not send a separate Web consultation at this checkpoint.

## Checkpoint 3: blockers, recovery, writer ownership, and adaptive scheduling

Validate:

- weak Luna quality alone does not trigger Terra;
- demanding or ambiguous technical judgment routes to Sol;
- duplicate responsibility ownership is suppressed;
- speculative work behind unresolved semantics is not spawned early;
- three or more distinct ready read-only responsibilities may run together when useful;
- spare native capacity alone does not create another child;
- Main + Worker, Main + Solver, and Worker + Solver do not write one canonical checkout concurrently;
- isolated physical checkouts/workspaces are only the filesystem precondition for simultaneous writers; semantic independence must also be established;
- disjoint files with a shared API/schema/migration/lockfile/generated artifact/persistent or external state are treated as semantically coupled;
- verify/review/read-only responsibilities cannot source-write merely because the sandbox permits it;
- `declared-output-only` permits only the named output and does not widen to source writes;
- a child that needs broader mutation returns the authority change to Main instead of self-upgrading;
- `INTEGRATION AFTER` may order independent accepted outputs but cannot make unresolved-semantics work ready;
- Main integrates dependency-ordered outputs and verifies the final combined artifact;
- exposed child completions can refill useful work without forcing artificial waves.

Use the A/B/C case:

```text
A = slow independent read-only work
B = fast independent read-only work
C = depends only on B
```

Record the real runtime wait/update surface. Do not invent event-driven behavior the host does not expose.

Also run:

```text
semantic-coupling negative control
A = isolated writer changes stable API producer implementation
B = isolated writer consumes same stable API
-> parallel execution may be valid when semantics are already fixed

C = isolated writer changes the API contract B depends on
-> C/B must not be treated as independent merely because files/checkouts differ

mutation-authority negative control
verify child finds a source defect
-> reports defect; does not repair source without new authority

integration-order case
producer and consumer can execute safely against stable semantics
-> consumer output may specify INTEGRATION AFTER producer
-> completion time does not override integration order
```

Also run a positive fan-out case with at least three independent read-only lanes and a negative control containing duplicate or speculative lanes.

### Review Checkpoint C

Separate product defects from native-runtime capacity/observability boundaries and from correctly detected semantic dependencies.

Record the sanitized evidence and unresolved consequential judgment in the consolidated review packet. Do not send a separate Web consultation at this checkpoint.

## Checkpoint 4: controlled product-value experiments and Final Review

`evals/` remains a measurement/regression surface, not runtime policy.

Run paired workloads covering:

- bounded Luna packet vs raw Luna prompt;
- Advisor + Luna handoff vs one Sol Solver;
- Sol-main direct execution vs redundant Sol Solver;
- Luna Reader vs Terra Investigator on stable-semantics investigation;
- adaptive multi-reader fan-out vs unnecessary serial waves;
- duplicate/speculative fan-out negative control;
- filesystem-isolated but semantically coupled writers vs dependency-aware scheduling;
- explicit mutation authority vs writable-sandbox-only instruction;
- dependency-respecting integration vs completion-order integration;
- accepted-only route evidence vs actual observed route evidence;
- demanding/ambiguous technical judgment must go to Sol;
- useful Final Review vs decorative process-history-only review.

Measure acceptance, wrong edits, unauthorized edits, correction turns, repeated work, duplicate ownership, dependency mistakes, integration mistakes, unnecessary children, redundant expensive calls, latency/tokens when exposed, and review findings.

Required Final Review lifecycle:

```text
semantic trigger
-> Candidate Ready
-> review_artifact_id
-> fresh codex_delegate_advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

A Sol main still needs a fresh Advisor when independence is required. Mutation after review invalidates the old verdict.

### Review Checkpoint D

Do not turn one workload result into a permanent model-quality claim.

Record the sanitized evidence and unresolved consequential judgment in the consolidated review packet. Do not send a separate Web consultation at this checkpoint.

## Checkpoint 5: consent, onboarding friction, and multi-session safety

Validate that adaptive delegation feels natural to a user who simply writes `$codex-delegate:codex-delegate <task>` and does not specify team size.

Confirm:

- no prompt merely because active child count crosses an arbitrary number;
- material permission, mutation-authority, scope, external-impact, or compute expansion asks for consent;
- several justified low-cost read-only lanes can stay inside ordinary execution;
- repeated Solver/Advisor/Investigator/re-review loops eventually require renewed consent when compute materially expands;
- initial role setup completes before delegated implementation;
- routine success does not add extra routing ceremony.

Multi-session matrix:

```text
M1 different sessions, different projects/checkouts
M2 different sessions, same repository source, isolated physical checkouts using independent temporary clones
M3 different sessions, same canonical physical checkout
M4 one project writer + one read-only session same checkout
M5 Worker + Solver proposed concurrently in same checkout
M6 Main writer + Worker/Solver proposed concurrently in same checkout
```

Do not add a workspace lock unless M3 reproduces a project-side coordination failure that drift detection and recommended isolation cannot safely contain.

### Review Checkpoint E

Any reproducible P0/P1 candidate requires local adversarial review before remediation is accepted. Record it in the consolidated review packet; do not send a separate Web consultation at this checkpoint.

## Checkpoint 6: immutable RC install and release closure

For the selected fixed RC:

1. record one immutable candidate SHA/ref;
2. run maintained CI and both required Plugin validators;
3. verify public website/privacy/terms/support path and Plugin listing metadata;
4. perform a real fresh Plugin installation from that fixed candidate;
5. confirm `$codex-delegate:codex-delegate`, `/skills`, candidate version, and disabled implicit invocation in a fresh thread;
6. prove first-use five-profile provisioning and readiness behavior;
7. verify repeat install is idempotent and `--check` is non-mutating;
8. verify managed-profile updates occur only with exact ownership proof;
9. verify modified/unowned reserved profiles fail closed and unrelated profiles remain untouched;
10. test same-CODEX_HOME installer races I1-I3;
11. rerun release-relevant routing, coordination, runtime-truth, and live checkpoints on the immutable candidate;
12. close only with no open reproducible P0/P1.

Same-CODEX_HOME races:

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 two current-profile update/addition attempts compete in one CODEX_HOME
```

Add inter-process serialization or CAS only if a reproducible invariant failure establishes the need.

## Definition of Done for v1.0.0

Release only when one immutable RC passes:

- complete Plugin/Skill compliance and deterministic preflight;
- maintained CI and then-current official Plugin validation;
- fresh marketplace install/update/five-profile lifecycle;
- `$codex-delegate:codex-delegate` invocation and onboarding behavior;
- representative daily routing and Sol capability-dedup cases;
- upstream workflow ownership and requested/accepted/observed runtime-truth cases;
- adaptive fan-out, semantic independence, mutation authority, integration ordering, blocker/retry/Terra investigation, and writer-safety cases;
- controlled product-value experiments;
- required Final Review lifecycle;
- multi-session and installer-concurrency validation;
- no open reproducible P0/P1.

Quality, speed, or cost claims must stay within evidence actually recorded.

Then tag `v1.0.0`, publish the GitHub Release, and make the immutable release ref the recommended stable user-install channel. `main` can remain the development channel after release.

## Required project consultation target

Review Checkpoint A is historical. For Review Checkpoints B-E, any later P0/P1 candidate, and RC closure, accumulate one sanitized consolidated review packet during validation. After all HEADOFF work is complete and the latest state is pushed, use `/webgpt-consult` once for the combined adversarial review and release judgment.

```text
CONSULTATION_ENTRYPOINT: /webgpt-consult
TARGET_CHATGPT_CONVERSATION_TITLE: codex-delegate
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
FAILURE: CONSULTATION_TARGET_UNRESOLVED
```

Do not fuzzy match, guess by recency, create a replacement conversation, or silently fall back to an isolated consultation. Consultation output is model judgment and never counts as runtime, install, or product evidence.
