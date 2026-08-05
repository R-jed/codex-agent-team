# codex delegate Local Runtime Validation Handoff

This is the finite deterministic/live-validation and v1.0.0 release checklist for the mechanism-compressed codex delegate candidate.

The candidate keeps the original product goal: one explicit command, main-session control, delegation only when useful, Luna for bounded execution, Sol for material judgment, Terra for narrow specialist uncertainty, one-writer safety, and independent review only when the final artifact warrants it.

Do not add routing ceremony during validation. Change the mechanism only when deterministic or controlled live evidence establishes a real user-facing defect or falsifies a product hypothesis.

## Current candidate baseline

```text
product: codex delegate
repository: R-jed/codex-delegate
marketplace/plugin id: codex-delegate
command: /codex-delegate
version: 0.9.0
current roles: codex_delegate_reader / worker / solver / investigator / advisor
current ownership manifest: .codex-delegate-agents.json
runtime policy surface: router-core.md / guardrails.md / final-review.md
machine policy: policy-contract.json schema 3
invocation: explicit only
known open reproducible PROJECT P0/P1: none established on exact current tree
release posture: HOLD FOR RELEASE / DETERMINISTIC + LIVE VALIDATION PENDING
```

Before every validation checkpoint, fetch `origin/main`, record the exact tested SHA/runtime, and invalidate evidence whose declared dependencies changed.

## Repository maintenance workflow

For clear, bounded, owner-authorized maintenance, inspect current `main` first and preserve unrelated work. Direct-main work is allowed when isolation adds no concrete value.

Use a branch/worktree when multiple independent writers, risky experimentation, or external review genuinely requires isolation. Do not overwrite concurrent work.

During pre-release development, `main` is a moving development ref. The final v1.0.0 installation/release proof must use one fixed immutable RC/tag. Do not treat a green result on an earlier `main` SHA as release evidence for a later SHA.

## Deterministic execution preflight

Complete this gate on one exact current SHA before treating live-runtime results as release evidence.

Record exact Git SHA, Python version, validator revision where applicable, commands, exit codes, relevant skips/xfails/warnings, and concise outputs in `LOCAL_VALIDATION_REPORT.md`.

Required deterministic execution:

```bash
python -m pytest tests/test_identity_cleanup.py -q
python -m pytest tests/test_install_agents.py tests/test_installer_safety.py tests/test_plugin_packaging.py tests/test_policy.py tests/test_runtime_evidence.py tests/test_capability_dedup.py tests/test_runtime_truth_policy.py tests/test_behavioral_evals.py tests/test_headoff.py tests/test_readme_user_facing.py -q
python -m pytest -q
```

Also run:

1. the repository-pinned official Plugin validator used by maintained CI;
2. the then-current official OpenAI Plugin validator against `plugins/codex-delegate`, recording its exact revision.

The deterministic gate passes only when:

- every required command exits successfully;
- the complete pytest suite has no failures or errors;
- release-relevant skips, xfails, and warnings are reviewed explicitly;
- the retired-identity guard passes on the exact tree;
- policy schema `3` validates and exactly five managed profiles match it;
- the installed Skill exposes only the three current runtime references;
- explicit invocation is enforced and implicit invocation is disabled;
- installer fresh/update/add-Solver/idempotent/non-mutating/safety tests pass;
- capability-dedup fixtures prove model + reasoning-effort behavior without treating local-only data as native observation;
- both required Plugin validator runs pass;
- the tested SHA remains unchanged after validation.

If any deterministic check fails, stop release validation, fix only evidence-backed defects, rerun focused checks, then rerun the full deterministic gate on the new exact SHA.

Deterministic execution does not prove real model quality, native capacity, cross-session safety, onboarding quality, Sol Solver value, Terra value, or Final Review yield.

## Product stop line

Do not change these principles merely to make one workload pass:

