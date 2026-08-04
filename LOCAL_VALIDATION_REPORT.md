# Codex Delegate Local Validation Report

This file is the release evidence ledger for Codex Delegate.

`HEADOFF.md` owns the remaining execution plan. This report owns only four questions:

1. what is the accepted repository/product baseline;
2. what has actually been established and by which evidence class;
3. what material claims remain unverified;
4. what live evidence was recorded for a specific revision/runtime.

Git history and pull requests own development history. This file is not a changelog, architecture document, or second handoff plan.

## Current accepted baseline

```text
Product: Codex Delegate
Plugin version: 0.6.0
Canonical entry point: /codex-delegate
Compatibility namespace: R-jed/codex-agent-team / codex-agent-team
Release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
Architecture posture: FROZEN AT v0.6.0
Repository maintenance posture: ENGINEERING CONSOLIDATION + POLICY REDUCTION COMPLETE
Known open reproducible PROJECT P0/P1: none
```

Latest accepted static validation before this dead-code/evidence-ledger sweep:

```text
PR: #31
exact tested head: 502e738f4a6ba16f8907d7d692c7d8364f734e36
workflow: 30891101018
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 158 passed
Plugin/marketplace JSON validation: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install / --check / idempotent reinstall: PASS
```

The static chain above proves repository consistency only. It does not prove current native route identity, permission enforcement, completion notification semantics, cross-session writer exclusion, installer multi-process safety, or Final Review quality yield.

## Evidence classes

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Deterministic evidence**: reproducible test, validator, installer, verifier, digest, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Upstream source fact**: behavior established from a specific OpenAI source revision or official documentation; version-sensitive when runtime behavior is involved.
- **Public issue telemetry**: user-reported upstream evidence used for risk discovery only.
- **Model judgment**: advisory conclusion; never deterministic/runtime proof.
- **Carried forward**: older evidence whose declared dependencies have not materially changed.
- **Pending revalidation**: policy/tooling exists but the current runtime claim has not been demonstrated.

## Evidence matrix

| Claim / invariant | Evidence class | Current status | Boundary |
| --- | --- | --- | --- |
| Plugin structure and marketplace metadata | Deterministic | PASS | Static only; real CLI install remains live work |
| Official pinned Plugin validator | Deterministic | PASS | Current CI pin, not the future RC validator revision |
| Four managed profile templates match policy contract | Deterministic | PASS | Configuration assurance only |
| Managed profile install / check / idempotent reinstall | Deterministic | PASS | Single-process CI path only |
| `policy-contract.json` owns stable route/resource/final-review constants | Repository fact + tests | PASS | Does not prove post-spawn runtime facts |
| `runtime-evidence.py` keeps route / ancestry / permission evidence separate | Deterministic | PASS | Normalized input only; no rollout scraping |
| `review-artifact.py` binds the source deliverable deterministically | Deterministic | PASS | Ignored/generated deliverables need an additional digest when material |
| One normative owner per major policy boundary | Repository fact + tests | PASS | Duplicate prose is not a second source of truth |
| Completion-driven ready-frontier refill | Repository fact + tests | STATIC PASS / LIVE PENDING | Native completion/wait surface is not yet proven |
| No unnecessary batch barrier when a dependency becomes ready | Policy contract | LIVE PENDING | Checkpoint 3 A/B/C timing case owns proof |
| Required Final Review Gate lifecycle | Repository fact + tests | STATIC PASS / LIVE PENDING | Fresh Sol route, artifact handoff, verdict lifecycle need live proof |
| Exact Reader route | Historical live evidence | CARRIED FORWARD WITH LIMITS | Predates v0.6.0; revalidate when material |
| Exact Worker / Investigator / Advisor routes | Live runtime evidence | PENDING | Current runtime must expose sufficient facts |
| Host-enforced read-only for read-only responsibilities | Live runtime evidence | PENDING | Configuration intent is not permission proof |
| Cross-session same-checkout one-writer safety | Live runtime evidence | PENDING | No global lock is added before reproduction |
| Native child capacity / slot refill / close behavior | Live runtime evidence | PENDING | Runtime-version specific |
| Same-`CODEX_HOME` installer concurrency | Live filesystem evidence | PENDING | I1-I3 in HEADOFF |
| Real marketplace add / upgrade / same-version refresh | Live CLI evidence | PENDING | Checkpoint 6 |
| Contract / Terra-delta / Final Review product value | Controlled live pairs | PENDING | No quality/cost claim before measurement |

