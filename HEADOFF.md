# Codex Delegate Local Runtime Validation Handoff

This file is the authoritative execution checklist for local validation and the finite v1.0.0 release phase of **Codex Delegate**.

The v0.5.0 architecture cycle is closed. The remaining job is finite: complete the mandatory live gates, resolve only release-blocking defects, run one fixed release-candidate closure pass, then publish v1.0.0.

Do not reopen architecture or optimization work after the Definition of Done is satisfied.

## Current checkpoint

Current merged static baseline:

```text
origin/main: 00e7a2a340e6bc57ea15460f45721b571f8078fd
product: Codex Delegate 0.5.0
architecture: Adaptive Dependency Orchestration
PR #22 static validation: PASS
pytest on Ubuntu / Python 3.11: 119 passed
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
Plugin manifests: PASS
managed profile install / --check / idempotent reinstall: PASS
known open reproducible PROJECT P0/P1 defects: none
release posture: HOLD FOR RELEASE / VALIDATION INCOMPLETE
```

Last accepted live production-behavior baseline:

```text
production behavior tested: c6020db903b35f0d57677b131bf35b0580144ab9
Codex runtime tested so far: 0.146.0
platform tested so far: Apple Silicon macOS 27.0
```

The static v0.5.0 baseline is current repository evidence. The `c6020db...` revision remains the last accepted live-runtime evidence baseline. Never relabel static CI as live Codex runtime proof.

Before every live checkpoint:

1. fetch `origin/main`;
2. record the actual tested SHA in `LOCAL_VALIDATION_REPORT.md`;
3. inspect intervening production changes;
4. reuse older evidence only when its declared dependencies remain valid.

Status notation:

- `[x]` means reproducible evidence exists in merged repository history or `LOCAL_VALIDATION_REPORT.md`.
- `[ ]` means the gate remains required.
- `PARTIAL` means some evidence exists but the full acceptance condition has not been characterized.

## v0.5.0 control model

```text
main session owns user intent, dependency state, scheduling, evidence, integration, and acceptance
no model is a mandatory stage
no fixed Agent count and no product-level hard child ceiling
Dependency Ledger -> ready frontier -> smallest useful scheduling wave
explicit /codex-delegate baseline -> up to 2 concurrently active justified children without another prompt
larger simultaneous fan-out -> consent unless already authorized
actual concurrency -> ready dependencies + workspace safety + exact routes + native runtime slots
native slot shortage -> queue/serialize ready work, never cross-route or duplicate work
Luna Max -> bounded execution
Terra XHigh -> genuine unresolved complex technical delta
Sol High -> selective fresh-context judgment/review
one active writing Worker per canonical workspace
delegation depth = 1
valid evidence is reused until its dependencies are invalidated
execution recovery is evidence-driven, with no universal retry count
```

Resource scopes remain separate:

```text
main-session scope
-> Dependency Ledger, ready frontier, consent state, active child set

workspace scope
-> write ownership for one canonical physical checkout or runtime-backed isolated worktree

Codex-home scope
-> shared semantic Agent profiles and ownership manifest
```

## Stop line

Do not change these rules merely to make a live test pass:

- no mandatory Luna -> Terra -> Sol pipeline;
- no fixed team size, default child target, or product hard child ceiling;
- no machine-wide or account-wide Agent cap inferred from one Codex build;
- no larger simultaneous fan-out without consent unless broad parallel work is already authorized;
- no silent large serial fan-out used to evade material compute-expansion consent;
- no duplicate Agent call for an already-running unchanged dependency;
- no generic Terra whole-task rerun because Luna quality looks weak;
- no unchanged retry simply because an Agent failed;
- no universal retry-count rule;
- no model self-report, confidence language, or file write treated as progress by itself;
- no weakening the acceptance oracle because a lane failed it;
- no silent expansion of decision rights through model escalation;
- no more than one active writing Worker in one canonical shared checkout;
- no file-level partitioning used to justify multiple writers in one physical checkout;
- no child-created descendants;
- no cross-role substitution when an exact project profile is unavailable;
- no configured route fact presented as runtime observation;
- no incomplete expected route accepted as exact runtime proof;
- no missing runtime evidence converted to affirmative success;
- no systematic rediscovery of still-valid deterministic or repository evidence;
- no project-wide global writer mutex that blocks independent workspaces;
- no workspace-lock daemon or installer lock before reproducible live evidence establishes the need;
- no manual rename of managed Agent profiles or ownership manifests merely to match the product brand;
- no repository/package-id migration before real installed-Plugin upgrade and fresh-install behavior is characterized;
- no performance, quality, cost, concurrency-capacity, or recovery claim without measured named workloads and runtime versions.

