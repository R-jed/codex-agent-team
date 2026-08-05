# Plugin Installation

codex delegate uses the native Codex Plugin system as its only supported distribution path.

## Recommended user installation

For ordinary users, installation is intentionally simple:

1. Open the **Codex Plugin Marketplace**.
2. Search for `codex-delegate`.
3. Select **Codex Delegate** and install or enable it.
4. Start a new Codex thread and invoke the Skill:

```text
$codex-delegate <task>
```

Codex CLI/IDE users can also open the Skill picker with `/skills`.

That is the normal supported installation path. Ordinary users do not need to register the repository as another marketplace, run CLI installation commands, edit `config.toml`, or configure Agent profiles manually.

Implicit invocation is disabled, so use `$codex-delegate` explicitly when you want the Plugin to orchestrate a task.

## Current identity

```text
Repository:       R-jed/codex-delegate
Marketplace id:  codex-delegate
Plugin id:        codex-delegate
Skill:            codex-delegate
Invocation:       $codex-delegate
Version:          0.9.0
```

Plugin packaging and custom Agent profiles are separate Codex surfaces. The Plugin distributes the Skill and bundled project files. Exact model-specific roles use Codex's native custom-Agent TOML mechanism and, after explicit user approval, are provisioned into the active Codex-home `agents` directory. The default personal location is `~/.codex/agents`.

Current managed Agent state:

```text
codex-delegate-reader.toml        -> codex_delegate_reader       -> GPT-5.6 Luna / max    / read-only
codex-delegate-worker.toml        -> codex_delegate_worker       -> GPT-5.6 Luna / max    / workspace-write
codex-delegate-solver.toml        -> codex_delegate_solver       -> GPT-5.6 Sol / high    / workspace-write
codex-delegate-investigator.toml  -> codex_delegate_investigator -> GPT-5.6 Terra / xhigh / read-only
codex-delegate-advisor.toml       -> codex_delegate_advisor      -> GPT-5.6 Sol / high    / read-only
.codex-delegate-agents.json       -> project ownership receipt
```

The custom Agent files are an official Codex host capability. The bundled installer is a project-specific lifecycle and ownership layer around those native profiles. It does not implement another Agent runtime.

These are implementation details of the current managed role set. Ordinary users do not need to install or edit them manually.

## Manual or development installation

Use the CLI path only when you are developing the Plugin, testing a specific repository revision, troubleshooting marketplace discovery, or explicitly need a manual installation path.

Before v1.0.0, `main` is the development channel:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread, then invoke explicitly:

```text
$codex-delegate <task>
```

Do not manually edit `config.toml`, marketplace state, Plugin cache state, or Agent profiles to simulate installation.

Because `main` moves during pre-release development, deterministic/live evidence applies only to the exact SHA tested. After v1.0.0 is cut, release validation should use the immutable release ref/tag validated for that release.

## Manual update or reinstall

For normal use, prefer the Plugin Marketplace UI. If you are deliberately using the manual/development path, the CLI update flow is:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after a manual update.

## First-use Agent readiness

Role setup should not interrupt an implementation halfway through.

When an explicit `$codex-delegate` task actually benefits from a child, the Skill checks the required exact role before delegated code execution starts. If provisioning is needed, it:

1. explains the project-managed write scope and asks permission;
2. resolves `../../scripts/install-agents.py` relative to the installed Skill;
3. writes or verifies only the five current native custom Agent profiles and `.codex-delegate-agents.json` under the active Codex home;
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

## Public Plugin metadata

The public Plugin manifest exposes a website, privacy policy, terms of use, category, brand assets, and starter prompts. Current public legal references are:

- `PRIVACY.md`
- `TERMS.md`

The Plugin remains skills-only. It does not declare MCP servers, apps, hooks, or another runtime because the current use case is fully expressed through a Skill plus native Codex custom Agents.

## Plugin validation before release

Each fixed release candidate must:

1. record an immutable candidate SHA/ref;
2. run the repository-pinned official Plugin validator used by maintained CI;
3. run the then-current official OpenAI Plugin validator against `plugins/codex-delegate` and record its revision;
4. verify the Plugin remains the smallest required skills-only shape and public legal/listing metadata is valid;
5. verify marketplace metadata points to `./plugins/codex-delegate`;
6. perform a real fresh Plugin Marketplace install from the fixed candidate;
7. start a new thread and confirm `$codex-delegate` discovery, `/skills` discovery, version `0.9.0`, and implicit invocation disabled;
8. verify first-use five-role provisioning/readiness before delegated execution;
9. verify installer idempotence, managed-profile update/addition, unrelated-profile preservation, and non-mutating `--check`;
10. exercise same-Codex-home installer concurrency cases owned by `HEADOFF.md`;
11. record exact runtime, Git revision, validator revision, commands, and outcomes in the maintainer evidence ledger.

Static Plugin validation remains separate from live product behavior. It cannot prove routing quality, main-session capability dedup value, Sol Solver value, Terra investigation value, onboarding quality, cross-session safety, or independent Final Review yield.

## Failure behavior

If Plugin Marketplace installation, manual registration/update, profile provisioning, validation, exactness verification, or a required review dependency fails, stop and report the actual failure. Do not patch user configuration manually to make the supported path appear successful.
