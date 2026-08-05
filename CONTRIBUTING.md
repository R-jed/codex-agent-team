# Contributing

codex delegate favors a small policy surface, explicit safety boundaries, and evidence-backed changes.

Before proposing a change:

1. Explain the concrete failure mode or user benefit.
2. Prefer simplifying an existing mechanism over adding another routing layer.
3. Update focused tests or evals that capture the intended behavior without turning measurement fixtures into runtime policy.
4. Keep the installed Skill surface under `plugins/codex-delegate/skills/codex-delegate/` focused on runtime behavior. Repository-only validation and maintainer material belongs outside the installed Skill.
5. Preserve the three runtime policy owners: `router-core.md`, `guardrails.md`, and `final-review.md`.
6. Run `pytest -q` and the relevant Plugin validation before treating a change as ready.

Model availability, Codex tool schemas, runtime telemetry, and pricing can change. Do not turn a temporary observation into a permanent platform guarantee. Main-session model awareness remains an optional capability-dedup optimization, and missing runtime evidence stays missing.

Security-sensitive changes should preserve fail-closed exact routing, explicit user authority, one-writer discipline, prompt-injection boundaries, delegation depth one, and fresh independent review when the final artifact requires it.
