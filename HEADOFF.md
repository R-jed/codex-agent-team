# Local Runtime Validation Handoff

This file is the authoritative execution checklist for the local validation and v1.0.0 release phase of `R-jed/codex-agent-team`.

The architecture cycle is closed. The remaining job is finite: complete the mandatory live gates, resolve only release-blocking defects, run one release-candidate closure pass, then publish v1.0.0. Do not continue pre-release optimization after the Definition of Done is met.

## Current checkpoint

Last live-tested production baseline:

```text
production behavior tested: c6020db903b35f0d57677b131bf35b0580144ab9
Codex runtime tested so far: 0.146.0
platform tested so far: Apple Silicon macOS 27.0
local deterministic suite after CAT-LOCAL-001 fix: 97 passed
remote branch hygiene at the last validated checkpoint: origin/main only
known open PROJECT P0/P1 defects: none
release posture: HOLD FOR RELEASE while mandatory live gates remain incomplete
```

`c6020db...` is an evidence baseline, not a permanently current HEAD. At the start of every checkpoint, fetch `origin/main`, record the actual SHA in `LOCAL_VALIDATION_REPORT.md`, and inspect any intervening production changes before reusing prior evidence.

The current `main` also contains the v1 concurrency-scope policy iteration added after the last live-tested baseline. Its policy and regression files are repository facts, but its new cross-session and concurrent-installer claims remain unverified until Checkpoints 5 and 6 run locally.

Status notation:

- `[x]` means reproducible evidence exists in `LOCAL_VALIDATION_REPORT.md` or merged repository history.
- `[ ]` means the live gate is still required.
- `PARTIAL` means only part of the acceptance condition is evidenced. Keep the checkbox open until the full condition is characterized or explicitly classified as an upstream limitation with a safe project fallback.

The control model remains:

```text
main session owns the task-level compute graph
no model is a mandatory stage
Luna Max = default bounded execution
Terra XHigh = unresolved complex technical delta only
Sol High = selective judgment / review
main-session child envelope = normal max 2, v1 hard max 4
canonical workspace = at most one active writing Worker
Codex home = one shared managed Agent-profile generation
delegation depth = 1
evidence is reused until its dependencies are invalidated
every Agent call must satisfy a distinct unresolved dependency
```

Concurrency is scoped, not global:

```text
session scope
-> child-count envelope and compute graph

workspace scope
-> write ownership for one canonical physical checkout or isolated worktree

Codex-home scope
-> shared semantic Agent profiles and ownership manifest
```

Different independent projects must not be blocked merely because another main session has active children. Two sessions targeting the same physical checkout still share the one-writer invariant.

## Stop line

Do not change these rules merely to make a live test pass:

- no mandatory Terra or Sol stage;
- no generic whole-task Terra rerun because Luna quality looks weak;
- no silent expansion of decision rights through model escalation;
- no more than one active writer in one canonical shared checkout;
- no file-level partitioning used to justify multiple writing Workers in one physical checkout;
- no child-created descendants;
- no cross-role substitution when an exact project profile is unavailable;
- no configured route fact presented as runtime observation;
- no incomplete expected route accepted as exact runtime proof;
- no missing runtime evidence converted to affirmative success;
- no systematic rediscovery of still-valid deterministic or repository evidence;
- no weakened acceptance oracle because a model failed it;
- no claim that the v1 hard maximum of four children is a machine-wide, account-wide, or native-runtime capacity limit;
- no project-wide global writer mutex that blocks independent workspaces merely to make same-checkout safety easy;
- no workspace-lock daemon, Codex-home lock, or installer serialization mechanism before a reproducible live failure proves the current runtime/filesystem behavior cannot satisfy the invariant;
- no performance, quality, or cost claim without measured named workloads and runtime versions.

If a live Codex limitation makes an invariant impossible, record the exact runtime behavior first and classify ownership before changing project policy.

# Completed work

## A. Repository and static baseline

