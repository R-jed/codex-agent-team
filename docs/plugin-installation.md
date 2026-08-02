# Plugin Installation

Codex Agent Team uses Codex Plugin as its only supported distribution path.

## Install the Plugin

Register the GitHub repository as a marketplace source:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Then reopen the ChatGPT desktop app, open the Plugins Directory, choose the `Codex Agent Team` marketplace, and install `Codex Agent Team`.

Use the single workflow entry point:

```text
/codex-agent-team
```

## First-run custom Agent provisioning

The Plugin packages the workflow Skill, four namespaced semantic Agent templates, and a fail-closed managed profile installer.

Required roles:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

Role names describe responsibilities, not permanent model identities.

The main Skill checks profile readiness only after a responsibility has actually justified model-specific delegation.

When a required role is missing, `/codex-agent-team`:

1. explains that four managed custom Agent profiles need to be written under Codex home;
2. asks permission before writing them;
3. resolves `../../scripts/install-agents.py` relative to the installed Skill;
4. runs the installer and its non-mutating `--check` verification;
5. re-inspects live native role discovery;
6. continues immediately if the required role is visible, otherwise asks the user to start a fresh Codex task.

Successful file installation is configuration evidence. It does not prove that the current task refreshed role discovery.

## Migration from older model-named profiles

Older managed releases used:

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

The v0.3 installer migrates away from those names. An old profile is removed only when its current bytes match a hash recorded by a previous Codex Agent Team managed install. A modified or unproven legacy file is left untouched.

The current semantic profiles are installed independently and verified byte-for-byte.

## Managed profile safety

The bundled installer:

- writes only the four current Agent profiles plus `.codex-agent-team-agents.json` under Codex home;
- rejects symlinked destinations;
- rejects another TOML file that claims a current reserved project role name;
- refuses to overwrite a differing current profile unless its bytes match a previous managed hash;
- removes an old model-named profile only when previous managed ownership is proven;
- stages replacements and rolls back managed changes if installation fails;
- supports a strictly non-mutating `--check` mode.

It does not edit `config.toml`, app settings, MCP configuration, credentials, repositories, or unrelated Agent profiles.

## Failure behavior

If profile installation or exactness verification fails, the affected responsibility stays in the main session. Do not manually overwrite, rename, or cross-route a conflicting role.

If file installation succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-agent-team` again.
