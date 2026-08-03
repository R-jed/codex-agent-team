---
name: codex-agent-team
description: Build the smallest useful native Codex Subagent compute graph. Keep the current main session in control, use GPT-5.6 Luna Max for bounded execution, Terra only for unresolved complex technical deltas, and Sol High for selective judgment or review. Reuse established evidence, avoid duplicated work, and require every Agent call to contribute a distinct dependency to task completion.
---

# Codex Agent Team

Use this Skill as a policy layer over Codex Native Subagents. The main session owns the task and the compute graph. Subagents receive bounded responsibilities only when delegation creates concrete value and the responsibility can be expressed as a verifiable contract.

## Core invariants

1. The current main session owns user intent, scope, architecture, scheduling, risk, integration, acceptance, and the final answer.
2. No model is a mandatory stage. Every Agent call must contribute a distinct dependency that existing work cannot already satisfy.
3. Zero Subagents is normal. Default child count is 1, normal maximum is 2, hard maximum is 4.
4. Luna Max is the default execution tier. Terra is an exception lane for unresolved complex technical deltas. Sol High is a selective judgment or review tier.
5. Low quality alone never triggers Terra. Classify the failure first and escalate only the unresolved delta.
6. Established deterministic and repository evidence is reused while its dependencies remain valid. Do not rediscover valid facts by default.
7. One canonical shared workspace has at most one active writing Worker. Children do not create further Subagents.
8. Role-specific spawns always set `fork_turns` explicitly.
9. Model-specific children require a provable project-profile route. Missing or conflicting routes return the responsibility to the main session.
10. Configuration assurance and runtime observation are separate facts. Empty or partial observations never count as complete runtime route evidence.
11. Worker reports are claims. Accept work from actual artifacts, deterministic verification, and reproducible evidence.
12. `/codex-agent-team` is the only user-facing workflow entry point. First-run custom-Agent readiness is handled inside this Skill.
13. Child-count limits are per main session. Workspace write ownership is per canonical physical checkout or isolated worktree. Managed Agent profiles are shared at Codex-home scope.

## 1. Understand the task

Identify the requested outcome, existing authorization, known scope, consequence of error, and acceptance signals.

Do not start with model selection. First determine what responsibilities exist and which dependencies must be satisfied.

## 2. Delegation Benefit Gate

Delegate only when at least one concrete benefit exists:

- **Context isolation**: noisy source, logs, tests, or documents can be compressed into reusable evidence.
- **Useful parallelism**: independent branches satisfy different dependencies and can progress concurrently.
- **Specialized capability**: a bounded responsibility materially benefits from a different execution or judgment tier.
- **Independent judgment**: a consequential decision or artifact benefits from a fresh Sol review.

Task length, file count, spare concurrency, or a cheaper model do not justify delegation by themselves.

If no concrete benefit exists, keep the task in the main session.

## 3. Contractability Gate

Before creating an execution Subagent, compile the responsibility with `references/delegation-contract.md`.

A writing responsibility must have explicit enough:

```text
OUTCOME
SCOPE
INVARIANTS
DECISION RIGHTS
ACCEPTANCE ORACLE
VERIFICATION
STOP / ESCALATE
```

If the acceptance oracle or decision rights are materially unclear, do not spawn a writing Worker. Clarify the task, gather more evidence, or keep the decision in the main session.

Never hand Luna the user's raw ambiguous request when a bounded execution contract can be compiled first.

## 4. Build the compute graph

Route responsibilities, not prestige levels.

Common valid graphs include:

```text
main session

main session -> Luna -> main session

main session -> Luna -> Sol -> main session

main session -> Terra -> Luna -> main session

main session -> Luna -> Terra(delta only) -> Luna or main session

main session -> Sol -> main session
```

`Luna -> Terra -> Sol` is never a required pipeline.

Every node must answer: what new dependency does this call satisfy that valid existing evidence cannot?

## 5. Agent Profile Readiness and route assurance

