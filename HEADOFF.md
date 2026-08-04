# Codex Delegate Local Runtime Validation Handoff

This is the finite deterministic/live-validation and v1.0.0 release checklist for codex delegate after the Routing V4 architecture refactor.

Routing V4 implementation is the current candidate architecture. It is not yet release-validated. Do not reopen model-routing design from preference or anecdote during validation; change it only when deterministic or controlled live evidence establishes a defect or falsifies a routing hypothesis.

## Current candidate baseline

```text
product: codex delegate
repository: R-jed/codex-delegate
marketplace/plugin id: codex-delegate
command: /codex-delegate
version: 0.8.0
current roles: codex_delegate_reader / worker / solver / investigator / advisor
current ownership manifest: .codex-delegate-agents.json
architecture: Routing V4 dependency classification + main judgment coverage + evidence-driven reclassification + consequence-driven Final Review
known open reproducible PROJECT P0/P1: none established on exact current tree
release posture: HOLD FOR RELEASE / DETERMINISTIC + LIVE V4 VALIDATION PENDING
```

The current repository tree uses only the `codex-delegate` / `codex_delegate_*` identity. Repository history is outside the current runtime, installation, policy, documentation, and release contract.

Before every validation checkpoint, fetch `origin/main`, record the exact tested SHA/runtime, and invalidate evidence whose declared dependencies changed.

## Repository maintenance workflow

For clear, bounded, low-risk maintenance already authorized by the repository owner, work directly on `main` after inspecting current state and preserving unrelated work. Do not create a branch or PR as ceremony.

Use isolation only when multiple independent writers, risky experimentation, external review, or an explicit owner request provides a concrete reason. Remove temporary branches after integration.

## Deterministic execution preflight

Complete this gate on one exact current `main` SHA before treating live-runtime results as release evidence.

Record exact Git SHA, Python version, validator revision where applicable, commands, exit codes, skips/xfails/warnings that affect claims, and concise outputs in `LOCAL_VALIDATION_REPORT.md`.

Required deterministic execution:

```bash
python -m pytest tests/test_identity_cleanup.py -q
python -m pytest tests/test_install_agents.py tests/test_installer_safety.py tests/test_plugin_packaging.py tests/test_policy.py tests/test_runtime_evidence.py tests/test_runtime_truth_policy.py tests/test_behavioral_evals.py tests/test_headoff.py tests/test_readme_user_facing.py -q
python -m pytest -q
```

Also run:

1. the repository-pinned official Plugin validator used by maintained CI;
2. the then-current official OpenAI Plugin validator against `plugins/codex-delegate`, recording its exact revision.

The deterministic gate passes only when:

- all required commands exit successfully;
- the complete pytest suite has no failures or errors;
- release-relevant skips, xfails, and warnings are reviewed explicitly;
- the retired-identity guard passes on the exact tree;
- policy schema `2` and routing/eval schema `4.0` validate;
- all five current profiles match `policy-contract.json`;
- installer fresh/adopt/update/add-Solver/idempotent/non-mutating/safety tests pass;
- main-session runtime-evidence fixtures prove `covered | uncovered | unknown` semantics without inference from local-only data;
- both required Plugin validator runs pass;
- tested SHA remains unchanged after validation.

If any deterministic check fails, stop release validation, classify the defect, fix only evidence-backed project issues, rerun focused checks, then rerun the complete deterministic gate on the new exact SHA. Do not carry forward a green result from an earlier SHA.

Deterministic execution is necessary for release candidacy. It does not prove real model quality, main-route observability, native concurrency, Sol Solver value, Terra value, cross-session safety, or Final Review yield.

## Routing V4 stop line

Do not change these rules merely to make a live workload pass:

- main session always owns task-level authority and final acceptance;
- main-session authority is independent of model identity, while judgment coverage can affect compute placement;
- `contractable` does not imply Luna-suitable;
- Luna Worker owns only standardized `bounded_execution`;
- Sol Solver owns `judgment_coupled_execution` only when a child is useful and the main session does not already cover normal Sol judgment capability;
- Sol Advisor owns bounded `judgment` uplift and fresh independent Final Review;
- Terra Investigator owns only `technical_investigation` after semantic intent is stable;
- unknown main-session model does not automatically route routine work to Sol;
- failure causes reclassification from new evidence, not a fixed model ladder;
- `CONTRACT_GAP`, `JUDGMENT_REQUIRED`, `TECHNICAL_GAP`, and `EXECUTION_STALL` are signals, not automatic transitions;
- one canonical checkout has at most one active writing project Agent; Worker and Solver are both writers;
- no fixed Agent count or mandatory Luna -> Terra -> Sol path;
- delegation depth remains one;
- exact route mismatch fails closed;
- configuration never becomes observed runtime evidence;
- deterministic/repository evidence is reused until its dependencies change;
- process history such as Terra/Solver use or recovery is not itself a Final Review trigger;
- required Final Review cannot be silently downgraded and a deliverable mutation invalidates the old verdict;
- static tests, Plugin validation, and model consultation never substitute for required live evidence.

Do not add Checkpoint 7.

## Checkpoint 1: five exact roles and main/child Runtime Evidence

Validate exact discovery/routing for:

```text
codex_delegate_reader
codex_delegate_worker
codex_delegate_solver
codex_delegate_investigator
codex_delegate_advisor
```

Expected tuples come from `plugins/codex-delegate/policy-contract.json`.

Also characterize main-session route evidence on the current Codex runtime:

```text
native Sol main metadata       -> main_judgment_coverage = covered
native non-Sol main metadata   -> main_judgment_coverage = uncovered
missing/partial/conflict       -> main_judgment_coverage = unknown
```

Use `plugins/codex-delegate/scripts/runtime-evidence.py`. Never relabel local/configured data as native main-session observation. For child routes keep route, ancestry, and permission evidence typed separately.

### Review Checkpoint A

Send only sanitized new evidence and unresolved consequential judgment to the required consultation target below.

## Checkpoint 2: classifier and quality-placement behavior

Exercise representative daily-development tasks:

```text
T1 trivial isolated fix                         -> main only
T2 large read-only trace                        -> Reader
T3 fully specified implementation               -> Worker
T4 contractable but judgment-coupled write      -> Sol main or Solver depending on main coverage
T5 material pre-write semantic decision         -> Sol main or Advisor depending on main coverage
T6 unknown main + routine bounded implementation -> Worker, no automatic Sol
T7 unknown main + material judgment             -> Advisor/Solver as appropriate
T8 ambiguous task truth                         -> no writer until contract truth is repaired
```

For T4 run both trusted Sol-main and trusted non-Sol-main variants. Verify the Sol-main path does not spawn redundant capability-uplift Sol solely to recreate capability already present.

Inspect actual files, judgment calls, acceptance evidence, and resource decisions. A task being large or contractable must not force Luna.

### Review Checkpoint B

Review any classifier misroute or repeated unnecessary Sol call before changing policy.

## Checkpoint 3: reclassification, Terra boundary, scheduling, and evidence reuse

Validate reclassification from actual execution evidence:

```text
bounded local defect
-> focused Worker correction

material semantic choice emerges during Worker execution
-> JUDGMENT_REQUIRED
-> judgment or judgment_coupled_execution

semantics stable + narrow difficult technical uncertainty
-> TECHNICAL_GAP
-> Investigator receives only that delta

claimed technical gap while semantics remain unresolved
-> no Terra; return to judgment

same-role repetition while classification remains valid
-> EXECUTION_STALL
-> optional clean same-role restart
```

Prove a child requesting Terra does not force Terra. Prove weak Luna quality alone does not become technical escalation.

Also run the A/B/C scheduling case:

```text
A = slow independent dependency
B = fast independent dependency
C = depends only on B
```

Characterize the strongest observed wait surface as `barrier_only | per_child_terminal | any_child_update`, and child-progress observability separately as `none | terminal_only | periodic_summary | structured_live`.

Validate evidence reuse/invalidation, duplicate-dependency suppression, semantic-cycle detection, and proposed/effective action separation.

### Review Checkpoint C

Distinguish Routing V4 defects from native-runtime observability/capacity boundaries.

## Checkpoint 4: controlled Routing V4 product-value experiments and Final Review

Use frozen workloads from `evals/behavioral-workloads.json` and schema `4.0`. Required controlled pairs include:

```text
raw_prompt_luna vs bounded_luna
advisor_then_luna vs sol_solver on non-Sol judgment-coupled work
main_session_only vs sol_solver on the same judgment-coupled work with Sol main
bounded_luna vs unnecessary sol_solver when main coverage is unknown but work is routine
bounded_luna vs adaptive_routing_v4 when material judgment emerges during execution
external_baseline vs terra_delta on a genuine technical delta
adaptive_routing_v4 vs adaptive_routing_v4_final_review on process-history negative control
```

Do not claim a winner from architecture preference. Record success, acceptance, wrong edits, material judgment violations, correction turns, reclassification events, redundant Sol calls, tokens/latency when exposed, and repeated work.

Mandatory Final Review lifecycle must prove:

```text
semantic trigger
-> Candidate Ready
-> exact review_artifact_id
-> fresh codex_delegate_advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Required direct trigger populations include public contract, security/authorization, persistent state, data integrity, concurrency semantics, material migration, user-requested review, and `verification_gap`.

Negative controls must prove Terra use, Solver use, recovery, or a large diff alone does not force review when no semantic trigger remains.

A Sol main must still use a fresh independent Advisor when the Final Review Gate is required.

### Review Checkpoint D

Do not convert one workload result into a permanent model-quality constant. Revise routing only from replicated evidence across representative task classes.

## Checkpoint 5: adaptive resources, consent, writer safety, and multi-session lifecycle

Validate explicit baseline consent, larger authorized fan-out, native slot/refill behavior, implicit Sol-cost consent, and declined required-review behavior.

Multi-session matrix:

```text
M1 different sessions, different projects/checkouts
M2 different sessions, same repository, isolated worktrees
M3 different sessions, same canonical physical checkout
M4 one project writer + one read-only session same checkout
M5 Worker + Solver proposed concurrently in same checkout
```

M5 must fail the project one-writer invariant unless they use genuinely isolated workspaces.

Do not add a workspace lock before M3/M5 establish a reproducible project-side coordination failure that policy alone cannot safely handle.

### Review Checkpoint E

Any reproducible P0/P1 candidate requires adversarial review before remediation is accepted.

## Checkpoint 6: official Plugin install and five-profile lifecycle

For the selected RC:

1. run the then-current official OpenAI Plugin validator and record its revision;
2. perform a real fresh install using `R-jed/codex-delegate` and `codex-delegate@codex-delegate`;
3. start a new thread and confirm `/codex-delegate` discovery and version `0.8.0`;
4. authorize provisioning and prove only the five current project roles are managed/exposed by this Plugin configuration;
5. verify repeat install is idempotent and `--check` is strictly non-mutating;
6. verify a proven previous current-generation receipt can add the new Solver profile without rewriting unchanged existing managed profiles;
7. verify a previously project-managed current profile can update only when the receipt proves exact prior bytes;
8. verify modified/unowned current filenames fail closed;
9. verify unrelated Agent profiles remain untouched;
10. test same-Codex-home installer races:

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 two current-profile update/addition attempts compete in one CODEX_HOME
```

Add inter-process serialization/CAS only if reproducible invariant failure establishes the need.

## Definition of Done for v1.0.0

Release v1.0.0 only when one fixed RC passes the complete deterministic preflight, maintained CI, current official Plugin validation, real fresh install/update/five-profile lifecycle, exact current role routing, main-session coverage characterization, classifier/reclassification safety cases, scheduling/resource/multi-session gates, required Final Review lifecycle, installer concurrency, and the required controlled Routing V4 product experiments with no open reproducible P0/P1.

Quality/cost claims must be limited to the named workloads and runtime evidence actually recorded.

Then feature-freeze that fixed RC, perform one final closure run, tag `v1.0.0`, publish the GitHub Release, and move P2/P3 work post-v1.

## Required project consultation target

Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E, any P0/P1 candidate, and RC closure.

```text
TARGET_CHATGPT_CONVERSATION_TITLE: R-jed/codex-delegate
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
FAILURE: CONSULTATION_TARGET_UNRESOLVED
```

Do not fuzzy match, guess by recency, create a replacement conversation, or silently fall back to an isolated consultation. Consultation output is `model_judgment` and never counts as codex delegate runtime/install/product evidence.