- [x] Fresh local checkout/fetch baseline established and environment versions recorded.
- [x] Development dependencies installed in an isolated local environment.
- [x] Initial deterministic suite passed with 96 tests.
- [x] Post-fix deterministic suite passed with 97 tests.
- [x] Plugin and marketplace manifests parse as valid JSON.
- [x] Isolated managed-profile first install succeeds.
- [x] Isolated installer `--check` is non-mutating.
- [x] Isolated second install is a true no-op.
- [x] Isolated install creates only four project profiles plus the ownership manifest.
- [x] Historical branch audit completed and the ten merged historical refs were deleted.
- [x] Remote branch inventory was rechecked as `origin/main only` at the last validation checkpoint.
- [x] v1 policy now distinguishes main-session, canonical-workspace, and Codex-home concurrency scopes without changing normal max 2, hard max 4, one-writer, or depth-one baselines.
- [x] Delegation Contract and Skill now require writing Workers to preserve unrelated concurrent edits, re-read affected state before mutation when drift is plausible, and stop when drift makes the contract stale.
- [x] Static regression coverage protects the new concurrency-scope contract. Live enforcement remains open below.

## B. Real Plugin path and role discovery

- [x] Marketplace registration succeeds from the documented Git source and `main` ref.
- [x] `codex-agent-team@codex-agent-team` v0.3.0 installs through the documented Plugin path.
- [x] Missing project profiles fail closed rather than cross-routing to another role.
- [x] Real profile provisioning writes the four project profiles plus one ownership manifest.
- [x] Real profile provisioning `--check` succeeds.
- [x] No unrelated Agent profile mutation was observed in the tested clean environment.
- [x] A task created before provisioning did not refresh custom-role discovery on Codex 0.146.0.
- [x] A fresh task after provisioning discovered all four semantic roles.
- [ ] PARTIAL: verify the complete first-run consent copy shown by the Skill matches the documented managed write/migration scope.

## C. Exact role/runtime evidence already observed

- [x] `codex_agent_team_reader` spawned with explicit `fork_turns=none`.
- [x] Reader returned the bounded probe result.
- [x] Reader local rollout inspection reported `gpt-5.6-luna`, effort `max`, read-only sandbox, managed permission profile, runtime 0.146.0, and the expected parent thread.
- [x] Reader result is limited to L1 local corroboration because independent native attestation was not separately exposed.
- [ ] `codex_agent_team_worker` exact live route still needs a real spawn and observation.
- [ ] `codex_agent_team_investigator` exact live route still needs a real spawn and observation.
- [ ] `codex_agent_team_advisor` exact live route still needs a real spawn and observation.

## D. Closed live defect

### CAT-LOCAL-001: direct Codex-home endpoint symlink

- [x] Real filesystem reproduction established the pre-fix defect.
- [x] Classified as `PROJECT/P1`.
- [x] Root cause identified at `expanduser().resolve()` before endpoint validation.
- [x] Minimal fix rejects a Codex-home endpoint that is itself a symlink before resolving it.
- [x] Arbitrary ancestor symlinks remain intentionally supported.
- [x] Public CLI regression was red before the fix and green after it.
- [x] Regression proves non-zero exit, explicit error, unchanged prior file state, and zero target directory entries.
- [x] Installer suite passed with 14 tests and complete local suite passed with 97 tests.
- [x] Real filesystem reproduction now exits 1 with zero target entries.
- [x] Fix and regression are present in merged production history.
- [x] Independent patch review verdict: `PATCH ACCEPTED`.

Residual pathname TOCTOU under concurrent local mutation is outside the threat model of this focused patch. Reopen only if new evidence makes that threat model release-relevant.

## E. Rejected current defect claim

- [x] The reported `inspect-runtime.py` failure with two `session_meta` records was reproduced only through a generic child using `fork_turns=all`.
- [x] The supported exact Reader path using `fork_turns=none` inspected successfully.
- [x] Current classification: latent rollout-schema compatibility risk, not a confirmed Plugin defect.

Reopen only if an exact project role using the supported fork policy produces legitimate multiple session metadata records that break inspection.

# Pending live validation

Execute the remaining gates in order. Update `LOCAL_VALIDATION_REPORT.md` after each checkpoint. Do not expand the checklist merely because an additional optimization is imaginable.

## Checkpoint 1: complete exact-role and Runtime Truth coverage

### 1. Exact custom-Agent route matrix

Run tiny bounded responsibilities with explicit `fork_turns=none`.

- [x] Reader: Luna Max / read-only / parent matched / L1 local corroboration.
- [ ] Worker: expected Luna Max / workspace-write.
- [ ] Investigator: expected Terra XHigh / read-only.
- [ ] Advisor: expected Sol High / read-only.

