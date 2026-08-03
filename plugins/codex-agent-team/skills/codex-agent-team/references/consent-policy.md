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

A single read-only Sol advisor may fit inside the explicit `/codex-delegate` baseline when it satisfies a distinct judgment or review dependency.

For implicit Skill invocation, ask before adding Sol unless the current user request already clearly authorizes stronger model review.

## 3. What does not require a new prompt

Do not ask again for actions already clearly authorized by the current request and baseline envelope.

Examples:

- "Fix this bug and run tests" authorizes ordinary in-scope edits and verification.
- "Review this branch carefully" can authorize one justified read-only Sol review when the Skill was explicitly invoked.
- Two independent read-only branches may run concurrently when they satisfy different ready dependencies.
- A Terra delta investigation does not require a separate prompt when it remains read-only, bounded, and replaces duplicated rework.
- A third child may run later after prior children close when it satisfies a newly ready dependency and the overall compute shape remains ordinary for the requested task.

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

## 6. One-time scope

Consent applies only to the described expansion.

Approval for one larger fan-out does not authorize unrelated later fan-out. Approval for one additional Sol pass does not authorize repeated Sol retries. Approval to broaden one module does not authorize unrelated modules. Approval to prepare an external action does not authorize executing it.

When the approved fan-out has completed or its dependency frontier changes materially, return to the normal consent model.
