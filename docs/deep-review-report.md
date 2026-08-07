# subagents-dispatch Release Candidate Deep Review

> Review date: 2026-08-08  
> Plugin version: `2.0.0`  
> Verified implementation baseline: `2d60ec3785691b6cb0e9bc7e9157393d4bc5fe0f`  
> Implementation evidence run: GitHub Actions `31200620004`  
> Scope: packaging, routing policy, Agent profiles, installation, legacy migration, Doctor, runtime evidence, tests, CI, documentation, security and release governance.

This report is the current release-candidate assessment. Earlier rolling review notes and findings tied to the removed nested Plugin layout are superseded.

## Verdict

**Code and policy verdict: GO.**

No open code-level release blocker was identified after the final adversarial closure. Formal release remains on HOLD until repository governance and external host smoke evidence are completed:

```text
main branch protection/ruleset
clean Codex Marketplace install/update smoke on the final main candidate
explicit user authorization for any version tag or GitHub Release
```

This report does not authorize creating, moving, or deleting a tag and does not authorize creating a GitHub Release.

## Current architecture

The repository is a single root-level Codex Plugin:

```text
.
├── .agents/plugins/marketplace.json
├── .codex-plugin/plugin.json
├── agent-profiles/
├── assets/
├── policy-contract.json
├── scripts/
├── skills/
├── docs/
├── evals/
└── tests/
```

Marketplace uses a Git URL source because the Plugin manifest is at repository root. The previous `git-subdir` concern no longer applies.

User commands are:

```text
/dispatch
/doctor
```

Plugin/host metadata may use the internal namespaced identities:

```text
/subagents-dispatch:dispatch
/subagents-dispatch:doctor
```

`/skills` remains an alternate Skill picker.

## Native optimized routing contract

`policy-contract.json` owns the machine-readable native role routes and capability-dedup constants.

| Role | Model | Effort | Mutation intent |
| --- | --- | --- | --- |
| Reader | `gpt-5.6-luna` | `max` | read-only |
| Worker | `gpt-5.6-luna` | `max` | workspace-write |
| Solver | `gpt-5.6-sol` | `high` | workspace-write |
| Investigator | `gpt-5.6-terra` | `xhigh` | read-only |
| Advisor | `gpt-5.6-sol` | `high` | read-only |

Capability dedup also owns the accepted Sol-equivalent runtime alias:

```text
gpt-5.6-sol
alias: gpt-5.6
reference effort: high
```

`runtime-evidence.py` reads this alias from the policy contract. It no longer hardcodes a special `gpt-5.6` branch in the verifier.

Stable runtime invariants remain coherent:

- Main owns user intent, authorization, team composition, integration, acceptance and final response.
- Delegation depth is one.
- Zero child Agents is normal; fan-out must add concrete value.
- Each child has one distinct responsibility.
- One canonical checkout has at most one active writer inside the orchestration.
- Failure does not imply a model escalation ladder.
- `UNKNOWN` is distinct from `FAILED`.
- Child completion claims require artifact/evidence verification.
- Final Review is consequence-driven and bound to the exact candidate.

There is no fixed Luna -> Terra -> Sol pipeline.

## Release closure findings

| Area | Status | Evidence / disposition |
| --- | --- | --- |
| Root Plugin packaging | CLOSED | CI validates root `.codex-plugin/plugin.json`; official OpenAI validator passes against `.`. |
| Marketplace source | CLOSED | Plugin is at repo root, so the current `url` source matches the root Plugin layout. |
| User command surface | CLOSED | Public docs use `/dispatch` and `/doctor`; namespaced identities remain internal metadata. |
| Current profile install/upgrade | CLOSED | Exact shipped bytes, ownership manifest, collision checks, symlink refusal, staged writes and rollback are enforced. |
| Doctor profile truth | CLOSED | Doctor reuses `install-agents.py --check`; no weaker second managed-profile validator remains. |
| Legacy/current mutual exclusion | CLOSED | Migration acquires the legacy OS lock before the current installer lock; a real process test holds the old lock. |
| Legacy migration transaction | CLOSED | Preflight precedes cleanup; snapshot drift is checked; cleanup self-rolls back; later current-install failure restores legacy state. |
| Modified/unowned legacy state | CLOSED | User-modified and unowned files are preserved with ownership evidence and stable terminal states. |
| Corrupt/missing legacy ownership | CLOSED | Automatic migration fails closed when ownership cannot be proven. |
| Reserved-role collision | CLOSED | Only ownership-proven removable files bypass collision preflight. |
| Windows lock compatibility | CLOSED | Legacy lock remains a coordination primitive and is excluded from migration payload snapshots. |
| Runtime Sol alias | CLOSED | Alias semantics are policy-owned and regression-tested. |
| Local pre-push gate | CLOSED | Root-aware, strict exit semantics, full pytest, official validator, installer and Doctor lifecycle. |
| Development dependency drift | CLOSED | Verification dependencies are pinned in `requirements-dev.txt`. |
| Stale local skill lock | CLOSED | `skills-lock.json` is excluded from the release tree. |
| Historical tag conflict | CLOSED | Current tag list is empty and no GitHub Release exists. |
| Branch protection | OPEN GOVERNANCE | `main` remains unprotected; this is a repository-setting gate, not a code defect. |

