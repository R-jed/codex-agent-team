# Plugin Installation

## Plugin Marketplace

Open **Plugins** in Codex, or enter `/plugins` in Codex CLI. Search for `subagents-dispatch`, install it, then start a new Codex session.

## Command line

Copy and run:

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

After installation, start a new Codex session and invoke:

```text
/dispatch <task>
```

Use `/doctor` for installation, configuration, Marketplace, and managed Agent profile diagnostics. You can also use `/skills` to open the Codex Skill picker.

## Update

Plugin Marketplace users update **subagents-dispatch** from the installed plugins area.

Command-line users run:

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after updating. If the installation originated from the legacy `codex-delegate` plugin, run `/doctor` in the fresh session so it can detect legacy state before any migration or profile repair.
