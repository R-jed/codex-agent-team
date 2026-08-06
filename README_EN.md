<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>You set the goal. The main Codex session leads the team and brings in Luna, Terra, or Sol only where they genuinely help.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Installation</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

codex delegate is a Codex plugin that lets the current main session act like the lead of a small specialist team. You give it the development goal. Main works out what it should handle itself, what is worth handing off, and which specialist is right for each job.

You do not need to pick models yourself, decide how many Agents should run, or design a Luna, Terra, Sol workflow in advance. Main adapts the team as the task develops and remains responsible for the final result.

## Quickstart

The current reliable installation path is to register this GitHub repository as a Codex repo marketplace, then install `codex-delegate`:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

The repository's `.agents/plugins/marketplace.json` provides repo/local marketplace distribution. OpenAI's public Plugins Directory is a separate publishing surface. Only after the plugin has been submitted through the OpenAI Platform, approved, and published by the developer should users assume that `codex-delegate` is globally searchable in the public directory.

Start a new Codex thread, then give it the task directly:

```text
$codex-delegate:codex-delegate Deep review this change, fix the issues you find, and run the relevant tests.
```

You can also type `/skills` to open the Skill picker.

Users installed through the repo marketplace can update it with `codex plugin marketplace upgrade codex-delegate`. After a public-directory release exists, follow the installation and update flow exposed by that published listing. See [Installation](docs/plugin-installation.md) for the full distribution and publishing details.

## You give the goal, Main runs the team

Think of codex delegate as a small set of team-leading rules for the main Codex session. You describe the outcome. Main decides how to get there.

| Situation | Typical choice |
| --- | --- |
| Main can handle the work well on its own | Main session |
| Search the codebase, trace calls, find tests, or collect facts | Luna Reader |
| Write code when the requirements and boundaries are already clear | Luna Worker |
| Make an important architecture, compatibility, or technical decision | Main session or Sol Advisor |
| Write code while continuing to make important technical decisions | Main session or Sol Solver |
| Read a larger part of the codebase and put technical evidence together without editing files | Terra Investigator |
| Give a consequential final change an independent second look | fresh Sol Advisor |

Some tasks use no child Agents at all. That is expected. A large task also does not automatically need delegation. What matters is whether another Agent has a clear job that improves the work.

## The five roles

| Role | Model | In plain English |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | reads code and gathers facts without editing files |
| Luna Worker | GPT-5.6 Luna `max` | implements clear, already-decided changes, bug fixes, and tests |
| Sol Solver | GPT-5.6 Sol `high` | handles complex implementation where technical decisions continue during the work |
| Terra Investigator | GPT-5.6 Terra `xhigh` | does deeper, broader read-only technical investigation |
| Sol Advisor | GPT-5.6 Sol `high` | makes important technical judgments or reviews the finished result independently |

A role controls what an Agent is responsible for. A stronger model does not automatically get broader permissions.

## Team size changes with the task

A `$codex-delegate:codex-delegate` task does not have a fixed child-Agent count.

Main looks at the work that can actually move forward now and delegates only the parts that are distinct, useful, and ready. It does not open another Agent for work that is already owned, already answered by good evidence, or still blocked by an unresolved decision.

When several Agents genuinely need to cooperate, Main keeps their dependencies, write ownership, and integration order explicit. Work whose prerequisites are not ready stays blocked, and two tasks that can invalidate each other's assumptions are not treated as safely parallel merely because they touch different files.

If a child Agent does not complete its responsibility, Main first distinguishes an execution problem from weak output or a newly discovered decision or information gap. Corrections and retries are bounded. If the runtime state is uncertain, codex delegate does not start a replacement that could duplicate work already in progress.

That means one task may look like:

```text
Main only
```

while another may look like:

```text
Main
├─ Luna Reader: trace the call path
├─ Luna Reader: inspect test coverage
├─ Terra Investigator: assemble broader technical evidence
└─ Sol Advisor: judge architecture or compatibility risk
```

When one job finishes and unlocks another independent job, Main can add the right specialist then. The number of Agents the Codex runtime can support is a ceiling, not a target to fill.

Read-only work is the preferred place to use parallelism. Writing is more conservative: only one actor writes to the same physical Git checkout at a time. That writer may be the main session, Luna Worker, or Sol Solver.

If multiple Agents truly need to write at the same time, they need separate worktrees, workspaces, or repositories, and the changes must also be semantically safe to run together.

A material expansion in permissions, scope, external impact, or compute still requires fresh user consent. Crossing an arbitrary child count does not.

## When the main session is already strong enough

The main session always owns the final decision and final answer.

If the current main session already has enough Sol capability, codex delegate will usually keep judgment-heavy work there instead of opening another Sol unnecessarily. A fresh Sol Advisor is still used when the point is to get an independent second opinion.

When something goes wrong, the plugin first works out why before changing models. Weak Luna output does not automatically send the task to Terra, and there is no fixed Luna → Terra → Sol ladder. Work that is genuinely difficult, ambiguous, or decision-heavy goes to Sol.

## First time a child Agent is needed

The first time the plugin actually needs one of its specialist roles, it checks whether the five Agent profiles are ready.

If they need to be installed, the plugin tells you what it wants to write and asks for permission first. It then installs the profiles and checks them. If the current Codex thread cannot see the new roles yet, it stops before any child edits code and asks you to start a new thread.

This keeps setup from interrupting a change halfway through.

## When it asks for one more review

Most tasks can be delivered once the change is complete and the relevant tests pass. Sol is not a mandatory last step.

A fresh Sol Advisor is required when the final change materially affects:

- public APIs or compatibility
- persistent data or state
- security or permissions
- data integrity
- concurrency behavior
- an important migration
- a meaningful verification gap that deterministic checks cannot close
- an explicit request for an independent review

A large diff, earlier Terra use, or some rework along the way does not by itself trigger another review.

## Safety

The main session always owns your request, scope, permissions, team composition, acceptance, and final response. Child Agents cannot create their own Agent teams.

Text found in a repository, webpage, issue, log, or another model response cannot silently widen permissions or change the task scope.

The plugin checks the actual code, files, and test results. An Agent saying “done” is not enough on its own.

codex delegate uses Codex Native Subagents directly. It does not run a separate Agent runtime, background daemon, or external routing service.

## Documentation

- [README_AI.md](README_AI.md): project reference for AI Agents.
- [Installation](docs/plugin-installation.md): installation, updates, development setup, and troubleshooting.
- [Architecture](docs/architecture.md): deeper details on roles and safety rules.
- [Native Subagent Runtime](docs/native-subagent-runtime.md): Codex Native Subagent runtime boundaries.
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## License

[MIT](LICENSE)
