# Native Subagent Runtime Contract

This document answers two practical questions:

1. How does Codex Agent Team make a requested model and reasoning effort actually land on the child?
2. What does the Skill create when it delegates work?

## 1. The Skill creates Native Subagents

Codex Agent Team calls Codex's native `spawn_agent` tool. OpenAI's Codex documentation defines a **Subagent** as a delegated agent started for a specific task and an **Agent thread** as the thread where that Subagent does its work.

That means “Subagent” and “child task session/thread” describe different layers of the same native mechanism. The Subagent is the delegated actor; the child thread is its runtime container.

Current Codex marks the created child as `SubAgent / ThreadSpawn`:

```text
SessionSource::SubAgent(
  SubAgentSource::ThreadSpawn { ... }
)
```

Conceptually:

```text
Root Codex session
└── spawn_agent(task_name="auth_fix", ...)
    └── Native Subagent: /root/auth_fix
        └── backed internally by a child Codex thread/session
```

The child thread/session is the runtime container for the Subagent. The Skill does not create an App Thread, a second user-facing chat, a custom task scheduler, or an external agent framework.

## 2. How this differs from plain Codex Subagent use

The runtime primitive is the same. Codex Agent Team adds an opinionated operating policy around it.

| Native Codex capability | Codex Agent Team policy |
| --- | --- |
| Generic `spawn_agent` | Delegation Gate decides whether a child has concrete value |
| Model may inherit or be explicitly overridden | Route Assurance permits only provable model/effort paths |
| Generic roles | Luna Max execution, Terra XHigh critic, Sol High judge |
| `fork_turns` can default to full history | Role-specific spawns set it explicitly |
| Native children can have Subagent tools | Skill fixes delegation depth to 1 |
| Multiple children are possible | Minimum Team limits default fan-out |
| Runtime permissions govern tools | One Writer and permission guarantees add policy constraints |
| Child result returns to Root | Evidence contract and deterministic verification gate acceptance |
| Powerful operations are possible | Consent Gate and high-impact actions stay with Root |

Codex Agent Team does not replace Codex Subagents. It makes native delegation more repeatable, model-aware, context-aware, and auditable.

## 3. Model and effort assurance

The Skill separates:

```text
preferred_route   what policy wants
configured_route  what exact native path was accepted
route_assurance   why the exact configuration is trusted
observed_route    what runtime explicitly reports after spawn
```

Current MultiAgentV2 spawn/list output does not expose a universal effective child model/reasoning receipt, so post-spawn observation is usually unavailable. This means the current guarantee is configuration-level: the exact route is locked or accepted by the native configuration path, while runtime observation remains separate.

Allowed `route_assurance` states:

### `profile_locked`

A custom role such as `luna_worker` pins the exact model and effort, and live role guidance confirms those values are locked.

### `native_explicit_validated`

Portable Mode explicitly sends model + effort. Current Codex validates the requested model against the available MultiAgent models and validates reasoning effort against the selected model before spawning. The Skill also confirms the selected role is not locked to an incompatible route.

If neither `profile_locked` nor `native_explicit_validated` can establish the exact tuple, keep the task in Root with `preferred_route_unavailable`.

The Skill does not use inherited model/effort as proof of an exact route because Codex can apply configured default Subagent model/effort values when request fields are omitted.

## 4. Why role shadowing matters

Current Codex lets user-defined Agent roles shadow built-in names. A user configuration can therefore redefine `worker`, `explorer`, or `default`.

Portable Mode inspects live role guidance before using a built-in name. If that role is locked to a different model or reasoning effort, the requested route is rejected by policy.

Profile Mode avoids this ambiguity by using project-specific names:

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

## 5. Context and child identity

MultiAgentV2 assigns the Subagent a canonical task path such as `/root/auth_fix` and internally a child thread ID.

`fork_turns` controls how much parent history initializes that child:

```text
none       fresh child context
N          recent N turns
all        full history
```

Codex Agent Team uses `none` by default for role-specific work. This keeps exploration and detached review isolated from Root history.

## 6. Recursion policy

Codex's native Subagent tool can give spawned Agents the ability to create additional Subagents. Codex Agent Team deliberately does not use that freedom.

```text
Root -> child
child -> no further delegation
```

The Skill keeps delegation depth at 1 so Root remains the single coordinator and final integration point.

## 7. User-facing takeaway

Codex already has a capable Native Subagent engine. Codex Agent Team adds a stable contract for how that engine is used:

```text
simple work -> Root
heavy bounded execution -> Luna Max
important detached judgment -> Terra XHigh
rare high-consequence adjudication -> Sol High after consent
unprovable route -> Root
```
