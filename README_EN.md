<p align="center">
  <img src="assets/subagents-dispatch-logo.svg#gh-light-mode-only" alt="subagents-dispatch" width="112">
  <img src="assets/subagents-dispatch-logo-dark.svg#gh-dark-mode-only" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><strong>You set the goal. Codex leads the team.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Install</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

subagents-dispatch is a Codex Plugin. You provide the goal. The main session decides what to keep, what is worth delegating, and handles integration and verification.

Version 2.1 adds four everyday controls around the existing orchestration kernel: preview before execution, live status/steering/takeover, a compact execution receipt, and evidence-bound handoff context between responsibilities.

## Quick start

Run a task normally:

```text
/dispatch Deep review this change, fix the issues you find, and run the relevant tests.
```

Preview the likely delegation shape without spawning children:

```text
/dispatch preview Deep review this change, fix the issues you find, and run the relevant tests.
```

Preview may perform bounded read-only inspection when needed. It does not spawn Subagents, provision profiles, mutate source, or perform external actions. The result is provisional because real execution may uncover new evidence.

## Control active work

Inspect current delegated responsibilities once:

```text
/dispatch status
```

Give focused guidance to one running responsibility:

```text
/dispatch steer U2: inspect the crash log before re-reading the parser path
```

Safely take a responsibility back into Main:

```text
/dispatch takeover U2
```

Takeover settles the previous owner before Main assumes the responsibility. For writing work, Main stays read-only until the previous writer is confirmed stopped or terminal. If the host cannot establish the old state, it remains `UNKNOWN` and conflicting work is not created.

## Compact execution receipt

When a task actually spawns at least one child, normal completion ends with one factual line such as:

```text
Dispatch: Reader evidence -> Worker implementation · no retry · Final Review not required
```

The receipt reports inspectable orchestration facts. It does not expose hidden reasoning or raw child transcripts. It does not estimate token usage or currency cost from model names or elapsed time. Exact model or usage details require actual host evidence.

Zero-child tasks, Preview, and Status-only requests do not add a receipt.

## Evidence-bound handoffs

When a later responsibility would otherwise repeat material repository discovery, Main can pass a small Handoff Capsule containing already-verified facts, evidence, interfaces, and `DO NOT REDO` guidance.

Children still start with fresh context. subagents-dispatch does not forward an earlier child transcript as inherited truth. A child claim enters the capsule only after Main verifies it. Relevant artifact drift invalidates the affected capsule evidence and requires narrow re-verification.

## Install

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after installation.

Development work uses:

```text
/dispatch <task>
```

Installation, configuration, profile, and upgrade diagnostics use:

```text
/doctor <diagnostic or maintenance request>
```

Doctor is read-only by default. You can also use `/skills` to open the Skill picker. Dispatch keeps implicit invocation disabled.

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
/doctor Upgrade subagents-dispatch and tell me what I need to do after the upgrade.
```

Start a new Codex session after updating.

## How it leads the team

The main session is the technical lead. It selects responsibilities by capability need.

| Role | Main job |
| --- | --- |
| Luna Reader | read code, trace call paths, find tests, and gather facts without editing files |
| Luna Worker | implement clear changes and tests once material behavior and boundaries are decided |
| Sol Solver | handle implementation where important technical judgment continues during the work |
| Terra Investigator | perform broader read-only technical investigation and evidence synthesis |
| Sol Advisor | make important technical judgments or independently review consequential results |

Simple work can remain entirely in Main. Delegation is used when parallelism, isolation, specialist capability, or independent judgment adds enough value to justify the handoff. There is no fixed Agent count and no fixed Luna → Terra → Sol pipeline.

## Safety boundaries

- Main owns the user's goal, permissions, team composition, and final response.
- Child Agents cannot create their own project teams.
- Only one actor writes to the same Git checkout at a time.
- Steering cannot silently widen responsibility, permission, mutation authority, or user scope.
- Takeover must settle the previous owner before conflicting work continues; `UNKNOWN` is preserved.
- Handoff Capsules carry only Main-accepted evidence and cannot grant write authority.
- An Agent saying “done” is a claim until actual artifacts and relevant checks support it.
- Exact model, token, or cost claims require actual runtime evidence.
- Uses Codex Native Subagents directly, with no separate runtime, daemon, or routing service.

See [Architecture](docs/architecture.md) for coordination, recovery, interaction-control, handoff, and review rules.

## Repository layout

```text
.
├── .agents/plugins/                  # Codex Marketplace registration
├── .codex-plugin/                    # Plugin manifest
├── agent-profiles/                   # five Native Subagent profiles
├── assets/                           # Plugin icons and README logo
├── policy-contract.json              # machine-readable roles and hard constraints
├── scripts/                          # installer, validators, and runtime evidence tools
├── skills/
│   ├── dispatch/                     # delegation Skill, interaction controls, and runtime rules
│   └── doctor/                       # install, config, profile, and upgrade diagnostics
├── docs/                             # installation, architecture, and runtime documentation
├── evals/                            # static and behavioral evaluation data
└── tests/                            # regression, packaging, and cross-platform tests
```

## Documentation

- [Installation](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Codex Native Subagent runtime boundaries](docs/native-subagent-runtime.md)
- [AI Agent project reference](README_AI.md)
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## License

[MIT](LICENSE)
