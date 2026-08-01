# Architecture

Codex Agent Team is a root-aware native Subagent policy layer.

## Control model

The current Codex session is always the Root Controller. The Skill never requires Sol as the root model.

Logical roles:

| Role | Default route | Responsibility |
| --- | --- | --- |
| ROOT_CONTROLLER | current session | intent, planning, architecture, risk, integration, final answer |
| EXECUTION_WORKER | GPT-5.6 Luna Max | context-heavy exploration, bounded implementation, debugging, testing |
| INDEPENDENT_CRITIC | GPT-5.6 Terra XHigh | detached review, synthesis, conflicting evidence, assumption challenge |
| SENIOR_JUDGE | GPT-5.6 Sol High | one-off high-consequence adjudication when Root is not Sol and the user consents |

## Decision sequence

```text
Root task
  -> Delegation Gate
  -> Capability Gate
  -> Role Router
  -> Consent Gate when a material boundary changes
  -> Execute
  -> Evidence Gate
  -> Close Workers
  -> Root integration
```

## Why role routing

A difficulty ladder creates unstable behavior as model pricing and capabilities change. Codex Agent Team routes by the cognitive role the task needs.

Luna Max handles execution depth and high-context work. Terra XHigh adds detached judgment. Sol remains focused on high-value control and adjudication.

## Two mutually exclusive spawn modes

### Portable Mode

Use built-in native roles and explicit model/effort overrides when the current `spawn_agent` schema exposes them.

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

### Profile Mode

Use a custom Agent profile that pins model/effort. Do not also send competing explicit model/effort overrides.

```text
agent_type = luna_worker
fork_turns = none
```

This separation matters because Codex applies Agent role/profile configuration after explicit spawn model overrides. A route-pinning profile can therefore become the effective source of model/effort.

## Runtime portability

The Skill does not assume that every Codex build exposes the same `spawn_agent` schema. Role-specific delegation requires the live `agent_type` and `fork_turns` surface; Portable Mode also requires the exact model/effort override surface when it depends on those fields.

Route resolution:

1. required live role/context-fork surface, then explicit live model/effort override for Portable Mode
2. exact parent inheritance when the target equals the current Root route and inheritance is documented by the runtime
3. optional custom Agent profile that pins the exact route
4. otherwise return the task to Root

Semantic probes, stale documentation, and model catalogs do not override the current native tool contract.

## Context strategy

Role-specific spawns always set `fork_turns` explicitly because current MultiAgentV2 defaults omitted `fork_turns` to full history.

- Explorer: `fork_turns = "none"`
- Worker: `fork_turns = "none"` by default; recent positive integer only when task-local re-packing would lose material decisions
- Critic: `fork_turns = "none"`
- Never combine `fork_turns = "all"` with `agent_type` on MultiAgentV2

## Permission semantics

Custom Agent profiles can declare sandbox defaults, but the live parent Turn's effective permission profile and approval policy are runtime-owned values. The Skill therefore treats actual child permissions as runtime facts.

A profile saying `sandbox_mode = "read-only"` is useful intent metadata, but it is not sufficient evidence for `permission_guarantee = runtime_enforced`.

## Lifecycle

```text
spawn -> work -> gather -> verify -> close
```

At most one focused follow-up is allowed for incomplete evidence. A completed Worker should be closed promptly so it does not continue consuming a concurrency slot.

## Scope boundary

Core deliberately excludes persistent Task orchestration, App Thread recovery, Worktree scheduling, external DAGs, provider routing, and production deployment automation.