## Legacy migration acceptance

Migration uses deterministic cross-generation lock ordering:

```text
.codex-delegate-agents.lock
        ↓
.subagents-dispatch-agents.lock
```

The legacy lock remains present during the compatibility period. It is coordination state and is never treated as migration payload.

Safety-focused tests cover:

- a real old-generation OS lock holder versus the new migrator;
- clean migration and idempotent rerun;
- modification after the legacy ownership hash was recorded;
- unowned legacy profile preservation;
- corrupt or missing ownership manifest;
- reserved current-role collision from a preserved legacy profile;
- symlinked legacy manifest;
- snapshot drift before deletion;
- injected partial cleanup failure with restoration;
- injected current-install failure after cleanup with legacy restoration.

Automatic migration fails closed when ownership is unknown. Preserved user state is reported as a terminal state and is not repeatedly auto-migrated in an attempt to force deletion.

## Verified CI evidence

Implementation baseline:

```text
SHA: 2d60ec3785691b6cb0e9bc7e9157393d4bc5fe0f
Run: 31200620004
Conclusion: success
```

Matrix:

```text
Ubuntu Python 3.11  PASS
Ubuntu Python 3.12  PASS
macOS Python 3.11   PASS
Windows Python 3.11 PASS
```

The run verifies:

```text
root manifest JSON validation
Marketplace JSON validation
pinned official OpenAI Plugin validator
full pytest suite
managed Agent profile install
managed Agent profile --check
Doctor --check
idempotent reinstall lifecycle
```

The predecessor `main` candidate `5079a285797c3f44c9801afc9ec9789b6451969c` also passed the same four-platform workflow in run `31196628767`, with `163 passed` on Ubuntu Python 3.11. The final implementation change only moved the already-supported `gpt-5.6` Sol alias from verifier-specific code into `policy-contract.json` and expanded the corresponding regression contract.

This report itself is documentation-only. The final `main` SHA containing this report must also pass the repository workflow before it is treated as the release candidate.

## Runtime evidence still external

Existing real Codex UI evidence confirms that an installed Plugin exposes Dispatch and Doctor in the command picker and that `/dispatch` selection produces the host namespaced Skill prompt. The exact Codex version for that earlier observation was not recorded.

A clean installation of the final candidate through a fresh Codex Marketplace instance cannot be proven from repository CI. Record this separately before formal release:

```text
Codex version
marketplace add/install result
plugin add result
fresh session
Dispatch present
Doctor present
/dispatch selection result
/doctor selection result
```

Until that is run against the final candidate, this specific clean-install evidence remains `UNKNOWN`, not `PASS`.

## Release governance

Current repository governance still requires branch protection/ruleset configuration for `main`, with the complete `policy-tests` workflow required for release candidates.

No tag or GitHub Release was created during this closure.

Before formal release:

```text
1. Confirm the final main SHA is green on all four CI jobs.
2. Enable main branch protection/ruleset with required CI.
3. Run one clean Codex Marketplace install/update smoke on the final main candidate.
4. Re-check tags and GitHub Releases.
5. Create a version tag or GitHub Release only after explicit user authorization.
```

Any implementation change after the verified baseline creates a new candidate and requires the complete evidence chain again.
