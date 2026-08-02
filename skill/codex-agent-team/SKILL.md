---
name: codex-agent-team
description: Build the smallest useful native Codex Subagent team for context-heavy execution, real parallelism, or independent verification. Keep the current Root session in control, route bounded execution to GPT-5.6 Luna Max, independent review to GPT-5.6 Terra XHigh, and request plain-language user consent before material capability, permission, scope, cost, or external-impact escalation.
---

# Codex Agent Team

Use this Skill as a policy layer over Codex Native Subagents. Code normally: it decides whether any Subagent is worth creating, which exact route is acceptable, what evidence is required after spawn, how results are verified, and when user consent is required.

## Core invariants

1. The current Root owns intent, planning, high-risk decisions, integration, and the final user-facing answer.
2. Zero Subagents is a normal outcome. Default child count is 1, normal maximum is 2, hard maximum is 4.
3. Model-specific children require a provable configuration route. An unverified route returns to Root.
4. Luna Max is the default execution route; Terra XHigh is the selective independent-judgment route; Sol High is a consent-gated Senior Judge when Root is not Sol.
5. Workers do not create further Subagents.
6. One shared workspace has at most one active writing Worker.
7. Role-specific spawns always set `fork_turns` explicitly.
8. Material permission, scope, external-impact, large-fanout, or out-of-envelope capability/cost escalation requires user consent unless already clearly authorized.
9. Role-to-route bindings are fixed; team composition is dynamic. The Skill does not silently change the current Root model or reasoning effort.
10. Configuration assurance and runtime observation are separate facts. Never relabel configured values or mutable local records as authoritative runtime telemetry.
11. Worker reports are claims. Root accepts work from actual artifacts, deterministic verification, and reproducible evidence.

## 1. Interpret the Root task

Identify the user objective, acceptance criteria, existing authorization, consequence of error, and whether Root can complete the task efficiently without delegation. Do not assume Root is Sol.

## 2. Delegation Gate

Delegate only when at least one concrete benefit exists:

- **Context isolation**: noisy code, logs, tests, documents, or tool output can stay outside Root and return as compact evidence.
- **Real parallelism**: independent branches can progress concurrently.
- **Independent verification**: a consequential result benefits from a reviewer that did not produce it.

Task length, file count, apparent difficulty, spare concurrency, or Luna's lower price do not justify delegation by themselves. If no concrete benefit exists, continue in Root.

## 3. Route Assurance Gate

Before a model-specific child is spawned, inspect the live native `spawn_agent` contract and role guidance.

Keep these facts separate:

```text
preferred_route
configured_route
route_assurance
observed_route
```

### Profile Mode

Prefer an installed project profile when live role guidance confirms that it pins the intended model and reasoning effort.

```text
luna_explorer   -> gpt-5.6-luna / max
luna_worker     -> gpt-5.6-luna / max
terra_reviewer  -> gpt-5.6-terra / xhigh
sol_judge       -> gpt-5.6-sol / high
```

Record `route_assurance = profile_locked`. This is configuration assurance only; it does not prove the effective post-spawn route.

Example:

```text
agent_type = luna_worker
fork_turns = none
```

Do not combine a route-pinning profile with competing explicit model/effort overrides.

When installed as a Plugin, custom Agent profiles are a separate companion setup. If the project-specific role names are missing, tell the user to invoke `$codex-agent-team-setup`, complete its exactness check, then start a fresh Codex task. Do not imply that Plugin installation alone registers the custom Agent TOML files.

### Portable Mode

When no exact profile is installed, use a built-in native role plus explicit `model` and `reasoning_effort` only when the live tool exposes `agent_type`, `fork_turns`, `model`, and `reasoning_effort`, the selected role is not locked to an incompatible route, and Codex accepts the exact tuple.

```text
agent_type = worker
model = gpt-5.6-luna
reasoning_effort = max
fork_turns = none
```

Record `route_assurance = native_explicit_validated` only after the exact request is accepted.

### Effective selection precedence

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Model and reasoning effort resolve independently.

### No inheritance assumption

Do not use omitted `model` or `reasoning_effort` as proof of a model-specific route. If explicit overrides are hidden and no exact locked profile is available, return the child task to Root with `preferred_route_unavailable`.

Read `references/routing-policy.md` for full route and fallback rules.

## 4. Route by responsibility

