# OpenAI references used by Codex Agent Team

This page records the OpenAI sources that materially influenced the Skill's design. It separates stable design facts from time-sensitive pricing and runtime implementation details.

Last reviewed: 2026-08-02.

## GPT-5.6 model family and role design

### GPT-5.6 launch announcement

https://openai.com/index/gpt-5-6/

Used for:

- Sol as the flagship tier
- Terra as the balanced intelligence/cost tier
- Luna as the most cost-efficient / high-throughput tier
- GPT-5.6 availability in Codex
- support for model effort selection
- historical launch pricing used to compare the later Luna/Terra price reduction

Historical launch pricing on 2026-07-09, per 1M standard tokens:

| Model | Input | Output |
| --- | ---: | ---: |
| GPT-5.6 Sol | $5.00 | $30.00 |
| GPT-5.6 Terra | $2.50 | $15.00 |
| GPT-5.6 Luna | $1.00 | $6.00 |

OpenAI's launch page now carries a July 30 update explicitly stating that Luna was reduced by 80% and Terra by 20%.

### Current OpenAI API pricing

https://developers.openai.com/api/docs/pricing

Used for the current economics behind the default Worker choice. As reviewed on 2026-08-02, standard short-context pricing per 1M tokens is:

| Model | Input | Output | Change vs. 2026-07-09 launch |
| --- | ---: | ---: | ---: |
| GPT-5.6 Sol | $5.00 | $30.00 | unchanged |
| GPT-5.6 Terra | $2.00 | $12.00 | 20% lower |
| GPT-5.6 Luna | $0.20 | $1.20 | 80% lower |

This price movement is a design input, not a routing invariant. Codex Agent Team routes by responsibility and runtime capability so future pricing changes do not require a policy rewrite.

The current pricing page is the source of truth for price-sensitive documentation. Individual model pages or older catalog entries can lag behind pricing updates.

### GPT-5.6 model guidance

https://developers.openai.com/api/docs/guides/latest-model

Used for:

- `gpt-5.6-sol` for frontier capability
- `gpt-5.6-terra` for intelligence/cost balance
- `gpt-5.6-luna` for efficient high-volume workloads
- GPT-5.6 reasoning efforts including `max`
- the recommendation to compare reasoning settings on representative workloads instead of assuming the highest effort is always optimal
- explicit autonomy/approval boundaries for normal local actions vs. destructive, external, costly, or scope-expanding actions

### Individual model pages

- Luna: https://developers.openai.com/api/docs/models/gpt-5.6-luna
- Terra: https://developers.openai.com/api/docs/models/gpt-5.6-terra
- Sol: https://developers.openai.com/api/docs/models/gpt-5.6-sol

Used for model identity, capability-tier descriptions, reasoning support, context/output limits, and tool support. For live prices, prefer the central pricing page above because some individual model/catalog pages can lag current pricing.

### OpenAI-published coding evaluations

The GPT-5.6 launch announcement also publishes coding results used as supporting context for assigning bounded execution work to Luna:

| Eval | Sol | Terra | Luna |
| --- | ---: | ---: | ---: |
| SWE-Bench Pro | 64.6% | 63.4% | 62.7% |
| DeepSWE v1.1 | 72.7% | 69.6% | 67.2% |
| Terminal-Bench 2.1 | 88.8% | 87.4% | 84.7% |

These are OpenAI model-family evaluations, not Codex Agent Team benchmarks. They are supporting context only; they do not establish that Luna Max beats Terra XHigh on a specific workload.

## Codex Native Subagent runtime contract

Codex is open source, so the Skill also checks the current implementation instead of treating prose docs as a substitute for the live tool schema.

### MultiAgentV2 spawn handler

https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs

Used for:

- `spawn_agent` V2 arguments including `agent_type`, `model`, `reasoning_effort`, and `fork_turns`
- `fork_turns` accepting `none`, `all`, or a positive integer string
- omitted `fork_turns` defaulting to `all`
- full-history forks rejecting an `agent_type` override
- why Codex Agent Team explicitly sets `fork_turns` on every role-specific spawn

### Multi-agent common runtime configuration

https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_common.rs

Used for:

- parent model/effort inheritance
- exact model availability and reasoning-effort validation
- Agent role/profile application order
- runtime-owned permission/approval state being applied to child configuration
- why a profile's sandbox declaration is treated as a default, not proof of effective runtime enforcement

### Multi-agent tool specification

https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs

Used for:

- the fact that model/reasoning overrides can be hidden from the V2 tool schema by runtime configuration
- close-agent lifecycle semantics, including completed Agents continuing to occupy concurrency until closed
- why the Capability Gate uses the live native contract and the lifecycle ends with explicit close

### Custom Agent role discovery and precedence

https://github.com/openai/codex/blob/main/codex-rs/core/src/config/agent_roles.rs

https://github.com/openai/codex/blob/main/codex-rs/core/src/agent/role_tests.rs

Used for:

- discovery of custom role files from configuration-layer `agents/` directories
- the role-file format (`name`, `description`, `nickname_candidates`, plus normal Codex config keys)
- validating that a custom role can provide model, reasoning, sandbox, and developer-instruction defaults
- custom role values taking precedence over earlier same-key session/config values
- why Portable Mode and Profile Mode are treated as mutually exclusive route-configuration paths

## Codex Skill structure

### OpenAI Skill Creator sample

https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md

Used for:

- `SKILL.md` as the required installable entry point
- concise YAML frontmatter
- progressive disclosure
- moving detailed policies into `references/`
- keeping repo-only documentation such as README outside the installable Skill directory

### `agents/openai.yaml` reference

https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md

Used for:

- `display_name`
- `short_description`
- `default_prompt`
- implicit invocation policy

## What is our policy vs. what is OpenAI's

OpenAI sources provide model positioning, pricing, reasoning support, Codex runtime behavior, and Skill packaging conventions.

The following are Codex Agent Team design choices:

- Luna Max as the default execution worker
- Terra XHigh as the selective detached critic
- Sol High as a consent-gated Senior Judge when Root is not Sol
- default 0-1 children, normal maximum 2, hard maximum 4
- one-writer rule
- no recursive Agent teams
- fail-closed exact-route behavior
- plain-language one-time Consent Gate

These choices are intentionally opinionated and should be evaluated on real Codex workloads.
