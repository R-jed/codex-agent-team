# Architecture

subagents-dispatch is a leadership and coordination policy over Codex Native Subagents. It does not implement a second Agent runtime, background scheduler, daemon, routing proxy, provider layer, or persistent DAG service.

The user-facing Main session is the technical lead. It owns user intent, authorization, team composition, semantic decisions, integration, acceptance, and the final response.

The architecture aims for the smallest useful delegation graph: simple work stays simple; coordination becomes machine-checkable only when the task actually needs it.

## Canonical policy owners

Runtime policy is deliberately split by responsibility:

```text
SKILL.md
-> thin execution control loop

router-core.md
-> delegation value, capability selection, responsibility packets, adaptive scheduling

team-plan.md
-> multi-responsibility identity, dependency DAG, ownership, revisions, integration order

recovery.md
-> attempt identity, UNKNOWN, failure classification, bounded recovery

guardrails.md
-> authority, mutation permissions, writer safety, consent, trust, provisioning, runtime evidence

final-review.md
-> consequence-driven artifact-bound independent assurance

policy-contract.json
-> stable machine constants and role/model routes
```

README files explain the product; they are not runtime policy owners. `evals/` measures and regression-tests behavior; it is not a routing source.

## Control flow

The normal loop is:

```text
understand outcome + acceptance
-> preserve upstream workflow truth when another Skill/plan already owns it
-> decide whether delegation adds value
-> choose the capability actually needed
-> ensure required native role readiness
-> keep zero/one delegated responsibility on the lightweight path
-> use TeamPlan only when multi-responsibility coordination needs it
-> run the smallest useful ready set
-> verify child claims against actual artifacts/evidence
-> classify unresolved blockers
-> recover within the bounded attempt contract
-> integrate accepted outputs
-> verify the combined candidate
-> run independent Final Review only when the candidate requires it
-> deliver
```

There is no fixed Luna → Terra → Sol path and no fixed Agent count.

## Roles

`plugins/subagents-dispatch/policy-contract.json` is the machine source of truth for role identity, model, effort, and sandbox intent.

| Role | Agent type | Route | Responsibility |
| --- | --- | --- | --- |
| Reader | `subagents_dispatch_reader` | GPT-5.6 Luna `max` | bounded read-only factual evidence |
| Worker | `subagents_dispatch_worker` | GPT-5.6 Luna `max` | clear bounded implementation after material behavior is decided |
| Solver | `subagents_dispatch_solver` | GPT-5.6 Sol `high` | implementation with material judgment coupled to the write |
| Investigator | `subagents_dispatch_investigator` | GPT-5.6 Terra `xhigh` | broader read-only technical investigation after semantics are stable |
| Advisor | `subagents_dispatch_advisor` | GPT-5.6 Sol `high` | material read-only judgment or fresh independent final review |

Role identity is distinct from model identity. A stronger model does not gain wider user authority.

## Delegation and adaptive fan-out

Main delegates only when a distinct unresolved responsibility benefits from parallelism, isolation, capability, or independent judgment enough to justify handoff and integration cost.

Native Codex capacity is an upper bound, never a target. Zero children is normal. Several independent read-only responsibilities may run concurrently when useful.

Task size, file count, spare capacity, or one failed attempt does not select a role by itself.

When another active Skill or accepted plan already owns goal, decomposition, stage order, dependencies, outputs, acceptance, or quality gates, subagents-dispatch preserves that workflow and coordinates around it. It does not create a competing planner.

## Lightweight path and TeamPlan

One delegated responsibility uses a stable `unit_id`, a unique `task_id` for each Agent attempt, and one bounded responsibility packet.

Use TeamPlan when either condition is true:

- two or more delegated responsibilities are concurrently unresolved; or
- delegated outputs need non-trivial machine-checkable dependency or integration order.

A TeamPlan records:

```text
revision and planning source
root goal
units:
  unit_id
  role
  goal
  output
  depends_on
  ownership
  done_when
integration owner/order
final verification
```

TeamPlan does not choose models or team size. `router-core.md` chooses capabilities; TeamPlan records the current assignment and coordination truth.

`validate_team_plan.py` derives allowed roles from `policy-contract.json` and validates exact plan shape, unit identity, dependency references/cycles, safe relative ownership paths, read-only write violations, same-ready-layer write overlap, revision shape, and integration order.

