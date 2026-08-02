---
name: codex-agent-team
description: Build the smallest useful native Codex Subagent team for context-heavy execution, real parallelism, or independent verification. Route bounded execution to GPT-5.6 Luna Max, independent review and synthesis to GPT-5.6 Terra XHigh, keep the current root session in control, and request plain-language user consent before material capability, permission, scope, cost, or external-impact escalation.
---

# Codex Agent Team

Use this Skill as a policy layer over Codex Native Subagents. The Skill does not create a parallel agent runtime. It decides when to call the native `spawn_agent` tool, which exact route is acceptable, how much context the child receives, how results are verified, and when the user must approve an escalation.

## Core invariants

1. The current Root owns intent, planning, high-risk decisions, integration, and the final user-facing answer.
2. Zero Subagents is a normal outcome. Default child count is 1, normal maximum is 2, hard maximum is 4.
3. Model-specific children require a provable configuration route. An unverified route returns to Root.
4. Luna Max is the default execution route; Terra XHigh is the selective independent-judgment route; Sol High is a consent-gated Senior Judge when Root is not Sol.
5. Workers do not create further Subagents.
6. One shared workspace has at most one active writing Worker.
7. Role-specific spawns always set `fork_turns` explicitly.
8. Material capability, permission, scope, cost, or external-impact escalation requires user consent unless already clearly authorized.
9. Role-to-route bindings are fixed; team composition is dynamic. The Skill does not silently change the current Root model or reasoning effort.
10. Configuration assurance and runtime observation are separate facts. Never relabel configured values as observed telemetry.
11. Worker reports are claims. Root accepts work from actual artifacts, deterministic verification, and reproducible evidence.

## Step 1: Interpret the Root task

Identify the user objective, acceptance criteria, existing authorization, consequence of error, and whether Root can complete the task efficiently without delegation.

If Root model or reasoning effort is observable, record it as runtime context. Do not assume Root is Sol.

## Step 2: Apply the Delegation Gate

Delegate only when at least one concrete benefit exists:

- **Context isolation**: noisy code, logs, tests, documents, or tool output can stay outside Root and return as compact evidence.
- **Real parallelism**: independent branches can make progress concurrently without waiting on each other's intermediate conclusions.
- **Independent verification**: a consequential result benefits from a detached reviewer that did not produce it.

Task length, file count, apparent difficulty, spare concurrency, or Luna's lower price do not justify delegation by themselves.

If no concrete benefit exists, continue in Root.

## Step 3: Apply the Route Assurance Gate

Before any model-specific child is spawned, inspect the live native `spawn_agent` contract and role guidance.

Track route intent, accepted configuration, and runtime observation separately:

```text
preferred_route
configured_route
route_assurance
observed_route
```

A successful exact spawn can establish `configured_route`, while `observed_route` may still be `not_exposed`. Never copy the preferred or configured route into the observed route.

A child route is allowed only with one of these configuration-assurance states:

### A. Profile Locked (Profile Mode)

Prefer an installed project profile when the live role guidance confirms that the profile pins the intended model and reasoning effort.

Example:

```text
agent_type = luna_worker
fork_turns = none
```

The profile owns `model` and `model_reasoning_effort`; omit competing explicit overrides.

Expected locked routes:

```text
luna_explorer -> gpt-5.6-luna / max
luna_worker   -> gpt-5.6-luna / max
terra_reviewer -> gpt-5.6-terra / xhigh
sol_judge     -> gpt-5.6-sol / high
```

Record `route_assurance = profile_locked`.

### B. Native Explicit Validated (Portable Mode)

When no exact profile is installed, use a built-in native role plus explicit `model` and `reasoning_effort` only when the live tool exposes the required `agent_type`, `fork_turns`, `model`, and `reasoning_effort` surface and the selected role is not locked to an incompatible route.

Example:

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

Codex validates the requested model against the available MultiAgent backend models and validates the effort against that model before spawning. A rejected tuple is a failed route, not a reason to improvise another model.

Record `route_assurance = native_explicit_validated` only after the native spawn accepts the exact request.

### Effective selection precedence

Current Codex resolves model and reasoning settings with this precedence when a custom Agent is involved:

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Model and reasoning effort resolve independently. Profile Mode and Portable Mode are alternative route paths; do not combine a route-pinning profile with competing explicit model/effort overrides.

### Do not treat inheritance as exact assurance

Do not use omitted `model` or `reasoning_effort` as proof of a model-specific route. Current Codex can apply configured default Subagent model/effort values before role configuration. If explicit overrides are hidden and no exact locked profile is available, return the child task to Root with `preferred_route_unavailable`.

Read `references/routing-policy.md` for the detailed routing contract and `references/runtime-assurance.md` for optional post-spawn attestation. Repository-level design notes are documentation only and are not required by the installed Skill.

