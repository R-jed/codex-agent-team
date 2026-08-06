# Plugin Installation

codex delegate uses the native Codex Plugin system as its only supported distribution path.

## Recommended user installation

For ordinary users, installation is intentionally simple:

1. Open the **Codex Plugin Marketplace**.
2. Search for `codex-delegate`.
3. Select **Codex Delegate** and install or enable it.
4. Start a new Codex thread and invoke the Plugin:

```text
$codex-delegate:codex-delegate <task>
```

Codex CLI/IDE users can also open the Skill picker with `/skills`.

That is the normal supported installation path. Ordinary users do not need to register the repository as another marketplace, run CLI installation commands, edit `config.toml`, or configure Agent profiles manually.

Implicit invocation is disabled, so use `$codex-delegate:codex-delegate` explicitly when you want the Plugin to orchestrate a task.

## Current identity

```text
Repository:       R-jed/codex-delegate
Marketplace id:  codex-delegate
Plugin id:        codex-delegate
Skill:            codex-delegate
Invocation:       $codex-delegate:codex-delegate
Version:          1.1.0
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
.codex-delegate-agents.lock       -> same-Codex-home installer serialization
```

The custom Agent files are an official Codex host capability. The bundled installer is a project-specific lifecycle and ownership layer around those native profiles. It does not implement another Agent runtime.

These are implementation details of the current managed role set. Ordinary users do not need to install or edit them manually.

## Manual or development installation

Use the CLI path only when you are developing the Plugin, testing a specific repository revision, troubleshooting marketplace discovery, or explicitly need a manual installation path.

`main` is the development channel for unreleased changes:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread, then invoke explicitly:

```text
$codex-delegate:codex-delegate <task>
```

Do not manually edit `config.toml`, marketplace state, Plugin cache state, or Agent profiles to simulate installation.

Because `main` can move between releases, evidence for a particular build applies only to the exact revision tested. Release validation should use the immutable release ref/tag intended for that release.

## Manual update or reinstall

For normal use, prefer the Plugin Marketplace UI. If you are deliberately using the manual/development path, the CLI update flow is:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after a manual update.

## First-use Agent readiness

Role setup should not interrupt an implementation halfway through.

When an explicit `$codex-delegate:codex-delegate` task actually benefits from a child, the Skill checks the required exact role before delegated code execution starts. If provisioning is needed, it:

1. explains the project-managed write scope and asks permission;
2. resolves `../../scripts/install-agents.py` relative to the installed Skill;
3. writes or verifies only the five current native custom Agent profiles, `.codex-delegate-agents.json`, and `.codex-delegate-agents.lock` under the active Codex home;
4. runs a non-mutating `--check`;
5. re-inspects the role surface exposed by the current runtime;
6. if a fresh thread is required to discover new roles, stops before delegated writing and asks the user to restart the task in a new thread.

The installer can extend an exact proven current-generation receipt by adding a newly shipped managed profile without rewriting unchanged managed profiles. A differing profile is overwritten only when the current ownership receipt proves its exact previous bytes.

Successful file installation is configuration evidence. It does not prove the model, effort, sandbox, ancestry, or route actually observed at runtime.

## Managed profile safety

The bundled installer:

- uses the active Codex-home `agents` directory;
- writes only the five current profiles, `.codex-delegate-agents.json`, and `.codex-delegate-agents.lock`;
- rejects symlinked Codex-home/profile/manifest destinations;
- rejects another TOML file claiming a current reserved `codex_delegate_*` role;
- refuses to overwrite a differing current profile unless previous ownership is proven by exact hash;
- leaves unrelated Agent profiles untouched;
- stages replacements and rolls back its managed single-process changes on failure;
- supports a strictly non-mutating `--check` mode.

It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

The persistent installer lock serializes installers targeting the same Codex home so one failed rollback cannot erase a successful peer.

## Public Plugin metadata

The public Plugin manifest exposes a website, privacy policy, terms of use, category, brand assets, and starter prompts. Current public legal references are:

- `PRIVACY.md`
- `TERMS.md`

The Plugin remains skills-only. It does not declare MCP servers, apps, hooks, or another runtime because the current use case is fully expressed through a Skill plus native Codex custom Agents.

## Plugin validation for a fixed release

For a fixed release candidate:

1. bind an immutable candidate SHA/ref;
2. run the repository-pinned official Plugin validator used by maintained CI;
3. run the then-current official OpenAI Plugin validator against `plugins/codex-delegate` when current compatibility evidence is required;
4. verify the Plugin remains the smallest required skills-only shape and public legal/listing metadata is valid;
5. verify marketplace metadata points to `./plugins/codex-delegate`;
6. perform a fresh Plugin Marketplace install when installation behavior itself changed or needs reconfirmation;
7. confirm `$codex-delegate:codex-delegate`, `/skills`, the intended version, and explicit-only invocation when those surfaces are part of acceptance;
8. verify first-use five-role provisioning/readiness when the managed-profile lifecycle changed or needs reconfirmation;
9. verify installer idempotence, ownership protection, unrelated-profile preservation, and non-mutating `--check` when installer behavior changed;
10. record the exact revision and validation evidence used for any release claim.

Static Plugin validation remains separate from live product behavior. It cannot prove routing quality, coordination quality, recovery quality, main-session capability dedup value, Sol Solver value, Terra investigation value, onboarding quality, or independent Final Review yield.

## Failure behavior

If Plugin Marketplace installation, manual registration/update, profile provisioning, validation, exactness verification, or a required review dependency fails, stop and report the actual failure. Do not patch user configuration manually to make the supported path appear successful.
