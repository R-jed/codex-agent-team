# Native Subagent Runtime Contract

Codex Agent Team uses Codex's native `spawn_agent` primitive. A **Subagent** is the delegated actor; an **Agent thread** is the child thread/session where that actor runs.

## Native mechanism

Current Codex represents a spawned child as `SubAgent / ThreadSpawn`:

```text
SessionSource::SubAgent(
  SubAgentSource::ThreadSpawn { ... }
)
```

Conceptually:

```text
main Codex session
└── spawn_agent(...)
    └── Native Subagent
        └── child Codex thread/session
```

The project does not create an App Thread, second user-facing chat, external Agent runtime, persistent DAG, or custom scheduler.

## What Codex Agent Team adds

The native primitive stays the same. The Skill adds policy around when and how to use it.

| Native capability | Agent Team policy |
| --- | --- |
| Generic `spawn_agent` | delegation must satisfy a distinct unresolved dependency |
| Arbitrary task prompt | main session compiles a bounded Delegation Contract |
| Multiple children | Minimum Team and useful-parallelism rules limit fan-out |
| Generic custom roles | namespaced semantic Reader / Worker / Investigator / Advisor roles |
| Context forking | role-specific spawns set `fork_turns` explicitly |
| Child reports | actual artifacts and deterministic evidence gate acceptance |
| Child Subagent capability | project delegation depth stays at 1 |
| Runtime tool permissions | one-writer and read-only evidence rules add safety constraints |

## Semantic roles and exact profile routing

Current project roles are:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

The role name describes responsibility. The model/effort binding is a route policy and may change in a future release without renaming the semantic role.

Model-specific delegation uses only the exact custom project profile. There is no Portable Mode or built-in-role substitution.

Before spawn, the Skill keeps:

```text
preferred_route
configured_route
route_assurance = profile_locked
```

separate from post-spawn runtime evidence.

## Runtime observation

Runtime Truth v2 separates:

```text
route_evidence
ancestry_evidence
permission_evidence
```

Complete route proof requires observed role, model, and effort. A partial observation remains partial.

See `model-route-assurance.md` and the installed `references/runtime-assurance.md`.

## Context and child identity

`fork_turns` controls how much main-session history initializes a child:

```text
none       fresh child context
N          recent N turns
all        full history
```

Role-specific work uses `none` by default because the Delegation Contract carries the task-local facts that the child actually needs.

The main session may pass a small recent-N only when a user decision cannot be safely repacked.

## Evidence instead of repeated history

Fresh context does not mean rediscovering the task from zero.

The main session passes:

- the bounded contract;
- valid established evidence needed by the responsibility;
- the current artifact or unresolved delta;
- explicit items that should not be recomputed when their dependencies are still valid.

Private model reasoning is not propagated as task state.

## Recursion policy

Codex can allow native children to spawn further children. Agent Team deliberately fixes delegation depth at 1:

```text
main session -> child
child -> no further delegation
```

This keeps one control plane and makes evidence ownership, permissions, and acceptance tractable.

## User-facing takeaway

The runtime is native Codex. Agent Team changes the scheduling discipline:

```text
simple work -> main session
bounded execution -> Luna Max
unresolved complex technical delta -> Terra
high-value judgment/review -> Sol
missing exact project profile -> main session
```

These are selectable resources, not mandatory pipeline stages.
