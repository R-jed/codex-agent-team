# Codex Delegate Local Runtime Validation Handoff

This file is the authoritative execution checklist for local validation and the finite v1.0.0 release phase of **Codex Delegate**.

The architecture cycle remains closed. The v0.5.1 work is a bounded refinement of recovery observability and Codex Plugin compliance. It does not reopen model routing, fan-out architecture, or the six-checkpoint release scope.

The remaining job is finite: complete the mandatory live gates, resolve only release-blocking defects, run one fixed release-candidate closure pass, then publish v1.0.0.

Do not reopen architecture or optimization work after the Definition of Done is satisfied.

## Current checkpoint

Last accepted v0.5.0 static architecture baseline:

```text
v0.5.0 architecture merge: 00e7a2a340e6bc57ea15460f45721b571f8078fd
product: Codex Delegate
last released candidate version: 0.5.0
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

v0.5.1 candidate scope:

```text
recovery refinement:
- explicit Intervention Gate before recovery classification
- structured execution signals without numeric auto-routing thresholds
- bounded Recovery Ledger across clean restarts
- proposed action vs effective action + decision provenance
- event-driven recovery evaluation
- child-progress observability treated as a measured runtime fact

Plugin compliance refinement:
- Plugin manifest remains the native distribution envelope
- custom Agent profiles remain a separate native Codex configuration surface
- user-approved profiles target $CODEX_HOME/agents
- marketplace + plugin installation uses Codex CLI commands
- new Codex thread required after install/reinstall for pickup validation
- current OpenAI plugin-creator validator becomes an RC validation gate
```

Do not mark the v0.5.1 candidate accepted until its exact content passes deterministic CI and is merged. Record the final accepted SHA and CI in `LOCAL_VALIDATION_REPORT.md` after merge.

Last accepted live production-behavior baseline remains:

```text
production behavior tested: c6020db903b35f0d57677b131bf35b0580144ab9
Codex runtime tested so far: 0.146.0
platform tested so far: Apple Silicon macOS 27.0
```

Never relabel static CI, Plugin validation, or model consultation as live Codex runtime proof.

Before every live checkpoint:

1. fetch `origin/main`;
2. record the actual tested SHA in `LOCAL_VALIDATION_REPORT.md`;
3. inspect intervening production changes;
4. reuse older evidence only when its declared dependencies remain valid.

Status notation:

- `[x]` means reproducible evidence exists in merged repository history or `LOCAL_VALIDATION_REPORT.md`.
- `[ ]` means the gate remains required.
- `PARTIAL` means some evidence exists but the full acceptance condition has not been characterized.

## v0.5.1 control model

```text
main session owns user intent, dependency state, scheduling, evidence, recovery, integration, and acceptance
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
acceptance failure != automatic intervention
Intervention Gate -> recovery classification only when evidence or a boundary justifies change
Recovery Ledger -> compact material attempt history, never a transcript or private reasoning store
proposed model action != effective orchestration action
execution recovery is event-driven and evidence-driven, with no universal retry or stall count
child mid-run observability -> runtime fact, never assumed
```

Resource scopes remain separate:

```text
main-session scope
-> Dependency Ledger, ready frontier, Recovery Ledger, consent state, active child set

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
- no universal retry-count or fixed stall-threshold rule;
- no acceptance failure treated as intervention by itself;
- no successful command, model self-report, confidence language, or file write treated as progress by itself;
- no model proposal treated as orchestration authority;
- no weakening the acceptance oracle because a lane failed it;
- no silent expansion of decision rights through model escalation;
- no more than one active writing Worker in one canonical shared checkout;
- no file-level partitioning used to justify multiple writers in one physical checkout;
- no child-created descendants;
- no cross-role substitution when an exact project profile is unavailable;
- no configured route fact presented as runtime observation;
- no incomplete expected route accepted as exact runtime proof;
- no missing runtime evidence converted to affirmative success;
- no child mid-run trajectory claim without an exposed runtime surface;
- no systematic rediscovery of still-valid deterministic or repository evidence;
- no project-wide global writer mutex that blocks independent workspaces;
- no workspace-lock daemon or installer lock before reproducible live evidence establishes the need;
- no invented `agents` Plugin-manifest component;
- no manual `config.toml` or marketplace edits used to make the supported Plugin install path appear successful;
- no manual rename of managed Agent profiles or ownership manifests merely to match the product brand;
- no repository/package-id migration before real installed-Plugin upgrade and fresh-install behavior is characterized;
- no performance, quality, cost, concurrency-capacity, recovery, or observability claim without measured named workloads and runtime versions.

