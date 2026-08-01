---
name: codex-agent-team
description: Build the smallest useful native Codex Subagent team for context-heavy execution, real parallelism, or independent verification. Route bounded execution to GPT-5.6 Luna Max, independent review and synthesis to GPT-5.6 Terra XHigh, keep the current root session in control, and request plain-language user consent before material capability, permission, scope, cost, or external-impact escalation.
---

# Codex Agent Team

Use this Skill to decide whether the current task benefits from a small native Subagent team and, when it does, route work by role while keeping the current root session in control.

## Core invariants

1. The current root session owns intent, planning, high-risk decisions, integration, and the final user-facing answer.
2. Zero Subagents is a normal outcome.
3. Default Subagent count is 1, normal maximum is 2, hard maximum is 4.
4. Workers do not create further Subagents.
5. One shared workspace has at most one active writing Worker.
6. Exact native route unavailable means return to Root. Do not randomly switch models.
7. Material capability, permission, scope, cost, or external-impact escalation requires user consent unless the user already clearly authorized it.
8. Role-specific spawns always set `fork_turns` explicitly. Do not rely on the runtime default.

## Step 1: Interpret the root task

Identify the user objective, acceptance criteria, existing authorization, consequence of error, and whether Root can complete the task efficiently without delegation.

If current root model or reasoning effort is observable, record it as runtime context. Do not assume the root model is Sol.

## Step 2: Apply the Delegation Gate

Delegate only when at least one concrete benefit exists:

- **Context isolation**: substantial code, logs, tests, documentation, or tool output would consume Root context for a result that can return as a compact evidence-backed summary.
- **Real parallelism**: two or more independent branches can run concurrently without depending on each other's intermediate results.
- **Independent verification**: a consequential result benefits from review by an Agent that did not produce it.

Insufficient reasons by themselves: task length, file count, apparent difficulty, unused concurrency, a request to be careful, or Luna's lower cost.

If no concrete benefit exists, continue in Root.

## Step 3: Apply the Capability Gate

Before any role-specific spawn, inspect the current native `spawn_agent` contract. Confirm that the required `agent_type` and `fork_turns` surface exists; for model-specific routing, also confirm the target model/effort combination when those overrides are exposed.

Choose exactly one route mode for a child:

### Portable Mode

Use a built-in native role plus explicit model and effort only when the live tool contract exposes and accepts them.

Example shape:

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

### Profile Mode

Use an installed custom Agent profile that already pins model/effort. When the profile owns model and reasoning effort, omit explicit `model` and `reasoning_effort` from the spawn request.

Example shape:

```text
agent_type = luna_worker
fork_turns = none
```

Do not combine a route-pinning custom profile with competing explicit model/effort overrides.

Route resolution priority:

1. Portable Mode when current runtime exposes the exact explicit route.
2. Exact inheritance only when the desired route equals the current Root route and inheritance is part of the live tool contract.
3. Profile Mode when an installed custom Agent profile pins the intended route and its effective permissions are acceptable.
4. Otherwise return that child task to Root with `preferred_route_unavailable`.

Do not use semantic HTTP probes or stale docs as substitutes for current native capability evidence.

## Step 4: Route by responsibility

| Logical responsibility | Native role | Default route | Purpose |
| --- | --- | --- | --- |
| explorer | `explorer` | GPT-5.6 Luna `max` | mapping, search, tracing, evidence collection |
| execution_worker | `worker` | GPT-5.6 Luna `max` | bounded implementation, debugging, testing, local refactor |
| independent_critic | `default` | GPT-5.6 Terra `xhigh` | detached review, synthesis, conflicting evidence, assumption challenge |
| senior_judge | `default` | GPT-5.6 Sol `high` | one-off high-consequence adjudication when Root is not Sol |

Do not create a Sol Worker for routine execution.

Use Terra because independent judgment is valuable, not merely because a task is difficult.

Use Senior Judge only when Root is not already Sol, the decision is consequential, lower routes leave material uncertainty or conflict, and the user consents.

Read `references/routing-policy.md` for detailed triggers and team limits.

## Step 5: Apply the Consent Gate

Do not ask about normal team operations already covered by this Skill and the user's task.

Ask in plain language when the next action materially expands:

- model cost or capability, such as adding a Sol Senior Judge from a non-Sol root
- filesystem or tool permissions
- task scope beyond the user's clear request
- destructive or difficult-to-reverse changes
- production, publication, sending, payment, account, or other external effects
- fan-out beyond the normal two-Agent team unless the user already requested broad parallel work

Explain why the escalation helps, what changes, whether files or external systems will be modified, and the likely cost/risk effect. Consent applies only to the described action.

Read `references/consent-policy.md` when consent may be required.

## Step 6: Build the minimum task packet and context fork

Use `references/task-packet.md`.

Prefer a self-contained packet and minimum history inheritance. For role-specific spawns, always set `fork_turns` explicitly:

- Explorer: `fork_turns = "none"`.
- Independent Critic: `fork_turns = "none"`.
- Execution Worker: `fork_turns = "none"` by default; use a positive integer string only when recent user decisions cannot be safely re-packed.
- Never omit `fork_turns` for a role-specific spawn.
- Never use `fork_turns = "all"` together with `agent_type` on MultiAgentV2.

Every packet must include the prompt-injection boundary and no-further-delegation rule.

## Step 7: Permission and safety checks

Read `references/safety-policy.md` when a Worker may write, handle sensitive material, or consume untrusted content.

Distinguish:

- `runtime_enforced`
- `instruction_enforced`
- `unknown`

Custom Agent profiles may declare sandbox defaults, but effective child permissions are runtime facts. Never treat a profile's sandbox declaration alone as proof of `runtime_enforced` read-only access.

If a task is safe only with enforced read-only access and current runtime cannot confirm it, do not spawn that Worker.

Workers do not perform high-impact external actions.

## Step 8: Execute and verify

After a Worker returns:

1. Check evidence, scope, changed files, tests, uncertainty, and policy violations.
2. Run deterministic verification when available: tests, lint, type checks, schema validation, diff inspection, or reproduction.
3. If evidence is incomplete, allow at most one focused follow-up to the same Worker.
4. If nested delegation is observed, reject the affected result and stop relying on descendants created by that Worker.
5. Root resolves disagreements and owns final acceptance.

## Step 9: Close Workers

Close completed, rejected, or no-longer-needed Workers promptly. Do not keep completed Agents open without a concrete reason.

## References

- `references/routing-policy.md`: team selection, route triggers, capability and context-fork rules
- `references/task-packet.md`: progressive Worker packet and result contract
- `references/consent-policy.md`: plain-language, one-time consent rules
- `references/safety-policy.md`: permission, prompt injection, recursion, side-effect boundaries
