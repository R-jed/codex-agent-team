# Orchestration Receipt

The receipt makes meaningful Codex Delegate decisions visible without turning normal coding into ceremony.

Emit a receipt when any of these are true:

- the user explicitly invoked `/codex-delegate`;
- at least one child Agent was created;
- a contractability, consent, route, runtime-evidence, or delta-escalation decision materially changed execution.

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
Luna Worker: implemented the bounded retry fix
Reused evidence: E03 reproduction, E07 caller trace
Verification: 38 tests passed
```

## Luna + Sol example

```text
Codex Delegate
Luna Worker: implemented the bounded retry fix
Sol Advisor: reviewed the actual diff because payment-state semantics were high consequence
Reused evidence: E03 reproduction, E07 caller trace, E11 baseline tests
Verification: 38 tests passed
```

## Delta-escalation example

```text
Codex Delegate
Luna Worker: stopped on one unresolved concurrency dependency
Terra Investigator: resolved delta U02 without repeating established repository mapping
Luna Worker: applied the revised bounded contract
Verification: 41 tests passed
```

Rules:

- Do not list Agents that were considered but never spawned.
- Do not imply a fixed Luna -> Terra -> Sol pipeline.
- Mention evidence reuse only for evidence actually carried forward as valid.
- Do not claim runtime evidence that was not observed.
- Use `C1`, `L1`, `R1`, `R2`, or `X0` only when the deterministic verifier established the corresponding compact grade.
- Keep detailed route diagnostics out of the receipt unless they materially affected execution.
- The receipt summarizes orchestration; it never replaces the normal completion report.
