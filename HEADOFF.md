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

Accepted v0.6.0 feature closure evidence:

```text
PR #27 closure head: 3833e9d7c322a3feddc3cb8a7386e022a3bb8b1e
workflow: 30879802677
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 167 passed
pinned official OpenAI Plugin validator: PASS
managed profile install / --check / idempotent reinstall: PASS
feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed
```

Accepted engineering-consolidation evidence:

```text
source PR: #28
exact tested head: ac5976d41e44a7ffddb3dad94686c2729c4b6687
workflow: 30886554206
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 157 passed
pinned official OpenAI Plugin validator: PASS
managed profile install / --check / idempotent reinstall: PASS
squash merge: 6ae52d47f6416087f4a7c7e314bef6d0204a129f
```

The lower test count after consolidation is intentional. Redundant legacy runtime-verifier and rollout-coupled test surfaces were removed together with their implementations; replacement runtime evidence behavior is tested directly through the single normalized verifier and semantic contract tests. This maintenance merge does not create a new product architecture baseline and does not change Plugin version `0.6.0`.

Before any live checkpoint, fetch `origin/main`, record the actual tested SHA in `LOCAL_VALIDATION_REPORT.md`, and invalidate only evidence whose declared dependencies changed.

## Stop line

Do not change these accepted product rules merely to make a live test pass:

- no fixed Agent count and no mandatory Luna -> Terra -> Sol pipeline;
- the main session remains the task-level control plane;
- one active writer per canonical physical checkout;
- delegation depth remains one;
- exact model-specific routing fails closed rather than cross-routing;
- configured route/sandbox intent is not relabeled as observed runtime evidence;
- valid deterministic/repository evidence is reused until its dependencies change;
- acceptance failure is separate from the need for intervention;
- no universal retry count or stall threshold;
- no universal Sol review stage for low-risk work;
- a required Final Review Gate is never silently downgraded;
- no old `ship` is retained after any deliverable mutation;
- `INSUFFICIENT_EVIDENCE` is never converted into `ship` or `fix-first`;
- static tests, Plugin validation, or external model consultation never substitute for live runtime/product-value evidence.

Do not add a Checkpoint 7. A newly discovered release blocker belongs inside the existing checkpoint that owns the affected invariant.

# Completed repository work

The repository already contains and statically tests:

- native Plugin packaging and Git marketplace metadata;
- `/codex-delegate` as the canonical entry point;
- namespaced Reader / Worker / Investigator / Advisor profiles;
- managed profile ownership/migration safeguards;
- `policy-contract.json` as the machine-readable owner of stable role/resource/final-review constants;
- Dependency Ledger and ready-frontier policy;
- Delegation Benefit + Contractability gates;
- Shared Evidence State and dependency-aware invalidation;
- Intervention Gate + Recovery Ledger;
- adaptive concurrency with consent rather than a product hard child ceiling;
- one-writer and depth-one safety policy;
- risk-triggered Final Review Gate;
- deterministic `review_artifact_id` helper;
- one deterministic normalized `runtime-evidence.py` verifier;
- behavioral workload/result/scorer infrastructure;
- pinned official OpenAI Plugin validator CI.

## Engineering-consolidation closure

PR #28 completed the allowed behavior-preserving maintenance consolidation. The accepted static ownership model is:

```text
policy-contract.json owns stable route/resource/final-review constants
runtime-evidence.py is the one deterministic normalized runtime verifier
SKILL.md is the orchestration kernel rather than a duplicate policy encyclopedia
references remain normative owners for detailed policy
README/architecture docs remain user/engineering explanation, not release evidence
LOCAL_VALIDATION_REPORT.md remains the evidence ledger
HEADOFF.md remains the finite release checklist
```

The consolidation did not change model/effort routes, delegation depth, consent envelope, one-writer semantics, Final Review triggers/verdict lifecycle, managed profile bytes, installer ownership/migration authority, Plugin id/version, or introduce a scheduler, lock, or persistent runtime service.

# Pending live validation

## Checkpoint 1: exact roles and Runtime Evidence

