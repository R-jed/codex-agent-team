# Codex Delegate Local Runtime Validation Handoff

This is the authoritative local-validation and finite v1.0.0 release checklist for **Codex Delegate**.

The architecture cycle remains closed. v0.5.1 is the accepted static baseline for the next live-validation phase. It is a bounded refinement of recovery observability and official Codex Plugin compliance; it does not reopen model routing, fan-out architecture, or the six-checkpoint release scope.

The remaining job is finite: complete Checkpoints 1-6, fix only release-blocking defects, run one fixed release-candidate closure pass, then publish v1.0.0.

## Current checkpoint

Accepted v0.5.1 static baseline:

```text
main merge: 9adf8edd303be22506744d569e6552b8fdbc7574
PR #24 final tested head: 7dadef8065f46bdb90accd38a3ffccfb75b23a51
GitHub Actions run: 30823406796
product: Codex Delegate
version: 0.5.1
architecture: Adaptive Dependency Orchestration + evidence-gated recovery
static CI: Ubuntu 3.11 PASS / Ubuntu 3.12 PASS / macOS 3.11 PASS
pytest: 131 passed
pinned official OpenAI Plugin validator: PASS
managed profile install / --check / idempotent reinstall: PASS
known open reproducible PROJECT P0/P1: none
release posture: HOLD FOR RELEASE / VALIDATION INCOMPLETE
```

Pinned static validator evidence:

```text
OpenAI Codex source revision: 7750465934d97dd3cbcb3b1655d2f622744010d3
validator: codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py
target: plugins/codex-agent-team
result: PASS
```

This establishes the accepted **static** v0.5.1 repository baseline. It does not prove real marketplace registration/upgrade, Plugin installation, fresh-thread discovery, custom-Agent discovery, exact runtime routes, child-progress observability, or cross-session behavior.

Last accepted live production-behavior baseline:

```text
production behavior tested: c6020db903b35f0d57677b131bf35b0580144ab9
Codex runtime: 0.146.0
platform: Apple Silicon macOS 27.0
```

Before every live checkpoint, fetch `origin/main`, record the actual tested SHA in `LOCAL_VALIDATION_REPORT.md`, and revalidate only evidence whose declared dependencies changed.

Static CI, Plugin validation, upstream source inspection, and model consultation are not live runtime proof.

## v0.5.1 control model

```text
main session owns user intent, dependency state, scheduling, evidence, recovery, integration, acceptance
no model is a mandatory stage
no fixed Agent count and no product-level hard child ceiling
Dependency Ledger -> ready frontier -> smallest useful scheduling wave
explicit /codex-delegate -> up to 2 concurrently active justified children without another prompt
larger simultaneous fan-out -> consent unless already authorized
actual concurrency -> ready dependencies + workspace safety + exact routes + native runtime slots
native slot shortage -> queue/serialize ready work
Luna Max -> bounded execution
Terra XHigh -> unresolved complex technical delta
Sol High -> selective fresh-context judgment/review
one active writing Worker per canonical workspace
delegation depth = 1
acceptance failure != automatic intervention
Intervention Gate -> recovery classification only when evidence or a boundary justifies change
Recovery Ledger -> bounded semantic attempt history, never transcript/private reasoning
proposed model action != effective orchestration action
child mid-run observability -> runtime fact, never assumed
```

## Stop line

Do not change these rules merely to make a live test pass:

