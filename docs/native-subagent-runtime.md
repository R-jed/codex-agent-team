# Native Subagent Runtime Contract

Codex Delegate uses Codex's native Subagent/thread mechanisms. A **Subagent** is the delegated actor; an **Agent thread** is the native child thread where that actor runs.

The project does not create a second Agent runtime, persistent scheduler, custom thread pool, background daemon, or routing proxy.

## Native versus policy responsibilities

| Native Codex | Codex Delegate policy |
| --- | --- |
| run the current main session | observe main-route metadata only when the host exposes it and routing actually needs it |
| spawn/run child threads | decide which classified unresolved dependencies deserve children |
| expose some capacity/wait/update surface | use available capacity without inventing a product hard ceiling |
| close/interrupt/inspect threads when supported | process completed work promptly and recover slots |
| custom Agent configuration | require exact semantic project roles |
| tool/sandbox behavior | add current-session writer ownership and runtime-evidence safety rules |
| child output/progress | treat reports as claims until artifacts/evidence are checked |

## Main-session model evidence

Routing V4 distinguishes authority from judgment capability.

The main session always remains the control plane. `policy-contract.json` declares `classification.main_coverage_reference_role`, and the runtime verifier derives the current judgment reference model from that role rather than maintaining another hard-coded model identity.

When material judgment is unresolved, trusted current-session metadata may establish:

```text
covered   -> complete native metadata matches the policy-owned judgment reference family
uncovered -> complete native metadata identifies another model family
unknown   -> metadata is missing, partial, local-only, or conflicted
```

The current reference role is Solver, currently GPT-5.6 Sol `high`.

Use `plugins/codex-delegate/scripts/runtime-evidence.py` with `subject: main_session` to normalize that evidence.

Do not infer the main model from child profiles, repository files, cached state, or another Agent's statement. Do not ask for or inspect main-route metadata merely for routine bounded work. Unknown coverage is a conservative routing state, not a reason to always spawn Sol.

Covered main judgment capability suppresses redundant capability-uplift Sol calls for normal judgment and judgment-coupled execution. It does not satisfy a required fresh independent Final Review of the integrated candidate.

## Completion-driven scheduling contract

Codex Delegate's desired scheduling policy remains completion-driven:

```text
compute ready frontier
-> classify ready dependencies
-> dispatch the smallest useful safe set into available native capacity
-> react when an individual child completion/material update is exposed
-> inspect / merge evidence / reclassify if needed / close that child
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
-> start C while A remains active, if the runtime exposes B's completion and a slot is available
```

A barrier is valid when a real join dependency requires every relevant result. A barrier may also be unavoidable when the tested Codex runtime exposes only a coarser wait/consolidation surface.

The policy degrades to the surface actually available. It never claims event-driven behavior that was not observed.

## Wait/update surface is runtime evidence

For every release-relevant runtime, characterize the strongest actual child-completion surface:

```text
barrier_only
per_child_terminal
any_child_update
```

Interpretation:

- `barrier_only`: the usable orchestration surface returns only after the requested set is complete;
- `per_child_terminal`: the main session can wait/inspect one selected child independently;
- `any_child_update`: the main session can block for whichever live child next exposes a meaningful update/final status.

These labels describe tested behavior, not permanent Codex architecture constants.

Avoid model-mediated busy polling. Prefer native blocking wait/update mechanisms when available. If the runtime forces polling, record the limitation and observed cost rather than hiding it behind policy claims.

## Main-session work while children run

When the native surface allows it, the main session may continue independent work while children run, such as preparing acceptance checks, integrating a completed read-only dependency, or resolving a separate judgment it already covers.

It must not duplicate a child's owned dependency. If Worker or Solver owns a writing dependency in the same canonical checkout, main-session work in that checkout remains read-only until a clear writer-ownership handoff occurs. Main may write concurrently only in a genuinely isolated workspace.

## Adaptive capacity

Codex Delegate defines no product hard child count.