If a native Codex limitation makes a project invariant impossible, record the exact runtime behavior and ownership classification before changing policy.

# Completed repository work

## A. Core architecture and policy

- [x] Main session remains the single control plane and final acceptance owner.
- [x] Delegation Benefit Gate and Contractability Gate remain upstream of model-specific delegation.
- [x] Delegation Contract binds each child to a dependency id, interfaces/dependencies, acceptance, verification, and execution evidence.
- [x] Shared Evidence State preserves deterministic/repository facts while dependencies remain valid.
- [x] Dependency Ledger uses `pending | ready | running | satisfied | blocked | invalidated` state.
- [x] Previous default-child and hard-four scheduling invariants are removed.
- [x] Static routing cases allow authorized fan-out beyond four and queue excess work under native slot pressure.
- [x] The two-child number exists only as the normal no-extra-consent simultaneous fan-out boundary.
- [x] One-writer-per-canonical-workspace and depth-one delegation remain hard safety invariants.

## B. Recovery policy

- [x] Execution evidence, progress signals, intervention, and effective recovery action are separate concepts.
- [x] Acceptance failure is not automatically an intervention trigger.
- [x] Successful commands, file writes, confidence, narration, and repeated discovery do not establish task progress by themselves.
- [x] Intervention Gate evaluates whether evidence still supports forward progress before recovery classification.
- [x] Failure classes remain mechanical, contract, execution stall/context pollution, capability, and judgment.
- [x] No universal retry count or fixed stall threshold is encoded.
- [x] Recovery Ledger preserves only compact material semantic history across fresh contexts.
- [x] Proposed actions remain separate from effective actions and decision source.
- [x] Recovery evaluation is event-driven rather than fixed-turn-driven.
- [x] Child-progress observability is defined as a runtime fact to characterize, not an assumed capability.

## C. Exact semantic routes and distribution

- [x] Reader -> GPT-5.6 Luna / max / read-only.
- [x] Worker -> GPT-5.6 Luna / max / workspace-write.
- [x] Investigator -> GPT-5.6 Terra / xhigh / read-only.
- [x] Advisor -> GPT-5.6 Sol / high / read-only.
- [x] Product name is `Codex Delegate` and canonical entry point is `/codex-delegate`.
- [x] Repository/package/profile compatibility identifiers remain unchanged during pre-v1 migration.
- [x] Installer ownership rules fail closed for user-modified or unproven profiles.
- [x] Plugin bundle uses `.codex-plugin/plugin.json` and repository marketplace uses `.agents/plugins/marketplace.json`.
- [x] Marketplace source path remains `./plugins/codex-agent-team`.
- [x] Plugin manifest does not claim an unsupported native custom-Agent component.
- [x] Managed profile provisioning targets the native personal custom-Agent surface `$CODEX_HOME/agents` only after user approval.

## D. Historical live evidence carried forward

- [x] Marketplace registration succeeded through the prior documented Git source.
- [x] A real v0.3.0 Plugin installation succeeded.
- [x] Missing project profiles failed closed instead of cross-routing.
- [x] Real profile provisioning created four profiles plus one ownership manifest.
- [x] Installer `--check` succeeded in the tested environment.
- [x] Fresh-task role discovery exposed all four semantic roles after provisioning.
- [x] Reader spawned with `fork_turns=none` and local rollout inspection reported Luna Max, read-only sandbox, expected parent, and runtime 0.146.0.
- [x] CAT-LOCAL-001 direct Codex-home endpoint symlink defect is closed in production history.

