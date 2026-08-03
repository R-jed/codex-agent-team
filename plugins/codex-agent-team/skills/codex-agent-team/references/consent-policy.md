# Consent Policy

## 1. Purpose

Consent protects meaningful user boundaries without turning ordinary orchestration into repeated prompts.

The user should understand practical changes in scope, permission, external impact, fan-out, or material model cost.

## 2. Baseline resource envelope

When the user explicitly invokes `/codex-delegate`, the normal orchestration envelope is:

```text
0-2 justified child Agents
at most 1 active writer per shared workspace
no permission expansion
no scope expansion
no external side effect
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

No Agent is mandatory, and using two Agents is not a goal by itself.

A single read-only Sol advisor may fit inside the explicit `/codex-delegate` baseline when it satisfies a distinct judgment or review dependency. Do not ask again merely because the selected tier is Sol.

For implicit Skill invocation, ask before adding Sol unless the current user request already clearly authorizes a stronger model review.

## 3. What does not require a new prompt

Do not ask again for actions already clearly authorized by the current request and baseline envelope.

Examples:

- "Fix this bug and run tests" authorizes ordinary in-scope edits and verification.
- "Review this branch carefully" can authorize one justified read-only Sol review when the Skill was explicitly invoked.
- Two independent read-only branches may run concurrently when they satisfy different dependencies and remain inside the normal two-child envelope.
- A Terra delta investigation does not require a separate prompt when it remains read-only, bounded, and replaces duplicated rework.

## 4. What requires consent

Ask before a material boundary change.

### Permission

Write access, privileged tools, workspace-external access, or stronger sandbox capability that the task did not already authorize.

### Scope

A local task requires changes to additional critical modules, public contracts, data migrations, or other responsibilities outside the agreed outcome.

### External impact

Publishing, sending, deployment, payment, account changes, destructive deletion, production changes, or similarly consequential actions remain with the main session and require clear authorization when not already granted.

### Large fan-out

More than two child Agents normally requires consent unless the user explicitly requested broad parallel work.

### Material compute expansion

Ask when orchestration would exceed the normal enabled envelope, such as repeated Sol calls, multiple expensive investigation branches, or a retry pattern that materially changes expected cost without a new dependency.

## 5. How to ask

Use plain language and answer:

1. What unresolved dependency remains?
2. Why can existing evidence or current Agents not satisfy it?
3. What new scope, permission, external effect, or compute cost is being added?
4. What safe alternative exists?

Bad:

```text
Enable higher capability?
```

Better:

```text
The implementation is complete, but the change alters a public authentication contract and deterministic tests cannot answer the compatibility tradeoff. I recommend one read-only Sol review of the diff and evidence. No files or external systems will be changed. Continue?
```

## 6. One-time scope

Consent applies only to the described expansion.

Approval for one additional Sol pass does not authorize repeated Sol retries. Approval to broaden one module does not authorize unrelated modules. Approval to prepare an external action does not authorize executing it.
