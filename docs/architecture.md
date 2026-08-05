# Architecture

codex delegate is a thin policy layer over Codex Native Subagents. It does not implement a second Agent runtime, persistent DAG service, background scheduler, daemon, or routing proxy.

The user-facing main session remains the control plane. It owns user intent, authorization, integration, acceptance, and final response.

The product target is the smallest useful delegation graph that improves everyday development quality without making the user manage Agent topology.

## Runtime mechanism

The normal control loop is intentionally short:

```text
understand outcome + acceptance
-> ask whether delegation helps
-> select the capability actually needed
-> execute under one-writer / consent boundaries
-> verify the real artifact
-> diagnose a blocker only when work is unresolved
-> run fresh independent review only when the final artifact requires it
-> deliver
```

The installed Skill has three model-facing runtime references:

```text
router-core.md
-> delegation benefit, role selection, child packet, blocker handling, scheduling, acceptance

guardrails.md
-> authority, explicit invocation, provisioning readiness, consent, writer ownership, trust, permissions, runtime evidence

final-review.md
-> artifact-bound independent assurance
```

`plugins/codex-delegate/policy-contract.json` contains only stable machine constants: role routes, delegation limits, capability-dedup reference, and Final Review reason codes.

## Direct capability selection

The router does not require a large internal taxonomy. It asks what capability the unresolved work actually needs.

| Work remaining | Typical actor |
| --- | --- |
| no meaningful delegation benefit | Main session |
| independent read-only factual evidence | Luna Reader |
| writing where behavior/invariants/acceptance are already decided | Luna Worker |
| material decision before implementation | capable Main or Sol Advisor |
| writing where material judgment is coupled to implementation | capable Main or Sol Solver |
| narrow difficult technical question after semantics are stable | Terra Investigator |
| independent final assurance for a consequential candidate | fresh Sol Advisor |

The important quality boundary is simple: Luna Worker receives work where material behavior decisions are already made. A task being large, many-file, or easy to describe in a contract does not make it Luna-suitable.

## Current roles

| Responsibility | Agent type | Route | Intent |
| --- | --- | --- | --- |
| Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | bounded reusable evidence |
| Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | standardized bounded implementation |
| Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | judgment-coupled implementation |
| Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | narrow difficult technical uncertainty |
| Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | material read-only judgment or fresh independent review |

Role identity is separate from model identity so future route changes do not redefine responsibility semantics.

## Compact task state

The normal runtime keeps one small work-item state rather than separate orchestration ledgers:

```text
outcome
owner
read/write intent
material judgment: none | separable | coupled
acceptance
valid evidence
current failure
blocker: none | contract | judgment | specialist | stalled
```

Add another work item only for a genuinely distinct unresolved responsibility. Valid evidence prevents repeated discovery and duplicate ownership.

## Blocked work

Failure does not imply a stronger model.

```text
contract
-> Main repairs missing task truth, scope, invariant, or acceptance

judgment
-> capable Main / Advisor / Solver handles the material decision

specialist
-> Investigator only when semantics are stable and the remaining technical delta is narrow

stalled
-> at most one clean same-role retry when the role remains correct and the packet materially improves
```

If the same failure continues without new evidence or acceptance progress, stop repeating the lane and diagnose the real blocker.

## Main-session capability dedup

Main-session model awareness exists to avoid redundant Sol compute. It is an optimization after the router has already established that material judgment needs Sol capability.

`policy-contract.json` declares the reference role and reasoning-effort order. `plugins/codex-delegate/scripts/runtime-evidence.py` can normalize trusted current-session model/effort metadata when the optimization is material.

Current reference role is Solver, GPT-5.6 Sol `high`:

```text
matching Sol family + high/xhigh/max
-> covered

matching Sol family + medium/low
-> uncovered

nonmatching family
-> uncovered

missing / partial / local-only / conflicted / unranked effort
-> unknown
```

Routine bounded work does not inspect the main model. Missing telemetry does not block ordinary routing.

A covered main session can avoid ordinary capability-uplift Advisor/Solver calls. It never substitutes for required independent review of its own candidate.

## Writer ownership

One canonical physical checkout has one active writing actor inside the current orchestration:

```text
Main session while mutating
Luna Worker
Sol Solver
```

If Worker or Solver owns the write, Main may continue read-only analysis but waits for ownership handoff before integration writes.

Multiple concurrent writers require real filesystem isolation such as separate worktrees/workspaces/repositories. File-list promises are insufficient isolation.

Independent sessions, editors, hooks, and external processes remain outside this session-local scheduler. Current policy relies on isolation where practical plus drift detection and fail-closed behavior. It does not claim a cross-session lock that has not been implemented and validated.

## Explicit invocation and onboarding

The supported user mental model is explicit:

```text
/codex-delegate <task>
```

Implicit invocation is disabled.

When an explicit task actually benefits from delegation, exact role readiness is checked before delegated implementation starts. If profiles must be provisioned, the Skill explains the managed scope, asks permission, runs the bundled installer plus `--check`, then verifies the role surface. If the runtime requires a fresh thread to discover new roles, execution stops before child writing begins.

This avoids discovering installation requirements midway through a development task.

## Runtime evidence boundary

Runtime evidence is diagnostic and on demand.

Use it when a claim genuinely depends on observed runtime facts, such as:

- Sol capability dedup;
- hard host-enforced read-only;
- exact route/model/effort proof;
- ancestry when depth-one proof matters;
- independent-review provenance;
- configuration/runtime conflicts;
- release diagnostics.

Ordinary bounded implementation can rely on exact configured role intent plus actual artifact verification when runtime route proof is not part of acceptance.

Configuration remains separate from observation. Missing evidence stays missing.

## Final Review

Final Review is an independent assurance decision after Candidate Ready.

Current semantic trigger classes are:

```text
user-requested review
public contract change
persistent state change
security boundary
authorization boundary
data integrity
concurrency semantics
material migration
verification gap
```

Prior use of Terra, Solver, recovery, a large diff, or many files does not by itself trigger review.

When required:

```text
bind exact candidate
-> fresh codex_delegate_advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Any deliverable mutation invalidates the old verdict.

## User-visible output

The product reports the development result first:

```text
what changed
verification
remaining material risk
```

It does not emit a separate orchestration receipt for every successful invocation. Routing details are surfaced when they materially affected consent, execution, a limitation, independent review, or when the user asks.

## Evaluation boundary

Static tests prove machine contracts and deterministic helpers. `evals/` is a measurement surface for controlled product experiments, not a second runtime policy specification.

Behavioral labels in eval schemas may remain more detailed than the runtime hot path so historical experiments stay comparable. They must not force the Skill to maintain the old runtime ontology.

No model-quality or cost-superiority claim is valid until named live workloads on named runtime versions support it.