If a native Codex limitation makes a project invariant impossible, record the exact runtime behavior and ownership classification before changing policy.

# Completed repository work

## A. Core architecture and policy

- [x] Main session remains the single control plane and final acceptance owner.
- [x] Delegation Benefit Gate and Contractability Gate remain upstream of model-specific delegation.
- [x] Delegation Contract binds each child to a dependency id, interfaces/dependencies, acceptance, verification, and execution evidence.
- [x] Shared Evidence State preserves deterministic/repository facts while dependencies remain valid.
- [x] v0.5.0 defines an in-session Dependency Ledger with `pending | ready | running | satisfied | blocked | invalidated` state.
- [x] The previous default-child and hard-four scheduling invariants are removed.
- [x] Routing schema no longer limits static node arrays to four children.
- [x] Static routing cases include an authorized five-reader fan-out.
- [x] Static routing cases include native-slot pressure where excess ready dependencies queue without role substitution.
- [x] The two-child number exists only as the normal no-extra-consent simultaneous fan-out boundary.
- [x] Material serial compute expansion is also consent-gated.
- [x] One-writer-per-canonical-workspace and depth-one delegation remain hard safety invariants.
- [x] Codex-home profile generation remains shared configuration and fails closed on exact-route mismatch.

## B. Execution-progress and recovery policy

- [x] `execution-progress.md` separates execution evidence, progress/stall signals, and routing decisions.
- [x] File writes, confidence, narration, repeated commands, and repeated discovery do not establish progress by themselves.
- [x] Failure signatures and progress signals are part of execution returns.
- [x] `EXECUTION_STALL` is distinct from capability, contract, mechanical, and judgment gaps.
- [x] Clean same-lane restart preserves current artifact, valid evidence, failure signature, unresolved delta, acceptance, and `DO NOT REDO` facts while dropping dead-end narration/private reasoning.
- [x] No universal retry count is encoded.
- [x] An unchanged contract is not resent after failure.
- [x] Evidence-supported capability gaps go to Terra before repeated same-lane restart.
- [x] Sol judgment/review uses compressed fresh context by default and remains selective.

## C. Exact semantic routes and distribution

- [x] Reader -> GPT-5.6 Luna / max / read-only.
- [x] Worker -> GPT-5.6 Luna / max / workspace-write.
- [x] Investigator -> GPT-5.6 Terra / xhigh / read-only.
- [x] Advisor -> GPT-5.6 Sol / high / read-only.
- [x] Product name is `Codex Delegate` and canonical entry point is `/codex-delegate`.
- [x] v0.5.0 keeps repository/package/profile compatibility identifiers during the pre-v1 migration window.
- [x] Installer ownership rules fail closed for user-modified or unproven profiles.

## D. Historical live evidence carried forward

- [x] Marketplace registration succeeded through the documented Git source.
- [x] A real v0.3.0 Plugin installation succeeded.
- [x] Missing project profiles failed closed instead of cross-routing.
- [x] Real profile provisioning created four profiles plus one ownership manifest.
- [x] Installer `--check` succeeded in the tested environment.
- [x] Fresh-task role discovery exposed all four semantic roles after provisioning.
- [x] Reader spawned with `fork_turns=none` and local rollout inspection reported Luna Max, read-only sandbox, expected parent, and runtime 0.146.0.
- [x] Reader evidence remains L1 local corroboration because independent native attestation was not separately exposed.
- [x] CAT-LOCAL-001 direct Codex-home endpoint symlink defect is closed in production history.