## Step 4: Route by responsibility

| Responsibility | Portable native role | Default route | Purpose |
| --- | --- | --- | --- |
| explorer | `explorer` | GPT-5.6 Luna `max` | mapping, search, tracing, evidence collection |
| execution_worker | `worker` | GPT-5.6 Luna `max` | bounded implementation, debugging, testing, local refactor |
| independent_critic | `default` | GPT-5.6 Terra `xhigh` | detached review, synthesis, conflicting evidence, assumption challenge |
| senior_judge | `default` | GPT-5.6 Sol `high` | one-off high-consequence adjudication when Root is not Sol |

Do not create a Sol Worker for routine execution. Use Terra because independent judgment has concrete value, not because a task merely looks difficult.

## Step 5: Apply the Consent Gate

Normal in-scope teamwork does not require repeated prompts.

Ask in plain language when the next action materially expands:

- model cost or capability, such as a one-time Sol Senior Judge from a non-Sol Root
- filesystem or tool permissions
- task scope beyond the user's clear request
- destructive or difficult-to-reverse changes
- production, publication, sending, payment, account, or other external effects
- fan-out beyond the normal two-child team unless the user already requested broad parallel work

Explain why the escalation helps, what changes, whether files or external systems will be modified, and the likely cost/risk effect. Consent applies only to the described action.

## Step 6: Build the minimum task packet and context fork

Use `references/task-packet.md`. For bounded coding work, use its Implementation Preset when that is more precise than the generic packet.

For role-specific spawns, always set `fork_turns` explicitly:

- Explorer: `fork_turns = "none"`.
- Independent Critic: `fork_turns = "none"`.
- Execution Worker: `fork_turns = "none"` by default; use a positive integer only when recent user decisions cannot be safely repacked.
- Never omit `fork_turns` for a role-specific spawn.
- Never combine `fork_turns = "all"` with an `agent_type` override on MultiAgentV2.

Every packet includes the prompt-injection boundary and no-further-delegation rule.

## Step 7: Permission and safety checks

Use `references/safety-policy.md` when a Worker may write, handle sensitive material, or consume untrusted content.

Distinguish `runtime_enforced`, `instruction_enforced`, and `unknown`. A profile sandbox declaration is a default configuration value, not proof of effective runtime enforcement.

If a task is safe only with enforced read-only access and current runtime cannot confirm it, keep the task in Root.

## Step 8: Execute, observe, and verify

After a Subagent returns:

1. Treat the child report as a claim, not self-validating evidence.
2. Inspect actual files, diff, scope, commands, tests, uncertainty, `judgment_calls`, and policy violations.
3. Rerun deterministic verification when available.
4. Obtain runtime observation when exposed. For ordinary tasks, missing telemetry may remain `not_exposed`; when safety or a high-consequence independence claim depends on effective route or sandbox, apply `references/runtime-assurance.md` as an acceptance requirement.
5. If native metadata and local rollout evidence both exist, require agreement on overlapping fields.
6. Allow at most one focused follow-up to the same child when evidence is incomplete.
7. Reject or quarantine affected results when route observation conflicts, unexpected mutation occurs, or nested delegation is observed.

## Step 9: Apply the Review Gate

Detached review is risk-triggered, not mandatory for every implementation.

Add one Terra Independent Critic when fresh judgment materially improves acceptance, especially for:

- security, permission, concurrency, or state-consistency logic;
- cross-module invariants, public contracts, migrations, or wide blast radius;
- weak deterministic oracles where tests alone do not establish correctness;
- substantial Worker `judgment_calls` outside mechanical execution;
- conflicting evidence or a consequential assumption that should be challenged independently.

Do not add Terra merely because the task was long or difficult. Give the critic the actual artifact or diff, objective, constraints, verification evidence, and material assumptions without the producer's private reasoning.

The critic returns one review status:

```text
clear
findings
insufficient_evidence
```

Root still owns acceptance. Bounded findings return to the Worker or Root for correction and deterministic re-verification. A fresh Terra review is required only when the correction materially changes the reviewed risk. If a high-consequence conflict remains unresolved and Root is not Sol, the Consent Gate may authorize one Sol Senior Judge.

## Step 10: Close Subagents

Close completed, rejected, or no-longer-needed Subagents promptly so they do not continue occupying concurrency.

## References

- `references/routing-policy.md`: team selection, route assurance, context fork, review gate, failure behavior
- `references/runtime-assurance.md`: post-spawn route and permission observation
- `references/task-packet.md`: progressive child packet, implementation preset, and route record
- `references/consent-policy.md`: plain-language one-time consent
- `references/safety-policy.md`: permissions, prompt injection, recursion, side effects
