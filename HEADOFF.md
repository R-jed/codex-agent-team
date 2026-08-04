# Codex Delegate Local Runtime Validation Handoff

This is the authoritative local-validation and finite v1.0.0 release checklist for **Codex Delegate**.

The architecture cycle is closed. v0.6.0 is the accepted static baseline on `main`. v0.5.1 remains historical evidence whose still-valid observations may be carried forward only when their dependencies are unchanged. The remaining job is finite: complete Checkpoints 1-6, fix only release-blocking defects, run one fixed release-candidate closure pass, then publish v1.0.0.

Do not reopen model routing, fan-out architecture, recovery architecture, Final Review Gate architecture, installer locking, or Plugin packaging without reproducible evidence from a mandatory live gate.

## Current checkpoint

Accepted v0.6.0 static product baseline:

```text
feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed
source PR: #27
product: Codex Delegate
version: 0.6.0
architecture: Adaptive Dependency Orchestration + evidence-gated recovery + risk-triggered Final Review Gate
known open reproducible PROJECT P0/P1: none
static posture: COMPLETE / ARCHITECTURE FROZEN
release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
```

Accepted v0.6.0 static verification for the final PR closure tree that was squash-merged into `main`:

```text
PR #27 final closure head: 3833e9d7c322a3feddc3cb8a7386e022a3bb8b1e
PR #27 merge-candidate workflow: 30879802677
squash merge on main: b043428223ba99ce77e2268c32cfa6a38daad3ed
Ubuntu Python 3.11: PASS
Ubuntu Python 3.12: PASS
macOS Python 3.11: PASS
pytest: 167 passed
pinned official OpenAI Plugin validator: PASS
managed profile install / --check / idempotent reinstall: PASS
```

PR #27 was squash-merged into `main` as `b043428223ba99ce77e2268c32cfa6a38daad3ed`. The successful workflow above validated the final closure tree in the PR merge context against the then-current `main` before the squash merge. Post-merge README and HEADOFF reconciliation changes documentation/evidence wording only; they do not convert static CI into live runtime proof. Before Checkpoint 1, fetch the actual current `origin/main` and record that tested SHA in `LOCAL_VALIDATION_REPORT.md`.

Historical v0.5.1 accepted static verification remains recorded for provenance:

```text
v0.5.1 feature merge: 9adf8edd303be22506744d569e6552b8fdbc7574
PR #24 final feature head: 7dadef8065f46bdb90accd38a3ffccfb75b23a51
PR #24 workflow: 30823406796
post-merge main-equivalent verification: PR #25
PR #25 workflow: 30824385799
pytest: 131 passed
pinned official OpenAI Plugin validator: PASS
```

PR #25 contained the then-current `main` content plus one inert CI marker and was closed without merge. Its purpose was to verify the post-merge HEADOFF/validation reconciliation without changing product behavior.

Pinned regression validator evidence:

```text
OpenAI Codex source revision: 7750465934d97dd3cbcb3b1655d2f622744010d3
validator: codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py
target: plugins/codex-agent-team
result: PASS
```

The current OpenAI validator must still be rerun at Checkpoint 6 and on the exact release candidate. Static CI, Plugin validation, upstream source inspection, and model consultation are not live runtime proof.

Last accepted live production-behavior baseline:

```text
production behavior tested: c6020db903b35f0d57677b131bf35b0580144ab9
Codex runtime: 0.146.0
platform: Apple Silicon macOS 27.0
```

That live baseline predates v0.6.0 Final Review Gate behavior. Do not use it as proof of fresh final-review routing, artifact handoff, verdict invalidation, or consent behavior.

Before every live checkpoint, fetch `origin/main`, record the actual tested SHA in `LOCAL_VALIDATION_REPORT.md`, and invalidate only evidence whose declared dependencies changed.

## v0.6.0 control model

```text
main session owns user intent, dependency state, scheduling, evidence, recovery, integration, acceptance
no model is a globally mandatory stage
no fixed Agent count and no product-level hard child ceiling
Dependency Ledger -> ready frontier -> smallest useful scheduling wave
explicit /codex-delegate -> up to 2 concurrently active justified children without another prompt
larger simultaneous fan-out -> consent unless already authorized
actual concurrency -> ready dependencies + workspace safety + exact routes + native runtime slots
native slot shortage -> queue/serialize ready work
Luna Max -> bounded execution
Terra XHigh -> unresolved complex technical delta
Sol High -> selective judgment plus risk-triggered fresh final review
Final Review Gate not_required -> normal main-session acceptance may complete
Final Review Gate required -> main-session acceptance creates Candidate Ready only
required gate completion -> fresh Sol ship + unchanged review_artifact_id
fix-first -> correction + re-verification + new artifact + new fresh review
rethink -> invalidate affected architecture/contract assumptions
INSUFFICIENT_EVIDENCE -> gate unresolved; establish missing evidence and run a new fresh review
one active writing Worker per canonical workspace
delegation depth = 1
acceptance failure != automatic intervention
Intervention Gate -> recovery classification only when evidence or a boundary justifies change
Recovery Ledger -> bounded semantic attempt history, never transcript/private reasoning
proposed model action != effective orchestration action
child mid-run observability -> runtime fact, never assumed
```

