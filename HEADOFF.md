# codex delegate v1.0 Validation Handoff

This is the finite deterministic/live-validation and v1.0.0 release checklist for the current codex delegate candidate.

The product model is now settled: the user gives one strong Main session the goal, Main acts as the team leader, and `/codex-delegate` gives that leader the rules for deciding what to keep, what to delegate, which specialist role fits, how much useful parallelism to use, and when to stop adding Agents.

The project should trust a capable Main model to lead. The policy exists to prevent loss of control, not to replace Main's judgment with a fixed Agent count or rigid model pipeline.

## Current candidate baseline

```text
product: codex delegate
repository: R-jed/codex-delegate
marketplace/plugin id: codex-delegate
skill: codex-delegate
explicit invocation: /codex-delegate
version: 0.9.1
current roles: codex_delegate_reader / worker / solver / investigator / advisor
current ownership manifest: .codex-delegate-agents.json
runtime policy surface: router-core.md / guardrails.md / final-review.md
machine policy: policy-contract.json schema 4
invocation: explicit only
plugin shape: skills-only
custom roles: native Codex custom-Agent TOML profiles + project lifecycle installer
parallelism policy: main-led ready frontier + progressive fan-out, no project ordinary numeric child ceiling
known open reproducible PROJECT P0/P1: none established on exact current tree
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
- one canonical physical checkout has one active writer inside one orchestration;
- delegation depth remains one;
- children do not widen scope, permissions, external impact, or user intent;
- there is no fixed Luna → Terra → Sol ladder;
- failure does not imply model escalation;
- exact role mismatch fails closed;
- configured intent does not count as observed runtime truth;
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

Use a branch or worktree when multiple independent writers, risky experimentation, or external review genuinely requires isolation. Never overwrite concurrent work.

During pre-release development, `main` is a moving development ref. The final v1.0.0 installation and release proof must use one fixed immutable RC/tag. A green earlier `main` SHA is not release evidence for a later SHA.

## Deterministic execution preflight

Complete this gate on one exact current SHA before treating live-runtime results as release evidence. Record commands, outputs, exit codes, Python version, validator revision, relevant warnings/skips, and the exact SHA in `LOCAL_VALIDATION_REPORT.md`.

Required deterministic execution:

```bash
python -m pytest tests/test_identity_cleanup.py -q
python -m pytest tests/test_official_plugin_compliance.py tests/test_install_agents.py tests/test_installer_safety.py tests/test_plugin_packaging.py tests/test_policy.py tests/test_concurrency_policy.py tests/test_runtime_evidence.py tests/test_capability_dedup.py tests/test_runtime_truth_policy.py tests/test_behavioral_evals.py tests/test_headoff.py tests/test_readme_user_facing.py -q
python -m pytest -q
```

Also run:

1. the repository-pinned official Plugin validator used by maintained CI;
2. the then-current official OpenAI Plugin validator against `plugins/codex-delegate`, recording its exact revision.

The deterministic gate passes only when:

- every required command exits successfully;
- the complete pytest suite has no failures or errors;
- release-relevant skips, xfails, and warnings are reviewed;
- canonical `/codex-delegate` and `/skills` behavior remains the documented project entry surface;
- no stale dollar-style codex-delegate invocation remains;
- public Plugin metadata still includes website, privacy policy, terms, category, brand assets, and valid starter prompts;
- the Plugin remains the smallest useful skills-only shape;
- policy-contract.json schema 4 defines exactly five managed profiles and no ordinary numeric child ceiling;
- `router-core.md / guardrails.md / final-review.md` remain the only model-facing runtime references;
- implicit invocation remains disabled;
- installer fresh/update/idempotent/non-mutating/safety tests pass;
- runtime evidence and Sol capability dedup preserve unknown when native truth is missing;
- both required Plugin validator runs pass;
- the tested SHA remains unchanged after validation.

If any deterministic check fails, stop release validation, fix the evidence-backed defect, rerun focused checks, then rerun the full deterministic gate on the new exact SHA.

Static checks do not prove model quality, native concurrent capacity, adaptive team-size quality, cross-session safety, onboarding quality, Sol Solver value, Terra investigation value, or Final Review yield.

## Product stop line

Do not reintroduce a fixed child count, role ladder, mandatory final Sol pass, or orchestration ceremony merely to make one workload easier to describe.

Blocked work stays compact:

```text
contract | judgment | investigation | stalled
```

A stall permits at most one clean same-role retry when the role remains correct and the packet materially improves. Ordinary successful tasks do not need a separate orchestration receipt.

Do not add Checkpoint 7.

## Checkpoint 1: Plugin discovery, command invocation, and exact five-role readiness

```text
Status: PASS
Runtime product bytes exercised: 55728b41592058575a6e35632adc6af75a355016
Checkpoint 1 closure SHA: cfd5f17cf18e19b5ed3afe4992fe5b8cbb45be97
Carry-forward basis: Plugin, Skill, Agent profiles, installer, policy, and runtime-reference bytes are unchanged after the runtime-tested revision; post-runtime closure changes are public/release documentation and regression tests only.
Evidence reference: LOCAL_VALIDATION_REPORT.md#checkpoint-1-plugin-discovery-command-invocation-and-five-role-readiness
Remaining blocker: none for Checkpoint 1.
Closure: Codex 0.146.0 `/skills` displayed and selected `Codex Delegate`, inserting `@Codex-Delegate`; unrelated and Skill-affine ordinary-task controls completed without observed Codex Delegate activation. The Skill-affine control visibly used other applicable Skills, providing a positive control for activation evidence.
```

Validate a fresh user path:

- Plugin is discoverable from the Codex Plugin Marketplace;
- a new thread exposes `/codex-delegate` and `/skills` can discover/select the Skill;
- ordinary tasks do not implicitly invoke codex delegate;
- first delegated use detects missing project roles before delegated implementation starts;
- provisioning requests permission and writes only the five managed native custom-Agent profiles plus `.codex-delegate-agents.json`;
- if a fresh thread is required to see new roles, stop before child writing;
- exact role/profile tuples come from policy-contract.json schema 4;
- missing or mismatched exact roles do not cross-route.

### Review Checkpoint A

Send only sanitized new evidence and unresolved consequential judgment to the consultation target below.

```text
Status: PASS
Result: REVIEW_COMPLETED
Request-ID: wgpt-a508773eef17481d
Evidence reference: LOCAL_VALIDATION_REPORT.md#adversarial-consultation
Finding: Checkpoint 1 PASS; the remaining `/skills` and non-implicit-invocation runtime gaps were closed. No reproducible project-side P0/P1 was established. One P2 public Final Review contract drift was corrected without changing runtime policy.
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
```

Verify trusted Sol-main capability can suppress redundant Sol delegation when appropriate. Unknown Main route telemetry must stay unknown and must not add routine cost.

### Review Checkpoint B

Review repeated unnecessary Agent calls, Luna semantic overreach, Terra used as an escalation rung, missed Sol judgment placement, and unjustified fan-out before changing policy.

## Checkpoint 3: blockers, recovery, writer ownership, and adaptive scheduling

Validate:

- weak Luna quality alone does not trigger Terra;
- demanding or ambiguous technical judgment routes to Sol;
- duplicate responsibility ownership is suppressed;
- speculative work behind unresolved semantics is not spawned early;
- three or more distinct ready read-only responsibilities may run together when useful;
- spare native capacity alone does not create another child;
- Main + Worker, Main + Solver, and Worker + Solver do not write one canonical checkout concurrently;
- isolated worktrees/workspaces may own separate writers;
- exposed child completions can refill useful work without forcing artificial waves.

Use the A/B/C case:

```text
A = slow independent read-only work
B = fast independent read-only work
C = depends only on B
```

Record the real runtime wait/update surface. Do not invent event-driven behavior the host does not expose.

Also run a positive fan-out case with at least three independent read-only lanes and a negative control containing duplicate or speculative lanes.

### Review Checkpoint C

Separate product defects from native-runtime capacity or observability boundaries.

## Checkpoint 4: controlled product-value experiments and Final Review

`evals/` remains a measurement surface, not runtime policy.

Run paired workloads covering:

- bounded Luna packet vs raw Luna prompt;
- Advisor + Luna handoff vs one Sol Solver;
- Sol-main direct execution vs redundant Sol Solver;
- Luna Reader vs Terra Investigator on stable-semantics investigation;
- adaptive multi-reader fan-out vs unnecessary serial waves;
- duplicate/speculative fan-out negative control;
- demanding/ambiguous technical judgment must go to Sol;
- useful Final Review vs decorative process-history-only review.

Measure acceptance, wrong edits, correction turns, repeated work, duplicate ownership, unnecessary children, redundant expensive calls, latency/tokens when exposed, and review findings.

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

## Checkpoint 5: consent, onboarding friction, and multi-session safety

Validate that adaptive delegation feels natural to a user who simply writes `/codex-delegate <task>` and does not specify team size.

Confirm:

- no prompt merely because active child count crosses an arbitrary number;
- material permission, scope, external-impact, or compute expansion asks for consent;
- several justified low-cost read-only lanes can stay inside ordinary execution;
- repeated Solver/Advisor/Investigator/re-review loops eventually require renewed consent when compute materially expands;
- initial role setup completes before delegated implementation;
- routine success does not add extra routing ceremony.

Multi-session matrix:

```text
M1 different sessions, different projects/checkouts
M2 different sessions, same repository, isolated worktrees
M3 different sessions, same canonical physical checkout
M4 one project writer + one read-only session same checkout
M5 Worker + Solver proposed concurrently in same checkout
M6 Main writer + Worker/Solver proposed concurrently in same checkout
```

Do not add a workspace lock unless M3 reproduces a project-side coordination failure that drift detection and recommended isolation cannot safely contain.

### Review Checkpoint E

Any reproducible P0/P1 candidate requires adversarial review before remediation is accepted.

## Checkpoint 6: immutable RC install and release closure

For the selected fixed RC:

1. record one immutable candidate SHA/ref;
2. run maintained CI and both required Plugin validators;
3. verify public website/privacy/terms/support path and Plugin listing metadata;
4. perform a real fresh Plugin installation from that fixed candidate;
5. confirm `/codex-delegate`, `/skills`, candidate version, and disabled implicit invocation in a fresh thread;
6. prove first-use five-profile provisioning and readiness behavior;
7. verify repeat install is idempotent and `--check` is non-mutating;
8. verify managed-profile updates occur only with exact ownership proof;
9. verify modified/unowned reserved profiles fail closed and unrelated profiles remain untouched;
10. test same-CODEX_HOME installer races I1-I3;
11. rerun release-relevant live checkpoints on the immutable candidate;
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
- `/codex-delegate` invocation and onboarding behavior;
- representative daily routing and Sol capability-dedup cases;
- adaptive fan-out, blocker/retry/Terra investigation, and writer-safety cases;
- controlled product-value experiments;
- required Final Review lifecycle;
- multi-session and installer-concurrency validation;
- no open reproducible P0/P1.

Quality, speed, or cost claims must stay within evidence actually recorded.

Then tag `v1.0.0`, publish the GitHub Release, and make the immutable release ref the recommended stable user-install channel. `main` can remain the development channel after release.

## Required project consultation target

Use `/webgpt-consult` at Review Checkpoints A-E, any P0/P1 candidate, and RC closure.

```text
CONSULTATION_ENTRYPOINT: /webgpt-consult
TARGET_CHATGPT_CONVERSATION_TITLE: codex-delegate
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
FAILURE: CONSULTATION_TARGET_UNRESOLVED
```

Do not fuzzy match, guess by recency, create a replacement conversation, or silently fall back to an isolated consultation. Consultation output is model judgment and never counts as runtime, install, or product evidence.