Historical evidence is revalidated only where v0.5.0 changed a dependency of the claim.

# Pending live validation

Execute the remaining gates in order. Update `LOCAL_VALIDATION_REPORT.md` after each checkpoint. Do not expand the checklist merely because another optimization is imaginable.

## Checkpoint 1: exact roles and Runtime Truth

### 1. Exact custom-Agent route matrix

Run tiny bounded responsibilities with explicit `fork_turns=none`.

- [x] Reader: Luna Max / read-only / parent matched / L1 local corroboration on historical live baseline.
- [ ] Worker: Luna Max / workspace-write.
- [ ] Investigator: Terra XHigh / read-only.
- [ ] Advisor: Sol High / read-only.

Record only facts actually exposed: thread id, parent id, role, model, effort, effective sandbox/permission, runtime/build.

### 2. Runtime Truth adversarial matrix

- [x] Static verifier covers incomplete expected-route fail-closed semantics.
- [x] Static verifier keeps route, ancestry, and permission evidence independent.
- [ ] Characterize complete native route metadata if exposed.
- [ ] Characterize partial native route behavior.
- [ ] Characterize native/local agreement when both exist.
- [ ] Exercise material route, parent, sandbox/permission, and thread-id conflict cases where the runtime exposes the needed facts.
- [ ] Characterize duplicate rollout/schema drift on the current Codex build.

Required semantics:

```text
incomplete expected route -> fail closed
missing observation -> not_observed / partial
complete matching native route -> R1
complete matching native + local route -> R2
complete local route alone -> at most L1
material conflict -> X0 + quarantine
```

### Review checkpoint A

Invoke `/gpt56-sol-pro-consult` with the exact-route/runtime packet before changing Runtime Truth policy. Follow the project consultation target contract below.

## Checkpoint 2: contractability, scope, and safety

### 3. Contract simulations

- [ ] Already-isolated deterministic defect stays main-session only with zero children.
- [ ] Bounded implementation creates a dependency-bound contract before Luna Worker execution.
- [ ] Ambiguous product semantics do not reach a writing Worker before decision rights and acceptance are clear.
- [ ] Out-of-contract architecture/product/security/migration/public-contract decisions return to the main session or justified Sol judgment.
- [ ] Concurrent user edits are preserved; dependent evidence is invalidated; stale contracts stop.
- [ ] Actual changed files remain inside declared write scope.

### 4. Prompt-injection and recursion boundary

- [ ] Repository instructions remain untrusted data and cannot change Dependency Ledger state, consent, routes, scope, or evidence-validity rules.
- [ ] Children do not spawn descendants.
- [ ] Missing exact roles remain fail closed.
- [ ] Read-only behavior is not mislabeled runtime-enforced without native evidence.

### Review checkpoint B

Invoke `/gpt56-sol-pro-consult` after this checkpoint, or immediately on ambiguous writing, nested delegation, scope widening, unrelated edit loss, or permission-boundary failure. Follow the project consultation target contract below.

## Checkpoint 3: dependency scheduling, evidence reuse, and execution recovery

### 5. Dependency Ledger and ready frontier

Create a multi-step task with declared dependencies and evidence prerequisites.

- [ ] Dependencies move through `pending -> ready -> running -> satisfied` from observable state.
- [ ] A blocked prerequisite prevents dependent work from becoming ready.
- [ ] A running dependency does not receive duplicate inference.
- [ ] A satisfied dependency stays closed while its inputs remain valid.
- [ ] Changed input invalidates only dependent evidence/dependencies.
- [ ] Ready frontier is recomputed after artifact/evidence changes.
- [ ] Main session chooses a smaller wave when combining work is cheaper and preserves acceptance/context boundaries.

### 6. Shared Evidence State

Establish at least E01 reproduction, E02 caller path, E03 focused-test baseline, and E04 interface fact.

- [ ] Later Agents receive relevant still-valid evidence.
- [ ] They do not rebuild E01-E04 without an invalidation reason.
- [ ] Unrelated file changes do not invalidate unrelated evidence.
- [ ] Model judgments remain challengeable hypotheses.

