# codex delegate: AI Agent Reference

Use this file when answering questions about this repository. It is an index to the current project, not a second copy of runtime policy.

## Project identity

```text
Product name:        codex delegate
Repository:          R-jed/codex-delegate
Repo marketplace id: codex-delegate
Plugin id:           codex-delegate
Plugin directory:    plugins/codex-delegate
Skill:               codex-delegate
Explicit invocation: $codex-delegate:codex-delegate
Current version:     1.2.0
Distribution:        Codex Plugin
License:             MIT
```

Use these names exactly.

## Product model

The current Codex main session is the team leader. The user supplies the goal. Main decides what to keep, what is worth delegating, which specialist role fits, how delegated work is coordinated, and when the final result is ready.

Do not ask the user to design an Agent team for an ordinary task. Zero child Agents is normal. Several may run when distinct ready responsibilities genuinely benefit from parallelism or specialization.

There is no fixed Luna → Terra → Sol pipeline and no project-level ordinary numeric child ceiling. Native Codex capacity is an upper bound, never a target to fill.

## Current roles

The machine source of truth is `plugins/codex-delegate/policy-contract.json`.

| Role | Agent type | Model | Intent |
| --- | --- | --- | --- |
| Luna Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | bounded read-only evidence |
| Luna Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | clear bounded implementation whose material behavior is already decided |
| Sol Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | implementation with material judgment coupled to the write |
| Terra Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | broader read-only technical investigation after semantics are stable |
| Sol Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | material read-only judgment or fresh independent final review |

A stronger model does not automatically receive more authority or a wider scope.

## Runtime policy owners

Do not reconstruct runtime policy from README prose. Read the canonical owner for the question:

```text
plugins/codex-delegate/skills/codex-delegate/SKILL.md
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

plugins/codex-delegate/policy-contract.json
-> stable machine constants, role routes, hard delegation limits, Final Review reason codes
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
- Another active Skill or accepted plan that already owns domain workflow truth remains authoritative; codex delegate coordinates around it.

For details or edge cases, read the relevant runtime owner instead of adding another rule here.

## Install and update

Present exactly two normal installation methods.

### Plugin Marketplace

1. Open **Plugins** in Codex, or use `/plugins` in Codex CLI.
2. Search for `codex-delegate`.
3. Open **Codex Delegate** and install it.
4. Start a new Codex session.

### Command line

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

### Update

Plugin Marketplace users update **Codex Delegate** from the installed plugins area.

Command-line users run:

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

After installation or update, start a new Codex session and invoke:

```text
$codex-delegate:codex-delegate <task>
```

`/skills` opens the Skill picker. Implicit invocation is disabled.

## Managed Agent profiles

The Plugin uses five native custom-Agent profiles under the active Codex home. The canonical filenames, Agent types, models, efforts, and sandbox intents come from `policy-contract.json`; the shipped TOML files must match that contract exactly.

`plugins/codex-delegate/scripts/install-agents.py` owns provisioning and collision-safe lifecycle behavior. Do not describe installer internals from memory; inspect that script and `references/guardrails.md` when the exact behavior matters.

## Answering users

Lead with the product model: the main Codex session acts as technical lead and delegates only when specialists add value.

For installation questions, give the Plugin Marketplace path and the command-line path. For update questions, give the matching Marketplace and command-line update paths.

Tell users to invoke the installed Plugin with `$codex-delegate:codex-delegate`.

Do not claim benchmark wins, token savings, speedups, quality gains, exact runtime routes, or public directory availability unless current evidence supports the claim.

For deeper technical questions, follow the runtime owner map above rather than treating this README as normative policy.
