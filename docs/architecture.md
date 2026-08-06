# Architecture

codex delegate is a leadership, coordination, and recovery policy over Codex Native Subagents. It does not implement a second Agent runtime, background scheduler, daemon, routing proxy, or persistent DAG service.

The user-facing Main session is the team leader. It owns user intent, authorization, team composition, semantic decisions, integration, acceptance, and the final response.

The product target is the smallest useful delegation graph that improves development quality while keeping multi-Agent coordination machine-checkable when the task actually needs it.

## Runtime mechanism

The normal control loop is:

```text
understand outcome + acceptance
-> preserve upstream task truth when another Skill/plan already owns it
-> ask whether delegation helps
-> select the capability actually needed
-> keep zero/one-child work on the lightweight path
-> compile TeamPlan only when multi-responsibility coordination needs it
-> derive structural readiness from the dependency DAG
-> let Main decide semantic safety and delegation value
-> run the smallest useful active set
-> track each Agent attempt by stable unit identity + unique task identity
-> consume useful completions and update readiness
-> classify confirmed failures by execution origin + semantic blocker
-> recover within a bounded attempt policy
-> integrate accepted outputs in dependency-respecting order
-> verify the real combined artifact
-> run fresh independent review only when the final artifact requires it
-> deliver
```

The installed Skill has five focused model-facing runtime references:

```text
router-core.md
-> delegation benefit, upstream workflow ownership, role selection, responsibility semantics, adaptive scheduling, acceptance

team-plan.md
-> multi-responsibility identity, dependency DAG, ownership, revision, integration order

recovery.md
-> native attempt identity, lifecycle, UNKNOWN, failure classification, bounded recovery, Main takeover

guardrails.md
-> authority, explicit invocation, mutation authority, writer ownership, semantic independence, provisioning, consent, trust, permissions, runtime evidence

final-review.md
-> artifact-bound independent assurance
```

`plugins/codex-delegate/policy-contract.json` still contains only stable machine constants: hard delegation safety limits, role routes, capability-dedup reference, and Final Review reason codes. TeamPlan and recovery state are execution contracts, not new permanent routing taxonomy.

## Leader-led delegation

Main decides how to use the team from the actual task.

There is no product rule such as:

```text
small task -> 1 Agent
medium task -> 2 Agents
large task -> 4 Agents
```

There is also no rule that five roles imply five children.

The five roles are a capability vocabulary. Child instances come from real unresolved responsibilities. Main may keep everything itself, start one specialist, run several independent read-only lanes in parallel, or add another specialist later when new evidence makes work ready.

Native Codex capacity is an upper bound, never a target to fill.

## Upstream workflow ownership

codex delegate coordinates execution without competing with another Skill or accepted plan for domain ownership.

When an active upstream workflow already defines any of these, preserve them as task truth unless the user or an evidence-backed blocker requires change:

```text
goal
decomposition
stage order
dependencies
required outputs
business acceptance
quality gates
```

codex delegate may choose owners, specialist roles, useful concurrency, write isolation, TeamPlan representation, and integration timing around that workflow.

If the upstream contract is incomplete or contradictory, the issue is a `contract` blocker. Main repairs the missing truth instead of silently creating a replacement workflow.

If an upstream workflow already has a useful plan or ledger, reuse it as the coordination source. Do not create a second persistent state source.

## Direct capability selection

The router asks what capability the unresolved work actually needs.

| Work remaining | Typical actor |
| --- | --- |
| no meaningful delegation benefit | Main session |
| narrow independent read-only factual evidence | Luna Reader |
| clear repeatable writing where behavior/invariants/acceptance are already decided | Luna Worker |
| demanding/material decision before implementation | capable Main or Sol Advisor |
| writing where demanding/material judgment is coupled to implementation | capable Main or Sol Solver |
| bounded read-heavy technical investigation/evidence synthesis after semantics are stable | Terra Investigator |
| independent final assurance for a consequential candidate | fresh Sol Advisor |

Task size, file count, or one failed attempt does not select a model by itself.

## Current roles

