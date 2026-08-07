# Recovery

Recovery owns what happens to one delegated responsibility after dispatch. It distinguishes uncertain runtime state from confirmed failure and keeps retries bounded without turning failure into a model ladder.

`router-core.md` decides which capability the unresolved work needs. `team-plan.md` owns dependency, assigned role, ownership, and integration truth when TeamPlan is active. This file owns attempt identity, lifecycle, failure classification, retry bounds, and Main takeover.

## Identity

Every delegated Agent attempt has:

```text
team_plan_revision, when TeamPlan exists
unit_id
task_id
attempt
```

`unit_id` identifies the stable responsibility. `task_id` identifies one concrete Agent attempt and must be unique. A retry keeps the same `unit_id` and uses a new `task_id`.

Without TeamPlan, the single delegated responsibility still gets a stable `unit_id` and unique `task_id`; `team_plan_revision` is null/absent as required by the ledger representation.

## Native lifecycle

Use only:

```text
PLANNED
SPAWN_PENDING
RUNNING
COMPLETED
FAILED
UNKNOWN
CLOSED
```

Normal accepted execution is:

```text
PLANNED -> SPAWN_PENDING -> RUNNING -> COMPLETED -> CLOSED
```

`COMPLETED` means the Agent produced a complete result. Main has not necessarily accepted it yet.

Use `FAILED` only for a confirmed unsuccessful attempt.

Use `UNKNOWN` when available host evidence cannot establish creation, identity, completion, or current Agent state. UNKNOWN is not failure.

While an attempt remains UNKNOWN:

```text
no replacement Agent
no retry
no semantic reroute
no conflicting ownership reassignment
no claim that the attempt failed
```

Wait for useful native evidence when available. If the runtime never exposes enough evidence to resolve the ambiguity, preserve the uncertainty and avoid duplicate mutation risk. Do not build a private scheduler or busy-poll to manufacture state.

## Failure classification

For a confirmed failed attempt, record both axes.

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

`runtime_ambiguous` is reserved for an UNKNOWN record; it does not mean a confirmed failed execution.

Semantic blocker:

```text
none
contract
judgment
investigation
stalled
```

These axes answer different questions: what is known about execution, and what unresolved task need remains. Do not invent additional blocker values in Agent profiles or local recovery logic.

Examples:

```text
runtime_unavailable + none
-> same role may still be correct

quality_failure + judgment
-> resolve the material decision through Main/Sol

quality_failure + contract
-> Main repairs missing task truth

runtime_ambiguous
-> UNKNOWN; do not replace
```

Infrastructure failure is not capability evidence.

## Bounded correction

One unchanged unit may use at most:

```text
2 Agent attempts
1 focused follow-up on an existing Agent
```

A focused follow-up is only for a complete result that is close enough to acceptance that the same Agent, role, responsibility, and authority still fit. It carries the exact failure and preserves valid evidence and DO NOT REDO facts.

A follow-up stays inside the same attempt and does not create a new `task_id`.

A second Agent attempt is allowed only after the first attempt is confirmed FAILED and Main has a concrete reason that another attempt is policy-compatible. The new attempt gets a new `task_id`.

After the second Agent attempt fails, Main takes ownership or reports the exact blocker. Do not create a third Agent attempt for the unchanged unit.

The two-attempt bound limits recovery. It is not a team-size or concurrency limit.

## Allowed recovery actions

Use only:

```text
same_agent_followup
same_role_retry
semantic_reroute
main_takeover
```

### same_agent_followup

Use once when the result is complete, the role remains correct, and a narrow correction can reasonably satisfy acceptance.

### same_role_retry

Use a new Agent attempt when responsibility and role remain correct and the retry packet is materially improved by new evidence, a concrete correction hypothesis, or a confirmed transient execution problem.

### semantic_reroute

Use only when the remaining semantic blocker changes the capability required:

```text
contract -> Main repairs task truth or acceptance
judgment -> capable Main or Sol Advisor/Solver
investigation -> Terra Investigator only when semantics are stable, the work is read-only, and broader investigation is actually useful
stalled -> same-role retry only if the role remains correct; otherwise Main takes over
```

Failure itself never means Luna -> Terra -> Sol.

If TeamPlan is active and semantic rerouting changes the unit's assigned role, create a new TeamPlan revision before the replacement attempt. Keep the same `unit_id` only when its goal and output remain the same. Role reassignment does not reset the attempt budget.

### main_takeover

Main takes ownership when recovery is exhausted, the safe route is unclear, authority would need to widen, or continuing delegation no longer adds value.

## TeamPlan revisions

A retry by itself does not create a new TeamPlan revision.

Revise TeamPlan only when coordination truth changes materially, including assigned role, dependency, ownership, deliverable, scope, or acceptance. A materially redefined goal/output is a new responsibility and requires a new `unit_id`.

Already-dispatched work remains bound to the revision it received. If a revision affects active work, pause new dispatch until affected attempts are safely settled or invalidated.

## Adoption and close

Main inspects actual artifacts/evidence and marks an attempt adopted only when acceptance is supported.

An adopted completed native Agent should be closed when the host exposes that control. `CLOSED` is lifecycle state, not correctness proof.

## Ledger validation

When machine-checkable recovery state is genuinely useful, validate it with:

```bash
python plugins/codex-delegate/scripts/validate_team_ledger.py /path/to/ledger.json
```

The validator checks exact record shape, policy-owned role bindings, TeamPlan revision binding, stable unit goal/output identity, unique task and Agent identity, attempt sequence, the two-attempt bound, follow-up bound, UNKNOWN replacement suppression, and lifecycle/adoption consistency.

Do not create a persistent ledger for ordinary short work merely because a validator exists. Keep state in context unless cross-session recovery, multiple long-lived worktrees, strict audit, or another real need justifies durable state. Reuse an upstream state source when one already owns the task.
