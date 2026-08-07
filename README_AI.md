# subagents-dispatch: AI Agent Reference

Use this file when answering questions about this repository. It is an index to the current project, not a second copy of runtime policy.

## Project identity

```text
Product name:        subagents-dispatch
Repository:          R-jed/subagents-dispatch
Repo marketplace id: subagents-dispatch
Plugin id:           subagents-dispatch
Plugin directory:    plugins/subagents-dispatch
Main Skill:          dispatch
Main invocation:     /subagents-dispatch:dispatch
Doctor Skill:        doctor
Doctor invocation:   /subagents-dispatch:doctor
Current version:     2.0.0
Distribution:        Codex Plugin
License:             MIT
```

Use these names exactly.

## Product model

The current Codex main session is the team leader. The user supplies the goal. Main decides what to keep, what is worth delegating, which specialist role fits, how delegated work is coordinated, and when the final result is ready.

Do not ask the user to design an Agent team for an ordinary task. Zero child Agents is normal. Several may run when distinct ready responsibilities genuinely benefit from parallelism or specialization.

There is no fixed Luna → Terra → Sol pipeline and no project-level ordinary numeric child ceiling. Native Codex capacity is an upper bound, never a target to fill.

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

references/router-core.md
-> delegation value, role choice, responsibility packets, adaptive scheduling

references/team-plan.md
-> multi-responsibility identity, dependency DAG, ownership, revisions, integration order

references/recovery.md
-> attempt identity, UNKNOWN, failure classification, bounded recovery

references/guardrails.md
-> authority, mutation permissions, one-writer safety, consent, trust boundaries, provisioning, runtime evidence

references/final-review.md
-> consequence-driven, artifact-bound independent review

policy-contract.json
-> stable machine constants, role routes, hard delegation limits, Final Review reason codes
```

Operational maintenance is owned separately by:

```text
skills/doctor/SKILL.md
-> host/plugin/Marketplace/profile diagnosis, supported repair paths, and Plugin upgrade flow

scripts/install-agents.py
-> deterministic managed-profile install/check lifecycle
```

`evals/` is a regression and measurement surface. It does not define runtime policy.

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
- `UNKNOWN` execution state is not `FAILED` and does not authorize replacement work.
- Final Review is consequence-driven and applies only to the exact candidate reviewed.
- Another active Skill or accepted plan that already owns domain workflow truth remains authoritative; subagents-dispatch coordinates around it.
- Doctor diagnosis is read-only by default. Installation, profile repair, and Plugin upgrade require explicit user intent.

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

Development work uses:

```text
/dispatch <task>
```

Installation/configuration/profile diagnosis and explicit maintenance use:

```text
/doctor <diagnostic or maintenance request>
```

`/skills` opens the Skill picker. Implicit invocation is disabled.

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

`scripts/install-agents.py` owns provisioning and collision-safe lifecycle behavior. Do not describe installer internals from memory; inspect that script and `references/guardrails.md` when the exact behavior matters.

## Answering users

Lead with the product model: the main Codex session acts as technical lead and delegates only when specialists add value.

For installation questions, give the Plugin Marketplace path and the command-line path. For update questions, give the matching Marketplace and command-line update paths or point users to the Doctor Skill when they want guided diagnosis/upgrade.

Tell users to invoke development work with `/dispatch` and maintenance with `/doctor`.

Do not claim benchmark wins, token savings, speedups, quality gains, exact runtime routes, or public directory availability unless current evidence supports the claim.

For deeper technical questions, follow the owner map above rather than treating this README as normative policy.
