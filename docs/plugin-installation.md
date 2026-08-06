# Plugin Installation

codex delegate supports two installation methods. Choose either the Codex Plugin Marketplace or the command line.

## Option 1: Codex Plugin Marketplace

In the ChatGPT desktop app:

1. Switch to **Codex**.
2. Open **Plugins**.
3. Search for `codex-delegate`.
4. Open **Codex Delegate** and select `+` to install it.
5. Start a new Codex session after installation.

Codex CLI users can also enter `/plugins` to open the plugin browser, search for `codex-delegate`, and install it there.

## Option 2: Command-line installation

Copy and run:

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

After installation, start a new Codex session and invoke:

```text
$codex-delegate:codex-delegate <task>
```

You can also use `/skills` to open the Codex Skill picker.

## Update

### Plugin Marketplace

Open **Plugins**, find **Codex Delegate** in your installed plugins, and apply the available update. Start a new Codex session after updating.

### Command line

Copy and run:

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex session after updating.
