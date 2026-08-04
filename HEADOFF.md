# Codex Delegate Local Runtime Validation Handoff

This is the authoritative finite live-validation and v1.0.0 release checklist for Codex Delegate.

The v0.6.0 architecture cycle, engineering consolidation, policy reduction, dead-surface sweep, release README, Plugin branding, and public-identity migration are statically complete. The remaining job is finite: validate the accepted behavior on a current real Codex runtime, fix only evidence-backed release blockers, run one fixed RC closure pass, and release v1.0.0.

## Current checkpoint

Accepted v0.6.0 static product baseline:

```text
product: Codex Delegate
public repository: R-jed/codex-delegate
marketplace id: codex-delegate
Plugin id: codex-delegate
command: /codex-delegate
version: 0.6.0
architecture: Adaptive Dependency Orchestration + evidence-gated recovery + risk-triggered Final Review Gate
known open reproducible PROJECT P0/P1: none
static posture: COMPLETE / ARCHITECTURE FROZEN AT v0.6.0
release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
```

The public package identity is `codex-delegate`. Internal managed role/profile ownership identifiers remain `codex_agent_team_*`, `codex-agent-team-*.toml`, and `.codex-agent-team-agents.json` for compatibility. Do not rename those internal compatibility identifiers without a separately proven migration need.

Before any live checkpoint, fetch `origin/main`, record the actual tested SHA in `LOCAL_VALIDATION_REPORT.md`, and invalidate only evidence whose declared dependencies changed.

## Stop line

Do not change these accepted rules merely to make a live test pass:

- no fixed Agent count and no mandatory Luna -> Terra -> Sol pipeline;
- the main session remains the task-level control plane;
- completion-driven ready-frontier scheduling is preferred when native completion/update events allow it;
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

## Checkpoint 1: exact roles and Runtime Evidence

Test independently:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

Expected tuples come from `plugins/codex-delegate/policy-contract.json` and must match shipped profile bytes.

Record only runtime-exposed facts: thread id, parent id, role, model, effort, sandbox/permission type, runtime/build version.

Use:

```bash
python plugins/codex-delegate/scripts/runtime-evidence.py --input <case.json>
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

Do not introduce a project rollout-file scraper to manufacture evidence.

### Review Checkpoint A

Send sanitized evidence to the required project consultation target below. Reviewer output is advisory `model_judgment` only.

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

### Dependency scheduling

- a running dependency does not receive duplicate inference;
- a satisfied dependency is reused until invalidated;
- independent ready dependencies can make useful progress concurrently;
- native slot shortage queues work rather than changing route identity.

### Completion-driven frontier refill

Use asymmetric durations:

```text
A = slow independent dependency
B = fast independent dependency
C = depends only on B
```

Start A and B concurrently. Record child identities and start/completion times. When native events and capacity allow:

```text
B completes
-> collect/verify B
-> close B
-> recompute ready frontier
-> C becomes ready
-> start C before A finishes
```

If C waits for A, record **barrier serialization** and determine whether policy or the native wait surface caused it.

Characterize the strongest actual wait surface:

```text
barrier_only
per_child_terminal
any_child_update
```

Record model-mediated polling and whether useful independent main-session work can continue while children run.

### Evidence reuse

Establish reusable deterministic/repository evidence, verify reuse, then change one dependency and confirm only affected evidence is invalidated.

### Intervention Gate and recovery

Exercise:

```text
Healthy incomplete case
False-progress case
same failure signature with no new evidence
hypothesis A -> B -> A
Capability gap
proposed recovery action remains separate from effective action
```

Characterize child-progress observability as `none`, `terminal_only`, `periodic_summary`, or `structured_live`. Do not infer a stronger level than exposed.

### Review Checkpoint C

Use the required consultation target to distinguish project defects from native-runtime boundaries.

## Checkpoint 4: product-value and Final Review experiments

Run controlled pairs with workload, revision, runtime, route, permissions, tool surface, and acceptance rubric held fixed.

Contract value:

```text
raw prompt -> Luna
vs
compiled bounded contract -> Luna
```

Terra delta value:

```text
whole-task stronger restart
vs
Terra receives unresolved delta + valid evidence + current artifact + DO NOT REDO
```

Required Final Review lifecycle:

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

### Review Checkpoint D

Send controlled results to the required consultation target. Do not turn one benchmark into a permanent architecture constant.

## Checkpoint 5: adaptive resources, consent, multi-session safety, and lifecycle

Adaptive fan-out:

```text
F1 explicit /codex-delegate -> up to 2 concurrently active justified children without another prompt
F2 >2 ready children without broad authorization -> ask consent or use smaller frontier
F3 larger fan-out authorized -> runtime capacity determines actual concurrency
F4 >=5 authorized independent read-only dependencies -> no product hard 4 ceiling
```

Record observed native capacity, runtime slot waits, peak active children, refill/recovery behavior, and duplicate calls.

Multi-session workspace matrix:

```text
M1 different sessions, different projects/checkouts
M2 different sessions, same repository, isolated worktrees
M3 different sessions, same canonical physical checkout
M4 one writing session + one read-only session same checkout
```

Do not implement a workspace lock before M3 establishes a reproducible failure.

### Review Checkpoint E

Send resource/multi-session evidence to the required consultation target. Any P0/P1 candidate gets immediate adversarial review.

## Checkpoint 6: official Plugin install, public-ID migration, and installer concurrency

Run the then-current official `plugin-creator/scripts/validate_plugin.py` against `plugins/codex-delegate` and record its source revision.

Fresh current install:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Current update/reinstall:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Then start a new Codex thread, confirm `/codex-delegate`, Plugin metadata, brand assets, profile-consent flow, and exact role discovery. While version remains `0.6.0`, verify that `marketplace upgrade` followed by explicit `plugin add` refreshes the installed Plugin bytes; otherwise bump patch version before RC.

Legacy public-ID migration must be tested from a real representative `codex-agent-team` installation because Codex marketplace upgrade requires the configured marketplace name to match the upgraded manifest name:

```bash
codex plugin remove codex-agent-team@codex-agent-team
codex plugin marketplace remove codex-agent-team
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Verify that existing exact managed `codex_agent_team_*` profiles and `.codex-agent-team-agents.json` remain safely reusable, while user-modified or unproven legacy files are never deleted or overwritten.