- main session always owns user intent, authorization, integration, acceptance, and final response;
- zero children is a valid and common result;
- delegation requires concrete value;
- Luna Worker receives writing work only when material behavior decisions are already made;
- material read-only judgment belongs to capable main or Sol Advisor;
- judgment-coupled writing belongs to capable main or Sol Solver;
- Terra receives only a narrow difficult technical question after semantics are stable;
- main-session Sol capability is a dedup optimization, not authority or task taxonomy;
- failure does not create a model ladder;
- blocked work is diagnosed as `contract | judgment | specialist | stalled`;
- a stall permits at most one clean same-role retry when the role remains correct and the packet materially improves;
- main session, Worker, and Solver share one writer domain per canonical checkout;
- delegation depth remains one;
- exact route mismatch fails closed;
- runtime evidence is on demand and missing telemetry remains missing;
- first-use role provisioning completes before delegated code execution begins;
- prior Terra/Solver/recovery/diff size does not itself require Final Review;
- required Final Review needs a fresh Advisor and an unchanged bound artifact;
- ordinary successful tasks do not need a separate orchestration receipt;
- static tests, validators, consultation, and configured intent never substitute for required live evidence.

Do not add Checkpoint 7.

## Checkpoint 1: installation readiness and exact five-role surface

Validate fresh Plugin discovery, explicit `/codex-delegate` invocation, and the first-use readiness boundary.

Exact project roles:

```text
codex_delegate_reader
codex_delegate_worker
codex_delegate_solver
codex_delegate_investigator
codex_delegate_advisor
```

Required behaviors:

- an ordinary task does not implicitly invoke codex delegate;
- first explicit invocation that needs delegation detects missing roles before delegated implementation starts;
- provisioning asks permission, manages only the five current profiles + ownership receipt, and runs `--check`;
- if the current thread cannot see newly provisioned roles, execution stops before child writing and asks for a fresh thread;
- after restart, exact role/profile tuples come from `policy-contract.json`;
- missing or mismatched exact roles do not cross-route.

### Review Checkpoint A

Send only sanitized new evidence and unresolved consequential judgment to the required consultation target below.

## Checkpoint 2: everyday routing quality and Sol dedup

Exercise representative daily-development tasks:

```text
T1 trivial isolated fix
-> main only

T2 large independent read-only trace
-> Reader when context isolation helps

T3 fully specified implementation
-> Worker when delegation helps

T4 material design decision before implementation
-> capable main or Advisor

T5 implementation requires continuing compatibility/state judgment
-> capable main or Solver

T6 semantics stable + one narrow difficult technical question
-> Investigator

T7 large/many-file task with no delegation benefit
-> main only

T8 ambiguous task truth
-> no child writer until main repairs the contract
```

For T4/T5 compare trusted Sol-main `high` or stronger with non-Sol/insufficient-effort main. Verify capability dedup avoids redundant Sol only when trusted model + effort meet the policy reference.

Verify unknown main-route telemetry does not add cost to routine bounded work.

### Review Checkpoint B

Review any repeated unnecessary Agent call, Luna semantic overreach, or missed Sol judgment placement before changing policy.

## Checkpoint 3: blockers, recovery, writer ownership, and scheduling

Validate the compact blocker model:

```text
contract
-> main repairs task truth

judgment
-> capable main / Advisor / Solver

specialist
-> Investigator only after semantics are stable

stalled
-> at most one materially improved clean same-role retry
```

Prove:

- weak Luna quality alone does not trigger Terra;
- a child requesting Terra does not force Terra;
- repeated same failure without new evidence does not create unbounded retry loops;
- valid evidence is reused and repeated discovery is suppressed;
- Main + Worker, Main + Solver, and Worker + Solver do not concurrently write one canonical checkout inside one orchestration;
- isolated worktrees/workspaces may own separate writers;
- independent read-only work can refill native capacity as completions become available.

Use the A/B/C case:

```text
A = slow independent read-only work
B = fast independent read-only work
C = depends only on B
```

Record the actual runtime wait/update surface without inventing event-driven behavior.

### Review Checkpoint C

Distinguish product defects from native-runtime observability/capacity boundaries.

## Checkpoint 4: controlled product-value experiments and Final Review

`evals/` remains a measurement surface. Its schema/workload labels are not runtime ontology.

Use frozen paired workloads to test the real product questions:

- bounded Luna packet vs raw Luna prompt;
- Advisor + Luna handoff vs one Sol Solver for judgment-coupled work;
- Sol-main direct execution vs redundant Sol Solver when capability is already covered;
- unknown-main routine work with and without unnecessary Sol;
- continuing Luna vs correct reroute when material judgment emerges;
- broad stronger restart vs Terra receiving only a genuine technical delta;
- no decorative Final Review vs unnecessary review after process-history-only signals.

Measure acceptance, wrong edits, material judgment violations, correction turns, repeated work, redundant Sol calls, tokens/latency when exposed, and review findings.

Mandatory Final Review lifecycle must prove:

```text
semantic trigger
-> Candidate Ready
-> review_artifact_id
-> fresh codex_delegate_advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

A Sol main must still use a fresh independent Advisor when review is required. Mutation after review invalidates the old verdict.

### Review Checkpoint D

Do not convert one workload result into a permanent model-quality claim. Change role placement only from replicated evidence across representative tasks.

## Checkpoint 5: consent, onboarding friction, and multi-session safety

Validate ordinary explicit-invocation consent:

```text
up to 2 concurrently active justified children
1 writer per canonical checkout inside the orchestration
no silent permission/scope/external/material-compute expansion
```

Validate user experience:

- routine successful tasks do not produce a separate orchestration receipt;
- user is prompted only for material boundary expansion;
- initial role setup occurs before delegated implementation;
- repeated Solver/Advisor/re-review loops eventually require renewed consent when compute materially expands.

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
3. perform a real fresh Plugin installation from that fixed candidate, not from a subsequently moving `main`;
4. start a new thread and confirm `/codex-delegate` discovery and version `0.9.0`;
5. prove implicit invocation is disabled;
6. prove first-use five-profile provisioning/readiness behavior;
7. verify repeat install is idempotent and `--check` is strictly non-mutating;
8. verify managed-profile update/addition only when exact ownership is proven;
9. verify modified/unowned current filenames fail closed and unrelated profiles remain untouched;
10. test same-Codex-home installer races I1-I3;
11. rerun all release-relevant live checkpoints on the immutable candidate with no open reproducible P0/P1.

Same-Codex-home races:

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 two current-profile update/addition attempts compete in one CODEX_HOME
```

Add inter-process serialization/CAS only if a reproducible invariant failure establishes the need.

## Definition of Done for v1.0.0

Release only when one immutable RC passes:

- complete deterministic preflight;
- maintained CI and current official Plugin validation;
- fresh install/update/five-profile lifecycle;
- explicit-invocation and onboarding behavior;
- representative daily routing and capability-dedup cases;
- blocker/retry/Terra/writer safety cases;
- controlled product-value experiments;
- required Final Review lifecycle;
- multi-session and installer-concurrency validation;
- no open reproducible P0/P1.

Quality/cost claims must remain scoped to evidence actually recorded.

Then tag `v1.0.0`, publish the GitHub Release, and make the immutable release ref the recommended stable user-install channel. `main` can remain the development channel after release.

## Required project consultation target

Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E, any P0/P1 candidate, and RC closure.

```text
TARGET_CHATGPT_CONVERSATION_TITLE: R-jed/codex-delegate
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
FAILURE: CONSULTATION_TARGET_UNRESOLVED
```

Do not fuzzy match, guess by recency, create a replacement conversation, or silently fall back to an isolated consultation. Consultation output is model judgment and never counts as runtime/install/product evidence.
