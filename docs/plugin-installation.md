# Plugin Installation

codex delegate uses the native Codex Plugin system as its only supported distribution path.

Plugin packaging and custom Agent profiles are separate Codex surfaces. The Plugin distributes the Skill and bundled project files. Exact model-specific roles are provisioned, after explicit user approval, into the active Codex-home `agents` directory. The default personal location is `~/.codex/agents`.

## Current identity

```text
Repository:       R-jed/codex-delegate
Marketplace id:  codex-delegate
Plugin id:       codex-delegate
Skill/command:   codex-delegate / /codex-delegate
Version:         0.7.0
```

Current managed Agent state is:

```text
codex-delegate-reader.toml        -> codex_delegate_reader       -> GPT-5.6 Luna / max
codex-delegate-worker.toml        -> codex_delegate_worker       -> GPT-5.6 Luna / max
codex-delegate-investigator.toml  -> codex_delegate_investigator -> GPT-5.6 Terra / xhigh
codex-delegate-advisor.toml       -> codex_delegate_advisor      -> GPT-5.6 Sol / high
.codex-delegate-agents.json       -> project ownership receipt
```

These are the only current project role/profile/ownership identities.

## Fresh install

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a **new Codex thread**, then use `/codex-delegate`.

Do not manually edit `config.toml`, marketplace state, Plugin cache state, or Agent profiles to simulate installation.

## Update or reinstall

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread before testing the updated Skill.

Version 0.7.0 intentionally changes the managed Agent namespace, so use the new Plugin bytes before testing role discovery.

## First-run custom Agent provisioning

The main Skill checks role readiness only after a responsibility justifies model-specific delegation. When an exact role is unavailable, `/codex-delegate`:

1. explains the exact project-managed file/migration scope and asks permission;
2. resolves `../../scripts/install-agents.py` relative to the installed Skill;
3. writes or verifies only the four current profiles and `.codex-delegate-agents.json` under the active Codex home;
4. performs bounded one-way migration of older project-owned profile state when required;
5. runs a non-mutating `--check` after installation;
6. re-inspects native role discovery;
7. asks for a fresh Codex task if the current task still cannot see the new roles.

Successful file installation is configuration evidence. It does not prove the route/model/effort/sandbox actually observed for a spawned child.

## Migration from codex delegate 0.6.x

0.6.x used an older internal Agent namespace even after the public Plugin id became `codex-delegate`. 0.7.0 removes that active compatibility layer.

After updating the Plugin, the first provisioning pass recognizes the prior project-owned generation only as migration input. When its ownership receipt proves the exact current bytes, the installer:

```text
creates/verifies codex-delegate-*.toml
creates .codex-delegate-agents.json
removes proven old codex-agent-team-*.toml files
removes proven old .codex-agent-team-*.json ownership receipts
verifies no codex_agent_team_* role remains
```

The old names do not remain as fallback roles after a successful migration.

If an old project-named Agent file exists but exact project ownership cannot be proven, installation fails closed. Back up/remove that file deliberately, then rerun the installer. Do not manually rename it into a current file because that would bypass ownership and content verification.

Older model-named files such as `luna-worker.toml` are removed only when exact historical project ownership proves they are safe to remove. Unproven files are treated as user-owned and left alone.

## Migration from the old public `codex-agent-team` Plugin

If the old public Plugin/marketplace registration is still installed, remove that registration first:

```bash
codex plugin remove codex-agent-team@codex-agent-team
codex plugin marketplace remove codex-agent-team
```

Then perform the current fresh install:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread. When exact roles are first needed, authorize the bounded profile migration described above.

## Managed profile safety

The bundled installer:

- uses the active Codex-home `agents` directory;
- writes only the four current profiles and `.codex-delegate-agents.json`;
- rejects symlinked Codex-home/profile/manifest destinations;
- rejects another TOML file claiming a current reserved `codex_delegate_*` role;
- refuses to overwrite a differing current profile unless previous current ownership is proven by exact hash;
- treats old `codex_agent_team_*` state as migration input only;
- removes old project-named state only when exact ownership evidence allows it;
- fails closed when a project-named old role cannot be proven safe to migrate;
- stages replacements and rolls back its managed single-process changes on failure;
- supports a strictly non-mutating `--check` mode.

It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

Concurrent same-Codex-home multi-process behavior remains a live release gate. Do not infer process-wide transactionality from single-process rollback.

## Plugin validation before release

Each release candidate must:

1. run the then-current OpenAI `plugin-creator/scripts/validate_plugin.py` against `plugins/codex-delegate` and record the validator revision;
2. verify marketplace metadata points to `./plugins/codex-delegate`;
3. perform a real fresh marketplace install and `codex plugin add codex-delegate@codex-delegate`;
4. start a new thread and confirm `/codex-delegate` discovery;
5. verify all four current `codex_delegate_*` roles after authorized provisioning;
6. exercise migration from representative 0.6.x internal state and confirm no old project role/profile/ownership generation remains after success;
7. exercise migration from a representative old public `codex-agent-team` registration;
8. verify user-modified/unproven legacy files are never silently overwritten/deleted;
9. exercise same-Codex-home installer concurrency cases owned by `HEADOFF.md`;
10. record exact runtime, revision, validator revision, commands, and outcomes in the maintainer evidence ledger.

CI uses a pinned official validator for deterministic regression protection. Release-candidate validation still reruns the then-current official validator.

## Failure behavior

If marketplace registration/update, Plugin installation, migration, official validation, profile provisioning, exactness verification, or a required review dependency fails, stop and report the actual failure. Do not patch user configuration manually to make the supported path appear successful.
