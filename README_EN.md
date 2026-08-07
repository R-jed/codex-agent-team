<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>You set the goal. The main Codex session leads the team and brings in Luna, Terra, or Sol only when they genuinely help.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Install</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.2.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

codex delegate is a Codex Plugin. You provide the development goal. The current main session decides what to keep, what is worth handing to a specialist Agent, and remains responsible for integration, verification, and delivery.

You do not need to choose models, set an Agent count, or design a Luna, Terra, Sol sequence yourself.

## Install

### Option 1: Codex Plugin Marketplace

1. Open **Plugins** in Codex. Codex CLI users can also enter `/plugins`.
2. Search for `codex-delegate`.
3. Open **Codex Delegate** and select `+` to install it.
4. Start a new Codex session after installation.

### Option 2: Command line

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex session after installation.

## Quick start

Give the task directly to the Plugin:

```text
$codex-delegate:codex-delegate Deep review this change, fix the issues you find, and run the relevant tests.
```

You can also use `/skills` to open the Skill picker. The Plugin does not invoke implicitly by default.

## Update

### Plugin Marketplace

Open **Plugins**, find **Codex Delegate** in your installed plugins, apply the available update, then start a new Codex session.

### Command line

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex session after updating.

## How it leads the team

The main session remains the technical lead. It first decides whether delegation is useful, then assigns only clear, distinct responsibilities that are ready to move.

| Role | Main job |
| --- | --- |
| Luna Reader | read code, trace call paths, find tests, and gather facts without editing files |
| Luna Worker | implement clear changes, fixes, and tests once requirements and boundaries are decided |
| Sol Solver | handle complex implementation where important technical decisions continue during the work |
| Terra Investigator | perform broader read-only technical investigation and evidence synthesis |
| Sol Advisor | make important technical judgments or independently review consequential results |

Some tasks stay entirely in Main. Others use several Agents at once. codex delegate does not choose a fixed Agent count and does not spawn work just to fill available concurrency.

When work has dependencies, Main owns start order, write scope, and final integration. Different files do not automatically make two changes safe to run in parallel.

## Safety boundaries

- Main always owns the user's goal, permissions, team composition, acceptance, and final response.
- Child Agents cannot create their own Agent teams.
- Only one actor writes to the same physical Git checkout at a time.
- Child Agents cannot widen permissions, mutation scope, or external impact on their own.
- An Agent saying “done” is not verification; final acceptance depends on actual files, code, and relevant checks.
- codex delegate uses Codex Native Subagents directly and does not run a separate Agent runtime, background daemon, or external routing service.

See [Architecture](docs/architecture.md) for the full coordination, recovery, runtime-evidence, and independent-review rules.

## Documentation

- [Installation](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Codex Native Subagent runtime boundaries](docs/native-subagent-runtime.md)
- [AI Agent project reference](README_AI.md)
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## License

[MIT](LICENSE)
