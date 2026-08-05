# Evaluation artifacts

This directory is a maintainer-facing measurement and regression surface. It is not part of the end-user installation flow and does not define the runtime router.

- `behavioral-workloads.json`: frozen experiment shapes, not benchmark results or product policy.
- `behavioral-result.schema.json`: machine-checkable result format.
- `LOCAL_EVAL_FIXTURE_TEMPLATE.md`: freezes a reproducible local workload before paired runs.
- `routing-cases.json`: static strategy regression cases used to catch obvious routing regressions. Their detailed labels do not require the runtime Skill to maintain the same ontology.
- `runtime-assurance-cases.json`: deterministic fixtures for optional runtime-evidence reconciliation.

The current runtime mechanism is owned only by the installed Skill's `router-core.md`, `guardrails.md`, and `final-review.md`, plus stable machine constants in `policy-contract.json`.

See [`../docs/behavioral-evals.md`](../docs/behavioral-evals.md) for the measurement protocol.
