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

Use Codex CLI commands rather than manually editing `config.toml`, marketplace state, or installed-Plugin state.

Register the repository-backed marketplace:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate
```

Install the Plugin:

```bash
codex plugin add codex-delegate@codex-delegate
```

Start a **new Codex thread** after installation, then use:

```text
/codex-delegate
```

The Codex desktop Plugins UI may be used after the marketplace is registered. The CLI sequence above remains the deterministic release-validation contract.

## Upgrade or reinstall

A configured Git marketplace is a local snapshot. Refresh it before reinstalling the current Plugin bytes:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a **new Codex thread** before testing the updated Skill.

During release validation, record the marketplace upgrade result, installed Plugin version, and fresh-thread discovery. Do not hand-edit marketplace files or `config.toml` to simulate an update.

For behavior-preserving development where semantic version `0.6.0` remains unchanged, Checkpoint 6 verifies on the tested Codex build that `marketplace upgrade` followed by explicit `plugin add` refreshes installed bytes. If that behavior is not reliable, bump the patch version before RC rather than relying on stale-cache assumptions.

## Public identity

The current public identity is:

```text
GitHub repository: R-jed/codex-delegate
Marketplace id:    codex-delegate
Plugin package id: codex-delegate
Skill / command:   codex-delegate / /codex-delegate
```

The repository Plugin bundle is:

```text
.agents/plugins/marketplace.json
plugins/codex-delegate/
  .codex-plugin/plugin.json
  assets/
  skills/
  scripts/
  agent-profiles/
```

The Plugin root folder, `.codex-plugin/plugin.json` `name`, marketplace name, and marketplace plugin entry are all `codex-delegate`. The marketplace source path is:

```text
./plugins/codex-delegate
```

Brand assets are packaged inside `plugins/codex-delegate/assets/` and declared through the supported Plugin `interface` fields so Codex can render the logo and composer icon from the installed archive.

## One-time migration from the legacy public id

Older releases used the public repository/package/marketplace id `codex-agent-team`. Codex's current Git marketplace upgrade path requires the configured marketplace name to match the upgraded marketplace manifest name, so an existing `codex-agent-team` marketplace cannot be converted in place by `marketplace upgrade` after the manifest becomes `codex-delegate`.

For a real legacy installation, remove the old public Plugin and marketplace registration first:

```bash
codex plugin remove codex-agent-team@codex-agent-team
codex plugin marketplace remove codex-agent-team
```

Then register and install the current identity:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a **new Codex thread** and verify `/codex-delegate` discovery before making any custom-role claim.

This public-ID migration deliberately does **not** rename the existing managed custom-Agent identities or ownership receipt:

```text
Agent role ids:      codex_agent_team_*
profile filenames:   codex-agent-team-*.toml
ownership manifest:  .codex-agent-team-agents.json
legacy manifest:     .codex-agent-team-install.json
```

Those values are compatibility identifiers for already-managed files. Keeping them stable lets the new Plugin reuse and safely verify previous exact profile installations without manufacturing a second ownership generation. Do not rename those files manually.

## First-run custom Agent provisioning

Required roles remain:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

These are internal compatibility identifiers. They do not change the `/codex-delegate` user entry point or current Plugin package id.

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

## Version 0.6.0

Version `0.6.0` retains adaptive dependency scheduling, evidence reuse, the Intervention Gate, Recovery Ledger, completion-driven scheduling policy, and the risk-triggered Final Review Gate. The public repository/marketplace/Plugin identity is now aligned with `codex-delegate`; the four managed Agent profile identities remain stable for compatibility.

Sol remains selective globally. A semantic trigger can make a fresh `codex_agent_team_advisor` review mandatory for one candidate after main-session verification. The candidate is bound to a deterministic `review_artifact_id`; any deliverable mutation after review invalidates the old verdict.

```text
main-session verification
-> Candidate Ready
-> fresh Sol final review when required
-> ship | fix-first | rethink
```

`INSUFFICIENT_EVIDENCE` keeps the gate unresolved until the named evidence dependency is established and a new fresh review runs. `fix-first` requires correction, re-verification, a new artifact identity, and a new fresh review. `rethink` returns affected architecture, contract, or invariant assumptions to the main session.

Final-review triggering is semantic rather than numeric. No fixed diff threshold, file threshold, retry threshold, model ladder, or mandatory Luna -> Terra -> Sol pipeline is introduced.

## Legacy managed-profile migration

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
- `.codex-agent-team-install.json` may seed ownership only before the companion manifest exists;
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

Each release candidate must:

1. run the then-current OpenAI `plugin-creator/scripts/validate_plugin.py` against `plugins/codex-delegate` and record the validator source revision/version;
2. verify the marketplace entry points to `./plugins/codex-delegate` and carries required policy/category metadata;
3. perform a real fresh `R-jed/codex-delegate` marketplace install;
4. run `codex plugin add codex-delegate@codex-delegate`;
5. start a new thread and confirm `/codex-delegate` discovery;
6. exercise the one-time legacy public-ID migration from a representative `codex-agent-team` install;
7. verify the legacy internal profile ids/filenames and ownership manifest remain safe and reusable across the public-ID migration;
8. authorize first-run profile provisioning when needed and verify all four exact roles are discovered;
9. exercise the required Final Review Gate path on representative live workloads;
10. record the exact Codex build, Plugin version, validator revision, commands, and outcomes in `LOCAL_VALIDATION_REPORT.md`.

CI also runs a pinned official OpenAI Plugin validator for deterministic regression protection. That pin is static evidence only; RC validation still reruns the then-current official validator.

## Failure behavior

If marketplace registration/upgrade, Plugin installation, public-ID migration, official validation, profile provisioning, exactness verification, or a required final-review dependency fails, stop and record the actual failure. Do not manually patch user config to make the supported path appear successful.

If profile installation fails, the affected responsibility stays in the main session. Do not manually overwrite, rename, or cross-route a conflicting role.

If provisioning succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-delegate` again.
