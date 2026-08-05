# Evaluation files

This folder contains the test data used to check routing and runtime behavior. It is for maintainers and is not part of the normal user setup.

- `behavioral-workloads.json`: saved task shapes for repeated live tests.
- `behavioral-result.schema.json`: format used to store test results.
- `LOCAL_EVAL_FIXTURE_TEMPLATE.md`: template for freezing a local test case before comparing runs.
- `routing-cases.json`: static cases that catch obvious routing regressions.
- `runtime-assurance-cases.json`: fixtures used by runtime-evidence tests.

These files do not control how the plugin routes work. The live behavior is defined by the installed Skill's `router-core.md`, `guardrails.md`, `final-review.md`, and the stable settings in `policy-contract.json`.

See [`../docs/behavioral-evals.md`](../docs/behavioral-evals.md) for the measurement protocol.
