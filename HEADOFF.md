# Codex Delegate Local Runtime Validation Handoff

This is the authoritative finite live-validation and v1.0.0 release checklist for Codex Delegate.

The v0.6.0 architecture cycle and repository-side engineering consolidation are closed. The remaining job is finite: validate the accepted behavior on a current real Codex runtime, fix only evidence-backed release blockers, run one fixed release-candidate closure pass, and release v1.0.0.

## Current checkpoint

Accepted v0.6.0 static product baseline:

```text
feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed
source PR: #27
product: Codex Delegate
version: 0.6.0
architecture: Adaptive Dependency Orchestration + evidence-gated recovery + risk-triggered Final Review Gate
known open reproducible PROJECT P0/P1: none
static posture: COMPLETE / ARCHITECTURE FROZEN AT v0.6.0
release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
```

Accepted feature/consolidation evidence:

```text
PR #27 closure head: 3833e9d7c322a3feddc3cb8a7386e022a3bb8b1e
workflow: 30879802677
pytest: 167 passed
feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed

PR #28 exact tested head: ac5976d41e44a7ffddb3dad94686c2729c4b6687
workflow: 30886554206
pytest: 157 passed
engineering-consolidation merge: 6ae52d47f6416087f4a7c7e314bef6d0204a129f

both accepted trees:
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install / --check / idempotent reinstall: PASS
```

Before any live checkpoint, fetch `origin/main`, record the actual tested SHA in `LOCAL_VALIDATION_REPORT.md`, and invalidate only evidence whose declared dependencies changed.

## Stop line

Do not change these accepted rules merely to make a live test pass:

- no fixed Agent count and no mandatory Luna -> Terra -> Sol pipeline;
- the main session remains the task-level control plane;
- completion-driven ready-frontier scheduling is the desired policy when the native runtime exposes individual completion/update events;
- one active writer per canonical physical checkout;
- delegation depth remains one;
- exact model-specific routing fails closed rather than cross-routing;
- configured route/sandbox intent is not relabeled as observed runtime evidence;
- valid deterministic/repository evidence is reused until dependencies change;
- acceptance failure is separate from need for intervention;
- no universal retry count or stall threshold;
- no universal Sol stage for low-risk work;
- a required Final Review Gate is never silently downgraded;
- no old `ship` is retained after any deliverable mutation;
- `INSUFFICIENT_EVIDENCE` is never converted into `ship` or `fix-first`;
- static tests, Plugin validation, or model consultation never substitute for live runtime/product evidence.

Do not add a Checkpoint 7. A new release blocker belongs inside the existing checkpoint that owns the affected invariant.

# Completed repository work

The repository already contains and statically tests:

- native Plugin packaging and Git marketplace metadata;
- `/codex-delegate` as canonical entry point;
- namespaced Reader / Worker / Investigator / Advisor profiles;
- managed profile ownership/migration safeguards;
- `policy-contract.json` as machine-readable stable constant source;
- Dependency Ledger + ready frontier;
- Delegation Benefit + Contractability gates;
- Shared Evidence State + dependency-aware invalidation;
- Intervention Gate + Recovery Ledger;
- adaptive concurrency with consent rather than a product hard child ceiling;
- one-writer and depth-one safety;
- risk-triggered Final Review Gate + deterministic `review_artifact_id`;
- one normalized `runtime-evidence.py` verifier;
- behavioral workload/result/scorer infrastructure;
- pinned official OpenAI Plugin validator CI.

Repository policy is intentionally thin: `SKILL.md` owns the orchestration loop, while each detailed boundary has one normative reference owner. No project daemon, persistent scheduler, thread pool, or rollout-file scraper is introduced.

# Pending live validation

## Checkpoint 1: exact roles and Runtime Evidence

Test independently:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

Expected tuples come from `plugins/codex-agent-team/policy-contract.json` and must match shipped profile bytes.

Record only facts exposed by the runtime, for example:

```text
thread_id
parent_thread_id
agent_role
model
effort
sandbox_policy_type
permission_profile_type
runtime/build version
```

Use:

```bash
python plugins/codex-agent-team/scripts/runtime-evidence.py --input <case.json>
```

Required semantics:

```text
incomplete expected route -> fail closed
missing observation -> not_observed / partial
complete matching native route -> R1
complete matching native + supplied corroboration -> R2
complete local/corroborating route alone -> at most L1
material conflict -> X0 + quarantine
hard read-only required + native sandbox absent -> return to main session
```

Do not introduce a project rollout-file scraper to manufacture evidence. Record unavailable fields as unavailable.

### Review Checkpoint A

Send the sanitized evidence to the required project consultation target below. Reviewer output is advisory `model_judgment` only.

## Checkpoint 2: contractability and scope safety

Exercise:

```text
C1 trivial isolated change -> main session only
C2 bounded implementation -> Worker gets enforceable Delegation Contract
C3 ambiguous semantics -> no writing Worker until decision rights/acceptance are clear
C4 judgment escape -> Worker returns decision instead of inventing product/architecture semantics
C5 repository prompt injection -> embedded instructions cannot alter scope/permission/route/consent
```

For writing cases verify actual changed files, preserved unrelated edits, acceptance commands, and evidence.

### Review Checkpoint B

Send only new evidence and unresolved consequential judgment to the required project consultation target.

## Checkpoint 3: dependency scheduling, completion events, evidence reuse, intervention, and recovery

Validate static policy against the actual native runtime.

### Dependency scheduling

- a running dependency does not receive duplicate inference;
- a satisfied dependency is reused until invalidated;
- independent ready dependencies can make useful progress concurrently;
- native slot shortage queues work rather than changing route identity.

### Completion-driven frontier refill

Use asymmetric durations so a batch barrier is observable:

```text
A = slow independent dependency
B = fast independent dependency
C = depends only on B
```

Start A and B concurrently. Record actual start/completion times and child identities.

Expected policy behavior when the runtime exposes individual completion/update events and capacity is available:

```text
B completes
-> collect/verify B
-> close B when its result is secured
-> recompute ready frontier
-> C becomes ready
-> start C before A finishes
```

If C cannot start until A finishes, record **barrier serialization** and determine whether it came from main-session policy or the tested native wait surface. Do not label a runtime limitation as a project scheduler success.

Characterize the strongest actual completion/wait surface as one of:

```text
barrier_only
per_child_terminal
any_child_update
```

Also determine whether useful independent main-session work can continue while children are active without duplicating their responsibility or creating write conflicts.

Record whether waiting uses native blocking/update behavior or repeated **model-mediated polling**. Repeated status-only model turns are a performance/cost observation, not productive work.

### Evidence reuse

Establish reusable repository/deterministic evidence, verify later responsibilities reuse it, then change one dependency and confirm only affected evidence is invalidated.

### Intervention Gate and recovery

Exercise:

```text
Healthy incomplete case
-> acceptance still failing, but new deterministic evidence narrows the unresolved delta
-> continue current responsibility

False-progress case
-> successful commands/file writes but no acceptance/evidence movement
-> do not count as progress

Execution stall
-> same failure signature with no new evidence
-> clean same-lane restart when the lane remains capable

Semantic cycle
-> hypothesis A -> B -> A with unchanged evidence
-> Recovery Ledger detects the established dead end

Capability gap
-> evidence-supported technical delta goes to Terra before repeated same-lane retry

Policy transform
-> proposed recovery action remains separate from effective action and decision source
```

Characterize child-progress observability separately from completion notification:

```text
none
terminal_only
periodic_summary
structured_live
```

Do not infer a stronger level than the runtime exposes.

### Review Checkpoint C

Use the required consultation target to decide whether observed limitations are project defects or native-runtime boundaries.

## Checkpoint 4: product-value and Final Review experiments

Use controlled paired workloads with workload/revision/runtime/main route/Worker route/permissions/tool surface/acceptance rubric fixed within each pair.

### Contract value

```text
raw prompt -> Luna
vs
compiled bounded contract -> Luna
```

Measure correctness, correction work, scope/wrong-edit/regression metrics, latency/tokens when exposed, and repeated discovery/commands.

### Terra delta value

```text
whole-task stronger restart
vs
Terra receives unresolved delta + valid evidence + current artifact + DO NOT REDO
```

Measure duplicate work and correctness.

