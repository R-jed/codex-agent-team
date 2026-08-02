# Model Route Assurance

Codex Agent Team uses model-specific Subagents only when it can establish a concrete configuration-assurance path for both model and reasoning effort. Post-spawn evidence is a separate layer.

## Why this exists

A routing table that says “Luna Max” is useful only if the native runtime can accept a route to `gpt-5.6-luna` with `max` reasoning. The Skill therefore separates four facts:

```text
preferred_route   what policy wants
configured_route  what the accepted native configuration path targets
route_assurance   why that configuration is trusted
observed_route    what post-spawn evidence actually reports or records
```

A configuration-level assured route never becomes observed telemetry merely because spawn succeeded.

## Assurance path 1: Profile Locked

A custom Agent profile pins model and reasoning effort:

```toml
name = "luna_worker"
model = "gpt-5.6-luna"
model_reasoning_effort = "max"
```

When the live `spawn_agent` surface exposes `agent_type` and live role guidance confirms the exact lock, record:

```text
route_assurance = profile_locked
```

`profile_locked` is the stable policy identifier for a configuration lock. It does not mean the child route has been independently observed after spawn.

Profile Mode omits competing explicit `model` and `reasoning_effort` fields.

## Assurance path 2: Native Explicit Validated

Portable Mode works without installing profiles.

When the live `spawn_agent` surface exposes `agent_type`, `fork_turns`, `model`, and `reasoning_effort`, the Skill can explicitly request:

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

The Skill also checks live role guidance because user-defined roles can shadow built-in names. After the native spawn accepts the exact tuple, record:

```text
route_assurance = native_explicit_validated
```

This proves the request was accepted through the exposed configuration surface. Post-spawn runtime identity still belongs to the runtime-evidence layer.

## Effective precedence in current Codex

OpenAI's current Subagents documentation defines the effective selection order for each setting:

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Model and reasoning effort are resolved independently. Profile Mode and Portable Mode are alternative assurance paths.

## Why inheritance is not an assurance path

Omitting model/effort can look like a convenient way to inherit Root. Current Codex also supports configured default Subagent values (`agents.default_subagent_model` and `agents.default_subagent_reasoning_effort`), so omission does not prove exact inheritance.

For model-specific policy routes, Codex Agent Team therefore requires Profile Locked or Native Explicit Validated. If neither is available, the child task stays in Root.

## Post-spawn evidence

Runtime evidence is graded separately:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

A local rollout record is mutable implementation-coupled telemetry. It may corroborate a runtime report but cannot establish `R1_runtime_reported` by itself.

Use the installed Skill reference `references/runtime-assurance.md` and deterministic `scripts/verify-runtime.py` for expected-vs-observed reconciliation, source agreement, parent-thread identity, and effective read-only requirements.

## Failure rule

```text
exact configuration route provable -> spawn may proceed
exact configuration route rejected -> Root
exact configuration route unprovable -> Root
post-spawn evidence conflicts -> quarantine
native report required but unavailable -> Root
```

The Skill does not silently substitute Terra for Luna, Sol for Terra, or another reasoning effort.