| Responsibility | Portable role | Default route | Purpose |
| --- | --- | --- | --- |
| explorer | `explorer` | GPT-5.6 Luna `max` | mapping, search, tracing, evidence collection |
| execution_worker | `worker` | GPT-5.6 Luna `max` | bounded implementation, debugging, testing, local refactor |
| independent_critic | `default` | GPT-5.6 Terra `xhigh` | detached review, synthesis, conflicting evidence, assumption challenge |
| senior_judge | `default` | GPT-5.6 Sol `high` | one-off high-consequence adjudication when Root is not Sol |

Do not create a Sol Worker for routine execution. Use Terra because independent judgment has concrete value, not because a task merely looks difficult.

## 5. Consent Gate

The normal enabled-Skill envelope is one Luna responsibility plus, when Review Gate justifies it, one Terra critic. Do not ask repeatedly inside that envelope.

Ask in plain language before an expansion in permission, scope, external impact, fan-out beyond the normal two-child team, or capability/cost outside the baseline envelope such as one Sol Senior Judge from a non-Sol Root.

Use `references/consent-policy.md` for details.

## 6. Task packet and context fork

Use `references/task-packet.md`. For bounded coding work, prefer its Implementation Preset.

Role-specific spawns always set `fork_turns` explicitly:

- Explorer: `fork_turns = "none"`.
- Independent Critic: `fork_turns = "none"`.
- Execution Worker: `fork_turns = "none"` by default; use a positive integer only when recent user decisions cannot be safely repacked.
- Never omit `fork_turns` for a role-specific spawn.
- Never combine `fork_turns = "all"` with an `agent_type` override on MultiAgentV2.

Every packet includes the prompt-injection boundary and no-further-delegation rule.

## 7. Permission and safety checks

Use `references/safety-policy.md` when a child may write, handle sensitive material, or consume untrusted content.

Distinguish `runtime_enforced`, `instruction_enforced`, and `unknown`. A profile sandbox declaration is a configuration default, not proof of effective enforcement.

If safety depends on host-enforced read-only access and current runtime cannot report it, keep the responsibility in Root.

## 8. Execute, observe, and verify

After a child returns:

1. Treat its report as a claim.
2. Inspect actual files/diff/scope, commands, tests, uncertainty, `judgment_calls`, and policy violations.
3. Rerun deterministic verification when available.
4. Collect public native runtime metadata when useful or required.
5. Optionally collect a matching local rollout record with `scripts/inspect-runtime.py` when public metadata is incomplete.
6. Use `scripts/verify-runtime.py` when route, parent-thread identity, source agreement, or effective read-only must be checked deterministically.
7. Use the evidence grades in `references/runtime-assurance.md`: `C1_configuration_only`, `L1_local_record_observed`, `R1_runtime_reported`, `R2_runtime_reported_and_local_record_agree`, `X0_conflicted`.
8. A local rollout record alone never satisfies a requirement for a native runtime report.
9. When Root thread id is known, verify the child's `parent_thread_id`; quarantine a mismatch.
10. Allow at most one focused follow-up when evidence is incomplete.

## 9. Review Gate

Detached review is risk-triggered, not mandatory for every implementation.

Add one Terra Independent Critic when fresh judgment materially improves acceptance, especially for security/permission/concurrency/state-consistency logic, cross-module invariants, public contracts, migrations, weak deterministic oracles, material Worker `judgment_calls`, or conflicting evidence.

Give the critic the actual artifact/diff, objective, constraints, verification evidence, and material assumptions without the producer's private reasoning.

The critic returns:

```text
clear
findings
insufficient_evidence
```

Root still owns acceptance. If high-consequence disagreement remains and Root is not Sol, Consent Gate may authorize one Sol Senior Judge.

## 10. Close children

Close completed, rejected, or no-longer-needed Subagents promptly.

## 11. Orchestration receipt

Use `references/orchestration-receipt.md`. Emit a compact receipt when the Skill was explicitly invoked, any child was created, or an orchestration gate materially changed execution. Keep implicit Root-only trivial work quiet by default.

## References

- `references/routing-policy.md`: team selection, configuration route assurance, context fork, review gate, failure behavior
- `references/runtime-assurance.md`: runtime evidence grades, ancestry, source reconciliation, deterministic verifier
- `references/task-packet.md`: progressive child packet, implementation preset, and attempt record
- `references/consent-policy.md`: baseline envelope and one-time escalation consent
- `references/safety-policy.md`: permissions, prompt injection, recursion, workspace mutation, side effects
- `references/orchestration-receipt.md`: compact user-visible record of Root-only or delegated execution
