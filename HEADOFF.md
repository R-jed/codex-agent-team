# Codex Delegate Local Runtime Validation Handoff

This is the finite live-validation and v1.0.0 release checklist for codex delegate. Architecture is frozen; current repository work is the 0.7.0 identity/migration closure plus AI-agent documentation. Do not reopen optional architecture tuning.

## Current static baseline candidate

```text
implementation baseline reviewed through: 476fcb45363844e680521d6484a90a81ca1cfd24
product: codex delegate
repository: R-jed/codex-delegate
marketplace/plugin id: codex-delegate
command: /codex-delegate
version: 0.7.0
current roles: codex_delegate_reader / worker / investigator / advisor
current ownership manifest: .codex-delegate-agents.json
architecture: Adaptive Dependency Orchestration + evidence-gated recovery + risk-triggered Final Review Gate
known open reproducible PROJECT P0/P1: none
release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
```

Old `codex_agent_team_*`, `codex-agent-team-*.toml`, and `.codex-agent-team-*.json` values are migration inputs only. A successful 0.7.0 migration must remove that project generation. Do not restore them as current fallback roles.

Before each live checkpoint, fetch `origin/main`, record the exact tested SHA/runtime, and invalidate only evidence whose declared dependencies changed.

## Repository maintenance workflow

For clear, bounded, low-risk maintenance that the repository owner has already authorized, work directly on `main`. Do not create a branch or pull request merely as process ceremony. Inspect current `main`, preserve unrelated work, apply the change, and verify the resulting repository state.

Use a separate branch or pull request only when there is a concrete need for isolation, multiple independent writers, external review, risky experimental work, or an explicit owner request. Remove temporary branches after their work is integrated. Do not accumulate merged documentation/refactor branches that must be cleaned up later.

## Stop line

Do not change these accepted rules merely to make a live test pass:

- no fixed Agent count and no mandatory Luna -> Terra -> Sol pipeline;
- main session owns task-level control and final acceptance;
- completion-driven ready-frontier scheduling when the runtime surface allows it;
- one active writer per canonical physical checkout;
- delegation depth one;
- exact route mismatch fails closed rather than cross-routing;
- configuration is not relabeled as observed runtime evidence;
- deterministic/repository evidence is reused until dependencies change;
- acceptance failure is separate from intervention requirement;
- no universal retry/stall threshold;
- no universal Sol stage;
- required Final Review cannot be silently downgraded;
- deliverable mutation invalidates an old review verdict;
- static tests/Plugin validation/model consultation never substitute for required live evidence.

Do not add Checkpoint 7.

## Checkpoint 1: exact current roles and Runtime Evidence

Test independently:

```text
codex_delegate_reader
codex_delegate_worker
codex_delegate_investigator
codex_delegate_advisor
```

Expected tuples come from `plugins/codex-delegate/policy-contract.json`. Use `plugins/codex-delegate/scripts/runtime-evidence.py` for normalized route/ancestry/permission evidence. Missing/partial observations remain missing/partial; hard read-only requires native permission evidence when material.

### Review Checkpoint A

Send sanitized new evidence and unresolved judgment to the required consultation target below.

## Checkpoint 2: contractability and scope safety

Exercise main-only trivial work, bounded Worker implementation, ambiguous semantics that must not reach a writer, Worker judgment escape, and repository prompt injection. Verify actual changed files, preserved unrelated edits, acceptance commands, and evidence.

### Review Checkpoint B

Send only new evidence and unresolved consequential judgment.

## Checkpoint 3: dependency scheduling, completion events, evidence reuse, intervention, recovery

Use the A/B/C asymmetric case:

```text
A = slow independent dependency
B = fast independent dependency
C = depends only on B
```

When the native surface allows, B should unlock C before A completes. Characterize the strongest wait surface as `barrier_only | per_child_terminal | any_child_update`, record model-mediated polling, and separately record child-progress observability as `none | terminal_only | periodic_summary | structured_live`.

Validate evidence reuse/invalidation, healthy incomplete work, false progress, same-failure stall, A -> B -> A semantic cycle, capability gap to Terra delta, and proposed/effective recovery action separation.

### Review Checkpoint C

Distinguish project defects from native-runtime boundaries using the required consultation target.

## Checkpoint 4: product-value and Final Review experiments

Run controlled pairs for raw-prompt Luna vs bounded-contract Luna, whole-task stronger restart vs Terra unresolved-delta handoff, and representative Final Review lifecycle.

Required Final Review path:

```text
semantic trigger -> Candidate Ready -> fresh codex_delegate_advisor
-> exact review_artifact_id -> ship | fix-first | rethink
```

Also prove `INSUFFICIENT_EVIDENCE` remains unresolved, `fix-first` requires a new artifact and fresh review, `rethink` invalidates affected assumptions, and post-review mutation invalidates old `ship`.

### Review Checkpoint D

Do not turn one benchmark into a permanent architecture constant.

## Checkpoint 5: adaptive resources, consent, multi-session safety, lifecycle

Validate explicit baseline consent (up to two justified concurrent children), larger authorized fan-out without a product hard four-child ceiling, native slot/refill behavior, and declined required review behavior.

Multi-session matrix:

```text
M1 different sessions, different projects/checkouts
M2 different sessions, same repository, isolated worktrees
M3 different sessions, same canonical physical checkout
M4 one writer + one read-only session same checkout
```

Do not add a workspace lock before M3 establishes a reproducible project failure.

### Review Checkpoint E

Any P0/P1 candidate requires immediate adversarial review before remediation is accepted.

## Checkpoint 6: official Plugin install, 0.7.0 migration, installer concurrency

For the selected RC:

1. run the then-current official OpenAI Plugin validator and record its revision;
2. perform real fresh install using `R-jed/codex-delegate` and `codex-delegate@codex-delegate`;
3. start a new thread and confirm `/codex-delegate` discovery and version 0.7.0;
4. authorize profile provisioning and prove only `codex_delegate_*` current roles are exposed;
5. migrate a representative codex delegate 0.6.x profile/ownership generation and prove old project-named profile/manifest/role state is absent after success;
6. test both recognized historical ownership receipts together: disjoint proven hashes must merge into one migration authority, while conflicting hashes for the same file must fail closed before mutation;
7. test an unproven/user-modified old project-named profile and prove fail-closed, no overwrite/delete;
8. test old public `codex-agent-team` Plugin/marketplace removal followed by current fresh install;
9. test same-Codex-home installer races:

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 different managed profile generations compete in one CODEX_HOME
```

Only add inter-process serialization/CAS if a reproducible invariant failure establishes the need.

## Definition of Done for v1.0.0

Release v1.0.0 when maintained CI and current official Plugin validation pass on a fixed RC, real install/update/migration pass, exact required role routing and permission behavior have no open P0/P1, contract/scope simulations pass, scheduling/recovery/resource/multi-session gates have no open P0/P1, required Final Review lifecycle passes, installer concurrency has no open P0/P1, and required product experiments are recorded without unsupported quality/cost claims.

Then feature-freeze, run one fixed RC closure, tag `v1.0.0`, publish the GitHub Release, and move P2/P3 work post-v1.

## Required project consultation target

Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E, any P0/P1 candidate, and RC closure.

```text
TARGET_CHATGPT_CONVERSATION_TITLE: 分支 · 分支 · 项目对比分析
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
FAILURE: CONSULTATION_TARGET_UNRESOLVED
```

Do not fuzzy match, guess by recency, create a replacement conversation, or silently fall back to an isolated consultation. Consultation output is `model_judgment` and never counts as codex delegate runtime/install evidence.
