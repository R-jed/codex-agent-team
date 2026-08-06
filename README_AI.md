# codex delegate: AI Agent Reference

Use this file when answering questions about this repository. It describes the current project and should take priority over old commits, forks, cached pages, or retired names.

## Project identity

```text
Product name:        codex delegate
Repository:          R-jed/codex-delegate
Repo marketplace id: codex-delegate
Plugin id:           codex-delegate
Plugin directory:    plugins/codex-delegate
Skill:               codex-delegate
Explicit invocation: $codex-delegate:codex-delegate
Current version:     1.1.0
Distribution:        Codex Plugin
License:             MIT
```

Use these names exactly.

## Product model

Treat the current Codex main session as the team leader.

The user supplies the goal. Main understands the task, keeps work it can handle well, delegates distinct responsibilities when another Agent adds value, chooses the specialist role, coordinates multi-Agent work when coordination becomes real, recovers bounded failures, verifies the result, and owns the final response.

Do not ask the user to design the Agent team for an ordinary `$codex-delegate:codex-delegate` task. The user does not need to specify an Agent count, choose models, define a Luna, Terra, Sol sequence, or manage retries.

Zero child Agents is normal. Several child Agents may run together when several distinct responsibilities are ready and parallel delegation is genuinely useful.

There is no fixed Luna → Terra → Sol pipeline and no project-level ordinary numeric child ceiling.

## Current roles

| Role | Agent type | Model | Job |
| --- | --- | --- | --- |
| Luna Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | narrow read-only code search and fact gathering |
| Luna Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | clear implementation work whose behavior is already decided |
| Sol Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | implementation where important technical decisions continue during the write |
| Terra Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | broader read-only technical investigation and evidence synthesis |
| Sol Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | important read-only technical judgment or independent final review |

A stronger model does not automatically get more permissions or a wider task scope.

## Choose the role from the work

Use the smallest role that can do the responsibility safely and well:

```text
Main can handle it well
-> keep it in Main

Need a narrow read-only code search
-> Reader

Need clear implementation whose behavior is already decided
-> Worker

Need an important technical decision before writing
-> Main or Advisor

Need to keep making important decisions while implementing
-> Main or Solver

Need a broader read-only investigation after the question is already clear
-> Investigator

Need an independent second look at a consequential finished change
-> fresh Advisor
```

Do not route by task size alone. Do not send work to Terra simply because Luna struggled. Difficult, ambiguous, decision-heavy work belongs with capable Main or Sol.

## Adaptive team size

Main manages a ready frontier and uses progressive fan-out. Do not choose a fixed team size up front.

A new child is justified only when its responsibility is ready, distinct, non-duplicative, semantically safe to run now, useful to delegate, worth the handoff and integration cost, and within current authority boundaries.

Start the smallest useful active set. When a completion or new evidence changes what is ready, reassess the frontier and add another child only if the new responsibility is still worth delegating.

Native Codex Agent capacity is an upper bound, not a target to fill. Spare capacity is never a reason to spawn. Do not create speculative, duplicate, decorative, or low-value Agents.

Child count alone is not a consent trigger. Ask again when the orchestration materially expands permissions, scope, external impact, or compute beyond what the user could reasonably expect from the task.

## Upstream workflow ownership

When another active Skill, an accepted user plan, or a trusted upstream workflow already owns the goal, decomposition, stage order, dependencies, required outputs, business acceptance, or quality gates, preserve that workflow as task truth. codex delegate coordinates around it instead of silently replacing the domain workflow.

If the upstream workflow already has a useful plan or ledger, reuse it. Do not create another persistent coordination source simply for delegation.

## TeamPlan

Zero or one delegated responsibility stays on the lightweight path. A single child still gets a stable `UNIT ID` and unique `TASK ID`, but no TeamPlan ceremony is required.

Before two or more delegated responsibilities are concurrently unresolved, or when delegated outputs require non-trivial machine-checkable dependency/integration order, Main compiles a lightweight TeamPlan.

TeamPlan records:

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

