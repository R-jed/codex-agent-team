# Consent Policy

## 1. Purpose

Consent Gate protects meaningful boundaries without turning normal Codex work into repeated permission questions.

The user should understand the practical effect of the next action. Internal route IDs and policy booleans are secondary.

## 2. Baseline orchestration envelope

When the user has enabled this Skill for an in-scope task, the normal orchestration envelope is already authorized:

```text
0-1 Luna Explorer or Worker when Delegation Gate has concrete value
+ at most 1 risk-triggered Terra Independent Critic when Review Gate has concrete value
```

This normal envelope does not require a separate consent prompt. The Skill still applies Minimum Team and does not add Terra merely because capability or concurrency is available.

A Sol Senior Judge is outside the baseline envelope when Root is not Sol and always requires the consent conditions below.

## 3. What does not require a new prompt

Do not ask again for actions already clearly authorized by the current user request.

Examples:

- "Fix this bug and run tests" authorizes normal in-scope edits and tests.
- "Review this branch" authorizes read-only inspection and ordinary verification commands that fit the current runtime permissions.
- Normal Luna Worker or risk-triggered Terra Critic creation inside the baseline envelope does not require a separate consent prompt.

## 4. What requires consent

Ask before a material expansion beyond the baseline envelope.

### Capability or cost

Example: Root is Luna and a one-time Sol Senior Judge would materially improve a high-consequence unresolved decision.

### Permission

Example: the task began as analysis and now requires file writes, privileged tools, workspace-external access, or stronger sandbox permissions.

### Scope

Example: the user asked for a local bug fix but a complete solution requires changing additional critical modules or public contracts.

### External impact

Always keep publishing, sending, payment, account changes, production changes, destructive deletion, or similarly consequential external actions with Root and obtain clear authorization when the current request did not already grant it.

### Large fan-out

A team larger than the normal two-child maximum should normally ask first unless the user explicitly requested broad parallel analysis.

## 5. How to ask

Use plain language and answer four questions:

1. Why is this useful now?
2. What exactly will change?
3. Will files or external systems be modified?
4. What additional cost or risk should the user expect?

Keep the question short. Offer a safe alternative when practical.

Bad:

```text
Enable allow_upscale=true?
```

Better:

```text
The two independent analyses disagree on a decision that affects the whole implementation. I recommend one stronger model pass to break the tie. It will only analyze the evidence, will not modify files, and will use additional model capacity. Continue?
```

## 6. One-time scope

Consent applies only to the described action.

Approval for one Sol review does not authorize future Sol reviews automatically.

Approval to modify the named files does not authorize unrelated modules.

Approval to prepare a deployment does not imply approval to deploy it.

If the next step crosses another material boundary, ask again.

## 7. Examples

### Analysis to write

```text
I found the cause. Fixing it requires changes to three project files and then running the existing tests. I have not changed anything yet. Should I apply the fix?
```

### Scope expansion

```text
A local patch can stop the immediate error, but a complete fix also needs a change in the session compatibility layer. That is broader than the original issue. Should I make the complete fix or keep the change local?
```

### High-impact operation

```text
The next step would run a database migration that can affect existing data. I can first inspect the migration plan and backup status, then return for confirmation before any migration runs.
```
