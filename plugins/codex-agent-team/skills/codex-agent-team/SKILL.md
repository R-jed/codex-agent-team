---
name: codex-delegate
description: Build the smallest useful native Codex Subagent compute graph. Keep the current main session in control, route only bounded responsibilities that satisfy distinct unresolved dependencies, reuse established evidence, and adapt execution through an evidence-driven intervention gate instead of fixed Agent counts, retry counts, or model ladders.
---

# Codex Delegate

Use this Skill as a policy layer over Codex Native Subagents. The main session owns the task and its logical dependency state. Subagents receive bounded responsibilities only when delegation creates concrete value and the responsibility can be expressed as a verifiable contract.

## Core invariants

1. The current main session owns user intent, scope, architecture, scheduling, risk, integration, acceptance, and the final answer.
2. No model is a mandatory stage. Every Agent call must satisfy a distinct unresolved dependency that valid existing evidence does not already satisfy.
3. There is no product-level hard child count and no fixed team shape. Zero Subagents is normal. Create only the smallest useful scheduling wave from currently ready dependencies.
4. Explicit `/codex-delegate` use includes a normal no-extra-consent envelope of up to two concurrently active child Agents. Larger simultaneous fan-out or other material compute expansion requires consent unless the user already requested broad parallel work.
5. Native runtime capacity is an observed execution constraint, not a Codex Delegate architecture constant. Slot pressure queues or serializes ready work; it does not justify duplicate work, cross-routing, or a fake product ceiling.
6. Luna Max is the default bounded execution tier. Terra XHigh is an exception lane for unresolved complex technical deltas. Sol High is a selective judgment or review tier.
7. Acceptance failure and need for intervention are separate facts. Continue a valid responsibility while evidence shows forward progress; classify recovery only when intervention is justified.
8. Progress is established from artifacts, deterministic verification, repository facts, or a materially narrowed unresolved dependency. Model confidence, narration, a successful command, or a file write alone is not progress.
9. Material recovery keeps a compact Recovery Ledger and distinguishes proposed actions from effective actions and their decision source. Model suggestions never become orchestration authority by themselves.
10. Established deterministic and repository evidence is reused while its dependencies remain valid. Do not rediscover valid facts by default.
11. One canonical shared workspace has at most one active writing Worker. Children do not create further Subagents.
12. Role-specific spawns always set `fork_turns` explicitly. Fresh bounded packets are preferred over inherited conversational history.
13. Model-specific children require a provable project-profile route. Missing or conflicting routes return the responsibility to the main session.
14. Configuration assurance and runtime observation are separate facts. Empty or partial observations never count as complete runtime route evidence.
15. Worker reports are claims. Accept work from actual artifacts, deterministic verification, and reproducible evidence.
16. `/codex-delegate` is the canonical user-facing workflow entry point. First-run custom-Agent readiness is handled inside this Skill with explicit user-approved provisioning.
17. Resource state has separate scopes: task dependency state is main-session scoped, write ownership is canonical-workspace scoped, and managed Agent profiles are Codex-home scoped.

## 1. Understand the task

Identify the requested outcome, existing authorization, known scope, consequence of error, acceptance signals, and current repository/runtime facts.

Do not start with model selection or an Agent-count target. First determine what must become true and which dependencies remain unresolved.

## 2. Build the Dependency Ledger

Maintain a compact in-session Dependency Ledger. It is logical task state, not a persistent external DAG or scheduler.

Each material dependency records enough information to answer whether it is ready and whether another Agent would add new value:

```text
DEPENDENCY ID
OUTCOME
STATUS: pending | ready | running | satisfied | blocked | invalidated
REQUIRES: dependency ids and/or evidence ids
PRODUCES: artifact, decision, or evidence expected
WRITE INTENT
WORKSPACE
ACCEPTANCE
```

A dependency becomes `ready` only when its prerequisites are satisfied. A dependency already `running` or `satisfied` must not receive a duplicate Agent call unless new evidence invalidates the prior result.

Recompute the ready frontier after meaningful evidence or artifact changes.

## 3. Delegation Benefit Gate

Delegate a ready dependency only when at least one concrete benefit exists:

- **Context isolation**: noisy source, logs, tests, or documents can be compressed into reusable evidence.
- **Useful parallelism**: independent ready dependencies can progress concurrently and materially shorten the critical path or protect main-session context.
- **Specialized capability**: a bounded responsibility materially benefits from a different execution or investigation tier.
- **Independent judgment**: a consequential decision or artifact benefits from a fresh Sol review.