Historical evidence is revalidated only where current content changed a dependency of the claim.

# Pending live validation

Execute the remaining gates in order. Update `LOCAL_VALIDATION_REPORT.md` after each checkpoint. Do not expand the checklist merely because another optimization is imaginable.

## Checkpoint 1: exact roles and Runtime Truth

### 1. Exact custom-Agent route matrix

Run tiny bounded responsibilities with explicit `fork_turns=none`.

- [x] Reader: Luna Max / read-only / parent matched / historical L1 local corroboration.
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

Invoke `/gpt56-sol-pro-consult` after this checkpoint, or immediately on ambiguous writing, nested delegation, scope widening, unrelated edit loss, or permission-boundary failure.

## Checkpoint 3: dependency scheduling, evidence reuse, intervention, and recovery

### 5. Dependency Ledger and ready frontier

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

### 7. Intervention Gate and recovery

Construct controlled cases around one bounded dependency.

- [ ] Healthy incomplete case: acceptance still fails but new evidence narrows the cause / unresolved delta -> `advanced`, continue, no intervention.
- [ ] False-progress case: successful inspection/tool commands with unchanged acceptance and no useful new evidence -> must not become `advanced`.
- [ ] Mechanical defect with concrete correction hypothesis -> focused Luna correction.
- [ ] Contract gap -> main session repairs the contract.
- [ ] Same failure signature with no new evidence -> execution stall, no blind unchanged retry.
- [ ] Clean same-lane restart uses fresh context and carries artifact, valid evidence, failure signature, unresolved delta, material Recovery Ledger, acceptance, and `DO NOT REDO`.
- [ ] Semantic cycle case `hypothesis A -> B -> A` is detected from Recovery Ledger rather than replaying the dead end.
- [ ] Evidence-supported capability gap -> Terra receives unresolved delta before repeated same-lane retry.
- [ ] Judgment gap -> main session or bounded Sol decision.
- [ ] Proposed recovery action remains separate from effective action and decision source.
- [ ] Acceptance oracle is never weakened to make a stalled lane pass.

Record:

```text
intervention_gate_evaluations
interventions_taken
execution_stall_events
clean_same_lane_restarts
recovery_ledger_entries
attempt_cycle_detected
proposed_recovery_action
effective_recovery_action
recovery_decision_source
policy_transform
unjustified_retry_calls
same_failure_without_new_evidence
```

### 8. Child progress observability

On the current Codex runtime, characterize what the parent can actually observe before child return:

```text
none
terminal_only
periodic_summary
structured_live
```

- [ ] Record the strongest level actually exposed by the tested build.
- [ ] Do not infer `structured_live` from prose or self-report.
- [ ] If only terminal evidence exists, document recovery as dependency-level/return-level and do not implement a fake mid-run detector.
- [ ] If structured live evidence exists, record the exact fields/events before considering any mid-run policy extension.

### Review checkpoint C

Invoke `/gpt56-sol-pro-consult` with Dependency Ledger, evidence reuse, Intervention Gate, Recovery Ledger, child-observability, clean-restart, and first Terra-delta evidence before modifying scheduling/recovery policy.

## Checkpoint 4: product-value experiments

### 9. Raw prompt versus compiled contract

```text
A: raw user prompt -> Luna Max
B: same prompt -> main session compiles Delegation Contract -> Luna Max
```

Freeze every workload before a pair. Record workload hash, repo revision, repeat index, routes, permissions/tool fingerprints, acceptance rubric, runtime version, correctness, corrections, latency/tokens when exposed, and evidence-reuse waste.

- [ ] Produce at least one valid pair before scaling.
- [ ] Target representative repeated pairs if cost permits.

### 10. Terra delta experiment

