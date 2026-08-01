# Routing Policy

## Contents

1. Root-aware control model
2. Delegation Gate
3. Minimum Team Principle
4. Capability Gate
5. Responsibility routing
6. Root-specific behavior
7. Parallelism and lifecycle
8. Failure behavior

## 1. Root-aware control model

The current user-facing Codex session is always `ROOT_CONTROLLER`, regardless of its model.

Root owns:

- user intent and acceptance criteria
- decomposition and architecture
- permission and high-impact decisions
- integration and diff acceptance
- final answer

The Skill never requires a Sol root.

## 2. Delegation Gate

A Subagent requires at least one concrete benefit:

### Context isolation

Use when the child will consume substantial source, logs, tests, documentation, search output, command output, or trial-and-error history that can return as a compact conclusion with evidence.

### Real parallelism

Use when branches are genuinely independent. If branch B needs branch A's intermediate conclusion, keep them sequential.

### Independent verification

Use when a consequential result benefits from a fresh Agent that did not produce it.

### Insufficient reasons

Do not delegate solely because:

- a task is long or difficult
- many files exist
- Luna is less expensive
- concurrency is available
- the user asked for careful work

## 3. Minimum Team Principle

- Zero children is normal.
- Default children: 1.
- Normal maximum: 2.
- Hard maximum: 4.
- Automatic Terra critics: at most 1.
- Automatic Sol Senior Judges: at most 1.
- More than 2 children normally requires Consent Gate unless the user already asked for broad parallel work.
- One shared workspace has at most one active writing Worker.
- One child receives at most one focused follow-up.
- Delegation depth is 1. Workers do not spawn descendants.

## 4. Capability Gate

Model-specific routing must be grounded in current native runtime evidence.

### Preferred route resolution

1. If live `spawn_agent` exposes the exact target model and reasoning effort, use it.
2. If model/effort override is unavailable but the desired route exactly equals the current root route and inheritance is part of the current tool contract, omit the override and use inheritance.
3. If an installed custom Agent profile pins the exact target model/effort, it may be used after permission checks.
4. Otherwise set `preferred_route_unavailable` and return the child task to Root.

A documentation page, model catalog, cached schema, or semantic API probe does not prove that the current native Subagent surface accepts a tuple.

### No automatic cross-role fallback

- Luna execution unavailable does not turn Terra into an implementation Worker.
- Terra critic unavailable means Root performs the review or reports that independent model diversity was unavailable.
- Sol Senior Judge unavailable means Root keeps control and reports the unresolved limitation.

## 5. Responsibility routing

### Explorer

Default: `gpt-5.6-luna`, `max`, native role `explorer`.

Use for repository mapping, symbol discovery, caller tracing, test mapping, documentation extraction, large read-only investigations, and evidence collection.

Prefer fresh context.

### Execution Worker

Default: `gpt-5.6-luna`, `max`, native role `worker`.

Use for bounded implementation, debugging, test creation, test execution, local refactors, mechanical changes, and tool-heavy investigation with a clear acceptance test.

Prefer a self-contained task packet. Inherit recent context only when re-packing would lose material user decisions.

### Independent Critic

Default: `gpt-5.6-terra`, `xhigh`, native role `default`.

Use when any of these are material:

- independent verification
- cross-module synthesis
- conflicting evidence
- requirement ambiguity
- challenge of a consequential assumption
- important review that deterministic tests cannot fully cover

Do not use Terra merely as a difficulty escalation. Prefer fresh context. Give the critic the objective, acceptance criteria, artifact or diff, relevant evidence, and known constraints. Do not give it the producer's chain of thought.

### Senior Judge

Default: `gpt-5.6-sol`, `high`, native role `default`.

Use only when:

1. Root is not already Sol,
2. the decision has substantial consequence,
3. Luna/Terra evidence remains materially conflicting or insufficient, and
4. the user approves the one-time higher-capability review.

Senior Judge receives a compressed decision packet and does not perform routine repository exploration or implementation.

## 6. Root-specific behavior

### Sol Medium or High Root

Typical team:

```text
Sol Root + Luna Max Worker
```

Add Terra XHigh only when independent judgment has concrete value.

Architecture, security boundaries, permissions, data integrity, and final high-risk adjudication stay with Root.

Do not create another Sol Worker automatically.

### Luna Max Root

Typical team:

```text
Luna Root + Luna Max Worker
```

The second Luna remains useful for context isolation and real parallelism.

For consequential review, prefer Terra XHigh to gain model diversity.

If a high-consequence conflict remains unresolved, trigger Consent Gate before a Sol Senior Judge.

### Other Root routes

Keep the same role policy. Do not infer that an unfamiliar root model is stronger or weaker. Use exact native routes only when available.

## 7. Parallelism and lifecycle

Safe patterns:

```text
Root + Luna Explorer
Root + Luna Worker
Root + Luna Worker + Terra Critic
Root + two independent Luna readers
Root + two independent Luna workers only when write environments are safely isolated
```

Avoid redundant quorum with same-model Agents unless the user explicitly requests it and independence is real.

Lifecycle:

```text
spawn -> work -> gather -> verify -> optional focused follow-up -> close
```

Close completed Agents promptly.

## 8. Failure behavior

### Configuration rejection

Record the exact failure and return to Root. Maximum one spawn attempt for a rejected exact configuration.

### Worker failure

Root decides whether deterministic retry with the same route has concrete evidence. Do not automatically climb a model ladder.

### Policy violation

Reject or quarantine results involving nested delegation, unauthorized writes, scope expansion, credential exposure, or unapproved high-impact side effects.

### Uncertainty

Workers report uncertainty. Root must not convert missing evidence into assumed success.