Task length, file count, spare concurrency, an arbitrary desire for more Agents, or a cheaper model do not justify delegation by themselves.

If no concrete benefit exists, keep the dependency in the main session.

## 4. Contractability Gate

Before creating an execution Subagent, compile the responsibility with `references/delegation-contract.md`.

A writing responsibility must have explicit enough:

```text
DEPENDENCY
OUTCOME
SCOPE
INTERFACES / DEPENDENCIES
INVARIANTS
DECISION RIGHTS
ACCEPTANCE ORACLE
VERIFICATION
STOP / ESCALATE
```

If the acceptance oracle or decision rights are materially unclear, do not spawn a writing Worker. Clarify the task, gather more evidence, or keep the decision in the main session.

Never hand Luna the user's raw ambiguous request when a bounded execution contract can be compiled first.

## 5. Schedule the ready frontier

Choose the smallest useful scheduling wave from dependencies that are simultaneously ready.

A dependency is eligible to run only when all of these hold:

```text
it contributes a distinct unresolved dependency
its contract is enforceable
its required exact route is available
its workspace mutation is compatible with active work
its consent requirements are already satisfied
native runtime capacity is currently available or the work can wait safely
```

Prefer fewer children when one child can satisfy the ready work without sacrificing context isolation, independent judgment, or critical-path progress.

Do not create multiple children for the same question simply because slots are available. Do not reserve a fixed number of children in advance.

When more than two children would be concurrently active, use the Consent Gate unless broad fan-out was already authorized. After consent, the ready frontier and native runtime decide actual concurrency. Codex Delegate does not impose another numerical hard ceiling.

If the runtime has fewer slots than ready dependencies, queue or serialize the remaining dependencies. Never change role/model identity solely to occupy a slot.

## 6. Official Plugin boundary, Agent Profile Readiness, and route assurance

Codex Delegate uses the native Codex Plugin system for distribution. The Plugin manifest packages the Skill and ordinary bundle files. Custom Agent profiles are a separate Codex configuration surface: Codex officially discovers personal custom agents from `$CODEX_HOME/agents` (normally `~/.codex/agents`) and project custom agents from `.codex/agents`.

The Plugin manifest does not claim a native `agents` component. The bundled profile templates and installer are project-managed post-install provisioning. Run that provisioning only after a model-specific dependency has justified a custom role and the user approves the exact Codex-home write scope.

Check the live native `spawn_agent` role surface only after a model-specific responsibility is justified.

Project roles:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

These role identifiers are compatibility-scoped internal profile names. The user-facing product and Skill entry point are Codex Delegate and `/codex-delegate`.

If the required role is visible with the expected locked configuration, record `route_assurance = profile_locked` and continue.

If it is missing, resolve the bundled managed installer from this Skill directory:

```text
skill_dir = directory containing this SKILL.md
installer = skill_dir/../../scripts/install-agents.py
```

Before running it, explain the exact managed write/migration scope and ask permission. The installer may:

- write or replace the four current Codex Delegate profile files under the active `$CODEX_HOME/agents` only when ownership/exactness rules permit;
- write `.codex-agent-team-agents.json` under Codex home;
- remove an older `luna_explorer`, `luna_worker`, `terra_reviewer`, or `sol_judge` profile only when its current bytes exactly match ownership recorded by a previous project manifest.

Unproven or user-modified legacy files are left untouched. Authorization covers only these project-managed paths and does not authorize edits to `config.toml`, credentials, MCP configuration, repositories, or unrelated Agent profiles.

After approval:

```bash
python "$installer"
python "$installer" --check
```

Then inspect the live role surface again. Continue immediately when the role is visible. If exact installation succeeded but current-task role discovery did not refresh, ask the user to start a fresh Codex task and invoke `/codex-delegate` again.

The four profiles and ownership manifest are Codex-home scoped shared configuration. Multiple projects may use one installed generation. Mixed concurrent profile generations are unsupported for v1.0.0: if a session's expected exact route does not match the installed profile, stop that delegation instead of substituting, silently downgrading, or cross-routing.

There is no Portable Mode and no built-in-role substitution.

Read `references/routing-policy.md` for route details.

## 7. Route by responsibility

Route responsibilities, not prestige levels and not prompt length.

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

### Luna Reader

Use `codex_agent_team_reader` for bounded search, tracing, test mapping, documentation extraction, and evidence collection.

