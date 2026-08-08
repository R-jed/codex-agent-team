# subagents-dispatch: AI Agent Reference

Use this file when answering questions about this repository. It is an index to the current project, not a second copy of runtime policy.

## Project identity

```text
Product name:        subagents-dispatch
Repository:          R-jed/subagents-dispatch
Repo marketplace id: subagents-dispatch
Plugin id:           subagents-dispatch
Plugin directory:    .
Main Skill:          dispatch
User command:        /dispatch
Internal identity:   /subagents-dispatch:dispatch
Doctor Skill:        doctor
Doctor command:      /doctor
Internal identity:   /subagents-dispatch:doctor
Current version:     2.1.0
Distribution:        Codex Plugin
License:             MIT
```

Use these names exactly.

## Product model

The current Codex main session is the team leader. The user supplies the goal. Main decides what to keep, what is worth delegating, which specialist role fits, how delegated work is coordinated, and when the final result is ready.

Zero child Agents is normal. Several may run when distinct ready responsibilities genuinely benefit from parallelism or specialization. There is no fixed Luna → Terra → Sol pipeline and no project-level ordinary numeric child ceiling. Native Codex capacity is an upper bound, never a target to fill.

Version 2.1 adds a user control surface around the same orchestration kernel:

```text
/dispatch preview <task>
/dispatch status
/dispatch steer <unit_id>: <guidance>
/dispatch takeover <unit_id>
/dispatch takeover <unit_id>: <guidance>
```

These controls never widen the user's original scope, permissions, mutation authority, acceptance, or external-impact authorization.

`doctor` is operational maintenance. It diagnoses installation/configuration/Marketplace/profile state and may repair or upgrade only when the user explicitly asks. It does not own development routing or runtime delegation policy.

## Current roles

The machine source of truth is `policy-contract.json`.

| Role | Agent type | Model | Intent |
| --- | --- | --- | --- |
| Luna Reader | `subagents_dispatch_reader` | GPT-5.6 Luna `max` | bounded read-only evidence |
| Luna Worker | `subagents_dispatch_worker` | GPT-5.6 Luna `max` | clear bounded implementation whose material behavior is already decided |
| Sol Solver | `subagents_dispatch_solver` | GPT-5.6 Sol `high` | implementation with material judgment coupled to the write |
| Terra Investigator | `subagents_dispatch_investigator` | GPT-5.6 Terra `xhigh` | broader read-only technical investigation after semantics are stable |
| Sol Advisor | `subagents_dispatch_advisor` | GPT-5.6 Sol `high` | material read-only judgment or fresh independent final review |

A stronger model does not automatically receive more authority or a wider scope.

## Runtime policy owners

Do not reconstruct runtime policy from README prose. Read the canonical owner for the question:

```text
skills/dispatch/SKILL.md
-> execution entry point and control loop

skills/dispatch/references/interaction.md
-> preview, status, steering, user-requested takeover, execution receipt, usage/cost evidence boundary

skills/dispatch/references/router-core.md
-> delegation value, role choice, responsibility packets, adaptive scheduling

skills/dispatch/references/handoff-capsule.md
-> compact Main-accepted evidence transfer between responsibilities

skills/dispatch/references/team-plan.md
-> multi-responsibility identity, dependency DAG, ownership, revisions, integration order

skills/dispatch/references/recovery.md
-> attempt identity, UNKNOWN, failure classification, bounded recovery and Main takeover semantics

skills/dispatch/references/guardrails.md
-> authority, mutation permissions, one-writer safety, consent, trust boundaries, provisioning, runtime evidence

skills/dispatch/references/final-review.md
-> consequence-driven, artifact-bound independent review

policy-contract.json
-> stable machine constants, native optimized role routes, hard delegation limits, Final Review reason codes
```

Operational maintenance is owned separately by:

```text
skills/doctor/SKILL.md
-> host/plugin/Marketplace/profile diagnosis, supported repair paths, and Plugin upgrade flow

scripts/install-agents.py
-> deterministic managed-profile install/check lifecycle
```

