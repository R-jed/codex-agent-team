# Router Core

This is the single runtime routing contract for codex delegate.

The product goal is simple: keep the user-facing main session in control, delegate only when doing so improves the task, use Luna for clear repeatable bounded work, use Sol where demanding or material judgment belongs, use Terra for bounded read-heavy technical investigation, and avoid repeated work.

Do not build a model ladder or an Agent team before understanding the task.

## 1. Minimal task state

Track one compact task state, not separate dependency, evidence, and recovery ledgers:

```text
WORK ITEM
outcome
owner: main | reader | worker | solver | investigator | advisor
write: yes | no
material_judgment: none | separable | coupled
acceptance
valid_evidence
current_failure
blocked_by: none | contract | judgment | investigation | stalled
```

Add another work item only when it represents a genuinely distinct unresolved responsibility. Do not duplicate work that valid evidence already satisfies or another active owner already holds.

## 2. First question: does delegation help?

Zero children is normal.

Keep work in the main session when a child would mostly duplicate context, add handoff overhead, or provide no useful isolation, parallelism, capability uplift, read-heavy investigation, or independent judgment.

A task being large, many-file, expensive, or "complex" does not by itself justify delegation.

## 3. Select by capability need

When delegation helps, answer these questions directly.

### Narrow read-only factual work

If the missing result is bounded inspectable evidence such as a focused repository trace, call mapping, test mapping, or narrow factual lookup:

```text
-> Luna Reader
```

### Writing with behavior already decided

If the desired behavior, invariants, scope, and acceptance are already clear, and remaining discretion is local, clear, and repeatable implementation detail:

```text
-> Luna Worker
```

The key test is whether Luna mainly answers "how do I implement the already-decided result?"

A writable contract alone does not make work Luna-suitable. If implementation is expected to require consequential architecture, compatibility, state, or cross-module semantic choices, use the Sol path.

### Demanding or material judgment before writing

If architecture, behavior, compatibility, risk, or difficult technical reasoning requires consequential judgment before implementation:

```text
-> main session when it already has sufficient Sol capability
-> otherwise Sol Advisor
```

### Writing with judgment coupled to implementation

If demanding or material semantic decisions cannot be safely separated from implementation and must be made while inspecting or changing the artifact:

```text
-> main session when it already has sufficient Sol capability
-> otherwise Sol Solver
```

Do not create Advisor -> Luna -> Advisor loops merely to avoid the Solver lane.

### Bounded read-heavy technical investigation

If semantic intent is already stable, no material decision remains, and the task benefits from broader read-only exploration, technical synthesis, or processing a larger supporting context than a narrow Reader task:

```text
-> Terra Investigator
```

Terra is an investigation/value lane. It is not the automatic destination for "hard" work and it is not an escalation rung above Luna.

Demanding, ambiguous, multi-step technical reasoning that still requires material judgment belongs on the Sol path. Weak Luna output, task size, one failing test, or low confidence does not justify Terra by itself.

## 4. Main-session Sol dedup is an optimization

Main-session model identity never changes authority. It is consulted only when material judgment already requires Sol capability and trusted current-session metadata is already available or inexpensive to obtain.

The policy-owned reference role is defined in `../../policy-contract.json`. `../../scripts/runtime-evidence.py` can normalize exact model/effort metadata when this optimization matters.

```text
covered
-> keep ordinary judgment or judgment-coupled writing in main

uncovered
-> Advisor or Solver when delegation helps

unknown
-> do not affect routine bounded work
-> use the normal Sol path only when material judgment genuinely requires it
```

Do not interrogate runtime metadata for a routine Luna or Terra task just to optimize cost. Missing telemetry is allowed to remain missing.

A covered main session never replaces a required fresh independent Final Review.

## 5. Responsibility packet

A child receives one bounded responsibility, not the raw user task.

Use the smallest packet that makes the responsibility safe and self-contained:

```text
OUTCOME
READ / WRITE SCOPE
INTERFACES AND INVARIANTS
DECISION RIGHTS
ACCEPTANCE
VALID EVIDENCE / DO NOT REDO
CURRENT FAILURE, if any
STOP WHEN
```

Writing roles additionally require a clear acceptance oracle and bounded write scope.

Decision boundaries:

- Reader gathers narrow evidence and does not invent semantics.
- Worker makes local implementation choices only; material semantic judgment returns to main/Sol.
- Solver may make implementation-coupled material choices explicitly inside its granted decision rights.
- Investigator performs bounded read-heavy technical investigation and synthesis after semantics stabilize; if material judgment appears, it returns the decision to main/Sol.
- Advisor resolves one demanding/material judgment or performs fresh independent review and remains read-only.

Children do not widen scope, permission, user intent, external impact, or their own role.

## 6. Return packet

Keep child output compact:

```text
status: complete | blocked
summary
files_changed, if any
verification
new_evidence
remaining_problem
blocker: none | contract | judgment | investigation | stalled
material_decisions, if any
```

A child report is a claim. The main session verifies actual artifact state and relevant checks before acceptance.

## 7. Blocked work means reroute, not escalation

When work is blocked, diagnose what remains.

```text
contract
-> main repairs missing task truth, scope, invariant, or acceptance

judgment
-> main or Sol resolves the demanding/material decision

investigation
-> Terra only when semantics are stable, the work remains read-only, and no material judgment is required

stalled
-> if the same role remains correct, allow at most one clean retry with a materially improved packet
-> otherwise reroute based on the real blocker
```

A failed Luna attempt never directly means "use Terra" or "use a stronger model."

A clean retry carries the current artifact, valid evidence, current failure, a correction hypothesis, acceptance, and explicit DO NOT REDO facts. Do not replay dead-end narration.

## 8. Scheduling

Use the smallest useful safe set of children.

- Explicit `$codex-delegate` use includes up to two concurrently active justified children within the ordinary consent envelope.
- Read-only independent work may run concurrently when native capacity allows.
- One canonical physical checkout has one active writing actor inside the current orchestration. Main-session writes, Luna Worker, and Sol Solver share this ownership domain.
- Concurrent writers require genuinely isolated workspaces or worktrees.
- Process an exposed completion when useful instead of imposing an artificial wave barrier.

## 9. Completion

The main session owns integration and final acceptance.

Normal completion requires the actual requested artifact plus the relevant deterministic or reproducible verification. Model agreement is not verification.

After Candidate Ready, apply `final-review.md` only when the final artifact's consequences require an independent second judgment.
