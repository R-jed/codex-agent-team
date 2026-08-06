# Plugin Installation

codex delegate is distributed through the native Codex Plugin system. Users can install it from the Codex Plugins Directory when a public listing is available, or through the canonical Git repo marketplace from the command line.

## Installation options

### Option 1: Codex Plugin Marketplace

Use this path when `codex-delegate` is visible in the Plugins Directory available to your Codex environment.

In the ChatGPT desktop app:

1. Switch to **Codex**.
2. Open **Plugins**.
3. Search for `codex-delegate`.
4. Open the plugin details and select `+` to install it.
5. Start a new Codex session after installation.

Codex CLI users can also enter `/plugins` to open the plugin browser, search or browse the available marketplace entries, and install from there.

The public Plugins Directory is a separate distribution surface from this repository marketplace. A public listing appears only after the plugin has been submitted, approved, and published through OpenAI's plugin publication flow. If `codex-delegate` is not visible in the Plugins Directory available to the user, use the command-line installation below.

### Option 2: Command-line installation

Copy and run this block once:

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

The marketplace registration command is safe to repeat when the same canonical source is already configured. Codex recognizes the existing registration and keeps using it.

After either installation path, start a new Codex thread and invoke explicitly:

```text
$codex-delegate:codex-delegate <task>
```

`/skills` opens the Codex Skill picker.

## Canonical command-line marketplace source

Keep this source shape unchanged:

```text
repository:    R-jed/codex-delegate
ref:           main
sparse path 1: .agents/plugins
sparse path 2: plugins/codex-delegate
marketplace:   codex-delegate
plugin:        codex-delegate
```

Codex treats the Git source, ref, and sparse paths as part of marketplace source identity. Changing those fields can make an existing registration look like a different source even when the repository ultimately contains the same Plugin.

For that reason, command-line documentation and support should always use the canonical command above.

Do not shorten the command by removing either `--sparse` path for existing users. Do not replace the source with a local checkout in normal command-line installation instructions.

## Update

For users installed through the command-line repo marketplace, copy and run:

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

Then start a new Codex thread.

The marketplace upgrade refreshes the configured Git snapshot. Re-running `codex plugin add` installs the Plugin from that refreshed snapshot.

For users installed through the Plugins Directory, use the **Plugins** installed area to review and manage the installed plugin, then start a new Codex session after an update.

## Source conflict repair

This section applies to the command-line repo marketplace path.

If installation reports:

```text
marketplace 'codex-delegate' is already added from a different source
```

first inspect the configured marketplaces:

```bash
codex plugin marketplace list --json
```

If `codex-delegate` is registered from an old or incorrect source, remove only that marketplace registration:

```bash
codex plugin marketplace remove codex-delegate
```

Then run the canonical command-line installation block again:

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

This repair is for historical or mismatched installations. New users and users already on the canonical source do not need the remove step.

Do not hand-edit `config.toml`, marketplace cache files, or installed Plugin cache directories to repair a source mismatch.

## Verify the installation

For a command-line repo marketplace installation, inspect the marketplace and installed Plugin state with:

```bash
codex plugin marketplace list --json
codex plugin list --marketplace codex-delegate
```

For a Plugins Directory installation, confirm that `codex-delegate` appears in the installed plugins area.

After installation or update, always test from a new Codex thread.

## Current identity

```text
Repository:          R-jed/codex-delegate
Repo marketplace id: codex-delegate
Plugin id:           codex-delegate
Skill:               codex-delegate
Invocation:          $codex-delegate:codex-delegate
Version:             1.1.0
```

Implicit invocation is disabled. Use `$codex-delegate:codex-delegate` explicitly when you want the Plugin to orchestrate a task.

## First-use Agent readiness

Plugin installation and custom Agent profile readiness are separate Codex surfaces.

When an explicit `$codex-delegate:codex-delegate` task actually benefits from a child, the Skill checks the required exact role before delegated code execution starts. If provisioning is needed, it:

1. explains the project-managed write scope and asks permission;
2. resolves `../../scripts/install-agents.py` relative to the installed Skill;
3. writes or verifies only the five managed native custom Agent profiles, `.codex-delegate-agents.json`, and `.codex-delegate-agents.lock` under the active Codex home;
4. runs a non-mutating `--check`;
5. re-inspects the role surface exposed by the current runtime;
6. stops before delegated writing and asks for a new thread if the current thread cannot discover the newly installed roles.

Current managed roles:

```text
codex_delegate_reader       -> GPT-5.6 Luna / max    / read-only
codex_delegate_worker       -> GPT-5.6 Luna / max    / workspace-write
codex_delegate_solver       -> GPT-5.6 Sol / high    / workspace-write
codex_delegate_investigator -> GPT-5.6 Terra / xhigh / read-only
codex_delegate_advisor      -> GPT-5.6 Sol / high    / read-only
```

The bundled installer manages only these profiles and its ownership/lock files. It leaves unrelated Agent profiles untouched and does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent state.

The persistent installer lock serializes installers targeting the same Codex home so one failed rollback cannot erase a successful peer.

## Development and release validation

`main` is a moving development channel. Validation evidence for a specific build applies only to the exact revision tested.

For a fixed release candidate:

1. bind an immutable candidate SHA or tag;
2. validate `plugins/codex-delegate/.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`;
3. run the repository-pinned official OpenAI Plugin validator;
4. run the then-current official OpenAI Plugin validator when current compatibility evidence is required;
5. run the full deterministic test suite;
6. verify the canonical Git marketplace install/update path when installation behavior changed;
7. verify the Plugins Directory path separately when public-directory discoverability is part of acceptance;
8. verify first-use five-role provisioning when the managed profile lifecycle changed;
9. test from a fresh Codex thread.

Static validation cannot prove routing quality, coordination quality, recovery quality, live runtime route identity, or public-directory publication.

## Public directory boundary

ChatGPT and Codex share one universal public plugin directory. Published plugins can be discovered and installed from supported Plugins surfaces.

Repository marketplace packaging does not establish that a public directory listing exists. Only describe `codex-delegate` as currently searchable in the public Plugins Directory after that listing has been independently verified.

## Failure behavior

If marketplace registration, marketplace refresh, Plugin installation, profile provisioning, or validation fails, report the actual failure and preserve the user's existing configuration.

Do not manually patch Codex configuration or caches to make the supported installation path appear successful.