Record only runtime facts actually exposed: thread id, parent id, role, model, reasoning effort, effective sandbox/permission, runtime/build.

### 2. Runtime Truth adversarial matrix

- [x] Static verifier covers incomplete expected route fail-closed semantics.
- [x] Static verifier covers typed route/ancestry/permission independence.
- [x] One real Reader local rollout was sanitized successfully.
- [ ] Characterize complete native metadata if exposed.
- [ ] Characterize partial native route behavior.
- [ ] Characterize complete local route without native route.
- [ ] Exercise native/local agreement when both sources exist.
- [ ] Exercise model conflict.
- [ ] Exercise parent-thread conflict, wrong parent, and missing parent.
- [ ] Exercise required read-only with missing or broader native sandbox evidence.
- [ ] Exercise sandbox/permission-profile conflict.
- [ ] Exercise thread-id conflict.
- [ ] Characterize rollout schema drift and duplicate rollout files against the current Codex build.

Required summary semantics:

```text
incomplete expected route -> fail closed
missing observation -> not_observed / partial
complete matching native route -> R1
complete matching native + local route -> R2
complete local route alone -> at most L1
material conflict -> X0 + quarantine
```

### Review checkpoint A

After the four-role matrix and materially available Runtime Truth cases are complete, invoke `gpt56-sol-pro-consult` using the feedback protocol below. Do not change runtime policy before that adversarial review returns.

## Checkpoint 2: contractability, scope, and user safety

### 3. Contractability simulations

- [ ] Case A: already-located one-line deterministic defect remains main-session only with zero children.
- [ ] Case B: bounded implementation produces an enforceable Delegation Contract before Luna Worker execution.
- [ ] Case C: ambiguous product semantics do not reach a writing Worker before decision rights and acceptance are clear.
- [ ] Case D: an out-of-contract architecture/product/security/migration/public-contract decision returns `JUDGMENT_REQUIRED` or equivalent.
- [ ] Case E: a concurrent user edit inside or adjacent to the write scope is preserved; affected evidence is invalidated, and the Worker stops if the change makes the contract or acceptance oracle stale.

A writing contract must contain meaningful `OUTCOME`, `SCOPE`, `CONCURRENCY / DRIFT`, `INVARIANTS`, `DECISION RIGHTS`, `ACCEPTANCE ORACLE`, `VERIFICATION`, and `STOP / ESCALATE`.

### 4. Prompt-injection and scope-boundary simulation

- [ ] Repository instructions remain untrusted data.
- [ ] Writing tasks do not expand changed-file scope because of embedded instructions.
- [ ] Child Agents do not spawn descendants.
- [ ] Missing exact roles remain fail closed.
- [ ] Actual changed files are independently inspected after every writing task.

### Review checkpoint B

Invoke `gpt56-sol-pro-consult` immediately if ambiguity crosses into writing, nested delegation appears, repository content changes orchestration policy, or concurrent drift causes unrelated edits to be reverted. Otherwise consult after the checkpoint before proceeding to product-value experiments.

## Checkpoint 3: incremental orchestration value

### 5. Shared Evidence State and invalidation

Create a task where the first Agent establishes E01 reproduction, E02 caller path, E03 focused-test baseline, and E04 public-interface fact.

- [ ] A later Agent receives relevant still-valid evidence.
- [ ] It does not rerun E01-E04 merely to rebuild context.
- [ ] An unrelated file change does not invalidate unrelated evidence.
- [ ] A declared dependency change invalidates only affected evidence.
- [ ] A concurrent user or independent-session change invalidates only evidence that depends on the changed state.
- [ ] Model judgments remain challengeable hypotheses.

Record `unjustified_repeated_commands`, `unjustified_repeated_discovery`, `duplicate_dependency_calls`, `evidence_established`, and `evidence_invalidated`.

### 6. Luna failure classification

- [ ] mechanical defect -> focused Luna correction.
- [ ] contract gap -> main session repairs the contract.
- [ ] capability gap -> Terra receives only the unresolved technical delta.
- [ ] judgment gap -> main session decides or uses justified Sol.
- [ ] workspace drift -> reconcile changed input and repair only invalidated contract/evidence; do not escalate merely because state changed.
- [ ] low quality alone never causes a whole-task Terra restart.

