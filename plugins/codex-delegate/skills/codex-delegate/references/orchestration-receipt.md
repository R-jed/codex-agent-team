# Orchestration Receipt

The receipt makes material Codex Delegate decisions visible without turning ordinary coding into ceremony.

Emit one when:

- the user explicitly invoked `/codex-delegate`;
- at least one child was created;
- main-session judgment coverage materially changed Sol placement;
- dependency reclassification materially changed execution;
- consent, route, runtime, recovery, or Final Review materially affected completion.

For trivial implicit main-session-only work, omit it unless requested.

Use **main session** in user-visible copy.

## Main-session-only

```text
Codex Delegate: Main session only
Why: the dependency was already isolated and delegation added no useful value
Verification: 12 tests passed
```

## Sol main avoided redundant Sol delegation

```text
Codex Delegate
Main judgment coverage: covered by current Sol session
Routing: architecture decision and judgment-coupled implementation stayed in the main session
Extra Sol capability-uplift calls: 0
Verification: 31 tests passed
```

Do not claim this unless trusted current-session metadata actually established coverage.

## Luna bounded execution

```text
Codex Delegate
Luna Worker: completed D01, bounded retry implementation
Reused evidence: E03 reproduction, E07 caller trace
Verification: 38 tests passed
```

## Sol Solver

```text
Codex Delegate
Main judgment coverage: uncovered
Sol Solver: completed D04 because implementation required material compatibility judgment that could not be separated from the write
Material judgment calls: preserved legacy fallback order; kept public response shape unchanged
Verification: 52 tests passed
```

## Reclassification

```text
Codex Delegate
D03 started as bounded execution
New evidence: implementation exposed an unresolved cache-invalidation semantic decision
Reclassified: judgment_coupled_execution
Effective actor: Sol Solver
```

A weak Luna result alone is not a reclassification reason. Report the evidence that changed the dependency kind.

## Technical investigation

```text
Codex Delegate
D05: semantic intent was already resolved
Terra Investigator: resolved only the remaining lock-order technical uncertainty
Returned evidence was reused by the writing dependency
```

Do not describe Terra as a generic escalation or stronger retry.

## Parallel evidence

```text
Codex Delegate
Ready dependencies: 5 independent read-only checks
Consent: broader fan-out approved
Runtime: 3 child slots observed; 2 checks queued
Duplicate dependency calls: 0
```

Never present one observed slot count as a universal Codex limit.

## Continue without intervention

```text
Codex Delegate
D03 still has one failing acceptance check
Intervention: none
Why: new deterministic evidence narrowed the cause and the unresolved delta is smaller
```

## Clean same-role restart

```text
Codex Delegate
D03 classification remained bounded_execution but repeated the same factual failure without new evidence
Recovery: fresh Luna context with current artifact, valid evidence, failure signature, and DO NOT REDO facts
```

## Required Final Review

```text
Codex Delegate
Review requirement: required
Why: public_contract_change
Candidate verification: 64 tests passed
Final Review: fresh Sol Advisor reviewed artifact sha256:A17F...
Verdict: ship
Artifact unchanged after review: yes
```

Process history such as Terra use, Solver use, recovery, or a large diff must not be listed as an automatic review reason. If it created material residual uncertainty, record the actual semantic trigger such as `verification_gap`.

## Required review incomplete

```text
Codex Delegate
Review requirement: required
Candidate verification: 64 tests passed
Final Review: incomplete
Reviewer outcome: INSUFFICIENT_EVIDENCE
Missing evidence: rollback behavior for partial state transition
State: Candidate Ready
```

or, when consent is declined:

```text
Codex Delegate
Review requirement: required
Final Review: incomplete
Consent: additional Sol review declined
State: Candidate Ready; independent assurance not satisfied
```

## Rules

- List only Agents actually spawned.
- Do not imply a fixed model pipeline or model escalation ladder.
- Do not claim a Sol capability-uplift call was necessary when main-session coverage already supplied that capability.
- A file write, successful irrelevant command, confidence statement, or child self-report is not progress evidence.
- Show reclassification only when new evidence changed the dependency kind or contract truth.
- Keep proposed child actions separate from the main session's effective action when they differ materially.
- `model_judgment` is never deterministic evidence.
- Do not claim runtime route, permission, ancestry, capacity, main-session model, or progress observability that was not observed.
- A required Final Review succeeds only with fresh Sol `ship` for the unchanged current artifact.
- The receipt summarizes orchestration; it does not replace the task completion report.
