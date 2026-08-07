# subagents-dispatch Release Candidate Deep Review

> Review date: 2026-08-08
> Repository: `R-jed/subagents-dispatch`
> Plugin version: `2.0.0`
> Plugin layout: repository root
> Verified implementation SHA: `eca49217b516948f5fd681533af40e1186cc9486`
> Verification workflow: GitHub Actions run `31199657005`

This document replaces the earlier rolling review notes as the current release-candidate assessment. Older findings that referred to the previous nested Plugin layout, stale CI paths, the historical `v1.0.0` tag, weak Doctor profile checks, or fake legacy-lock contention tests are superseded by the current repository state.

## Current verdict

**Implementation verdict: GO.**

The reviewed implementation has no open code-level release blocker identified by this review. Formal release still has an external governance gate: `main` branch protection/ruleset has not been enabled. A clean Codex Marketplace install should also be re-smoked after this candidate is merged to `main`, because the Marketplace entry intentionally resolves `main`.

No version tag or GitHub Release is authorized by this report.

## Verified product contract

The repository is a single root-level Codex Plugin:

```text
.
├── .agents/plugins/marketplace.json
├── .codex-plugin/plugin.json
├── agent-profiles/
├── policy-contract.json
├── scripts/
└── skills/
```

The Marketplace source is a Git URL source that resolves the repository root. The previous `git-subdir` concern no longer applies after the Plugin was moved to the repository root.

User-facing commands are:

```text
/dispatch
/doctor
```

Codex may use the namespaced internal Skill identities:

```text
/subagents-dispatch:dispatch
/subagents-dispatch:doctor
```

`/skills` remains an alternate Skill picker. Public documentation must keep user commands distinct from internal namespaced identities.

## Runtime architecture assessment

The routing architecture remains release-ready and was not broadened during this closure.

`policy-contract.json` owns the five native role routes:

| Role | Model | Effort | Mutation intent |
| --- | --- | --- | --- |
| Reader | `gpt-5.6-luna` | `max` | read-only |
| Worker | `gpt-5.6-luna` | `max` | workspace-write |
| Solver | `gpt-5.6-sol` | `high` | workspace-write |
| Investigator | `gpt-5.6-terra` | `xhigh` | read-only |
| Advisor | `gpt-5.6-sol` | `high` | read-only |

The core invariants remain:

- Main owns user intent, authorization, team composition, integration, acceptance, and the final response.
- Delegation depth is one.
- Delegation must add concrete value; zero child Agents is normal.
- One canonical checkout has at most one active writing actor inside an orchestration.
- Failure does not imply a model ladder.
- `UNKNOWN` execution state remains distinct from `FAILED`.
- Child reports are claims until actual artifacts and verification support them.
- Final Review is consequence-driven and bound to the exact candidate reviewed.

No fixed Luna -> Terra -> Sol pipeline was introduced.

## Release closure results

| Area | Result | Evidence / current behavior |
| --- | --- | --- |
| Root Plugin packaging | CLOSED | Plugin manifest, Skills, profiles, scripts, and assets live at repository root |
| Marketplace source | CLOSED | root Plugin uses Git URL source; manifest syntax and official Plugin validation pass |
| CI root-path drift | CLOSED | CI validates `.codex-plugin/plugin.json`, validates `.`, and runs root `scripts/install-agents.py` |
| Local pre-push root-path drift | CLOSED | pre-push uses root paths, full pytest exit status, pinned validator, installer and Doctor smoke |
| User command surface | CLOSED | public docs use `/dispatch` and `/doctor`; internal namespaced identities remain explicit where appropriate |
| Doctor profile truth | CLOSED | Doctor reuses `install-agents.py --check`; exact failure stderr is preserved |
| Current installer lifecycle | CLOSED | collision-safe install, exact ownership receipt, exact profile verification, rollback, idempotent repeat install |
| Legacy/current cross-generation lock | CLOSED | migration acquires legacy compatibility lock before current installer lock; real process test holds the legacy OS lock |
| Legacy cleanup partial failure | CLOSED | destructive cleanup and current install are inside one rollback boundary; fault injection verifies restoration |
| Legacy snapshot drift | CLOSED | bytes are re-read before deletion; drift aborts cleanup; rollback does not overwrite external changes |
| Modified legacy ownership | CLOSED | modified profile and ownership receipt are preserved; terminal state is reported explicitly |
| Unowned/corrupt legacy state | CLOSED | ownership-unknown state is preserved and cannot authorize deletion |
| Reserved-role collision through preserved legacy file | CLOSED | only files actually scheduled for removal bypass legacy filename collision scanning |
| Windows legacy lock compatibility | CLOSED | lock file is excluded from migration payload snapshots while remaining held as the coordination primitive |
| GPT-5.6 Sol alias | CLOSED | capability dedup aliases are policy-owned; `gpt-5.6` is accepted as declared Sol-equivalent route evidence |
| Historical tag conflict | CLOSED | current GitHub tag list is empty; no tag was created or moved during this closure |
| Local development `skills-lock.json` | CLOSED | removed from release tree and ignored |
| Branch protection / ruleset | OPEN GOVERNANCE | `main` remains unprotected and should be protected before formal release |

