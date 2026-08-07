# Plugin Installation

subagents-dispatch supports two installation methods. Choose either the Codex Plugin Marketplace or the command line.

## Option 1: Codex Plugin Marketplace

In the ChatGPT desktop app:

1. Switch to **Codex**.
2. Open **Plugins**.
3. Search for `subagents-dispatch`.
4. Open **subagents-dispatch** and select `+` to install it.
5. Start a new Codex session after installation.

Codex CLI users can also enter `/plugins` to open the plugin browser, search for `subagents-dispatch`, and install it there.

## Option 2: Command-line installation

Copy and run:

```bash
codex plugin marketplace add R-jed/subagents-dispatch@main \
  --sparse .agents/plugins \
  --sparse plugins/subagents-dispatch && \
codex plugin add subagents-dispatch@subagents-dispatch
```

After installation, start a new Codex session and invoke:

```text
/subagents-dispatch:dispatch <task>
```

You can also use `/skills` to open the Codex Skill picker.

## Update

### Plugin Marketplace

Open **Plugins**, find **subagents-dispatch** in your installed plugins, and apply the available update. Start a new Codex session after updating.

### Command line

Copy and run:

```bash
codex plugin marketplace upgrade subagents-dispatch && \
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after updating.