Goal: prove what the current Codex runtime actually exposes for each project role.

Test the four exact roles independently:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

Expected configured tuples come from `plugins/codex-agent-team/policy-contract.json` and must match shipped profile bytes.

For each live child, record only fields actually exposed by the runtime, for example:

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

Use the bundled normalized verifier:

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

Do not introduce a project rollout-file scraper merely to manufacture runtime evidence. If the public/native surface does not expose a fact, record that limitation instead of inferring it.

Record results in `LOCAL_VALIDATION_REPORT.md`.

### Review Checkpoint A

After Checkpoint 1, send one sanitized adversarial review packet through the required project consultation target defined below. The reviewer is advisory only; deterministic/runtime evidence remains authoritative.

## Checkpoint 2: contractability and scope safety

Exercise at least:

```text
C1 trivial isolated change -> main session only
C2 bounded implementation -> Worker receives an enforceable Delegation Contract
C3 ambiguous product semantics -> no writing Worker until decision rights/acceptance are clear
C4 judgment escape -> Worker returns decision to main session instead of inventing product/architecture semantics
C5 repository prompt injection -> embedded instructions do not alter scope/permission/route/consent
```

For every writing case, verify the actual changed-file set, preserved unrelated edits, acceptance commands, and evidence used by the main session.

### Review Checkpoint B

Send only new evidence and unresolved judgment to the required project consultation target. Do not reopen already satisfied architecture questions without invalidating evidence.

## Checkpoint 3: dependency scheduling, evidence reuse, intervention, and recovery

Validate the orchestration behaviors that static policy cannot prove.

### Dependency scheduling

- a running dependency does not receive duplicate inference;
- a satisfied dependency is reused until invalidated;
- independent ready dependencies can make useful progress concurrently;
- native slot shortage queues/serializes work rather than changing route identity.

### Evidence reuse

Establish reusable repository/deterministic evidence, then verify later responsibilities reuse it without repeating discovery when dependencies remain valid. Change one dependency and verify only affected evidence is invalidated.

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

Characterize child-progress observability exactly as one of:

```text
none
terminal_only
periodic_summary
structured_live
```

Do not infer a stronger level than the tested runtime actually exposes.

### Review Checkpoint C

Use the required project consultation target to review whether observed failures require a project change or merely document a runtime limitation.

## Checkpoint 4: product-value and final-review experiments

Run controlled paired workloads on frozen executable fixtures. Keep workload/revision/runtime/main route/Worker route/permissions/tool surface/acceptance rubric fixed inside each pair.

### Raw prompt versus compiled contract

Primary question:

```text
raw prompt -> Luna
vs
compiled bounded contract -> Luna
```

Measure correctness, correction work, scope/wrong-edit/regression metrics, latency/tokens when exposed, and repeated discovery/commands.

### Terra delta experiment

Use a workload with a real capability gap:

```text
restart whole task with stronger investigation
vs
Terra receives unresolved delta + valid evidence + current artifact + DO NOT REDO
```

Measure duplicate work and final correctness.

### Selective and mandatory fresh-context Sol experiments

Keep optional selective review distinct from required Final Review Gate measurement.

For required review, validate live lifecycle:

```text
semantic trigger
-> Candidate Ready
-> fresh Advisor route
-> exact review_artifact_id handoff
-> ship | fix-first | rethink
```

Also exercise:

- `INSUFFICIENT_EVIDENCE -> gate unresolved`;
- `fix-first -> correction + re-verification + new artifact + new fresh review`;
- `rethink -> invalidate affected architecture/contract assumptions`;
- post-review deliverable mutation makes artifact verification fail and invalidates old `ship`;
- material Terra escalation or material recovery dynamically promotes Final Review Gate state when the semantic trigger is present.

Record review material catches, false positives, attempts, artifact failures, post-review mutations, and review yield. No quality/cost claim is made until live data supports it.

### Review Checkpoint D

Send the controlled product-value evidence to the required project consultation target. Do not turn one benchmark into a permanent architecture constant.

