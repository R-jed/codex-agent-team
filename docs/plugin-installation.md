# Plugin Installation

codex delegate is packaged as a Codex Plugin. The repository marketplace and OpenAI's public Plugins Directory are separate distribution surfaces.

## Current distribution status

The repository contains a valid repo/local marketplace entry at `.agents/plugins/marketplace.json` and a Plugin package at `plugins/codex-delegate`.

That repository metadata is sufficient for repo marketplace installation and development testing. It does not prove that the Plugin has been submitted, approved, or published in OpenAI's universal public Plugins Directory.

Do not tell users to search for `codex-delegate` in the public directory unless a current published OpenAI listing has been independently verified.

## Current reliable installation

Register this GitHub repository as a Codex marketplace, then install the Plugin:

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

Codex CLI/IDE users can also open the Skill picker with `/skills`.

Implicit invocation is disabled, so use `$codex-delegate:codex-delegate` when you want the Plugin to orchestrate a task.

## Repo marketplace update

For an installation registered from this repository:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after an update.

`main` is the moving development channel. Evidence for a particular build applies only to the exact revision tested. A stable public release should use an immutable release ref or tag.

## Public Plugins Directory publication

OpenAI's public Plugins Directory is shared by ChatGPT and Codex. A repo/local marketplace entry does not automatically register a Plugin there.

To make codex delegate globally searchable, the publisher must complete the OpenAI Platform publication flow:

1. Use an OpenAI Platform organization with Plugin submission write access. The current Platform permission is labeled **Apps Management**.
2. Complete individual or business developer identity verification for the publishing organization.
3. Open the OpenAI Plugin submission portal and create a **Skills only** submission.
4. Complete the public listing with the Plugin name, descriptions, logo, category, website, support URL, privacy policy URL, and terms URL.
5. Upload the final Skill bundle, add realistic starter prompts, provide at least five positive and three negative test cases, choose availability, and add release notes.
6. Submit the Plugin for OpenAI review.
7. After approval, explicitly **Publish** the approved version from the portal.
8. Only after publication should documentation treat public-directory search as an ordinary installation path.

Useful current public URLs for the listing are:

```text
Website:        https://github.com/R-jed/codex-delegate
Support:        https://github.com/R-jed/codex-delegate/issues
Privacy policy: https://github.com/R-jed/codex-delegate/blob/main/PRIVACY.md
Terms:          https://github.com/R-jed/codex-delegate/blob/main/TERMS.md
```

Official publication documentation:

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/build/plugins

Repository CI, the official Plugin validator, a successful repo marketplace install, and `.agents/plugins/marketplace.json` are packaging and local-distribution evidence. None of them establish public-directory approval or publication.

## Current identity

```text
Repository:          R-jed/codex-delegate
Repo marketplace id: codex-delegate
Plugin id:           codex-delegate
Skill:               codex-delegate
Invocation:          $codex-delegate:codex-delegate
Version:             1.1.0
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

These are implementation details of the current managed role set. Users do not need to edit them manually.

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

The Plugin manifest exposes a website, privacy policy, terms of use, category, brand assets, and starter prompts. Current legal references are:

- `PRIVACY.md`
- `TERMS.md`

The Plugin remains skills-only. It does not declare MCP servers, apps, hooks, or another runtime because the current use case is fully expressed through a Skill plus native Codex custom Agents.

The public submission portal owns the actual public listing state. Repository metadata should not be treated as a substitute for that state.

## Plugin validation for a fixed release

For a fixed release candidate:

1. bind an immutable candidate SHA/ref;
2. run the repository-pinned official Plugin validator used by maintained CI;
3. run the then-current official OpenAI Plugin validator against `plugins/codex-delegate` when current compatibility evidence is required;
4. verify the Plugin remains the smallest required skills-only shape and public legal/listing metadata is valid;
5. verify repo marketplace metadata points to `./plugins/codex-delegate`;
6. perform a fresh repo marketplace install when installation behavior itself changed or needs reconfirmation;
7. confirm `$codex-delegate:codex-delegate`, `/skills`, the intended version, and explicit-only invocation when those surfaces are part of acceptance;
8. verify first-use five-role provisioning/readiness when the managed-profile lifecycle changed or needs reconfirmation;
9. verify installer idempotence, ownership protection, unrelated-profile preservation, and non-mutating `--check` when installer behavior changed;
10. separately verify the OpenAI Platform listing state before making any public-directory availability claim.

Static Plugin validation remains separate from live product behavior and public-directory publication. It cannot prove routing quality, coordination quality, recovery quality, main-session capability dedup value, Sol Solver value, Terra investigation value, onboarding quality, independent Final Review yield, OpenAI review approval, or public publication.

## Failure behavior

If repo marketplace installation, profile provisioning, validation, exactness verification, or a required review dependency fails, stop and report the actual failure. Do not patch user configuration manually to make the supported path appear successful.

If the Plugin cannot be found in the public Plugins Directory, do not infer a packaging defect from that fact alone. First distinguish public-directory publication state from repo marketplace installation state.
