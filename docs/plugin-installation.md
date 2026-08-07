# Plugin Installation

Install the Marketplace source and Plugin:

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

After installation, start a new Codex session.

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
