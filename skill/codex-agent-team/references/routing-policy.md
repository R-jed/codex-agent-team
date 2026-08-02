# Routing Policy

## Contents

1. Root-aware control model
2. Delegation Gate
3. Minimum Team Principle
4. Route Assurance Gate
5. Runtime Observation Gate
6. Context-fork contract
7. Responsibility routing
8. Review Gate
9. Root-specific behavior
10. Parallelism and lifecycle
11. Failure behavior

## 1. Root-aware control model

The current user-facing Codex session is always `ROOT_CONTROLLER`, regardless of its model.

Root owns user intent, decomposition, architecture, permission decisions, integration, diff acceptance, high-impact decisions, and the final answer.

The Skill never requires a Sol Root and never silently changes the current Root model or reasoning effort.

Role-to-route bindings are stable policy. Team composition is task-aware and dynamic: Root decides whether the task needs execution, detached review, or a consent-gated senior judgment role.

## 2. Delegation Gate

A Subagent requires at least one concrete benefit.

### Context isolation

Use when substantial source, logs, tests, documentation, search output, command output, or trial-and-error history can stay outside Root and return as compact evidence.

### Real parallelism

Use when branches are genuinely independent. If branch B needs branch A's intermediate conclusion, keep them sequential.

### Independent verification

Use when a consequential result benefits from a fresh Agent that did not produce it.

### Insufficient reasons

Do not delegate solely because a task is long, many files exist, Luna is inexpensive, concurrency is available, or the user asked for careful work.

## 3. Minimum Team Principle

- Zero children is normal.
- Default children: 1.
- Normal maximum: 2.
- Hard maximum: 4.
- Automatic Terra critics: at most 1.
- Automatic Sol Senior Judges: at most 1.
- More than 2 children normally requires Consent Gate unless broad parallel work was already requested.
- One shared workspace has at most one active writing Worker.
- Multiple active writing Workers require runtime-backed filesystem/workspace isolation.
- One child receives at most one focused follow-up.
- Delegation depth is 1. Workers do not spawn descendants.

Runtime assurance and review must not increase Agent count by themselves. They can strengthen evidence for an already-justified responsibility.

## 4. Route Assurance Gate

Model-specific routing must be grounded in current native runtime evidence available before or at spawn. Keep route intent, accepted configuration, assurance, and later observation separate:

```text
preferred_route
configured_route
route_assurance
observed_route
```

The Skill never manufactures observation that Codex does not expose. A successful exact spawn can establish `configured_route`; `observed_route` may remain `not_exposed`.

### Assurance state: `profile_locked`

Use Profile Mode when an installed custom role pins the exact model and reasoning effort and the live `spawn_agent` role guidance reports those settings as locked.

Expected profiles:

| Agent type | Locked model | Locked effort |
| --- | --- | --- |
| `luna_explorer` | `gpt-5.6-luna` | `max` |
| `luna_worker` | `gpt-5.6-luna` | `max` |
| `terra_reviewer` | `gpt-5.6-terra` | `xhigh` |
| `sol_judge` | `gpt-5.6-sol` | `high` |

Spawn shape:

```text
agent_type = luna_worker
fork_turns = none
```

Do not also send explicit model/effort when the profile owns them.

### Assurance state: `native_explicit_validated`

Use Portable Mode when:

1. live `spawn_agent` exposes `agent_type`, `fork_turns`, `model`, and `reasoning_effort`;
2. the target model is available for the current MultiAgent backend;
3. the selected role is not reported as locked to an incompatible model or effort; and
4. Codex accepts the exact explicit request.

Spawn shape:

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

Codex validates the requested model and supported reasoning effort before the child is created. Treat rejection as `preferred_route_unavailable`.

### Built-in role shadowing

Current Codex allows user-defined roles to shadow built-in role names. Before Portable Mode uses `explorer`, `worker`, or `default`, inspect the live role guidance. If that role is locked to a different model or effort, Portable Mode for the requested route is invalid.

### Effective selection precedence

Current Codex resolves model and reasoning settings with this precedence when a custom Agent is involved:

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Model and reasoning effort resolve independently. Profile Mode and Portable Mode are alternative assurance paths.

### No inheritance-based exact route

Do not treat omission of `model` or `reasoning_effort` as exact assurance. Current Codex may apply configured `agents.default_subagent_model` or `agents.default_subagent_reasoning_effort` before role configuration.

If explicit overrides are hidden and an exact locked profile is unavailable, return the task to Root.

### No automatic cross-role fallback

- Luna execution unavailable does not turn Terra into an implementation Worker.
- Terra critic unavailable means Root reviews without claiming independent Terra verification.
- Sol Senior Judge unavailable means Root keeps control and reports the limitation.
- An unused role being unavailable does not block responsibilities that do not depend on it.

## 5. Runtime Observation Gate

After spawn, use `runtime-assurance.md` when effective route or permission evidence matters.

Track:

```text
observation_source: native_metadata | local_rollout | none
observed_agent_type
observed_route
observed_sandbox
observed_permission_profile
observation_status: matched | not_exposed | mismatch | invalid
```

Prefer public native metadata. Use the bundled local rollout inspector only as a read-only fallback when required fields are omitted and the local sessions store is accessible.

