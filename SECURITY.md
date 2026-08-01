# Security Policy

Codex Agent Team controls delegation policy. It does not replace Codex sandboxing, approval policies, operating-system permissions, or repository access controls.

Please report security issues through GitHub private vulnerability reporting when it is available for this repository. Avoid publishing exploit details before a maintainer has had a reasonable opportunity to review them.

High-priority security areas include:

- permission escalation without user consent
- prompt injection that changes scope, model routing, credentials, or side effects
- nested Subagent delegation that bypasses the root policy
- unsafe fallback to a different model or permission mode
- multiple writing Workers mutating the same shared workspace
- workers performing high-impact external actions