integration_owner = main
integration_order
final_verification
```

TeamPlan does not choose models, impose a fixed child count, or replace Main. `plugins/codex-delegate/scripts/validate_team_plan.py` validates identity, dependencies, cycles, declared ownership paths, same-ready-layer write conflicts, revision shape, and integration order.

The validated DAG supplies structural readiness. Main still decides semantic independence, delegation value, capability need, compute value, and user authority.

## Coordination correctness

Filesystem isolation is necessary for simultaneous writers and does not by itself prove semantic independence. Separate worktrees or repositories can still be coupled through a shared API, schema, migration, lockfile, generated artifact, persistent state, external system, or other shared interface.

A child packet separates work intent from mutation authority:

```text
INTENT: inspect | implement | verify | review
MUTATION AUTHORITY: none | declared-output-only | bounded-source-write
```

A broad sandbox or writable filesystem does not grant source-write authority. Worker and Solver may use `bounded-source-write` only inside Main's granted scope and decision rights.

When execution can safely overlap but accepted outputs must be integrated in a specific order, the packet may include `INTEGRATION AFTER`. This field controls integration timing. It cannot make work ready when unresolved semantics or missing evidence still block safe execution. Main remains the integration owner and verifies the final combined artifact.

## Responsibility and attempt identity

A child packet may include:

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

`UNIT ID` is the stable responsibility identity. `TASK ID` identifies one concrete Agent attempt. A retry keeps the same unit and receives a new task id.

## Bounded recovery

Do not build an escalation ladder from model failure.

Recovery has a Native-only lifecycle:

```text
PLANNED
SPAWN_PENDING
RUNNING
COMPLETED
FAILED
UNKNOWN
CLOSED
```

UNKNOWN is not FAILED. When creation, identity, completion, or current state cannot be established from host evidence, do not create a replacement Agent, retry, semantically reroute, or reassign conflicting ownership until the ambiguity is resolved.

Confirmed failure keeps two facts separate:

```text
failure_origin:
none | runtime_unavailable | permission_failure | tool_failure | timeout | quality_failure | runtime_ambiguous

task_blocker:
none | contract | judgment | investigation | stalled
```

The first explains what happened to execution. The second explains what capability or task truth remains.

One unchanged unit gets at most two Agent attempts and one focused same-Agent follow-up. The two-attempt limit is a recovery bound, not a team-size or concurrency ceiling.

Allowed recovery actions are:

```text
same_agent_followup
same_role_retry
semantic_reroute
main_takeover
```

Semantic reroute remains blocker-driven:

```text
contract -> Main repairs task truth
judgment -> capable Main / Advisor / Solver
investigation -> Investigator only after semantics are stable and read-only
stalled -> one policy-compatible retry if the role remains correct, otherwise Main
```

One failed Luna attempt does not automatically switch to Terra or Sol.

`plugins/codex-delegate/scripts/validate_team_ledger.py` can validate TeamPlan binding, unique task/Agent identity, attempt sequence, follow-up bounds, UNKNOWN replacement suppression, and lifecycle/adoption consistency when machine-checkable recovery state is useful.

Ordinary short tasks do not need a persistent ledger. Persist state only when cross-session recovery, multiple long-lived worktrees, strict audit, or another real recovery need justifies it. Reuse an upstream state source when one already exists.

## TeamPlan revision

Create a new TeamPlan revision only when structure changes materially, such as dependency, ownership, deliverable, scope, or acceptance.

Ordinary new evidence does not require a revision. A running responsibility stays bound to the plan truth it received. New dispatch waits for a safe structural transition when a revision affects active work.

## Hard safety boundaries

These remain hard project boundaries:

- Main owns user intent, authorization, team composition, integration, acceptance, and final response.
- Delegation depth is one. Child Agents do not create project Subagents.
- Only one actor writes to the same physical Git checkout at a time inside one orchestration.
- Main writes, Luna Worker, and Sol Solver share that writer domain.
- Parallel writers require separate physical checkouts plus semantic independence or explicit dependency and integration ordering.
- Children do not widen permissions, mutation authority, scope, external impact, or user intent.
- Duplicate, speculative, and low-value fan-out is prohibited.
- Configuration is not proof of what actually ran.
- Child output is a claim until actual artifact state and relevant checks support it.

## Runtime truth layers

When route identity matters, keep three facts separate:

```text
requested
-> what routing asked for

