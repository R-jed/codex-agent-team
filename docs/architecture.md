# Architecture

Codex Agent Team is a Root-aware policy layer over Codex Native Subagents.

## Control model

The current user-facing Codex session is always the Root Controller. The Skill never requires a Sol Root and never creates a second orchestration runtime.

Logical roles:

| Role | Default route | Responsibility |
| --- | --- | --- |
| ROOT_CONTROLLER | current session | intent, planning, architecture, risk, integration, final answer |
| EXECUTION_WORKER | GPT-5.6 Luna Max | context-heavy exploration, bounded implementation, debugging, testing |
| INDEPENDENT_CRITIC | GPT-5.6 Terra XHigh | detached review, synthesis, conflicting evidence, assumption challenge |
| SENIOR_JUDGE | GPT-5.6 Sol High | one-off high-consequence adjudication when Root is not Sol and the user consents |

## Native runtime, not a parallel thread system

The Skill calls Codex Native `spawn_agent`.

Internally, Codex backs each Subagent with a child thread and a canonical Agent path such as `/root/auth_fix`. That child thread is the Subagent's runtime container. Codex Agent Team does not call an App Thread `create_thread` API, manage an external DAG, or maintain a separate scheduler.

See [`native-subagent-runtime.md`](native-subagent-runtime.md) for the runtime distinction and the policy differences from plain native Subagent usage.

## Decision sequence

```text
Root task
  -> Delegation Gate
  -> Route Assurance Gate
  -> Role Router
  -> Consent Gate when a material boundary changes
  -> Execute Native Subagent
  -> Evidence Gate
  -> Close Subagent
  -> Root integration
```

## Route assurance

Model-specific children use only provable routes. The Skill keeps these facts separate:

```text
preferred_route
configured_route
route_assurance
observed_route
```

A successful exact spawn can establish a configuration-level assured route. Current MultiAgentV2 does not expose a universal post-spawn model/effort receipt, so `observed_route = not_exposed` is valid. The architecture never upgrades configuration assurance into a claim of runtime-observed telemetry.

### Profile Mode

Preferred when an installed custom Agent role pins the intended model and reasoning effort and the live role guidance confirms the lock.

```text
route_assurance = profile_locked
```

### Portable Mode

Uses a built-in role plus explicit model/effort only when the live `agent_type` and `fork_turns` surface is available, model/effort overrides are exposed, and the selected role is not locked to an incompatible route. Current Codex validates the requested model and supported effort before spawn.

```text
route_assurance = native_explicit_validated
```

### No exact inheritance assumption

The Skill does not treat omitted model/effort as exact assurance because Codex can apply configured default Subagent model/effort values. If no exact profile or explicit route is provable, the child task returns to Root.

Current MultiAgentV2 spawn and list output do not expose a universal child model/effort receipt, so `observed_route = not_exposed` remains valid unless a future runtime adds that telemetry.

See `model-route-assurance.md` for details.

## Context strategy

Role-specific spawns always set `fork_turns` explicitly.

- Explorer: `none`
- Critic: `none`
- Worker: `none` by default, positive recent-N only when required

This avoids accidental full-history inheritance and preserves detached review.

## Permission semantics

Custom Agent profiles may declare sandbox defaults, but effective child permissions are runtime facts. A profile declaring `sandbox_mode = "read-only"` is useful intent metadata; it is not proof of effective runtime enforcement.

When safety depends on enforced read-only access, the Skill requires runtime evidence before delegation.

## Lifecycle

```text
spawn -> work -> gather -> verify -> optional focused follow-up -> close
```

At most one focused follow-up is allowed for incomplete evidence. Completed Subagents are closed promptly.

## Scope boundary

Core deliberately excludes persistent Task orchestration, App Thread recovery, Worktree scheduling, external DAGs, provider routing, and production deployment automation.
