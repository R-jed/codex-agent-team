# Runtime Evidence

Runtime evidence answers three separate questions after a native Subagent is spawned:

```text
route_evidence
ancestry_evidence
permission_evidence
```

Do not collapse missing evidence into a successful boolean merely because no mismatch was observed.

## 1. Configuration and observation are separate

Track configuration facts independently:

```text
preferred_route
configured_route
route_assurance
```

Track only actually observed runtime facts in the evidence objects. Never copy configured values into observed fields.

## 2. Typed evidence

### Route evidence

```text
status: not_observed | partial | matched | conflict
source: none | native | local | both
observed_fields: [agent_role, model, effort]
```

`matched` requires complete observed `agent_role`, `model`, and `effort` for the accepted source path and agreement with expected values.

A native object that exists but omits one or more route fields is `partial`, not `matched`.

### Ancestry evidence

```text
status: not_required | not_observed | matched | conflict
source: none | native | local | both
```

When expected `parent_thread_id` is known, `matched` requires an observed matching parent. Absence is `not_observed`, not `true`.

If native and local sources expose different parent ids, ancestry is `conflict` even when no expected parent was supplied. That conflict does not rewrite an otherwise matched route into route conflict.

### Permission evidence

```text
status: not_required | not_observed | matched | broader_than_required | conflict
source: none | native | local | both
```

A host-enforced read-only claim requires native runtime evidence of effective read-only sandboxing. Local rollout evidence alone cannot establish it.

If native and local sources expose conflicting sandbox or permission-profile values, permission evidence is `conflict`. Route evidence remains independent.

## 3. Compact compatibility grades

The legacy compact grades remain summaries for receipts and compatibility:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

They are derived from complete route evidence:

- `C1`: no complete observed route;
- `L1`: complete matching local route only;
- `R1`: complete matching native route;
- `R2`: complete matching native and local routes that agree;
- `X0`: route, ancestry, source, or required-permission conflict.

A partial native or local record never earns `R1`, `L1`, or `R2` merely because an observation object exists.

## 4. Observation sources

Use the least coupled source that exposes the required fact:

1. Prefer public native spawn/details metadata.
2. Use `scripts/inspect-runtime.py` only when local rollout evidence is useful and available.
3. If a required field is not exposed, report that fact explicitly.

Local rollout records are mutable implementation-coupled telemetry. They are corroborating evidence, not authoritative attestation.

## 5. Deterministic verifier

`scripts/verify-runtime.py` accepts:

```text
expected
native  optional normalized runtime metadata
local   optional normalized local rollout metadata
```

Expected may include:

```text
thread_id
parent_thread_id
agent_role
model
effort
runtime_observation_required
requires_enforced_read_only
```

The verifier returns typed route, ancestry, and permission evidence plus a compact compatibility grade and decision.

If `runtime_observation_required` is true, complete matching native route evidence is required. A native object with missing role/model/effort fields does not satisfy that requirement.

Legacy compatibility fields such as `configuration_match`, `source_agreement`, `ancestry_match`, and `permission_match` are tri-state. They return `null` when the relevant fact was not established. Treat the typed evidence objects as primary.

## 6. Source agreement

When native and local sources both expose the same field, they must agree.

A conflict in role, model, effort, thread identity, parent identity, sandbox, or permission profile produces a conflict state and quarantines the affected result.

Two empty or partial observations do not become `R2` merely because neither contradicts the other. `source_agreement` is `null` when two sources have no overlapping observed field.

## 7. Depth-one ancestry

When the main session knows its thread id, include it as `expected.parent_thread_id`.

```text
matching observed parent -> matched
missing observed parent -> not_observed
mismatched observed parent -> conflict -> quarantine
native/local parent disagreement -> conflict -> quarantine
```

This preserves the distinction between lack of evidence and affirmative ancestry proof.

## 8. Permission evidence

When `requires_enforced_read_only = true`:

```text
native reports read-only -> matched
native reports broader sandbox -> broader_than_required -> quarantine/return
native omits sandbox -> not_observed -> return to main session
local says read-only but native absent -> not_observed -> return to main session
native/local permission evidence conflicts -> conflict -> quarantine
```

Behavioral read-only remains an instruction-level safety path defined in `safety-policy.md`; it does not upgrade runtime permission evidence.

## 9. When to collect runtime evidence

Do not inspect rollout data for every routine child.

Runtime evidence becomes material when:

- safety depends on host-enforced permissions;
- exact route identity is part of the acceptance claim;
- cross-model independence is part of the claim;
- parent-thread identity matters;
- configuration and observed facts conflict;
- the user explicitly asks for proof.

Ordinary bounded work may proceed from `profile_locked` configuration assurance plus deterministic artifact verification when runtime telemetry is not required.

## 10. Failure behavior

```text
configuration route unavailable
-> do not spawn model-specific child

complete native route matches
-> R1, or R2 when complete local evidence also agrees

only complete local route matches
-> L1; never claim native runtime proof

observations partial and optional
-> C1 + typed partial/not_observed states

complete native observation required but missing/partial
-> return to main session

any material conflict
-> X0 + quarantine
```
