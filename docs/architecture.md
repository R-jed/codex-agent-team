# Architecture

Codex Agent Team is a Root-aware policy layer over Codex Native Subagents.

## Control model

The current user-facing Codex session is always the Root Controller. The Skill never requires a Sol Root and never creates a second orchestration runtime.

| Role | Default route | Responsibility |
| --- | --- | --- |
| ROOT_CONTROLLER | current session | intent, planning, architecture, risk, integration, final answer |
| EXECUTION_WORKER | GPT-5.6 Luna Max | context-heavy exploration, bounded implementation, debugging, testing |
| INDEPENDENT_CRITIC | GPT-5.6 Terra XHigh | detached review, synthesis, conflicting evidence, assumption challenge |
| SENIOR_JUDGE | GPT-5.6 Sol High | one-off high-consequence adjudication when Root is not Sol and the user consents |

The role table stays deliberately narrow. Terra is not a default implementation escalation lane, and Sol is not a mandatory final reviewer.

## Native runtime, not a parallel thread system

The Skill calls Codex Native `spawn_agent`.

Internally, Codex backs each Subagent with a child thread. Codex Agent Team does not call an App Thread `create_thread` API, manage an external DAG, or maintain a separate scheduler.

See [`native-subagent-runtime.md`](native-subagent-runtime.md).

## Decision sequence

```text
Root task
  -> Agent Profile Readiness Gate
  -> Delegation Gate
  -> Route Assurance Gate
  -> Role Router
  -> Consent Gate when a material boundary changes
  -> Execute Native Subagent
  -> Runtime Evidence when useful or required
  -> Evidence Gate
  -> Review Gate when detached judgment has concrete value
  -> Close Subagent
  -> Root integration and acceptance
```

Minimum Team remains upstream of every later delegation decision. Runtime evidence and review strengthen an already-justified responsibility; they do not justify extra Agents by themselves.

## Plugin and profile readiness

Codex Plugin is the only supported distribution path. The Plugin packages the canonical Skill, role-pinned Agent templates, and the managed custom-Agent installer.

`/codex-agent-team` is the single user-facing workflow entry point. Before model-specific delegation, it checks whether the required project roles are visible through the current native role surface.

When a required role is missing, the Skill asks permission to write only the four managed Agent TOML profiles plus the ownership manifest under Codex home. It then runs the bundled installer and exactness check, and re-inspects live role discovery.

Exact file installation does not imply that the current task has refreshed custom-Agent discovery. If the new roles remain unavailable after exact installation, the current task stops model-specific delegation and asks the user to start a fresh task.

## Configuration route assurance

Model-specific children use only provable configuration routes. The Skill keeps these facts separate:

```text
preferred_route
configured_route
route_assurance
observed_route
```

A successful exact spawn can establish a configuration-level assured route. The architecture never upgrades configuration assurance into a claim of runtime-observed telemetry.

### Profile Mode

An installed custom Agent role pins the intended model and reasoning effort and live role guidance confirms the lock.

```text
route_assurance = profile_locked
```

`profile_locked` describes a configuration lock, not post-spawn proof. This is the normal Plugin route.

### Portable Mode

A built-in role plus explicit model/effort remains an internal compatibility path only when profile-free operation is explicitly required, the live surface exposes the required fields, and Codex accepts the exact tuple.

```text
route_assurance = native_explicit_validated
```

Portable Mode is never an automatic fallback for missing project profiles. The Skill does not treat omitted model/effort as exact inheritance assurance.

See [`model-route-assurance.md`](model-route-assurance.md).

## Runtime evidence mechanism

Post-spawn evidence is graded by source strength:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

Public/native runtime metadata is preferred. `scripts/inspect-runtime.py` inside the installed Skill can read one exact local rollout as an optional fallback record. That local record is mutable implementation-coupled telemetry, so it never becomes an authoritative runtime report by itself.

`scripts/verify-runtime.py` is the deterministic mechanism that compares expected role/model/effort, child identity, expected parent-thread identity, source agreement, and required read-only state. Policy decides when that evidence is required; the verifier decides whether supplied evidence matches.

When Root knows its own thread id, a child `parent_thread_id` mismatch is quarantined. This gives the Depth 1 policy a runtime-verifiable path when ancestry metadata is available.

See `plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md` and [`compatibility.md`](compatibility.md).

## Context strategy

Role-specific spawns always set `fork_turns` explicitly.

- Explorer: `none`
- Critic: `none`
- Worker: `none` by default, positive recent-N only when required

This avoids accidental full-history inheritance and preserves detached review.

## Implementation contract

Bounded coding work can use the Task Packet Implementation Preset:

```text
OBJECTIVE
OWNERSHIP
INTERFACES
CONSTRAINTS
VERIFICATION
STOP CONDITIONS
RETURN
```

Workers return `judgment_calls`. Worker reports remain claims; Root inspects actual changes and reruns deterministic verification.

## Review model

Independent review is risk-triggered. A Terra critic is added when detached judgment materially improves acceptance, such as security/permission logic, concurrency/state consistency, public contracts, migrations, broad cross-module invariants, weak deterministic oracles, material Worker judgment calls, or conflicting evidence.

The critic returns `clear`, `findings`, or `insufficient_evidence`. Root retains final acceptance authority. A remaining high-consequence disagreement may reach one consent-gated Sol Senior Judge when Root is not already Sol.

## Permission semantics

Custom Agent profiles may declare sandbox defaults, but effective child permissions are runtime facts. A profile declaring `sandbox_mode = "read-only"` is useful intent metadata; it is not proof of effective runtime enforcement.

`runtime_enforced` is reserved for effective read-only reported by the native runtime. Local rollout evidence may corroborate it but cannot establish it alone.

When hard isolation is not required and the host broadens a critic's sandbox, Safety Policy permits behavioral read-only only with explicit no-write instructions and verified before/after state. That path remains `instruction_enforced`.

## Managed custom-Agent lifecycle

The Plugin-bundled `scripts/install-agents.py` validates shipped profile sources, preflights conflicts, refuses symlinked destinations and reserved-role collisions, stages managed profile replacements, verifies exact bytes, and supports a strictly non-mutating `--check`.

It stores `.codex-agent-team-agents.json` under Codex home. The manifest records hashes of package-managed profiles. A later Plugin version may replace a differing profile only when the installed bytes still match a previous managed hash. User-modified profiles remain protected.

The installer can recognize ownership hashes from earlier Codex Agent Team standalone releases so existing users can migrate to Plugin-only distribution without weakening overwrite protection.

Rollback errors are treated as a separate failure condition and must be reported as `ROLLBACK INCOMPLETE` rather than silently swallowed.

## Compatibility and behavior evidence

Repository tests verify Plugin packaging, managed profile installation, policy regressions, runtime-evidence fixtures, and deterministic verification. Live spawn/model/effort capability remains an in-session fact.

Static repository tests do not prove real Skill behavior in a particular Codex build. `behavioral-evals.md` defines the live workload/result protocol used to compare Root-only and Agent Team runs without inventing missing token or latency telemetry.

## Lifecycle

```text
spawn -> work -> observe when useful -> gather -> verify -> review when justified -> optional focused follow-up -> close
```

## Scope boundary

Core deliberately excludes persistent Task orchestration, App Thread recovery, Worktree scheduling, external DAGs, provider routing, mandatory all-task review, and production deployment automation.