- no mandatory Luna -> Terra -> Sol pipeline;
- no fixed team size, default child target, or product hard child ceiling;
- no machine-wide Agent cap inferred from one runtime build;
- no larger simultaneous fan-out without consent unless already authorized;
- no silent serial fan-out used to evade material compute-expansion consent;
- no duplicate Agent call for an unchanged running dependency;
- no generic Terra whole-task rerun because Luna quality looks weak;
- no unchanged retry simply because an Agent failed;
- no universal retry count or fixed stall threshold;
- no acceptance failure treated as intervention by itself;
- no successful command, self-report, confidence, or file write treated as progress by itself;
- no model proposal treated as orchestration authority;
- no weakened acceptance oracle because a lane failed it;
- no more than one active writing Worker in one canonical checkout;
- no file-level partitioning used to authorize multiple writers in one physical checkout;
- no child-created descendants;
- no cross-role substitution when an exact profile is unavailable;
- no configured route fact presented as runtime observation;
- no incomplete expected route accepted as exact runtime proof;
- no missing runtime evidence converted to affirmative success;
- no child mid-run trajectory claim without an exposed runtime surface;
- no systematic rediscovery of still-valid evidence;
- no project-wide global writer mutex that blocks independent workspaces;
- no workspace or installer lock before reproducible evidence establishes the need;
- no invented `agents` Plugin-manifest component;
- no manual `config.toml` or marketplace edits used to rescue the supported install path;
- no repository/package-id migration before real install/upgrade behavior is characterized;
- no performance, quality, cost, capacity, recovery, or observability claim without measured workloads and runtime versions.

# Completed repository work

## A. Architecture

- [x] Main session remains the control plane and final acceptance owner.
- [x] Delegation Benefit Gate and Contractability Gate precede model-specific delegation.
- [x] Dependency Ledger states are `pending | ready | running | satisfied | blocked | invalidated`.
- [x] Shared Evidence State reuses valid deterministic/repository facts.
- [x] No product-level hard child ceiling remains.
- [x] The two-child number is only the normal no-extra-consent simultaneous fan-out boundary.
- [x] One-writer-per-canonical-workspace and depth-one delegation remain invariants.

## B. Recovery

- [x] Execution evidence, progress signals, intervention, and recovery action are separate concepts.
- [x] Acceptance failure is not automatically an intervention trigger.
- [x] Successful commands and file writes do not establish task progress by themselves.
- [x] Intervention Gate precedes recovery classification.
- [x] No universal retry count or fixed stall threshold is encoded.
- [x] Recovery Ledger carries compact material attempt history across clean restarts.
- [x] Proposed actions remain separate from effective actions and decision source.
- [x] Recovery evaluation is event-driven.
- [x] Child-progress observability is a runtime fact to characterize.

## C. Routes and Plugin boundary

- [x] Reader -> GPT-5.6 Luna / max / read-only.
- [x] Worker -> GPT-5.6 Luna / max / workspace-write.
- [x] Investigator -> GPT-5.6 Terra / xhigh / read-only.
- [x] Advisor -> GPT-5.6 Sol / high / read-only.
- [x] Product name is `Codex Delegate`; canonical entry point is `/codex-delegate`.
- [x] Plugin bundle uses `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`.
- [x] Marketplace source path is `./plugins/codex-agent-team`.
- [x] Plugin manifest does not claim an unsupported custom-Agent component.
- [x] Managed personal profiles target `$CODEX_HOME/agents` only after explicit user approval.
- [x] Compatibility repository/package/profile identifiers remain unchanged pre-v1.
- [x] Pinned official OpenAI `plugin-creator/scripts/validate_plugin.py` validation passes on the accepted v0.5.1 static content.
- [x] Current upstream PluginStore source shows Plugin installation recursively copies the complete Plugin source tree and rejects symlink entries; this is upstream source evidence, not local runtime proof.

## D. Historical live evidence

- [x] Real marketplace registration and v0.3.0 Plugin install succeeded historically.
- [x] Missing project profiles failed closed.
- [x] Real provisioning created four profiles plus one ownership manifest.
- [x] Installer `--check` succeeded.
- [x] Fresh-task role discovery exposed all four semantic roles.
- [x] Reader used `fork_turns=none`; local rollout reported Luna Max, read-only, expected parent, runtime 0.146.0.
- [x] CAT-LOCAL-001 direct Codex-home symlink defect is closed.

# Pending live validation

Update `LOCAL_VALIDATION_REPORT.md` after every checkpoint. Do not add a Checkpoint 7.

## Checkpoint 1: exact roles and Runtime Truth

- [x] Reader historical L1 local corroboration.
- [ ] Worker exact route.
- [ ] Investigator exact route.
- [ ] Advisor exact route.
- [ ] Complete native route metadata if exposed.
- [ ] Partial native route behavior.
- [ ] Native/local agreement and material conflict cases.
- [ ] Duplicate rollout/schema drift on current Codex build.

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