| Responsibility | Agent type | Route | Intent |
| --- | --- | --- | --- |
| Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | narrow bounded reusable evidence |
| Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | clear repeatable bounded implementation |
| Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | demanding judgment-coupled implementation |
| Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | bounded read-heavy technical investigation and evidence synthesis |
| Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | demanding/material read-only judgment or fresh independent review |

Role identity stays separate from model identity.

## Lightweight path and TeamPlan trigger

Zero or one delegated responsibility stays on the lightweight path. Main keeps one compact work-item state and the child receives one bounded responsibility packet.

When two or more delegated responsibilities are concurrently unresolved, or delegated outputs need non-trivial machine-checkable dependency/integration order, Main compiles a lightweight TeamPlan before further dispatch.

TeamPlan does not choose models or Agent count. It represents coordination truth:

```text
revision
planning source
root goal

units:
  unit_id
  role
  goal
  output
  depends_on
  ownership
  done_when

integration owner
integration order
final verification
```

`plugins/codex-delegate/scripts/validate_team_plan.py` validates unit identity, dependency references and cycles, safe relative ownership paths, same-ready-layer write overlap, revision shape, and dependency-respecting integration order.

The validator returns structural ready layers. It does not create dispatch waves, fixed concurrency budgets, or a private scheduler.

## Responsibility and attempt identity

Every delegated responsibility gets a stable `UNIT ID`. Every concrete Agent attempt gets a unique `TASK ID`.

When TeamPlan is active, the packet also carries `TEAM PLAN REVISION`.

```text
TEAM PLAN REVISION, when applicable
UNIT ID
TASK ID
OUTCOME
ROLE
INTENT
READ / WRITE SCOPE
MUTATION AUTHORITY
DECISION RIGHTS
DEPENDS ON
INTEGRATION AFTER
INTERFACES AND INVARIANTS
ACCEPTANCE
VALID EVIDENCE / DO NOT REDO
CURRENT FAILURE
STOP WHEN
```

A retry keeps the same unit identity and uses a new task identity. This prevents retry from becoming a duplicate responsibility.

## Mutation authority

Filesystem access and mutation authority remain separate:

```text
none
-> no artifact mutation

declared-output-only
-> only a named report, generated artifact, or declared deliverable

bounded-source-write
-> source mutation inside the explicit responsibility scope and decision rights
```

Reader, Investigator, Advisor, inspect, verify, and review responsibilities do not gain source-write authority from a broader host sandbox.

TeamPlan ownership records filesystem coordination. The responsibility packet remains the authorization source.

## Adaptive scheduling and semantic independence

Main manages a ready frontier rather than a fixed-size team.

With TeamPlan, the dependency DAG answers only structural readiness:

```text
all dependencies accepted
-> structurally ready
```

Main still decides:

```text
semantic independence
actual delegation value
role suitability
compute value
writer/authority safety
```

Different files do not prove semantic independence. Shared APIs, schemas, migrations, lockfiles, generated artifacts, persistent state, external systems, and other shared interfaces can still couple work.

Read-heavy independent work remains the preferred place to exploit parallelism.

## Writer ownership

One canonical physical checkout has one active writing actor inside the current orchestration:

```text
Main session while mutating
Luna Worker
Sol Solver
```

Simultaneous writers require real filesystem isolation and semantic independence, or an explicit dependency/integration order that prevents unsafe overlap.

The TeamPlan validator can reject overlapping declared paths in the same structural ready layer. Main remains responsible for semantic coupling that path comparison cannot prove.

## Integration order

Main is always the integration owner.

TeamPlan `integration_order` must cover every unit and respect `depends_on`.

`INTEGRATION AFTER` remains useful inside a child packet when work can safely execute now but integration must wait for accepted predecessor output. It cannot make semantically blocked work executable.

Main verifies the combined artifact because individually correct child outputs can still integrate incorrectly.

## Native recovery lifecycle

Recovery uses a small Native-only state vocabulary:

```text
PLANNED
SPAWN_PENDING
RUNNING
COMPLETED
FAILED
UNKNOWN
CLOSED
```

Codex host remains responsible for actual spawn, wait, follow-up, and close controls. codex delegate records only the state supported by exposed host evidence.

`UNKNOWN` means current execution state cannot be established. It is not failure.