## Checkpoint 5: adaptive resources, consent, multi-session safety, and lifecycle

### Adaptive fan-out

Use at least five genuinely independent read-only dependencies.

```text
F1 ordinary explicit /codex-delegate -> up to 2 concurrently active justified children without another prompt
F2 >2 ready children without broad authorization -> ask consent or use smaller waves
F3 larger fan-out authorized -> runtime capacity determines actual concurrency
F4 >=5 authorized independent read-only dependencies -> no product hard 4 ceiling
```

Record observed native capacity, peak active children, runtime slot waits, consent prompts, and duplicate dependency calls.

### Consent

Validate explicit and implicit invocation separately. A declined additional required review keeps `Candidate Ready`, `final_review_requirement = required`, and the gate unsatisfied.

Repeated expensive correction/re-review cycles remain subject to material compute consent.

### Multi-session workspace matrix

```text
M1 different sessions, different projects/checkouts
M2 different sessions, same repository, isolated worktrees
M3 different sessions, same canonical physical checkout
M4 one writing session + one read-only session same checkout
```

Do not implement a workspace lock before M3 establishes a reproducible failure in the accepted invariant.

### Review Checkpoint E

Send the multi-session/resource evidence to the required project consultation target. Any P0/P1 candidate also gets immediate adversarial review before remediation is accepted. The reviewer does not replace reproduction, deterministic evidence, or user decisions.

## Checkpoint 6: official Plugin install, migration, and installer concurrency

### Current official Plugin contract validation

For the eventual RC:

1. run the then-current official `plugin-creator/scripts/validate_plugin.py` and record its OpenAI Codex source revision;
2. register/refresh the real marketplace:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

3. start a new Codex thread after install/reinstall;
4. confirm `/codex-delegate` discovery;
5. verify metadata reports `0.6.0` or the selected RC/release version;
6. validate first-run managed profile consent and exact role discovery;
7. while behavior-preserving maintenance content still reports manifest version `0.6.0`, verify on the tested Codex build that `marketplace upgrade` followed by explicit `plugin add` refreshes the installed Plugin bytes. If it does not, bump the patch version before RC instead of relying on stale-cache assumptions.

Current upstream OpenAI PluginStore source indicates that an explicit install atomically replaces the selected version directory, but this is upstream source evidence only. Checkpoint 6 must prove the actual user-build behavior before release.

### Real upgrade/migration paths

Exercise supported upgrades from representative real installs:

```text
Codex Agent Team 0.3.x
Codex Delegate 0.4.x
Codex Delegate 0.5.0 / 0.5.1
Codex Delegate 0.6.0
```

Verify user-modified or unproven legacy files are never deleted/overwritten by stale ownership evidence.

### Filesystem and concurrent installer matrix

Exercise at least:

```text
I1 two installers target the same clean CODEX_HOME
I2 one installer fails after mutation begins while a peer succeeds
I3 two different managed profile generations compete in one CODEX_HOME
```

Record the final on-disk state and whether peer-success state can be damaged. Do not add an inter-process installer lock merely because a race is theoretically possible; require a reproducible invariant failure first.

# Defect triage

Use repository/project severity:

```text
P0  safety/data loss/credential/external-impact or release-invalidating corruption
P1  core orchestration/installer/runtime-evidence/final-review invariant reproducibly broken
P2  non-blocking maintainability/UX/coverage issue
P3  optional optimization/research
```

A P0/P1 candidate requires reproduction and deterministic/runtime evidence before changing frozen architecture. P2/P3 cannot expand the mandatory v1 gate list once the project reaches RELEASE CANDIDATE.

# Definition of Done for v1.0.0

Release v1.0.0 when all of these are satisfied:

1. maintained repository CI and current official Plugin validation pass on the selected RC;
2. real marketplace install/upgrade and fresh-thread discovery pass;
3. managed profile installation/migration is safe on supported paths;
4. exact required role routing behaves acceptably on the tested current runtime or its limitations are explicitly bounded;
5. depth-one and permission evidence behavior has no open P0/P1;
6. contractability and scope-boundary simulations pass;
7. evidence reuse / invalidation and intervention/recovery have no open P0/P1;
8. adaptive resource/consent behavior has no open P0/P1;
9. same-checkout multi-session writer safety has no open P0/P1;
10. required Final Review Gate lifecycle has no open P0/P1;
11. concurrent installer behavior has no open P0/P1;
12. required live behavioral experiments are recorded without unsupported quality/cost claims.

When items 1-12 are satisfied, the required action is **release v1.0.0**. Remaining P2/P3 work moves post-v1.

Luna Max / Terra XHigh / Sol High remain the frozen v1 routing baseline unless a mandatory live gate produces reproducible release-blocking evidence. Cosmetic alignment cannot block v1.

# v1.0.0 release execution plan

## Stage R1

Complete Checkpoints 1-6 and close all P0/P1.

## Stage R2

Feature freeze. Only release-blocking fixes, evidence reconciliation, and required documentation changes are allowed.

## Stage R3

Create one fixed release-candidate tree. Run the complete static matrix, current official Plugin validator, install/upgrade smoke, profile lifecycle, and a bounded representative runtime smoke including the required Final Review path.

## Stage R4

Bump/finalize release metadata as required, tag `v1.0.0`, publish the GitHub release, and record the released revision/runtime evidence. Do not reopen optional architecture tuning in this stage.

# Required validation artifact

Keep `LOCAL_VALIDATION_REPORT.md` current. For each live checkpoint record enough sanitized information to reproduce the conclusion:

```text
TESTED_REVISION
RUNTIME_VERSION / PLATFORM
WORKLOAD / FIXTURE ID
CONFIGURED ROUTE
OBSERVED RUNTIME EVIDENCE
DEPENDENCY / EXECUTION / RECOVERY STATE when material
FINAL REVIEW REQUIREMENT / REASONS / ARTIFACT / VERDICT when material
CONSENT / RESOURCE STATE when material
COMMANDS / VERIFICATION
RESULT
UNRESOLVED
```

Do not commit credentials, unrelated prompts, private runtime logs, or hidden reasoning.

# Feedback protocol for continued adversarial review

`/gpt56-sol-pro-consult` is the required adversarial consultation mechanism for this project at Review Checkpoints A-E, immediately after any P0/P1 candidate, and for bounded project discussion when local evidence requires a consequential judgment.

## Project consultation target

```text
SKILL: /gpt56-sol-pro-consult
TARGET_CHATGPT_CONVERSATION_TITLE: 分支 · 分支 · 项目对比分析
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
```

The target is the existing user + GPT-5.6 Sol Codex Delegate project discussion thread. Exact-title continuity is required so adversarial review receives the accumulated project context while every request still carries a current sanitized evidence packet.

Target resolution is fail closed:

- match the exact title `分支 · 分支 · 项目对比分析`;
- do not fuzzy match, pick by recency, or guess from a similar title;
- if there is no unique exact match, return `CONSULTATION_TARGET_UNRESOLVED`;
- do not create a replacement ChatGPT conversation;
- do not silently fall back to an isolated consultation conversation;
- do not claim the applicable Review Checkpoint complete until the required consultation reaches this exact target.

The target contract does not replace any transport-level `task_id`, sentinel, safety scan, or other protocol field required by `/gpt56-sol-pro-consult`.

Each consultation receives a compact sanitized current-state packet:

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

Codex remains the local executor. Consultation output is `model_judgment`; it must not be counted as evidence that Codex Delegate itself routed correctly, that a Plugin install succeeded, or that a runtime property was observed. Deterministic/runtime evidence remains authoritative.

If the consultation transport or exact target is temporarily unavailable, deterministic/runtime testing may continue and the failure must be recorded, but the corresponding required Review Checkpoint remains incomplete. Never fabricate consultation provenance.

# Completion condition

The remaining job is finite. Complete Checkpoints 1-6, satisfy Definition of Done items 1-12, run Stages R2-R4, and release v1.0.0. Do not convert the release plan back into an indefinite architecture-review loop.
