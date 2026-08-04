# Codex Delegate Local Validation Report

This is the evidence ledger for Codex Delegate. `HEADOFF.md` defines the remaining live/release gates. This report records what was actually established, on which repository/runtime baseline, and which claims remain unverified.

Repository policy, static CI, Plugin validation, upstream source inspection, and model judgment are not substitutes for live Codex runtime evidence.

## Current reconciliation

Reconciled: 2026-08-04.

```text
Product: Codex Delegate
Plugin version: 0.6.0
Canonical entry point: /codex-delegate
Repository/package compatibility namespace: R-jed/codex-agent-team / codex-agent-team
Accepted v0.6.0 feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed
Accepted engineering-consolidation merge: 6ae52d47f6416087f4a7c7e314bef6d0204a129f
Accepted completion-driven/policy-reduction merge: a086229a6fd8e64f502fc3574c0da931ffa8c929
Completion-driven source PR: #30
Exact tested completion-driven head: 148a5ab599578b0a4f0aafaa09e5007633388143
Completion-driven workflow: 30890469536
Release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
Static architecture posture: ARCHITECTURE FROZEN AT v0.6.0
Repository maintenance posture: ENGINEERING CONSOLIDATION + POLICY REDUCTION COMPLETE
Known open reproducible PROJECT P0/P1: none
```

PR #27 established the accepted v0.6.0 product behavior. PR #28 consolidated duplicated executable/policy machinery without changing that product baseline. PR #30 then finished the README/policy reduction and made the already intended adaptive scheduler explicitly completion-driven around the ready frontier, without adding a new runtime or changing frozen model/resource/final-review constants.

The remaining release work is the finite live-validation sequence in `HEADOFF.md`.

## Evidence classes

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Deterministic evidence**: reproducible test, validator, installer, verifier, digest, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Upstream source fact**: behavior established from a specific OpenAI Codex source revision or official documentation; version-sensitive until matched to a tested runtime when runtime behavior is involved.
- **Public issue telemetry**: user-reported evidence in an upstream issue; useful for risk discovery, never a product/runtime guarantee.
- **Model judgment**: advisory conclusion; never deterministic/runtime proof.
- **Carried forward**: older evidence whose dependencies have not materially changed.
- **Pending revalidation**: policy/tooling exists but the corresponding current runtime claim has not been demonstrated.

## Accepted v0.6.0 static evidence

The final PR #27 feature closure tree was:

```text
closure head: 3833e9d7c322a3feddc3cb8a7386e022a3bb8b1e
workflow: 30879802677
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 167 passed
pinned official OpenAI Plugin validator: PASS
managed profile install: PASS
managed profile --check: PASS
idempotent managed profile reinstall: PASS
```

That tree was squash-merged as `b043428223ba99ce77e2268c32cfa6a38daad3ed`.

These results establish repository/static consistency for the v0.6.0 feature tree. They do not establish current live Worker/Investigator/Advisor route identity, host-enforced read-only, child progress observability, cross-session writer exclusion, installer multi-process behavior, completion-driven native scheduling, or mandatory Final Review quality yield.

### Final Review Gate

The accepted v0.6.0 static contract establishes:

```text
low-risk candidate
-> main-session inspection + deterministic acceptance
-> review may remain not_required

semantic risk trigger
-> final_review_requirement = required
-> Candidate Ready
-> deterministic review_artifact_id
-> fresh codex_agent_team_advisor review
-> ship | fix-first | rethink
```

`INSUFFICIENT_EVIDENCE` remains a fail-closed unresolved reviewer outcome. It cannot be converted into `ship` or silently treated as `fix-first`.

The machine-readable behavioral schema includes `contract_luna_final_review_gate` plus review requirement/reasons/attempts/verdict/gate state/artifact verification failures/post-review mutation fields. Static workloads describe the expected lifecycle; they are not live benchmark results.

### Artifact identity

`plugins/codex-agent-team/scripts/review-artifact.py` is accepted deterministic tooling for binding a Git deliverable to a `review_artifact_id`.

It covers current `HEAD` when present, complete tracked working-tree diff, Git-relevant executable-mode changes, non-ignored untracked regular files/symlinks, unborn repositories, and double-sampled workspace state so mutation during identity capture fails closed.

Ignored/generated deliverables require an additional deterministic digest when they are part of the requested deliverable.

## Accepted engineering-consolidation static evidence

PR #28 reduced repository maintenance surface while preserving the v0.6.0 product contract.

```text
PR: #28
exact tested head: ac5976d41e44a7ffddb3dad94686c2729c4b6687
workflow: 30886554206
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 157 passed
Plugin/marketplace JSON validation: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install: PASS
managed profile --check: PASS
idempotent reinstall: PASS
squash merge: 6ae52d47f6416087f4a7c7e314bef6d0204a129f
```

