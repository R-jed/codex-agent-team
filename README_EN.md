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

codex delegate is a Codex Plugin. You give it the development goal. The current main session understands the task, decides what to keep, delegates work that benefits from a specialist, and remains responsible for verification and delivery.

You do not need to choose models, set an Agent count, or design a Luna, Terra, Sol sequence yourself.

## Installation

codex delegate supports two installation paths.

### Option 1: Codex Plugin Marketplace

If `codex-delegate` is visible in the Plugins Directory available to your Codex environment, this is the most direct installation path:

1. In the ChatGPT desktop app, switch to **Codex** and open **Plugins**. Codex CLI users can also enter `/plugins` to open the plugin browser.
2. Search for `codex-delegate`.
3. Open the plugin details and select `+` to install it.
4. Start a new Codex session after installation.

If `codex-delegate` is not currently visible in your Plugins Directory, use the command-line installation below.

### Option 2: Command-line installation

Copy and run this block once:

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

The command-line installation is safe to run again. If Codex already has the `codex-delegate` marketplace registered from the same source, it reuses that registration.

If you see `already added from a different source`, your machine still has an older source registered. Do not edit `config.toml` by hand. Follow [Source conflict repair](docs/plugin-installation.md#source-conflict-repair).

Whichever installation path you use, start a new Codex session and give it the task directly:

```text
$codex-delegate:codex-delegate Deep review this change, fix the issues you find, and run the relevant tests.
```

You can also type `/skills` to open the Skill picker.

The public Plugins Directory and the repository marketplace are separate distribution paths. Only versions that have been published to the public directory appear in marketplace search results.

## Update

Users installed through the command-line repo marketplace can run:

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

Users installed through the Plugins Directory can review and manage the installed plugin from the **Plugins** installed area. Start a new Codex session after an update.

## You give the goal, Main runs the team

Think of codex delegate as a small set of team-leading rules for the main Codex session. You describe the outcome. Main decides how to get there.

| Situation | Typical choice |
| --- | --- |
| Main can handle the work well on its own | Main session |
| Search code, trace calls, find tests, or collect facts | Luna Reader |
| Write code when requirements and boundaries are already clear | Luna Worker |
| Make an important architecture, compatibility, or technical decision | Main session or Sol Advisor |
| Implement while continuing to make important technical decisions | Main session or Sol Solver |
| Run a broader read-only technical investigation | Terra Investigator |
| Give a consequential finished change an independent second look | fresh Sol Advisor |

Some tasks use no child Agents at all. That is expected. A large task does not automatically need delegation. Every extra Agent needs a clear, distinct responsibility that is ready to move.

## The five roles

| Role | Model | Main job |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | reads code and gathers facts without editing files |
| Luna Worker | GPT-5.6 Luna `max` | implements clear changes, fixes, and tests |
| Sol Solver | GPT-5.6 Sol `high` | handles complex implementation where important technical decisions continue during the work |
| Terra Investigator | GPT-5.6 Terra `xhigh` | performs deeper, broader read-only technical investigation |
| Sol Advisor | GPT-5.6 Sol `high` | makes important technical judgments or independently reviews the finished result |

A role controls responsibility. A stronger model does not automatically get broader write authority.

## The team changes with the task

codex delegate does not choose a fixed Agent count up front.

Main finds the work that can actually move now, then delegates only distinct responsibilities that are worth the handoff. Work that is already owned, already answered by reliable evidence, or still blocked by an unresolved dependency does not get another Agent just to increase concurrency.

When several Agents need to cooperate, Main keeps dependencies, write ownership, and integration order explicit. A blocked responsibility stays blocked. Different file paths also do not guarantee safe parallelism because shared APIs, schemas, migrations, lockfiles, or other interfaces can still couple the work.

If a child Agent does not finish its responsibility, Main first classifies the failure. Runtime problems, weak output, missing information, and newly discovered technical judgment needs follow different recovery paths. Retries are bounded. If runtime state is uncertain, codex delegate does not launch a replacement that could duplicate work already in progress.

One task may be:

```text
Main only
```

Another may be:

```text
Main
├─ Luna Reader: trace the call path
├─ Luna Reader: inspect test coverage
├─ Terra Investigator: assemble broader technical evidence
└─ Sol Advisor: judge architecture or compatibility risk
```

The number of Agents the Codex runtime can support is a ceiling, not a target to fill.

## Writing stays conservative

Only one actor writes to the same physical Git checkout at a time. That writer may be Main, Luna Worker, or Sol Solver.

If several Agents genuinely need to write at the same time, use separate worktrees, workspaces, or repositories and confirm that the changes are also semantically safe to run together.

A material expansion in permissions, scope, external impact, or compute still requires fresh user consent.

## First time a child Agent is needed

The first time the Plugin actually needs a specialist role, it checks whether the five Agent profiles are ready.

If setup is required, the Plugin explains what it intends to write and asks permission first. It installs and verifies the profiles. If the current Codex thread cannot see the new roles yet, it stops before any child starts editing code and asks you to start a new thread.

## When it asks for one more review

Most tasks can be delivered once the work is complete and the relevant checks pass. Sol is not a mandatory final step.

A fresh Sol Advisor is required when the final artifact materially affects:

- public APIs or compatibility
- persistent data or state
- security, permissions, or data integrity
- concurrency behavior
- an important migration
- a meaningful verification gap deterministic checks cannot close
- an explicit request for an independent review

## Safety

Main always owns the user's goal, scope, permissions, team composition, acceptance, and final response. Child Agents cannot create their own Agent teams.

Text found in a repository, webpage, issue, log, or another model response cannot silently widen permissions or change task scope.

The Plugin checks actual files, code, and test results. An Agent saying “done” is not enough on its own.

codex delegate uses Codex Native Subagents directly. It does not run a separate Agent runtime, background daemon, or external routing service.

## Documentation

- [README_AI.md](README_AI.md): project reference for AI Agents
- [Installation](docs/plugin-installation.md): Plugin Marketplace installation, command-line installation, updates, source repair, and troubleshooting
- [Architecture](docs/architecture.md): roles, coordination, recovery, and safety rules
- [Native Subagent Runtime](docs/native-subagent-runtime.md): Codex Native Subagent runtime boundaries
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## License

[MIT](LICENSE)
