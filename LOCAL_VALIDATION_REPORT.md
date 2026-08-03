# Codex Delegate Local Validation Report

This file is the evidence ledger for local runtime validation. `HEADOFF.md` defines what must be tested next; this report records what was actually observed, on which revision/runtime, what evidence remains reusable, and what is still unverified.

Do not treat repository policy text, CI, or model consultation as proof of live Codex runtime behavior.

## Current reconciliation

- Report reconciled: 2026-08-03.
- Product name: **Codex Delegate**.
- Current Plugin version: `0.4.0`.
- Canonical user entry point: `/codex-delegate`.
- Compatibility repository/package namespace remains `R-jed/codex-agent-team` / `codex-agent-team` pending live migration evidence.
- Repository head observed immediately before this reconciliation: `6945771556b1295ca2c4fcf2ee8bbe5b1516686f`.
- Remote branch inventory observed immediately before this reconciliation: `origin/main` only.
- Last complete deterministic CI baseline recorded for the v0.4.0 rename contract: `6ee045e8f27e62252430403bbe7b1df6ca52d64f`, with 109 tests passing on Ubuntu/Python 3.11, plus passing Ubuntu/Python 3.12 and macOS/Python 3.11 jobs, Plugin manifest validation, and managed-profile install/check/idempotent reinstall.
- The 18 commits between `6ee045e...` and the pre-reconciliation `main` observation were limited by repository compare to README/SVG documentation and `tests/test_policy.py`; no Plugin runtime, Agent profile, installer, routing, safety, or verifier production file changed in that range. Full CI on the exact pre-reconciliation head is not recorded here unless a later checkpoint supplies it.
- Last live-tested production behavior baseline remains `c6020db903b35f0d57677b131bf35b0580144ab9`.
- Known open reproducible PROJECT P0/P1 defects: none.
- Operational release posture: **HOLD FOR RELEASE / VALIDATION INCOMPLETE** while mandatory live gates in `HEADOFF.md` remain unfinished.

At every new checkpoint, fetch `origin/main`, record the actual current SHA, and inspect intervening changes before reusing evidence whose dependencies may have changed.

## Evidence status rules

Use these distinctions throughout this report:

- **Repository fact**: current source, manifest, policy, test, or commit state observed directly from the repository.
- **Deterministic evidence**: reproducible test, verifier, installer, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Model judgment**: advisory conclusion that remains challengeable and cannot substitute for deterministic or runtime evidence.
- **Carried forward**: older evidence whose declared dependencies have not changed materially.
- **Pending revalidation**: policy or code exists, but the corresponding live claim has not yet been demonstrated on the current validation cycle.

## Last live runtime environment

The most recent accepted real-runtime evidence currently carried forward was collected on:

- Initial validation date: 2026-08-02 (Asia/Shanghai).
- Initial validation revision: `1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d`.
- Accepted symlink-fix production baseline: `c6020db903b35f0d57677b131bf35b0580144ab9`.
- Platform: Apple Silicon, macOS 27.0 (26A5388g).
- Python: 3.14.6.
- Git: 2.50.1.
- Codex CLI/runtime: 0.146.0.

The `c6020db...` revision is an evidence baseline, not the current repository head.

## Branch and repository hygiene

Historical merged development refs and the former `local-runtime-validation` ref were previously removed after accepted work reached `main`.

Later temporary refs `docs/handoff-progress-v2` and `noop-check` were also removed. The most recent remote branch query before this reconciliation returned only:

```text
origin/main
```

No open branch contains unique code that must be merged before continuing validation.

## Deterministic repository evidence

Historical deterministic progression:

- Initial suite: 96 passed.
- Post CAT-LOCAL-001 fix: 97 passed.
- Handoff/release closure later reached 98 and 99 tests in merged CI milestones.
- Concurrency-policy closure reached 105 passed.
- User-facing README closure reached 107 passed.
- Codex Delegate v0.4.0 rename closure reached **109 passed** on Ubuntu/Python 3.11; Ubuntu/Python 3.12 and macOS/Python 3.11 also passed.
- Plugin and marketplace manifests validated successfully on the v0.4.0 CI baseline.
- Managed profile lifecycle passed install, `--check`, and idempotent reinstall on the v0.4.0 CI baseline.

