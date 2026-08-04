# Consent Policy

## 1. Purpose

Consent protects meaningful user boundaries without turning ordinary orchestration into repeated prompts.

The user should understand practical changes in scope, permission, external impact, concurrent fan-out, or material model cost.

Consent is a resource boundary. It is not the scheduler and does not define the total number of Agents a task may ever use.

## 2. Baseline resource envelope

When the user explicitly invokes `/codex-delegate`, ordinary orchestration may proceed without another prompt while all of these remain true:

```text
up to 2 concurrently active justified child Agents
at most 1 active writer per canonical workspace
no permission expansion
no scope expansion
no external side effect
no material compute expansion beyond the task's ordinary bounded execution
```

The exact team shape is dynamic. Examples that may fit inside the baseline when justified:

```text
Luna only
Luna Reader + Luna Worker
Luna + Terra delta investigation
Luna + Sol selective review
Terra + Luna
Sol only
```

Zero Agents is normal. One Agent is not a required default. Two Agents is not a goal.

The baseline count applies to simultaneously active fan-out, not to the lifetime number of child calls. A later child may run after an earlier dependency completes when the new child satisfies a new ready dependency and does not create material compute expansion.

A single read-only Sol advisor may fit inside the explicit `/codex-delegate` baseline when it satisfies a distinct judgment or review dependency. This includes the first risk-triggered Final Review Gate pass when that gate is required by the current deliverable.

For implicit Skill invocation, ask before adding Sol unless the current user request already clearly authorizes stronger model review. A risk-triggered Final Review Gate does not silently expand implicit-call compute authorization.

## 3. What does not require a new prompt

Do not ask again for actions already clearly authorized by the current request and baseline envelope.

Examples:

- "Fix this bug and run tests" authorizes ordinary in-scope edits and verification.
- "Review this branch carefully" can authorize one justified read-only Sol review when the Skill was explicitly invoked.
- Two independent read-only branches may run concurrently when they satisfy different ready dependencies.
- A Terra delta investigation does not require a separate prompt when it remains read-only, bounded, and replaces duplicated rework.
- A third child may run later after prior children close when it satisfies a newly ready dependency and the overall compute shape remains ordinary for the requested task.
- After explicit `/codex-delegate` invocation, one required fresh Sol Final Review Gate pass can proceed without another prompt when it remains the ordinary bounded completion dependency for the task.

## 4. What requires consent

Ask before a material boundary change.

### Permission

Write access, privileged tools, workspace-external access, or stronger sandbox capability that the task did not already authorize.

### Scope

A local task requires changes to additional critical modules, public contracts, data migrations, or other responsibilities outside the agreed outcome.

### External impact

Publishing, sending, deployment, payment, account changes, destructive deletion, production changes, or similarly consequential actions remain with the main session and require clear authorization when not already granted.

### Larger simultaneous fan-out

More than two concurrently active child Agents normally requires consent unless the user explicitly requested broad parallel work.

Before asking, the main session should identify the ready dependencies and explain why concurrent execution materially helps. Do not ask for abstract permission to "use more Agents" without a concrete scheduling reason.

After approval, actual concurrency is bounded by justified ready dependencies, workspace safety, and native runtime capacity. Codex Delegate does not add another numerical hard ceiling.

### Material compute expansion

Ask when execution would materially exceed the expected bounded resource shape even if it remains serial. Examples include repeated expensive investigation/review passes, many sequential delegated retries, or a large new batch of dependencies that was not implied by the user's request.

Do not evade this gate by keeping only two Agents active at a time while silently creating an unexpectedly large sequence of child calls.

A `fix-first` verdict invalidates the old final review and requires a new fresh review after correction. One bounded correction-and-re-review cycle may remain ordinary execution after explicit `/codex-delegate` invocation. Repeated Sol review cycles that materially expand compute cross this consent boundary; the Final Review Gate does not authorize unlimited reviewer retries.

## 4A. Consent interaction with a required Final Review Gate

Keep quality state separate from compute authorization.

```text
review_requirement = required
```

means independent final review is part of Codex Delegate's quality policy for the candidate. It does not by itself prove that an otherwise-unapproved Sol call may be started.

If the required Sol call is outside the current consent envelope:

1. keep the candidate at **Candidate Ready**;
2. explain why the semantic gate requires independent review and what additional Sol call is proposed;
3. ask for the smallest consent needed for that review pass;
4. if approved, run the fresh review normally;
5. if declined, do not downgrade `review_requirement`, do not fabricate `ship`, and do not claim the Final Review Gate succeeded.

When the user declines the additional review, the main session may hand off the verified candidate with an explicit receipt that independent final review was declined or remains incomplete. User choice controls compute use; it does not rewrite the historical fact that the configured quality gate was unsatisfied.

## 5. How to ask

Use plain language and answer:

1. What unresolved dependencies are ready?
2. Why can existing evidence or current Agents not satisfy them cheaply enough?
3. What new concurrency, scope, permission, external effect, or compute cost is being added?
4. What safe slower or smaller alternative exists?

Bad:

```text
Enable higher capability?
```

Better:

```text
Five independent read-only checks are ready and none depends on the others. Running them together would shorten the critical path, but it exceeds the normal two-child concurrent envelope. No files or external systems will be changed. I can run them concurrently if the runtime has capacity, or process them in smaller waves. Allow the larger fan-out?
```

For a required review outside the current envelope, be specific:

```text
The implementation and deterministic checks are complete, but this change crosses a public API boundary, so the Final Review Gate requires one fresh read-only Sol review before I can claim the quality gate passed. Allow that additional review pass?
```

## 6. One-time scope

Consent applies only to the described expansion.

Approval for one larger fan-out does not authorize unrelated later fan-out. Approval for one additional Sol pass does not authorize repeated Sol retries. Approval to broaden one module does not authorize unrelated modules. Approval to prepare an external action does not authorize executing it.

When the approved fan-out has completed or its dependency frontier changes materially, return to the normal consent model.