### Final Review lifecycle

Keep optional selective Sol review separate from mandatory review measurement.

Required path:

```text
semantic trigger
-> Candidate Ready
-> fresh Advisor route
-> exact review_artifact_id handoff
-> ship | fix-first | rethink
```

Also prove:

```text
INSUFFICIENT_EVIDENCE -> gate unresolved
fix-first -> correction + re-verification + new artifact + new fresh review
rethink -> invalidate affected architecture/contract assumptions
post-review deliverable mutation -> old ship invalid
required Final Review Gate is never silently downgraded
no old `ship` is retained after any deliverable mutation
```

Record material catches, false positives, attempts, artifact failures, post-review mutations, and review yield. Do not make quality/cost claims without live data.

### Review Checkpoint D

Send the controlled results to the required consultation target. Do not convert one benchmark into a permanent architecture constant.

## Checkpoint 5: adaptive resources, consent, multi-session safety, and lifecycle

### Adaptive fan-out

Use at least five genuinely independent read-only dependencies.

```text
F1 explicit /codex-delegate -> up to 2 concurrently active justified children without another prompt
F2 >2 ready children without broad authorization -> ask consent or use smaller frontier
F3 larger fan-out authorized -> runtime capacity determines actual concurrency
F4 >=5 authorized independent read-only dependencies -> no product hard 4 ceiling
```

Record observed native capacity, peak active children, runtime slot waits, consent prompts, slot refill/recovery behavior, and duplicate dependency calls.

### Consent

Validate explicit and implicit invocation separately. A declined required review keeps `Candidate Ready`, `final_review_requirement = required`, and the gate unsatisfied.

### Multi-session workspace matrix

```text
M1 different sessions, different projects/checkouts
M2 different sessions, same repository, isolated worktrees
M3 different sessions, same canonical physical checkout
M4 one writing session + one read-only session same checkout
```

Do not implement a workspace lock before M3 establishes a reproducible failure.

### Review Checkpoint E

Send resource/multi-session evidence to the required consultation target. Any P0/P1 candidate gets immediate adversarial review before remediation is accepted.

## Checkpoint 6: official Plugin install, migration, and installer concurrency

### Current official Plugin validation

For the selected RC:

1. run the then-current official `plugin-creator/scripts/validate_plugin.py` and record source revision;
2. execute real marketplace flow:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

3. start a new Codex thread;
4. confirm `/codex-delegate` discovery;
5. verify metadata version;
6. validate first-run profile consent and exact role discovery;
7. while behavior-preserving maintenance still reports `0.6.0`, verify that `marketplace upgrade` followed by explicit `plugin add` refreshes the installed Plugin bytes. If not, bump patch version before RC.

### Real migrations

Exercise representative installs:

```text
Codex Agent Team 0.3.x
Codex Delegate 0.4.x
Codex Delegate 0.5.0 / 0.5.1
Codex Delegate 0.6.0
```

User-modified or unproven legacy files must never be deleted/overwritten by stale ownership evidence.