### 7. Terra delta-escalation experiment

Compare at least three controlled pairs if cost permits:

```text
A: restart the whole task with Terra
B: Terra receives unresolved delta + valid evidence + current artifact + DO NOT REDO
```

- [ ] Correctness measured.
- [ ] Repeated discovery and deterministic commands measured.
- [ ] Tokens recorded only when exposed.
- [ ] Latency and main-session correction work recorded.

Do not claim delta escalation is better until paired evidence supports it.

### Review checkpoint C

Invoke `gpt56-sol-pro-consult` with the Shared Evidence and first Terra pair evidence before modifying evidence or routing policy.

## Checkpoint 4: product-value experiments

### 8. Primary raw-prompt versus compiled-contract experiment

Highest-priority behavioral comparison:

```text
A: raw user prompt -> Luna Max
B: same user prompt -> main session compiles Delegation Contract -> Luna Max
```

Freeze each workload with `evals/LOCAL_EVAL_FIXTURE_TEMPLATE.md`. Every pair records:

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

- [ ] At least one valid controlled pair is produced before scaling.
- [ ] Target at least five paired repeats across representative bounded workloads if cost permits.
- [ ] Result JSON validates against `evals/behavioral-result.schema.json`.
- [ ] `scripts/score-behavioral-evals.py` accepts the result.
- [ ] Primary conclusions use candidate-minus-baseline paired deltas.
- [ ] No missing token, latency, route, or runtime telemetry is estimated.

### 9. Luna + selective Sol experiment

Compare:

```text
A: contract -> Luna Max -> main acceptance
B: contract -> Luna Max -> selective Sol review -> main acceptance
```

- [ ] At least three controlled pairs per selected workload if cost permits.
- [ ] Material issues caught, false positives, correction work, latency, exposed tokens, and final acceptance score recorded.
- [ ] Sol receives the actual artifact plus compressed evidence and does not rescan without a named missing dependency.

### Review checkpoint D

Invoke `gpt56-sol-pro-consult` with the first valid raw-vs-contract results and first Sol pair set before changing model/effort routing.

## Checkpoint 5: resource governance and lifecycle stress

### 10. Useful parallelism

- [ ] Two independent read-only Luna branches satisfy different dependencies concurrently and the parent requires both outputs.
- [ ] Two independent main sessions on different projects/checkouts can each use justified children without a project-created machine-wide concurrency bottleneck.

### 11. Duplicate inference rejection

- [ ] One question with no independent dependencies does not trigger redundant Luna/Terra/Sol parallel inference.

### 12. Workspace-scoped one-writer and multi-session matrix

Use real independent main sessions where the case requires them. Record canonical workspace identity, main-session identity, child thread ids when exposed, start/overlap/close timing, and actual changed files.

- [ ] Same main session, same physical checkout: attempt two writing Workers; the second concurrent writer is not launched.
- [ ] M1 different sessions, different projects/checkouts: one Worker in each may proceed concurrently when native capacity permits.
- [ ] M2 different sessions, same repository, different runtime-backed isolated worktrees: one Worker in each may proceed concurrently when filesystem isolation is real. If the current Codex runtime cannot preserve this isolation, classify the limitation as upstream before changing project policy.
- [ ] M3 different sessions, same canonical physical checkout: attempt one Worker from each session; never accept a state with two simultaneous writing Workers. If both become active against the same checkout, classify as `PROJECT/P1 candidate` unless native runtime evidence shows the project cannot observe or control the collision and ownership must be reassessed.
- [ ] M4 one writing session plus one read-only session on the same checkout: after writer mutation, stale read-side repository evidence is invalidated or revalidated before acceptance rather than silently reused.
- [ ] No test uses disjoint intended file lists as proof that simultaneous writers are safe in one physical checkout.

Do not implement a workspace lock before M3 establishes a reproducible failure. If M3 fails, prefer the smallest workspace-scoped mechanism that blocks only the conflicting canonical checkout and does not serialize independent projects or isolated worktrees.

### 13. Fan-out consent and native capacity characterization