```text
A: whole-task Terra restart
B: Terra receives unresolved delta + valid evidence + artifact + failure signature + Recovery Ledger + DO NOT REDO
```

Do not claim an advantage until paired evidence supports it.

### 11. Selective fresh-context Sol experiment

```text
A: contract -> Luna
B: contract -> Luna -> fresh-context selective Sol
```

Measure material catches, false positives, total correction work, and latency/cost when exposed.

### Review checkpoint D

Invoke `/gpt56-sol-pro-consult` with the first valid product-value pairs. Do not tune Luna/Terra/Sol routes pre-v1 unless a reproducible correctness/safety regression makes the frozen route unusable.

## Checkpoint 5: adaptive resources, multi-session safety, and lifecycle

### 12. Consent boundary and no product hard cap

```text
F0 no useful delegated dependency -> 0 children valid
F1 one useful dependency -> one child when justified
F2 two independent ready dependencies -> both may run inside explicit-command baseline when safe
F3 >=3 ready dependencies without broad authorization -> ask consent before larger simultaneous fan-out
F4 >=5 authorized independent read-only dependencies -> no product hard 4 ceiling; native capacity decides active count; remainder queues
```

Record ready dependencies, peak active children, observed child capacity, runtime slot waits, consent prompts, duplicate dependency calls.

Do not infer a universal native maximum from one version/build.

### 13. Slot recovery and lifecycle

- [ ] Queued ready dependencies become runnable as prior children close.
- [ ] No orphan/ghost dependency ownership after completion, failure, cancellation, or close.
- [ ] Slot pressure never triggers cross-route substitution or duplicate work.
- [ ] Run at least 10 bounded spawn/close cycles across representative read-only and writing work where practical.
- [ ] Characterize cancellation and failed-child slot recovery.

### 14. Workspace-scoped one-writer and multi-session matrix

```text
M1 different sessions, different projects/checkouts -> both writers should be allowed
M2 different sessions, same repository, isolated worktrees -> both writers only when real isolation is evidenced
M3 different sessions, same canonical physical checkout -> never accept two simultaneous writing Workers
M4 one writing session + one read-only session same checkout -> dependent read evidence refreshes/invalidates after writes
```

Do not implement a workspace lock before M3 establishes a reproducible failure. If M3 fails, classify it as a PROJECT/P1 candidate and use the smallest canonical-workspace coordination mechanism that preserves independent-workspace concurrency.

## Checkpoint 6: official Plugin install, migration, and installer concurrency

### 15. Current official Plugin contract validation

Use the **current** OpenAI Codex `plugin-creator` tooling/source that corresponds to the release-validation date/build. Record its source revision/version.

- [ ] Run the official `plugin-creator/scripts/validate_plugin.py` against `plugins/codex-agent-team` and record the exact outcome.
- [ ] Confirm Plugin root folder name equals `.codex-plugin/plugin.json` `name`.
- [ ] Confirm strict semver, required interface metadata, and `https://` URL metadata where present.
- [ ] Confirm unsupported manifest components such as invented `agents` or `hooks` fields are absent.
- [ ] Confirm `.agents/plugins/marketplace.json` points to `./plugins/codex-agent-team` and declares `policy.installation`, `policy.authentication`, and `category`.
- [ ] Register the Git marketplace through CLI, not manual config edits:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team
```

- [ ] Install through CLI:

```bash
codex plugin add codex-agent-team@codex-agent-team
```

- [ ] Start a new Codex thread after install/reinstall and confirm `/codex-delegate` is discovered.
- [ ] Confirm Plugin installation itself does not pretend to have installed custom Agent roles.
- [ ] Authorize first-run provisioning, confirm profiles are written only to the active `$CODEX_HOME/agents` plus the ownership manifest, then verify native role discovery.
- [ ] Do not hand-edit `config.toml` or marketplace files to rescue a failing release test; classify the observed failure instead.

### 16. Real installed-Plugin migration

- [ ] Starting from real v0.3.x Codex Agent Team, update through the supported marketplace path and confirm one Codex Delegate package path with `/codex-delegate`.
- [ ] Starting from real v0.4.x Codex Delegate, update through current release and characterize managed profile migration.
- [ ] Starting from v0.5.0, update/reinstall v0.5.1 and confirm the new Skill is picked up in a fresh thread while unchanged exact managed profile bytes remain valid.
- [ ] Confirm user-modified/unproven profiles remain untouched and the affected route fails closed.
- [ ] Characterize old `/codex-agent-team` invocation after upgrade. Do not assume alias behavior.
- [ ] Verify installed metadata reports `0.5.1` while compatibility package id remains `codex-agent-team`.
- [ ] Decide repository/package slug migration only from real install/upgrade evidence. Cosmetic alignment cannot block v1.

### 17. Filesystem and concurrent installer matrix

```text
I1 same clean CODEX_HOME, two same-generation installers concurrently
-> exact converged state or one safe refusal
-> four current profiles + one exact manifest
-> no corruption or staging/backup debris

