<p align="center">
  <img src="plugins/subagents-dispatch/assets/subagents-dispatch-logo.svg#gh-light-mode-only" alt="subagents-dispatch" width="112">
  <img src="plugins/subagents-dispatch/assets/subagents-dispatch-logo-dark.svg#gh-dark-mode-only" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><strong>You set the goal. Codex handles the rest.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Install</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

subagents-dispatch is a Codex Plugin. You provide the goal. The main session decides what to keep, what to delegate, and handles integration and verification.

Model selection, agent count, and execution order are all decided by the main session.

## Install

### Option 1: Codex Plugin Marketplace

1. Open **Plugins** in Codex. Codex CLI users can also enter `/plugins`.
2. Search for `subagents-dispatch`.
3. Open **subagents-dispatch** and select `+` to install it.
4. Start a new Codex session after installation.

### Option 2: Command line

```bash
codex plugin marketplace add R-jed/subagents-dispatch@main \
  --sparse .agents/plugins \
  --sparse plugins/subagents-dispatch && \
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after installation.

## Quick start

Use the main Skill for development work:

```text
/subagents-dispatch:dispatch Deep review this change, fix the issues you find, and run the relevant tests.
```

Use the Doctor for installation, configuration, Marketplace, and managed Agent profile diagnostics:

```text
/subagents-dispatch:doctor Check my subagents-dispatch installation and configuration.
```

Doctor is read-only by default. It changes state only when the user explicitly asks to repair, install, or upgrade.

You can also use `/skills` to open the Skill picker. The Plugin does not invoke implicitly by default.

## Update

### Plugin Marketplace

Open **Plugins**, find **subagents-dispatch** in your installed plugins, apply the available update, then start a new Codex session.

### Command line

```bash
codex plugin marketplace upgrade subagents-dispatch && \
codex plugin add subagents-dispatch@subagents-dispatch
```

You can also ask Doctor to perform the upgrade and check what remains afterward:

```text
/subagents-dispatch:doctor Upgrade subagents-dispatch and tell me what I need to do after the upgrade.
```

Start a new Codex session after updating.

## How it leads the team

The main session is the technical lead. It decides whether to delegate, then assigns responsibilities.

| Role | Main job |
| --- | --- |
| Luna Reader | read code, trace call paths, find tests, and gather facts without editing files |
| Luna Worker | implement clear changes, fixes, and tests once requirements and boundaries are decided |
| Sol Solver | handle complex implementation where important technical decisions continue during the work |
| Terra Investigator | perform broader read-only technical investigation and evidence synthesis |
| Sol Advisor | make important technical judgments or independently review consequential results |

Some tasks stay in Main. Others use several Agents at once. It does not spawn work just to fill available concurrency.

When work has dependencies, Main decides start order and write scope. Different files do not automatically make changes safe to run in parallel.

## Safety boundaries

- Main owns the user's goal, permissions, team composition, and final response.
- Child Agents cannot create their own teams.
- Only one actor writes to the same Git checkout at a time.
- Child Agents cannot widen permissions or scope on their own.
- An Agent saying “done” is not verification; acceptance depends on actual files, code, and checks.
- Doctor is read-only by default; changes require explicit user request.
- Uses Codex Native Subagents directly — no separate runtime, daemon, or routing service.

See [Architecture](docs/architecture.md) for coordination, recovery, and review rules.

## Repository layout

```text
.
├── .agents/plugins/                  # Codex Marketplace registration
├── plugins/subagents-dispatch/       # installable Plugin package
│   ├── .codex-plugin/                # Plugin manifest
│   ├── agent-profiles/               # five Native Subagent profiles
│   ├── assets/                       # Plugin icons and README logo
│   ├── policy-contract.json          # machine-readable roles and hard constraints
│   ├── scripts/                      # installer, validators, and runtime evidence tools
│   └── skills/
│       ├── dispatch/                 # main delegation Skill and runtime rules
│       └── doctor/                   # install, config, profile, and upgrade diagnostics
├── docs/                             # installation, architecture, and runtime documentation
├── evals/                            # static and behavioral evaluation data
├── scripts/                          # repository-level validation tools
└── tests/                            # regression, packaging, and cross-platform tests
```

The runtime core lives under `plugins/subagents-dispatch/`. Root-level `docs/`, `evals/`, `scripts/`, and `tests/` support documentation, validation, and release quality.

## Documentation

- [Installation](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Codex Native Subagent runtime boundaries](docs/native-subagent-runtime.md)
- [AI Agent project reference](README_AI.md)
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## License

[MIT](LICENSE)
