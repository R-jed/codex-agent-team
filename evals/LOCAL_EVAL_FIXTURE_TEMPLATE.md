# Local Eval Fixture Template

Use this template before starting any formal paired live behavioral run from `HEADOFF.md`.

The repository workload registry defines experiment shapes. This file defines the minimum information that must be frozen locally so a baseline/candidate pair is reproducible and comparable.

```text
fixture_id:
workload_id:
workload_definition_hash:

repository:
base_revision:

exact_user_prompt:
<verbatim prompt bytes used by both modes>

starting_state:
<setup commands, fixture files, seed data, or other deterministic preconditions>

acceptance_rubric_id:
acceptance_rubric:
<observable scoring / pass-fail criteria>

allowed_verification:
- <command or inspection>

main_session_route:
worker_route: <route or null>
permissions_fingerprint:
tool_surface_fingerprint:
codex_runtime_version:

sanitization_notes:
<what was removed from the public/local report, without changing the executable task>
```

Rules:

- Freeze this definition before the first run in a pair.
- Baseline and candidate use the same exact prompt, repository revision, starting state, acceptance rubric, routes, permissions, and tool surface unless the compared mode explicitly changes that one experimental factor.
- Compute `workload_definition_hash` from the frozen executable definition, not from the generic workload id alone.
- If any controlled input changes, create a new fixture version, pair id, and workload-definition hash.
- Do not place credentials, private transcripts, hidden reasoning, or unrelated local paths in the fixture.
- Store a sanitized copy or equivalent reproduction data with `LOCAL_VALIDATION_REPORT.md` when safe.
