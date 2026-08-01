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

Luna Max handles depth and execution. Terra XHigh adds independent judgment. Sol remains focused on high-value control and adjudication.

## Runtime portability

The Skill does not assume that every Codex build exposes the same `spawn_agent` schema. It only uses an exact model/effort route when current runtime evidence supports it.

Portable route resolution:

1. explicit live model/effort override
2. exact parent inheritance when the target equals the current root route and inheritance is documented by the runtime
3. optional custom Agent profile that pins the exact route
4. otherwise return the task to Root

Semantic probes, stale documentation, and model catalogs do not override the current native tool contract.

## Context strategy

Default context inheritance should be minimal.

- Explorer: fresh context whenever possible
- Worker: fresh self-contained task packet by default; inherit recent context only when re-packing would lose material user decisions
- Critic: fresh context by default to preserve independence

## Lifecycle

```text
spawn -> work -> gather -> verify -> close
```

At most one focused follow-up is allowed for incomplete evidence. A completed Worker should be closed promptly so it does not continue consuming a concurrency slot.

## Scope boundary

Core deliberately excludes persistent Task orchestration, App Thread recovery, Worktree scheduling, external DAGs, provider routing, and production deployment automation.
