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

The current Codex main session is the team leader. The user supplies the goal. Main owns authorization, team composition, integration, acceptance, and the final response. Zero child Agents is normal. Delegation is adaptive and only used when a distinct responsibility benefits from isolation, parallelism, or specialist capability.

Version 2.1 adds explicit preview and live-control intents to the same `/dispatch` entrypoint. Their exact grammar and behavior are owned by `skills/dispatch/references/interaction.md`.

`doctor` is operational maintenance. It diagnoses installation, configuration, Marketplace, and managed-profile state and may repair or upgrade only when the user explicitly asks. It does not own development routing or runtime delegation policy.

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
-> host/plugin/Marketplace/profile diagnosis and supported repair or upgrade flows

scripts/install-agents.py
-> deterministic managed-profile install/check lifecycle

docs/plugin-installation.md
-> user-facing install, first-run provisioning, update, and uninstall procedure
```

`evals/` is a regression and measurement surface. It does not define runtime policy.

## Reading order by task

- Routing or role choice: `skills/dispatch/SKILL.md`, then `references/router-core.md` and `policy-contract.json`.
- Preview, status, steer, takeover, or receipts: `references/interaction.md`.
- Cross-responsibility context reuse: `references/handoff-capsule.md`.
- Multi-unit dependencies or ownership: `references/team-plan.md`.
- Failure, `UNKNOWN`, retry, or takeover recovery: `references/recovery.md`.
- Permissions, writer safety, provisioning, consent, or runtime trust: `references/guardrails.md`.
- Independent final review: `references/final-review.md`.
- Installation, update, or removal: `docs/plugin-installation.md` and `skills/doctor/SKILL.md`.

Do not duplicate an owner contract into this file. If a rule changes, update the owner and keep this index pointing to it.
