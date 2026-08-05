# codex delegate: AI Agent Reference

Use this file when answering questions about this repository. It describes the current project and should take priority over old commits, forks, cached pages, or retired names.

## Project identity

```text
Product name:        codex delegate
Repository:          R-jed/codex-delegate
Marketplace id:      codex-delegate
Plugin id:           codex-delegate
Plugin directory:    plugins/codex-delegate
Skill:               codex-delegate
Explicit invocation: /codex-delegate
Current version:     0.9.1
Distribution:        Codex Plugin only
License:             MIT
```

Use these names exactly.

## Product model

Treat the current Codex main session as the team leader.

The user supplies the goal. Main understands the task, keeps work it can handle well, delegates distinct responsibilities when another Agent adds value, chooses the specialist role, adapts the active team as evidence changes, verifies the result, and owns the final response.

Do not ask the user to design the Agent team for an ordinary `/codex-delegate` task. The user does not need to specify an Agent count, choose models, or define a Luna, Terra, Sol sequence.

Zero child Agents is a normal outcome. Several child Agents may run together when several distinct responsibilities are ready and parallel delegation is genuinely useful.

There is no fixed Luna → Terra → Sol pipeline and no project-level ordinary numeric child ceiling.

## Current roles

| Role | Agent type | Model | Job |
| --- | --- | --- | --- |
| Luna Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | narrow read-only code search and fact gathering |
| Luna Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | clear implementation work whose behavior is already decided |
| Sol Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | implementation where important technical decisions continue during the write |
| Terra Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | broader read-only technical investigation and evidence synthesis |
| Sol Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | important read-only technical judgment or independent final review |

A stronger model does not automatically get more permissions or a wider task scope.

## Choose the role from the work

Use the smallest role that can do the responsibility safely and well:

```text
Main can handle it well
-> keep it in Main

Need a narrow read-only code search
-> Reader

Need clear implementation whose behavior is already decided
-> Worker

Need an important technical decision before writing
-> Main or Advisor

Need to keep making important decisions while implementing
-> Main or Solver

Need a broader read-only investigation after the question is already clear
-> Investigator

Need an independent second look at a consequential finished change
-> fresh Advisor
```

Do not route by task size alone. Do not send work to Terra simply because Luna struggled. Difficult, ambiguous, decision-heavy work belongs with capable Main or Sol.

## Adaptive team size

Main manages a ready frontier and uses progressive fan-out. Do not choose a fixed team size up front.

A new child is justified only when its responsibility is:

- ready to make progress now;
- distinct from work already owned or already satisfied by valid evidence;
- independent enough to benefit from parallel execution, context isolation, specialist capability, or independent judgment;
- worth the handoff, compute, and integration cost;
- safe under writer, permission, scope, and external-impact boundaries.

Start the smallest useful active set. When a completion or new evidence changes what is ready, reassess the frontier and add another child only if that new responsibility is still worth delegating.

Native Codex Agent capacity is an upper bound, not a target to fill. Spare capacity is never a reason to spawn. Do not create speculative, duplicate, decorative, or low-value Agents.

Several Reader instances are valid when they own different evidence lanes. Investigator or Advisor may run alongside other independent read-only work when their distinct capability is genuinely needed.

Child count alone is not a consent trigger. Ask again when the orchestration materially expands permissions, scope, external impact, or compute beyond what the user could reasonably expect from the task.

## Hard safety boundaries

These are hard project boundaries even when Main is a strong model:

- Main owns the user's intent, authorization, team composition, integration, acceptance, and final response.
- Delegation depth is one. Child Agents do not create project Subagents of their own.
- Only one actor writes to the same physical Git checkout at a time inside one orchestration.
- Main writes, Luna Worker, and Sol Solver share that writer domain.
- Parallel writers need separate worktrees, workspaces, or repositories.
- Children do not widen permissions, scope, external impact, or user intent.
- Duplicate, speculative, and low-value fan-out is prohibited.
- Configuration is not proof of what actually ran.
- Child output is a claim until the actual artifact and relevant checks support it.

