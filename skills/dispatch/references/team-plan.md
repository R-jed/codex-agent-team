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

Allowed roles come from `../../../policy-contract.json`. TeamPlan records the role currently assigned by the router; it does not independently choose that role or its model.

TeamPlan does not duplicate the full child packet. The responsibility packet still carries intent, mutation authority, decision rights, interfaces, evidence, optional Handoff Capsule, current failure, and stop conditions.

## 3. Dependency truth

`depends_on` is the machine-checkable structural dependency graph.

A unit is structurally ready only when all units named in `depends_on` have been accepted. Main still decides whether a structurally ready unit is worth delegating, semantically safe to run now, and justified under current compute and authority boundaries.

Different files do not prove semantic independence. Shared APIs, schemas, migrations, lockfiles, generated artifacts, persistent state, external systems, or other shared interfaces remain Main-level semantic checks even when the validator sees disjoint paths.

Do not use integration order to hide an unresolved execution dependency. If a unit cannot make safe progress until another unit establishes missing semantics or evidence, that dependency belongs in `depends_on`.

A Handoff Capsule may carry already-accepted evidence across a dependency boundary, but it does not make an unresolved predecessor accepted and it does not replace `depends_on`.

## 4. Ownership

`ownership.write` lists the relative paths the unit may own for source mutation when its responsibility packet separately grants `bounded-source-write` mutation authority.

`ownership.forbidden` lists relative paths the unit must not mutate.

Filesystem ownership does not create mutation authority. The responsibility packet remains the authorization source.

Read-only roles, as defined by `policy-contract.json`, must not declare write ownership.

Units that are structurally ready at the same time must not declare overlapping write paths. If they would collide, add a real dependency, repartition ownership, or serialize the work.

A user-requested takeover that moves responsibility ownership to Main is a coordination change. Settle the old child owner first under `recovery.md` and `interaction.md`, then revise TeamPlan when the ownership/assigned role recorded by the plan changes.

## 5. Integration

`integration_owner` is always `main`.

`integration_order` must contain every unit exactly once and must respect `depends_on`.

Completion order does not decide integration order. Main integrates accepted outputs in dependency-respecting order and verifies the resulting combined artifact.

## 6. Revision

Create a new TeamPlan revision only when coordination structure changes materially, including:

```text
role assignment
dependency
ownership
deliverable
scope
acceptance
```

New evidence, a Handoff Capsule refresh, steering that stays within the same responsibility, or an implementation detail does not require a revision by itself. A role change requires a revision only when TeamPlan is active; the router remains the authority that decides the new role.

Revision 1 uses `supersedes_revision: null`. Every later revision must point to the direct previous revision.

Keep the same `unit_id` across revisions only when the responsibility identity remains the same. `goal` and `output` therefore stay stable for that unit. A role may change after blocker-driven rerouting, and ownership, dependencies, scope, or acceptance may be revised, without resetting responsibility identity. If the goal or output is materially split, replaced, or redefined, use a new unit ID. This keeps the recovery attempt budget bound to one stable responsibility instead of resetting it through plan revision.

Already-dispatched work remains bound to the plan truth it received. Do not silently rewrite a running responsibility. When a structural change affects active work, pause new dispatch, settle or safely invalidate the affected responsibility, then dispatch against the new revision.

## 7. Validation

Before multi-responsibility dispatch, validate the plan:

```bash
python scripts/validate_team_plan.py /path/to/team-plan.json
```

The validator checks the exact schema shape, unit identity, roles from `policy-contract.json`, dependency validity and cycles, safe ownership paths, ready-layer write collisions, revision shape, and integration order.

When TeamPlan revisions are recorded in a recovery ledger, the ledger validator also rejects reuse of one `unit_id` for a changed goal or output.

It intentionally does not impose standard/expanded team sizes, fixed waves, model routing, Provider routing, or a private scheduler. Native Codex capacity remains the concurrency ceiling; Main still chooses the smallest useful active set.
