---
name: codex-delegate
description: Delegate only when it improves the task, keep clear repeatable bounded execution on Luna, place demanding or material judgment on Sol, use Terra for bounded read-heavy technical investigation, preserve one-writer safety, and apply fresh independent review only when the final artifact requires it.
---

# codex delegate

codex delegate is a thin leadership and coordination layer over Codex Native Subagents. The current user-facing main session is the team leader. It understands the user's goal, decides what to keep, decides what to delegate, assigns the right specialist, coordinates multi-Agent work when coordination is actually needed, recovers bounded failures, and owns the final result.

The user does not design an Agent team, predeclare a team size, choose a model ladder, or manage recovery attempts.

The runtime policy has five focused owners:

- `references/router-core.md`: delegation benefit, role selection, upstream-workflow ownership, responsibility semantics, adaptive scheduling, acceptance
- `references/team-plan.md`: multi-responsibility identity, dependency DAG, ownership, plan revision, integration order
- `references/recovery.md`: native attempt identity, lifecycle, UNKNOWN, failure classification, bounded recovery, Main takeover
- `references/guardrails.md`: consent, mutation authority, writer ownership, semantic independence, permissions, trust boundaries, provisioning, runtime evidence
- `references/final-review.md`: independent artifact-bound final assurance

Stable role/model constants and hard delegation safety limits live in `../../policy-contract.json`.

## Core invariants

1. Main session owns user intent, authorization, team composition, integration, acceptance, and final response.
2. Zero children is normal. Delegation must provide concrete value.
3. There is no fixed team size, Agent-count target, or ordinary numeric child ceiling in project policy. Native Codex capacity is a ceiling, never a target to fill.
4. Every child owns a distinct responsibility. Do not create duplicate, speculative, or low-value Agents just because capacity exists.
5. Preserve an upstream Skill or accepted plan that already owns goal, decomposition, stage order, dependencies, outputs, acceptance, or quality gates.
6. Luna Reader gathers narrow bounded evidence. Luna Worker implements clear, repeatable behavior that is already decided.
7. Sol Advisor handles demanding or material read-only judgment. Sol Solver handles implementation where demanding or material judgment is coupled to the write.
8. Terra Investigator handles bounded read-heavy technical investigation and evidence synthesis after semantics are stable and no material judgment remains. Terra is not an escalation rung.
9. Main-session Sol capability is a dedup optimization, never authority or task taxonomy.
10. Failure does not imply model escalation. Diagnose execution origin and the remaining semantic blocker.
11. One canonical checkout has one active writing actor inside this orchestration. Main writes, Luna Worker, and Sol Solver share that domain.
12. Filesystem isolation alone does not prove semantic independence.
13. Filesystem permission is capability, not mutation authority.
14. Child reports are claims. Accept from actual artifact state plus relevant deterministic or reproducible evidence.
15. Requested, platform-accepted, and runtime-observed route facts remain separate. Missing evidence stays missing.
16. Fresh independent Final Review is consequence-driven and artifact-bound.
17. Children do not create project Subagents. Delegation depth is one.
18. TeamPlan coordinates delegated work but does not choose models or replace Main.
19. UNKNOWN is not FAILED. Ambiguous native execution does not authorize duplicate work.
20. Do not emit orchestration ceremony when it adds no user value.

## 1. Understand the task

Identify:

```text
observable user outcome
scope / authorization
important invariants
acceptance conditions
known repository/runtime facts
```

Do not start by choosing Luna, Terra, Sol, an Agent count, or a pipeline.

If an active upstream Skill or accepted user plan already defines the workflow, keep its goal, stage order, dependencies, outputs, business acceptance, and quality gates authoritative. Reuse an existing useful plan or ledger rather than creating a second coordination truth source.

For one ordinary unresolved responsibility, keep compact state in context:

```text
outcome
owner
read/write intent
material judgment: none | separable | coupled
acceptance
valid evidence
current failure
blocker
```

Do not create TeamPlan or a persistent ledger merely because the mechanism exists.

## 2. Decide whether delegation helps

Use `references/router-core.md`.

Keep work in Main when a child would mostly duplicate context or add handoff overhead.

Delegate only for concrete value such as useful context isolation, independent parallel work that is ready now, clear repeatable bounded implementation, demanding or material Sol judgment, judgment-coupled Sol implementation, bounded read-heavy Terra investigation, or required independent final assurance.

A large task can justify several children when it contains several independent valuable responsibilities. A small task can justify none. Task size never maps to an Agent count by itself.

## 3. Complete readiness before delegated execution

This Skill is designed for explicit `$codex-delegate:codex-delegate` use. Codex users may also select it through `/skills`.

Once the task actually justifies a child, check the exact required project role before delegated implementation begins. If provisioning is missing:

```text
installer = skill_dir/../../scripts/install-agents.py
```

Explain that the installer manages only the five codex delegate profiles, `.codex-delegate-agents.json`, and `.codex-delegate-agents.lock`, request permission, then run:

```bash
python "$installer"
python "$installer" --check
```

The profile files use Codex's native custom-Agent TOML mechanism. The bundled installer supplies project-specific lifecycle, ownership, and fail-closed collision handling; it does not implement another Agent runtime.

If the current Codex thread cannot see newly provisioned roles until restart, stop before delegated code execution and ask the user to start a fresh thread. Do not discover this halfway through a Worker/Solver implementation.