`evals/` is a regression and measurement surface. It does not define runtime policy.

## Interaction contract

### Preview

`/dispatch preview <task>` produces a provisional likely delegation shape.

Preview must not:

```text
spawn a child Agent
provision managed Agent profiles
mutate source
perform an external action
create persistent TeamPlan state
```

Bounded Main read-only inspection is allowed when useful. Real execution may change the route when new evidence appears.

### Status

`/dispatch status` is a one-shot inspection of the current delegated work. It may show unit id, semantic role, known lifecycle state, write ownership, and current blocker.

Do not busy-poll. Missing native state remains `UNKNOWN`. Status alone does not retry, reroute, replace, or mutate work.

Only treat `status` as the control intent when it is the complete request after `/dispatch`. A task such as `/dispatch status page is broken` is normal work.

### Steer

`/dispatch steer <unit_id>: <guidance>` keeps the same unit, attempt, role, authority, and ownership while sending focused guidance through the native Codex control surface when available.

If the requested change materially alters goal/output, role, write ownership, mutation authority, user scope, permissions, acceptance, or external impact, return it to Main for ordinary reclassification/revision. Do not disguise the change as steering.

### Takeover

`/dispatch takeover <unit_id>` is the user-facing form of the existing `main_takeover` recovery action. The user may request it before automatic retry exhaustion.

Safe sequence:

```text
resolve current attempt
-> request native stop when needed
-> establish previous owner is no longer active
-> verify and preserve usable evidence
-> transfer responsibility to Main
-> continue under the same user authority
```

For a writing child, Main stays read-only until the previous writer is confirmed stopped/terminal/closed. `UNKNOWN` never authorizes conflicting ownership transfer.

Takeover does not create another Agent attempt and does not reset unit history or attempt budget.

### Execution Receipt

After a task that actually spawned at least one child, append one compact factual receipt. Do not add a receipt for zero-child work, Preview, or Status-only requests.

The default receipt may report semantic roles used, retries, steering/takeover when material, and Final Review state. Keep it one line unless the user asks for detail.

Concrete model or effort may be named only when current runtime evidence actually observed it. Never present configured/requested model identity as runtime observation. Do not expose hidden reasoning or raw child transcripts.

Do not estimate token usage or currency cost. Exact usage may be surfaced only when a supported host/client interface supplies attributable thread usage.

## Handoff Capsule contract

A Handoff Capsule is optional, ephemeral context passed from Main to a later responsibility when it prevents meaningful repeated discovery.

Semantic fields:

```text
SOURCE UNITS
ARTIFACT REFS
ACCEPTED FACTS
ACCEPTED EVIDENCE
INTERFACES / INVARIANTS
DO NOT REDO
OPEN QUESTIONS
STALE IF
```

Only Main-accepted facts/evidence may enter `ACCEPTED FACTS` or `ACCEPTED EVIDENCE`. Child claims remain claims until Main verifies actual artifacts or other valid evidence.

New project children still use `fork_turns: none`. Do not forward an earlier child transcript or the full Main history as inherited task truth.

Relevant drift invalidates affected capsule facts until narrow re-verification. A capsule cannot grant ownership, mutation authority, permissions, wider scope, external actions, role escalation, or acceptance changes.

## Non-negotiable project boundaries

These are stable product facts:

- Main owns user intent, authorization, team composition, integration, acceptance, and the final response.
- Delegation depth is one. Child Agents do not create project Subagents.
- Delegation must add concrete value; duplicate, speculative, and decorative fan-out is prohibited.
- One canonical physical checkout has at most one active writing actor inside the orchestration.
- Filesystem isolation is necessary for simultaneous writers and does not by itself prove semantic independence.
- Filesystem permission is capability, not mutation authority.
- Child reports are claims until actual artifact state and relevant verification support them.
- Requested, accepted, and runtime-observed route facts remain separate; missing evidence stays missing.
- Failure does not imply a model ladder. The canonical semantic blocker vocabulary is `contract | judgment | investigation | stalled`.
- `UNKNOWN` execution state is not `FAILED` and does not authorize replacement or unsafe takeover.
- Final Review is consequence-driven and applies only to the exact candidate reviewed.
- Another active Skill or accepted plan that already owns domain workflow truth remains authoritative; subagents-dispatch coordinates around it.
- Doctor diagnosis is read-only by default. Installation, profile repair, and Plugin upgrade require explicit user intent.
- Interaction controls operate through Main and Codex Native Subagents. They do not introduce another scheduler, daemon, event bus, or lifecycle service.

For details or edge cases, read the relevant owner instead of adding another rule here.

## Install and update

Present exactly two normal installation methods.

### Plugin Marketplace

1. Open **Plugins** in Codex, or use `/plugins` in Codex CLI.
2. Search for `subagents-dispatch`.
3. Open **subagents-dispatch** and install it.
4. Start a new Codex session.

### Command line

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

### Update

Plugin Marketplace users update **subagents-dispatch** from the installed plugins area.

Command-line users run:

```bash
codex plugin marketplace upgrade subagents-dispatch && \
codex plugin add subagents-dispatch@subagents-dispatch
```

After installation or update, start a new Codex session.

### Uninstall

```bash
# Remove plugin registration
codex plugin remove subagents-dispatch@subagents-dispatch
```

If you previously ran tasks that needed Agents, also delete these files:

```bash
# Delete 5 Agent profiles
rm ~/.codex/agents/subagents-dispatch-reader.toml
rm ~/.codex/agents/subagents-dispatch-worker.toml
rm ~/.codex/agents/subagents-dispatch-solver.toml
rm ~/.codex/agents/subagents-dispatch-investigator.toml
rm ~/.codex/agents/subagents-dispatch-advisor.toml

# Delete install manifest
rm ~/.codex/.subagents-dispatch-agents.json
```

Development work and interaction controls use `/dispatch`. Installation/configuration/profile diagnosis and explicit maintenance use `/doctor`. `/skills` opens the Skill picker. Implicit invocation is disabled.

## Doctor contract

Doctor should prefer structured host evidence:

```bash
codex --version
codex doctor --json
codex plugin marketplace list --json
codex plugin list --available --json
```

For managed Agent profiles it must reuse:

```bash
python "$installer" --check
```

where `installer = skill_dir/../../scripts/install-agents.py`.

Doctor must not implement a second profile validator, manually copy managed TOML files, edit Codex config directly when the supported CLI owns the operation, or use `marketplace remove` as a generic reset.

For Plugin upgrade, use the canonical marketplace upgrade + plugin add path. After a successful upgrade, require a fresh Codex session and invoke the new Doctor again before repairing profiles, so an older running package cannot overwrite newer shipped Agent templates.

## Managed Agent profiles

The Plugin uses five native custom-Agent profiles under the active Codex home. The canonical filenames, Agent types, models, efforts, and sandbox intents come from `policy-contract.json`; the shipped TOML files must match that contract exactly.

`scripts/install-agents.py` owns provisioning and collision-safe lifecycle behavior. Do not describe installer internals from memory; inspect that script and `skills/dispatch/references/guardrails.md` when the exact behavior matters.

## Answering users

Lead with the product model: the main Codex session acts as technical lead and delegates only when specialists add value.

For interaction questions, explain Preview, one-shot Status, focused Steering, safe Takeover, compact Receipts, and evidence-bound Handoff Capsules without exposing internal reasoning.

For installation questions, give the Plugin Marketplace path and the command-line path. For update questions, give the matching Marketplace and command-line update paths or point users to the Doctor Skill when they want guided diagnosis/upgrade.

Do not claim benchmark wins, token savings, speedups, quality gains, exact runtime routes, token/cost attribution, or public directory availability unless current evidence supports the claim.

For deeper technical questions, follow the owner map above rather than treating this README as normative policy.