The 109-test result belongs to `6ee045e...` plus the inert PR validation marker used only to trigger CI. The marker was never merged. Do not relabel this as live Codex runtime evidence.

## Product rename and compatibility state

Repository facts now establish:

```text
Product display name: Codex Delegate
Canonical command: /codex-delegate
Plugin version: 0.4.0
Repository slug: R-jed/codex-agent-team
Plugin package id: codex-agent-team
Managed role names: codex_agent_team_*
Ownership manifest: .codex-agent-team-agents.json
```

The internal repository/package/profile identifiers are intentionally retained as compatibility identifiers until real upgrade behavior is characterized.

Still pending live migration evidence:

- upgrade from a real installed v0.3.x `Codex Agent Team` to v0.4.0;
- confirm the installed product displays as `Codex Delegate`;
- confirm `/codex-delegate` is discoverable in a fresh task after upgrade;
- characterize the old `/codex-agent-team` invocation after upgrade rather than assuming alias behavior;
- prove the four existing managed profiles and ownership manifest are preserved or updated only under existing ownership rules;
- confirm no duplicate/conflicting Plugin installation appears;
- decide after evidence whether the GitHub repository/package slug should also migrate to `codex-delegate` before v1.0.0.

A cosmetic slug mismatch alone is not a v1 blocker unless it breaks the documented install/upgrade path or creates an unsafe/conflicting Plugin state.

## Plugin installation and role discovery carried forward

The following live evidence from the earlier validated environment remains carried forward unless a changed dependency invalidates it:

- Marketplace registration succeeded from the documented Git source and `main` ref.
- Plugin `codex-agent-team@codex-agent-team` version 0.3.0 installed successfully at that time.
- Before profile provisioning, a fresh task correctly reported the four custom roles unavailable and did not substitute another role.
- Real profile provisioning wrote exactly the four project profiles plus one ownership manifest; `--check` passed.
- No unrelated Agent profiles existed or were changed in the tested clean environment.
- A task created before provisioning did not refresh custom-role discovery on Codex 0.146.0.
- A fresh task after provisioning discovered all four semantic roles.
- Exact first-run consent wording still requires explicit live UX confirmation on the current product path.

Because the product is now v0.4.0 and the canonical command changed, successful v0.3.0 installation evidence does not by itself prove the current upgrade/new-command user path.

## Exact role and route matrix

| Role | Spawn tested | Model | Effort | Sandbox | Parent | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `codex_agent_team_reader` | yes, `fork_turns=none` | `gpt-5.6-luna` | `max` | `read-only` | matched | local rollout, L1 |
| `codex_agent_team_worker` | discovery only | not observed | not observed | not observed | not observed | C1/config only |
| `codex_agent_team_investigator` | discovery only | not observed | not observed | not observed | not observed | C1/config only |
| `codex_agent_team_advisor` | discovery only | not observed | not observed | not observed | not observed | C1/config only |

The Reader returned the requested bounded probe result. `inspect-runtime.py` emitted the expected role, model, effort, sandbox, managed permission profile, runtime version, and parent id.

Independent native runtime attestation was not separately exposed, so the Reader result remains L1 rather than R1/R2.

Pending:

- real Worker spawn and route observation;
- real Investigator spawn and route observation;
- real Advisor spawn and route observation;
- sufficient native/local conflict characterization to support the exact runtime claims in `HEADOFF.md`.

## Runtime Truth evidence

Established deterministic/repository evidence:

- incomplete expected exact routes fail closed;
- route, ancestry, and permission evidence are typed independently;
- one real Reader local rollout was sanitized and inspected successfully;
- configured route identity is not presented as runtime observation;
- partial or missing observations do not establish complete runtime proof.

Still pending live characterization where the runtime exposes the relevant facts:

- complete native route metadata;
- partial native route behavior;
- native/local agreement;
- model conflict;
- parent-thread conflict, wrong parent, and missing parent;
- required read-only with missing or broader native sandbox evidence;
- sandbox/permission-profile conflict;
- thread-id conflict;
- rollout schema drift and duplicate rollout records.

## Contractability, concurrent drift, and user-flow status

Carried-forward live evidence:

- missing-profile case failed closed and avoided role substitution;
- fresh-task Reader used an explicit bounded responsibility and `fork_turns=none`.

Repository policy added after the last live production baseline now requires:

- a bounded Delegation Contract before ambiguous writing execution;
- writing Workers to preserve unrelated existing edits;
- re-read affected state before mutation when concurrent drift is plausible;
- stop and return to the main session if drift invalidates scope, invariants, decision rights, acceptance oracle, or dependent evidence.

These are current policy/repository facts. Their complete live behavior remains pending.

Still pending:

- main-session-only deterministic case;
- bounded Luna Worker contract;
- ambiguous-writing stop behavior;
- judgment escape;
- prompt-injection/scope-boundary behavior;
- actual changed-file verification after writing;
- concurrent user edit preservation;
- Shared Evidence invalidation and reuse;
- Luna failure classification;
- Terra delta escalation;
- selective Sol behavior;
- representative multi-step user flow.

## Concurrency and lifecycle status

The current v1 policy is repository-defined as:

```text
main-session scope: normal child maximum 2, v1 hard maximum 4
canonical workspace scope: at most one active writing Worker
Codex-home scope: one installed managed profile generation
delegation depth: 1
```

No machine-wide/account-wide Agent cap is claimed by the project.

Static regression coverage protects these scopes, but the following live multi-session matrix remains pending:

- M1: two independent sessions, different projects/checkouts, each may use justified children without a project-created global bottleneck;
- M2: same repository, genuinely isolated runtime-backed worktrees, one Writer per isolated workspace when the runtime preserves isolation;
- M3: two independent sessions targeting the same canonical physical checkout must never result in two simultaneous writing Workers;
- M4: writer plus read-only session on the same checkout must invalidate or revalidate stale read-side repository evidence after mutation.

M3 is the release-critical cross-session one-writer test. Do not claim project-side cross-session exclusion until live evidence demonstrates it. If two same-checkout Writers become active, classify the reproduction before implementing the smallest workspace-scoped mechanism.

Also pending:

- useful parallel read-only work;
- duplicate-inference rejection;
- fan-out consent beyond two children;
- native three/four-child capacity characterization;
- slot recovery;
- cancellation/spawn-failure recovery;
- minimum 10-cycle lifecycle stress;
- orphan-child behavior.

## Installer evidence and fault injection

### CAT-LOCAL-001: direct Codex-home endpoint symlink

- Severity: P1.
- Ownership: PROJECT.
- Pre-fix revision: `1eaeb5a7bcb7a55edc1f57aad22d4f00c80d9c0d`.
- Fixed production revision: `c6020db903b35f0d57677b131bf35b0580144ab9`.
- Runtime used for reproduction: Python 3.14.6 on macOS 27.0.
- Expected: a symlink supplied as the `--codex-home` endpoint is rejected before any managed target entry is created.
- Pre-fix actual: installer exited 0, resolved the link, and wrote four profiles plus the ownership manifest into the target.
- Root cause: `install()` resolved the caller-supplied Codex-home path before preserving and validating endpoint identity.
- Fix: preserve the expanded caller path, reject when that endpoint itself is a symlink, then resolve normally. Arbitrary ancestor symlinks remain supported.
- Regression: public CLI fails non-zero, emits the explicit refusal, preserves prior file state, and leaves the target with zero entries.
- Verification: focused regression passed; installer suite 14 passed; complete suite 97 passed; `git diff --check` passed; original filesystem reproduction exits 1 with zero target entries.
- Compatibility characterization: a non-symlink Codex-home endpoint below a symlinked ancestor still installs successfully and creates the expected managed files.
- Independent patch review final verdict: `PATCH ACCEPTED`.
- Current status: **CLOSED ON PRODUCTION HISTORY**.

Residual pathname TOCTOU under concurrent local mutation remains outside that focused patch threat model unless new evidence makes it release-relevant.

### Remaining installer live gates

Still pending:

- user-modified current profile refuses overwrite;
- unrelated TOML claiming a reserved semantic role refuses;
- proven legacy model-named profile migrates safely;
- unproven legacy profile is preserved;
- stale standalone manifest cannot re-delete a recreated user file;
- symlinked managed agents directory/manifest/profile is rejected as documented;
- unwritable agents directory;
- interrupted/staged replacement;
- disk-full or manifest-write failure when practical;
- rollback after partial mutation;
- post-success cleanup failure when safely reproducible.