Exact role mismatch fails closed. Do not substitute another role/model simply to keep moving.

## 4. Route the smallest useful responsibility

Use this mapping:

```text
narrow read-only factual evidence
-> main or codex_delegate_reader

write; behavior/invariants/acceptance already decided; remaining work clear/repeatable
-> main or codex_delegate_worker

demanding/material judgment before writing
-> capable main or codex_delegate_advisor

write where demanding/material judgment cannot be separated
-> capable main or codex_delegate_solver

semantics stable + bounded read-heavy technical investigation with no material judgment
-> main or codex_delegate_investigator
```

A task being large or contractable does not make it Luna work. A task being hard or technical does not make it Terra work. Demanding, ambiguous, multi-step technical reasoning that requires material judgment belongs on the Sol path.

Consult main-session model/effort only when material judgment already needs Sol capability and trusted current-session metadata is available or worth checking. `../../scripts/runtime-evidence.py` is optional diagnostic evidence, not an every-task hot-path dependency.

## 5. Coordinate only when coordination complexity exists

Each delegated Agent receives one bounded responsibility packet:

```text
TEAM PLAN REVISION, when applicable
UNIT ID
TASK ID
OUTCOME
INTENT: inspect | implement | verify | review
READ / WRITE SCOPE
MUTATION AUTHORITY: none | declared-output-only | bounded-source-write
INTERFACES AND INVARIANTS
DECISION RIGHTS
ACCEPTANCE
VALID EVIDENCE / DO NOT REDO
CURRENT FAILURE, if any
INTEGRATION AFTER, when needed
STOP WHEN
```

A single delegated responsibility does not require TeamPlan. Give it a stable `UNIT ID` and unique `TASK ID`, then keep the lightweight path.

Before two or more delegated responsibilities are concurrently unresolved, or when delegated outputs need non-trivial machine-checkable dependency/integration order, compile and validate `references/team-plan.md`.

TeamPlan owns structural dependency truth. Main still owns semantic independence, delegation value, role choice, and final acceptance.

Main manages a ready frontier rather than choosing a fixed team size up front. Start a child only when the responsibility is ready now, distinct, non-duplicative, semantically safe, worth the handoff and integration cost, and within current authority boundaries.

Use progressive fan-out. Start the smallest useful active set, process an exposed child completion when useful, merge valid evidence, update the ready frontier, and add another child only when new evidence makes another responsibility ready and delegation is still worthwhile.

Do not create speculative children, duplicate a satisfied responsibility, fill native capacity for appearance, impose an artificial wave barrier, or simulate event-driven scheduling with busy polling.

Read-only independent work is the preferred place to exploit parallelism. Concurrent writers require genuine filesystem isolation plus semantic independence or explicit dependency and integration order.

## 6. Verify, then diagnose blockers

When a child returns:

1. inspect actual artifact/diff/state;
2. inspect relevant verification results;
3. merge only supported new evidence;
4. check user acceptance;
5. if unresolved, diagnose both execution origin and semantic blocker.

The semantic blocker classes remain:

```text
contract
judgment
investigation
stalled
```

Then use `references/recovery.md` for lifecycle and bounded recovery.

```text
contract -> Main repairs task truth or acceptance
judgment -> capable Main or Sol
investigation -> Terra only for bounded read-heavy work after semantics stabilize and no material judgment remains
stalled -> one policy-compatible retry only when the role remains correct; otherwise Main takes over
```

Do not translate “Luna failed” directly into Terra or Sol.

Recovery is bounded to one focused same-Agent follow-up, at most two Agent attempts for one unchanged unit, semantic reroute only when the blocker changes capability need, and Main takeover when recovery is exhausted or unsafe.

UNKNOWN execution state forbids replacement, retry, reroute, or conflicting ownership reassignment until host evidence resolves the ambiguity.

## 7. Keep route truth layered

When route identity matters, preserve three separate facts:

```text
requested
accepted
observed
```

Requested is what routing asked for. Accepted is what the host explicitly acknowledged, when exposed. Observed is what the runtime actually reported, when exposed.

Do not turn accepted into observed. Do not copy configured model, effort, sandbox, ancestry, or identity values into missing runtime fields. Keep `unknown`, `not_reported`, or `not_observed` when that is the real evidence state.

Use `../../scripts/runtime-evidence.py` only when these distinctions materially affect capability dedup, hard permission claims, provenance, diagnostics, or release evidence.

## 8. Apply Final Review only when the candidate needs it

After ordinary acceptance reaches Candidate Ready, use `references/final-review.md`.

Prior use of Terra, Solver, recovery, TeamPlan, a large diff, or many files does not itself require review. The current artifact's consequences and any material verification gap decide the gate.

When review is required:

```text
bind exact candidate
-> fresh codex_delegate_advisor with fork_turns: none
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Only a fresh `ship` verdict for the unchanged candidate satisfies required independent review.

## 9. Report the task result

Normal completion focuses on:

```text
what changed
verification performed
remaining material risk, if any
```

Do not append a separate orchestration receipt merely because `$codex-delegate:codex-delegate` was explicitly invoked.

Mention routing, TeamPlan, or recovery only when it materially affected the result or user decision, such as additional consent, meaningful rerouting, unresolved UNKNOWN state, required Final Review, or an explicit user request for orchestration details.