For ordinary bounded work, configuration assurance remains sufficient and missing runtime telemetry may stay `not_exposed`.

Make runtime observation an acceptance requirement when:

- safety depends on effective host-enforced read-only isolation;
- a high-consequence conclusion specifically relies on verified cross-model independence;
- the user explicitly requests proof of effective route or permission state; or
- available runtime evidence conflicts with the configured route.

If two observation sources expose the same field, require agreement. A mismatch quarantines the affected child result.

## 6. Context-fork contract

MultiAgentV2 defaults `fork_turns` to full history when omitted. Role-specific spawns therefore set it explicitly.

- Explorer: `fork_turns = "none"`.
- Independent Critic: `fork_turns = "none"`.
- Execution Worker: `fork_turns = "none"` by default.
- Execution Worker may use a positive integer such as `"2"` only when recent user decisions cannot be safely encoded in the task packet.
- Never omit `fork_turns` for a role-specific spawn.
- Never combine `fork_turns = "all"` with `agent_type` on MultiAgentV2.

Fresh context does not remove task-local facts. Every child still receives a self-contained objective, scope, constraints, acceptance criteria, evidence requirements, and stop conditions.

## 7. Responsibility routing

### Explorer

Default route: `gpt-5.6-luna`, `max`.

Use for repository mapping, symbol discovery, caller tracing, test mapping, documentation extraction, large read-only investigations, and evidence collection.

### Execution Worker

Default route: `gpt-5.6-luna`, `max`.

Use for bounded implementation, debugging, test creation, test execution, local refactors, mechanical changes, and tool-heavy investigation with clear acceptance criteria.

For coding tasks, prefer the Implementation Preset in `task-packet.md`. Require explicit ownership, interfaces, constraints, verification, and `judgment_calls` in the return report.

### Independent Critic

Default route: `gpt-5.6-terra`, `xhigh`.

Use when independent verification, cross-module synthesis, conflicting evidence, requirement ambiguity, or challenge of a consequential assumption is material.

Do not use Terra as a generic difficulty escalation or implementation lane. Give the critic the objective, acceptance criteria, actual artifact/diff, relevant evidence, and constraints without the producer's private reasoning.

### Senior Judge

Default route: `gpt-5.6-sol`, `high`.

Use only when Root is not already Sol, the decision has substantial consequence, lower routes leave material uncertainty/conflict, and the user approves one higher-capability review.

## 8. Review Gate

Independent review is selective. Root first inspects the actual mutation and reruns deterministic verification.

Add one Terra critic when fresh judgment has concrete acceptance value, especially for:

- security, permissions, concurrency, or state consistency;
- cross-module invariants, public contracts, migrations, or broad blast radius;
- weak deterministic oracles;
- material Worker `judgment_calls` beyond mechanical execution;
- conflicting evidence or consequential assumptions.

The critic returns:

```text
review_status: clear | findings | insufficient_evidence
findings
residual_risk
```

`clear` means no material issue was found in the reviewed evidence. Root still owns final acceptance.

For bounded findings, correct the work and rerun deterministic verification. Run a fresh Terra review only when the correction materially changes the risk that justified detached review.

If high-consequence disagreement remains after the critic and Root is not Sol, apply Consent Gate before one Sol Senior Judge.

## 9. Root-specific behavior

### Sol Root

Typical team is `Sol Root + Luna Max Worker`. Add Terra only when detached judgment has concrete value. Do not create another Sol Worker automatically.

### Luna Max Root

A second Luna remains useful for context isolation and real parallelism. Consequential review prefers Terra for model diversity. A remaining high-consequence conflict may trigger Consent Gate before one Sol Senior Judge.

### Terra XHigh Root

Do not create another Terra solely to claim model diversity. A Terra child is valid when detached clean-context review itself has value. A high-consequence need for stronger independent diversity may trigger Consent Gate before one Sol Senior Judge.

### Other Root routes

Do not infer relative strength from an unfamiliar Root route. Use only provable exact child routes.

## 10. Parallelism and lifecycle

Safe patterns include Root + Luna Explorer, Root + Luna Worker, Root + Luna Worker + Terra Critic, two independent Luna readers, or two writing Luna Workers only with runtime-backed isolated workspaces.

Lifecycle:

```text
spawn -> work -> observe when useful -> gather -> verify -> review when justified -> optional focused follow-up -> close
```

Close completed Agents promptly.

## 11. Failure behavior

### Configuration rejection

Record the exact failure and return to Root. Do not cycle through model IDs or efforts.

### Runtime observation unavailable

If observation is optional, record `not_exposed` and continue from configuration assurance plus deterministic evidence. If observation is required by safety or the acceptance claim, return the affected responsibility to Root and state the limitation.

### Runtime observation mismatch

Quarantine the affected child result. Do not accept useful-looking output from a child whose effective observed route conflicts with the selected route.

### Worker failure

Root may retry the same route only when there is concrete evidence that a deterministic retry is useful. Do not climb a hidden model ladder.

### Policy violation

Reject or quarantine results involving nested delegation, unauthorized writes, scope expansion, credential exposure, or unapproved high-impact side effects.

### Uncertainty

Workers report uncertainty. Root must not convert missing evidence into assumed success.
