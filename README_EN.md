# Codex Agent Team

<p align="center">
  <img src="assets/readme/hero.svg" alt="Codex Agent Team" width="100%">
</p>

<p align="center">
  <a href="README.md">中文</a> ·
  <a href="docs/architecture.md">Architecture</a> ·
  <a href="docs/native-subagent-runtime.md">Native Runtime</a> ·
  <a href="docs/model-route-assurance.md">Route Assurance</a>
</p>

Code normally. Codex Agent Team adds a specialist Subagent only when it has concrete value.

Small, already-isolated work stays in the current Root. Context-heavy or clearly bounded execution can go to Luna. Terra is added only when a risky change benefits from detached judgment. If a high-consequence disagreement still remains, a non-Sol Root may request one Sol judgment after explicit user consent.

## Recommended install: Codex Plugin

The Plugin is the recommended community distribution path. It installs the workflow Skills while keeping the current session as Root.

First register this repository as a marketplace source with Codex CLI:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Then reopen the ChatGPT desktop app, choose the `Codex Agent Team` marketplace in the Plugins Directory, and install `Codex Agent Team`. This follows the currently documented OpenAI Plugin flow and avoids making a build-specific convenience command the only installation path.

### Install companion custom agents

After the Plugin is installed, complete one explicit Agent setup step. The current Plugin manifest natively declares Skills, MCP, hooks, and interface assets, while Codex custom Agent TOML files are still discovered from `~/.codex/agents/` or project `.codex/agents/`. Codex Agent Team therefore installs them as explicit companion profiles.

Invoke in Codex:

```text
$codex-agent-team-setup
```

The setup Skill runs the bundled fail-closed installer and byte-exactly verifies:

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

Then start a new Codex task so the native `spawn_agent` surface can discover the roles.

## Standalone install

Without the Plugin, the repository installer installs the main Skill and all companion custom agents in one transaction:

```bash
git clone https://github.com/R-jed/codex-agent-team.git
cd codex-agent-team
python scripts/install.py
python scripts/install.py --check
python scripts/doctor.py
```

Skill-only Portable Mode remains available:

```bash
python scripts/install.py --skill-only
```

The standalone installer places profiles under `~/.codex/agents/`, records package-managed hashes, and refuses to overwrite user-modified managed files.

## Daily use

Explicit invocation:

```text
$codex-agent-team
```

You can also describe the development task normally. The Skill allows implicit invocation and first asks whether delegation has a concrete benefit.

```text
Fix this authentication issue, run the relevant tests, then decide whether independent review is actually warranted.
```

<p align="center">
  <img src="assets/readme/workflow.svg" alt="Codex Agent Team workflow" width="100%">
</p>

Typical decision shape:

```text
small and isolated          -> Root
context-heavy / bounded     -> Luna
independent judgment pays   -> Terra
unresolved high consequence -> consent -> Sol
```

Minimum Team keeps ordinary development lightweight while still adding execution or review capacity when the task earns it.

## Roles

<p align="center">
  <img src="assets/readme/roles.svg" alt="Codex Agent Team role map" width="100%">
</p>

| Role | Default route | Responsibility |
| --- | --- | --- |
| Root Controller | current session | intent, planning, risk, acceptance, final answer |
| Explorer / Worker | GPT-5.6 Luna `max` | search, tracing, bounded implementation, debugging, tests |
| Independent Critic | GPT-5.6 Terra `xhigh` | detached review, conflicting evidence, assumption checks |
| Senior Judge | GPT-5.6 Sol `high` | rare high-consequence adjudication after consent |

## What the user sees

When explicitly invoked, when a child is actually created, or when an orchestration gate materially changes execution, the Skill emits a compact receipt such as:

```text
Agent Team
Luna Worker: implemented bounded auth refresh change
Terra Reviewer: triggered by security boundary; verdict clear
Runtime evidence: Luna R1, Terra R2
Verification: 38 tests passed
```

When explicit invocation correctly stays Root-only:

```text
Agent Team: Root only
Why: change already isolated; delegation had no concrete benefit
```

This makes both delegation and deliberate non-delegation visible without adding noise to trivial implicit tasks.

## Core rules

- Minimum Team: zero Subagents is normal; default 1; normal maximum 2.
- Root stays in control: the Skill never silently switches the active Root model or reasoning effort.
- One Writer: one active writing Worker per shared workspace.
- Depth 1: Workers do not create another Subagent team; when observable, Root verifies the child's `parent_thread_id`.
- Fail closed: unprovable exact routes or required permissions return work to Root.
- Evidence first: Worker reports are claims; Root accepts work from actual files, diffs, commands, tests, and reproducible evidence.

If the required route, permission, scope, or external-impact boundary cannot be established safely, the responsibility stays in Root. The project distinguishes configuration assurance, native runtime reports, and mutable local rollout records; local records are never presented as authoritative runtime proof.

Codex Agent Team uses Codex's native `spawn_agent` primitive. It does not create a second Agent runtime, persistent task DAG, or background scheduler.

## Documentation

- [Plugin Installation](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Native Subagent Runtime](docs/native-subagent-runtime.md)
- [Model Route Assurance](docs/model-route-assurance.md)
- [Runtime Evidence](plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md)
- [Compatibility](docs/compatibility.md)
- [Behavioral Evals](docs/behavioral-evals.md)
- [OpenAI References](docs/openai-references.md)
- Policy: [Routing](plugins/codex-agent-team/skills/codex-agent-team/references/routing-policy.md) · [Safety](plugins/codex-agent-team/skills/codex-agent-team/references/safety-policy.md) · [Consent](plugins/codex-agent-team/skills/codex-agent-team/references/consent-policy.md)

## Validation status

The repository includes policy regressions, routing cases, installer lifecycle tests, runtime-evidence fixtures, a deterministic verifier, and a live behavioral benchmark harness. Static tests are never presented as real Codex runtime evidence.

## License

[MIT](LICENSE)
