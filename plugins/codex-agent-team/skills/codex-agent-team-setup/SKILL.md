---
name: codex-agent-team-setup
description: Install or verify the role-pinned custom Agent profiles required by Codex Agent Team Profile Mode after the Plugin has been installed. Use only when the user asks to set up, repair, verify, or update Codex Agent Team custom agents.
---

# Codex Agent Team Setup

Use this setup Skill only for the companion custom Agent profiles. Plugin installation provides the workflow Skills; the four role-pinned Agent TOML files live under Codex home and require this separate explicit setup step.

## Safety boundary

The user's invocation of this setup Skill authorizes writing only the four Codex Agent Team profile files and the companion ownership manifest under Codex home. Do not edit `config.toml`, other Agent profiles, repositories, credentials, apps, MCP configuration, or unrelated files.

The required roles are:

```text
luna_explorer   -> gpt-5.6-luna / max
luna_worker     -> gpt-5.6-luna / max
terra_reviewer  -> gpt-5.6-terra / xhigh
sol_judge       -> gpt-5.6-sol / high
```

## Resolve the bundled installer

Resolve paths from the directory containing this `SKILL.md`, not from the caller's working directory.

```text
skill_dir = directory containing this SKILL.md
installer = skill_dir/../../scripts/install-agents.py
```

Require Python 3.11 or newer. If the installer is missing, stop and report that the Plugin package is incomplete.

## Install or repair

Run:

```bash
python "$installer"
```

The installer must fail closed on a differing profile unless the installed bytes are proven unchanged from a previous Codex Agent Team managed install. Never replace a conflicting or user-modified profile manually and never silently rename the project roles.

After installation, run the non-mutating exactness check:

```bash
python "$installer" --check
```

Both commands must succeed before reporting Profile Mode ready.

## Completion

Report the four verified role names and the Codex home used by the installer. Then tell the user to start a new Codex task or reopen Codex so the native spawn surface can discover the profiles.

Do not claim that the current task can see newly installed custom agents until a fresh task actually exposes them.
