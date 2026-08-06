# Recovery

Recovery governs one delegated responsibility after dispatch. It keeps execution bounded, distinguishes uncertain state from confirmed failure, and returns semantic decisions to the correct owner instead of turning failure into a model ladder.

`router-core.md` still decides which role is correct for the responsibility. `team-plan.md` owns dependency and integration truth. This file owns attempt identity, native lifecycle, failure classification, retry bounds, and Main takeover.

## 1. Identity

Every delegated Agent attempt has:

```text
team_plan_revision, when TeamPlan exists
unit_id
task_id
attempt
```

`unit_id` identifies the stable responsibility. `task_id` identifies one concrete Agent attempt and must be unique. A retry keeps the same `unit_id` and uses a new `task_id`.

When no TeamPlan is needed, a single delegated responsibility still gets a stable `unit_id` and unique `task_id`; `team_plan_revision` remains absent.

## 2. Native lifecycle

Use this state vocabulary for native Agent execution:

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
PLANNED
-> SPAWN_PENDING
-> RUNNING
-> COMPLETED
-> CLOSED
```

A confirmed unsuccessful attempt enters `FAILED`.

If creation, identity, completion, or current Agent state cannot be established from the host evidence available to Main, enter `UNKNOWN`.

UNKNOWN is not failure.

While a unit has an unresolved `UNKNOWN` attempt:

```text
no replacement Agent
no retry
no semantic reroute
no conflicting ownership reassignment
no claim that the attempt failed
```

Wait for useful host evidence when available. If the host never exposes enough evidence to resolve the ambiguity, Main must preserve the uncertainty and avoid duplicate mutation risk rather than invent a definitive state.

Do not build a private scheduler, poll continuously, or manufacture lifecycle telemetry that Codex does not expose.

## 3. Two-axis failure classification

When an attempt is confirmed unsuccessful, classify both the execution origin and any remaining task blocker.

Record the execution axis as `failure_origin`:

```text
none
runtime_unavailable
permission_failure
tool_failure
timeout
quality_failure
runtime_ambiguous
```

Record the semantic axis as `task_blocker`:

```text
none
contract
judgment
investigation
stalled
```

These axes answer different questions.

Examples:

```text
runtime_unavailable + none
-> the responsibility may still belong to the same role

quality_failure + judgment
-> the implementation exposed a material decision and the Sol path is now required

quality_failure + contract
-> Main repairs missing task truth before another child can proceed

runtime_ambiguous
-> state is UNKNOWN, not a candidate for immediate replacement
```

Do not convert infrastructure failure into a capability judgment.

## 4. Bounded correction and attempts

A unit may use at most:

```text
2 Agent attempts
1 focused follow-up on an existing Agent
```

The focused follow-up is only for a complete result that is close enough to correct that the same Agent and same role still fit. It carries the precise failure, preserved valid evidence, acceptance, and explicit DO NOT REDO facts.

A follow-up does not create a new `task_id` because it is the same Agent attempt.

If the follow-up still fails, or if a follow-up is not appropriate, Main diagnoses the two failure axes before deciding whether a second Agent attempt is allowed.

After the second Agent attempt fails, Main takes ownership or reports the exact blocker. Do not create a third Agent attempt for the same unchanged unit.

The two-attempt bound is a recovery limit, not a team-size or concurrency limit.

## 5. Allowed recovery actions

Recovery is constrained to these actions:

```text
same_agent_followup
same_role_retry
semantic_reroute
main_takeover
```

### same_agent_followup

Use once when the result is complete, the role remains correct, and a narrow correction can reasonably satisfy acceptance.

### same_role_retry

Use a new Agent attempt only when the responsibility and role remain correct and the retry packet is materially improved by new evidence or a concrete correction hypothesis.

Runtime unavailability, a transient tool failure, or a confirmed failed attempt with `task_blocker: none` can justify this path when the role remains policy-compatible.

### semantic_reroute

Use only when the remaining task blocker changes the required capability:

```text
contract -> Main repairs task truth or acceptance
judgment -> capable Main or Sol Advisor/Solver
investigation -> Terra Investigator only when semantics are stable, read-only, and no material judgment remains
stalled -> same-role retry only if the role is still correct; otherwise Main takes over
```

Failure itself never means Luna -> Terra -> Sol.

### main_takeover

Main takes ownership when recovery is exhausted, the safe route is unclear, authority would need to widen, or continuing delegation no longer adds value.

## 6. Recovery and TeamPlan

A retry does not create a new TeamPlan unit. It remains another attempt for the same `unit_id`.

A routing or execution failure does not revise TeamPlan by itself.

Create a new TeamPlan revision only when recovery evidence changes task structure such as dependency, ownership, deliverable, scope, or acceptance.

If a new revision affects running work, pause new dispatch and preserve each active attempt's original plan binding until it is safely settled or invalidated.

## 7. Adoption and close

`COMPLETED` means the Agent produced a complete result. It does not mean Main accepted it.

Main inspects the actual artifact/evidence and sets the attempt as adopted only when acceptance is supported.

An adopted completed native Agent should be closed when the host exposes that control. `CLOSED` is a lifecycle state, not proof that the work was correct; acceptance still belongs to Main.

## 8. Ledger validation

For tasks that need machine-checkable recovery state, validate the in-context or persisted ledger with:

```bash
python plugins/codex-delegate/scripts/validate_team_ledger.py /path/to/ledger.json
```

The validator checks unique task and Agent identity, TeamPlan revision binding, per-unit attempt sequence and limits, UNKNOWN replacement suppression, follow-up bounds, and basic lifecycle/adoption consistency.

Do not create a persistent ledger for ordinary short work solely because this validator exists. Keep state in context unless cross-session recovery, multiple long-lived worktrees, strict audit, or another real recovery need justifies durable state. Reuse an upstream ledger when one already owns task state.