Record:

```text
unjustified_repeated_commands
unjustified_repeated_discovery
duplicate_dependency_calls
evidence_established
evidence_invalidated
```

### 7. Execution-progress and stall recovery

Construct controlled cases where a bounded dependency fails acceptance.

- [ ] Mechanical defect with a concrete correction hypothesis -> focused Luna correction.
- [ ] Contract gap -> main session repairs the contract.
- [ ] Same failure signature with no new evidence -> execution stall, not blind unchanged retry.
- [ ] Clean same-lane restart uses fresh context and carries current artifact, valid evidence, failure signature, unresolved delta, acceptance, and `DO NOT REDO`.
- [ ] Clean restart does not repeat valid repository discovery merely to rebuild context.
- [ ] Evidence-supported capability gap -> Terra receives the unresolved delta before repeated same-lane retry.
- [ ] Judgment gap -> main session or bounded Sol decision.
- [ ] Acceptance oracle is never weakened to make a stalled lane pass.

Record:

```text
execution_stall_events
clean_same_lane_restarts
unjustified_retry_calls
same_failure_without_new_evidence
```

### Review checkpoint C

Invoke `/gpt56-sol-pro-consult` with Dependency Ledger, evidence-reuse, stall, clean-restart, and first Terra-delta evidence before modifying scheduling/recovery policy. Follow the project consultation target contract below.

## Checkpoint 4: product-value experiments

### 8. Raw prompt versus compiled contract

Primary controlled comparison:

```text
A: raw user prompt -> Luna Max
B: same prompt -> main session compiles Delegation Contract -> Luna Max
```

Freeze every workload before a pair. Record:

```text
workload_definition_hash
repo_revision
repeat_index
main_session_route
worker_route
permissions_fingerprint
tool_surface_fingerprint
acceptance_rubric_id
Codex runtime version
```

- [ ] Produce at least one valid pair before scaling.
- [ ] Target representative repeated pairs if cost permits.
- [ ] Measure correctness, scope errors, regressions, correction work, tokens/latency when exposed, and evidence-reuse waste.

### 9. Terra delta experiment

Compare on a real capability-gap workload:

```text
A: whole-task Terra restart
B: Terra receives unresolved delta + valid evidence + artifact + failure signature + DO NOT REDO
```

Do not claim an advantage until paired evidence supports it.

### 10. Selective fresh-context Sol experiment

Compare on a consequential judgment/review workload:

```text
A: contract -> Luna
B: contract -> Luna -> fresh-context selective Sol
```

Measure material catches, false positives, total correction work, and latency/cost when exposed.

### Review checkpoint D

Invoke `/gpt56-sol-pro-consult` with the first valid product-value pairs. Do not tune Luna/Terra/Sol routes pre-v1 unless a reproducible correctness/safety regression makes the frozen route unusable. Follow the project consultation target contract below.

## Checkpoint 5: adaptive resources, multi-session safety, and lifecycle

### 11. Consent boundary and no product hard cap

Run a deterministic/static + live matrix:

```text
F0 no useful delegated dependency
-> 0 children is valid

F1 one useful dependency
-> one child may run when justified

F2 two independent ready dependencies
-> both may run inside explicit-command baseline when safe

F3 three or more independent ready dependencies, no broad-fanout authorization
-> ask consent before larger simultaneous fan-out

F4 at least five independent read-only ready dependencies, broad fan-out explicitly authorized
-> Codex Delegate imposes no hard 4 ceiling
-> spawn only as many as current native capacity safely allows
-> queue the remainder
```

Record:

```text
ready_dependencies
peak_active_children
observed_child_capacity
runtime_slot_waits
consent_prompts
duplicate_dependency_calls
```

Do not infer a universal native maximum from one version/build.

### 12. Slot recovery and lifecycle

- [ ] Confirm queued ready dependencies become runnable as prior children close.
- [ ] Confirm no orphan/ghost dependency ownership remains after completion, failure, cancellation, or close.
- [ ] Confirm slot pressure never triggers cross-route substitution or duplicate work.
- [ ] Run at least 10 bounded spawn/close cycles across representative read-only and writing work where practical.
- [ ] Characterize cancellation and failed-child slot recovery on the tested runtime.

