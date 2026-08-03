# Native Subagent Runtime Contract

Codex Delegate uses Codex's native `spawn_agent` primitive. A **Subagent** is the delegated actor; an **Agent thread** is the child thread/session where that actor runs.

## Native mechanism

Current Codex represents a spawned child as `SubAgent / ThreadSpawn`.

Conceptually:

```text
main Codex session
└── spawn_agent(...)
    └── Native Subagent
        └── child Codex thread/session
```

The project does not create a second user-facing chat, external Agent runtime, persistent DAG service, background scheduler, or custom thread pool.

## What Codex Delegate adds

The native primitive stays the same. Codex Delegate adds policy around when and how to use it.

| Native capability | Codex Delegate policy |
| --- | --- |
| Generic `spawn_agent` | every call must satisfy a distinct ready dependency |
| Arbitrary task prompt | main session compiles a bounded Delegation Contract |
| Multiple children | ready-frontier scheduling + consent + workspace safety decide useful fan-out |
| Native slot capacity | observed runtime fact; excess ready work queues instead of changing role identity |
| Generic custom roles | namespaced semantic Reader / Worker / Investigator / Advisor roles |
| Context forking | role-specific spawns set `fork_turns` explicitly; clean restarts prefer fresh context |
| Child reports | actual artifacts and deterministic evidence gate acceptance |
| Child Subagent capability | project delegation depth stays at 1 |
| Runtime tool permissions | one-writer and read-only evidence rules add safety constraints |

## Adaptive child scheduling

Codex Delegate does not define a product hard child count.

The main session maintains a Dependency Ledger and selects from its ready frontier. Explicit `/codex-delegate` use permits up to two concurrently active justified children without another consent prompt. Larger simultaneous fan-out normally requires consent unless already authorized.

After consent, actual concurrency is bounded by:

```text
justified ready dependencies
workspace write safety
exact role availability
native runtime child capacity
```

If the runtime exposes fewer slots than the ready frontier, remaining dependencies stay pending until capacity becomes available.

A runtime capacity value such as 4, 6, or another number is version-scoped runtime evidence. It must not become a permanent Codex Delegate architecture constant without an independent product reason.

## Semantic roles and exact profile routing

Current project roles are:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

The role name describes responsibility. The model/effort binding is route policy and may change in a future release without renaming the semantic role.

Model-specific delegation uses only the exact custom project profile. There is no Portable Mode or built-in-role substitution.

Before spawn, the Skill keeps:

```text
preferred_route
configured_route
route_assurance = profile_locked
```

separate from post-spawn runtime evidence.

## Runtime observation

Runtime Truth separates:

```text
route_evidence
ancestry_evidence
permission_evidence
```

Exact route proof requires a complete expected role/model/effort tuple and a complete matching observed role/model/effort tuple. Incomplete expectations fail closed; partial observations stay partial.

Native capacity and lifecycle behavior are separate runtime observations. Observing N successful simultaneous children proves only that the tested build/environment supported at least that tested pattern. It does not prove a universal maximum.

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

A clean same-lane restart also prefers `fork_turns=none`. It carries current artifacts, valid evidence, failure signature, unresolved delta, acceptance, and `DO NOT REDO` items while dropping dead-end narration and private reasoning.

## Evidence instead of repeated history

Fresh context does not mean rediscovering the task from zero.

The main session passes:

- the bounded dependency contract;
- valid established evidence needed by the responsibility;
- current artifact or unresolved delta;
- current deterministic failure signature when relevant;
- explicit items that should not be recomputed while their dependencies remain valid.

Private model reasoning is not propagated as task state.

## Execution progress

Native thread completion does not prove task progress.

The main session evaluates progress from artifacts, deterministic verification, repository facts, and whether the unresolved dependency materially narrows.

Repeated completion with the same failure signature and no new evidence is an execution-stall signal. Codex Delegate has no universal retry count and does not resend unchanged contracts merely because a child completed unsuccessfully.

See the installed `references/execution-progress.md`.

## Recursion policy

Codex can allow native children to spawn further children. Codex Delegate deliberately fixes delegation depth at 1:

```text
main session -> child
child -> no further delegation
```

This keeps one control plane and makes evidence ownership, permissions, and acceptance tractable.

## Workspace scope

Native child capacity and write safety are independent constraints.

One canonical physical checkout has at most one active Writing Worker even if the runtime has many available child slots. Multiple writers require genuinely isolated workspaces or runtime-backed worktrees.

Read-only children may fan out across independent dependencies when consent and runtime capacity permit.

## User-facing takeaway

The runtime is native Codex. Codex Delegate changes the delegation discipline:

```text
no useful delegated dependency -> main session
bounded execution -> Luna Max
unresolved complex technical delta -> Terra
high-value judgment/review -> Sol
missing exact project profile -> main session
more ready work than native slots -> queue remaining dependencies
```

These are selectable resources, not mandatory pipeline stages or a fixed-size team.