Explicit `/codex-delegate` use permits up to two concurrently active justified children without another consent prompt. Larger fan-out normally requires authorization unless already implied by the user request.

After authorization, actual active concurrency is bounded by:

```text
useful ready dependencies
workspace safety
exact role availability
native runtime capacity
```

Excess work remains pending. When a child completes and a native slot becomes reusable, completion-driven policy may refill that slot with newly-ready useful work.

One observed capacity proves only the tested build/environment behavior.

## Semantic roles and exact profiles

Current Routing V4 roles are:

```text
codex_delegate_reader        -> gpt-5.6-luna / max   / read-only
codex_delegate_worker        -> gpt-5.6-luna / max   / workspace-write
codex_delegate_solver        -> gpt-5.6-sol  / high  / workspace-write
codex_delegate_investigator  -> gpt-5.6-terra / xhigh / read-only
codex_delegate_advisor       -> gpt-5.6-sol  / high  / read-only
```

Role semantics are:

```text
Reader        evidence
Worker        bounded_execution
Solver        judgment_coupled_execution
Investigator  technical_investigation
Advisor       judgment or fresh independent final review
```

Model-specific delegation uses exact custom project profiles. There is no Portable Mode, built-in-role substitution, or hidden fallback ladder.

After explicit user approval, the managed installer provisions current profiles into the active Codex-home `agents` directory and records project ownership in `.codex-delegate-agents.json`. Other Agent profiles remain user-owned and untouched.

Profile matching establishes configuration assurance only. It does not prove what a child actually ran as.

## Child runtime observations

When post-spawn proof matters, child Runtime Evidence keeps concerns separate:

```text
route_evidence
ancestry_evidence
permission_evidence
```

The bundled verifier requires complete evidence for complete claims. Partial observations remain partial. A configured read-only sandbox is not proof of host enforcement.

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

A runtime may support `any_child_update` while exposing only terminal-quality execution evidence. Do not infer deterministic mid-run anti-thrashing from a wake-up event or streaming prose.

If rich progress is unavailable, Codex Delegate verifies and reclassifies at dependency return/completion boundaries. It does not invent telemetry.

## Context and evidence

Role-specific children use fresh context by default (`fork_turns=none`) because the Delegation Contract carries the task-local truth they need.

Fresh context does not mean fresh discovery. Pass valid evidence, current artifact/failure, unresolved delta, acceptance, and explicit `DO NOT REDO` facts while omitting private reasoning and dead-end narration.

## Recursion and writer policy

Delegation depth remains one:

```text
main session -> child
child -> no further project delegation
```

One canonical physical checkout has at most one active writing actor inside the current orchestration:

```text
main session while mutating the checkout
codex_delegate_worker
codex_delegate_solver
```

A child writer and the main session do not concurrently mutate the same checkout. Transfer writer ownership at a clear dependency boundary. Multiple simultaneous writers require genuine filesystem isolation such as runtime-backed worktrees/workspaces or independent repositories.

This session-local policy cannot exclude another Codex session, editor, hook, or process. External drift remains an observed runtime/workspace condition and writing responsibilities fail closed when it invalidates their contract.

Read-only children may fan out across independent dependencies when consent and native capacity allow.

## Lifecycle

Process completed child results promptly and close completed/no-longer-needed threads when supported so capacity can recover.

Do not assume close/wait operations are instantaneous or nonblocking. If a tested runtime shows stale slots, long blocking close operations, repeated wait polling, missing main-route metadata, or missing completion notifications, record that as version-scoped runtime evidence and adapt release claims accordingly.

## User-facing takeaway

Codex Delegate controls **what unresolved responsibility should run where**, **who owns writes in a checkout**, and **when newly available capacity should be used**. Native Codex controls **how the main session and child threads actually execute and which route/completion/progress signals exist**.

That distinction is why routing quality cannot be reduced to model prestige, cheaper tokens, or more Agent slots alone.
