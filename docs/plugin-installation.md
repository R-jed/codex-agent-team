# Plugin Installation

codex delegate is distributed through the native Codex Plugin system. The supported repository installation path uses a Git marketplace source and the normal `codex plugin` commands.

## Normal installation

Copy and run this block once:

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

Then start a new Codex thread and invoke explicitly:

```text
$codex-delegate:codex-delegate <task>
```

`/skills` opens the Codex Skill picker.

This is the normal installation path for new users.

The marketplace registration command is also safe to repeat when the same canonical source is already configured. Codex recognizes the existing registration and keeps using it.

## Canonical marketplace source

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

For that reason, normal documentation and support should always use the canonical command above.

Do not shorten the command by removing either `--sparse` path for existing users. Do not replace the source with a local checkout in normal installation instructions.

## Update

Copy and run:

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

Then start a new Codex thread.

The marketplace upgrade refreshes the configured Git snapshot. Re-running `codex plugin add` installs the Plugin from that refreshed snapshot.

## Source conflict repair

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

Then run the normal installation block again:

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

This repair is for historical or mismatched installations. New users and users already on the canonical source do not need the remove step.

Do not hand-edit `config.toml`, marketplace cache files, or installed Plugin cache directories to repair a source mismatch.

## Verify the installation

To inspect the marketplace and installed Plugin state:

```bash
codex plugin marketplace list --json
codex plugin list --marketplace codex-delegate
```

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
7. verify first-use five-role provisioning when the managed profile lifecycle changed;
8. test from a fresh Codex thread.

Static validation cannot prove routing quality, coordination quality, recovery quality, or live runtime route identity.

## Public directory note

The repository marketplace and any OpenAI-hosted public Plugin directory are separate distribution surfaces. Repository installation does not establish that a public directory listing exists.

Only describe codex delegate as directly searchable in an OpenAI-hosted public directory after that listing has been independently verified.

## Failure behavior

If marketplace registration, marketplace refresh, Plugin installation, profile provisioning, or validation fails, report the actual failure and preserve the user's existing configuration.

Do not manually patch Codex configuration or caches to make the supported installation path appear successful.
