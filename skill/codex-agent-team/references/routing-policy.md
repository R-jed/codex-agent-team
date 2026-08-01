# Routing Policy

## Contents

1. Root-aware control model
2. Delegation Gate
3. Minimum Team Principle
4. Capability Gate
5. Context-fork contract
6. Responsibility routing
7. Root-specific behavior
8. Parallelism and lifecycle
9. Failure behavior

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
- Multiple active writing Workers require runtime-backed filesystem/workspace isolation. File-level promises inside one shared checkout are not sufficient.
- One child receives at most one focused follow-up.
- Delegation depth is 1. Workers do not spawn descendants.

## 4. Capability Gate

Role-specific and model-specific routing must be grounded in current native runtime evidence. If the required `agent_type` or `fork_turns` surface is unavailable, do not approximate the route; return the task to Root. Model/effort overrides also require live support when Portable Mode depends on them.

### Portable Mode

Use the built-in role and explicit exact route when the live `spawn_agent` contract exposes model and reasoning overrides.

Example:

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

### Profile Mode

Use a custom Agent profile when it pins the intended model/effort. If the profile owns those values, omit explicit model/effort from the spawn request.

Example:

```text
agent_type = luna_worker
fork_turns = none
```

Portable Mode and Profile Mode are alternative configuration paths. Do not combine a route-pinning profile with competing explicit model/effort overrides.

### Preferred route resolution

1. If live `spawn_agent` exposes the exact target model and reasoning effort, use Portable Mode.
2. If model/effort override is unavailable but the desired route exactly equals the current Root route and inheritance is part of the current tool contract, omit the override and use exact inheritance.
3. If an installed custom Agent profile pins the exact target model/effort, Profile Mode may be used after permission checks.
4. Otherwise set `preferred_route_unavailable` and return the child task to Root.

A documentation page, model catalog, cached schema, or semantic API probe does not prove that the current native Subagent surface accepts a tuple.

### No automatic cross-role fallback

- Luna execution unavailable does not turn Terra into an implementation Worker.
- Terra critic unavailable means Root performs the review or reports that independent model diversity was unavailable.
- Sol Senior Judge unavailable means Root keeps control and reports the unresolved limitation.

## 5. Context-fork contract

MultiAgentV2 defaults `fork_turns` to full history when omitted. Role-specific spawns therefore set it explicitly.

- Explorer: `fork_turns = "none"`.
- Independent Critic: `fork_turns = "none"`.
- Execution Worker: `fork_turns = "none"` by default.
- Execution Worker may use a positive integer string such as `"2"` only when recent user decisions cannot be safely encoded in the task packet.
- Never omit `fork_turns` for a role-specific spawn.
- Never combine `fork_turns = "all"` with `agent_type` on MultiAgentV2. A full-history fork inherits the parent Agent type.

Fresh context is a default, not an excuse to omit task-local facts. Every child still receives a self-contained packet with objective, scope, constraints, acceptance criteria, evidence requirements, and stop conditions.

## 6. Responsibility routing

### Explorer

Default: `gpt-5.6-luna`, `max`, native role `explorer`.

Use for repository mapping, symbol discovery, caller tracing, test mapping, documentation extraction, large read-only investigations, and evidence collection.

Use `fork_turns = "none"`.

### Execution Worker

Default: `gpt-5.6-luna`, `max`, native role `worker`.

Use for bounded implementation, debugging, test creation, test execution, local refactors, mechanical changes, and tool-heavy investigation with a clear acceptance test.

Use a self-contained task packet and `fork_turns = "none"` by default. Use recent-N inheritance only when required to preserve material user decisions.

### Independent Critic

Default: `gpt-5.6-terra`, `xhigh`, native role `default`.

Use when any of these are material:

- independent verification
- cross-module synthesis
- conflicting evidence
- requirement ambiguity
- challenge of a consequential assumption
- important review that deterministic tests cannot fully cover

Do not use Terra merely as a difficulty escalation. Use `fork_turns = "none"`. Give the critic the objective, acceptance criteria, artifact or diff, relevant evidence, and known constraints. Do not give it the producer's private chain of thought.

### Senior Judge

Default: `gpt-5.6-sol`, `high`, native role `default`.

Use only when:

1. Root is not already Sol,
2. the decision has substantial consequence,
3. lower routes leave materially conflicting or insufficient evidence, and
4. the user approves the one-time higher-capability review.

Senior Judge receives a compressed decision packet and does not perform routine repository exploration or implementation.

## 7. Root-specific behavior

### Sol Root

For the common Medium or High Root settings, the typical team is:

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

### Terra XHigh Root

Root already provides Terra-class judgment.

Do not create another Terra Critic solely to claim model diversity. A Terra child is still valid when detached clean-context review itself has concrete value.

If a high-consequence task specifically needs independent model diversity beyond Terra, trigger Consent Gate before a Sol Senior Judge.

### Other Root routes

Keep the same role policy. Do not infer that an unfamiliar Root model is stronger or weaker. Use exact native routes only when available.

## 8. Parallelism and lifecycle

Safe patterns:

```text
Root + Luna Explorer
Root + Luna Worker
Root + Luna Worker + Terra Critic
Root + two independent Luna readers
Root + two Luna writers only with runtime-backed isolated workspaces
```

Avoid redundant quorum with same-model Agents unless the user explicitly requests it and independence is real.

Lifecycle:

```text
spawn -> work -> gather -> verify -> optional focused follow-up -> close
```

Close completed Agents promptly.

## 9. Failure behavior

### Configuration rejection

Record the exact failure and return to Root. Maximum one spawn attempt for a rejected exact configuration.

### Worker failure

Root decides whether deterministic retry with the same route has concrete evidence. Do not automatically climb a model ladder.

### Policy violation

Reject or quarantine results involving nested delegation, unauthorized writes, scope expansion, credential exposure, or unapproved high-impact side effects.

### Uncertainty

Workers report uncertainty. Root must not convert missing evidence into assumed success.