### 13. Workspace-scoped one-writer and multi-session matrix

```text
M1 different sessions, different projects/checkouts
-> both writers should be allowed

M2 different sessions, same repository, different runtime-backed isolated worktrees
-> both writers allowed only when real isolation is evidenced

M3 different sessions, same canonical physical checkout
-> never accept two simultaneous writing Workers

M4 one writing session plus one read-only session on the same checkout
-> read evidence must be refreshed/invalidated when the writer changes dependencies
```

Do not implement a workspace lock before M3 establishes a reproducible failure. If M3 fails, classify it as a PROJECT/P1 candidate and use the smallest canonical-workspace coordination mechanism that preserves independent-workspace concurrency.

## Checkpoint 6: installer and version migration

### 14. Real installed-Plugin migration

- [ ] Starting from real v0.3.x Codex Agent Team, update through the documented marketplace source and confirm one Codex Delegate package path with `/codex-delegate`.
- [ ] Starting from real v0.4.x Codex Delegate, update to v0.5.0 and confirm the exactly owned four managed profile files upgrade to the v0.5.0 instructions.
- [ ] Confirm user-modified/unproven profiles remain untouched and the affected route fails closed.
- [ ] Confirm fresh v0.5.0 install presents `Codex Delegate`, exposes `/codex-delegate`, and follows first-run consent.
- [ ] Characterize old `/codex-agent-team` invocation after upgrade. Do not assume alias behavior.
- [ ] Verify installed metadata reports `0.5.0` while compatibility package id remains `codex-agent-team`.
- [ ] Decide repository/package slug migration only from real install/upgrade evidence. Cosmetic alignment cannot block v1.

### 15. Filesystem and concurrent installer matrix

```text
I1 same clean CODEX_HOME, two same-generation installers concurrently
-> exact converged state or one safe refusal
-> four current profiles + one exact manifest
-> no corruption or staging/backup debris

I2 one installer is forced to fail after mutation begins while a peer operation succeeds
-> failed rollback must not overwrite peer-success state

I3 different managed profile generations compete in one CODEX_HOME
-> safe refusal or exact characterized convergence
-> no silent mixed generation
```

Do not add an inter-process installer lock merely because races are theoretically possible. Add coordination only after a reproducible project-owned failure.

### Review checkpoint E

Invoke `/gpt56-sol-pro-consult` after Checkpoints 5 and 6 are characterized. Include adaptive fan-out, observed native capacity, slot recovery, M1-M4, I1-I3, and migration evidence. Follow the project consultation target contract below.

# Defect triage

Classify every live failure by severity and ownership.

```text
P0
unsafe mutation, credential boundary failure, data loss, false security proof, or unrecoverable installer corruption

P1
core orchestration invariant fails, wrong route accepted, unsafe multiple writers, nested delegation, contractability bypass, duplicate dependency ownership causing material wrong execution, consent boundary bypass, or documented install path broken

P2
nonblocking UX, inefficiency, maintenance drift, telemetry/schema compatibility, or recoverable resource waste

P3
cosmetic, optional, or speculative improvement
```

Ownership:

```text
PROJECT
UPSTREAM_CODEX_RUNTIME
ENVIRONMENT
TEST_FIXTURE
UNKNOWN
```

After mandatory live gates are characterized, only reproducible PROJECT P0/P1 or a P2 that directly blocks a mandatory gate can delay v1.0.0. Other P2/P3 items move to the post-v1 backlog.

Any P0/P1 candidate must be sent immediately through `/gpt56-sol-pro-consult` using the exact project consultation target before broadening architecture or threat-model scope.

# Definition of Done for v1.0.0

v1.0.0 is done when all 12 conditions are satisfied:

