# Plugin Installation

Codex Delegate uses the native Codex Plugin system as its only supported distribution path.

The Plugin and the custom Agent profiles have different responsibilities:

```text
Codex Plugin
-> distributes the Codex Delegate Skill and bundled project files

Codex custom-Agent configuration
-> exposes the four exact semantic roles used for model-specific delegation
```

The Plugin manifest does not claim a native `agents` component. The four Agent templates are bundled project files and are provisioned only after explicit user approval into Codex's supported personal custom-Agent location under `$CODEX_HOME/agents` (normally `~/.codex/agents`).

## Install the Plugin

For this repository-backed marketplace, use Codex's marketplace and Plugin commands rather than manually editing `config.toml` or marketplace state.

Register the Git marketplace with the two paths needed for discovery and installation:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team
```

Then install the Plugin by its package id and marketplace name:

```bash
codex plugin add codex-agent-team@codex-agent-team
```

Start a **new Codex thread** after installation or reinstall so the runtime can pick up the installed Skill surface, then use:

```text
/codex-delegate
```

The Codex desktop Plugins UI may be used as a user-interface alternative after the marketplace is registered, but the CLI sequence above is the deterministic installation contract used by this project's release validation.

The repository slug and Plugin package identifier still use `codex-agent-team` during the pre-v1 migration window. They are compatibility identifiers, not the user-facing product name.

## Official Plugin boundary

The repository follows the current Codex Plugin bundle shape:

```text
.agents/plugins/marketplace.json
plugins/codex-agent-team/
  .codex-plugin/plugin.json
  skills/
  scripts/
  agent-profiles/
```

The Plugin root name and `.codex-plugin/plugin.json` `name` remain identical: `codex-agent-team`.

The marketplace entry points to the Plugin through the relative source path:

```text
./plugins/codex-agent-team
```

It also declares installation policy, authentication policy, and category metadata.

Only components supported by the Plugin manifest are declared there. In particular, Codex Delegate does **not** invent an unsupported `agents` manifest field. Custom Agent provisioning is an explicit post-install workflow over Codex's native custom-Agent configuration surface.

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
2. discloses that the installer may write the four current profiles under the active `$CODEX_HOME/agents` and `.codex-agent-team-agents.json` under Codex home;
3. discloses that a project-owned earlier profile may be replaced only when its current bytes match the active previous ownership hash;
4. discloses that an older model-named profile may be removed only when its current bytes exactly match proven previous project ownership;
5. resolves `../../scripts/install-agents.py` relative to the installed Skill;
6. runs the installer and its non-mutating `--check` verification;
7. re-inspects live native role discovery;
8. continues immediately if the required role is visible, otherwise asks the user to start a fresh Codex task.

Successful file installation is configuration evidence. It does not prove that the current task refreshed role discovery or that a spawned child used the expected effective route.

## Version 0.5.1

Version `0.5.1` keeps the v0.5.0 semantic routes and adaptive dependency scheduling while refining execution recovery and Plugin-installation documentation.

The recovery policy now distinguishes:

```text
execution evidence
-> structured progress signals
-> Intervention Gate
-> recovery classification
-> effective action
```

It adds a bounded Recovery Ledger, proposed-versus-effective action provenance, event-driven recovery evaluation, and an explicit release gate for native child-progress observability.

No fixed retry count, fixed stall threshold, cheap-first model ladder, or product hard child ceiling is introduced.

The managed Agent profile bytes are unchanged from v0.5.0 in this release. Version `0.5.1` therefore does not require profile replacement solely because of the recovery-policy refinement. Existing profile exactness is still checked before model-specific delegation.

## Migration from Codex Agent Team 0.3.x and Codex Delegate 0.4.x / 0.5.0

Version `0.4.0` introduced the user-facing `Codex Delegate` name and `/codex-delegate` entry point. Version `0.5.0` introduced adaptive dependency/evidence-driven orchestration. Version `0.5.1` refines recovery governance and makes the official Plugin/custom-Agent boundary explicit.

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

- writes only the four current Agent profiles plus `.codex-agent-team-agents.json` under the active Codex home;
- uses the official personal custom-Agent directory `$CODEX_HOME/agents` for those profiles;
- rejects a symlinked Codex home and symlinked managed destination entries;
- rejects another TOML file that claims a current reserved project role name;
- refuses to overwrite a differing current profile unless its bytes match the active previous managed hash;
- removes an old model-named profile only when active previous managed ownership is proven;
- accepts the retired standalone manifest as a one-time ownership seed only for its exact historical schema-1 profile-install shape;
- stages replacements and rolls back managed changes if installation fails;
- supports a strictly non-mutating `--check` mode.

It does not edit `config.toml`, app settings, MCP configuration, credentials, repositories, or unrelated Agent profiles.

The installer is transactional within one process. Concurrent same-Codex-home multi-process behavior remains a live release-validation gate until it is characterized with real filesystem tests.

## Plugin validation before release

Static repository tests are not sufficient to claim official Plugin compatibility.

For each release candidate:

1. validate the Plugin root against the current OpenAI `plugin-creator` validator (`scripts/validate_plugin.py` from the matching current Codex source/tooling);
2. verify the repository marketplace file points to the nested Plugin root and declares the required policy/category metadata;
3. perform the real marketplace-add and `codex plugin add codex-agent-team@codex-agent-team` flow on the tested Codex build;
4. start a new thread and confirm `/codex-delegate` is discovered;
5. authorize first-run profile provisioning and verify all four exact roles are discovered from `$CODEX_HOME/agents`;
6. record the exact Codex build, Plugin version, validator source revision/version, and actual result in `LOCAL_VALIDATION_REPORT.md`.

Do not hand-edit `config.toml` or marketplace files as a substitute for the installation commands during this release test.

## Failure behavior

If marketplace registration, Plugin installation, Plugin validation, profile installation, or exactness verification fails, stop and report the observed failure. Do not manually patch user config to make the release gate appear successful.

If profile installation or exactness verification fails, the affected responsibility stays in the main session. Do not manually overwrite, rename, or cross-route a conflicting role.

If file installation succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-delegate` again.
