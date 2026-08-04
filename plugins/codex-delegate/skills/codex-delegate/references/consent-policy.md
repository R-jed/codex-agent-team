# Consent Policy

Consent protects meaningful user boundaries without turning ordinary orchestration into repeated prompts. It governs resource expansion, not routing quality or team shape.

## 1. Baseline envelope

Explicit `/codex-delegate` invocation authorizes ordinary bounded orchestration while all of these remain true:

```text
up to 2 concurrently active justified child Agents
at most 1 active writing project Agent per canonical workspace
no permission expansion
no scope expansion
no external side effect
no material compute expansion beyond the requested task's ordinary execution
```

This is an authorization envelope, not a target. Zero children is normal.

A justified Sol capability-uplift child can fit inside this baseline when Routing V4 establishes material judgment that the current main session does not already cover. This includes either:

```text
Sol Advisor for one bounded judgment dependency
Sol Solver for one bounded judgment-coupled implementation dependency
```

The first required fresh Sol Final Review pass can also fit after explicit invocation when it is the ordinary bounded completion dependency for the task.

Do not spend Sol merely because the baseline permits it. A Sol main session normally covers ordinary judgment itself, and routine bounded work does not need a Sol child.

## 2. Sequential calls still count as compute

The two-child baseline limits simultaneous fan-out, not lifetime calls. Later children may run as new dependencies become ready.

However, do not evade consent by serializing an unexpectedly large sequence of expensive calls. Material compute expansion includes patterns such as:

- repeated Sol Solver or Advisor cycles;
- repeated expensive investigation;
- many delegated retries for one unresolved dependency;
- a large new batch of dependencies not implied by the user request.

When the workflow materially exceeds the expected bounded shape, ask before continuing even if only one child is active at a time.

## 3. Implicit invocation

For implicit Skill use, do not silently add a Sol child unless the user's request already clearly authorizes the corresponding stronger judgment/review work.

If material judgment requires Sol capability uplift and authorization is unclear, ask before starting Advisor or Solver. Routine Luna evidence/execution may proceed within the ordinary task authorization when all other boundaries are satisfied.

A required Final Review state does not silently expand implicit-call compute authorization.

## 4. What does not require a new prompt

Do not re-ask for work already covered by the current request and baseline.

Examples:

- a bounded Luna fix and its verification;
- one evidence Reader for a large trace when delegation is useful;
- one justified Sol judgment/solver dependency after explicit `/codex-delegate` invocation;
- one narrow Terra technical investigation that replaces duplicated rework;
- a second independent read-only child within the two-child concurrent envelope;
- the first required fresh Final Review pass after explicit invocation;
- a later child after an earlier child closes when the new dependency is ordinary and the overall compute shape remains bounded.

## 5. What requires consent

Ask before a material boundary change.

### Permission

New write access, privileged tools, workspace-external access, or stronger sandbox capability not already authorized.

### Scope

Work must expand into additional critical modules, public contracts, state transitions, or responsibilities outside the agreed outcome.

### External impact

Publishing, sending, deployment, payment, account changes, destructive deletion, production changes, or equivalent consequential actions not already authorized.

### Larger simultaneous fan-out

More than two concurrently active children normally requires consent unless the user already requested broad parallel work.

Explain the concrete ready dependencies and why concurrency helps. Do not ask abstractly for permission to "use more Agents".

### Material compute expansion

Ask before a workflow turns into repeated expensive investigation, Solver, Advisor, or correction/re-review cycles beyond the ordinary bounded shape.

A single `fix-first` correction plus fresh re-review may remain ordinary after explicit invocation. Repeated loops require renewed consent when they materially expand compute.

## 6. Required Final Review and user choice

Keep quality state separate from compute authorization.

If `review_requirement = required` but the fresh Sol pass is outside the current consent envelope:

1. keep the candidate at Candidate Ready;
2. state the semantic reason independent review is required;
3. ask for the smallest additional consent;
4. if approved, run the fresh review;
5. if declined, report the review as incomplete.

Do not rewrite `review_requirement` to save compute and do not fabricate `ship`.

## 7. How to ask

Explain:

1. what unresolved dependency remains;
2. why the current main/children/evidence cannot satisfy it within the existing envelope;
3. what additional compute, concurrency, permission, scope, or external effect is proposed;
4. what smaller/slower alternative exists when one is meaningful.

Consent applies only to the described expansion. Approval for one fan-out, Solver, review pass, or scope increase does not authorize unrelated later expansion.
