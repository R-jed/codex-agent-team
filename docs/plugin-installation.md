# Plugin Installation

Codex Agent Team supports two distribution paths:

- **Plugin** is the recommended community path.
- **Standalone** remains available for users who prefer a repository-managed Skill install.

## Why Plugin setup has two stages

The Codex Plugin package provides the workflow Skills. The model-pinned custom Agent profiles are user-level Codex files under `~/.codex/agents/`, so Codex Agent Team treats them as explicit companion setup rather than assuming Plugin installation registered them.

This keeps the boundary visible:

```text
Plugin package
  -> codex-agent-team Skill
  -> codex-agent-team-setup Skill

Companion setup
  -> luna_explorer
  -> luna_worker
  -> terra_reviewer
  -> sol_judge
```

## Install the Plugin

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
codex plugin add codex-agent-team@codex-agent-team
```

Then invoke:

```text
$codex-agent-team-setup
```

The setup Skill resolves the bundled `scripts/install-agents.py` from its own Plugin package, installs only the four project profiles, and runs a byte-exact check.

Start a fresh Codex task after setup. Custom Agent discovery happens at task/runtime initialization, so the task that performed setup must not claim the new roles are already visible.

## Companion installer safety

`scripts/install-agents.py`:

- writes only the four Codex Agent Team TOML profiles plus `.codex-agent-team-agents.json` under Codex home;
- rejects symlinked destinations;
- rejects another TOML file that claims a reserved project role name;
- refuses to overwrite a differing profile unless its current bytes match a previous Codex Agent Team managed hash;
- can use the standalone install manifest as prior ownership evidence when a user migrates from standalone to Plugin;
- stages replacements and rolls back managed changes if installation fails;
- supports a strictly non-mutating `--check` mode.

It does not edit `config.toml`, app settings, MCP configuration, credentials, or unrelated Agent profiles.

## Standalone installation

Standalone installation already includes the custom Agent step:

```bash
git clone https://github.com/R-jed/codex-agent-team.git
cd codex-agent-team
python scripts/install.py
python scripts/install.py --check
```

There is no need to run `$codex-agent-team-setup` after a successful default standalone install.

## Portable Mode

Users who deliberately want Skill-only routing can install:

```bash
python scripts/install.py --skill-only
```

Portable Mode depends on the live native spawn surface exposing and accepting exact model and reasoning-effort fields. It does not use the companion project profiles.

## Troubleshooting

If Profile Mode reports that `luna_explorer`, `luna_worker`, `terra_reviewer`, or `sol_judge` is missing:

1. run `$codex-agent-team-setup`;
2. require its install and exactness check to succeed;
3. start a fresh Codex task;
4. inspect the live `spawn_agent` role surface again.

If setup reports a differing profile, inspect that local file. The installer intentionally refuses to replace it automatically because it may contain a user modification.
