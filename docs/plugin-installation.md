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

These are the only project-managed role/profile/ownership identities.

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

## First-run custom Agent provisioning

The main Skill checks role readiness only after a responsibility justifies model-specific delegation. When an exact role is unavailable, `/codex-delegate`:

1. explains the exact project-managed write scope and asks permission;
2. resolves `../../scripts/install-agents.py` relative to the installed Skill;
3. writes or verifies only the four current profiles and `.codex-delegate-agents.json` under the active Codex home;
4. runs a non-mutating `--check` after installation;
5. re-inspects native role discovery;
6. asks for a fresh Codex task if the current task still cannot see the new roles.

Successful file installation is configuration evidence. It does not prove the route/model/effort/sandbox actually observed for a spawned child.

## Managed profile safety

The bundled installer:

- uses the active Codex-home `agents` directory;
- writes only the four current profiles and `.codex-delegate-agents.json`;
- rejects symlinked Codex-home/profile/manifest destinations;
- rejects another TOML file claiming a current reserved `codex_delegate_*` role;
- refuses to overwrite a differing current profile unless previous current ownership is proven by exact hash;
- leaves unrelated Agent profiles untouched;
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
6. verify installer idempotence, current-profile update behavior, unrelated-profile preservation, and non-mutating `--check`;
7. exercise same-Codex-home installer concurrency cases owned by `HEADOFF.md`;
8. record exact runtime, revision, validator revision, commands, and outcomes in the maintainer evidence ledger.

CI uses a pinned official validator for deterministic regression protection. Release-candidate validation still reruns the then-current official validator.

## Failure behavior

If marketplace registration/update, Plugin installation, official validation, profile provisioning, exactness verification, or a required review dependency fails, stop and report the actual failure. Do not patch user configuration manually to make the supported path appear successful.
