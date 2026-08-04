# Codex Delegate Local Runtime Validation Handoff

This is the finite live-validation and v1.0.0 release checklist for codex delegate. Architecture and public identity are frozen. Current repository work is limited to validating the accepted current implementation on a real Codex runtime and fixing evidence-backed release blockers.

## Current static baseline candidate

```text
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

The current repository tree uses only the `codex-delegate` / `codex_delegate_*` project identity. Repository history is not part of the current runtime, installation, policy, documentation, or release contract.

Before each live checkpoint, fetch `origin/main`, record the exact tested SHA/runtime, and invalidate only evidence whose declared dependencies changed.

## Repository maintenance workflow

For clear, bounded, low-risk maintenance that the repository owner has already authorized, work directly on `main`. Do not create a branch or pull request merely as process ceremony. Inspect current `main`, preserve unrelated work, apply the change, and verify the resulting repository state.

Use a separate branch or pull request only when there is a concrete need for isolation, multiple independent writers, external review, risky experimental work, or an explicit owner request. Remove temporary branches after their work is integrated. Do not accumulate merged documentation/refactor branches that must be cleaned up later.

## Deterministic execution preflight

Complete this gate on the exact current `main` revision before treating any live-runtime checkpoint as release evidence.

Record the exact Git SHA, Python version, validator revision where applicable, commands, exit codes, and concise outputs in `LOCAL_VALIDATION_REPORT.md`.

Required deterministic execution:

```bash
python -m pytest tests/test_identity_cleanup.py -q
python -m pytest tests/test_install_agents.py tests/test_installer_safety.py tests/test_plugin_packaging.py tests/test_policy.py tests/test_runtime_truth_policy.py tests/test_headoff.py tests/test_readme_user_facing.py -q
python -m pytest -q
```

Also run the repository's pinned official Plugin validator path used by maintained CI, then run the then-current official OpenAI Plugin validator against `plugins/codex-delegate` and record the validator revision.

The deterministic gate passes only when:

- every command above exits successfully;
- the complete pytest suite has no failures or errors;
- any skips, xfails, or warnings that affect release claims are explicitly reviewed and recorded rather than ignored;
- the retired-identity tree guard passes on the exact tested tree;
- focused installer/profile lifecycle regressions pass;
- Plugin packaging and policy contracts pass;
- both required Plugin validator runs pass;
- the tested SHA remains unchanged after validation.

If any deterministic check fails, stop the release-validation sequence, classify the failure, fix only evidence-backed project defects, rerun the affected focused checks, then rerun the complete deterministic gate on the new exact SHA. Do not carry forward a green result from an earlier SHA.

Deterministic execution passing is necessary for release candidacy but does not prove native runtime routing, permissions, concurrency, lifecycle, or product-value behavior. Those remain owned by Checkpoints 1–6.

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

## Checkpoint 6: official Plugin install and installer lifecycle

For the selected RC:

1. run the then-current official OpenAI Plugin validator and record its revision;
2. perform real fresh install using `R-jed/codex-delegate` and `codex-delegate@codex-delegate`;
3. start a new thread and confirm `/codex-delegate` discovery and version 0.7.0;
4. authorize profile provisioning and prove only the four current `codex_delegate_*` project roles are exposed by the managed configuration;
5. verify repeat install is idempotent and `--check` is strictly non-mutating;
6. verify a previously project-managed current profile can update only when the current ownership receipt proves its exact prior bytes;
7. verify a modified/unowned current filename fails closed rather than being overwritten;
8. verify unrelated Agent profiles remain untouched;
9. test same-Codex-home installer races:

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 two current-profile update attempts compete in one CODEX_HOME
```

Only add inter-process serialization/CAS if a reproducible invariant failure establishes the need.

## Definition of Done for v1.0.0

Release v1.0.0 when the deterministic execution preflight passes on the fixed RC, maintained CI and current official Plugin validation pass on that same RC, real fresh install/update/profile lifecycle validation passes, exact required role routing and permission behavior have no open P0/P1, contract/scope simulations pass, scheduling/recovery/resource/multi-session gates have no open P0/P1, required Final Review lifecycle passes, installer concurrency has no open P0/P1, and required product experiments are recorded without unsupported quality/cost claims.

Then feature-freeze, run one fixed RC closure, tag `v1.0.0`, publish the GitHub Release, and move P2/P3 work post-v1.

## Required project consultation target

Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E, any P0/P1 candidate, and RC closure.

```text
TARGET_CHATGPT_CONVERSATION_TITLE: R-jed/codex-delegate
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
FAILURE: CONSULTATION_TARGET_UNRESOLVED
```

Do not fuzzy match, guess by recency, create a replacement conversation, or silently fall back to an isolated consultation. Consultation output is `model_judgment` and never counts as codex delegate runtime/install evidence.