Invoke `/gpt56-sol-pro-consult` with the exact-route/runtime packet before changing Runtime Truth policy.

## Checkpoint 2: contractability, scope, and safety

- [ ] Already-isolated deterministic defect stays main-session only with zero children.
- [ ] Bounded implementation creates a dependency-bound contract before Luna Worker execution.
- [ ] Ambiguous product semantics do not reach a writing Worker before decision rights and acceptance are clear.
- [ ] Concurrent user edits are preserved and stale dependent evidence is invalidated.
- [ ] Actual changed files remain inside declared write scope.
- [ ] Repository prompt injection cannot change policy, consent, routes, dependency state, or evidence rules.
- [ ] Children do not spawn descendants.
- [ ] Missing exact roles remain fail closed.

### Review checkpoint B

Invoke `/gpt56-sol-pro-consult` after this checkpoint or immediately on scope, permission, recursion, or unrelated-edit loss.

## Checkpoint 3: dependency scheduling, evidence reuse, intervention, and recovery

### 5. Dependency Ledger and ready frontier

- [ ] Dependencies move through observable `pending -> ready -> running -> satisfied` state.
- [ ] A blocked prerequisite prevents dependent work from becoming ready.
- [ ] A running dependency does not receive duplicate inference.
- [ ] Satisfied dependencies stay closed while inputs remain valid.
- [ ] Changed inputs invalidate only dependent evidence/dependencies.
- [ ] Ready frontier is recomputed after material changes.

### 6. Shared Evidence State

Establish E01 reproduction, E02 caller path, E03 focused-test baseline, and E04 interface fact.

- [ ] Later Agents receive valid relevant evidence.
- [ ] They do not rebuild E01-E04 without invalidation.
- [ ] Unrelated changes do not invalidate unrelated evidence.
- [ ] Model judgments remain hypotheses.

### 7. Intervention Gate and recovery

- [ ] Healthy incomplete case: acceptance still fails but new evidence narrows cause/unresolved delta -> `advanced`, continue, no intervention.
- [ ] False-progress case: successful commands with unchanged acceptance and no useful new evidence -> must not become `advanced`.
- [ ] Mechanical defect -> focused Luna correction with a distinct hypothesis.
- [ ] Contract gap -> main session repairs contract.
- [ ] Same failure signature with no new evidence -> execution stall, no blind retry.
- [ ] Clean same-lane restart uses fresh context and carries artifact, valid evidence, failure signature, unresolved delta, Recovery Ledger, acceptance, and `DO NOT REDO`.
- [ ] Semantic cycle case `hypothesis A -> B -> A` is detected from Recovery Ledger.
- [ ] Evidence-supported capability gap -> Terra receives unresolved delta before repeated same-lane retry.
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

Classify only what the tested runtime actually exposes:

```text
none
terminal_only
periodic_summary
structured_live
```

- [ ] Record the strongest observed level.
- [ ] Do not infer `structured_live` from prose/self-report.
- [ ] If only terminal evidence exists, keep recovery dependency-level/return-level.
- [ ] If structured live evidence exists, record exact fields/events before any mid-run policy change.

### Review checkpoint C

Invoke `/gpt56-sol-pro-consult` with Dependency Ledger, evidence reuse, Intervention Gate, Recovery Ledger, child-progress observability, clean restart, and first Terra-delta evidence.

## Checkpoint 4: product-value experiments

### 9. Raw prompt versus compiled contract

```text
A: raw user prompt -> Luna Max
B: same prompt -> main session compiles Delegation Contract -> Luna Max
```

Freeze every workload before a pair and record these exact controls:

```text
workload_definition_hash
repo_revision
repeat_index
main_session_route
worker_route
permissions_fingerprint
tool_surface_fingerprint
acceptance_rubric_id
```

- [ ] Produce at least one valid pair before scaling.
- [ ] Repeat representative pairs if cost permits.

### 10. Terra delta experiment

```text
A: whole-task Terra restart
B: Terra receives unresolved delta + valid evidence + artifact + failure signature + Recovery Ledger + DO NOT REDO
```

### 11. Selective fresh-context Sol experiment

