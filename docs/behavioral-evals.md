# Live behavioral evaluation protocol

Static repository tests prove policy text, schemas, installer behavior, and deterministic evidence tooling. They do not prove that a particular Codex build will follow the Skill correctly in a real session.

This repository therefore keeps live behavioral evaluation separate from unit tests.

## Workload suite

`evals/behavioral-workloads.json` contains representative tasks for:

- Root-only small fixes;
- context isolation;
- bounded implementation;
- genuine read-only parallelism;
- risk-triggered Terra review;
- one-writer enforcement;
- repository prompt injection;
- unavailable routes;
- runtime-route mismatch;
- broadened reviewer sandbox;
- high-consequence unobservable independence;
- consent-gated Sol escalation.

These workload definitions are expectations, not benchmark results.

## Modes

Record at least:

```text
root_only
agent_team
```

An external baseline such as another orchestration project may be recorded as `external_baseline`, but do not mix results from different Codex versions without retaining runtime metadata.

## Required run metadata

Each result file follows `evals/behavioral-result.schema.json` and records:

- Codex version and date;
- workload id and mode;
- task success;
- actual Agent count and roles;
- route evidence grade when available;
- policy violations;
- review findings and material catches;
- consent prompts;
- input/output/reasoning tokens when exposed;
- latency when exposed.

Missing token or latency telemetry stays `null`. Do not estimate it.

## Scoring

```bash
python scripts/score-behavioral-evals.py path/to/result.json
```

The scorer validates the result schema and summarizes success rate, mean Agent count, policy violations, review catches, consent prompts, and any recorded token/latency metrics.

## Release evidence rule

Do not claim that Minimum Team reduces token cost, that Luna Max is the optimal Worker effort, that Terra XHigh improves review quality, or that runtime evidence reduces misrouting unless a live result set supports the claim on named Codex versions.

When comparing reasoning settings, keep the workload, Root model, Codex build, permissions, and acceptance rubric fixed.

Recommended first comparisons:

```text
Luna High vs Luna Max          bounded implementation
Luna High/Max vs Terra Medium/High   large read-heavy exploration
Terra High vs Terra XHigh      detached review
```

Routing policy should remain stable until representative workloads show a repeatable reason to change it.