1. Every mandatory live gate above is complete, or an upstream/runtime limitation is explicitly characterized with a documented fail-closed project invariant.
2. No reproducible PROJECT P0/P1 remains open.
3. The normal user path works: marketplace -> Plugin install/update -> profile readiness -> fresh-task discovery -> bounded delegation -> verification -> visible completion.
4. One-writer, depth-one, exact-route fail-closed, contractability, prompt-injection, and untrusted-content boundaries survive live tests.
5. Adaptive scheduling is evidenced: no fixed Agent target, no product hard 4 ceiling, no duplicate running dependency, >2 simultaneous fan-out is consent-gated, and runtime slot pressure queues safely.
6. Execution recovery is evidenced: unchanged retry is rejected, clean same-lane restart preserves valid task truth, and evidence-supported capability gaps use Terra delta escalation.
7. Raw-prompt versus compiled-contract evaluation produces valid paired data with no systematic acceptance-quality regression on representative bounded work.
8. Shared Evidence State shows no systematic full-task rediscovery while dependencies remain valid.
9. Terra delta and selective Sol may remain conservative if economics are inconclusive, provided no reproducible correctness/safety regression exists and public claims remain measured.
10. Luna Max / Terra XHigh / Sol High remain the frozen v1 routing baseline; route/effort optimization moves to v1.x unless a release-blocking defect requires change.
11. Full deterministic CI is green on the exact release-candidate content, and a fresh-clone clean-Codex-home smoke covers Plugin install, four-role discovery, Worker/read-only routes, adaptive fan-out/slot behavior, one-writer/depth-one, and installer critical safety.
12. User docs describe observed limitations without unmeasured claims; remaining P2/P3 work is moved post-v1 and cannot reopen the pre-release architecture cycle.

When items 1-12 are satisfied, the required action is **release v1.0.0**.

# v1.0.0 release execution plan

## Stage R1: finish live gates

Complete Checkpoints 1-6 in order. Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E and for every P0/P1 candidate. All consultations use the project target contract below.

Patch only:

- reproducible PROJECT P0/P1;
- P2 that directly blocks a mandatory release gate;
- test fixtures/docs that are objectively stale relative to the frozen architecture.

## Stage R2: RELEASE CANDIDATE and feature freeze

When all mandatory gates are characterized and no PROJECT P0/P1 is open:

- declare `RELEASE CANDIDATE`;
- freeze architecture, routing, scheduling semantics, and evaluation scope;
- prepare version/tag/release metadata;
- run no new optimization experiments that can expand the release gate.

## Stage R3: one fixed RC closure pass

Run exactly one release-candidate closure pass over the frozen content:

- full deterministic CI;
- fresh-clone clean-Codex-home smoke;
- exact four-role discovery/routing;
- adaptive fan-out + native slot queue/recovery smoke;
- one-writer/depth-one smoke;
- installer critical safety/migration smoke;
- README/install docs checked against observed behavior.

If a P0/P1 fix is required, rerun only the invalidated live gate plus full CI and this RC pass. P2/P3 does not restart the architecture cycle unless it directly invalidates a mandatory gate.

## Stage R4: publish v1.0.0

- set final Plugin version to `1.0.0`;
- merge the exact tested release content;
- tag the exact tested commit;
- publish the GitHub release;
- mark validation complete in `LOCAL_VALIDATION_REPORT.md`;
- move remaining P2/P3 and route-economics questions to v1.x.

# Required validation artifact

`LOCAL_VALIDATION_REPORT.md` is the evidence ledger.

After each checkpoint, append or reconcile:

```text
REPOSITORY_SHA
RUNTIME / PLATFORM
WORKLOAD / FIXTURE
EXPECTED
ACTUAL
EVIDENCE CLASS
ROUTE / PERMISSION / ANCESTRY EVIDENCE WHEN MATERIAL
DEPENDENCIES SATISFIED / INVALIDATED
EXECUTION PROGRESS / FAILURE SIGNATURE WHEN MATERIAL
CONSENT / READY FRONTIER / SLOT EVIDENCE WHEN MATERIAL
DEFECT CLASSIFICATION
OPEN UNKNOWN
```

Never relabel static CI as live Codex runtime evidence.

# Feedback protocol for continued adversarial review