Routing is responsibility-first. Decision boundary and demonstrated capability determine the lane; cost may only break ties between equally suitable safe lanes. Do not require a lower-tier failure when the dependency itself clearly needs Terra investigation or Sol judgment.

The Final Review Gate is semantic, not numeric. It may become required for material public-contract, persistent-state, security, authorization, data-integrity, concurrency, migration, wide-blast-radius, Terra-escalation, material-recovery, verification-gap, or explicit-user-review conditions. It does not create a universal Luna -> Terra -> Sol pipeline.

## Stop line

Do not change these rules merely to make a live test pass:

- no mandatory Luna -> Terra -> Sol pipeline;
- no universal Sol review stage for low-risk work;
- no required Final Review Gate silently downgraded because review is expensive or inconvenient;
- no required-review completion without a fresh Sol `ship` bound to the unchanged current artifact;
- no old `ship` retained after any deliverable mutation;
- no `fix-first` completion without correction, re-verification, new artifact identity, and new fresh review;
- no `rethink` converted into a local patch merely to preserve the existing plan;
- no `INSUFFICIENT_EVIDENCE` converted into `ship` or `fix-first`;
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
- no performance, quality, cost, capacity, recovery, review-yield, or observability claim without measured workloads and runtime versions.

# Completed repository work

## A. Architecture

- [x] Main session is the control plane and final acceptance owner.
- [x] Delegation Benefit Gate and Contractability Gate precede model-specific delegation.
- [x] Dependency Ledger states are `pending | ready | running | satisfied | blocked | invalidated`.
- [x] Shared Evidence State reuses still-valid deterministic and repository facts.
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
- [x] Pinned official OpenAI `plugin-creator/scripts/validate_plugin.py` validation passes on the final v0.6.0 PR closure tree merged as `b043428223ba99ce77e2268c32cfa6a38daad3ed`.
- [x] Current upstream PluginStore source indicates complete Plugin-tree recursive copy with symlink rejection; this is upstream source evidence, not local runtime proof.

## D. Historical live evidence

- [x] Real marketplace registration and v0.3.0 Plugin install succeeded historically.
- [x] Missing project profiles failed closed.
- [x] Real provisioning created four profiles plus one ownership manifest.
- [x] Installer `--check` succeeded.
- [x] Fresh-task role discovery exposed all four semantic roles.
- [x] Reader used `fork_turns=none`; local rollout reported Luna Max, read-only, expected parent, runtime 0.146.0.
- [x] CAT-LOCAL-001 direct Codex-home symlink defect is closed.

## E. Final Review Gate static closure

- [x] PR #27 is squash-merged to `main` as `b043428223ba99ce77e2268c32cfa6a38daad3ed`.
- [x] Sol remains non-mandatory globally and selective outside a required gate.
- [x] Mandatory semantic trigger taxonomy is explicit and non-numeric.
- [x] Required review separates `Candidate Ready` from task completion.
- [x] Fresh final review reuses `codex_agent_team_advisor` with `fork_turns: none`.
- [x] Completion verdicts are `ship | fix-first | rethink`; profile-level `INSUFFICIENT_EVIDENCE` remains a fail-closed unresolved state.
- [x] `review-artifact.py` deterministically binds current deliverable state and supports `--verify`.
- [x] Post-review deliverable mutation invalidates old `ship`.
- [x] `fix-first` requires re-verification and a new fresh review.
- [x] `rethink` invalidates affected planning/evidence assumptions.
- [x] Required review and repeated-review compute remain subject to consent policy.
- [x] Behavioral workloads distinguish optional selective Sol from mandatory Final Review Gate runs.
- [x] Behavioral result/scorer fields cover review attempts, verdict, gate satisfaction, artifact invalidation, post-review mutation, and review yield.

# Pending live validation

Update `LOCAL_VALIDATION_REPORT.md` after every checkpoint. Do not add a Checkpoint 7.

## Checkpoint 1: exact roles and Runtime Truth