- [ ] Attempt three children without broad-parallel authorization.
- [ ] Consent is requested before exceeding the normal two-child envelope.
- [ ] With explicit authorization, characterize three-child and four-child behavior when practical: spawn success, latency, slot recovery, and failure mode.
- [ ] Keep `hard maximum = 4` as the frozen v1 policy even if native capacity is higher. If native capacity is lower, record the upstream limit and ensure the Skill fails safely rather than inventing capacity.
- [ ] Do not infer a machine-wide or account-wide limit from one main session's observed capacity.

### 14. Lifecycle stress

Run at least 10 sequential harmless read-only spawn/wait/close cycles, preferably 20 if cost permits.

- [ ] 10-cycle minimum completed.
- [ ] Concurrency slots return to expected state after close.
- [ ] No unexplained orphan children remain.
- [ ] Wait, interrupt/cancel, and spawn-failure recovery characterized.
- [ ] Closing one child does not corrupt siblings or the main task.

### Review checkpoint E

Invoke `gpt56-sol-pro-consult` immediately if capacity leaks, orphan children, nested delegation, same-checkout writer overlap, false global writer blocking, or sibling corruption appears. Otherwise send the checkpoint packet after stress completion.

## Checkpoint 6: installer migration and fault injection

- [x] clean install.
- [x] exact repeat no-op.
- [x] direct symlinked Codex-home endpoint rejects with zero target entries.
- [ ] current managed profile modified by user -> refuse overwrite.
- [ ] unrelated TOML claiming a reserved semantic role -> refuse.
- [ ] proven legacy model-named profile -> migrate safely.
- [ ] unproven legacy profile -> preserve.
- [ ] stale standalone manifest after migration -> does not re-delete a recreated user file.
- [ ] symlinked managed agents directory / manifest / profile entry -> reject as documented.
- [ ] unwritable agents directory.
- [ ] interrupted or staged replacement.
- [ ] disk-full or manifest-write failure if practical.
- [ ] rollback after a failure following at least one profile mutation.
- [ ] post-success cleanup failure if safely reproducible.

### 15. Concurrent Codex-home installer matrix

Use separate OS processes so this tests shared filesystem state, not one Python call stack.

- [ ] I1 same clean `CODEX_HOME`, same shipped profile generation, two installers start concurrently. Accept only exact convergence or one safe refusal. Final four profiles and manifest must be exact, and no staging or backup debris may remain.
- [ ] I2 one installer is forced to fail after mutation begins while a peer installer is allowed to succeed. The failing process must not roll back or corrupt a peer-success state. Final state must be exact or both operations must have failed closed without managed-file corruption.
- [ ] Re-run I1 with pre-existing exact managed state to characterize concurrent idempotent checks/installs.
- [ ] Characterize two independent sessions expecting different managed profile generations in one Codex home. v1 support contract is one installed generation; any mismatched lane must stop on exact-route conflict rather than cross-role substitute. Do not claim simultaneous mixed-generation support.
- [ ] Record process exit codes, final profile hashes, manifest bytes/hash, leftover staging/backup entries, and whether any successful peer state was later reverted.

Do not add an inter-process installer lock merely because races are theoretically possible. If I1 or I2 produces corruption or rollback of a peer-success state, classify the concrete reproduction first and implement the smallest fail-closed serialization or compare-and-swap mechanism that closes it.

For every failure verify profile bytes, ownership manifest, unrelated files, staging files, and backups after recovery.

# Version-scoped unknowns and technical debt

Use this register to avoid rediscovering already-characterized items.

