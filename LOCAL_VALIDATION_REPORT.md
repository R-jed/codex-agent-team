# Local Validation Report

## Baseline and environment

- Validation date: 2026-08-02 (Asia/Shanghai)
- Repository revision: `1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d`
- Validation branch: `local-runtime-validation`
- Platform: Apple Silicon, macOS 27.0 (26A5388g)
- Python: 3.14.6
- Git: 2.50.1
- Codex CLI/runtime: 0.146.0

## Branch cleanup

GitHub reported zero open pull requests and all ten named non-main branches as merged pull-request heads. The ten historical remote refs were deleted and the final remote inventory is `origin/main` only.

## Repository baseline

- Development dependencies installed in an ignored local virtual environment.
- Initial deterministic suite: 96 passed. Post-fix deterministic suite: 97 passed.
- Plugin manifest and marketplace manifest: valid JSON.
- Isolated managed-profile lifecycle: first install passed, `--check` passed without byte changes, and the second install was a byte-identical no-op.
- Isolated install created only four project profiles and the ownership manifest.

## Plugin installation and profile discovery

- Marketplace registration succeeded from the documented Git source and `main` ref.
- Plugin `codex-agent-team@codex-agent-team` version 0.3.0 installed successfully.
- Before profile provisioning, a fresh task correctly reported that the four custom roles were unavailable and did not substitute another role.
- Real profile provisioning wrote the four project profiles and one ownership manifest; `--check` passed. No unrelated Agent profiles existed or were changed.
- A second fresh task discovered all four roles.

## Exact role and route matrix

| Role | Spawn tested | Model | Effort | Sandbox | Parent | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `codex_agent_team_reader` | yes, `fork_turns=none` | `gpt-5.6-luna` | `max` | `read-only` | matched | local rollout, L1 |
| `codex_agent_team_worker` | discovery only | not observed | not observed | not observed | not observed | C1 |
| `codex_agent_team_investigator` | discovery only | not observed | not observed | not observed | not observed | C1 |
| `codex_agent_team_advisor` | discovery only | not observed | not observed | not observed | not observed | C1 |

The Reader returned the requested `RUNTIME_ROLE_OK`. `inspect-runtime.py` emitted the expected role, model, effort, sandbox, managed permission profile, runtime version, and parent id.

## Runtime Truth adversarial matrix

The deterministic repository cases passed as part of the 96-test suite. One real Reader record passed local inspection. Native runtime attestation was not separately exposed, so the live result is L1 rather than R1/R2. Remaining live conflict and schema-drift cases are not yet executed.

## Contractability and user-flow simulations

The missing-profile case failed closed and avoided role substitution. The fresh-task Reader case used an explicit bounded responsibility and `fork_turns=none`. Ambiguous-writing, prompt-injection, Shared Evidence invalidation, Luna failure classification, Terra delta, and selective Sol simulations are not yet executed.

## Parallelism and lifecycle stress

Not yet executed. No claim is made about one-writer enforcement, slot leakage, orphan cleanup, cancellation recovery, or 10-cycle stress.

## Installer fault injection

### CAT-LOCAL-001: Codex home symlink is followed instead of rejected — resolved locally

- Severity: P1
- Ownership: PROJECT
- Revision: `1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d`
- Runtime: Python 3.14.6 on macOS 27.0
- Expected: a symlink supplied as `--codex-home` is rejected before any managed file is written.
- Pre-fix actual: the installer exited 0, resolved the link, and wrote four profiles plus the ownership manifest into the link target.
- Root cause: `install()` calls `expanduser().resolve()` before preserving and validating the caller-supplied destination identity. Later checks see only the resolved real directory.
- Minimal reproduction: create an empty real directory, create a symlink to it, pass the symlink as `--codex-home`, then enumerate the real directory.
- Pre-fix evidence: exit 0 and five files appeared in the real target.
- Fix: preserve the expanded caller path, reject it when the Codex-home endpoint is a symlink, then resolve it normally. Arbitrary ancestor symlinks remain supported.
- Regression: the public installer CLI now fails non-zero and leaves the real target completely empty, including no empty directories.
- Verification: focused installer suite 14 passed; complete suite 97 passed; the original filesystem reproduction exits 1 with zero target files.
- Compatibility characterization: a non-symlink Codex-home endpoint below a symlinked ancestor still installs successfully and creates only the expected five managed files.

Other fault-injection cases remain unexecuted.

## Review reconciliation

A secondary review claimed that `inspect-runtime.py` fails on two `session_meta` records. That reproduction used a generic review child with `fork_turns=all`; it does not match the Plugin's required `fork_turns=none` path. The real custom Reader rollout had one applicable session record and inspected successfully. This claim is rejected as a Plugin defect unless it reproduces on an exact project role using the supported fork policy.

GPT-5.6 Sol High independently reviewed the evidence and agreed with PROJECT/P1 and HOLD. It rejected P0 because there is no demonstrated privilege escalation, unrelated-file overwrite, credential exposure, or unrecoverable damage. It also rejected expanding this patch into a ban on arbitrary ancestor symlinks: the supported minimum is to reject a symlinked Codex-home endpoint before `resolve()`, preserve the existing managed-entry checks, and document the precise boundary. During patch review it found that the first regression only counted files and could miss empty directories; the regression was tightened to require a completely empty target. After the focused, installer, complete-suite, and real-filesystem checks passed again, its final verdict was `PATCH ACCEPTED` with no remaining patch-scope blocker. The `fork_turns=all` inspector claim remains a latent schema-risk signal, not a current blocker.

## Behavioral evaluation and performance

Paired raw-prompt versus compiled-contract trials were not run. No cost, latency, or quality advantage is claimed. One fresh-task role probe consumed roughly 711k input tokens, mostly cached; this single diagnostic path is not representative enough for a product-cost conclusion.

## Upstream and environment observations

- A task created before profile provisioning did not refresh custom-role discovery; a fresh task did. This matches the documented unknown and recovery path.
- In a read-only task, the system Git binary emitted temporary-cache warnings. The requested read-only role probe still completed; ownership and product impact remain unclassified.

## Current takeover status

**INCOMPLETE — release recommendation not yet available**

Unfinished gate set:

1. The remaining live release gates, especially all-role execution, lifecycle stress, one-writer enforcement, and behavioral controls, have not yet been completed.

`CAT-LOCAL-001` is fixed locally and no longer blocks a core invariant. Until the unfinished gates produce evidence, this report cannot truthfully choose either `RELEASE CANDIDATE` or the handoff-defined `HOLD`. Do not redesign the orchestration architecture from this finding.