## Accepted static design boundaries

The current repository statically establishes these product rules:

```text
main session = task-level control plane
no fixed Agent count
no mandatory Luna -> Terra -> Sol pipeline
delegation depth = 1
baseline no-extra-consent envelope = up to 2 concurrently active justified children
one active writing Worker per canonical physical checkout
exact model-specific routing fails closed without cross-role substitution
acceptance failure != intervention requirement
no universal retry count or stall threshold
completion-driven ready-frontier refill is preferred when the native runtime exposes suitable events
required Final Review Gate cannot be silently downgraded
post-review deliverable mutation invalidates an old ship verdict
```

Stable route/resource/final-review constants live in `plugins/codex-agent-team/policy-contract.json`. Detailed policy lives with the installed Skill reference that owns each boundary.

## Last accepted real Codex runtime baseline

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

This live baseline predates v0.6.0 and the completion-driven refinement. Carry it forward only when the relevant dependency has not changed.

It is not proof that the current accepted tree:

- exposes every expected current role/model/effort tuple;
- enforces read-only intent at the host boundary;
- provides `any_child_update` or equivalent completion wakeups;
- starts C before independent slow A finishes when B alone unlocks C;
- avoids model-mediated status polling;
- closes/reclaims child slots without blocking;
- enforces same-checkout writer exclusion across independent sessions;
- runs the required Final Review Gate with fresh Sol and the exact current artifact;
- refreshes same-version Plugin bytes on the user's current Codex build;
- handles concurrent installers safely.

## Pending live claims

The live evidence backlog is exactly the six release checkpoints in `HEADOFF.md`:

1. exact route, ancestry, and permission evidence where material;
2. contractability, scope safety, and prompt-injection resistance;
3. dependency scheduling, completion/wait behavior, evidence reuse, intervention, and recovery;
4. controlled product-value pairs plus required Final Review lifecycle;
5. adaptive fan-out, consent, native capacity, lifecycle, and multi-session writer safety;
6. current official Plugin validation, real install/upgrade/migration, same-version refresh, and installer concurrency.

Do not add a second planning checklist here. Update `HEADOFF.md` when the execution protocol changes; update this report when evidence changes.

## Adversarial consultation

Required project consultation mechanism:

```text
/gpt56-sol-pro-consult
```

Exact target conversation:

```text
分支 · 分支 · 项目对比分析
```

Resolution is exact-title unique-match and fail closed. Consultation output is `model_judgment`; it never counts as Plugin-install, route, permission, filesystem, or runtime evidence.

## Live validation record format

Append one compact record per material live case. Keep raw/private logs outside the repository unless specifically sanitized for the evidence claim.

```text
TEST_ID
CHECKPOINT
TESTED_REVISION
RUNTIME_VERSION / PLATFORM
WORKLOAD / FIXTURE
EXPECTED INVARIANT
CONFIGURED ROUTE / RESOURCE STATE
OBSERVED RUNTIME EVIDENCE
COMMANDS / VERIFICATION
RESULT: PASS | FAIL | PARTIAL | NOT_EXPOSED
EVIDENCE CLASS
DEPENDENCIES
UNRESOLVED
```

For completion/concurrency cases also record:

```text
CHILD IDS
START / COMPLETION TIMES
WAIT SURFACE: barrier_only | per_child_terminal | any_child_update
SLOT REFILL TIMING
MODEL-MEDIATED POLLING OBSERVED: yes | no | unknown
```

For Final Review cases also record:

```text
FINAL_REVIEW_REQUIREMENT
TRIGGER_REASONS
REVIEW_ARTIFACT_ID
ADVISOR ROUTE EVIDENCE
VERDICT
POST_REVIEW_MUTATION
GATE SATISFIED
```

## Minimal provenance

Only the current structural lineage is retained here; Git and PRs contain the detailed history.

```text
PR #27 -> v0.6.0 Final Review Gate feature baseline
PR #28 -> policy/runtime-evidence engineering consolidation
PR #30 -> README/policy reduction + completion-driven scheduling contract
PR #31 -> post-merge evidence reconciliation
```

Historical v0.5.x evidence remains available in Git history and prior PRs. It should not be copied forward into this ledger unless a current claim explicitly depends on it.
