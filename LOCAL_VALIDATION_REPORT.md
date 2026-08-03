# Local Validation Report

## Current reconciliation

- Report reconciled: 2026-08-03.
- Current remote `main`: `c6020db903b35f0d57677b131bf35b0580144ab9`.
- Remote branch inventory after cleanup: `origin/main` only.
- Open PROJECT P0/P1 defects currently known: none.
- Operational release posture: **HOLD FOR RELEASE / VALIDATION INCOMPLETE** while mandatory live gates remain unfinished.
- Authoritative next-step checklist: `HEADOFF.md`.

## Baseline and environment

- Initial validation date: 2026-08-02 (Asia/Shanghai).
- Initial validation revision: `1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d`.
- Accepted symlink-fix main revision: `c6020db903b35f0d57677b131bf35b0580144ab9`.
- Historical local validation branch: `local-runtime-validation`; its remote ref has since been removed after the accepted work reached `main`.
- Platform: Apple Silicon, macOS 27.0 (26A5388g).
- Python: 3.14.6.
- Git: 2.50.1.
- Codex CLI/runtime: 0.146.0.

## Branch cleanup

GitHub reported zero open pull requests and all ten original non-main branches as merged pull-request heads. Those historical remote refs were deleted. The later temporary `local-runtime-validation` ref was also deleted after its accepted work reached `main`.

Current verified remote inventory: `origin/main` only.

## Repository baseline

- Development dependencies installed in an ignored local virtual environment.
- Initial deterministic suite: 96 passed.
- Post-fix deterministic suite: 97 passed.
- Plugin manifest and marketplace manifest: valid JSON.
- Isolated managed-profile lifecycle: first install passed, `--check` passed without byte changes, and the second install was a byte-identical no-op.
- Isolated install created only four project profiles and the ownership manifest.

## Plugin installation and profile discovery

- Marketplace registration succeeded from the documented Git source and `main` ref.
- Plugin `codex-agent-team@codex-agent-team` version 0.3.0 installed successfully.
- Before profile provisioning, a fresh task correctly reported that the four custom roles were unavailable and did not substitute another role.
- Real profile provisioning wrote the four project profiles and one ownership manifest; `--check` passed. No unrelated Agent profiles existed or were changed in the tested clean environment.
- A task created before provisioning did not refresh custom-role discovery on Codex 0.146.0.
- A second fresh task discovered all four roles.
- Exact first-run consent wording still requires explicit live UX confirmation even though resulting managed file scope was correct.

## Exact role and route matrix

| Role | Spawn tested | Model | Effort | Sandbox | Parent | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `codex_agent_team_reader` | yes, `fork_turns=none` | `gpt-5.6-luna` | `max` | `read-only` | matched | local rollout, L1 |
| `codex_agent_team_worker` | discovery only | not observed | not observed | not observed | not observed | C1 |
| `codex_agent_team_investigator` | discovery only | not observed | not observed | not observed | not observed | C1 |
| `codex_agent_team_advisor` | discovery only | not observed | not observed | not observed | not observed | C1 |

The Reader returned the requested bounded probe result. `inspect-runtime.py` emitted the expected role, model, effort, sandbox, managed permission profile, runtime version, and parent id.

Native runtime attestation was not separately exposed, so the live Reader result is L1 rather than R1/R2.

## Runtime Truth adversarial matrix

- Deterministic verifier regression cases pass as part of the repository suite.
- Incomplete expected exact routes fail closed in static coverage.
- Typed route, ancestry, and permission concerns are independently represented in static coverage.
- One real Reader record passed sanitized local inspection.
- Remaining live conflict, partial-observation, native/local agreement, permission, ancestry, duplicate-rollout, and schema-drift cases are still pending where the runtime can expose the required facts.

## Contractability and user-flow simulations

Completed evidence:

- missing-profile case failed closed and avoided role substitution;
- fresh-task Reader used an explicit bounded responsibility and `fork_turns=none`.

Still pending:

- main-session-only deterministic task;
- bounded Luna Worker contract;
- ambiguous-writing stop behavior;
- judgment escape;
- prompt injection;
- Shared Evidence invalidation;
- Luna failure classification;
- Terra delta;
- selective Sol;
- real multi-step user-flow set.

## Parallelism and lifecycle stress

