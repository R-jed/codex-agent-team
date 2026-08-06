# TeamPlan

TeamPlan is the lightweight coordination contract for tasks that need more than one delegated responsibility at the same time or need machine-checkable dependency and integration order.

It does not choose models, replace Main, create another planner, or impose a project-level child-count target. `router-core.md` still decides whether delegation is useful and which specialist role owns each responsibility. Main remains the integration and acceptance owner.

## 1. When TeamPlan is required

Do not create TeamPlan ceremony for zero or one delegated responsibility.

Compile TeamPlan before dispatch when either condition becomes true:

- two or more delegated responsibilities are concurrently unresolved; or
- delegated outputs have a non-trivial dependency or integration order that must remain explicit across attempts.

If the task later returns to one simple responsibility, keep the current accepted plan truth but do not create new plan machinery without value.

When an upstream Skill or accepted plan already owns decomposition, dependencies, outputs, acceptance, or quality gates, compile those responsibilities into TeamPlan without changing the upstream workflow.

## 2. Minimal contract

A TeamPlan is one JSON object:

```json
{
  "schema_version": "1.0",
  "revision": 1,
  "supersedes_revision": null,
  "planning_source": "ad_hoc",
  "source_refs": [],
  "root_goal": "deliver the verified requested result",
  "units": [
    {
      "unit_id": "U1",
      "role": "reader",
      "goal": "trace the existing API contract",
      "output": "bounded evidence for Main",
      "depends_on": [],
      "ownership": {"write": [], "forbidden": []},
      "done_when": "the relevant call path and contract are evidenced"
    },
    {
      "unit_id": "U2",
      "role": "worker",
      "goal": "implement the already-decided bounded change",
      "output": "verified source changes",
      "depends_on": ["U1"],
      "ownership": {"write": ["src/example.py"], "forbidden": []},
      "done_when": "the change satisfies its acceptance checks"
    }
  ],
  "integration_owner": "main",
  "integration_order": ["U1", "U2"],
  "final_verification": "Main verifies the combined artifact against user acceptance",
  "revision_reason": "initial"
}
```

Each unit keeps exactly these coordination fields:

```text
unit_id
role
goal
output
depends_on
ownership
done_when
```

Allowed roles are the five codex delegate specialist roles:

```text
reader
worker
solver
investigator
advisor
```

TeamPlan does not duplicate the full child packet. The responsibility packet still carries intent, mutation authority, decision rights, interfaces, evidence, current failure, and stop conditions.

## 3. Dependency truth

`depends_on` is the machine-checkable structural dependency graph.

A unit is structurally ready only when all units named in `depends_on` have been accepted. Main still decides whether a structurally ready unit is worth delegating, semantically safe to run now, and justified under current compute and authority boundaries.

Different files do not prove semantic independence. Shared APIs, schemas, migrations, lockfiles, generated artifacts, persistent state, external systems, or other shared interfaces remain Main-level semantic checks even when the validator sees disjoint paths.

Do not use integration order to hide an unresolved execution dependency. If a unit cannot make safe progress until another unit establishes missing semantics or evidence, that dependency belongs in `depends_on`.

## 4. Ownership

`ownership.write` lists the relative paths the unit may own for source mutation when its responsibility packet separately grants `bounded-source-write` mutation authority.

`ownership.forbidden` lists relative paths the unit must not mutate.

Filesystem ownership does not create mutation authority. The responsibility packet remains the authorization source.

Read-only roles (`reader`, `investigator`, `advisor`) must not declare write ownership.

Units that are structurally ready at the same time must not declare overlapping write paths. If they would collide, add a real dependency, repartition ownership, or serialize the work.

## 5. Integration

`integration_owner` is always `main`.

`integration_order` must contain every unit exactly once and must respect `depends_on`.

Completion order does not decide integration order. Main integrates accepted outputs in dependency-respecting order and verifies the resulting combined artifact.

## 6. Revision

Create a new TeamPlan revision only when task structure changes materially:

```text
dependency
ownership
deliverable
scope
acceptance
```

New evidence or an implementation detail does not require a revision by itself.

Revision 1 uses `supersedes_revision: null`. Every later revision must point to the direct previous revision.

Already-dispatched work remains bound to the plan truth it received. Do not silently rewrite a running responsibility. When a structural change affects active work, pause new dispatch, settle or safely invalidate the affected responsibility, then dispatch against the new revision.

## 7. Validation

Before multi-responsibility dispatch, validate the plan:

```bash
python plugins/codex-delegate/scripts/validate-team-plan.py /path/to/team-plan.json
```

The validator checks schema shape, unit identity, dependency validity and cycles, safe ownership paths, ready-layer write collisions, revision continuity, and integration order.

It intentionally does not impose standard/expanded team sizes, fixed waves, model routing, Provider routing, or a private scheduler. Native Codex capacity remains the concurrency ceiling; Main still chooses the smallest useful active set.