- **U1 RESOLVED for Codex 0.146.0:** current task did not refresh roles after provisioning; a fresh task did.
- **U2 PARTIAL:** Reader local rollout exposed route/parent/sandbox metadata; native independent attestation and three roles remain open.
- **U3 PARTIAL:** supported Reader `fork_turns=none` inspected successfully; generic `fork_turns=all` multi-session behavior is not a current Plugin defect.
- **U4 PARTIAL:** Reader reported read-only sandbox; host-enforced denial is not yet demonstrated for all read-only roles.
- **U5 PARTIAL:** `fork_turns=none` works for Reader; other roles remain open.
- **U6 OPEN:** Shared Evidence compliance is unmeasured live.
- **U7 OPEN:** Luna Max is a frozen v1 baseline, not a proven globally optimal effort level.
- **U8 OPEN:** Terra XHigh value as delta Investigator remains unproven.
- **U9 OPEN:** Sol High selective-review value remains unproven.
- **U10 OPEN:** repeated lifecycle behavior remains untested.
- **U11 PARTIAL:** normal installer/no-op/direct symlink are live-tested; remaining failure modes are open.
- **U12 PARTIAL:** real Plugin installation and recovery work; exact first-run consent copy remains open.
- **U13 P2 MAINTENANCE:** dependencies are lower-bound compatible rather than release-locked. Do not block v1 solely for this unless reproducible drift occurs.
- **U14 RESOLVED:** historical merged branches were cleaned at the last validation checkpoint.
- **U15 ONGOING:** runtime/tool version drift requires version-scoped evidence, not perpetual pre-release retesting.
- **U16 NON-BLOCKING SO FAR:** read-only Git temporary-cache warning did not break the Reader probe.
- **U17 OPEN:** cross-session one-writer enforcement for two independent main sessions targeting the same canonical physical checkout has not been demonstrated live.
- **U18 OPEN:** same-Codex-home installer behavior is single-process transactional today; multi-process convergence and rollback interaction remain uncharacterized.
- **U19 OPEN:** one installed managed profile generation per Codex home is the v1 support boundary; concurrent sessions expecting different generations still require live fail-closed characterization.

# Defect triage

Classify each new failure before patching:

```text
P0
unsafe mutation, credential/scope boundary failure, data-loss risk,
false runtime security proof, or installer corruption without safe recovery

P1
core orchestration invariant fails, wrong model/role is accepted as exact,
multiple writers appear in one shared checkout, nested delegation occurs,
contractability is bypassed, or the normal documented install path is broken

P2
non-blocking UX friction, measurable inefficiency, maintenance drift,
telemetry compatibility limitation with a safe fallback, or documentation mismatch

P3
cosmetic cleanup, optional ergonomics, or speculative optimization
```

Ownership is one of `PROJECT`, `UPSTREAM_CODEX_RUNTIME`, `ENVIRONMENT`, `TEST_FIXTURE`, or `UNKNOWN`.

Only reproducible PROJECT P0/P1 defects block the v1.0.0 release once the mandatory live gates are characterized. P2/P3 items go to the post-v1 backlog unless they are trivial and zero-risk to close during the fixed RC pass.

# Release acceptance gate

The repository remains **HOLD FOR RELEASE** while mandatory live validation is incomplete. This does not mean a known P0/P1 is currently open.

Release can move to `RELEASE CANDIDATE` when all of these are evidenced:

- [x] deterministic repository suite green on accepted production content before the current concurrency-policy iteration.
- [ ] deterministic repository suite green on the current concurrency-policy iteration.
- [x] historical remote branches cleaned at the validated checkpoint.
- [x] documented marketplace and Plugin installation path works in a clean real environment.
- [x] all four semantic roles are discoverable after the documented fresh-task recovery path.
- [x] managed profile provisioning changed no unrelated Agent files in the tested clean environment.
- [ ] all four semantic roles have sufficient live route characterization for their intended claims.
- [ ] depth-one rules hold in live use.
- [ ] same-checkout one-writer holds when two independent main sessions target the same canonical physical checkout.
- [ ] independent projects or isolated workspaces are not serialized by a false project-created global writer mutex.
- [ ] partial runtime evidence never produces a live false-positive exact match.
- [ ] live cross-source conflicts quarantine the correct typed concern where both sources exist.
- [ ] ambiguous writing tasks stop before unsafe delegation.
- [ ] concurrent user/session workspace drift preserves unrelated edits and invalidates only dependent evidence.
- [ ] Luna failure classification avoids generic Terra reruns.
- [ ] Shared Evidence tests show no systematic full-task rediscovery while dependencies remain valid.
- [ ] behavioral pair controls pass schema/scorer integrity checks.
- [ ] lifecycle stress has no unexplained orphan/slot leak.
- [ ] installer fault injection has no unrecovered managed-file corruption.
- [ ] concurrent same-Codex-home installer tests converge or fail closed without peer-success rollback or managed-state corruption.
- [ ] mixed profile-generation conflict is characterized as a v1 unsupported case that stops the affected lane without cross-role substitution.
- [x] CAT-LOCAL-001 has no remaining patch-scope blocker and is merged.
- [ ] no new PROJECT P0/P1 remains after pending live gates.
- [ ] performance and cost statements are limited to measured named workloads and runtime versions.