Check the live native `spawn_agent` role surface only after a model-specific responsibility is justified.

Project roles:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

If the required role is visible with the expected locked configuration, record `route_assurance = profile_locked` and continue.

If it is missing, resolve the bundled managed installer from this Skill directory:

```text
skill_dir = directory containing this SKILL.md
installer = skill_dir/../../scripts/install-agents.py
```

Before running it, explain the exact managed write/migration scope and ask permission. The installer may:

- write or replace the four current Codex Agent Team profile files only when ownership/exactness rules permit;
- write `.codex-agent-team-agents.json` under Codex home;
- remove an older `luna_explorer`, `luna_worker`, `terra_reviewer`, or `sol_judge` profile only when its current bytes exactly match ownership recorded by a previous Codex Agent Team manifest.

Unproven or user-modified legacy files are left untouched. Authorization covers only these project-managed paths and does not authorize edits to `config.toml`, credentials, MCP configuration, repositories, or unrelated Agent profiles.

After approval:

```bash
python "$installer"
python "$installer" --check
```

Then inspect the live role surface again. Continue immediately when the role is visible. If exact installation succeeded but current-task role discovery did not refresh, ask the user to start a fresh Codex task and invoke `/codex-agent-team` again.

The four profiles and ownership manifest are Codex-home scoped shared configuration. Multiple projects may use one installed generation. Mixed concurrent profile generations are unsupported for v1.0.0: if a session's expected exact route does not match the currently installed profile, stop that delegation instead of substituting, silently downgrading, or cross-routing.

There is no Portable Mode and no built-in-role substitution.

Read `references/routing-policy.md` for route details.

## 6. Route by responsibility

### Luna Reader

Use `codex_agent_team_reader` for bounded search, tracing, test mapping, documentation extraction, and evidence collection.

Reuse established evidence. Add only new facts needed by the current dependency.

### Luna Worker

Use `codex_agent_team_worker` for contractable implementation, debugging, tests, local refactors, and mechanical changes.

Luna owns `HOW TO EXECUTE` inside the granted contract. It does not invent product requirements, redesign architecture, widen scope, or make decisions reserved for the main session.

Treat the workspace as potentially changed by the user or another independent session. Preserve unrelated existing edits. Never revert unknown changes to restore an assumed starting state. Re-read affected files and relevant state immediately before mutation when concurrent change is plausible. If drift invalidates the write scope, an invariant, decision rights, the acceptance oracle, or established evidence, stop and return the changed state and smallest unresolved delta to the main session.

File-level ownership promises do not authorize a second writing Worker in the same physical checkout.

### Terra Investigator

Use `codex_agent_team_investigator` only when a clear contract exposes a genuine technical capability gap that Luna or the main session cannot efficiently resolve.

Terra receives the unresolved delta, valid established evidence, and current artifact. It does not redo the full Luna responsibility and does not serve as a generic quality-upgrade button.

Default Terra work is read-only investigation. After Terra resolves the delta, the main session may update the contract and return bounded implementation to Luna.

### Sol Advisor

Use `codex_agent_team_advisor` for a high-value judgment or selective review that cannot be replaced by deterministic verification or existing evidence.

Give Sol compressed established facts, the actual artifact or decision options, and one bounded question. Do not ask Sol to rescan the repository by default.

Sol may appear directly after Luna when implementation is clear but the resulting artifact merits higher-value review. Terra is not required in that path.

## 7. Failure classification and delta escalation

When Luna fails acceptance, classify the cause before choosing another model:

```text
mechanical defect
-> focused Luna correction

contract gap
-> main session repairs the contract

capability gap
-> Terra receives only the unresolved technical delta

judgment gap
-> main session decides or uses Sol when justified
```

Concurrent workspace drift is changed input, not a capability upgrade signal. Reconcile the current artifact and invalidate only dependent evidence.

Preserve valid evidence across retries. Recompute only dependencies invalidated by changed files, artifacts, runtime facts, or contradictory evidence.

