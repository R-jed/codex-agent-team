# Architecture

codex delegate is a thin policy layer over Codex Native Subagents. It does not implement a second Agent runtime, persistent DAG service, background scheduler, daemon, or routing proxy.

The user-facing main session is the team leader. It owns user intent, authorization, team composition, integration, acceptance, and the final response.

The product target is the smallest useful delegation graph that improves everyday development quality without making the user manage Agent topology or specify an Agent count.

## Runtime mechanism

The normal control loop is intentionally short:

```text
understand outcome + acceptance
-> ask whether delegation helps
-> identify the current ready frontier
-> assign distinct responsibilities to the capability actually needed
-> run the smallest useful active set
-> consume useful completions and update the ready frontier
-> expand only when another responsibility is now ready and worth delegating
-> verify the real artifact
-> diagnose a blocker only when work is unresolved
-> run fresh independent review only when the final artifact requires it
-> deliver
```

The installed Skill has three model-facing runtime references:

```text
router-core.md
-> delegation benefit, role selection, child packet, adaptive scheduling, blocker handling, acceptance

guardrails.md
-> authority, explicit invocation, provisioning readiness, consent, writer ownership, trust, permissions, runtime evidence

final-review.md
-> artifact-bound independent assurance
```

`plugins/codex-delegate/policy-contract.json` contains only stable machine constants: hard delegation safety limits, role routes, capability-dedup reference, and Final Review reason codes. Adaptive team size is intentionally not encoded as a numeric project constant.

## Leader-led delegation

Main decides how to use the team from the task in front of it.

There is no product rule such as:

```text
small task -> 1 Agent
medium task -> 2 Agents
large task -> 4 Agents
```

There is also no rule that five roles imply five children.

The five roles are a capability vocabulary. Child instances come from real unresolved responsibilities. Main may keep everything itself, start one specialist, run several independent read-only lanes in parallel, or add another specialist later when new evidence makes that work ready.

A child is justified only when its responsibility is ready, distinct, non-duplicative, useful to delegate, and safe under current boundaries. Native Codex capacity is an upper bound, never a target to fill.

## Direct capability selection

The router does not require a large internal taxonomy. It asks what capability the unresolved work actually needs.

| Work remaining | Typical actor |
| --- | --- |
| no meaningful delegation benefit | Main session |
| narrow independent read-only factual evidence | Luna Reader |
| clear repeatable writing where behavior/invariants/acceptance are already decided | Luna Worker |
| demanding/material decision before implementation | capable Main or Sol Advisor |
| writing where demanding/material judgment is coupled to implementation | capable Main or Sol Solver |
| bounded read-heavy technical investigation/evidence synthesis after semantics are stable | Terra Investigator |
| independent final assurance for a consequential candidate | fresh Sol Advisor |

The quality boundaries follow current Codex model guidance:

- Luna is reserved for clear, repeatable, high-volume bounded work.
- Terra is a read-heavy investigation/value lane when broader synthesis is useful and material semantics are already stable.
- Sol is the judgment lane for demanding, ambiguous, multi-step reasoning and judgment-coupled implementation.

A task being large, many-file, hard, or easy to describe in a contract does not by itself select a model or an Agent count.

## Current roles

| Responsibility | Agent type | Route | Intent |
| --- | --- | --- | --- |
| Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | narrow bounded reusable evidence |
| Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | clear repeatable bounded implementation |
| Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | demanding judgment-coupled implementation |
| Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | bounded read-heavy technical investigation and evidence synthesis |
| Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | demanding/material read-only judgment or fresh independent review |

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
blocker: none | contract | judgment | investigation | stalled
```

Add another work item only for a genuinely distinct unresolved responsibility. Valid evidence prevents repeated discovery and duplicate ownership.

## Adaptive scheduling

Main manages a ready frontier rather than a fixed-size team.

```text
ready responsibility
+ distinct owner
+ non-duplicative
+ delegation value
+ safe boundaries
= eligible child work
```

Read-heavy independent work is the preferred place to exploit parallelism. Multiple Reader instances are valid when they own different evidence lanes. Investigator or Advisor can run alongside other independent read-only work when their specific capability is actually needed.

Use progressive fan-out. Start useful ready work, consume useful completions, merge valid evidence, then decide whether any newly ready responsibility is worth another child. Do not spawn speculative work that is likely to be invalidated by unresolved decisions.

The host decides how many child threads can physically run. codex delegate does not mirror that capacity into a permanent project limit. Spare capacity never creates a reason to spawn.

## Blocked work

Failure does not imply a stronger model.

```text
contract
-> Main repairs missing task truth, scope, invariant, or acceptance

judgment
-> capable Main / Advisor / Solver handles the demanding or material decision

investigation
-> Investigator only when semantics are stable, the work remains read-only, and no material judgment remains

stalled
-> at most one clean same-role retry when the role remains correct and the packet materially improves
```

Terra is not the automatic destination for a difficult technical problem. If the remaining technical work is demanding, ambiguous, multi-step, or requires a consequential decision, route it to capable Main/Sol.

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

## Consent and anti-sprawl boundary

Child count by itself is not a consent trigger.

Several distinct low-cost read-only lanes can be an ordinary response to a large parallel task. Conversely, a smaller number of repeated Sol/Terra calls can become material compute expansion.

Ask again when permissions, scope, external impact, or compute expands materially beyond what the user could reasonably expect from the requested task.

Do not create duplicate, speculative, or low-value children. Do not serialize expensive calls merely to avoid admitting that the orchestration has materially expanded.

## Explicit invocation and onboarding

The supported user command is:

```text
/codex-delegate <task>
```

Codex CLI/IDE users may also open the Skill picker with `/skills`. Implicit invocation is disabled.

When an explicit task actually benefits from delegation, exact role readiness is checked before delegated implementation starts. If profiles must be provisioned, the Skill explains the managed scope, asks permission, runs the bundled installer plus `--check`, then verifies the role surface. If the runtime requires a fresh thread to discover new roles, execution stops before child writing begins.

The five managed TOML files use Codex's native custom-Agent mechanism. The installer only provides project-specific lifecycle, ownership, and collision safety around those native profiles.

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

## Plugin boundary

The Plugin intentionally remains skills-only because the product is fully expressible through instructions, Codex Native Subagents, and native custom Agents. It does not declare MCP servers, apps, hooks, or another runtime.

Public Plugin metadata includes the website, privacy policy, terms of use, category, brand assets, and starter prompts. Public user installation is marketplace-first; local repository marketplace metadata remains a development/testing surface.

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
