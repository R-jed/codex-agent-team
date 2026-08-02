# Runtime Assurance

Runtime assurance strengthens route and permission evidence after a native Subagent is spawned. It does not replace configuration-level Route Assurance and it does not make local Codex implementation details a universal dependency.

## 1. Keep configuration and observation separate

Track these facts independently:

```text
preferred_route
configured_route
route_assurance
observation_source
observed_agent_type
observed_route
observed_sandbox
observed_permission_profile
observation_status
```

`route_assurance` explains why the requested configuration is trusted before or at spawn time. Runtime observation describes only fields actually exposed after spawn.

Allowed observation sources:

```text
native_metadata
local_rollout
none
```

Allowed observation status values:

```text
matched
not_exposed
mismatch
invalid
```

Never copy preferred or configured values into observed fields.

## 2. Observation order

Use the least coupled source that exposes the required fact:

1. Prefer public native spawn/details metadata when the current runtime exposes role, model, effort, sandbox, or permission information.
2. When required fields are omitted and the local Codex sessions store is accessible, the bundled `scripts/inspect-runtime.py` may be used as a read-only fallback for the exact child thread id.
3. If neither source exposes the required fact, record `observation_source = none` and `observation_status = not_exposed`.

When public metadata and local rollout evidence both expose the same field, they must agree. A disagreement is `observation_status = mismatch`; quarantine the affected result and return control to Root.

## 3. Local rollout adapter contract

The bundled inspector is an optional adapter over the current local Codex rollout store. It is not part of the native Subagent runtime and may stop working when Codex changes its local session format.

The adapter must:

- accept one canonical lowercase child thread UUID;
- locate exactly one rollout filename ending in that UUID;
- reject symlinked rollout files and paths resolving outside the selected sessions root;
- stream JSONL instead of printing or copying arbitrary rollout contents;
- require an exact session id, agent role, model, and reasoning effort;
- reject missing or conflicting required route fields;
- emit only an allowlisted routing and permission object;
- never emit prompts, messages, instructions, environment variables, tokens, configuration payloads, tool arguments, or arbitrary event bodies.

Local rollout evidence is implementation-coupled. If its schema is missing, stale, inaccessible, or inconsistent, mark observation unavailable or invalid according to the task's evidence requirement. Do not infer a route from filenames, preferred policy, or profile contents.

## 4. When observation is optional

For ordinary bounded work, a valid `profile_locked` or `native_explicit_validated` route remains sufficient to delegate. Runtime observation is useful evidence when available but its absence does not automatically create another Agent or block the task.

Examples:

- a bounded mechanical implementation;
- repository mapping or search;
- a routine test addition where Root will inspect the diff and rerun deterministic verification.

In these cases:

```text
route_assurance = profile_locked | native_explicit_validated
observation_status = matched | not_exposed
```

Both can be acceptable.

## 5. When observation becomes an acceptance requirement

Require the relevant runtime fact when the safety or claimed independence of the task materially depends on it.

Examples:

- the task requires host-enforced read-only isolation;
- a high-consequence conclusion specifically relies on verified cross-model review;
- current native metadata conflicts with the configured role;
- the user explicitly asks for proof of the effective child route or permission profile.

If the required runtime fact cannot be observed, return the affected responsibility to Root or report that the stronger assurance claim cannot be established. Do not silently weaken the requirement.

## 6. Route matching

For a route observation to match, the observed role, model, and effort must agree with the selected route when those fields are available.

Example:

```text
configured_route = gpt-5.6-luna/max
observed_agent_type = luna_worker
observed_route = gpt-5.6-luna/max
observation_status = matched
```

A different model, effort, or role is a mismatch. Do not accept the child result as correctly routed work even when its output appears useful.

## 7. Permission observation

A configured `sandbox_mode = "read-only"` remains intent until runtime evidence establishes the effective sandbox.

When runtime reports read-only isolation:

```text
permission_guarantee = runtime_enforced
```

When runtime is broader and hard isolation is not required, a critic may proceed only under the behavioral read-only fallback defined in `safety-policy.md`. Keep the guarantee at `instruction_enforced` and report the broader observed sandbox as residual risk.

When hard isolation is required and effective read-only cannot be observed, stop the delegated responsibility with `permission_requirement_unmet`.

## 8. Failure behavior

```text
configuration assurance fails
-> do not spawn the model-specific child

runtime observation matches
-> record evidence and continue

runtime observation unavailable but optional
-> record not_exposed and continue

runtime observation unavailable but required
-> return affected responsibility to Root

runtime observation conflicts
-> quarantine result and return to Root
```

Runtime assurance must never create an automatic hidden model ladder or force a larger team.