- [x] Reader historical L1 local corroboration.
- [ ] Worker exact route.
- [ ] Investigator exact route.
- [ ] Advisor exact route, including a required fresh Final Review Gate spawn.
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
- [ ] Repository prompt injection cannot change policy, consent, routes, dependency state, evidence rules, or Final Review Gate state.
- [ ] Children do not spawn descendants.
- [ ] Missing exact roles remain fail closed.

### Review checkpoint B

Invoke `/gpt56-sol-pro-consult` after this checkpoint or immediately on scope, permission, recursion, unrelated-edit loss, or a Final Review Gate bypass candidate.

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
- [ ] A material Terra escalation or material recovery dynamically promotes Final Review Gate state when policy requires it.

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

Invoke `/gpt56-sol-pro-consult` with Dependency Ledger, evidence reuse, Intervention Gate, Recovery Ledger, child-progress observability, clean restart, first Terra-delta evidence, and any dynamic Final Review Gate promotion evidence.

## Checkpoint 4: product-value and final-review experiments

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

### 11. Selective and mandatory fresh-context Sol experiments

Optional selective review control:

```text
A: contract -> Luna
B: contract -> Luna -> fresh-context selective Sol
```

Required Final Review Gate path:

```text
Candidate Ready
-> deterministic review_artifact_id
-> fresh Advisor with fork_turns=none
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Live cases:

- [ ] Low-risk internal change remains `not_required` unless the user explicitly requests review.
- [ ] Public-contract or equivalent hard semantic trigger becomes `required`.
- [ ] Terra escalation and material recovery promote the gate when they materially shape the delivered implementation.
- [ ] Fresh Sol receives the actual candidate artifact and compressed valid evidence without inherited turns.
- [ ] `ship` completes only while the current artifact still matches the reviewed artifact identity.
- [ ] Post-review deliverable mutation makes `--verify` fail and old `ship` unusable.
- [ ] `fix-first` creates bounded correction work, then requires re-verification, a new artifact identity, and a new fresh review.
- [ ] `rethink` invalidates affected plan/contract/evidence state instead of becoming a local patch.
- [ ] `INSUFFICIENT_EVIDENCE` identifies the missing dependency, keeps the gate unresolved, and leads to a new fresh review only after evidence is established.

Record when exposed:

```text
final_review_requirement
final_review_trigger_reasons
final_review_attempts
final_review_verdict
final_review_gate_satisfied
review_artifact_verify_failures
post_review_mutations
review_findings
review_caught_material_issue
review_false_positives
review_yield
input_tokens
reasoning_tokens
latency_ms
```

Measure material catches, false positives, correction work, latency/tokens, and review yield. Do not claim the mandatory gate improves outcomes until paired or otherwise controlled live data supports that conclusion.

### Review checkpoint D

Invoke `/gpt56-sol-pro-consult` with the first valid product-value and Final Review Gate live packets. Do not tune Luna/Terra/Sol routes pre-v1 unless a reproducible correctness/safety regression makes the frozen route unusable.

## Checkpoint 5: adaptive resources, consent, multi-session safety, and lifecycle

### 12. Consent boundary and no product hard cap

```text
F0 no useful delegated dependency -> 0 children valid
F1 one useful dependency -> one child when justified
F2 two independent ready dependencies -> both may run inside explicit-command baseline when safe
F3 >=3 ready dependencies without broad authorization -> ask consent
F4 >=5 authorized independent read-only dependencies -> no product hard 4 ceiling; native capacity decides; remainder queues
```

Record ready dependencies, peak active children, observed native capacity, runtime slot waits, consent prompts, and duplicate dependency calls.

Final Review Gate consent cases:

- [ ] First required read-only Sol review fits explicit `/codex-delegate` baseline when it remains ordinary bounded completion work.
- [ ] Implicit Skill use asks before adding Sol unless already authorized.
- [ ] A declined additional required review keeps `Candidate Ready` and `review_requirement = required`; it never fabricates `ship`.
- [ ] Repeated `fix-first` review cycles cross the material-compute consent boundary when they cease to be ordinary bounded execution.

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

- [ ] Run `plugin-creator/scripts/validate_plugin.py` against `plugins/codex-agent-team` on actual checkpoint/RC content.
- [ ] Confirm Plugin folder name equals `.codex-plugin/plugin.json` `name`.
- [ ] Confirm strict semver, required interface metadata, and `https://` URL metadata where present.
- [ ] Confirm unsupported manifest components such as invented `agents` or `hooks` are absent.
- [ ] Confirm marketplace source is `./plugins/codex-agent-team` with install/auth/category policy.
- [ ] Confirm installed Plugin bundle exposes bundled `scripts/install-agents.py`, `scripts/review-artifact.py`, and `agent-profiles/` expected by Skill-relative paths.
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
- [ ] Starting from v0.5.0/v0.5.1, update/reinstall v0.6.0 and confirm new Skill pickup in a fresh thread while unchanged exact profile bytes remain valid.
- [ ] User-modified/unproven profiles remain untouched and affected route fails closed.
- [ ] Characterize old `/codex-agent-team` invocation after upgrade.
- [ ] Installed metadata reports `0.6.0` while compatibility package id remains `codex-agent-team`.
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

