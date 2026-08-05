# OpenAI references used by codex delegate

This page records the current OpenAI sources that materially constrain codex delegate. It separates official Codex/Plugin/model facts from project policy and from product hypotheses that still require live evidence.

Last reviewed: 2026-08-05.

## Normative source order

When these sources disagree with older repository notes, samples, cached pages, issues, or historical commits, prefer the current official documentation and then revalidate the project.

```text
current OpenAI documentation
-> current official validator / current Codex host behavior where applicable
-> project policy
-> historical samples and issue telemetry only as supporting context
```

Do not turn a version-specific runtime observation into a permanent OpenAI guarantee.

## Skills

### Build skills

https://developers.openai.com/codex/skills

Used for:

- `SKILL.md` as the Skill entry point with `name` and `description` frontmatter;
- progressive disclosure through optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`;
- `/skills` as the Codex CLI/IDE Skill picker;
- `policy.allow_implicit_invocation: false` disabling implicit matching;
- restart/reload expectations when newly installed Skill state is not visible;
- preferring plugins for reusable distribution beyond local/repository-scoped Skill authoring.

Current codex delegate consequence:

```text
canonical user command: /codex-delegate
Skill picker: /skills
implicit invocation: disabled
```

The project keeps `/codex-delegate` consistent across its Plugin starter prompts, Skill metadata, public docs, and regression tests.

## Plugin architecture and packaging

### Plugin architecture

https://developers.openai.com/plugins/concepts/plugins

Used for:

- Plugins as the installable/discoverable package shared across supported ChatGPT and Codex surfaces;
- skills-only Plugins when instructions plus existing host tools are sufficient;
- the principle to start with the smallest shape that supports the use case;
- adding MCP/UI only when the product actually needs service-backed tools or visual interaction.

Current codex delegate consequence:

```text
shape: skills-only
no project MCP server
no project UI
no second Agent runtime
```

Native Codex Subagents and custom Agents already supply the execution surface needed by this product, so an MCP server would add infrastructure without a demonstrated user requirement.

### Package your plugin

https://developers.openai.com/plugins/build/plugins

Used for:

- `.codex-plugin/plugin.json` as the required Plugin entry point;
- `skills/` at the Plugin root for bundled Skills;
- stable kebab-case Plugin identity;
- local repository marketplace metadata under `$REPO_ROOT/.agents/plugins/marketplace.json` for authoring/testing;
- manifest install-surface metadata including descriptions, category, capabilities, legal links, starter prompts, and brand assets;
- relative component/asset paths;
- CLI marketplace commands for manual/development authoring rather than hand-editing Plugin configuration.

Current package:

```text
plugins/codex-delegate/.codex-plugin/plugin.json
plugins/codex-delegate/skills/
plugins/codex-delegate/assets/
.agents/plugins/marketplace.json
```

The public user path remains the native Plugin Marketplace. Repository marketplace/CLI instructions are development and troubleshooting paths.

## Public Plugin submission

### Submit plugins

https://developers.openai.com/plugins/deploy/submission

Used for:

- public Skills-only submission being a supported Plugin type;
- verified developer/business identity requirements;
- public listing materials including name, descriptions, logo, category, website, support path, privacy policy, terms, starter prompts, test cases, availability, and release notes;
- public website/support/privacy/terms URLs matching the publisher and accurately describing data handling.

Current repository support:

```text
website: repository/homepage
privacy: PRIVACY.md
terms: TERMS.md
support/security: repository issue and security-reporting surfaces
starter prompts: manifest interface.defaultPrompt
```

Operational publisher verification, submission-form fields, countries/regions, final support URL, release notes, and required positive/negative submission test cases remain release-operations work. Repository files cannot prove those external submission steps are complete.

## Native Subagents and custom Agents

### Subagents

https://developers.openai.com/codex/subagents

Used for:

- native Codex Subagents and child-thread execution;
- parallel read-heavy work as a useful starting point and extra caution for parallel write-heavy workflows;
- custom Agent TOML files under `~/.codex/agents/` for personal roles and `.codex/agents/` for project-scoped roles;
- custom-Agent fields such as `name`, `description`, `developer_instructions`, model, reasoning effort, and sandbox intent;
- native concurrency remaining a host/runtime capability rather than a codex delegate product constant;
- subagent workflows consuming additional tokens and therefore requiring delegation to justify itself.

Current codex delegate custom profiles:

```text
codex_delegate_reader
codex_delegate_worker
codex_delegate_solver
codex_delegate_investigator
codex_delegate_advisor
```

The five TOML files use the native custom-Agent mechanism. `install-agents.py` is a project-specific lifecycle/ownership/collision-safety layer around those native files. It does not implement a second runtime.

Whether future Codex releases provide a simpler first-class Plugin lifecycle for shipping these exact custom Agent profiles must be rechecked before preserving the installer indefinitely.

## Current model guidance

### Model catalog

https://developers.openai.com/api/docs/models

### GPT-5.6 guidance

https://developers.openai.com/api/docs/guides/latest-model

### Individual model pages

- Sol: https://developers.openai.com/api/docs/models/gpt-5.6-sol
- Terra: https://developers.openai.com/api/docs/models/gpt-5.6-terra
- Luna: https://developers.openai.com/api/docs/models/gpt-5.6-luna

Current official positioning used by this project:

```text
GPT-5.6 Sol
-> frontier / complex professional work
-> demanding, ambiguous, multi-step reasoning and coding

