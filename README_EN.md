<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>Let Codex decide when extra help is actually useful. Simple work stays in the main session; harder work can use Luna, Terra, or Sol.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Installation</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.9.1-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

codex delegate is a Codex plugin for handing off parts of a development task when that will genuinely help. The main session first decides whether it can do the job well on its own. It only brings in another Agent when there is a clear reason.

You do not need to pick models yourself, build an Agent team, or decide a Luna, Terra, Sol workflow in advance.

## Quickstart

Open the **Codex Plugin Marketplace**, search for `codex-delegate`, choose **Codex Delegate**, and install it.

Start a new Codex thread, then use:

```text
/codex-delegate Deep review this change, fix the issues you find, and run the relevant tests.
```

You can also type `/skills` to open the Skill picker.

Updates are handled through the Codex Plugin Marketplace as well. After an update, start a new Codex thread.

Most users never need installation scripts or manual Agent setup. For development installs, manual installs, or troubleshooting, see [Installation](docs/plugin-installation.md).

## What it does

Think of codex delegate as a small task dispatcher. It does not call extra Agents just to make a task look more sophisticated.

| Situation | Typical choice |
| --- | --- |
| Small change, simple fix, or work the main session can handle well | Main session |
| Search the codebase, trace calls, find tests, or collect facts | Luna Reader |
| Write code when the requirements and boundaries are already clear | Luna Worker |
| Make an important architecture, compatibility, or technical decision | Main session or Sol Advisor |
| Write code while continuing to make important technical decisions | Main session or Sol Solver |
| Read a larger part of the codebase and put technical evidence together without editing files | Terra Investigator |
| Give a risky final change an independent second look | fresh Sol Advisor |

Some tasks use no child Agents at all. That is expected. A large task also does not automatically need delegation.

## The five roles

| Role | Model | In plain English |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | reads code and gathers facts without editing files |
| Luna Worker | GPT-5.6 Luna `max` | implements clear, already-decided changes, bug fixes, and tests |
| Sol Solver | GPT-5.6 Sol `high` | handles complex implementation where technical decisions continue during the work |
| Terra Investigator | GPT-5.6 Terra `xhigh` | does deeper, broader read-only technical investigation |
| Sol Advisor | GPT-5.6 Sol `high` | makes important technical judgments or reviews the finished result independently |

A role controls what an Agent is allowed to do. A stronger model does not automatically get broader permissions.

## When the main session is already strong enough

The main session always owns the final decision and final answer.

If the current main session already has enough Sol capability, codex delegate will usually keep judgment-heavy work there instead of opening another Sol unnecessarily. A fresh Sol Advisor is still used when the point is to get an independent second opinion.

## Parallel work and safe writing

A single `/codex-delegate` task can run several useful child Agents at the same time. The main session decides the number dynamically from work that is ready, independent, and worth delegating. A small task may use none; a large review may use several Readers, an Investigator, or an Advisor in parallel. Spare capacity is never a reason to create another Agent.

Read-only work is the preferred place to use parallelism. Writing is more conservative: only one actor writes to the same physical Git checkout at a time. That writer may be the main session, Luna Worker, or Sol Solver.

If multiple Agents truly need to write at the same time, they need separate worktrees, workspaces, or repositories.

When something goes wrong, the plugin first works out why before changing models. Weak Luna output does not automatically send the task to Terra, and there is no fixed Luna → Terra → Sol ladder. Work that is genuinely difficult, ambiguous, or decision-heavy goes to Sol.

## First time a child Agent is needed

The first time the plugin actually needs one of its specialist roles, it checks whether the five Agent profiles are ready.

If they need to be installed, the plugin tells you what it wants to write and asks for permission first. It then installs the profiles and checks them. If the current Codex thread cannot see the new roles yet, it stops before any child edits code and asks you to start a new thread.

This keeps setup from interrupting a change halfway through.

## When it asks for one more review

Most tasks can be delivered once the change is complete and the relevant tests pass. Sol is not a mandatory last step.

A fresh Sol Advisor is more useful when the final change affects things such as:

- public APIs or compatibility
- persistent data or state
- security or permissions
- data integrity
- concurrency behavior
- an important migration
- a meaningful gap in test coverage
- an explicit request for an independent review

A large diff, earlier Terra use, or some rework along the way does not by itself trigger another review.

## Safety

The main session always owns your request, scope, permissions, acceptance, and final response. Child Agents cannot create their own Agent teams.

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