Reuse established evidence. Add only new facts needed by the assigned dependency.

### Luna Worker

Use `codex_agent_team_worker` for contractable implementation, debugging, tests, local refactors, and mechanical changes.

Luna owns `HOW TO EXECUTE` inside the granted contract. It does not invent product requirements, redesign architecture, widen scope, or make decisions reserved for the main session.

Treat the workspace as potentially changed by the user or another independent session. Preserve unrelated existing edits. Never revert unknown changes to restore an assumed starting state. Re-read affected files and relevant state immediately before mutation when concurrent change is plausible. If drift invalidates the write scope, an invariant, decision rights, the acceptance oracle, or established evidence, stop and return the changed state and smallest unresolved delta to the main session.

File-level ownership promises do not authorize a second writing Worker in the same physical checkout.

### Terra Investigator

Use `codex_agent_team_investigator` when a clear dependency exposes a genuine technical capability gap that Luna or the main session cannot efficiently resolve.

Terra receives the unresolved delta, valid established evidence, and current artifact. It does not redo the full Luna responsibility and does not serve as a generic quality-upgrade button.

Default Terra work is read-only investigation. After Terra resolves the delta, the main session may update the contract and return bounded implementation to Luna.

### Sol Advisor

Use `codex_agent_team_advisor` for a high-value judgment or selective review that deterministic verification and existing evidence cannot replace.

A consequential architecture, security, migration, data-integrity, or public-contract commitment is a valid Sol boundary when the unresolved question is genuinely judgmental.

Give Sol compressed established facts, the actual artifact or decision options, and one bounded question. Use fresh context by default. Do not ask Sol to rescan the repository or inherit dead-end narration when established evidence can carry the dependency.

Final Sol review is selective, not mandatory.

## 8. Execution Progress and Intervention Gate

Use `references/execution-progress.md` after a delegated execution attempt or whenever repeated work, a lane change, or a context reset is being considered.

Progress must be grounded in observable task movement. Examples include:

- a previously failing acceptance check now passes;
- a new deterministic result narrows the failure space;
- a new repository fact resolves part of the dependency;
- the unresolved delta becomes materially smaller;
- the artifact moves toward the acceptance oracle without violating invariants.

These are not progress by themselves:

- model confidence or narration;
- a successful command that does not improve acceptance or establish useful new evidence;
- rewriting a file while verification remains unchanged;
- rerunning the same command with the same result and no invalidation reason;
- repeating repository discovery that valid evidence already covers.

### Stage A: should execution be interrupted or changed?

Ask whether the current responsibility still has evidence-supported forward progress inside a valid contract and safe runtime boundary.

If yes, continue the current responsibility even when acceptance is not reached yet. Do not trigger recovery simply because a test still fails while the failure space is materially narrowing.

If no, or the responsibility is blocked by contract, capability, judgment, workspace, permission, consent, or runtime state, continue to Stage B.

### Stage B: classify the intervention

```text
mechanical defect
-> focused Luna correction when there is a concrete local correction path

contract gap
-> main session repairs the contract

execution stall / context pollution
-> fresh same-lane packet with current artifact + valid evidence + material Recovery Ledger + DO NOT REDO

capability gap
-> Terra receives only the unresolved technical delta

judgment gap
-> main session decides or uses Sol when justified
```

Do not retry an unchanged contract merely because a prior attempt failed. A follow-up requires new evidence, a repaired contract, a distinct correction hypothesis, or a changed artifact/runtime state.

Capability takes precedence over repeatedly restarting the same execution lane. A clean same-lane restart is for polluted or unproductive context when the lane still appears capable of satisfying the contract.

The main session keeps a compact Recovery Ledger of material attempt ids, lanes, correction hypotheses, failure signatures, progress signals, evidence ids, unresolved deltas, recovery actions, and decision sources. It is not a transcript and contains no private reasoning.

When an Agent suggests a recovery action, record that as a proposal. The main session applies consent, workspace, route, permission, and runtime policy before choosing the effective action. Keep proposed action, effective action, decision source, and any policy transform separate when the distinction matters.

Recovery evaluation is event-driven. Re-evaluate after child return, material acceptance/failure/evidence changes, user changes, dependency blocking, or material workspace/runtime changes. Do not invent turn-count checkpoints or claim mid-run child observability that the current Codex runtime has not exposed.

Preserve facts and artifacts across a clean restart. Do not transfer private reasoning or dead-end narration as task state.

