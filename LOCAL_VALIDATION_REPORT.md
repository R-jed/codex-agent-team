# Codex Delegate Local Validation Report

This file is the evidence ledger for local runtime validation. `HEADOFF.md` defines what must be tested next. This report records what was actually observed, on which revision/runtime, what evidence remains reusable, and what is still unverified.

Repository policy, CI, and model consultation are not proof of live Codex runtime behavior.

## Current reconciliation

Report reconciled: 2026-08-03.

Current product state:

```text
Product: Codex Delegate
Plugin version: 0.5.0
Canonical user entry point: /codex-delegate
Compatibility repository/package namespace: R-jed/codex-agent-team / codex-agent-team
Release posture: HOLD FOR RELEASE / VALIDATION INCOMPLETE
Known open reproducible PROJECT P0/P1: none
```

The v0.5.0 adaptive-orchestration candidate was statically validated on PR #22 at branch head:

```text
31b9f4e0a14048ee3d500736c5faf45dad61be49
```

GitHub Actions run `30803487630` passed on:

```text
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest on Ubuntu / Python 3.11: 119 passed
Plugin manifest validation: PASS
managed profile install: PASS
managed profile --check: PASS
idempotent managed profile reinstall: PASS
```

This report reconciliation is documentation-only and follows that tested candidate. The exact final merge SHA must be recorded at the next local checkpoint after `origin/main` is fetched.

The last accepted real Codex production-behavior baseline remains:

```text
c6020db903b35f0d57677b131bf35b0580144ab9
```

Do not relabel v0.5.0 static CI as live runtime evidence.

## Evidence status rules

Use these distinctions throughout this report:

- **Repository fact**: source, manifest, policy, test, or commit state observed directly from the repository.
- **Deterministic evidence**: reproducible test, verifier, installer, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Model judgment**: advisory conclusion that remains challengeable and cannot substitute for deterministic or runtime evidence.
- **Carried forward**: older evidence whose declared dependencies have not changed materially.
- **Pending revalidation**: policy or code exists, but the corresponding live claim has not yet been demonstrated on the current validation cycle.

## Last accepted live runtime environment

The live evidence currently carried forward was collected on:

