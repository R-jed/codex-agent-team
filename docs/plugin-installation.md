# Plugin Installation

Codex Delegate uses the native Codex Plugin system as its only supported distribution path.

The Plugin and custom Agent profiles are separate Codex surfaces:

```text
Codex Plugin
-> distributes the Codex Delegate Skill and bundled project files

Codex custom-Agent configuration
-> exposes the four exact semantic roles used for model-specific delegation
```

The Plugin manifest does not claim a native `agents` component. The four Agent templates are bundled project files and are provisioned only after explicit user approval into the active personal Codex Agent directory. The default personal location is `~/.codex/agents`; when an explicit `CODEX_HOME` is used, the project targets that Codex home's `agents` directory and validates live discovery.

## Fresh install

For this repository-backed Git marketplace, use Codex CLI commands rather than manually editing `config.toml`, marketplace state, or installed-Plugin state.

Register the marketplace with the two sparse paths required for marketplace discovery and Plugin installation:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team
```

Then install the Plugin by its package id and configured marketplace name:

```bash
codex plugin add codex-agent-team@codex-agent-team
```

Start a **new Codex thread** after installation so the runtime can pick up the installed Skill surface, then use:

```text
/codex-delegate
```

The Codex desktop Plugins UI may be used as a user-interface alternative after the marketplace is registered. The CLI sequence above is the deterministic installation contract used by this project's release validation.

The repository slug and Plugin package identifier remain `codex-agent-team` during the pre-v1 compatibility window. They are internal compatibility identifiers, not the user-facing product name.

## Upgrade or reinstall from the Git marketplace

A configured Git marketplace is a local snapshot. A newer remote `main` does not by itself prove that the installed marketplace snapshot or Plugin content is current.

For an existing Codex Delegate marketplace installation, refresh the configured marketplace first:

```bash
codex plugin marketplace upgrade codex-agent-team
```

Then reinstall the Plugin from that refreshed marketplace:

```bash
codex plugin add codex-agent-team@codex-agent-team
```

Start a **new Codex thread** before testing the updated Skill.

During release validation, record the marketplace upgrade result, installed Plugin version, and fresh-thread discovery. Do not hand-edit marketplace files or `config.toml` to simulate an update.

For local Plugin-development iteration where the semantic version is intentionally unchanged, follow the current OpenAI plugin-creator cachebuster/reinstall workflow. Release versions such as `0.5.0 -> 0.5.1` use the real version change and do not need an artificial cachebuster solely to represent that release.

## Official Plugin boundary

The repository follows the Codex Plugin bundle shape:

```text
.agents/plugins/marketplace.json
plugins/codex-agent-team/
  .codex-plugin/plugin.json
  skills/
  scripts/
  agent-profiles/