The lower test count versus the feature closure is intentional. Redundant legacy runtime-verifier and rollout-coupled implementation/test surfaces were removed together. Replacement semantics are covered through the single normalized runtime evidence verifier and semantic policy tests.

Accepted maintenance ownership became:

```text
plugins/codex-agent-team/policy-contract.json
-> stable route/resource/final-review constants

plugins/codex-agent-team/scripts/runtime-evidence.py
-> normalized route/ancestry/permission evidence reconciliation

SKILL.md
-> orchestration kernel

reference documents
-> detailed normative policy

LOCAL_VALIDATION_REPORT.md
-> evidence ledger

HEADOFF.md
-> finite release checklist
```

The consolidation did not change Reader/Worker/Investigator/Advisor profile bytes or model/effort tuples, delegation depth, the baseline two-child no-extra-consent envelope, the one-writer rule, Final Review trigger/verdict semantics, installer ownership authority, Plugin package id/version, or the no-new-daemon/no-new-lock boundary.

### Normalized Runtime Evidence tool

The accepted verifier consumes normalized JSON with optional native/local observations and keeps:

```text
route_evidence
ancestry_evidence
permission_evidence
```

independent.

Compatibility grades remain:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

Incomplete expected role/model/effort fails input validation. Partial native route never becomes runtime proof. Local corroboration alone never establishes host-enforced read-only permission. When enforced read-only is required and native sandbox evidence is absent, the affected responsibility returns to the main session.

The project no longer manufactures missing runtime facts from private rollout internals. Missing runtime evidence remains missing/partial.

## Accepted completion-driven / policy-reduction static evidence

PR #30 completed the interrupted README and engineering-bloat cleanup while preserving the frozen v0.6.0 product constants.

Exact accepted test evidence:

```text
PR: #30
exact tested head: 148a5ab599578b0a4f0aafaa09e5007633388143
workflow: 30890469536
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 158 passed
Plugin/marketplace JSON validation: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install: PASS
managed profile --check: PASS
idempotent reinstall: PASS
squash merge: a086229a6fd8e64f502fc3574c0da931ffa8c929
```

Repository diff against its starting `main` baseline:

```text
19 changed files
+1234 / -1915
net: -681 lines
```

The net reduction is primarily in user/policy/documentation surface rather than executable capability deletion. Major reductions were:

```text
README.md                 -216 net lines
README_EN.md              -95
architecture.md           -80
native-subagent-runtime   -38
SKILL.md                  -33
delegation-contract.md    -124
routing-policy.md         -135
```

Tests were rewritten to validate the correct normative owner rather than requiring the same policy sentence to be copied into SKILL, routing, contract, safety, and runtime documents. Test-surface growth stayed small relative to removed duplicate prose.

The accepted ownership model is now:

```text
SKILL.md              -> orchestration loop + operational entry points
delegation-contract   -> responsibility contract + return packets
routing-policy        -> readiness + completion-driven dispatch + semantic routing
execution-progress    -> progress + Intervention Gate + recovery
safety-policy         -> trust + permission + workspace boundaries
consent-policy        -> resource authorization
runtime-assurance     -> observed route/ancestry/permission evidence
final-review-gate     -> mandatory artifact-bound review lifecycle
```

PR #30 also removed the stale policy reference to the deleted `verify-runtime.py`; the only shipped deterministic normalized Runtime Evidence executable remains `plugins/codex-agent-team/scripts/runtime-evidence.py`.

### Completion-driven scheduling contract

Static policy now says:

```text
dispatch useful safe work from the current ready frontier
-> react to any independently exposed child completion/material update
-> inspect + merge evidence + update dependency state
-> close completed child promptly
-> recompute ready frontier
-> refill newly free capacity immediately when useful work is ready
```

A batch barrier is justified only by a real join dependency or a tested native runtime that exposes only a coarser wait surface.

This is a **policy contract, not live runtime proof**. The current accepted static tree has not yet demonstrated that a real current Codex build supports any-child completion/update handling, non-polling wakeups, or C-start-before-A-finish behavior.

Checkpoint 3 therefore contains the asymmetric live case:

```text
A = slow independent dependency
B = fast independent dependency
C = depends only on B
```

When the runtime exposes suitable completion events and capacity, expected behavior is:

```text
A + B start
B completes first
-> process B
-> C becomes ready
-> C starts before A finishes
```

If C waits for A, record barrier serialization and identify whether the cause is main-session policy or native wait semantics.

Completion/wait surface must be characterized as:

```text
barrier_only
per_child_terminal
any_child_update
```

Child-progress observability remains a separate dimension:

```text
none
terminal_only
periodic_summary
structured_live
```

