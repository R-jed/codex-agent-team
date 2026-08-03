# Orchestration Receipt

The receipt makes meaningful Codex Delegate decisions visible without turning normal coding into ceremony.

Emit a receipt when any of these are true:

- the user explicitly invoked `/codex-delegate`;
- at least one child Agent was created;
- a contractability, consent, route, runtime-capacity, intervention, execution-recovery, or delta-escalation decision materially changed execution.

For an implicit trivial task that stays in the main session, omit the receipt unless the user asks for orchestration details.

Use **main session** in user-visible copy. Internal architecture terminology should not be required vocabulary for ordinary users.

## Main-session-only example

```text
Codex Delegate: Main session only
Why: the change was already isolated and delegation added no useful dependency
Verification: 12 tests passed
```

## Luna-only example

```text
Codex Delegate
Luna Worker: implemented dependency D01, the bounded retry fix
Reused evidence: E03 reproduction, E07 caller trace
Verification: 38 tests passed
```

## Adaptive parallel example

```text
Codex Delegate
Ready dependencies: 5 independent read-only checks
Consent: broader fan-out approved
Runtime: 3 child slots were available; 2 checks waited for a slot
Duplicate dependency calls: 0
```

Do not present an observed slot count as a universal Codex limit.

## Continue-without-intervention example

```text
Codex Delegate
Luna Worker: D03 still has one failing acceptance check
Intervention: none
Why: new deterministic evidence narrowed the root cause and the unresolved delta is smaller
```

A failing check does not automatically justify a restart or stronger lane.

## Clean-restart example

```text
Codex Delegate
Luna Worker: D03 stalled on the same failing verification without new evidence
Recovery: restarted D03 in fresh Luna context with the current artifact, valid evidence, material recovery history, and DO NOT REDO facts
Decision source: deterministic evidence
Verification: the failure signature changed and the dependency advanced
```

## Policy-transform example

Use this only when the proposed and effective actions materially differ:

```text
Codex Delegate
Proposed action: Terra escalation
Effective action: continue Luna with a focused correction
Decision source: main-session judgment
Policy transform: capability gap was not established by the available evidence
```

Do not surface proposed/effective action fields when they add no useful explanation.

## Luna + Sol example

```text
Codex Delegate
Luna Worker: implemented the bounded retry fix
Sol Advisor: reviewed the actual diff in fresh context because payment-state semantics were high consequence
Reused evidence: E03 reproduction, E07 caller trace, E11 baseline tests
Verification: 38 tests passed
```

## Delta-escalation example

```text
Codex Delegate
Luna Worker: stopped on unresolved concurrency dependency D04
Terra Investigator: resolved only D04 using the existing reproduction, caller evidence, and material recovery history
Luna Worker: applied the revised bounded contract
Verification: 41 tests passed
```

Rules:

- Do not list Agents that were considered but never spawned.
- Do not imply a fixed Luna -> Terra -> Sol pipeline or fixed Agent count.
- Mention broader fan-out only when it actually affected scheduling or consent.
- Mention evidence reuse only for evidence actually carried forward as valid.
- A file write, successful command, or Agent self-report is not evidence of progress by itself.
- Acceptance failure is not automatically an intervention trigger; mention intervention only when the Intervention Gate materially changed execution.
- When a proposed action differs from the effective action, the effective action belongs to the main session after policy/runtime gates.
- `model_judgment` is never displayed as deterministic evidence.
- Do not claim child mid-run observability, runtime capacity, route, permission, or ancestry evidence that was not observed.
- Use `C1`, `L1`, `R1`, `R2`, or `X0` only when the deterministic verifier established the corresponding compact grade.
- Keep detailed route diagnostics and Recovery Ledger internals out of the receipt unless they materially affected execution.
- The receipt summarizes orchestration; it never replaces the normal completion report.