## 9. Useful parallelism

Parallel work is justified only when outputs satisfy different ready dependencies.

Good examples:

- independent Luna Readers map separate subsystems;
- the main session prepares acceptance and risk checks while Luna implements;
- a slow deterministic test suite runs while unrelated read-only analysis proceeds;
- independent projects or runtime-backed isolated worktrees each use a writer without creating a machine-wide bottleneck.

Do not parallelize multiple models over the same question merely to keep compute busy.

Concurrency has three scopes:

```text
main-session scope: Dependency Ledger, ready frontier, consent state, active child set
workspace scope: one active writer per canonical physical checkout or isolated worktree
Codex-home scope: one installed managed profile generation shared by sessions using that home
```

Two sessions targeting the same physical checkout share the one-writer invariant even if their intended file sets differ. Current session-local orchestration must not be assumed to enforce cross-session exclusion until live validation proves native coordination or a reproducible failure justifies a project-side mechanism.

## 10. Consent Gate

Use `references/consent-policy.md`.

Explicit `/codex-delegate` invocation authorizes ordinary orchestration within the baseline resource envelope. The baseline covers up to two concurrently active justified children, at most one writer per canonical workspace, and no permission, scope, external-impact, or material compute expansion.

The number two is a consent boundary for concurrent fan-out, not a task lifetime cap and not a scheduler target.

Ask before larger simultaneous fan-out, repeated serial delegation that materially expands compute cost, additional permissions, broader scope, external side effects, or other material capability/cost expansion outside the enabled envelope.

## 11. Safety

Use `references/safety-policy.md` when a child may write, handle untrusted content, or require read-only guarantees.

Prompt text does not prove runtime permission enforcement. If safety requires host-enforced read-only and the runtime cannot report it, keep that responsibility in the main session.

Do not claim cross-session writer exclusion or multi-process installer safety unless current runtime/filesystem evidence proves it. Those are v1 release gates, not assumptions derived from Skill text.

## 12. Execute, merge evidence, and verify

After each child returns:

1. Treat the report as a claim.
2. Inspect actual files, diff, commands, tests, and scope.
3. Merge new deterministic or repository evidence into Shared Evidence State.
4. Update Dependency Ledger status and recompute the ready frontier.
5. Invalidate only evidence whose declared dependencies changed or conflicted, including changes made by the user or another independent session.
6. Rerun deterministic verification when required by the acceptance oracle.
7. Record structured execution signals and update the Recovery Ledger before deciding whether intervention is justified.
8. Pass the Intervention Gate before changing lane, restarting context, or escalating judgment.
9. Collect runtime evidence only when route identity, ancestry, permission, child-progress observability, conflict, or an explicit user request makes it material.
10. Use `scripts/verify-runtime.py` for deterministic runtime-evidence reconciliation.
11. Never spawn a duplicate dependency call solely because the previous Agent returned slowly, confidently, or incompletely.

## 13. Runtime evidence

Use `references/runtime-assurance.md`.

Runtime evidence is typed by concern:

```text
route_evidence
ancestry_evidence
permission_evidence
```

The compact legacy grades `C1`, `L1`, `R1`, `R2`, and `X0` remain derived summaries only. A grade must never imply evidence for fields that were missing.

Child-progress observability is also a runtime fact. Classify it only from the surface actually exposed by the tested Codex build, for example `none`, `terminal_only`, `periodic_summary`, or `structured_live`. Do not infer a stronger observability level from documentation or a child self-report.

## 14. Close and report

Close completed, rejected, superseded, or no-longer-needed Subagents promptly so native capacity can recover.

Use `references/orchestration-receipt.md` when the Skill was explicitly invoked, any child was created, or orchestration materially changed execution. Keep trivial implicit main-session-only work quiet by default.

## References

- `references/delegation-contract.md`: dependency contract, Shared Evidence State, Recovery Ledger, delta escalation
- `references/execution-progress.md`: observable progress, Intervention Gate, structured signals, recovery provenance, clean same-lane restart
- `references/routing-policy.md`: adaptive compute graph, semantic responsibilities, route policy, ready-frontier scheduling
- `references/runtime-assurance.md`: typed runtime evidence and deterministic verifier
- `references/consent-policy.md`: baseline concurrent resource envelope and expansion consent
- `references/safety-policy.md`: permissions, prompt injection, depth, mutation, shared-workspace and Codex-home safety
- `references/orchestration-receipt.md`: compact user-visible execution record