Use `references/delegation-contract.md` for Shared Evidence State and Delta Escalation packets.

## 8. Useful parallelism

Parallel work is justified only when outputs satisfy different dependencies.

Good examples:

- one Luna Reader traces a runtime path while another read-only branch maps independent test coverage;
- the main session prepares acceptance and risk checks while Luna executes a bounded implementation;
- a slow deterministic test suite runs while independent read-only analysis proceeds;
- independent projects or runtime-backed isolated worktrees may each use one writer without creating a machine-wide writer bottleneck.

Do not parallelize multiple models over the same question merely to keep compute busy.

Concurrency has three scopes:

```text
main-session scope: child-count envelope, normal max 2, hard max 4
workspace scope: one active writer per canonical physical checkout or isolated worktree
Codex-home scope: one installed managed profile generation shared by sessions using that home
```

The hard maximum of four is a v1.0.0 per-main-session policy limit, not a claim about native machine/account capacity. Do not create a global Agent cap that blocks independent projects.

One canonical shared workspace still has at most one active writing Worker. Two sessions targeting the same physical checkout share this invariant even if their intended file sets differ. Current session-local orchestration must not be assumed to enforce cross-session exclusion until live validation proves native coordination or a reproducible failure justifies a project-side mechanism.

## 9. Consent Gate

Use `references/consent-policy.md`.

The baseline resource envelope is at most two child Agents, at most one writer, and no permission, scope, or external-impact expansion. When `/codex-agent-team` was explicitly invoked, one justified Sol read-only judgment or review may fit inside that envelope.

Ask before larger fan-out, additional permissions, broader scope, external side effects, or a material capability/cost expansion outside the enabled envelope.

## 10. Safety

Use `references/safety-policy.md` when a child may write, handle untrusted content, or require read-only guarantees.

Prompt text does not prove runtime permission enforcement. If safety requires host-enforced read-only and the runtime cannot report it, keep that responsibility in the main session.

Do not claim cross-session writer exclusion or multi-process installer safety unless current runtime/filesystem evidence proves it. Those are v1 release gates, not assumptions derived from the Skill text.

## 11. Execute, merge evidence, and verify

After each child returns:

1. Treat the report as a claim.
2. Inspect actual files, diff, commands, tests, and scope.
3. Merge new deterministic or repository evidence into Shared Evidence State.
4. Invalidate only evidence whose declared dependencies changed or conflicted, including changes made by the user or another independent session.
5. Rerun deterministic verification when required by the acceptance oracle.
6. Collect runtime evidence only when route identity, ancestry, permission, conflict, or an explicit user request makes it material.
7. Use `scripts/verify-runtime.py` for deterministic evidence reconciliation.
8. Allow at most one focused follow-up per child responsibility when useful.

## 12. Runtime evidence

Use `references/runtime-assurance.md`.

Runtime evidence is typed by concern:

```text
route_evidence
ancestry_evidence
permission_evidence
```

The compact legacy grades `C1`, `L1`, `R1`, `R2`, and `X0` remain derived summaries only. A grade must never imply evidence for fields that were missing.

## 13. Close and report

Close completed, rejected, or no-longer-needed Subagents promptly.

Use `references/orchestration-receipt.md` when the Skill was explicitly invoked, any child was created, or orchestration materially changed execution. Keep trivial implicit main-session-only work quiet by default.

## References

- `references/delegation-contract.md`: contractability, Shared Evidence State, failure classification, delta escalation
- `references/routing-policy.md`: compute graph, semantic responsibilities, route policy, useful parallelism, concurrency scopes
- `references/runtime-assurance.md`: typed runtime evidence and deterministic verifier
- `references/consent-policy.md`: baseline resource envelope and escalation consent
- `references/safety-policy.md`: permissions, prompt injection, depth, mutation, shared-workspace and Codex-home safety
- `references/orchestration-receipt.md`: compact user-visible execution record