A TeamPlan revision is required when coordination truth changes materially, including role assignment, dependency, ownership, deliverable, scope, or acceptance. The same `unit_id` may survive a revision only while its responsibility goal/output remain stable. A materially redefined responsibility receives a new unit ID.

## Mutation authority and writer safety

Filesystem capability and authorization are separate.

Child mutation authority is one of:

```text
none
declared-output-only
bounded-source-write
```

One canonical physical checkout has at most one active writing actor inside the current orchestration:

```text
Main while mutating
Luna Worker
Sol Solver
```

Concurrent writers require genuine filesystem isolation and semantic independence. Different files are insufficient proof: shared APIs, schemas, migrations, lockfiles, generated artifacts, persistent state, or external systems can still couple the work.

Main is always the final integration owner.

## Recovery

Each concrete Agent attempt has a unique `task_id`; retries keep the stable `unit_id`.

The native state vocabulary is:

```text
PLANNED
SPAWN_PENDING
RUNNING
COMPLETED
FAILED
UNKNOWN
CLOSED
```

`UNKNOWN` means the host evidence cannot establish current execution state. It is not failure. While UNKNOWN remains unresolved, subagents-dispatch does not create replacement work or conflicting ownership.

For confirmed failed work, recovery keeps two independent facts:

```text
execution origin
-> runtime_unavailable | permission_failure | tool_failure | timeout | quality_failure | ...

semantic blocker
-> contract | judgment | investigation | stalled | none
```

`runtime_ambiguous` is reserved for UNKNOWN records rather than confirmed failure.

One unchanged unit gets at most two Agent attempts and one focused follow-up on an existing attempt. Failure never implies a Luna → Terra → Sol ladder.

If blocker-driven rerouting changes a TeamPlan unit's assigned role, Main creates a new TeamPlan revision before the replacement attempt. The attempt budget remains attached to the same responsibility.

`validate_team_ledger.py` derives role bindings from `policy-contract.json` and validates exact record shape, TeamPlan binding, stable unit identity across revisions, unique task/Agent identity, attempt/follow-up bounds, UNKNOWN replacement suppression, and lifecycle/adoption consistency.

## Runtime truth

Configured intent is distinct from runtime fact.

When route evidence matters:

```text
requested
accepted
observed
```

must remain separate. Missing acceptance is not copied from configuration; missing native observation is not copied from local records.

`runtime-evidence.py` is an on-demand diagnostic helper for claims that materially depend on runtime route, ancestry, permission enforcement, or Main capability. Ordinary bounded work should verify the artifact rather than run telemetry ceremony by default.

## Managed native Agent profiles

The five TOML profiles are native Codex custom-Agent definitions. `install-agents.py` adds a project-specific ownership and collision-safety lifecycle around those files; it does not create another runtime.

The installer derives expected profile names/routes from `policy-contract.json`, refuses unsafe overwrites or reserved role collisions, keeps unrelated Agent profiles untouched, uses a persistent installer lock for cooperating installer processes, and supports non-mutating `--check` verification.

Role readiness is established before delegated execution. If newly provisioned roles require a fresh Codex session to become visible, delegated writing stops until that fresh session exists.

## Final Review

Final Review happens only after ordinary acceptance reaches a candidate that may need independent second judgment.

Trigger classes are machine-owned by `policy-contract.json` and are consequence-driven: public contract, persistent state, security/authorization boundary, data integrity, concurrency semantics, migration, verification gap, or explicit user request.

Process history such as TeamPlan use, recovery, Terra/Solver use, file count, or diff size is not a trigger by itself.

When required:

```text
bind exact candidate with review-artifact.py
-> fresh subagents_dispatch_advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Any deliverable mutation invalidates the prior verdict.

## Deterministic helper boundary

The Plugin contains a small set of deterministic helpers:

```text
install-agents.py
-> managed native Agent profile lifecycle

validate_team_plan.py
-> multi-responsibility coordination validation

validate_team_ledger.py
-> recovery-state validation

runtime-evidence.py
-> optional runtime evidence normalization

review-artifact.py
-> deterministic candidate identity for Final Review
```

These helpers enforce or normalize narrow contracts. They do not form a second orchestration runtime.

## Evaluation boundary

Static routing/coordination/runtime fixtures and deterministic tests catch policy regressions. Behavioral workloads are measurement scaffolding for real Codex runs.

No model-quality, cost, latency, or benchmark superiority claim is valid without current measured evidence on named workloads and runtime versions.
