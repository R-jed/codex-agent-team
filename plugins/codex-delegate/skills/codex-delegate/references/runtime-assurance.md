# Runtime Evidence

Runtime evidence keeps configured intent separate from what the current Codex runtime actually exposed. Routing V4 uses the same bundled verifier for two subjects:

```text
main_session
child
```

Missing evidence remains missing.

## 1. Main-session route evidence

Main-session model identity affects compute placement for material judgment, but it never changes main-session authority.

When trusted current-session or host metadata exposes model and effort, normalize it with:

```json
{
  "subject": "main_session",
  "native": {
    "model": "gpt-5.6-sol",
    "effort": "high"
  },
  "local": null
}
```

The verifier returns:

```text
main_judgment_coverage: covered | uncovered | unknown
coverage_source: trusted_session_metadata | not_observed
observed_main_model
observed_main_effort
```

For the current Routing V4 contract, complete native metadata identifying the GPT-5.6 Sol family yields `covered`; complete native metadata identifying another family yields `uncovered`; missing, partial, local-only, or conflicting evidence yields `unknown`.

This is intentionally conservative. A configured child profile, repository file, child statement, or cached assumption cannot prove which model owns the current main session.

Main-session coverage is used only to avoid redundant capability-uplift Sol calls. It does not satisfy fresh independent Final Review.

## 2. Child route/safety evidence

Child mode retains exact route reconciliation:

```json
{
  "subject": "child",
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

Child route evidence is typed independently from ancestry and permission evidence.

### Route

```text
status: not_observed | partial | matched | conflict
source: none | native | local | both
```

`matched` requires a complete expected `agent_role/model/effort` tuple and a complete agreeing observation.

### Ancestry

```text
status: not_required | not_observed | matched | conflict
```

When parent identity matters, absence remains `not_observed`.

### Permission

```text
status: not_required | not_observed | matched | broader_than_required | conflict
```

A host-enforced read-only claim requires native evidence of effective sandbox behavior. Local reconstruction can corroborate but cannot establish host enforcement.

## 3. Deterministic verifier

Resolve it relative to the installed Skill:

```text
skill_dir=<directory-containing-this-SKILL.md>
runtime_verifier="$skill_dir/../../scripts/runtime-evidence.py"
```

Run:

```bash
python "$runtime_verifier" --input <case.json>
```

or pipe normalized JSON to stdin.

The compact grades remain:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

A partial observation never earns `R1` or `R2`.

## 4. When evidence is material

Do not require runtime telemetry for every routine child.

Main-session route evidence becomes material when the route decision depends on whether Sol judgment is already covered. If the main route is not exposed, keep `main_judgment_coverage = unknown` and use the Routing V4 unknown-coverage rules. Do not invent a route merely to save compute.

Child runtime evidence becomes material when:

- hard host-enforced read-only matters;
- exact post-spawn model/role/effort is part of an acceptance claim;
- cross-context or cross-model independence is part of required Final Review;
- ancestry is material to depth-one enforcement;
- configured and observed facts conflict;
- release validation is characterizing capacity, lifecycle, or observability;
- the user explicitly requests runtime proof.

Ordinary bounded execution may proceed from exact profile configuration plus deterministic artifact verification when post-spawn proof is not part of acceptance.

## 5. Conflict behavior

For child evidence:

```text
configuration route unavailable
-> do not cross-route

required native route incomplete
-> return to main session

required read-only native sandbox missing/broader
-> return to main session or quarantine

route / identity / ancestry / permission conflict
-> X0 + quarantine affected result
```

For main-session evidence:

```text
complete native Sol route
-> judgment coverage = covered

complete native non-Sol route
-> judgment coverage = uncovered

missing / partial / local-only route
-> judgment coverage = unknown

native/local conflict
-> judgment coverage = unknown; quarantine the route claim
```

A runtime-evidence result never upgrades model judgment into deterministic task evidence. It only establishes routing/runtime facts that were actually observed.
