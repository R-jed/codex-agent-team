# Plugin Installation

Codex Delegate uses Codex Plugin as its only supported distribution path.

## Install the Plugin

Register the GitHub repository as a marketplace source:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Then reopen the ChatGPT desktop app, open the Plugins Directory, choose `Codex Delegate`, and install it.

Use the canonical workflow entry point:

```text
/codex-delegate
```

The repository slug and Plugin package identifier still use `codex-agent-team` during the pre-v1 migration window. They are compatibility identifiers, not the user-facing product name.

## First-run custom Agent provisioning

The Plugin packages the workflow Skill, four namespaced semantic Agent templates, and a fail-closed managed profile installer.

Required roles:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

These role names are retained compatibility identifiers. They describe responsibilities and do not change the `/codex-delegate` user entry point.

The main Skill checks profile readiness only after a responsibility has justified model-specific delegation.

When a required role is missing or an exactly owned earlier profile generation needs upgrading, `/codex-delegate`:

1. explains the exact project-managed file scope and asks permission;
2. discloses that the installer may write the four current profiles and `.codex-agent-team-agents.json`;
3. discloses that a project-owned earlier profile may be replaced only when its current bytes match the active previous ownership hash;
4. discloses that an older model-named profile may be removed only when its current bytes exactly match proven previous project ownership;
5. resolves `../../scripts/install-agents.py` relative to the installed Skill;
6. runs the installer and its non-mutating `--check` verification;
7. re-inspects live native role discovery;
8. continues immediately if the required role is visible, otherwise asks the user to start a fresh Codex task.

Successful file installation is configuration evidence. It does not prove that the current task refreshed role discovery.

## Version 0.5.0

Version `0.5.0` keeps the same four semantic routes and compatibility identifiers while changing orchestration policy from fixed child-count limits to adaptive dependency scheduling.

The shipped profile instructions are updated to support:

- dependency-bound responsibilities;
- evidence-based progress reporting;
- execution-stall reporting instead of unchanged retry loops;
- clean same-lane recovery packets;
- Terra capability-gap validation;
- fresh-context Sol judgment packets.

Because the managed profile bytes changed, upgrading from an exactly owned `0.4.x` profile generation may replace those four managed profile files. This replacement is allowed only when the installed bytes match the ownership hashes from the active project manifest. User-modified or unproven profiles remain untouched and cause the affected route to fail closed.

## Migration from Codex Agent Team 0.3.x and Codex Delegate 0.4.x

Version `0.4.0` introduced the user-facing `Codex Delegate` name and `/codex-delegate` entry point. Version `0.5.0` keeps that identity and introduces adaptive dependency/evidence-driven orchestration.

For migration safety, these identifiers remain unchanged during the pre-v1 window:

```text
GitHub repository:     R-jed/codex-agent-team
Plugin package id:     codex-agent-team
Agent profile ids:     codex_agent_team_*
ownership manifest:    .codex-agent-team-agents.json
```

Do not rename managed profile files or manifests manually. The v1 release process validates real installed-Plugin upgrade/reinstall behavior before any repository or package-id migration is considered.

Older managed releases also used these model-named profiles:

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

The installer migrates away from those names. An old profile is removed only when its current bytes match a hash recorded by the authoritative previous project ownership state. A modified or unproven legacy file is left untouched.

The ownership model has an explicit migration epoch:

- when `.codex-agent-team-agents.json` already exists, that companion manifest is authoritative;
- the older standalone `.codex-agent-team-install.json` may seed ownership only before the companion manifest exists;
- that standalone seed is accepted only for the historical schema `1`, `mode = "profile"` manifest shape actually written by the former profile installer;
- an unknown schema or any other mode is never accepted as legacy-profile deletion authority;
- after migration writes the companion manifest, stale standalone hashes no longer grant deletion authority over a legacy filename that a user may intentionally recreate later.

The current semantic profiles are installed independently and verified byte-for-byte.

## Managed profile safety

The bundled installer:

- writes only the four current Agent profiles plus `.codex-agent-team-agents.json` under Codex home;
- rejects a symlinked Codex home and symlinked managed destination entries;
- rejects another TOML file that claims a current reserved project role name;
- refuses to overwrite a differing current profile unless its bytes match the active previous managed hash;
- removes an old model-named profile only when active previous managed ownership is proven;
- accepts the retired standalone manifest as a one-time ownership seed only for its exact historical schema-1 profile-install shape;
- stages replacements and rolls back managed changes if installation fails;
- supports a strictly non-mutating `--check` mode.

It does not edit `config.toml`, app settings, MCP configuration, credentials, repositories, or unrelated Agent profiles.

The installer is transactional within one process. Concurrent same-Codex-home multi-process behavior remains a live release-validation gate until it is characterized with real filesystem tests.

## Failure behavior

If profile installation or exactness verification fails, the affected responsibility stays in the main session. Do not manually overwrite, rename, or cross-route a conflicting role.

If file installation succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-delegate` again.
