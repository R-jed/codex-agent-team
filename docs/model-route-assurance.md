# Model Route Assurance

Codex Agent Team uses model-specific Subagents only when it can establish a concrete assurance path for both the model and the reasoning effort.

## Why this exists

A routing table that says “Luna Max” is useful only if the native runtime can actually execute `gpt-5.6-luna` with `max` reasoning. The Skill therefore separates four facts:

```text
preferred_route   what the policy wants
configured_route  what the accepted native configuration path targets
route_assurance   why that configuration is trusted
observed_route    what the runtime explicitly reports after spawn
```

Current MultiAgentV2 does not expose a universal child model/effort receipt in spawn or list output, so `observed_route = not_exposed` is the normal state. The Skill does not relabel requested or configured settings as observed settings.

## Assurance path 1: Profile Locked

This is the strongest optional path.

A custom Agent profile pins model and reasoning effort:

```toml
name = "luna_worker"
model = "gpt-5.6-luna"
model_reasoning_effort = "max"
```

Current Codex role handling applies a role layer at high precedence. Its spawn tool description can report that a role's model/effort is fixed and cannot be changed.

When the live `spawn_agent` surface exposes `agent_type` and the live role guidance confirms the exact lock, the Skill records:

```text
route_assurance = profile_locked
```

Profile Mode omits competing explicit `model` and `reasoning_effort` fields.

## Assurance path 2: Native Explicit Validated

Portable Mode works without installing profiles.

The Skill explicitly requests:

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

Current Codex validates the requested model against the available models for the active MultiAgent backend and validates the requested effort against that model's supported reasoning levels before spawning.

The Skill additionally checks live role guidance because user-defined roles can shadow built-in names. If `worker`, `explorer`, or `default` is locked to an incompatible route, the explicit route is rejected by policy.

After the native spawn accepts the exact tuple, record:

```text
route_assurance = native_explicit_validated
```

## Effective precedence in current Codex

OpenAI's current Subagents documentation defines the effective selection order for each setting:

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Model and reasoning effort are resolved independently. This is why Profile Mode and Portable Mode are alternative assurance paths instead of two sources that should be mixed in one spawn.

## Why inheritance is not an assurance path

Omitting model/effort can look like a convenient way to inherit Root. Current Codex also supports configured default Subagent model/effort values (`agents.default_subagent_model` and `agents.default_subagent_reasoning_effort`), so omission does not prove exact inheritance.

For model-specific policy routes, Codex Agent Team therefore requires Profile Locked or Native Explicit Validated. If neither is available, the child task stays in Root.

## Failure rule

```text
exact route provable -> spawn
exact route rejected -> Root
exact route unprovable -> Root
```

The Skill does not silently substitute Terra for Luna, Sol for Terra, or another reasoning effort.
