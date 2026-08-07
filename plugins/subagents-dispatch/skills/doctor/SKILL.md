---
name: doctor
description: Diagnose subagents-dispatch installation, Codex host and marketplace state, and managed Agent profiles; repair managed profiles or upgrade the Plugin only when the user explicitly asks for mutation.
---

# doctor

Use this Skill to diagnose subagents-dispatch installation and configuration, repair its managed Agent profiles, or upgrade the Plugin.

This Skill is operational maintenance for subagents-dispatch. It does not route development work, create a Subagent team, or redefine the runtime policy owned by `/subagents-dispatch:dispatch`.

## Safety model

Diagnosis is read-only by default.

Do not mutate Plugin, marketplace, Codex configuration, or Agent profile state unless the user explicitly asks to install, repair, or upgrade. Never edit Codex config files directly when the supported Codex CLI can perform the operation. Never remove a marketplace as a routine repair step.

Treat command output as evidence. Do not claim a component is installed, enabled, current, or healthy without checking it.

## Canonical identities

```text
marketplace: subagents-dispatch
plugin:      subagents-dispatch@subagents-dispatch
main skill:  /subagents-dispatch:dispatch
doctor:      /subagents-dispatch:doctor
```

The bundled managed-profile installer is:

```text
installer = skill_dir/../../scripts/install-agents.py
```

## 1. Diagnose

Run the smallest useful set of checks. Prefer structured JSON output where Codex exposes it.

### Host

```bash
codex --version
codex doctor --json
```

If `codex doctor --json` is unavailable on the installed Codex build, report that limitation and continue with the Plugin-specific checks below. Do not treat the missing host-doctor command as proof that subagents-dispatch is broken.

### Marketplace and Plugin inventory

```bash
codex plugin marketplace list --json
codex plugin list --available --json
```

Check for the canonical marketplace and Plugin identities above. Distinguish these states when the evidence allows it:

```text
marketplace unavailable
plugin unavailable
plugin available but not installed
plugin installed
plugin installed but disabled
update available
state cannot be established from current evidence
```

Do not infer Marketplace health from the Codex Plugins UI alone when CLI inventory is available.

### Managed Agent profiles

Run the existing deterministic verifier rather than recreating its profile logic:

```bash
python "$installer" --check
```

A passing check proves the five subagents-dispatch managed Agent profiles and their ownership receipt match the currently running Plugin package. A failing check is diagnostic evidence; preserve the exact failure reason.

### Package-local facts

When useful, inspect the installed Plugin package that contains this Skill:

```text
skill_dir/../../.codex-plugin/plugin.json
skill_dir/../../policy-contract.json
```

Use those files for the running package version and shipped role contract. Do not guess the version from README text.

## 2. Report

Give a compact status report with these categories when relevant:

```text
Codex host
Marketplace
Plugin
Managed Agent profiles
Recommended action
```

Use `OK`, `WARN`, `FAIL`, or `UNKNOWN` only when supported by collected evidence. Keep `UNKNOWN` distinct from `FAIL`.

If everything required is healthy, say so and stop. Do not mutate a healthy installation.

## 3. Repair managed Agent profiles

Only when the user explicitly asks to repair or install the managed profiles, run the existing installer:

```bash
python "$installer"
python "$installer" --check
```

The installer owns collision detection, one-process locking, ownership receipts, safe upgrades, rollback, and exact profile verification. Do not bypass it by copying TOML files manually.

If the current Codex session still cannot discover a required custom Agent role after a successful repair, ask the user to start a fresh Codex session before testing the role surface again.

## 4. Install the Plugin from the command line

Only when installation is explicitly requested and the Plugin is not already installed, use the canonical commands:

```bash
codex plugin marketplace add R-jed/subagents-dispatch@main \
  --sparse .agents/plugins \
  --sparse plugins/subagents-dispatch && \
codex plugin add subagents-dispatch@subagents-dispatch
```

After installation, start a fresh Codex session and run this Doctor again. The fresh invocation uses the installed package that Codex actually selected.

## 5. Upgrade the Plugin

Upgrade only when the user explicitly asks for an upgrade. First report the current package version and any available-version evidence from the Plugin inventory.

Use the canonical update path:

```bash
codex plugin marketplace upgrade subagents-dispatch && \
codex plugin add subagents-dispatch@subagents-dispatch
```

Do not continue by running the old package's installer as if it were the upgraded package. After a successful Plugin upgrade:

1. ask the user to start a fresh Codex session;
2. invoke `/subagents-dispatch:doctor` again;
3. let the new Doctor run `python "$installer" --check` against the newly selected package;
4. if the new package reports stale managed profiles, repair them through its own installer and verify again.

This prevents an older running Skill from overwriting newer Agent profile templates.

## 6. Failure handling

If a supported Codex CLI command fails, preserve the command, exit status when available, and concise stderr. Diagnose from that evidence before proposing mutation.

Do not delete caches, marketplaces, Plugin state, Agent profiles, or Codex configuration speculatively. Do not use `marketplace remove` as a generic reset. Prefer the smallest supported repair that addresses the evidenced failure.

If the Plugin inventory and filesystem/package evidence disagree, report the disagreement as `UNKNOWN` or `WARN` and ask for a fresh Codex session before destructive action.