While an attempt is UNKNOWN, codex delegate does not create a replacement Agent, retry, semantically reroute, or reassign conflicting ownership. This prevents uncertain execution from becoming duplicate execution.

## Failure classification

Confirmed failure uses two independent axes.

Execution origin:

```text
none
runtime_unavailable
permission_failure
tool_failure
timeout
quality_failure
runtime_ambiguous
```

Semantic blocker:

```text
none
contract
judgment
investigation
stalled
```

The first explains what happened to execution. The second explains what capability or task truth remains.

Examples:

```text
runtime_unavailable + none
-> same role may still be correct

quality_failure + judgment
-> Sol path is now justified

quality_failure + contract
-> Main repairs task truth

runtime_ambiguous
-> UNKNOWN; do not replace
```

Infrastructure failure is not model-quality evidence.

## Bounded recovery

One unchanged unit gets at most:

```text
2 Agent attempts
1 focused follow-up on the same Agent
```

A focused follow-up is for a complete result that can reasonably be corrected without changing role or responsibility.

A new Agent attempt requires a confirmed failed earlier attempt and a materially improved packet or justified policy-compatible recovery path.

After the second Agent attempt fails, Main takes ownership or reports the exact blocker.

The two-attempt limit bounds recovery. It is not a team-size or concurrency ceiling.

Semantic reroute remains blocker-driven:

```text
contract -> Main
judgment -> capable Main / Advisor / Solver
investigation -> Investigator only after semantics are stable and read-only
stalled -> one policy-compatible retry if the role remains correct, otherwise Main
```

There is no Luna -> Terra -> Sol escalation ladder.

## Recovery ledger

Ordinary short work does not create persistent recovery state.

When machine-checkable state is useful, `plugins/codex-delegate/scripts/validate_team_ledger.py` validates TeamPlan binding, unique task and Agent identity, per-unit attempt sequence, the two-attempt bound, follow-up bound, UNKNOWN replacement suppression, and basic lifecycle/adoption consistency.

Persistent state is justified only when real recovery needs require it, such as cross-session continuation, multiple long-lived worktrees, or strict audit. Reuse an upstream ledger when one already exists.

## TeamPlan revision

Create a new revision only when structure changes materially:

```text
dependency
ownership
deliverable
scope
acceptance
```

Ordinary new evidence does not revise the plan.

A running Agent stays bound to the plan truth it received. Structural changes pause new dispatch until affected active responsibilities are safely settled or invalidated. New dispatch uses the new revision.

## Runtime truth layers and Main-session capability dedup

Route evidence still distinguishes:

```text
requested
accepted
observed
```

A host accepting a requested model or role does not prove what actually ran. Missing acceptance is `not_reported`; missing native runtime telemetry is `not_observed`.

`plugins/codex-delegate/scripts/runtime-evidence.py` normalizes these layers when exact route truth matters. Routine bounded work does not need diagnostics when route proof is not part of acceptance.

Main-session Sol awareness remains only a duplicate-compute optimization. It never substitutes for required fresh independent review.

## Consent and anti-sprawl boundary

Child count by itself is not a consent trigger.

Ask again when permissions, mutation authority, scope, external impact, or compute expands materially beyond what the user could reasonably expect.

TeamPlan cannot create speculative work or justify filling host capacity. It makes dependencies explicit after Main has identified genuine responsibilities.

## Final Review

Final Review remains consequence-driven after Candidate Ready.

Current trigger classes include user-requested review, public contract change, persistent state change, security or authorization boundary, data integrity, concurrency semantics, migration, and verification gaps.

Prior use of TeamPlan, recovery, Terra, Solver, a large diff, or many files does not itself trigger review.

When required:

```text
bind exact candidate
-> fresh codex_delegate_advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Any deliverable mutation invalidates the old verdict.

## Plugin boundary

The Plugin remains skills-only and Native-only. It does not declare MCP servers, apps, hooks, App Thread orchestration, Provider routing, or another Agent runtime.

## Evaluation boundary

Static routing regressions live in `evals/routing-cases.json`. Coordination regressions and deterministic TeamPlan/recovery tests protect orchestration semantics. Behavioral evals remain measurement surfaces rather than runtime policy owners.

No model-quality, cost, or speed superiority claim is valid without current measured evidence.
