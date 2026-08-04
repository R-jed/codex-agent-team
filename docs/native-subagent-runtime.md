# Native Subagent Runtime Contract

Codex Delegate uses Codex's native Subagent/thread mechanisms. A **Subagent** is the delegated actor; an **Agent thread** is the native child thread where that actor runs.

The project does not create a second Agent runtime, persistent scheduler, custom thread pool, background daemon, or routing proxy.

## Native versus policy responsibilities

| Native Codex | Codex Delegate policy |
| --- | --- |
| spawn/run child threads | decide which unresolved dependencies deserve children |
| expose some capacity/wait/update surface | use available capacity without inventing a product hard ceiling |
| close/interrupt/inspect threads when supported | process completed work promptly and recover slots |
| custom Agent configuration | require exact semantic project roles |
| tool/sandbox behavior | add one-writer and runtime-evidence safety rules |
| child output/progress | treat reports as claims until artifacts/evidence are checked |

## Completion-driven scheduling contract

Codex Delegate's desired scheduling policy is completion-driven:

```text
compute ready frontier
-> dispatch safe useful dependencies into available native capacity
-> react when an individual child completion/material update is exposed
-> inspect/merge/update/close that child
-> recompute frontier
-> refill freed capacity immediately when newly-ready work exists
```

Example:

```text
A slow, independent
B fast, independent
C requires B only

spawn A + B
B completes
-> process B
-> start C while A is still active, if the runtime exposes B's completion and a slot is available
```

This avoids an unnecessary batch barrier.

A barrier is valid when a real join dependency requires all active results. A barrier may also be unavoidable when the tested Codex runtime exposes only a coarser wait/consolidation surface.

The policy must degrade to the surface actually available; it must not claim an event-driven runtime that was not observed.

## Wait/update surface is runtime evidence

For every release-relevant runtime, characterize the strongest actual child-completion surface, for example:

```text
barrier_only
per_child_terminal
any_child_update
```

Interpretation:

- `barrier_only`: the usable orchestration surface returns only after the relevant requested set is complete;
- `per_child_terminal`: the main session can wait/inspect one selected child independently;
- `any_child_update`: the main session can block for whichever live child next has a meaningful update/final status.

These labels describe tested behavior, not permanent Codex architecture constants.

Avoid model-mediated busy polling. If a native blocking wait/update mechanism exists, prefer it over repeated model turns whose only action is status checking. If the current runtime forces polling, record the limitation and its observed cost rather than hiding it behind a policy claim.

## Main-session work while children run

Native child execution need not make the main session conceptually idle. When the tool/runtime surface allows it, the main session may perform independent work while children are active, such as preparing acceptance checks, reviewing unaffected context, or processing another completed child.

It must not duplicate a child's assigned responsibility or create conflicting writes merely to appear busy.

## Adaptive capacity

Codex Delegate defines no product hard child count.

Explicit `/codex-delegate` use permits up to two concurrently active justified children without another consent prompt. Larger fan-out normally needs authorization unless already implied by the user request.

After authorization, actual active concurrency is bounded by:

```text
useful ready dependencies
workspace safety
exact role availability
native runtime capacity
```

Excess ready work remains pending. When a child completes and the runtime releases its slot, completion-driven policy refills that slot if useful work is ready.

An observed capacity of 4, 6, or another number proves only the tested build/environment behavior.

## Semantic roles and exact profiles

Current roles are configured as:

```text
codex_delegate_reader        -> gpt-5.6-luna / max
codex_delegate_worker        -> gpt-5.6-luna / max
codex_delegate_investigator  -> gpt-5.6-terra / xhigh
codex_delegate_advisor       -> gpt-5.6-sol / high
```

Model-specific delegation uses exact custom project profiles. There is no Portable Mode or built-in-role substitution.

The Plugin bundles the profile templates. After explicit user approval, the managed installer provisions them into the active personal Codex-home `agents` directory and records exact project ownership in `.codex-delegate-agents.json`.

The installer manages only the current project profiles. Other Agent profiles remain user-owned and are not modified or removed.

Profile matching establishes configuration assurance only. It does not prove what a child actually ran as.

## Runtime observations

When post-spawn proof matters, Runtime Evidence keeps concerns separate:

```text
route_evidence
ancestry_evidence
permission_evidence
```

The bundled normalized verifier requires complete evidence for complete claims. Partial observations remain partial. A configured read-only sandbox is not proof of host enforcement.

See the installed `references/runtime-assurance.md`.

## Child progress observability

Completion/update notification and structured in-flight execution progress are different capabilities.

Characterize child-progress observability separately:

```text
none
terminal_only
periodic_summary
structured_live
```

A runtime may support `any_child_update` for completion/status while still exposing only `terminal_only` useful execution evidence. Do not infer deterministic mid-run anti-thrashing from a wake-up event or streaming prose.

If rich progress is unavailable, Codex Delegate performs recovery at dependency/return level. That is an explicit boundary, not a reason to invent telemetry.

## Context and evidence

Role-specific work uses fresh context by default (`fork_turns=none`) because the Delegation Contract carries the task-local facts needed by the child.

Fresh context does not mean fresh discovery. Pass valid evidence, current artifact/failure, unresolved delta, acceptance, and explicit `DO NOT REDO` facts while omitting private reasoning and dead-end narration.

## Recursion and workspace policy

Delegation depth remains one:

```text
main session -> child
child -> no further project delegation
```

One canonical physical checkout has at most one active Writing Worker. Multiple writers require genuine filesystem isolation such as runtime-backed worktrees or independent repositories.

Read-only children may fan out across independent dependencies when consent and native capacity allow.

## Lifecycle

Process completed child results promptly and close completed/no-longer-needed threads when supported so capacity can recover.

Do not assume close/wait operations are instantaneous or nonblocking. If a tested runtime shows stale slots, long blocking close operations, repeated wait polling, or missing completion notifications, record that as version-scoped runtime evidence and adapt release claims accordingly.

## User-facing takeaway

Codex Delegate controls **what should run and when newly available capacity should be used**. Native Codex controls **how child threads actually execute and which completion/progress signals exist**.

That distinction is why performance cannot be reduced to either "better prompts" or "more Agent slots" alone.
