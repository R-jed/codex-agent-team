# Runtime Evidence

Runtime evidence answers three separate questions after a native Subagent is spawned:

```text
route_evidence
ancestry_evidence
permission_evidence
```

Missing evidence is never success merely because no mismatch was observed.

## 1. Keep configuration separate from observation

Before spawn, configuration assurance may record:

```text
preferred_route
configured_route
route_assurance = profile_locked
```

After spawn, record only facts the runtime or another explicitly supplied observation source actually exposed. Never copy configured role/model/effort or sandbox intent into observed fields.

## 2. Typed evidence

### Route

```text
status: not_observed | partial | matched | conflict
source: none | native | local | both
observed_fields: [agent_role, model, effort]
```

`matched` requires both a complete expected route and a complete observed `agent_role`, `model`, and `effort` tuple that agrees with it. An incomplete expected tuple is invalid input. An incomplete observed tuple is `partial` or `not_observed`.

### Ancestry

```text
status: not_required | not_observed | matched | conflict
source: none | native | local | both
```

When `parent_thread_id` matters, absence remains `not_observed`. Native/local parent disagreement is a typed ancestry conflict and does not relabel an otherwise matched route as a route conflict.

### Permission

```text
status: not_required | not_observed | matched | broader_than_required | conflict
source: none | native | local | both
```

A host-enforced read-only claim requires native evidence of the effective sandbox. A local or reconstructed record can corroborate native evidence but cannot establish host-enforced read-only by itself.

## 3. One deterministic verifier

The bundled verifier is resolved from the installed Skill directory:

```text
skill_dir=<directory-containing-this-SKILL.md>
runtime_verifier="$skill_dir/../../scripts/runtime-evidence.py"
```

Run it with normalized JSON on stdin or with `--input <case.json>`:

```bash
python "$runtime_verifier" --input <case.json>
```

Input shape:

```json
{
  "expected": {
    "agent_role": "codex_delegate_worker",
    "model": "gpt-5.6-luna",
    "effort": "max",
    "thread_id": "optional expected child id",
    "parent_thread_id": "optional expected parent id",
    "runtime_observation_required": false,
    "requires_enforced_read_only": false
  },
  "native": {
    "agent_role": "observed when exposed",
    "model": "observed when exposed",
    "effort": "observed when exposed",
    "thread_id": "observed when exposed",
    "parent_thread_id": "observed when exposed",
    "sandbox_policy_type": "observed when exposed",
    "permission_profile_type": "observed when exposed"
  },
  "local": null
}
```

`native` and `local` are optional normalized observations. Codex Delegate no longer ships a rollout-file inspector. If another source is used for `local`, the caller owns collecting and sanitizing it. Runtime internals are intentionally not scraped by this project.

The verifier returns typed route, ancestry, and permission evidence plus the compact compatibility grade:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

A partial record never earns `L1`, `R1`, or `R2`.

## 4. Source rules

Prefer public native spawn/details metadata whenever the required fact is exposed. An optional `local` observation is corroborating evidence only.

When two supplied sources expose the same field, disagreement is a material conflict. Keep conflicts typed by concern:

- role/model/effort disagreement -> route conflict;
- parent disagreement -> ancestry conflict;
- sandbox/permission disagreement -> permission conflict;
- child thread identity disagreement -> identity conflict.

A conflict quarantines the affected result, but one concern must not be rewritten as another concern merely to produce one global failure flag.

## 5. When runtime evidence is required

Do not demand runtime telemetry for every routine child. It becomes material when:

- safety depends on host-enforced read-only;
- exact post-spawn route identity is part of the acceptance claim;
- cross-model independence is part of a required Final Review claim;
- parent-thread identity is material to the depth-one claim;
- configured and observed facts conflict;
- release validation is characterizing native capacity, lifecycle, or observability;
- the user explicitly requests runtime proof.

Ordinary bounded work may proceed from exact profile configuration assurance plus deterministic artifact verification when post-spawn runtime proof is not part of the acceptance claim.

## 6. Failure behavior

```text
incomplete expected agent_role/model/effort
-> invalid verifier input; fail closed

configuration route unavailable
-> do not spawn the model-specific child

complete matching native route
-> R1, or R2 when complete local corroboration also agrees

only complete matching local route
-> L1; never claim native runtime proof

partial observations and runtime proof optional
-> C1 + typed partial/not_observed states

runtime observation required but native route missing/partial
-> return to main session

required read-only but native sandbox missing
-> return to main session

broader required sandbox or any material conflict
-> X0 + quarantine
```
