# Contributing

Codex Agent Team favors a small policy surface, explicit safety boundaries, and evidence-backed changes.

Before proposing a change:

1. Explain the concrete failure mode or user benefit.
2. Prefer simplifying an existing rule over adding another routing layer.
3. Add or update a routing eval that captures the behavior.
4. Keep the installable Skill under `skill/codex-agent-team/` free of repository-only documentation and development dependencies.
5. Run `pytest -q`.

Model availability, Codex tool schemas, and pricing can change. Avoid treating a temporary runtime observation as a permanent platform guarantee. When a rule depends on runtime support, make the Capability Gate explicit.

Security-sensitive changes should preserve fail-closed behavior, one-writer discipline, prompt-injection boundaries, recursion limits, and human consent for material escalation.
