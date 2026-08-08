# Plugin Installation

Install the Marketplace source and Plugin:

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

After installation, start a new Codex session.

## First delegated run

The Plugin package and its five managed custom-Agent profiles have separate local lifecycle state. On the first `/dispatch` task that actually needs a child, Dispatch checks those five profiles before delegated execution. If they are missing, it explains the local files it manages and asks permission before running the bundled installer and `--check`.

Some Codex builds may require another fresh Codex session before newly installed profiles become visible. When that happens, Dispatch stops before delegated writing and asks you to continue the task in the fresh session.

Normal development work:

```text
/dispatch <task>
```

Optional 2.1 controls use the same Skill:

```text
/dispatch preview <task>
/dispatch status
/dispatch steer <unit_id>: <guidance>
/dispatch takeover <unit_id>
```

Use `/doctor` for installation, configuration, managed-profile, and upgrade diagnostics. You can also use `/skills` to open the Codex Skill picker.

## Update

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after updating.

Doctor can perform the supported upgrade flow when explicitly requested:

```text
/doctor Upgrade subagents-dispatch and tell me what remains afterward.
```
