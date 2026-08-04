# Routing Policy

This file owns dependency readiness, completion-driven dispatch, semantic role selection, and route availability. Consent, recovery, safety, and runtime-evidence semantics have separate normative owners.

## 1. Control model

The current user-facing Codex session is the main session and owns the task-level compute graph:

```text
intent / scope / architecture / decision rights
Dependency Ledger / scheduling
Shared Evidence State / Recovery Ledger
integration / acceptance / final answer
```

Models are compute lanes, not authority levels or mandatory stages. The main session does not need to be Sol.

## 2. No fixed pipeline or team size

Valid graphs include:

```text
main
main -> Luna -> main
main -> Luna -> Sol -> main
main -> Terra -> Luna -> main
main -> Luna -> Terra(delta) -> Luna or main
main -> Sol -> main
```

`Luna -> Terra -> Sol` is never required merely because those lanes exist.

Every Agent call must satisfy a distinct unresolved dependency. Zero children is normal. Codex Delegate has no product-level hard child count.

## 3. Dependency Ledger and ready frontier

Track material task dependencies as compact in-session state:

```text
id
outcome
status: pending | ready | running | satisfied | blocked | invalidated
requires
produces
write_intent
workspace
acceptance
```

A dependency is `ready` only when its prerequisites are satisfied and no valid evidence already satisfies it.

Rules:

- one dependency has at most one active owner;
- never rerun a satisfied dependency unless changed inputs invalidate it;
- invalidation propagates through declared dependencies rather than reopening the whole task by default;
- combine ready work when one responsibility can satisfy it more cheaply without losing useful isolation or critical-path progress;
- split work only when each packet has distinct acceptance value;
- recompute the ready frontier after every material user, evidence, artifact, dependency, workspace, route, permission, or runtime-capacity event.

The ledger is logical task state. Codex Delegate does not add a persistent DAG service, background scheduler, thread pool, or second Agent runtime.

## 4. Delegation gates

A ready dependency is dispatchable only when:

1. delegation has concrete benefit: context isolation, useful parallelism, specialized capability, or independent high-value judgment;
2. a writing responsibility passes `delegation-contract.md`;
3. `safety-policy.md`, `consent-policy.md`, exact route availability, and native capacity allow it.

Task length, file count, lower price, free slots, or a generic desire for caution do not justify an Agent by themselves.

## 5. Completion-driven dispatch

The scheduling policy is **completion-driven around the ready frontier**, not wave/barrier driven by default.

At every scheduling point:

```text
1. recompute currently ready dependencies
2. choose the smallest useful set that fits current safe capacity
3. dispatch those responsibilities
4. keep independent main-session work moving when it does not duplicate or conflict
5. react to each child completion/material update as soon as the runtime exposes it
6. inspect and merge that result, update dependency/evidence state, and close completed child
7. recompute the frontier immediately
8. if safe capacity is free and useful work is newly ready, dispatch it without waiting for unrelated children
```

Example:

```text
A = slow independent dependency
B = fast independent dependency
C = depends only on B

spawn A + B
B completes
-> collect B
-> C becomes ready
-> start C while A is still running, when native capacity and safety allow
```

Do **not** wait for A merely because A and B were launched in the same scheduling wave.

A barrier wait is justified only when:

- a real join dependency requires all relevant active results before any useful next work can begin; or
- the tested native runtime exposes only a coarser waiting/completion surface.

If the runtime cannot expose individual completion/update events, record that runtime limitation and degrade to the available surface. Do not claim event-driven runtime behavior that was not observed.

Avoid model-mediated busy polling. When the runtime offers a blocking/event-like wait, mailbox/update notification, or equivalent native mechanism, prefer that to repeated status-only model turns. The exact available wait surface is a version-scoped runtime fact and must be characterized during live validation.

## 6. Resource scopes

Scheduling, consent, native capacity, and workspace safety are different constraints.

### Consent

Explicit `/codex-delegate` use includes the baseline in `consent-policy.md`: up to two concurrently active justified children without another prompt. This is a consent envelope, not a team-size target or lifetime child limit.

Larger simultaneous fan-out requires consent when that policy says so. After authorization, there is no second product numerical ceiling.

### Native capacity

