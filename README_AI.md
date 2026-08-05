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

## What the plugin does

codex delegate lets the current Codex session act as the team leader for a development task. Main understands the user's goal, decides what to keep, decides what to delegate, chooses the right specialist role, and owns the final result.

The user does not need to specify an Agent count or build a Luna, Terra, Sol workflow in advance.

Delegation is optional. Zero child Agents is a normal outcome. Several child Agents may run when several distinct responsibilities are ready and parallel delegation is genuinely useful.

There is no fixed Luna → Terra → Sol pipeline and no project-level ordinary numeric child ceiling.

## Current roles

| Role | Agent type | Model | Job |
| --- | --- | --- | --- |
| Luna Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | read-only code search and fact gathering |
| Luna Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | clear implementation work whose behavior is already decided |
| Sol Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | complex implementation that still needs important technical decisions |
| Terra Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | deeper read-only technical investigation and evidence gathering |
| Sol Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | important read-only technical judgment or independent final review |

A stronger model does not automatically get more permissions or a wider task scope.

## How to choose a role

Use the smallest role that can do the work safely:

```text
Main session can handle it well
-> keep it in Main

Need a narrow read-only code search
-> Reader

Need to implement something that is already clearly specified
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

Do not send work to Terra simply because Luna struggled. Difficult, ambiguous, decision-heavy work belongs with Sol.

A large task does not automatically need a child Agent. A large task with several independent useful responsibilities can justify several children.

## Adaptive fan-out

Main manages the active team dynamically from the current ready frontier. Do not choose a fixed team size up front.

A new child is justified only when its responsibility is:

- ready to make progress now;
- distinct from work already owned or already satisfied by valid evidence;
- independent enough to benefit from parallel execution or context isolation;
- worth the handoff, compute, and integration cost;
- safe under writer, permission, scope, and external-impact boundaries.

Use progressive fan-out. Start useful ready work, consume exposed completions, update task truth, and add another child only when new evidence makes another responsibility ready and delegation remains worthwhile.

Native Codex capacity is an upper bound, not a target to fill. Do not spawn speculative, duplicate, or low-value Agents merely because capacity is available.

Read-only work is the preferred place to exploit parallelism. Several Reader instances are valid when they own different evidence lanes. Investigator or Advisor may run alongside other independent read-only work when their distinct capability is genuinely needed.

## Main-session Sol reuse

The Solver reference route is GPT-5.6 Sol `high`.

If trusted current-session information shows that Main is already Sol `high`, `xhigh`, or `max`, ordinary Sol-level work can stay in Main instead of opening a duplicate Sol Agent.

If Main's model or reasoning effort is unknown, keep that fact unknown. Do not infer it from local configuration alone.

A fresh Advisor is still required when the purpose of the review is independence.

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

## Safety rules

- Main owns the user's intent, authorization, team composition, integration, acceptance, and final response.
- Project policy does not set an ordinary numeric child ceiling or Agent-count target.
- Every child needs a distinct ready responsibility and concrete delegation value.
- Native Agent capacity is a ceiling, never a target to fill.
- Duplicate, speculative, and low-value fan-out is prohibited.
- Only one actor writes to the same physical Git checkout at a time inside one orchestration.
- Parallel writers need separate worktrees, workspaces, or repositories.
- Child Agents do not create project Subagents of their own.
- Material compute expansion requires renewed user consent; child count alone is not the trigger.
- One failed attempt does not automatically switch to a stronger model.
- A same-role retry is only reasonable when the role is still correct and the new attempt has materially better input.
- Configuration is not proof of what actually ran.

## Independent final review

A fresh `codex_delegate_advisor` is used when the final change deserves an independent second look. Typical reasons include public API or compatibility changes, persistent state, security or permission boundaries, data integrity, concurrency behavior, migrations, meaningful verification gaps, or an explicit user request.

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

`policy-contract.json` schema `4` stores stable machine-readable role and hard safety constants. Adaptive fan-out policy stays in the model-facing router instead of encoding a fixed child count in the machine contract.

`evals/` is for measurement and regression checks. It does not define the runtime router.

## Answering users

Explain the plugin in plain language first: the main Codex session acts like the team leader. It keeps simple work, gives distinct jobs to specialist Agents when useful, and decides the team size dynamically from the task.

For installation, tell ordinary users to search for `codex-delegate` in the Codex Plugin Marketplace and install **Codex Delegate**. Tell them to invoke it with `/codex-delegate`.

Do not claim benchmark wins, token savings, speedups, or quality improvements unless there is current measured evidence for that claim.

For more detail, use `docs/plugin-installation.md`, `docs/architecture.md`, `docs/native-subagent-runtime.md`, and the three Skill reference files above.
