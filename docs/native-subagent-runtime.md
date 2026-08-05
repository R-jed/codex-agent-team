# Native Subagent Runtime Contract

codex delegate uses Codex Native Subagents and child threads directly. It does not create another Agent runtime, persistent scheduler, daemon, thread pool, or routing proxy.

The distinction is deliberate:

| Native Codex | codex delegate |
| --- | --- |
| runs the main session and child threads | decides whether delegation helps and which exact project role is useful |
| exposes whatever capacity/wait/update/runtime metadata the build supports | uses only observed capability without inventing a universal runtime contract |
| provides custom Agent configuration and sandbox/tool surfaces | adds one-writer, consent, trust, and exact-role boundaries |
| returns child output | verifies claims against the actual artifact and relevant evidence |

## Explicit entry point

The product follows the Codex Skill invocation convention:

```text
$codex-delegate <task>
```

Codex CLI/IDE users may also open the Skill picker with `/skills`. Implicit invocation is disabled. The user chooses when adaptive delegation is worth applying.

## First-use readiness

The exact project roles use Codex's native custom-Agent TOML mechanism. Personal custom Agents are stored under the active Codex home `agents` directory, normally `~/.codex/agents/`.

When an explicit task actually needs a child, role readiness is checked before delegated implementation starts. If profiles are missing, codex delegate asks permission, runs the bundled installer and `--check`, then verifies the role surface. The installer is a project-specific lifecycle and ownership layer around native custom Agent files; it is not a second runtime.

If the current Codex thread cannot discover newly provisioned roles until restart, the task stops before child writing and resumes in a fresh thread.

## Current exact roles

```text
codex_delegate_reader        -> gpt-5.6-luna  / max   / read-only
codex_delegate_worker        -> gpt-5.6-luna  / max   / workspace-write
codex_delegate_solver        -> gpt-5.6-sol   / high  / workspace-write
codex_delegate_investigator  -> gpt-5.6-terra / xhigh / read-only
codex_delegate_advisor       -> gpt-5.6-sol   / high  / read-only
```

Responsibility semantics follow the current model guidance:

```text
Luna Reader/Worker
-> clear, repeatable, bounded work

Terra Investigator
-> bounded read-heavy technical investigation / evidence synthesis after semantics stabilize

Sol Advisor/Solver
-> demanding, ambiguous, multi-step material judgment and judgment-coupled implementation
```

Terra is not an escalation rung above Luna. A difficult technical problem that still requires demanding or material judgment belongs on the Sol path.

Model-specific delegation requires the exact current profile. There is no built-in-role substitution or hidden model ladder.

Profile matching proves configuration intent only. It does not prove the route a live child actually ran.

## Main-session capability dedup

Main-session route evidence is optional optimization data.

Only when the router has already established that material judgment needs Sol capability may trusted current-session model/effort metadata be used to avoid a redundant Advisor/Solver call.

`policy-contract.json` owns the capability reference. `plugins/codex-delegate/scripts/runtime-evidence.py` normalizes observed metadata.

Current reference is Solver, GPT-5.6 Sol `high`:

```text
Sol family + high/xhigh/max
-> covered

Sol family + medium/low
-> uncovered

other model family
-> uncovered

missing / partial / local-only / conflicted / unranked effort
-> unknown
```

Routine bounded work does not inspect main-session metadata. `unknown` is allowed to remain unknown.

A covered main session can suppress ordinary Sol capability uplift. It cannot satisfy fresh independent review of its own final candidate.

## Runtime evidence is diagnostic

The helper supports:

```text
subject: main_session
subject: child
```

For child diagnostics it keeps route, ancestry, and permission evidence separate:

```text
route_evidence
ancestry_evidence
permission_evidence
```

Use runtime diagnostics when the claim actually depends on runtime observation, including:

- exact model/role/effort proof;
- hard host-enforced read-only;
- main capability dedup;
- ancestry when depth-one proof matters;
- independent-review provenance;
- configuration/runtime conflicts;
- release validation.

Do not run these checks as routine ceremony for every bounded child. Exact profile configuration plus real artifact verification may be sufficient when runtime route proof is not part of acceptance.

Configured values never become observed values by assumption.

## Completion and wait surface

The desired scheduling behavior is completion-driven when the native runtime exposes a usable completion surface.

For release-relevant builds characterize the strongest actually observed surface:

```text
barrier_only
per_child_terminal
any_child_update
```

These are observed runtime labels, not permanent Codex constants.

Example:

```text
A slow independent read-only task
B fast independent read-only task
C depends only on B

spawn A + B
B completes
-> process B
-> start C while A remains active only if the runtime exposes B completion and reusable capacity
```

If the runtime exposes only a barrier, codex delegate degrades to that surface. It does not simulate event-driven behavior with model-mediated busy polling.

Child progress observability is separate:

```text
none
terminal_only
periodic_summary
structured_live
```

A wake-up event does not imply deterministic insight into child progress.

## Capacity

codex delegate has no product-level hard child count.

Explicit `$codex-delegate` invocation includes up to two concurrently active justified children in the ordinary consent envelope. Larger fan-out requires user authorization unless the request already clearly asks for broad parallel work.

Actual active concurrency remains bounded by:

```text
useful independent work
writer safety
exact role availability
native runtime capacity
```

One observed capacity value applies only to the tested runtime/environment.

## Writer ownership

One canonical physical checkout has one active writing actor inside the current orchestration:

```text
main session while mutating
codex_delegate_worker
codex_delegate_solver
```

When a child writer owns the checkout, Main can continue read-only analysis but waits for ownership handoff before integration writes.

Concurrent writers require genuine filesystem isolation such as separate worktrees/workspaces/repositories.

This session-local rule cannot exclude another Codex session, editor, hook, or external process. Current safety relies on recommended isolation plus drift detection and fail-closed behavior. Cross-session coordination must be validated empirically before a stronger mechanism is added.

## Context transfer

Children normally use fresh context (`fork_turns=none`) and receive a compact responsibility packet from `references/router-core.md`.

Fresh context does not mean repeated discovery. Pass only task-local truth:

```text
outcome
scope
interfaces/invariants
decision rights
acceptance
valid evidence / DO NOT REDO
current failure, if any
stop condition
```

Do not transfer private reasoning or dead-end narration.

## Delegation depth

```text
main session -> child
child -> no further project delegation
```

Unexpected descendants are outside the supported product contract.

## Lifecycle

Process completed/no-longer-needed children promptly and close them when the native surface supports it so capacity can recover.

If a runtime shows stale slots, blocking close operations, missing completion signals, absent route metadata, or other limitations, record the exact build and adapt product claims. Do not hide runtime limitations behind policy wording.

## User-facing takeaway

codex delegate decides when additional native compute is useful and keeps it inside a small set of quality/safety boundaries. Native Codex decides how sessions and child threads actually execute.

This separation lets the Plugin improve daily development without becoming a second orchestration runtime.