```text
A: contract -> Luna
B: contract -> Luna -> fresh-context selective Sol
```

Measure material catches, false positives, total correction work, latency/tokens when exposed.

### Review checkpoint D

Invoke `/gpt56-sol-pro-consult` with the first valid product-value pairs. Do not tune Luna/Terra/Sol routes pre-v1 unless a reproducible correctness/safety regression makes the frozen route unusable.

## Checkpoint 5: adaptive resources, multi-session safety, and lifecycle

### 12. Consent boundary and no product hard cap

```text
F0 no useful delegated dependency -> 0 children valid
F1 one useful dependency -> one child when justified
F2 two independent ready dependencies -> both may run inside explicit-command baseline when safe
F3 >=3 ready dependencies without broad authorization -> ask consent
F4 >=5 authorized independent read-only dependencies -> no product hard 4 ceiling; native capacity decides; remainder queues
```

Record ready dependencies, peak active children, observed native capacity, runtime slot waits, consent prompts, and duplicate dependency calls.

### 13. Slot recovery and lifecycle

- [ ] Queued ready dependencies run as slots recover.
- [ ] No orphan/ghost ownership after completion, failure, cancellation, or close.
- [ ] Slot pressure never triggers cross-route substitution or duplicate work.
- [ ] At least 10 bounded spawn/close cycles where practical.

### 14. Workspace-scoped one-writer and multi-session matrix

```text
M1 different sessions, different projects/checkouts -> both writers should be allowed
M2 different sessions, same repository, isolated worktrees -> both writers only with real isolation
M3 different sessions, same canonical physical checkout -> never accept two simultaneous writing Workers
M4 one writing session + one read-only session same checkout -> dependent read evidence refreshes/invalidates after writes
```

Do not implement a workspace lock before M3 establishes a reproducible failure.

## Checkpoint 6: official Plugin install, migration, and installer concurrency

### 15. Current official Plugin contract validation

Use the **current** OpenAI Codex `plugin-creator` tooling at validation time and record its source revision/version. The pinned CI validator is regression evidence only.

- [ ] Run `plugin-creator/scripts/validate_plugin.py` against `plugins/codex-agent-team` on the actual checkpoint/RC content.
- [ ] Confirm Plugin folder name equals `.codex-plugin/plugin.json` `name`.
- [ ] Confirm strict semver, required interface metadata, and `https://` URL metadata where present.
- [ ] Confirm unsupported manifest components such as invented `agents` or `hooks` are absent.
- [ ] Confirm marketplace source is `./plugins/codex-agent-team` with install/auth/category policy.
- [ ] Confirm the installed Plugin bundle exposes the bundled `scripts/install-agents.py` and `agent-profiles/` content expected by the Skill's relative paths.
- [ ] Register a fresh Git marketplace through CLI:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team
```

- [ ] Install through CLI:

```bash
codex plugin add codex-agent-team@codex-agent-team
```

- [ ] Start a new Codex thread after install/reinstall and confirm `/codex-delegate` discovery.
- [ ] Confirm Plugin install itself does not claim custom Agent roles were installed.
- [ ] Authorize profile provisioning and verify writes are limited to active `$CODEX_HOME/agents` plus ownership manifest.
- [ ] Confirm native role discovery after provisioning.
- [ ] Do not hand-edit `config.toml` or marketplace files to rescue a failing release test.

### 16. Real installed-Plugin migration

For an already configured Git marketplace, refresh the marketplace snapshot before reinstall:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Then start a new Codex thread before checking updated Skill discovery.

- [ ] Starting from real v0.3.x Codex Agent Team, update through supported marketplace flow.
- [ ] Starting from real v0.4.x Codex Delegate, update and characterize managed profile migration.
- [ ] Starting from v0.5.0, update/reinstall v0.5.1 and confirm new Skill pickup in a fresh thread while unchanged exact profile bytes remain valid.
- [ ] User-modified/unproven profiles remain untouched and affected route fails closed.
- [ ] Characterize old `/codex-agent-team` invocation after upgrade.
- [ ] Installed metadata reports `0.5.1` while compatibility package id remains `codex-agent-team`.
- [ ] Cosmetic alignment cannot block v1.

### 17. Filesystem and concurrent installer matrix

```text
I1 same clean CODEX_HOME, two same-generation installers concurrently
-> exact convergence or one safe refusal
-> four profiles + one exact manifest, no debris