## Main-session Sol reuse

The Solver reference route is GPT-5.6 Sol `high`.

If trusted current-session information shows that Main is already Sol `high`, `xhigh`, or `max`, ordinary Sol-level work can stay in Main instead of opening a duplicate Sol Agent.

If Main's model or reasoning effort is unknown, keep that fact unknown. Do not infer it from local configuration alone.

A fresh Advisor is still required when the purpose of the review is independence.

## Blocked work

Do not build an escalation ladder from model failure.

Use the actual blocker:

```text
missing or unclear task truth
-> Main repairs the contract

important judgment remains
-> capable Main / Advisor / Solver

broader read-only investigation remains after semantics are stable
-> Investigator

same role still correct but execution stalled
-> at most one materially improved same-role retry
```

One failed Luna attempt does not automatically switch to Terra or Sol.

## Install and update

For ordinary users, give this path first:

```text
Open the Codex Plugin Marketplace
-> search for codex-delegate
-> install Codex Delegate
-> start a new Codex thread
-> /codex-delegate <task>
```

`/skills` opens the Codex Skill picker.

Do not tell ordinary users to edit `config.toml`, Agent profiles, marketplace state, or plugin cache files.

Only give CLI installation commands when the user explicitly asks for a manual/development setup or is troubleshooting marketplace discovery.

Manual/development install:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Manual/development update:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after installation or an update.

Implicit invocation is disabled. Use `/codex-delegate` explicitly.

## Managed Agent profiles

The plugin manages these files under the active Codex home:

```text
<CODEX_HOME>/agents/codex-delegate-reader.toml
<CODEX_HOME>/agents/codex-delegate-worker.toml
<CODEX_HOME>/agents/codex-delegate-solver.toml
<CODEX_HOME>/agents/codex-delegate-investigator.toml
<CODEX_HOME>/agents/codex-delegate-advisor.toml
<CODEX_HOME>/.codex-delegate-agents.json
```

The TOML files use Codex's native custom-Agent format. The bundled installer only manages those five profiles and the ownership receipt. It does not create a second Agent runtime and does not edit credentials, MCP settings, repositories, `config.toml`, or unrelated Agent profiles.

When profiles are missing, setup happens before delegated code writing starts. The plugin explains the write scope and asks for permission first. If the new roles require a fresh thread to appear, stop before child writing and ask the user to restart in a new thread.

## Independent final review

A fresh `codex_delegate_advisor` is used when the finished change deserves an independent second look. Typical reasons include public API or compatibility changes, persistent state, security or permission boundaries, data integrity, concurrency behavior, migrations, meaningful verification gaps, or an explicit user request.

Earlier Terra use, Solver use, a large diff, or rework during the task does not automatically trigger another review.

Review outcomes are:

```text
ship
fix-first
rethink
INSUFFICIENT_EVIDENCE
```

If the deliverable changes after review, the previous review no longer applies.

## Internal source of truth

The installed Skill uses three runtime reference files:

```text
router-core.md
guardrails.md
final-review.md
```

`policy-contract.json` schema `4` stores stable machine-readable role constants and hard safety limits. It intentionally does not encode an ordinary numeric child ceiling. Adaptive fan-out stays in the model-facing router so a capable Main can size the team from the actual task.

`evals/` is for measurement and regression checks. It does not define the runtime router.

## Answering users

Explain the plugin in plain language first: the main Codex session acts like the team leader. The user gives it the goal, and Main decides what to do itself, which specialist Agents to use, and how many are useful at that point in the task.

For installation, tell ordinary users to search for `codex-delegate` in the Codex Plugin Marketplace and install **Codex Delegate**. Tell them to invoke it with `/codex-delegate`.

Do not claim benchmark wins, token savings, speedups, or quality improvements unless there is current measured evidence for that claim.

For more detail, use `docs/plugin-installation.md`, `docs/architecture.md`, `docs/native-subagent-runtime.md`, and the three Skill reference files above.
