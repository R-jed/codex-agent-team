# Security Policy

subagents-dispatch controls delegation policy. It does not replace Codex sandboxing, approval policies, operating-system permissions, repository access controls, or the user's own authorization boundaries.

Please report security issues through GitHub private vulnerability reporting when it is available for this repository. Avoid publishing exploit details before a maintainer has had a reasonable opportunity to review them.

High-priority security areas include:

- permission escalation without user consent
- prompt injection that changes scope, routing, credentials, or side effects
- child Agent delegation beyond depth one
- unsafe fallback to a different role, model, effort, or permission mode
- multiple writing actors mutating the same canonical checkout inside one orchestration
- managed Agent-profile installation overwriting unrelated user state
- incorrect runtime claims being treated as observed evidence
- child Agents performing high-impact external actions without explicit user authority
- independent Final Review being bypassed when the final artifact requires a fresh second observer