## Legacy migration contract after closure

Migration uses a fixed lock order:

```text
.codex-delegate-agents.lock
        ↓
.subagents-dispatch-agents.lock
```

The legacy lock remains present during the compatibility period. It is a coordination primitive, not migration payload.

Mutation follows this sequence:

```text
acquire legacy lock
acquire current lock
snapshot ownership-relevant legacy data
run all current-state preflight checks
re-read removable legacy bytes
commit ownership-proven legacy cleanup
install/verify current profiles
write/verify current manifest
release current lock
release legacy lock
```

If destructive cleanup or current installation fails, snapshot-owned deletions are restored. If an external actor changes a legacy file after the snapshot, migration fails closed and does not overwrite the external change during rollback.

Terminal legacy states include preserved user/unknown state:

```text
current_with_preserved_legacy_modified
current_with_preserved_legacy_ownership_unknown
```

Doctor reports these as explicit review states and does not recommend repeatedly running migration to force deletion.

## GitHub Actions evidence

Verified implementation:

```text
SHA: eca49217b516948f5fd681533af40e1186cc9486
Run: 31199657005
Conclusion: success
```

Matrix result:

```text
Ubuntu 3.11   PASS
Ubuntu 3.12   PASS
macOS 3.11    PASS
Windows 3.11  PASS
```

Ubuntu 3.11 evidence:

```text
pytest: 163 passed
pinned official OpenAI Plugin validator: PASS
managed Agent profile install: PASS
managed Agent profile --check: PASS
repeat install/no-op lifecycle: PASS
```

Windows also completes pytest and managed-profile lifecycle successfully. Platform-specific POSIX-only tests remain skipped where their semantics are unavailable; the cross-generation legacy lock test itself runs cross-platform and uses `fcntl` on POSIX and `msvcrt` on Windows.

## Runtime evidence

A real Codex command picker was previously observed exposing `Dispatch` and `Doctor`, with `/dispatch` selection producing the host namespaced Skill prompt. That evidence establishes the user-command/internal-identity distinction used by the current docs.

The exact Codex version for that observation was not recorded, so this report does not invent one.

Because the Marketplace entry resolves `main`, perform one clean Marketplace install smoke after this candidate is merged to `main` and before creating a formal release. Record the Codex version, marketplace-add result, plugin-add/install result, and fresh-session `/dispatch` and `/doctor` presence. This is an external release verification step, not an unresolved repository implementation defect.

## Accepted non-blocking risks

`requirements-dev.txt` uses lower-bound dependency constraints rather than a fully hashed lock file. CI pins GitHub Actions by commit SHA and pins the OpenAI validator source commit, while Python development dependencies remain intentionally range-based. This is a reproducibility tradeoff, not a current correctness blocker.

The pre-push script downloads the validator from the pinned OpenAI commit over HTTPS without an additional local content hash. The immutable source commit and `curl --fail` provide the current trust boundary. A second checksum would be optional hardening.

## Release gates remaining outside the implementation

Before formal tag / GitHub Release creation:

```text
1. Merge the reviewed candidate to main without changing implementation semantics.
2. Require the resulting main SHA to pass the same four-platform GitHub Actions matrix.
3. Enable branch protection/ruleset so required CI cannot be bypassed for release candidates.
4. Run one clean Codex Marketplace install from main and verify /dispatch and /doctor in a fresh session.
5. Confirm tags/releases are still in the intended state.
6. Only create a version tag or GitHub Release after explicit user authorization.
```

If a code change is required after the verified implementation SHA, treat it as a new candidate and rerun the full evidence chain.