I2 one installer forced to fail after mutation begins while peer succeeds
-> failed rollback must not overwrite peer-success state

I3 different managed profile generations compete in one CODEX_HOME
-> safe refusal or characterized exact convergence, never silent mixed generation
```

Do not add an inter-process installer lock merely because races are theoretically possible.

### Review checkpoint E

Invoke `/gpt56-sol-pro-consult` with adaptive fan-out, native capacity, slot recovery, M1-M4, official Plugin validation/install evidence, I1-I3, and migration evidence.

# Defect triage

```text
P0: unsafe mutation, credential boundary failure, data loss, false security proof, unrecoverable installer corruption
P1: core orchestration invariant failure, wrong route accepted, unsafe writers, nested delegation, contractability/consent bypass, documented Plugin/install path broken
P2: nonblocking UX, inefficiency, maintenance drift, telemetry/schema compatibility, recoverable resource waste
P3: cosmetic, optional, speculative improvement
```

Ownership:

```text
PROJECT
UPSTREAM_CODEX_RUNTIME
ENVIRONMENT
TEST_FIXTURE
UNKNOWN
```

After mandatory gates are characterized, only reproducible PROJECT P0/P1 or a P2 directly blocking a mandatory gate can delay v1.0.0. Other P2/P3 work moves post-v1.

Any P0/P1 candidate goes immediately through `/gpt56-sol-pro-consult` before architecture or threat-model scope expands.

# Definition of Done for v1.0.0

v1.0.0 is done when all 12 conditions hold:

1. Mandatory live gates are complete or an upstream limitation is explicitly characterized with fail-closed project behavior.
2. No reproducible PROJECT P0/P1 remains open.
3. Normal path works: Git marketplace -> `codex plugin add` -> fresh-thread Skill discovery -> authorized profile readiness -> bounded delegation -> verification -> completion.
4. Current official Plugin validation passes on exact RC content and Plugin/custom-Agent boundaries match observed Codex behavior.
5. One-writer, depth-one, exact-route fail-closed, contractability, prompt-injection, and untrusted-content boundaries survive live tests.
6. Adaptive scheduling is evidenced: no fixed Agent target, no product hard 4 ceiling, no duplicate running dependency, >2 simultaneous fan-out consent-gated, slot pressure queues safely.
7. Recovery is evidenced: healthy incomplete progress avoids premature intervention; unchanged retry is rejected; clean restart preserves task truth and Recovery Ledger; capability gaps use Terra delta escalation.
8. Child-progress observability is characterized and public claims do not exceed it.
9. Raw-prompt versus compiled-contract evaluation has valid paired data with no systematic acceptance-quality regression.
10. Shared evidence shows no systematic full-task rediscovery; Terra delta and selective Sol may remain conservative if economics are inconclusive and correctness/safety is sound.
11. Luna Max / Terra XHigh / Sol High remain the frozen v1 routing baseline; route optimization moves to v1.x unless release-blocking evidence requires change.
12. Full CI and one fresh-clone clean-Codex-home RC smoke are green on exact release content; docs describe observed limitations; remaining P2/P3 work moves post-v1.

When items 1-12 are satisfied, the required action is **release v1.0.0**.

# v1.0.0 release execution plan

## Stage R1: finish live gates

Complete Checkpoints 1-6 in order. Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E and every P0/P1 candidate.

Patch only reproducible PROJECT P0/P1, P2 directly blocking a mandatory gate, and objectively stale test/docs relative to frozen architecture or current official Codex contract.

## Stage R2: RELEASE CANDIDATE and feature freeze

When mandatory gates are characterized and no PROJECT P0/P1 is open, declare `RELEASE CANDIDATE` and freeze architecture, routing, scheduling/recovery semantics, Plugin packaging, and evaluation scope.

## Stage R3: one fixed RC closure pass

Run exactly one RC closure pass:

- current official Plugin validator;
- Git marketplace add/upgrade + Plugin add + new-thread discovery;
- installed bundle script/template accessibility;
- authorized clean-Codex-home profile provisioning and four-role discovery;
- full deterministic CI;
- exact four-role routing smoke;
- Intervention Gate / child-observability recovery smoke;
- adaptive fan-out + native slot queue/recovery smoke;
- one-writer/depth-one smoke;
- installer safety/migration smoke;
- README/install docs checked against observed behavior.

If P0/P1 requires a fix, rerun the invalidated live gate, full CI, and this fixed RC pass. P2/P3 does not restart the architecture cycle unless it invalidates a mandatory gate.

## Stage R4: publish v1.0.0

- set Plugin version to `1.0.0`;
- merge exact tested content;
- tag exact tested commit;
- publish GitHub Release;
- mark validation complete in `LOCAL_VALIDATION_REPORT.md`;
- move remaining P2/P3 and route-economics questions to v1.x.

# Required validation artifact

`LOCAL_VALIDATION_REPORT.md` is the evidence ledger. Record after each checkpoint:

```text
REPOSITORY_SHA
RUNTIME / PLATFORM
WORKLOAD / FIXTURE
EXPECTED
ACTUAL
EVIDENCE CLASS
DEPENDENCIES SATISFIED / INVALIDATED
EXECUTION PROGRESS / FAILURE SIGNATURE
INTERVENTION / RECOVERY LEDGER / DECISION PROVENANCE
CHILD PROGRESS OBSERVABILITY
CONSENT / READY FRONTIER / SLOT EVIDENCE
PLUGIN VALIDATOR / MARKETPLACE / INSTALL EVIDENCE
DEFECT CLASSIFICATION
OPEN UNKNOWN
```

# Feedback protocol for continued adversarial review

`gpt56-sol-pro-consult` is the required adversarial consultation mechanism for Review Checkpoints A-E and immediately after any P0/P1 candidate.

Codex remains the local executor. Consultation output is `model_judgment` and must not be counted as evidence that Codex Delegate itself routed correctly. Do not replace this consultation with an ad hoc generic Sol call.

## Project consultation target

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

Rules:

1. Match `分支 · 分支 · 项目对比分析` exactly.
2. Continue that existing conversation for checkpoint review and project discussion.
3. Do not create a replacement ChatGPT conversation when the exact target is missing or ambiguous.
4. Do not choose a similarly named conversation by fuzzy match, recency, or guesswork.
5. Do not silently fall back to an isolated consultation conversation.
6. If exact unique resolution fails, return `CONSULTATION_TARGET_UNRESOLVED`.
7. If the user renames the project conversation, update this target from a user-confirmed title.
8. Every consultation still sends a compact current evidence packet.
9. Consultation returns as `model_judgment`; Codex reconciles it with repository/runtime evidence.

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
<actual runtime/build and platform when material>

COMPLETED_HEADOFF_ITEMS
<newly completed items>

NEW_EVIDENCE
<deterministic / repository / live runtime evidence>

DEPENDENCY_STATE
<ready/running/satisfied/invalidated facts>

EXECUTION_PROGRESS
<failure signature, progress signal, Intervention Gate outcome>

RECOVERY_STATE
<Recovery Ledger, proposed/effective action, decision source, policy transform>

RESOURCE_STATE
<consent, peak children, observed slots, queues, writer domains>

PLUGIN_STATE
<validator, marketplace/ref/sparse paths, Plugin/version, fresh-thread discovery, profile provisioning>

DEFECTS
<severity + ownership + reproduction, or none>

TESTS
<commands and exact outcomes>

CHANGES
<production/test/docs changes>

UNRESOLVED
<smallest remaining unknowns>

LOCAL_JUDGMENT
<executor conclusion>

ASK
Challenge severity, ownership, evidence sufficiency, strongest counterexample, and whether execution should continue without architecture change.
```

# Completion condition

There is no Checkpoint 7 and no automatic post-checkpoint optimization phase.

When Checkpoints 1-6 are characterized, the 12 Definition-of-Done conditions hold, full RC validation is green, and no reproducible PROJECT P0/P1 remains, release v1.0.0.
