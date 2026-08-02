# Plugin Installation

Codex Agent Team uses Codex Plugin as its only supported distribution path.

## Install the Plugin

Register the GitHub repository as a marketplace source:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Then reopen the ChatGPT desktop app, open the Plugins Directory, choose the `Codex Agent Team` marketplace, and install `Codex Agent Team`.

After installation, use the single user entry point:

```text
/codex-agent-team
```

## First-run custom Agent provisioning

The Plugin contains the workflow Skill, the four role-pinned Agent templates, and a fail-closed managed profile installer. Codex custom Agent TOML files are discovered from the user's Codex Agent directory, so the main Skill performs a readiness check before any model-specific delegation.

Required roles:

```text
luna_explorer   -> gpt-5.6-luna / max
luna_worker     -> gpt-5.6-luna / max
terra_reviewer  -> gpt-5.6-terra / xhigh
sol_judge       -> gpt-5.6-sol / high
```

When all four exact roles are already visible through the current native `spawn_agent` role surface, normal orchestration continues.

When one or more roles are missing, `/codex-agent-team`:

1. explains that four managed custom Agent profiles need to be written under Codex home;
2. asks the user for permission before writing them;
3. resolves the bundled `../../scripts/install-agents.py` relative to the installed Skill;
4. runs the installer and then its strictly non-mutating `--check` verification;
5. re-inspects the live native role surface;
6. continues immediately if the roles are now visible, otherwise asks the user to start a fresh Codex task and invoke `/codex-agent-team` again.

The Skill never treats successful file installation as proof that the current task has refreshed custom-Agent discovery.

## Managed profile safety

The bundled `scripts/install-agents.py`:

- writes only the four Codex Agent Team TOML profiles plus `.codex-agent-team-agents.json` under Codex home;
- rejects symlinked destinations;
- rejects another TOML file that claims a reserved project role name;
- refuses to overwrite a differing profile unless its current bytes match a previous Codex Agent Team managed hash;
- can recognize hashes from older Codex Agent Team managed installs for migration safety;
- stages replacements and rolls back managed changes if installation fails;
- supports a strictly non-mutating `--check` mode.

It does not edit `config.toml`, app settings, MCP configuration, credentials, repositories, or unrelated Agent profiles.

## Failure behavior

If profile installation or verification fails, the affected model-specific delegation stays in Root and the installer error is reported without manual overwrite or role substitution.

If profile installation succeeds but the current task still does not expose the four roles, start a fresh Codex task. This is a runtime discovery boundary, not an installation failure.

If a local profile differs from a managed version, inspect the local modification deliberately. The installer fails closed instead of replacing it automatically.