Installer concurrency:

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 two different managed profile generations compete in one CODEX_HOME
```

Record final disk state and peer-success preservation. Do not add an inter-process installer lock merely because a race is theoretical; require a reproducible invariant failure first.

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
2. real marketplace install/upgrade, legacy public-ID migration, and fresh-thread discovery pass;
3. managed profile installation/migration is safe on supported paths;
4. exact required role routing is acceptable on the tested runtime or limitations are bounded;
5. depth-one and permission evidence behavior has no open P0/P1;
6. contractability and scope simulations pass;
7. completion-driven scheduling/evidence reuse/intervention/recovery have no open P0/P1;
8. adaptive resource/consent behavior has no open P0/P1;
9. same-checkout multi-session writer safety has no open P0/P1;
10. required Final Review Gate lifecycle has no open P0/P1;
11. concurrent installer behavior has no open P0/P1;
12. required live behavioral experiments are recorded without unsupported quality/cost claims.

When items 1-12 are satisfied, the required action is **release v1.0.0**. Remaining P2/P3 work moves post-v1.

## Stage R1

Complete Checkpoints 1-6 and close all P0/P1.

## Stage R2

Feature freeze. Only release-blocking fixes, evidence reconciliation, and required documentation changes.

## Stage R3

Create one fixed RC tree and run the complete static matrix, current official validator, install/upgrade/migration smoke, profile lifecycle, and bounded representative runtime smoke.

## Stage R4

Finalize release metadata, tag `v1.0.0`, publish GitHub Release, and record released revision/runtime evidence. Do not reopen optional architecture tuning.

# Required validation artifact

Keep `LOCAL_VALIDATION_REPORT.md` current. Static evidence never substitutes for live runtime evidence.

# Feedback protocol for continued adversarial review

`/gpt56-sol-pro-consult` is required at Review Checkpoints A-E, immediately after any P0/P1 candidate, and for bounded project discussion requiring consequential judgment.

Codex remains the local executor. Consultation returns `model_judgment` and must not be counted as evidence that Codex Delegate itself routed correctly.

## Project consultation target

```text
TARGET_CHATGPT_CONVERSATION_TITLE: 分支 · 分支 · 项目对比分析
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
```

Resolution rules:

- do not fuzzy match;
- do not choose by recency;
- do not create a replacement ChatGPT conversation;
- do not silently fall back to an isolated consultation conversation;
- if exact unique resolution fails, return `CONSULTATION_TARGET_UNRESOLVED`.

The target contract does not replace any transport-level `task_id`, sentinel, safety scan, or evidence sanitization requirement.