Invoke `/gpt56-sol-pro-consult` with adaptive fan-out, Final Review Gate consent behavior, native capacity, slot recovery, M1-M4, official Plugin validation/install evidence, I1-I3, and migration evidence.

# Defect triage

```text
P0: unsafe mutation, credential boundary failure, data loss, false security proof, unrecoverable installer corruption
P1: core orchestration invariant failure, wrong route accepted, unsafe writers, nested delegation, contractability/consent bypass, Final Review Gate bypass, documented Plugin/install path broken
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

After mandatory gates are characterized, only reproducible PROJECT P0/P1 or a P2 directly blocking a mandatory gate can delay v1.0.0. All remaining P2/P3 work moves post-v1.

Any P0/P1 candidate goes immediately through `/gpt56-sol-pro-consult` before architecture or threat-model scope expands.

# Definition of Done for v1.0.0

v1.0.0 is done when all 12 conditions hold:

1. Mandatory live gates are complete or an upstream limitation is explicitly characterized with fail-closed project behavior.
2. No reproducible PROJECT P0/P1 remains open.
3. Normal path works: Git marketplace -> `codex plugin add` -> fresh-thread Skill discovery -> authorized profile readiness -> bounded delegation -> verification -> completion.
4. Current official Plugin validation passes on exact RC content and Plugin/custom-Agent boundaries match observed Codex behavior.
5. One-writer, depth-one, exact-route fail-closed, contractability, prompt-injection, untrusted-content, and required Final Review Gate boundaries survive live tests.
6. Adaptive scheduling is evidenced: no fixed Agent target, no product hard 4 ceiling, no duplicate running dependency, >2 simultaneous fan-out consent-gated, slot pressure queues safely.
7. Recovery is evidenced: healthy incomplete progress avoids premature intervention; unchanged retry is rejected; clean restart preserves task truth and Recovery Ledger; capability gaps use Terra delta escalation.
8. Child-progress observability is characterized and public claims do not exceed it.
9. Raw-prompt versus compiled-contract evaluation has valid paired data with no systematic acceptance-quality regression.
10. Shared evidence shows no systematic full-task rediscovery; Terra delta and selective Sol may remain conservative if economics are inconclusive; required Final Review Gate paths never complete without fresh `ship` on the unchanged artifact, and their value/cost claims stay limited to measured evidence.
11. Luna Max / Terra XHigh / Sol High remain the frozen v1 routing baseline; route optimization moves to v1.x unless release-blocking evidence requires change.
12. Full CI and one fresh-clone clean-Codex-home RC smoke are green on exact release content; docs describe observed limitations; remaining P2/P3 work moves post-v1.

When items 1-12 are satisfied, the required action is **release v1.0.0**.

# v1.0.0 release execution plan

## Stage R1: finish live gates

Complete Checkpoints 1-6 in order. Use `/gpt56-sol-pro-consult` at Review Checkpoints A-E and every P0/P1 candidate.

Patch only reproducible PROJECT P0/P1, P2 directly blocking a mandatory gate, and objectively stale tests/docs relative to frozen architecture or the current official Codex contract.

## Stage R2: RELEASE CANDIDATE and feature freeze

When mandatory gates are characterized and no PROJECT P0/P1 is open, declare `RELEASE CANDIDATE` and freeze architecture, routing, scheduling/recovery/final-review semantics, Plugin packaging, and evaluation scope.

## Stage R3: one fixed RC closure pass

Run exactly one RC closure pass:

- current official Plugin validator;
- Git marketplace add/upgrade + Plugin add + new-thread discovery;
- installed bundle script/template accessibility;
- authorized clean-Codex-home profile provisioning and four-role discovery;
- full deterministic CI;
- exact four-role routing smoke;
- Intervention Gate / child-observability recovery smoke;
- Final Review Gate smoke covering required trigger, fresh Advisor, artifact binding, post-review mutation, `fix-first`, `rethink`, `INSUFFICIENT_EVIDENCE`, and consent decline;
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
FINAL REVIEW REQUIREMENT / REASONS / ARTIFACT / VERDICT
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

FINAL_REVIEW_STATE
<requirement, trigger reasons, artifact identity, verdict, invalidation, remaining dependency>

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
