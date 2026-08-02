# Runtime Evidence

Runtime evidence strengthens route, ancestry, and permission claims after a native Subagent is spawned. It does not replace configuration-level Route Assurance, and it does not treat mutable local Codex records as authoritative attestation.

## 1. Separate configuration from observation

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
evidence_grade
```

`route_assurance` explains why the requested configuration is trusted before or at spawn time. Observation fields describe only facts actually reported or recorded after spawn.

Never copy preferred or configured values into observed fields.

## 2. Evidence grades

Use explicit grades so the strength of a claim is not hidden behind the word “attestation”.

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

Meanings:

- `C1_configuration_only`: the route is configuration-assured, but no post-spawn observation is available.
- `L1_local_record_observed`: a mutable local Codex rollout record contains matching route facts. This is useful telemetry, not an authoritative runtime receipt.
- `R1_runtime_reported`: the live/public native runtime reports the effective route facts.
- `R2_runtime_reported_and_local_record_agree`: native runtime metadata and the local record independently expose the same facts and agree.
- `X0_conflicted`: an expected fact mismatches observation or two observation sources disagree. Quarantine the affected result.

Reserve stronger terminology such as `runtime_attested` for a future authoritative runtime receipt with semantics that justify that claim.

## 3. Observation sources

Use the least coupled source that exposes the required fact:

1. Prefer public native spawn/details metadata.
2. When required fields are omitted and the local Codex sessions store is accessible, the bundled `scripts/inspect-runtime.py` may read one exact child rollout as a fallback record.
3. If neither source exposes the required fact, record `observation_source = none` and `observation_status = not_exposed`.

When public metadata and local rollout evidence both expose the same field, they must agree.

## 4. Local rollout adapter contract

The bundled inspector is an optional adapter over the current local Codex rollout store. It may stop working when Codex changes its local session format.

The adapter must:

- accept one canonical lowercase child thread UUID;
- locate exactly one rollout filename ending in that UUID;
- reject symlinked rollout files and paths resolving outside the selected sessions root;
- stream JSONL instead of printing arbitrary rollout contents;
- require an exact session id, agent role, model, and reasoning effort;
- reject missing or conflicting required route fields;
- emit only an allowlisted routing and permission object;
- never emit prompts, messages, instructions, environment variables, tokens, configuration payloads, tool arguments, or arbitrary event bodies.

A local rollout record is mutable telemetry. Do not describe it as cryptographic, authoritative, or host-enforced proof.

## 5. Deterministic verifier

Use `scripts/verify-runtime.py` to reconcile normalized expected and observed facts. The verifier accepts:

```text
expected
native  (optional normalized public runtime metadata)
local   (optional normalized local rollout metadata)
```

It deterministically checks:

- expected role/model/effort;
- expected child thread id when known;
- expected parent thread id when known;
- agreement between native and local sources;
- required read-only enforcement;
- whether a required runtime report is actually present.

Output includes:

```text
status
decision
evidence_grade
configuration_match
runtime_reported
local_record_observed
source_agreement
permission_match
ancestry_match
violations
```

Policy decides when verification is required. The verifier decides whether supplied evidence matches.

## 6. Depth-one ancestry

When Root knows its own thread id, include it as `expected.parent_thread_id`.

If an observed child reports another parent:

```text
parent_thread_id mismatch
-> ancestry_match = false
-> quarantine
```

This turns delegation depth from a prompt-only rule into a runtime-verifiable invariant when ancestry metadata is exposed.

## 7. Optional vs required observation

For ordinary bounded work, a valid `profile_locked` or `native_explicit_validated` configuration route remains sufficient to delegate. Missing runtime telemetry may remain `C1_configuration_only`.

Require a native runtime report when:

- safety depends on effective host-enforced read-only isolation;
- a high-consequence conclusion specifically relies on verified cross-model independence;
- the user explicitly asks for proof of the effective child route or permission state;
- available runtime evidence conflicts with the configured route.

A local rollout record alone cannot satisfy a requirement for a native runtime report.

## 8. Permission evidence

A configured `sandbox_mode = "read-only"` remains intent until runtime evidence establishes the effective sandbox.

When native runtime metadata reports read-only isolation:

```text
permission_guarantee = runtime_enforced
```

When only behavioral read-only can be established, keep:

```text
permission_guarantee = instruction_enforced
```

When hard isolation is required and effective read-only is unavailable or broader than requested, return the responsibility to Root.

## 9. Failure behavior

```text
configuration assurance fails
-> do not spawn the model-specific child

runtime report matches
-> record R1 or R2 and continue

only local record matches
-> record L1; never promote it to runtime-reported proof

observation unavailable but optional
-> record C1 and continue

native runtime report required but unavailable
-> return affected responsibility to Root

any source conflict or expected-route mismatch
-> record X0, quarantine result, return to Root
```

Runtime evidence must never create an automatic hidden model ladder or force a larger team.