GPT-5.6 Terra
-> balance intelligence and cost
-> useful for exploration, read-heavy scans, larger supporting context, and distilled investigation results

GPT-5.6 Luna
-> cost-sensitive, high-volume workloads
-> useful for fast, narrowly scoped, clear, repeatable work
```

All three support configurable reasoning effort. The best effort setting remains workload-dependent and must be evaluated rather than inferred solely from the maximum available setting.

Current codex delegate role interpretation:

- Luna Reader: narrow bounded factual evidence.
- Luna Worker: clear repeatable bounded implementation after material behavior is decided.
- Terra Investigator: bounded read-heavy technical investigation/evidence synthesis after semantics stabilize and material judgment is absent.
- Sol Advisor: demanding/material read-only judgment and fresh independent review.
- Sol Solver: demanding/material judgment-coupled implementation.

Terra is not an escalation rung above Luna. Weak Luna output does not imply Terra. Demanding, ambiguous, multi-step technical reasoning that still requires consequential judgment belongs to capable Main/Sol.

These role placements are project policy informed by official model guidance. Their user-value and cost effectiveness still require controlled live workloads.

## Official validation

The maintained CI downloads and runs the official OpenAI Plugin validator from a pinned `openai/codex` revision so deterministic CI is reproducible.

For a fixed release candidate, `HEADOFF.md` additionally requires the then-current official OpenAI Plugin validator and records its revision separately. A pinned validator passing does not prove a later upstream validator will pass.

Plugin validation proves package/metadata rules. It does not prove live model routing quality, child discovery, exact runtime model/effort, onboarding behavior, writer safety across independent sessions, or independent-review value.

## Runtime facts versus configured intent

The project preserves this distinction:

```text
configured profile/model/effort/sandbox
!=
observed live runtime fact
```

Use live/runtime evidence only when a claim actually depends on it. Missing telemetry remains missing. Do not make runtime diagnostics ordinary ceremony for a bounded task whose acceptance depends on the artifact rather than exact route provenance.

## Project policy choices

The following are codex delegate choices, not OpenAI requirements:

- Main session owns user intent, authorization, integration, acceptance, and final response.
- Zero children is normal.
- Explicit `/codex-delegate` use has a project ordinary-consent envelope of up to two justified concurrent children.
- One canonical checkout has one active writing actor inside the current orchestration.
- Main, Luna Worker, and Sol Solver share that writer domain.
- Delegation depth is one.
- Main-session Sol capability is a cost/quality dedup optimization.
- Failure does not create Luna -> Terra -> Sol escalation.
- Blockers are diagnosed as `contract | judgment | investigation | stalled`.
- A stalled same-role lane gets at most one materially improved clean retry.
- Final Review is consequence-driven and uses a fresh Sol Advisor when independent assurance is required.
- Ordinary successful tasks do not receive a separate orchestration receipt by default.

These choices must be validated against representative daily-development workloads and real Codex runtime behavior before v1.0.0 claims are made.

## Non-normative telemetry

Public GitHub issues, community discussion, and prior project experiments can motivate tests, but they do not override official documentation or prove current runtime behavior. Keep any such evidence explicitly labeled as user-reported/version-scoped and do not copy community percentages or anecdotes into product guarantees.