# Definition of Done for v1.0.0

This project must stop pre-release iteration when the following finite standard is met.

## Product correctness

1. Every mandatory release-acceptance checkbox above is either `[x]` or explicitly classified as an upstream/runtime limitation with a documented fail-closed project behavior that preserves the invariant.
2. No reproducible PROJECT P0/P1 remains open.
3. The normal user path works from marketplace registration through Plugin installation, profile readiness, fresh-task role discovery, bounded delegation, verification, and user-visible completion.
4. One-writer across independent sessions sharing one canonical checkout, depth-one, exact-route fail-closed, contractability, concurrent-drift preservation, and untrusted-content boundaries survive live tests. Independent workspaces remain independently writable when the runtime provides real isolation.

## Product value

5. The primary raw-prompt versus compiled-contract experiment has valid paired data on representative bounded work and does not show a systematic acceptance-quality regression from contract compilation.
6. Shared Evidence testing does not show systematic full-task rediscovery when dependencies remain valid.
7. Terra delta escalation and selective Sol are allowed to remain conservatively scoped if their economic advantage is inconclusive, provided they do not show a reproducible correctness/safety regression and README claims remain limited to measured evidence.
8. Luna Max / Terra XHigh / Sol High are frozen as the v1.0.0 routing baseline. Effort tuning and model-route optimization move to v1.1+ and cannot delay v1.0.0 merely because a cheaper or faster route might exist.

## Release engineering

9. Full deterministic CI is green on the exact release-candidate content across the maintained matrix.
10. A fresh-clone, clean-Codex-home RC smoke pass succeeds for Plugin install, four-role discovery, one representative Worker task, one read-only route, one two-session same-checkout writer-collision check, depth-one enforcement, concurrent same-Codex-home installer safety, and the installer critical-path cases that previously produced PROJECT P1 evidence.
11. Documentation describes observed limitations without claiming unmeasured performance, native capacity, cross-session exclusion, mixed-profile-generation support, or multi-process installer guarantees.
12. Remaining P2/P3 items are recorded as post-v1 work and are not used to reopen the pre-release architecture cycle.

When items 1-12 are satisfied, the required action is **release v1.0.0**, not another optimization pass.

# v1.0.0 release execution plan

## Stage R1: finish mandatory live validation

Complete Checkpoints 1-6. At Review Checkpoints A-E, use `gpt56-sol-pro-consult` for adversarial review. Patch only reproducible PROJECT P0/P1 or a P2 that directly prevents completion of a mandatory gate.

The concurrency additions remain inside Checkpoints 2, 3, 5, and 6. They do not create new checkpoints, raise the frozen v1 child limits, or authorize a new scheduler/lock architecture without failure evidence.

## Stage R2: declare RELEASE CANDIDATE and feature freeze

When the Release acceptance gate is satisfied:

- declare `RELEASE CANDIDATE` in `LOCAL_VALIDATION_REPORT.md`;
- freeze architecture, role definitions, model routes, and new features;
- create/update release notes and a changelog entry;
- prepare version `1.0.0` in Plugin metadata on a release branch or focused PR;
- do not add new experiments to the mandatory gate list.

During feature freeze, only P0/P1 fixes, required release metadata, and evidence-backed documentation corrections may change behavior.

## Stage R3: one fixed RC closure pass

On the exact release candidate commit:

- run complete deterministic CI;
- validate both manifests;
- run managed-profile install / `--check` / idempotent reinstall;
- fresh-install the Plugin in a clean Codex home;
- confirm four roles discover after the documented recovery path;
- execute one bounded Worker smoke task and one read-only role smoke task;
- run one two-independent-session same-checkout writer-collision smoke and confirm independent workspaces are not falsely serialized;
- recheck depth-one behavior;
- rerun one concurrent same-Codex-home installer convergence case;
- rerun the critical installer safety cases that previously produced PROJECT P1 evidence;
- verify README/HEADOFF/release notes match the tested runtime scope.

If this pass finds a PROJECT P0/P1, fix only that defect, rerun its invalidated gate plus full CI, and repeat the RC closure pass. P2/P3 does not restart the release cycle unless it invalidates a mandatory gate.

