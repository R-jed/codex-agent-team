# Release Candidate Final Checklist

Use this checklist only after code changes are complete. `docs/deep-review-report.md` is the current review record.

## Canonical product facts

```text
Repository:          R-jed/subagents-dispatch
Plugin directory:    .
Plugin manifest:     .codex-plugin/plugin.json
Marketplace:         .agents/plugins/marketplace.json
Plugin version:      2.0.0
User command:        /dispatch
Doctor command:      /doctor
Internal identities: /subagents-dispatch:dispatch
                     /subagents-dispatch:doctor
```

The Plugin is rooted at the repository root. Do not reintroduce `plugins/subagents-dispatch/` paths or `git-subdir` packaging assumptions unless the repository layout changes again.

Current command-line install contract:

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Current update contract:

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

## Required automated evidence

The final candidate SHA must pass the repository workflow without content changes afterward:

```text
Ubuntu Python 3.11 PASS
Ubuntu Python 3.12 PASS
macOS Python 3.11 PASS
Windows Python 3.11 PASS
full pytest PASS
pinned official OpenAI Plugin validator PASS
managed profile install/check PASS
Doctor --check PASS
idempotent reinstall PASS
```

Run the strict local gate when available:

```bash
./scripts/pre-push-ci.sh
```

Do not ignore, regex-away, or reinterpret a non-zero test/validator result.

## Legacy migration acceptance

The current migration contract must keep these properties:

```text
lock order: legacy lock -> current lock
legacy lock file is preserved
unknown ownership fails closed
modified/unowned legacy files are preserved
legacy manifest is retained when preserved files still need ownership evidence
preserved legacy state is terminal and does not loop automatic migration
all current preflight happens before destructive legacy cleanup
cleanup detects snapshot drift
partial cleanup failure restores earlier deletions
current-install failure after cleanup restores legacy state
preserved files still participate in reserved-role collision checks
```

Safety-critical tests must include a real second process that actually holds `.codex-delegate-agents.lock`. Merely creating the lock file is not contention evidence.

## Doctor acceptance

`install-agents.py --check` is the only managed-profile exact-health verifier. Doctor may interpret and report its result, but must not maintain a second weaker validator.

Legacy states must remain distinguishable:

```text
legacy_only
mixed
legacy_ownership_unknown
current_with_preserved_legacy
current_with_preserved_legacy_modified
current_with_preserved_legacy_ownership_unknown
migration_complete
```

When ownership is unknown or user state was intentionally preserved, report the state and stop automatic migration. Mutation requires explicit user intent.

## Runtime evidence acceptance

Keep requested, accepted, and observed route facts separate. Missing runtime telemetry stays missing. The official `gpt-5.6` alias may satisfy the Sol model identity check because it routes to `gpt-5.6-sol`; Luna and Terra must not be mistaken for that alias.

## Manual host evidence

Before a formal tag/Release, record a clean Codex install or update against the final candidate:

```text
codex version
marketplace add/upgrade result
plugin add result
fresh-session result
Dispatch/Doctor command picker presence
/dispatch invocation result
/doctor invocation result
```

If this cannot be executed, record `UNKNOWN`. Do not promote JSON validity into an end-to-end install claim.

## Repository governance

Before formal release:

1. enable branch protection or a ruleset for `main`;
2. require the full `policy-tests` workflow;
3. confirm tags and GitHub Releases are still in the intended state;
4. merge/freeze one candidate SHA;
5. verify the full workflow on that exact `main` SHA.

Do not create, move, or delete version tags and do not create a GitHub Release unless the user explicitly requests the release action after these gates are satisfied.

## Final decision format

```text
Final main SHA: <sha>
Plugin version: 2.0.0
CI run: <id>
Matrix: PASS | FAIL
Tests: <exact result>
Official validator: PASS | FAIL
Managed profile lifecycle: PASS | FAIL
Legacy migration acceptance: PASS | FAIL
Marketplace clean install: PASS | UNKNOWN | FAIL
/dispatch: PASS | UNKNOWN | FAIL
/doctor: PASS | UNKNOWN | FAIL
Branch protection: PASS | FAIL
Tags/Releases: <state>
Verdict: GO | HOLD
```

A release `GO` requires no unresolved blocker. `UNKNOWN` host evidence must remain visible and be judged explicitly rather than silently converted to PASS.
