# Plugin Installation

codex delegate uses the native Codex Plugin system as its only supported distribution path.

Plugin packaging and custom Agent profiles are separate Codex surfaces. The Plugin distributes the Skill and bundled project files. Exact model-specific roles are provisioned, after explicit user approval, into the active Codex-home `agents` directory. The default personal location is `~/.codex/agents`.

## Current identity

```text
Repository:       R-jed/codex-delegate
Marketplace id:  codex-delegate
Plugin id:        codex-delegate
Skill/command:   codex-delegate / /codex-delegate
Version:         0.9.0
```

Current managed Agent state:

```text
codex-delegate-reader.toml        -> codex_delegate_reader       -> GPT-5.6 Luna / max    / read-only
codex-delegate-worker.toml        -> codex_delegate_worker       -> GPT-5.6 Luna / max    / workspace-write
codex-delegate-solver.toml        -> codex_delegate_solver       -> GPT-5.6 Sol / high    / workspace-write
codex-delegate-investigator.toml  -> codex_delegate_investigator -> GPT-5.6 Terra / xhigh / read-only
codex-delegate-advisor.toml       -> codex_delegate_advisor      -> GPT-5.6 Sol / high    / read-only
.codex-delegate-agents.json       -> project ownership receipt
```

These are the only project-managed role/profile/ownership identities.

## Current pre-release install

Before v1.0.0, `main` is the development channel:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread, then invoke explicitly:

```text
/codex-delegate <task>
```

Implicit invocation is disabled.

Do not manually edit `config.toml`, marketplace state, Plugin cache state, or Agent profiles to simulate installation.

Because `main` moves during pre-release development, deterministic/live evidence applies only to the exact SHA tested. After v1.0.0 is cut, the recommended stable user-install channel should use the immutable release ref/tag validated for that release.

## Update or reinstall

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after an update.

## First-use Agent readiness

Role setup should not interrupt an implementation halfway through.

When an explicit `/codex-delegate` task actually benefits from a child, the Skill checks the required exact role before delegated code execution starts. If provisioning is needed, it:

1. explains the project-managed write scope and asks permission;
2. resolves `../../scripts/install-agents.py` relative to the installed Skill;
3. writes or verifies only the five current profiles and `.codex-delegate-agents.json` under the active Codex home;
4. runs a non-mutating `--check`;
5. re-inspects the role surface exposed by the current runtime;
6. if a fresh thread is required to discover new roles, stops before delegated writing and asks the user to restart the task in a new thread.

The installer can extend an exact proven current-generation receipt by adding a newly shipped managed profile without rewriting unchanged managed profiles. A differing profile is overwritten only when the current ownership receipt proves its exact previous bytes.

Successful file installation is configuration evidence. It does not prove the model, effort, sandbox, ancestry, or route actually observed at runtime.

## Managed profile safety

The bundled installer:

- uses the active Codex-home `agents` directory;
- writes only the five current profiles and `.codex-delegate-agents.json`;
- rejects symlinked Codex-home/profile/manifest destinations;
- rejects another TOML file claiming a current reserved `codex_delegate_*` role;
- refuses to overwrite a differing current profile unless previous ownership is proven by exact hash;
- leaves unrelated Agent profiles untouched;
- stages replacements and rolls back its managed single-process changes on failure;
- supports a strictly non-mutating `--check` mode.

It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

Concurrent same-Codex-home multi-process behavior remains a live release-validation concern until tested. Single-process rollback does not prove multi-process transactionality.

## Plugin validation before release

Each fixed release candidate must:

1. record an immutable candidate SHA/ref;
2. run the repository-pinned official Plugin validator used by maintained CI;
3. run the then-current official OpenAI Plugin validator against `plugins/codex-delegate` and record its revision;
4. verify marketplace metadata points to `./plugins/codex-delegate`;
5. perform a real fresh marketplace install from the fixed candidate;
6. start a new thread and confirm explicit `/codex-delegate` discovery and version `0.9.0`;
7. prove implicit invocation remains disabled;
8. verify first-use five-role provisioning/readiness before delegated execution;
9. verify installer idempotence, managed-profile update/addition, unrelated-profile preservation, and non-mutating `--check`;
10. exercise same-Codex-home installer concurrency cases owned by `HEADOFF.md`;
11. record exact runtime, Git revision, validator revision, commands, and outcomes in the maintainer evidence ledger.

Static Plugin validation remains separate from live product behavior. It cannot prove routing quality, main-session capability dedup value, Sol Solver value, Terra value, onboarding quality, cross-session safety, or independent Final Review yield.

## Failure behavior

If marketplace registration/update, Plugin installation, profile provisioning, validation, exactness verification, or a required review dependency fails, stop and report the actual failure. Do not patch user configuration manually to make the supported path appear successful.
