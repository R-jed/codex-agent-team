# Orchestration Receipt

The receipt makes Agent Team decisions visible without turning normal coding into ceremony.

Emit a receipt when any of these are true:

- the user explicitly invoked `$codex-agent-team`;
- at least one child Agent was created;
- a Review Gate, Consent Gate, route failure, or runtime-evidence decision materially changed execution.

For an implicit invocation that stays Root-only on a trivial isolated task, omit the receipt unless the user asks for orchestration details.

Keep the receipt compact. Report only facts established during the task.

## Root-only example

```text
Agent Team: Root only
Why: change already isolated; delegation had no concrete benefit
Verification: 12 tests passed
```

## Delegated example

```text
Agent Team
Luna Worker: implemented bounded auth refresh change
Terra Reviewer: triggered by security boundary; verdict clear
Runtime evidence: Luna R1, Terra R2
Verification: 38 tests passed
```

Rules:

- Do not list Agents that were considered but never spawned.
- Do not claim runtime evidence that was not observed.
- Use `C1`, `L1`, `R1`, `R2`, or `X0` only when the corresponding runtime-assurance grade was actually established.
- State `not_exposed` when runtime observation was required for the explanation but unavailable.
- Keep detailed route diagnostics out of the receipt unless a mismatch or fallback affected the result.
- The receipt summarizes orchestration; it never replaces the normal user-facing completion report.
