# Upgrading a pre-manifest installation

Current Codex Agent Team installs create `.codex-agent-team-install.json` under Codex home so future upgrades can distinguish package-managed files from user modifications.

Installations created before that manifest existed have no trustworthy ownership hash for a differing installed Skill. The installer therefore fails closed instead of silently replacing it.

If an upgrade reports a differing **pre-manifest Skill**:

1. review any local changes under `~/.codex/skills/codex-agent-team/`;
2. keep or back up changes you still need;
3. only when the current package may replace that legacy Skill, run:

```bash
python scripts/install.py --adopt-legacy-install
```

The flag authorizes this one migration only. A managed manifest is then written, and later upgrades return to hash-based ownership checks.

`--adopt-legacy-install` cannot be combined with `--check` because `--check` is strictly non-mutating.

Differing Agent profiles remain fail-closed unless their installed bytes are proven by an existing managed manifest to be unchanged from the previous package version. The legacy-adoption flag does not authorize overwriting a custom profile.
