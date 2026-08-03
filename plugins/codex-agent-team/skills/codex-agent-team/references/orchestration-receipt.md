# Orchestration Receipt

The receipt makes meaningful Codex Delegate decisions visible without turning normal coding into ceremony.

Emit a receipt when any of these are true:

- the user explicitly invoked `/codex-delegate`;
- at least one child Agent was created;
- a contractability, consent, route, runtime-capacity, execution-recovery, or delta-escalation decision materially changed execution.

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

## Clean-restart example

```text
Codex Delegate
Luna Worker: D03 stalled on the same failing verification without new evidence
Recovery: restarted D03 in fresh Luna context with the current artifact, valid evidence, and DO NOT REDO facts
Verification: the failure signature changed and the dependency advanced
```

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
Terra Investigator: resolved only D04 using the existing reproduction and caller evidence
Luna Worker: applied the revised bounded contract
Verification: 41 tests passed
```

Rules:

- Do not list Agents that were considered but never spawned.
- Do not imply a fixed Luna -> Terra -> Sol pipeline or fixed Agent count.
- Mention broader fan-out only when it actually affected scheduling or consent.
- Mention evidence reuse only for evidence actually carried forward as valid.
- A file write or Agent self-report is not evidence of progress by itself.
- Do not claim runtime capacity, route, permission, or ancestry evidence that was not observed.
- Use `C1`, `L1`, `R1`, `R2`, or `X0` only when the deterministic verifier established the corresponding compact grade.
- Keep detailed route diagnostics out of the receipt unless they materially affected execution.
- The receipt summarizes orchestration; it never replaces the normal completion report.