### Upstream concurrency/wait evidence

Current official OpenAI Subagents documentation establishes that independent Subagent work can run in parallel and may save time, and documents `agents.max_concurrent_threads_per_session` as a native cap on concurrently open spawned-Agent threads. The same official documentation currently describes Codex as waiting until all requested agent results are available before returning a consolidated response.

These official facts justify distinguishing native parallel capability from completion-driven dependency scheduling. They do not establish which completion/update surface a specific user build exposes.

`docs/openai-references.md` also records two public OpenAI Codex issues as risk-discovery evidence only:

- #35259 reports substantial model-mediated wait/status polling in one measured user workload and proposes event-driven/harness-managed wakeups;
- #24389 reports a version-specific `close_agent` call blocking a parent thread for hours on an unresponsive child.

Those are public user reports, not OpenAI runtime guarantees or Codex Delegate benchmark data. They motivate live measurement of polling and lifecycle blocking without being promoted into product claims.

### Same-version Plugin maintenance boundary

PR #28 and PR #30 intentionally keep Plugin manifest version `0.6.0` because both are maintenance/refinement merges over the same frozen product baseline.

Current inspected OpenAI PluginStore source indicates explicit install replaces the selected version directory atomically. Current CLI source routes `codex plugin add` through Plugin installation. These are upstream source facts, not proof of the user's current Codex build.

Checkpoint 6 therefore requires a real test that:

```text
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

refreshes installed Plugin bytes even when marketplace content changed while manifest version remains `0.6.0`. If the tested runtime does not refresh correctly, bump a patch version before RC.

## Accepted v0.5.1 historical static evidence

The prior accepted static baseline remains useful for provenance:

```text
feature merge: 9adf8edd303be22506744d569e6552b8fdbc7574
PR #24 feature head: 7dadef8065f46bdb90accd38a3ffccfb75b23a51
PR #24 workflow: 30823406796
post-merge main-equivalent validation: PR #25 / workflow 30824385799
pytest on that accepted baseline: 131 passed
pinned official OpenAI Plugin validator: PASS
```

Historical test counts are evidence provenance, not current documentation-size requirements.

## Last accepted real Codex runtime baseline

The last accepted real production-behavior baseline remains:

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

That live baseline predates v0.6.0 and the completion-driven refinement.

It may be carried forward only for observations whose dependencies have not changed. It is not proof that the accepted current tree:

- exposes every expected exact role/model/effort through current native runtime metadata;
- uses the expected fresh Sol route for a required Final Review Gate;
- passes the intended artifact identity into that review;
- invalidates `ship` after post-review mutation;
- handles `fix-first`, `rethink`, or `INSUFFICIENT_EVIDENCE` correctly in a current live task;
- provides any-child completion/update events;
- avoids model-mediated wait/status polling;
- refills a freed child slot before unrelated active children finish;
- permits useful independent main-session work while children run;
- recovers child slots/close operations without blocking;
- enforces writer exclusion across independent sessions;
- has safe concurrent same-`CODEX_HOME` installation behavior;
- refreshes same-version maintenance Plugin bytes on the user's current Codex build.

## Adversarial consultation contract

Required project consultation mechanism:

```text
/gpt56-sol-pro-consult
```

Exact target conversation:

```text
分支 · 分支 · 项目对比分析
```

Resolution uses exact-title unique-match semantics. Missing or ambiguous resolution returns `CONSULTATION_TARGET_UNRESOLVED`; no replacement or isolated conversation may be substituted for a required Review Checkpoint. Consultation output remains `model_judgment` and never counts as Plugin-install, route, permission, or runtime evidence.

## Pending live validation

The remaining release evidence is runtime work, not another architecture-design cycle:

1. exact live Reader/Worker/Investigator/Advisor route behavior where runtime proof is material;
2. permission/ancestry evidence behavior with the current Codex runtime surface;
3. completion-driven ready-frontier behavior, completion/wait surface, polling overhead, slot refill, and child lifecycle behavior;
4. required Final Review Gate fresh Sol routing, artifact handoff, `ship` invalidation, `fix-first`, `rethink`, and `INSUFFICIENT_EVIDENCE` lifecycle;
5. Dependency Ledger/evidence reuse/intervention/recovery behavior on representative tasks;
6. authorized adaptive read-only fan-out and observed native capacity behavior;
7. same-checkout multi-session writer characterization;
8. real marketplace install/upgrade, same-version maintenance refresh, and current official Plugin validator;
9. concurrent same-`CODEX_HOME` installer characterization;
10. controlled live behavioral pairs and review-yield/cost measurements.

Until those gates are complete, release posture remains:

```text
HOLD FOR RELEASE / LIVE VALIDATION PENDING
```

Known open reproducible PROJECT P0/P1 remains: none.