### Concurrent Codex-home installer matrix

The installer is currently proven transactional only in the single-process cases already exercised. Multi-process behavior remains uncharacterized.

Pending:

- I1: two installer processes start concurrently against the same clean `CODEX_HOME` and same shipped profile generation; acceptable result is exact convergence or one safe refusal with exact final managed state and no debris;
- I2: one process fails after mutation begins while a peer succeeds; the failing process must not roll back or corrupt the peer-success state;
- repeat I1 against pre-existing exact managed state;
- mixed expected profile generations in one Codex home must fail closed at the affected route rather than cross-role substitute.

Do not claim multi-process installer safety and do not add a lock solely from theoretical concern. A concrete I1/I2 failure must be reproduced and classified first.

## Shared Evidence and behavioral evaluation

Shared Evidence reuse has not yet been demonstrated on the required live multi-Agent workflow.

Pending measures include:

- unjustified repeated commands;
- unjustified repeated repository discovery;
- duplicate dependency calls;
- evidence established;
- evidence invalidated;
- preservation of unrelated evidence after unrelated changes.

The primary controlled behavioral experiment remains:

```text
A: raw user prompt -> Luna Max
B: same prompt -> main session compiles Delegation Contract -> Luna Max
```

No claim is currently established that compiled contracts improve quality, cost, or latency.

Terra delta-escalation and Luna-plus-selective-Sol controlled pairs also remain pending. Missing token/latency telemetry must not be estimated.

One historical fresh-task role probe consumed roughly 711k input tokens, mostly cached. That single diagnostic path is not representative enough for a product-cost conclusion.

## Review and adversarial consultation record

The CAT-LOCAL-001 symlink defect received repeated adversarial review and converged on PROJECT/P1 with a minimal endpoint-only repair. The first regression was tightened to prove zero target entries before the patch was accepted.

A separate claim that `inspect-runtime.py` fails with two `session_meta` records was reproduced only through a generic child using `fork_turns=all`; it did not reproduce on the supported exact Reader path using `fork_turns=none`. Current classification remains a latent schema-compatibility signal rather than a confirmed Plugin defect.

For the current validation cycle, `gpt56-sol-pro-consult` is the required independent adversarial consultation mechanism at Review Checkpoints A-E, after any P0/P1 candidate, and for release-candidate review as defined in `HEADOFF.md`.

Consultation output is model judgment. It must not be counted as evidence that Codex Delegate itself routed the four managed Agent roles correctly. Codex remains the local executor and reconciles consultation against repository/runtime evidence.

## Upstream and environment observations

- On Codex 0.146.0, a task created before profile provisioning did not refresh role discovery; a fresh task did. This is version-scoped evidence, not a permanent statement about newer runtimes.
- A read-only task emitted system Git temporary-cache warnings while still completing successfully. No release-blocking product impact has been established.

## Current release status

**HOLD FOR RELEASE / VALIDATION INCOMPLETE**

This status reflects unfinished mandatory live gates. It does not mean a reproducible PROJECT P0/P1 is currently open.

Highest-priority unfinished evidence now is:

1. v0.3.x to Codex Delegate v0.4.0 real Plugin upgrade and `/codex-delegate` fresh-task discovery;
2. exact live Worker, Investigator, and Advisor route characterization;
3. materially available Runtime Truth conflict/partial cases;
4. contractability, prompt-injection, and concurrent-drift simulations;
5. Shared Evidence reuse/invalidation and Luna failure classification;
6. raw-prompt versus compiled-contract paired evaluation;
7. Terra delta and selective Sol controlled pairs;
8. M1-M4 multi-session/workspace concurrency matrix;
9. fan-out and lifecycle stress;
10. remaining installer fault injection and I1/I2 multi-process installer matrix.

Continue in the order defined by `HEADOFF.md`. After every review checkpoint, send the compact `CONTEXT_PACKET_V1` through `gpt56-sol-pro-consult` before changing core policy or architecture.

The pre-release process remains finite. When the v1.0.0 Definition of Done and fixed release-candidate closure pass are satisfied, the required next action is release, not another open-ended optimization cycle.
