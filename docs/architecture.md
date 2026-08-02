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

The role table stays deliberately narrow. Terra is not a default implementation escalation lane, and Sol is not a mandatory final reviewer.

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
  -> Runtime Observation when useful or required
  -> Evidence Gate
  -> Review Gate when detached judgment has concrete value
  -> Close Subagent
  -> Root integration and acceptance
```

Minimum Team remains upstream of every later gate. Runtime observation and review strengthen evidence; they do not justify delegation by themselves.

## Route assurance

Model-specific children use only provable configuration routes. The Skill keeps these facts separate:

```text
preferred_route
configured_route
route_assurance
observed_route
```

A successful exact spawn can establish a configuration-level assured route. The architecture never upgrades configuration assurance into a claim of runtime-observed telemetry.

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

See `model-route-assurance.md` for details.

## Runtime observation

Post-spawn observation is a separate evidence layer:

```text
observation_source: native_metadata | local_rollout | none
observation_status: matched | not_exposed | mismatch | invalid
```

Public native metadata is preferred. The installed Skill also carries an optional standard-library `scripts/inspect-runtime.py` adapter for environments where public child details omit model or effort but the local Codex rollout store is accessible.

The adapter emits only allowlisted route and permission metadata for one exact thread id. It is an implementation-coupled fallback and never becomes a universal dependency.

Ordinary bounded work may accept `not_exposed` after a valid configuration route. Runtime observation becomes an acceptance requirement when the task depends on effective host-enforced read-only isolation, verified high-consequence cross-model independence, or an explicit user request for effective-route proof.

See `skill/codex-agent-team/references/runtime-assurance.md` for the installed policy.

## Context strategy

Role-specific spawns always set `fork_turns` explicitly.

- Explorer: `none`
- Critic: `none`
- Worker: `none` by default, positive recent-N only when required

This avoids accidental full-history inheritance and preserves detached review.

## Implementation contract

Bounded coding work can use the Task Packet Implementation Preset:

```text
OBJECTIVE
OWNERSHIP
INTERFACES
CONSTRAINTS
VERIFICATION
STOP CONDITIONS
RETURN
```

Workers return `judgment_calls` so Root can identify decisions that were not mechanically determined by the packet. Worker reports remain claims; Root inspects actual changes and reruns deterministic verification.

## Review model

Independent review is risk-triggered.

A Terra critic is added when detached judgment materially improves acceptance, such as security or permission logic, concurrency or state consistency, public contracts, migrations, broad cross-module invariants, weak deterministic oracles, material Worker judgment calls, or conflicting evidence.

The critic returns `clear`, `findings`, or `insufficient_evidence`. Root retains final acceptance authority. A remaining high-consequence disagreement may reach one consent-gated Sol Senior Judge when Root is not already Sol.

This preserves producer, critic, and judge separation without imposing a mandatory final-review tax on small changes.

## Permission semantics

Custom Agent profiles may declare sandbox defaults, but effective child permissions are runtime facts. A profile declaring `sandbox_mode = "read-only"` is useful intent metadata; it is not proof of effective runtime enforcement.

When safety depends on enforced read-only access, the Skill requires runtime evidence before accepting delegated review.

When hard isolation is not required and the host broadens a critic's sandbox, the Safety Policy permits a behavioral read-only fallback only with explicit no-write instructions and verified before/after repository or artifact state. That path remains `instruction_enforced` and reports the broader sandbox as residual risk.

## Lifecycle

```text
spawn -> work -> observe when useful -> gather -> verify -> review when justified -> optional focused follow-up -> close
```

At most one focused follow-up is allowed for incomplete evidence. Completed Subagents are closed promptly.

## Installation integrity

The repository installer validates shipped Skill/profile sources, preflights destination conflicts before mutation, refuses symlinked locked-profile destinations, stages the Skill, creates only missing exact locked profiles, verifies the final installed state, and supports a non-mutating `--check` mode.

Profile conflicts remain fail-closed. The installer does not silently overwrite a differing user-owned locked role.

## Scope boundary

Core deliberately excludes persistent Task orchestration, App Thread recovery, Worktree scheduling, external DAGs, provider routing, mandatory all-task review, and production deployment automation.
