# subagents-dispatch Release Candidate Deep Review

> Review date: 2026-08-07  
> Plugin version: `2.0.0`  
> Reviewed code baseline: `196bf862fea35f4e054d46f546c03e91e05c7d4d`  
> Evidence run: GitHub Actions `31196076765`  
> Scope: packaging, routing policy, Agent profiles, installation, legacy migration, Doctor, runtime evidence, tests, CI, documentation, security and release governance.

This report replaces the earlier rolling review notes. Historical findings that were superseded by later repository changes are not release truth.

## Current architecture

The repository is a single Plugin rooted at `.`:

```text
.codex-plugin/
.agents/plugins/
agent-profiles/
assets/
policy-contract.json
scripts/
skills/
docs/
evals/
tests/
```

Marketplace uses a Git URL source because the Plugin manifest is at repository root. User commands are `/dispatch` and `/doctor`; Plugin/host metadata may use the internal namespaced identities `/subagents-dispatch:dispatch` and `/subagents-dispatch:doctor`.

`policy-contract.json` is the machine source for the five native role routes and hard delegation limits. `skills/dispatch/SKILL.md` owns the control loop. Router, TeamPlan, recovery, guardrails and Final Review remain separated by responsibility rather than duplicated into another orchestration runtime.

## Release findings

| Area | Status | Evidence / disposition |
| --- | --- | --- |
| Root Plugin packaging | CLOSED | CI validates root `.codex-plugin/plugin.json`; official OpenAI validator passes against `.`. |
| Marketplace source | CLOSED | Plugin is at repo root, so current `url` source matches the root-Plugin layout. |
| User command surface | CLOSED | Public docs use `/dispatch` and `/doctor`; namespaced identities remain internal metadata. Real Codex UI evidence supplied during review showed Dispatch and Doctor in the command picker. |
| Current profile install/upgrade | CLOSED | Exact shipped profile bytes, manifest ownership, collision checks, symlink refusal, staged writes and rollback remain enforced by `scripts/install-agents.py`. |
| Doctor profile truth | CLOSED | Doctor reuses `install-agents.py --check`; it does not maintain a weaker second managed-profile validator. |
| Legacy/current mutual exclusion | CLOSED | Migration acquires the legacy OS lock before the current installer lock. A real second process holds `.codex-delegate-agents.lock` in the cross-generation contention test. |
| Legacy migration transaction | CLOSED | Preflight precedes destructive cleanup. Cleanup verifies snapshot drift, restores earlier deletions when cleanup itself fails, and restores legacy state if current installation subsequently fails. |
| Modified/unowned legacy state | CLOSED | Modified or unowned files are preserved with ownership evidence and produce terminal `current_with_preserved_legacy*` states instead of an infinite migration loop. |
| Corrupt/missing legacy ownership | CLOSED | Automatic migration fails closed when ownership metadata is invalid, unsafe or missing while legacy profiles remain. |
| Reserved-role collision | CLOSED | Only files proven removable are excluded from collision preflight; preserved legacy files cannot silently duplicate a current reserved Agent role. |
| Windows lock compatibility | CLOSED | Legacy lock is a coordination primitive and is never snapshotted or deleted. Windows CI exercises the migration/lock path successfully. |
| Runtime Sol alias | CLOSED | Runtime evidence recognizes the official `gpt-5.6` alias as Sol capability without treating Luna/Terra names as aliases. |
| Local pre-push gate | CLOSED | Root-aware, strict exit semantics, full pytest, official validator and installer/Doctor lifecycle. No ignored core tests or swallowed pytest exit code. |
| Development dependency drift | CLOSED | Verification dependencies are pinned in `requirements-dev.txt`. |
| Stale local skill lock | CLOSED | `skills-lock.json` is excluded from the release tree. |
| Historical tag conflict | CLOSED | Current repository tag list is empty; no GitHub Release exists. |
| Branch protection | OPEN GOVERNANCE | `main` remains unprotected. This repository-setting action is intentionally separate from code correctness and must be enabled before formal release. |

## CI evidence for reviewed code baseline

GitHub Actions run `31196076765` completed successfully for `196bf862fea35f4e054d46f546c03e91e05c7d4d`.

```text
Ubuntu 24.04 / Python 3.11   PASS
Ubuntu 24.04 / Python 3.12   PASS
macOS / Python 3.11          PASS
Windows / Python 3.11        PASS

Full pytest on Ubuntu 3.11   163 passed
Official OpenAI validator    PASS
Managed profile install      PASS
Managed profile --check      PASS
Doctor --check               PASS
Idempotent reinstall         PASS
```

The Windows job also completed the full test suite and managed-profile lifecycle, which is material because legacy lock semantics differ between `fcntl` and `msvcrt`.

## Adversarial migration acceptance

The safety-focused suite covers the failure modes that matter to persistent user state:

- real OS-level old-lock holder versus new migrator;
- clean migration and idempotent rerun;
- user modification after the legacy manifest recorded the original hash;
- unowned legacy profile preservation;
- corrupt or missing ownership manifest;
- reserved current-role collision from a preserved legacy profile;
- symlinked legacy manifest;
- snapshot drift between planning and deletion;
- injected partial-cleanup failure with restoration;
- injected current-install failure after legacy cleanup with legacy restoration.

The migration contract is fail-closed where ownership cannot be proven. Preserved user state is reported as a terminal warning state, not silently removed and not repeatedly auto-migrated.

## Runtime and product-policy review

No release-blocking defect was found in the core Dispatch policy during the final review. Stable invariants remain coherent:

- Main owns user intent, authorization, integration, acceptance and final response.
- Delegation depth is one.
- Zero child Agents is normal; fan-out must add concrete value.
- Each child has one distinct responsibility.
- One canonical checkout has at most one active writer inside the orchestration.
- Failure does not imply a model escalation ladder.
- `UNKNOWN` is distinct from `FAILED`.
- Child completion claims require artifact/evidence verification.
- Final Review is consequence-driven and bound to the exact candidate.

Luna Reader/Worker, Sol Solver/Advisor and Terra Investigator remain the native optimized role routes for the current product contract.

## Evidence that remains external

A clean install of this exact candidate through a fresh local Codex Marketplace instance was not executable from the review environment, so that specific end-to-end step remains `UNKNOWN`, not `PASS`. Existing real Codex UI evidence confirms the installed product exposes `/dispatch` and `/doctor`, but it is not a clean-install proof for this exact SHA.

Before a formal tag/Release, perform one clean Codex install/update smoke against the final `main` candidate and record the result. Do not infer this from JSON validity alone.

## Release governance

No tag or GitHub Release was created during this closure.

The remaining repository-level governance action is branch protection/ruleset configuration for `main`, with the full `policy-tests` workflow required before release changes are accepted. After this report-only documentation update is merged, rerun CI on the final `main` SHA because release evidence must match the final tree.

## Verdict

**Code and policy verdict: GO for Release Candidate merge to `main`.**

**Formal release verdict: HOLD until the final `main` SHA is green, `main` protection is enabled, and the clean Codex Marketplace install smoke is recorded.**

There are no known open code-level release blockers in the reviewed baseline. Do not create a tag or GitHub Release from an unverified or unprotected `main` state.