## Stage R4: publish the full release

When the fixed RC closure pass is green:

1. set Plugin version to `1.0.0`;
2. ensure README status says stable v1.0.0 and links measured limitations;
3. merge the release PR;
4. create Git tag `v1.0.0` on the exact tested release commit;
5. create the GitHub v1.0.0 release with concise release notes, installation path, supported runtime evidence, and known non-blocking limitations;
6. mark the local validation cycle complete;
7. move every remaining P2/P3/speculative optimization to v1.x backlog or issues.

After v1.0.0 is published, do not keep `HEADOFF.md` as an open-ended pre-release repair loop. Any further route tuning, cost optimization, additional stress coverage, or model experiments belong to a new v1.x milestone with separate evidence and scope.

# Required validation artifact

Maintain `LOCAL_VALIDATION_REPORT.md` as the evidence record. For each completed checkbox add runtime version, repository revision, prompt/command, expected result, actual result, and reproducible evidence when material.

For multi-session cases, record each main session separately and identify the canonical workspace each session targeted. For concurrent installer cases, record each process separately and capture final managed-state hashes after both exit.

For formal behavioral comparisons, freeze the workload with `evals/LOCAL_EVAL_FIXTURE_TEMPLATE.md` and validate sanitized JSON against `evals/behavioral-result.schema.json`.

Never commit credentials, complete rollout JSONL, private transcripts, raw environment dumps, hidden reasoning, or unrelated local paths.

# Feedback protocol for continued adversarial review

`gpt56-sol-pro-consult` is the required adversarial consultation mechanism for this validation cycle. It is independent of the four Agent roles being tested and must not be counted as evidence that `codex-agent-team` itself routed correctly.

At Review Checkpoints A-E, and immediately after any P0/P1 candidate, Codex must invoke `gpt56-sol-pro-consult` and pass a compact evidence packet. Codex remains the local executor and must reconcile the consultation with repository/runtime evidence rather than blindly applying advice.

Use:

```text
CONTEXT_PACKET_V1

TASK: codex-agent-team local validation checkpoint
BASELINE_SHA: <current origin/main>
LOCAL_SHA: <current local validation commit if different>
RUNTIME: <Codex / ChatGPT build>
PLATFORM: <macOS / Apple Silicon>
CHECKPOINT: <A | B | C | D | E | defect | release-candidate>

COMPLETED_HEADOFF_ITEMS:
- <exact checkbox names or section numbers>

NEW_EVIDENCE:
- <fact + reproducible command/prompt/artifact>

DEFECTS:
- <id, severity candidate, ownership candidate, minimal reproduction>

TESTS:
- <focused result>
- <full-suite result if code changed>

CHANGES:
- <files changed, or NONE>

UNRESOLVED:
- <smallest remaining questions>

LOCAL_JUDGMENT:
- <continue | patch candidate | HOLD reason | RELEASE CANDIDATE candidate>

ASK:
Use gpt56-sol-pro-consult to adversarially review this evidence. Challenge severity and ownership, identify the strongest counterexample, and state whether the next HEADOFF checkpoint may proceed without a code or policy change.
```

For Checkpoint E multi-session evidence, include both main-session identifiers, canonical workspace identities, observed overlap, and whether either session knew about the other. For Checkpoint 6 installer concurrency evidence, include both process outcomes and the final shared Codex-home state.

When a project-side defect is reproducible, stop the experiment, create the smallest focused regression and patch, run focused plus complete tests, update `LOCAL_VALIDATION_REPORT.md`, then send the defect packet before expanding scope.

# Completion condition

The local handoff has a finite end state:

```text
RELEASE CANDIDATE
Mandatory live gates are characterized, no open PROJECT P0/P1 remains,
and the v1 Definition of Done is satisfied enough to enter feature freeze.

HOLD
A reproducible PROJECT P0/P1 or uncharacterized runtime limitation blocks a core invariant.

v1.0.0 RELEASED
The fixed RC closure pass is green, version 1.0.0 is merged/tagged/released,
and remaining P2/P3 work has moved to the post-v1 backlog.
```

Until the release gate is met, use `HOLD FOR RELEASE / VALIDATION INCOMPLETE`. Once the Definition of Done is met, the project must transition to the v1.0.0 release plan rather than reopening completed architecture work.