I2 one installer forced to fail after mutation begins while peer succeeds
-> failed rollback must not overwrite peer-success state

I3 different managed profile generations compete in one CODEX_HOME
-> safe refusal or exact characterized convergence
-> no silent mixed generation
```

Do not add an inter-process installer lock merely because races are theoretically possible. Add coordination only after a reproducible project-owned failure.

### Review checkpoint E

Invoke `/gpt56-sol-pro-consult` after Checkpoints 5 and 6 are characterized. Include adaptive fan-out, observed native capacity, slot recovery, M1-M4, official Plugin validator/install evidence, I1-I3, and migration evidence.

# Defect triage

```text
P0
unsafe mutation, credential boundary failure, data loss, false security proof, or unrecoverable installer corruption

P1
core orchestration invariant fails, wrong route accepted, unsafe multiple writers, nested delegation, contractability bypass, duplicate dependency ownership causing material wrong execution, consent boundary bypass, or documented Plugin/install path broken

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
3. The normal user path works: Git marketplace -> `codex plugin add` -> fresh-thread Skill discovery -> authorized profile readiness -> bounded delegation -> verification -> visible completion.
4. Current OpenAI Plugin validation passes on the exact release candidate and the Plugin/custom-Agent provisioning boundary matches observed Codex behavior.
5. One-writer, depth-one, exact-route fail-closed, contractability, prompt-injection, and untrusted-content boundaries survive live tests.
6. Adaptive scheduling is evidenced: no fixed Agent target, no product hard 4 ceiling, no duplicate running dependency, >2 simultaneous fan-out is consent-gated, and runtime slot pressure queues safely.
7. Recovery is evidenced: healthy incomplete progress does not trigger premature intervention; unchanged retry is rejected; clean restart preserves valid task truth and Recovery Ledger; capability gaps use Terra delta escalation.
8. Child-progress observability is characterized for the tested runtime and public claims do not exceed the observed level.
9. Raw-prompt versus compiled-contract evaluation produces valid paired data with no systematic acceptance-quality regression on representative bounded work.
10. Shared Evidence State shows no systematic full-task rediscovery while dependencies remain valid; Terra delta and selective Sol may remain conservative if economics are inconclusive and no correctness/safety regression exists.
11. Luna Max / Terra XHigh / Sol High remain the frozen v1 routing baseline; route/effort optimization moves to v1.x unless a release-blocking defect requires change.
12. Full deterministic CI and one fresh-clone clean-Codex-home RC smoke are green on the exact release content; user docs describe observed limitations; remaining P2/P3 work moves post-v1.

When items 1-12 are satisfied, the required action is **release v1.0.0**.

# v1.0.0 release execution plan

## Stage R1: finish live gates

Complete Checkpoints 1-6 in order. Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E and for every P0/P1 candidate.

Patch only:

- reproducible PROJECT P0/P1;
- P2 that directly blocks a mandatory release gate;
- test fixtures/docs objectively stale relative to frozen architecture or current official Codex contract.