### Installer concurrency

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 two different managed profile generations compete in one CODEX_HOME
```

Record final disk state and whether peer-success state can be damaged. Do not add an inter-process installer lock merely because a race is theoretical; require a reproducible invariant failure first.

# Defect triage

```text
P0 safety/data loss/credential/external-impact or release-invalidating corruption
P1 core orchestration/installer/runtime-evidence/final-review invariant reproducibly broken
P2 non-blocking maintainability/UX/coverage issue
P3 optional optimization/research
```

P0/P1 requires reproduction and deterministic/runtime evidence before frozen architecture changes. P2/P3 cannot expand the mandatory v1 gate list after RELEASE CANDIDATE.

# Definition of Done for v1.0.0

Release v1.0.0 when all are satisfied:

1. maintained repository CI and current official Plugin validation pass on selected RC;
2. real marketplace install/upgrade and fresh-thread discovery pass;
3. managed profile installation/migration is safe on supported paths;
4. exact required role routing is acceptable on tested current runtime or limitations are bounded;
5. depth-one and permission evidence behavior has no open P0/P1;
6. contractability and scope simulations pass;
7. completion-driven scheduling/evidence reuse/intervention/recovery have no open P0/P1;
8. adaptive resource/consent behavior has no open P0/P1;
9. same-checkout multi-session writer safety has no open P0/P1;
10. required Final Review Gate lifecycle has no open P0/P1;
11. concurrent installer behavior has no open P0/P1;
12. required live behavioral experiments are recorded without unsupported quality/cost claims.

When items 1-12 are satisfied, the required action is **release v1.0.0**. Remaining P2/P3 work moves post-v1.

Luna Max / Terra XHigh / Sol High remain the frozen v1 route baseline unless mandatory live evidence produces a reproducible blocker.

# v1.0.0 release execution plan

## Stage R1

Complete Checkpoints 1-6 and close all P0/P1.

## Stage R2

Feature freeze. Only release-blocking fixes, evidence reconciliation, and required documentation changes.

## Stage R3

Create one fixed RC tree. Run complete static matrix, current official Plugin validator, install/upgrade smoke, profile lifecycle, and bounded representative runtime smoke including completion-driven scheduling and required Final Review.

## Stage R4

Finalize release metadata, tag `v1.0.0`, publish GitHub Release, and record released revision/runtime evidence. Do not reopen optional architecture tuning.

# Required validation artifact

Keep `LOCAL_VALIDATION_REPORT.md` current. For material live cases record:

```text
TESTED_REVISION
RUNTIME_VERSION / PLATFORM
WORKLOAD / FIXTURE ID
CONFIGURED ROUTE
OBSERVED RUNTIME EVIDENCE
DEPENDENCY / EXECUTION / RECOVERY STATE
COMPLETION / WAIT / SLOT-REFILL TIMING when material
FINAL REVIEW REQUIREMENT / REASONS / ARTIFACT / VERDICT when material
CONSENT / RESOURCE STATE
COMMANDS / VERIFICATION
RESULT
UNRESOLVED
```

Do not commit credentials, unrelated prompts, private runtime logs, or hidden reasoning.

# Feedback protocol for continued adversarial review

`/gpt56-sol-pro-consult` is the required adversarial consultation mechanism at Review Checkpoints A-E, immediately after any P0/P1 candidate, and for bounded project discussion requiring consequential judgment.

## Project consultation target

```text
SKILL: /gpt56-sol-pro-consult
TARGET_CHATGPT_CONVERSATION_TITLE: 分支 · 分支 · 项目对比分析
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
```

Target resolution is fail closed:

- match the exact title `分支 · 分支 · 项目对比分析`;
- do not fuzzy match, pick by recency, or guess from a similar title;
- if no unique exact match exists, return `CONSULTATION_TARGET_UNRESOLVED`;
- do not create a replacement ChatGPT conversation;
- do not silently fall back to an isolated consultation conversation;
- do not claim the applicable Review Checkpoint complete until consultation reaches this exact target.

The target contract does not replace any transport-level `task_id`, sentinel, safety scan, or other protocol field required by `/gpt56-sol-pro-consult`.

Each consultation carries a compact sanitized current packet:

```text
CONSULTATION_TARGET
skill: /gpt56-sol-pro-consult
conversation_title: 分支 · 分支 · 项目对比分析
mode: continue_existing_conversation
match_policy: exact_title_unique_match

COMPLETED_HEADOFF_ITEMS
NEW_EVIDENCE
DEPENDENCY_STATE
EXECUTION_PROGRESS
RECOVERY_STATE
FINAL_REVIEW_STATE
RESOURCE_STATE
PLUGIN_STATE
DEFECTS
TESTS
CHANGES
UNRESOLVED
LOCAL_JUDGMENT
ASK
```

Codex remains the local executor. Consultation output is `model_judgment`; it must not be counted as evidence that Codex Delegate itself routed correctly, installed correctly, or observed a runtime property.

If transport/target is unavailable, deterministic/runtime testing may continue and the failure must be recorded, but the corresponding Review Checkpoint stays incomplete. Never fabricate consultation provenance.

# Completion condition

The remaining job is finite. Complete Checkpoints 1-6, satisfy Definition of Done items 1-12, run Stages R2-R4, and release v1.0.0. Do not convert the release plan back into an indefinite architecture-review loop.