```

The Plugin root folder and `.codex-plugin/plugin.json` `name` are both `codex-agent-team`.

The marketplace entry points to the nested Plugin through:

```text
./plugins/codex-agent-team
```

and declares installation policy, authentication policy, and category metadata.

Only supported Plugin-manifest components are declared. Codex Delegate does **not** invent an unsupported `agents` manifest field. Custom Agent provisioning is an explicit post-install workflow over Codex's native custom-Agent configuration surface.

## First-run custom Agent provisioning

Required roles:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

These names are compatibility identifiers. They do not change the `/codex-delegate` user entry point.

The main Skill checks role readiness only after a responsibility has justified model-specific delegation.

When a required role is missing or an exactly owned earlier generation needs migration, `/codex-delegate`:

1. explains the exact project-managed file scope and asks permission;
2. discloses that the installer may write the four current profiles under the active Codex-home `agents` directory and `.codex-agent-team-agents.json` under Codex home;
3. replaces an earlier project-owned profile only when its current bytes match active previous ownership evidence;
4. removes an older model-named profile only when its current bytes exactly match proven previous project ownership;
5. resolves `../../scripts/install-agents.py` relative to the installed Skill;
6. runs the installer and non-mutating `--check` verification;
7. re-inspects native role discovery;
8. continues when the required exact role is visible, otherwise asks the user to start a fresh Codex task.

Successful file installation is configuration evidence. It does not prove current-task role refresh or the effective route of a spawned child.

## Version 0.5.1

Version `0.5.1` keeps the v0.5.0 semantic routes and adaptive dependency scheduling while refining recovery governance and official Plugin installation documentation.

Recovery now separates:

```text
execution evidence
-> structured progress signals
-> Intervention Gate
-> recovery classification
-> effective action
```

It adds a bounded Recovery Ledger, proposed-versus-effective action provenance, event-driven recovery evaluation, and an explicit live gate for child-progress observability.

No fixed retry count, fixed stall threshold, cheap-first model ladder, or product hard child ceiling is introduced.

The managed Agent profile bytes are unchanged from v0.5.0. An exact v0.5.0 profile generation therefore does not need replacement solely because the Plugin Skill moved to v0.5.1.

## Migration from Codex Agent Team 0.3.x and Codex Delegate 0.4.x / 0.5.0

For real installed upgrades, use the supported Git marketplace lifecycle:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Then start a new Codex thread and verify the installed Plugin version and `/codex-delegate` discovery before any custom-role claim.

For migration safety, these identifiers remain unchanged during pre-v1:

```text
GitHub repository:     R-jed/codex-agent-team
Plugin package id:     codex-agent-team
Agent profile ids:     codex_agent_team_*
ownership manifest:    .codex-agent-team-agents.json
```

Do not rename managed profile files or manifests manually. The v1 release process validates real upgrade/reinstall behavior before repository or package-id migration is considered.

Older managed releases also used:

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

An old profile is removed only when its current bytes match authoritative previous project ownership. A modified or unproven legacy file is left untouched.

The ownership epoch is explicit:

- `.codex-agent-team-agents.json`, once present, is authoritative;
- the older `.codex-agent-team-install.json` may seed ownership only before the companion manifest exists;
- that seed is accepted only for the historical schema `1`, `mode = "profile"` shape;
- unknown schemas/modes never grant legacy deletion authority;
- after migration, stale standalone hashes do not authorize deletion of a legacy filename a user may later recreate.

## Managed profile safety

The bundled installer:

- writes only the four current Agent profiles plus `.codex-agent-team-agents.json` under the active Codex home;
- uses the active Codex-home `agents` directory, whose default personal location is `~/.codex/agents`;
- rejects a symlinked Codex home and symlinked managed destinations;
- rejects another TOML file claiming a reserved project role name;
- refuses to overwrite a differing current profile unless previous managed ownership is proven by exact hash;
- removes legacy model-named profiles only with exact ownership proof;
- stages replacements and rolls back managed changes if one-process installation fails;
- supports a strictly non-mutating `--check` mode.

It does not edit `config.toml`, app settings, MCP configuration, credentials, repositories, or unrelated Agent profiles.

Concurrent same-Codex-home multi-process behavior remains a live release gate. No inter-process lock is added until reproducible evidence shows it is needed.

## Plugin validation before release

Static repository tests are insufficient to claim current official Plugin compatibility.

Each release candidate must:

1. run the current OpenAI `plugin-creator/scripts/validate_plugin.py` against `plugins/codex-agent-team` and record the validator source revision/version;
2. verify the marketplace entry points to `./plugins/codex-agent-team` and carries required policy/category metadata;
3. perform a real Git marketplace add or upgrade as appropriate;
4. run `codex plugin add codex-agent-team@codex-agent-team`;
5. start a new thread and confirm `/codex-delegate` discovery;
6. authorize first-run profile provisioning when needed and verify all four exact roles are discovered from the active Codex Agent directory;
7. record the exact Codex build, Plugin version, validator revision, commands, and outcomes in `LOCAL_VALIDATION_REPORT.md`.

CI also runs a pinned official OpenAI Plugin validator for deterministic regression protection. That pin is static evidence only; RC validation still reruns the then-current official validator.

## Failure behavior

If marketplace registration/upgrade, Plugin installation, official validation, profile provisioning, or exactness verification fails, stop and record the actual failure. Do not manually patch user config to make the supported path appear successful.

If profile installation fails, the affected responsibility stays in the main session. Do not manually overwrite, rename, or cross-route a conflicting role.

If provisioning succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-delegate` again.
