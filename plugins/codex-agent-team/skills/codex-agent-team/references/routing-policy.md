# Routing Policy

## 1. Root-aware control model

The current user-facing Codex session is always `ROOT_CONTROLLER`, regardless of its model.

Root owns user intent, decomposition, architecture, permission decisions, integration, diff acceptance, high-impact decisions, and the final answer.

The Skill never requires a Sol Root and never silently changes the current Root model or reasoning effort.

Role-to-route bindings are stable policy. Team composition is task-aware and dynamic.

## 2. Delegation Gate

A Subagent requires at least one concrete benefit:

- **Context isolation** for noisy source, logs, tests, documentation, or tool output.
- **Real parallelism** for genuinely independent branches.
- **Independent verification** when a consequential result benefits from a fresh reviewer.

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

The baseline orchestration envelope is one Luna responsibility plus, only when Review Gate justifies it, one Terra critic. Sol and larger fan-out remain outside that baseline.

## 4. Route Assurance Gate

Model-specific routing must be grounded in current native configuration evidence before or at spawn. Keep configuration and later observation separate:

```text
preferred_route
configured_route
route_assurance
observed_route
```

A successful exact spawn can establish `configured_route`; `observed_route` may remain `not_exposed`.

### `profile_locked`

The supported Plugin workflow uses Profile Mode as its normal route. `/codex-agent-team` performs the managed first-run readiness flow when a required project role is missing.

Use Profile Mode when an installed custom role pins the exact model and reasoning effort and live role guidance reports those settings as locked.

`profile_locked` is a configuration-assurance state. It does not claim that the effective child route was observed after spawn.

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

A missing project profile never triggers automatic substitution with a built-in role. Complete the managed readiness flow or keep the affected responsibility in Root.

### `native_explicit_validated`

Portable Mode is an internal compatibility path, not a public installation mode and not an automatic fallback for missing project profiles. Use it only when profile-free operation is explicitly required and all of the following hold:

1. live `spawn_agent` exposes `agent_type`, `fork_turns`, `model`, and `reasoning_effort`;
2. the target model is available for the active MultiAgent backend;
3. the selected role is not locked to an incompatible model or effort; and
4. Codex accepts the exact request.

Spawn shape:

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

Treat rejection as `preferred_route_unavailable`.

### Built-in role shadowing

Before Portable Mode uses `explorer`, `worker`, or `default`, inspect live role guidance. A conflicting role lock invalidates the requested Portable route.

### Effective selection precedence

Current Codex resolves model and reasoning settings with this precedence:

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Model and reasoning effort resolve independently. Profile Mode is the normal Plugin path. Portable Mode remains an explicit compatibility path.

### No inheritance-based exact route

Do not treat omission of `model` or `reasoning_effort` as exact assurance. Current Codex may apply configured `agents.default_subagent_model` or `agents.default_subagent_reasoning_effort` before role configuration.

If explicit overrides are hidden and an exact locked profile is unavailable, return the task to Root.

### No automatic cross-role fallback

- Luna execution unavailable does not turn Terra into an implementation Worker.
- Terra critic unavailable means Root reviews without claiming independent Terra verification.
- Sol Senior Judge unavailable means Root keeps control and reports the limitation.
- An unused role being unavailable does not block responsibilities that do not depend on it.

## 5. Runtime Evidence Gate

After spawn, use `runtime-assurance.md` when effective route, ancestry, or permission evidence matters.

Evidence grades are:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

A local rollout record is mutable telemetry. `L1` never becomes a runtime-reported claim merely because it matches the configured route.

Prefer public native metadata. Use the bundled local rollout inspector only as a read-only fallback record. Use `scripts/verify-runtime.py` to compare expected facts and supplied normalized observations.

For ordinary bounded work, configuration assurance remains sufficient and missing runtime telemetry may stay `not_exposed` / `C1_configuration_only`.

Require a native runtime report when:

- safety depends on effective host-enforced read-only isolation;
- a high-consequence conclusion specifically relies on verified cross-model independence;
- the user explicitly requests proof of effective route or permission state; or
- available runtime evidence conflicts with the configured route.

If two observation sources expose the same field, require agreement. A mismatch produces `X0_conflicted` and quarantines the affected result.

When Root knows its own thread id, pass it as the expected `parent_thread_id`. A mismatch is an ancestry violation and quarantines the child result.

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

Use for repository mapping, symbol discovery, caller tracing, test mapping, documentation extraction, large read-only investigations, and evidence collection. This default is a policy hypothesis to be tested on representative workloads; do not infer optimality from model price alone.

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

Add one Terra critic when fresh judgment has concrete acceptance value, especially for security/permissions, concurrency/state consistency, cross-module invariants, public contracts, migrations, weak deterministic oracles, material Worker `judgment_calls`, or conflicting evidence.

The critic returns:

```text
review_status: clear | findings | insufficient_evidence
findings
residual_risk
```

Root still owns final acceptance. For bounded findings, correct the work and rerun deterministic verification. Run a fresh Terra review only when the correction materially changes the risk that justified detached review.

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

```text
spawn -> work -> observe when useful -> gather -> verify -> review when justified -> optional focused follow-up -> close
```

Close completed Agents promptly.

## 11. Failure behavior

### Configuration rejection

Record the exact failure and return to Root. Do not cycle through model IDs or efforts.

### Runtime observation unavailable

If observation is optional, record `C1_configuration_only` and continue from configuration assurance plus deterministic evidence. If a native report is required by safety or the acceptance claim, return the affected responsibility to Root.

### Runtime observation mismatch

Record `X0_conflicted` and quarantine the affected child result.

### Worker failure

Root may retry the same route only when there is concrete evidence that a deterministic retry is useful. Do not climb a hidden model ladder.

### Policy violation

Reject or quarantine results involving nested delegation, wrong parent-thread identity, unauthorized writes, scope expansion, credential exposure, or unapproved high-impact side effects.

### Uncertainty

Workers report uncertainty. Root must not convert missing evidence into assumed success.
