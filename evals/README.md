# Evaluation files

This folder contains the test data used to check routing, coordination, and runtime behavior. It is for maintainers and is not part of the normal user setup.

- `behavioral-workloads.json`: saved task shapes for repeated live tests.
- `behavioral-result.schema.json`: format used to store test results.
- `LOCAL_EVAL_FIXTURE_TEMPLATE.md`: template for freezing a local test case before comparing runs.
- `routing-cases.json`: static cases that catch routing regressions, including adaptive multi-Agent fan-out.
- `coordination-cases.json`: static cases for upstream workflow ownership, semantic independence, mutation authority, integration ordering, and requested/accepted/observed route truth.
- `runtime-assurance-cases.json`: fixtures used by runtime-evidence tests.

The adaptive-routing checks cover both sides of the policy: several independent ready responsibilities may run together when useful, while duplicate, speculative, or low-value work stays out of the active team. The project does not use a fixed ordinary child-Agent count as the routing target.

The coordination cases protect a separate concern: parallel work must remain correct after delegation. They check that codex delegate preserves upstream workflow truth, does not confuse filesystem isolation with semantic independence, does not let a verification or read-only responsibility acquire source-write authority, respects explicit integration dependencies, and never relabels an accepted/configured route as an observed runtime route.

These files do not control how the plugin routes or coordinates work. Live behavior is defined by the installed Skill's `router-core.md`, `guardrails.md`, `final-review.md`, and stable settings in `policy-contract.json`.

See [`../docs/behavioral-evals.md`](../docs/behavioral-evals.md) for the measurement protocol.