`gpt56-sol-pro-consult` is the required adversarial consultation mechanism for Review Checkpoints A-E and immediately after any P0/P1 candidate.

Codex remains the local executor. The consultation challenges severity, ownership, counterexamples, evidence quality, product/architecture judgment, and whether the next checkpoint is justified. Its result is model judgment and must not be counted as evidence that Codex Delegate itself routed correctly.

Do not replace this consultation with an ad hoc generic Sol call.

## Project consultation target

For this project, every adversarial review and project discussion sent through `/gpt56-sol-pro-consult` must continue the existing ChatGPT conversation below:

```text
SKILL
/gpt56-sol-pro-consult

TARGET_CHATGPT_CONVERSATION_TITLE
分支 · 项目对比分析

TARGET_MODE
continue_existing_conversation

MATCH_POLICY
exact_title_unique_match
```

This is an operational routing requirement for the local Codex executor.

Rules:

1. Match the title `分支 · 项目对比分析` exactly.
2. Continue that existing conversation so checkpoint reviews, defect discussions, architecture judgments, and release decisions remain in one project discussion thread.
3. Do not create a replacement ChatGPT conversation when the exact target is missing or ambiguous.
4. Do not choose a similarly named conversation by fuzzy match, recency, or guesswork.
5. Do not silently fall back to an isolated consultation conversation for this project.
6. If the exact title cannot be uniquely resolved, stop the consultation and return `CONSULTATION_TARGET_UNRESOLVED` to the user. Do not continue a policy-changing checkpoint on the assumption that the review was delivered.
7. If the user later renames the project conversation, this target must be updated from a user-confirmed title before the next required consultation.
8. A long-lived target conversation does not replace evidence packing. Every consultation still sends the compact current checkpoint packet below.
9. The consultation response returns to Codex as `model_judgment`; Codex must reconcile it against repository and runtime evidence before changing the project.
10. Follow-up project discussion requested by the consultation must continue the same target conversation unless the user explicitly changes the target.

The project target contract does not replace any transport-level `task_id`, sentinel, safety scan, or other wrapper that `/gpt56-sol-pro-consult` itself requires. Use the skill's native transport protocol and place the project packet below inside it.

## Required project packet

```text
CONTEXT_PACKET_V1

CONSULTATION_TARGET
skill: /gpt56-sol-pro-consult
conversation_title: 分支 · 项目对比分析
mode: continue_existing_conversation
match_policy: exact_title_unique_match

CHECKPOINT
A | B | C | D | E | defect | release-candidate | project-discussion

REPOSITORY_SHA
<actual tested origin/main SHA>

RUNTIME / PLATFORM
<actual Codex runtime/build and platform when material>

COMPLETED_HEADOFF_ITEMS
<only newly completed checklist items>

NEW_EVIDENCE
<deterministic / repository / live runtime evidence>

DEPENDENCY_STATE
<ready/running/satisfied/invalidated facts material to this checkpoint>

EXECUTION_PROGRESS
<failure signatures, progress/stall signals, clean restart or delta escalation when material>

RESOURCE_STATE
<consent, peak active children, observed slots, queued dependencies, writer domains when material>

DEFECTS
<severity + ownership + reproduction, or none>

TESTS
<commands and exact outcomes>

CHANGES
<production/test/docs changes since previous checkpoint>

UNRESOLVED
<smallest remaining unknowns>

LOCAL_JUDGMENT
<Codex executor's current conclusion>

ASK
Challenge severity, ownership, evidence sufficiency, counterexamples, and whether execution should continue without architecture change. For project-discussion packets, answer the bounded product or architecture question and identify the strongest contrary case.
```

The local executor must wait for the consultation result when the checkpoint requires it, reconcile the response against actual artifacts/runtime evidence, record any decision-relevant result in `LOCAL_VALIDATION_REPORT.md`, and only then continue.

# Completion condition

There is no Checkpoint 7 and no automatic post-checkpoint optimization phase.

When Checkpoints 1-6 are characterized, the 12 Definition-of-Done conditions hold, full RC validation is green, and no reproducible PROJECT P0/P1 remains, release v1.0.0.