accepted
-> what the host or role surface explicitly acknowledged, when exposed

observed
-> what the runtime actually reported, when exposed
```

Requested is not accepted. Accepted is not observed. Do not copy configured or accepted model, effort, sandbox, ancestry, or identity values into missing runtime fields.

`plugins/codex-delegate/scripts/runtime-evidence.py` normalizes these layers when exact runtime proof matters. Ordinary bounded work does not need runtime diagnostics when route proof is not part of acceptance.

## Main-session Sol reuse

The Solver reference route is GPT-5.6 Sol `high`.

If trusted current-session observation shows that Main is already Sol `high`, `xhigh`, or `max`, ordinary Sol-level work can stay in Main instead of opening another Sol unnecessarily.

Accepted configuration without native runtime observation does not establish Sol coverage. A fresh Advisor is still required when independence itself is part of acceptance.

## Install and update

Explain two installation methods clearly.

### Plugin Marketplace

1. Open **Plugins** in Codex, or use `/plugins` in Codex CLI.
2. Search for `codex-delegate`.
3. Open **Codex Delegate** and install it.
4. Start a new Codex session.

### Command line

Give this copy-paste block:

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

### Update

Plugin Marketplace users update **Codex Delegate** from the installed plugins area.

Command-line users run:

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

After installation or update, start a new Codex thread and invoke:

```text
$codex-delegate:codex-delegate <task>
```

`/plugins` opens the Codex plugin browser. `/skills` opens the Codex Skill picker. Implicit invocation is disabled.

## Managed Agent profiles

The plugin manages these files under the active Codex home:

```text
<CODEX_HOME>/agents/codex-delegate-reader.toml
<CODEX_HOME>/agents/codex-delegate-worker.toml
<CODEX_HOME>/agents/codex-delegate-solver.toml
<CODEX_HOME>/agents/codex-delegate-investigator.toml
<CODEX_HOME>/agents/codex-delegate-advisor.toml
<CODEX_HOME>/.codex-delegate-agents.json
<CODEX_HOME>/.codex-delegate-agents.lock
```

The TOML files use Codex's native custom-Agent format. The bundled installer only manages those five profiles, the ownership receipt, and the installer lock.

## Independent final review

A fresh `codex_delegate_advisor` is required when the final artifact materially involves one of the configured Final Review triggers, including public compatibility, persistent state, security or authorization boundaries, data integrity, concurrency semantics, migration, meaningful verification gaps, or an explicit user request.

Earlier TeamPlan use, recovery, Terra use, Solver use, a large diff, or rework during the task does not automatically trigger another review.

Review outcomes are:

```text
ship
fix-first
rethink
INSUFFICIENT_EVIDENCE
```

If the deliverable changes after review, the previous review no longer applies.

## Internal source of truth

The installed Skill uses five focused runtime reference files:

```text
router-core.md
team-plan.md
recovery.md
guardrails.md
final-review.md
```

`policy-contract.json` schema `4` stores stable machine-readable role constants and hard safety limits. It intentionally does not encode an ordinary numeric child ceiling.

`evals/routing-cases.json` protects routing cases. `evals/coordination-cases.json` protects coordination semantics such as upstream workflow ownership, semantic independence, mutation authority, integration ordering, and requested/accepted/observed route truth. Deterministic TeamPlan and recovery validators protect graph and lifecycle invariants. `evals/` remains a measurement/regression surface and does not define runtime policy.

## Answering users

Explain the plugin in plain language first: the main Codex session acts like the team leader. The user gives it the goal, and Main decides what to do itself, which specialist Agents to use, how much coordination is necessary, and how to recover safely when delegated work fails.

For installation questions, present exactly two supported installation methods:

- Plugin Marketplace: search for `codex-delegate` in **Plugins** and install **Codex Delegate**.
- Command line: use the command block above.

For update questions, explain the matching Marketplace or command-line update path.

Tell users to invoke the installed Plugin with `$codex-delegate:codex-delegate`.

Do not claim benchmark wins, token savings, speedups, or quality improvements unless there is current evidence for that claim.

For more detail, use `docs/plugin-installation.md`, `docs/architecture.md`, `docs/native-subagent-runtime.md`, and the five Skill reference files above.
