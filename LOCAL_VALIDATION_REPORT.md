# Codex Delegate Local Validation Report

This is the evidence ledger for Codex Delegate. `HEADOFF.md` defines the remaining live/release gates. This report records what was actually established, on which repository/runtime baseline, and which claims remain unverified.

Repository policy, static CI, Plugin validation, source inspection, and model judgment are not substitutes for live Codex runtime evidence.

## Current reconciliation

Reconciled: 2026-08-04.

```text
Product: Codex Delegate
Plugin version: 0.6.0
Canonical entry point: /codex-delegate
Repository/package compatibility namespace: R-jed/codex-agent-team / codex-agent-team
Accepted v0.6.0 feature merge: b043428223ba99ce77e2268c32cfa6a38daad3ed
Current main at start of engineering consolidation: bbadaf0febf3c9b89b542c2a62ff208ea268e176
Release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
Static architecture posture: ARCHITECTURE FROZEN AT v0.6.0
Known open reproducible PROJECT P0/P1: none
```

PR #27 is merged. It is no longer a feature candidate. The accepted v0.6.0 implementation baseline is the squash merge `b043428...`; later main commits reconciled README/HEADOFF wording without claiming new runtime proof.

The current `refactor/engineering-consolidation-v061` branch is a behavior-preserving maintenance candidate. Until its own CI is green and it is accepted/merged, this report does not treat its new verifier/policy-contract refactor as accepted static evidence.

## Evidence classes

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Deterministic evidence**: reproducible test, validator, installer, verifier, digest, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Upstream source fact**: behavior established from a specific OpenAI Codex source revision; version-sensitive until matched to a tested runtime.
- **Model judgment**: advisory conclusion; never deterministic/runtime proof.
- **Carried forward**: older evidence whose dependencies have not materially changed.
- **Pending revalidation**: policy/tooling exists but the corresponding current runtime claim has not been demonstrated.

## Accepted v0.6.0 static evidence

The final PR #27 closure tree was:

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

These results establish repository/static consistency for the v0.6.0 feature tree. They do not establish current live Worker/Investigator/Advisor route identity, host-enforced read-only, child progress observability, cross-session writer exclusion, installer multi-process behavior, or mandatory Final Review quality yield.

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

It covers:

- current `HEAD` when present;
- complete tracked working-tree diff against `HEAD`;
- Git-relevant executable-mode changes;
- non-ignored untracked regular files and symlinks;
- unborn repositories without writing synthetic Git objects;
- double-sampled workspace state so a mutation during identity capture fails closed.

Ignored/generated deliverables require an additional deterministic digest when they are part of the requested deliverable.

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

Do not use historical test counts as requirements for current documentation. They are evidence provenance only.

## Last accepted real Codex runtime baseline

The last accepted real production-behavior baseline remains:

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

That live baseline predates v0.6.0.

It may be carried forward only for observations whose dependencies have not changed. It is not proof that v0.6.0:

- uses the expected fresh Sol route for a required Final Review Gate;
- passes the intended artifact identity into that review;
- invalidates `ship` after post-review mutation;
- handles `fix-first`, `rethink`, or `INSUFFICIENT_EVIDENCE` correctly in a current live task;
- preserves current consent behavior across repeated review cycles;
- enforces writer exclusion across independent sessions;
- has safe concurrent same-`CODEX_HOME` installation behavior.

## Current engineering-consolidation candidate

`refactor/engineering-consolidation-v061` is intentionally behavior-preserving. Its engineering goals are maintenance and contract repair:

```text
restore a shipped deterministic Runtime Evidence executable path
remove dependence on a project rollout-file inspector
introduce policy-contract.json as the stable constant source
make installer/profile tests consume that contract
reduce SKILL.md to the task-level policy kernel
replace arbitrary README line budgets / broad phrase locks with semantic tests
reconcile user architecture and evidence docs with merged v0.6.0 state
```

This candidate does not intentionally change:

- Luna/Terra/Sol model routes;
- delegation depth;
- one-writer policy;
- consent envelope;
- Final Review trigger semantics or verdict lifecycle;
- installer ownership/migration authority;
- Plugin package id or version.

Its acceptance requires its own complete maintained CI matrix and pinned Plugin validator result before merge.

## Pending live validation

The remaining release evidence is runtime work, not another architecture-design cycle:

1. exact live Reader/Worker/Investigator/Advisor route behavior where runtime proof is material;
2. permission/ancestry evidence behavior with the current Codex runtime surface;
3. required Final Review Gate fresh Sol routing, artifact handoff, `ship` invalidation, `fix-first`, `rethink`, and `INSUFFICIENT_EVIDENCE` lifecycle;
4. Dependency Ledger/evidence reuse/intervention/recovery behavior on representative tasks;
5. authorized adaptive read-only fan-out and observed native capacity behavior;
6. same-checkout multi-session writer characterization;
7. real marketplace install/upgrade and current official Plugin validator;
8. concurrent same-`CODEX_HOME` installer characterization;
9. controlled live behavioral pairs and review-yield/cost measurements.

Until those gates are complete, release posture remains:

```text
HOLD FOR RELEASE / LIVE VALIDATION PENDING
```