Codex runtime decides how many child threads can actually be active. If useful ready work exceeds slots, keep the excess pending and refill capacity as children complete.

Do not convert one observed runtime capacity into a permanent product constant and do not cross-route merely to fill a slot.

### Workspace

At most one active writing Worker may target one canonical physical checkout. Multiple writers require genuinely isolated runtime-backed worktrees/workspaces/repositories.

Disjoint intended file lists inside one checkout do not prove write isolation.

### Codex home

Managed custom-Agent profiles are shared configuration. Mixed concurrent managed-profile generations are unsupported for v1; an exact-route mismatch fails closed instead of cross-routing or silently rewriting shared state.

Delegation depth remains one.

## 7. Semantic roles

Role identity is separate from model identity. Exact current constants live in `../../policy-contract.json`.

| Responsibility | Agent type | Current route | Default intent | Use |
| --- | --- | --- | --- | --- |
| reader | `codex_agent_team_reader` | GPT-5.6 Luna `max` | read-only | bounded search, tracing, mapping, evidence |
| worker | `codex_agent_team_worker` | GPT-5.6 Luna `max` | workspace-write | contractable implementation/debugging/tests |
| investigator | `codex_agent_team_investigator` | GPT-5.6 Terra `xhigh` | read-only | unresolved difficult technical delta |
| advisor | `codex_agent_team_advisor` | GPT-5.6 Sol `high` | read-only | consequential judgment and review |

Changing a future model route must not require renaming the semantic role.

## 8. Route by responsibility

Route first by responsibility, decision boundary, and demonstrated capability. Cost is only a tie-breaker between equally suitable safe lanes.

### Reader / Worker

Use Luna Reader for bounded reusable evidence and Luna Worker for contractable implementation.

Worker authority comes from the Delegation Contract, not task difficulty.

### Investigator

Terra is not a mandatory reviewer and not a generic second implementation attempt.

Use it only when a clear contract and execution evidence establish a genuinely difficult unresolved technical dependency. Pass the unresolved delta, valid evidence, current artifact/failure, material recovery facts, and explicit `DO NOT REDO` items.

Low quality alone is not a Terra trigger.

### Advisor

Sol handles bounded consequential judgment or independent review when that adds value. It should consume compressed established facts and one review/decision question rather than repeat still-valid discovery.

Sol is not globally mandatory. `final-review-gate.md` may make a fresh Advisor `ship` verdict mandatory for one high-risk deliverable.

## 9. Execution progress and recovery boundary

Routing does not decide retry/restart/escalation from failure alone. Use `execution-progress.md`.

```text
healthy incomplete work -> continue current responsibility
mechanical defect       -> focused Luna correction
contract gap            -> main repairs contract
stall/context pollution -> clean same-lane restart
capability gap          -> Terra receives unresolved delta
judgment gap            -> main or justified Sol
```

There is no universal retry count or numerical stall threshold.

## 10. Evidence reuse

Use the Shared Evidence State carried by `delegation-contract.md` and execution policy.

Deterministic/repository facts remain reusable while their declared dependencies are valid. Model judgments remain challengeable. A changed input invalidates only affected evidence.

Completion-driven dispatch uses these updates to unlock new dependencies immediately rather than waiting for an unrelated scheduling wave to finish.

## 11. Runtime route assurance

Model-specific lanes use exact custom project profiles. There is no Portable Mode, built-in-role substitution, or hidden model ladder.

Before spawn, profile matching provides only configuration assurance:

```text
route_assurance = profile_locked
```

When post-spawn route identity, ancestry, permission, capacity, wait semantics, or review independence is material, use `runtime-assurance.md` and the bundled normalized verifier:

```text
skill_dir/../../scripts/runtime-evidence.py
```

Do not use or reference removed rollout-coupled project inspectors. Missing runtime observations remain missing.

## 12. Completion and lifecycle

A completed child should be inspected and closed promptly once its result is no longer needed as an active thread. This allows native capacity to recover and prevents a finished thread from acting as an accidental slot barrier.

Do not close/interrupt a running child solely to create artificial throughput. If the runtime's close/wait behavior itself blocks or leaks capacity, record it as version-scoped runtime evidence and handle it in release validation rather than hiding it with policy claims.