## Stage R2: RELEASE CANDIDATE and feature freeze

When all mandatory gates are characterized and no PROJECT P0/P1 is open:

- declare `RELEASE CANDIDATE`;
- freeze architecture, routing, scheduling/recovery semantics, Plugin packaging, and evaluation scope;
- prepare version/tag/release metadata;
- run no new optimization experiments that can expand the release gate.

## Stage R3: one fixed RC closure pass

Run exactly one release-candidate closure pass over frozen content:

- current official Plugin validator;
- Git marketplace add + Plugin add + new-thread discovery;
- authorized clean-Codex-home profile provisioning and four-role discovery;
- full deterministic CI;
- exact four-role routing smoke;
- Intervention Gate / child-observability recovery smoke;
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
INTERVENTION / RECOVERY LEDGER / DECISION PROVENANCE WHEN MATERIAL
CHILD PROGRESS OBSERVABILITY WHEN MATERIAL
CONSENT / READY FRONTIER / SLOT EVIDENCE WHEN MATERIAL
PLUGIN VALIDATOR / MARKETPLACE / INSTALL EVIDENCE WHEN MATERIAL
DEFECT CLASSIFICATION
OPEN UNKNOWN
```

Never relabel static CI, Plugin validator success, or model consultation as live Codex runtime evidence.

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
分支 · 分支 · 项目对比分析

TARGET_MODE
continue_existing_conversation

MATCH_POLICY
exact_title_unique_match
```

This is an operational routing requirement for the local Codex executor. The user-confirmed current project discussion thread is the ChatGPT conversation titled `分支 · 分支 · 项目对比分析`.

Rules:

1. Match the title `分支 · 分支 · 项目对比分析` exactly.
2. Continue that existing conversation so checkpoint reviews, defect discussions, architecture judgments, release decisions, and bounded project questions remain in one user + GPT-5.6 Sol project discussion thread.
3. Do not create a replacement ChatGPT conversation when the exact target is missing or ambiguous.
4. Do not choose a similarly named conversation by fuzzy match, recency, or guesswork.
5. Do not silently fall back to an isolated consultation conversation for this project.
6. If the exact title cannot be uniquely resolved, stop the consultation and return `CONSULTATION_TARGET_UNRESOLVED` to the user.
7. If the user later renames the project conversation, update this target from a user-confirmed title before the next required consultation.
8. A long-lived target conversation does not replace evidence packing. Every consultation still sends the compact current checkpoint packet below.
9. The consultation response returns to Codex as `model_judgment`; Codex reconciles it against repository/runtime evidence before changing the project.
10. Follow-up project discussion requested by the consultation continues the same target conversation unless the user explicitly changes the target.

The target contract does not replace any transport-level `task_id`, sentinel, safety scan, or wrapper required by `/gpt56-sol-pro-consult` itself.

## Required project packet

```text
CONTEXT_PACKET_V1

CONSULTATION_TARGET
skill: /gpt56-sol-pro-consult
conversation_title: 分支 · 分支 · 项目对比分析
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
<failure signatures, progress/stall signals, Intervention Gate outcome when material>

RECOVERY_STATE
<material Recovery Ledger entries, proposed/effective action, decision source, policy transform when material>

RESOURCE_STATE
<consent, peak active children, observed slots, queued dependencies, writer domains when material>

PLUGIN_STATE
<validator, marketplace source/ref/sparse paths, installed Plugin/version, fresh-thread discovery, profile provisioning when material>

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

The local executor waits for the consultation result when required, reconciles it against actual artifacts/runtime evidence, records decision-relevant results in `LOCAL_VALIDATION_REPORT.md`, and only then continues.

# Completion condition

There is no Checkpoint 7 and no automatic post-checkpoint optimization phase.

When Checkpoints 1-6 are characterized, the 12 Definition-of-Done conditions hold, full RC validation is green, and no reproducible PROJECT P0/P1 remains, release v1.0.0.
