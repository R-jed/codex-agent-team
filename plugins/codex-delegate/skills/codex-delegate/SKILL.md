---
name: codex-delegate
description: Delegate only when it improves the task, keep bounded execution on Luna, place material judgment on Sol, use Terra only for narrow specialist uncertainty, preserve one-writer safety, and apply fresh independent review only when the final artifact requires it.
---

# codex delegate

codex delegate is a thin policy layer over Codex Native Subagents. The current user-facing main session stays in control. The product exists to make everyday development more reliable without forcing users to design an Agent team or pay for unnecessary review loops.

The runtime policy has three owners only:

- `references/router-core.md`: delegation benefit, actor selection, child packet, reroute, scheduling, acceptance
- `references/guardrails.md`: consent, writer ownership, permissions, trust boundaries, provisioning, runtime evidence
- `references/final-review.md`: independent artifact-bound final assurance

Stable role/model constants and review reason codes live in `../../policy-contract.json`.

## Core invariants

1. Main session owns user intent, authorization, integration, acceptance, and final response.
2. Zero children is normal. Delegation must provide concrete value.
3. Luna Reader gathers bounded evidence. Luna Worker implements behavior that is already decided.
4. Sol Advisor handles material read-only judgment. Sol Solver handles implementation where material judgment is coupled to the write.
5. Terra Investigator receives only a narrow difficult technical question after semantics are stable.
6. Main-session Sol capability is a dedup optimization, not task taxonomy or authority. Do not buy duplicate Sol capability when trusted current-session evidence already covers it.
7. Failure does not imply model escalation. Diagnose the remaining blocker and reroute only when the work really changed.
8. One canonical checkout has one active writing actor inside this orchestration. Main writes, Luna Worker, and Sol Solver share that domain.
9. Child reports are claims. Accept from actual artifact state plus relevant deterministic or reproducible evidence.
10. Fresh independent Final Review is on demand for consequential artifacts. A Sol main does not review its own candidate independently.
11. Children do not create project Subagents. Delegation depth is one.
12. Do not emit orchestration ceremony when it adds no user value.

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

Maintain one compact task state per unresolved work item:

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

Do not maintain separate ledgers unless the task genuinely needs persistent structured state.

## 2. Decide whether delegation helps

Use `references/router-core.md`.

Keep the task in main when delegation would mostly duplicate context or add handoff overhead.

Delegate only for concrete value such as:

- useful context isolation;
- independent read-only work;
- standardized bounded implementation;
- material Sol judgment or judgment-coupled implementation;
- narrow specialist technical investigation;
- required independent final assurance.

## 3. Complete readiness before delegated execution

This Skill is designed for explicit `/codex-delegate` use.

Once the task actually justifies a child, check the exact required project role before delegated implementation begins. If provisioning is missing:

```text
installer = skill_dir/../../scripts/install-agents.py
```

Explain that the installer manages only the five codex delegate profiles plus `.codex-delegate-agents.json`, request permission, then run:

```bash
python "$installer"
python "$installer" --check
```

If the current Codex thread cannot see newly provisioned roles until restart, stop before delegated code execution and ask the user to start a fresh thread. Do not discover this halfway through a Worker/Solver implementation.

Exact role mismatch fails closed. Do not substitute another role/model simply to keep moving.

## 4. Route the smallest useful responsibility

The practical mapping is:

```text
read-only factual evidence
-> main or codex_delegate_reader

write; behavior/invariants/acceptance already decided
-> main or codex_delegate_worker

material judgment before writing
-> capable main or codex_delegate_advisor

write where material judgment cannot be separated
-> capable main or codex_delegate_solver

semantics stable + narrow difficult technical uncertainty
-> main or codex_delegate_investigator
```

A task being large or contractable does not make it Luna work.

Consult main-session model/effort only when material judgment already needs Sol capability and trusted current-session metadata is available or worth checking. `../../scripts/runtime-evidence.py` is an optional diagnostic for that dedup decision and other runtime claims. It is not part of every routine task.

## 5. Run with minimal safe coordination

Compile one bounded responsibility packet using `router-core.md`.

Use the smallest useful set of children. Explicit `/codex-delegate` permits up to two concurrently active justified children inside the ordinary consent envelope, subject to native capacity and `guardrails.md`.

Read-only independent work may run concurrently. A canonical checkout has only one writing actor inside this orchestration. If Worker or Solver owns the write, main stays read-only in that checkout until ownership returns.

Process exposed child completion when useful. Do not manufacture a wave barrier, busy-poll telemetry the runtime does not expose, or repeat discovery that valid evidence already covers.

## 6. Verify, then diagnose blockers

When a child returns:

1. inspect actual artifact/diff/state;
2. inspect relevant verification results;
3. merge only supported new evidence;
4. check the user acceptance conditions;
5. if unresolved, diagnose the blocker.

Use only these blocker classes in the hot path:

```text
contract
judgment
specialist
stalled
```

Then:

```text
contract -> main repairs task truth or acceptance
judgment -> main/Sol handles the material decision
specialist -> Terra only for a narrow technical delta after semantics are stable
stalled -> at most one clean same-role retry when the role remains correct and the packet is materially improved
```

Do not translate “Luna failed” directly into Terra or Sol.

## 7. Apply Final Review only when the candidate needs it

After normal acceptance reaches Candidate Ready, use `references/final-review.md`.

Prior use of Terra, Solver, recovery, a large diff, or many files does not itself require review. The current artifact's consequences and any material verification gap decide the gate.

When review is required:

```text
bind exact candidate
-> fresh codex_delegate_advisor with fork_turns: none
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Only a fresh `ship` verdict for the unchanged candidate satisfies required independent review.

## 8. Report the task result

Normal completion output focuses on:

```text
what changed
verification performed
remaining material risk, if any
```

Do not append a separate orchestration receipt just because `/codex-delegate` was explicitly invoked.

Mention routing only when it materially affected the result or user decision, such as additional consent, meaningful rerouting, a route/runtime limitation, required Final Review, or an explicit user request for orchestration details.