Not yet executed. No claim is made about:

- useful parallel read-only work;
- duplicate-inference rejection;
- one-writer live enforcement;
- fan-out consent;
- slot leakage;
- orphan cleanup;
- cancellation recovery;
- 10-cycle or 20-cycle lifecycle stress.

## Installer fault injection

### CAT-LOCAL-001: direct Codex-home endpoint symlink

- Severity: P1.
- Ownership: PROJECT.
- Pre-fix revision: `1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d`.
- Fixed main revision: `c6020db903b35f0d57677b131bf35b0580144ab9`.
- Runtime used for reproduction: Python 3.14.6 on macOS 27.0.
- Expected: a symlink supplied as the `--codex-home` endpoint is rejected before any managed target entry is created.
- Pre-fix actual: installer exited 0, resolved the link, and wrote four profiles plus the ownership manifest into the target.
- Root cause: `install()` resolved the caller-supplied Codex-home path before preserving and validating endpoint identity.
- Fix: preserve the expanded caller path, reject when that endpoint is itself a symlink, then resolve normally. Arbitrary ancestor symlinks remain supported.
- Regression: public CLI fails non-zero, emits the explicit refusal, preserves prior file state, and leaves the target with zero directory entries.
- Verification: focused regression passed; installer suite 14 passed; complete suite 97 passed; `git diff --check` passed; original filesystem reproduction exits 1 with zero target entries.
- Compatibility characterization: a non-symlink Codex-home endpoint below a symlinked ancestor still installs successfully and creates the expected managed files.
- Independent patch review final verdict: `PATCH ACCEPTED`.
- Current status: **CLOSED ON REMOTE MAIN**.

Residual pathname TOCTOU under concurrent local mutation was explicitly excluded from this focused patch threat model and is not a current blocker without new evidence.

### Remaining installer live gates

Other real filesystem fault-injection cases remain pending, including user-modified profiles, reserved-role collisions, legacy ownership cases, symlinked managed entries, unwritable directories, interrupted replacement, manifest/write failure, rollback after partial mutation, and cleanup failure.

## Review reconciliation

A secondary review claimed that `inspect-runtime.py` fails on two `session_meta` records. That reproduction used a generic review child with `fork_turns=all`; it does not match the Plugin's required exact-role `fork_turns=none` path. The real custom Reader rollout had one applicable session record and inspected successfully.

Current classification: latent schema-compatibility signal, not a confirmed Plugin defect. Reopen only if the supported exact-role path reproduces the failure.

The symlink defect received repeated adversarial review. Final consensus was PROJECT/P1, minimal endpoint-only repair, no arbitrary-ancestor ban, and no descriptor-relative filesystem rewrite in this patch. The first regression was tightened after review to prove zero target directory entries, then the patch was accepted and pushed to `main`.

## Behavioral evaluation and performance

Paired raw-prompt versus compiled-contract trials have not been run. No quality, cost, or latency advantage is currently established.

One fresh-task role probe consumed roughly 711k input tokens, mostly cached. This single diagnostic path is not representative enough for a product-cost conclusion.

## Upstream and environment observations

- Current-task role discovery did not refresh after profile provisioning on Codex 0.146.0; a fresh task did. This is now a version-scoped characterized behavior rather than an unresolved question for that build.
- A read-only task emitted system Git temporary-cache warnings. The role probe still completed. Ownership and product impact remain unclassified and non-blocking unless the behavior becomes reproducible harm.

## Current takeover status

**HOLD FOR RELEASE / VALIDATION INCOMPLETE**

This status is caused by unfinished mandatory live gates, not by a currently known open PROJECT P0/P1.

Highest-priority unfinished evidence:

1. exact live Worker, Investigator, and Advisor route characterization;
2. materially available Runtime Truth live conflict/partial cases;
3. contractability and prompt-injection simulations;
4. Shared Evidence and Luna failure-classification behavior;
5. raw-prompt versus compiled-contract paired evaluation;
6. Terra delta and selective Sol controlled pairs;
7. one-writer, fan-out, useful-parallelism, and lifecycle stress;
8. remaining installer filesystem fault injection.

Continue in the order and review checkpoints defined by `HEADOFF.md`. After each checkpoint, send the compact feedback packet from `HEADOFF.md` for external adversarial review before changing core policy or architecture.