```text
initial validation revision: 1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d
accepted symlink-fix baseline: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon, macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

The `c6020db...` revision is an evidence baseline, not the current repository head.

## v0.5.0 static architecture evidence

The repository now defines **Adaptive Dependency Orchestration**.

### Dependency-driven scheduling

Repository facts established by policy, schemas, eval fixtures, and tests:

- the main session owns an in-session Dependency Ledger;
- dependency states are `pending | ready | running | satisfied | blocked | invalidated`;
- scheduling starts from the ready frontier rather than a desired Agent count;
- zero children remains a valid outcome;
- there is no product-level hard child ceiling;
- the previous `default 1 / normal max 2 / hard max 4` scheduling model is removed;
- routing schema no longer limits `nodes` to four items;
- an authorized static case with five independent read-only Reader dependencies is valid;
- a slot-pressure case schedules only the currently available children and leaves remaining ready dependencies queued;
- an already-running dependency must not receive duplicate inference.

These are repository and deterministic facts. They do not prove how many child threads a particular Codex runtime can run simultaneously.

### Consent boundary

The number `2` now has one narrow meaning:

```text
up to 2 concurrently active justified child Agents
-> normal no-extra-consent envelope for explicit /codex-delegate use
```

More than two simultaneous children normally requires consent unless broad parallel work was already authorized.

This is not a lifetime child-call cap, scheduler target, or native capacity claim. Material serial compute expansion is also consent-gated so orchestration cannot evade resource consent by running a large number of calls two at a time.

### Native capacity

The repository policy now treats native child-slot capacity as runtime evidence.

Expected behavior when ready work exceeds current slots:

```text
queue or serialize remaining ready dependencies
preserve exact role/model identity
never duplicate the same dependency merely to keep compute busy
never infer a universal product ceiling from one runtime build
```

No live capacity number is established yet for the current v0.5.0 validation cycle.

### Workspace safety

The existing invariant remains:

```text
one active Writing Worker per canonical physical checkout/workspace
```

Independent runtime-backed worktrees or independent repositories may have independent writers.

The policy applies across independent main sessions, but native cross-session enforcement has not yet been proven. Until the M1-M4 live matrix is complete, no claim is made that current Codex itself prevents two independent sessions from writing one checkout simultaneously.

### Execution-progress and recovery policy

v0.5.0 introduces `execution-progress.md` and extends contracts/Agent profiles with:

```text
failure_signature
progress_signal: advanced | unchanged | regressed | blocked
new_evidence
invalidated_evidence
unresolved_delta
DO NOT REDO
EXECUTION_STALL
```

Repository rules now establish:

- model confidence, narration, or file writes do not count as progress by themselves;
- repeated same-failure execution without new evidence is a stall signal;
- there is no universal retry count;
- an unchanged contract is not resent merely because the previous attempt failed;
- a clean same-lane restart preserves current artifact, valid evidence, failure signature, unresolved delta, acceptance, and `DO NOT REDO` facts while dropping dead-end narration/private reasoning;
- evidence-supported capability gaps go to Terra as unresolved technical delta before repeated same-lane retry;
- Sol receives compressed fresh context for selective high-value judgment/review.

These are static product contracts. Real clean-restart, stall detection, and capability-before-retry behavior remain live-validation items.

## Exact semantic route state

Current shipped configuration remains:

| Role | Configured route | Sandbox intent | Live evidence carried forward |
| --- | --- | --- | --- |
| Reader | GPT-5.6 Luna / max | read-only | historical L1 local corroboration |
| Worker | GPT-5.6 Luna / max | workspace-write | discovery only, live exact route pending |
| Investigator | GPT-5.6 Terra / xhigh | read-only | discovery only, live exact route pending |
| Advisor | GPT-5.6 Sol / high | read-only | discovery only, live exact route pending |

The model/effort/sandbox routes did not change in v0.5.0. The profile instruction bytes did change to support dependency-bound execution and progress reporting.

Configuration assurance remains separate from runtime observation.

## Historical Plugin and profile evidence carried forward

Real historical evidence:

- marketplace registration succeeded from the documented Git source and `main` ref;
- Plugin `codex-agent-team@codex-agent-team` version 0.3.0 installed successfully;
- before custom-profile provisioning, a fresh task reported the roles unavailable and did not substitute another role;
- real profile provisioning wrote four project profiles and one ownership manifest;
- installer `--check` passed;
- a task created before provisioning did not refresh custom-role discovery on Codex 0.146.0;
- a fresh task after provisioning discovered all four semantic roles;
- the real Reader used `fork_turns=none` and returned the bounded probe result;
- local rollout inspection reported Reader role, Luna model, max effort, read-only sandbox, managed permission profile, runtime 0.146.0, and expected parent id;
- native independent attestation was not separately exposed, so that Reader result remains L1 rather than R1/R2.

Because v0.5.0 changes managed profile instruction bytes, real installed-profile **upgrade behavior** from 0.4.x to 0.5.0 is pending even though the deterministic installer lifecycle is green.

## Runtime Truth evidence carried forward

Static verifier coverage remains valid for:

- incomplete expected exact route fails closed;
- route, ancestry, and permission evidence remain typed independently;
- missing or partial observations do not become affirmative proof;
- configuration/local/native conflict can be quarantined;
- exact role/model/effort proof is two-sided.

One historical real Reader record passed sanitized local inspection.

Still pending where the live runtime exposes enough facts:

- Worker/Investigator/Advisor exact route observation;
- native complete route observation;
- native/local agreement;
- partial native route behavior;
- role/model/effort/parent/sandbox conflict characterization;
- duplicate rollout and schema drift on the current Codex build.

## Contractability and safety evidence

Historical live evidence carried forward:

- missing-profile path failed closed;
- a fresh Reader task used a bounded responsibility and explicit `fork_turns=none`.

Static v0.5.0 policy now additionally covers:

- dependency-bound Delegation Contract;
- concurrent workspace drift invalidation;
- one owner for one running dependency;
- no child descendants;
- prompt-injection content cannot change dependency state, consent, routes, or evidence policy;
- exact profile mismatch fails closed;
- behavioral read-only never becomes a runtime-enforced claim without native evidence.

Live contractability, prompt injection, changed-file scope, and concurrent-edit simulations remain pending.

## Shared Evidence and dependency-state evidence

Static v0.5.0 contract defines both:

```text
Dependency Ledger
Shared Evidence State
```

No live claim is yet made that the current Codex behavior consistently:

- prevents duplicate running-dependency calls;
- avoids rediscovering valid evidence;
- propagates invalidation only through dependent facts;
- recomputes the ready frontier correctly after concurrent/user changes.

These are Checkpoint 3 live gates.

## Behavioral evaluation state

Behavioral schema/workloads/scorer are now version `3.0` for the adaptive architecture.

New measurable fields include:

```text
peak_active_children
ready_dependencies
dependency_ids
runtime_slot_waits
execution_stall_events
clean_same_lane_restarts
unjustified_retry_calls
same_failure_without_new_evidence
```

The scorer still enforces paired controls for primary product-value experiments.

No live behavioral result has yet established that:

- compiled contracts improve acceptance quality or cost;
- adaptive fan-out improves latency;
- a clean same-lane restart improves recovery;
- Terra delta reduces rework;
- selective Sol improves review quality;
- any particular Codex runtime supports a particular universal concurrency maximum.

Those remain measurements, not product claims.

## Adaptive fan-out and lifecycle status

Static coverage includes:

```text
F0 zero child valid
F1 one dependency may use one child
F2 two concurrent justified children fit the explicit-command baseline
F3 more than two simultaneous children without broad authorization asks consent
F4 five authorized independent read-only dependencies are legal at the product-policy level
slot pressure queues remaining dependencies
```

Live evidence is still required for:

- actual available native slots;
- peak active children;
- slot recovery after close/failure/cancellation;
- queued dependency resumption;
- orphan/ghost ownership;
- 10-cycle lifecycle stress;
- no duplicate dependency call under real fan-out.

## Multi-session workspace status

The required live matrix is:

```text
M1 different sessions + different projects/checkouts
M2 different sessions + isolated worktrees
M3 different sessions + same canonical physical checkout
M4 writer session + read-only session on same checkout
```

No cross-session workspace lock has been added. A project-side coordination mechanism remains conditional on a reproducible M3 failure.

## Installer evidence

### CAT-LOCAL-001: direct Codex-home endpoint symlink

Historical defect:

```text
Severity: P1
Ownership: PROJECT
Pre-fix revision: 1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d
Fixed baseline: c6020db903b35f0d57677b131bf35b0580144ab9
Status: CLOSED
```

Expected behavior was to reject a symlink supplied directly as the `--codex-home` endpoint before creating any managed target entry. Pre-fix behavior resolved the symlink and wrote the four profiles plus manifest into the target. The accepted fix rejects the endpoint symlink before normal resolution while preserving compatibility with a non-symlink endpoint beneath symlinked ancestors.

Focused regression, installer suite, full deterministic suite, and the original filesystem reproduction all passed after the fix.

Residual pathname TOCTOU was outside that focused patch threat model and is not a blocker without new evidence.

### v0.5.0 managed profile upgrade

Deterministic CI proves fresh v0.5.0 profile install, exact `--check`, and idempotent reinstall.

Real upgrade still required:

```text
0.3.x Codex Agent Team -> current Codex Delegate
0.4.x Codex Delegate -> 0.5.0 profile instruction generation
user-modified/unproven profile -> untouched + affected route fail closed
fresh v0.5.0 install -> display name and /codex-delegate discovery
```

### Concurrent installer gates

Still pending:

```text
I1 two same-generation installers on one clean CODEX_HOME
I2 one forced-failure transaction concurrent with a peer success
I3 competing managed profile generations in one CODEX_HOME
```

No inter-process lock has been added before evidence establishes the need.

## Review reconciliation

Historical inspector dispute remains characterized as a latent schema-compatibility risk rather than a confirmed supported-path defect. The reproduction that saw two `session_meta` records used a generic child with `fork_turns=all`; the supported Reader path used `fork_turns=none` and inspected successfully.

The historical symlink defect received adversarial review and was accepted as a minimal PROJECT/P1 repair.

For the v0.5.0 cycle, `gpt56-sol-pro-consult` remains the required independent adversarial consultation mechanism at Review Checkpoints A-E and for any P0/P1 candidate. Its output is model judgment and cannot count as Codex Delegate runtime-route evidence.

## Current takeover status

**HOLD FOR RELEASE / VALIDATION INCOMPLETE**

This status is caused by unfinished mandatory live gates, not by a currently known reproducible PROJECT P0/P1.

Highest-priority unfinished evidence now follows `HEADOFF.md`:

1. exact live Worker, Investigator, and Advisor routes plus Runtime Truth cases;
2. contractability, concurrent-edit, prompt-injection, and scope simulations;
3. Dependency Ledger, ready-frontier, evidence-reuse, stall, clean-restart, and capability-before-retry behavior;
4. raw-prompt versus compiled-contract product-value pairs plus Terra/Sol controlled pairs;
5. adaptive fan-out, consent boundary, native slot capacity/recovery, lifecycle, and M1-M4 workspace matrix;
6. real 0.3/0.4 -> 0.5 migration and I1-I3 installer concurrency.

Continue in the finite checkpoint order in `HEADOFF.md`. After each checkpoint, append the actual tested `origin/main` SHA, runtime/platform, evidence class, dependency/progress/resource state, defects, and unresolved unknowns before the required adversarial review.
