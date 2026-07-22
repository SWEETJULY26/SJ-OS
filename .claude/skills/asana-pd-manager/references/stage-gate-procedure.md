---
name: Formula Tracker stage-gate procedure
description: The 5-stage Formula Development Tracker workflow plus the IL Review Gate handoff to claims-il-and-label-keeper. Walks SKN-OPS-008 on the regulatory side. Used by asana-pd-manager and by sibling PD skills proposing stage moves.
last_updated: 2026-07-21
---

# Formula Tracker stage-gate procedure

The SJ SKIN – Formula Development Tracker (project GID `1213280384100264`) is the only project that carries the 5-stage workflow plus the `IL Status` custom field. Every formula moves through these stages from intake to launch readiness.

## The 5 stages

**Correction (confirmed with Alvin 2026-07-21):** "Signed Approvals" is not a literal Asana section — it's a custom-field-driven view. The actual Asana section is **Approved**. The trigger for the move isn't a section drag — it's the relevant review/approval custom field (e.g. `Review Status`) being set to `Approved`; when that happens, the task moves to the **Approved** section *from whatever section it's currently sitting in*, not just from "In Review." An eval run against the live workspace on 2026-07-21 confirmed there is no section literally named "Signed Approvals" anywhere in the project — this table below uses "Signed Approvals" only as the conceptual/gate-trigger name that this doc and the IL Review Gate refer to; the literal Asana destination is always **Approved**.

| Stage (conceptual name used in this procedure) | Live Asana section | Meaning |
|---|---|---|
| **Intake / Concept** | Intake / Concept | Formula submitted, not yet in active review |
| **In Review** | In Review, Sampling, Revisions in Progress, Final Review | Formula under evaluation — color match, texture, stability, sampling, final review (the live workspace splits this into several sections; treat all of them as pre-approval) |
| **Signed Approvals** | **Approved** | Formula approved, signed off — driven by the review/approval custom field being set to Approved, not a section literally named "Signed Approvals" |
| **Revisions Required** | Revisions in Progress | Sent back — needs reformulation or adjustments |
| **Rejected** | Archived/Rejected | Formula not moving forward |

## Stage move rules

When moving a task between stages:

- Confirm the move with stage name, task name, and reason before executing (per Rule 1 in `references/confirmation-protocol.md`)
- Moving to **Revisions Required** (live section: Revisions in Progress) — ask Alvin if he wants to add a comment explaining what revisions are needed
- Moving to **Rejected** (live section: Archived/Rejected) — ask if a reason should be logged as a comment
- Moving **backward** (Approved → In Review, etc.) — flag as unusual and ask Alvin to confirm intent (Rule 6)
- Moving to **Approved** (i.e. the review/approval field being set to Approved — this is what "Signed Approvals" means in this doc) — fire the IL Review Gate every time, no exceptions (see below)

## IL Review Gate — handoff to claims-il-and-label-keeper

The Formula Tracker carries an `IL Status` custom field that gates regulatory review of the ingredient list before a SKU launches.

### Field reference

`IL Status` (single-select) — field GID `1214676606090922` on Formula Tracker project `1213280384100264`. Option GIDs cached in the canonical GID file per `references/gids-pointer.md`.

| Option | Meaning |
|---|---|
| `Not Yet Triggered` | Default on new tasks |
| `Pending IL Review` | Formula approved, IL packet needs to go to Pedrero |
| `In IL Review` | claims-il-and-label-keeper has staged the IL to Pedrero |
| `IL Approved` | Pedrero approved; component and carton artwork can finalize |
| `IL Returned for Reformulation` | Pedrero flagged a problem; back to PD |
| `IL Reformulated — Re-review Required` | Formula reformulated; IL re-review queued |

### Trigger rule

When a task moves to **Approved** (i.e. the review/approval field is set to Approved — see the correction above), do all of the following as a single atomic action confirmed once via Rule 1:

1. **Dedup check first (confirmed with Alvin 2026-07-21):** before creating anything, search SJS Regulatory Management for an existing task with `Linked SKU` matching this formula's SKU code, or an existing `[IL Review Pending — claims-il-and-label-keeper]`-prefixed task referencing this Formula Tracker task. If one already exists, do not create a duplicate — surface the existing task to Alvin and ask whether to link/update it instead (e.g. if this is a re-approval after a revision, or if the task is already sitting in a later regulatory section). This matters most on a re-approval or a re-run of this gate, where a prior IL Review task may already be open or even already resolved.
2. Flip `IL Status = Pending IL Review` on the Formula Tracker task
3. Create a task in SJS Regulatory Management (project GID `1214660807386611`) with title prefix `[IL Review Pending — claims-il-and-label-keeper]` — **only if step 1 found no existing task**
4. Place the new task in the **Inbound Staging** section (GID `1214661463988658`)
5. Set custom field `Artifact Type = IL Review`
6. Set custom field `Linked SKU` to the SKU code + name
7. Link the new task to the originating Formula Tracker task in its description

### Hold rule

The PD launch flow holds at Signed Approvals until `IL Status = IL Approved`. claims-il-and-label-keeper writes the sync-back comment plus the IL Status flip when Pedrero approves. Component and carton artwork finalization is gated on this flip.

### Reformulation rule

If a SKU reformulates after a prior IL approval, set `IL Status = IL Reformulated — Re-review Required`. claims-il-and-label-keeper re-fires the gate when the reformulated formula reaches Signed Approvals.

### Scope boundary

asana-pd-manager never drafts IL packet contents and never sends to Pedrero directly. claims-il-and-label-keeper owns both. This skill only flips the gate field and stages the inbound task.

## SOP anchor

This procedure walks the regulatory side of **SKN-OPS-008 — IL / Claims / Label Procedure**, Rev 1.0, ratified 2026-05-09. The skill-side mirror lives at `claims-il-and-label-keeper/references/il-claims-label-procedure.md`. Catalog reference: `quality-manager/references/sop-catalog.md`.

## Update protocol

If the 5 stages change, or if the IL Review Gate's trigger/hold/reformulation rules shift, update this file plus:
- `claims-il-and-label-keeper/references/il-claims-label-procedure.md`
- `references/cross-skill-handoffs.md` in this skill
- Re-confirm with `quality-manager/references/sop-catalog.md` whether a SOP revision is required

Bump `last_updated` here when the change lands.

## History

- **2026-07-21** — Eval-driven correction from Alvin: fixed the stale claim that "Signed Approvals" is a literal Asana section — it's a custom-field-driven view, and the real destination section is **Approved**, reached whenever the review/approval field is set to Approved from any prior section (not just from In Review). Also added a dedup check to the IL Review Gate trigger rule — search for an existing regulatory task on the same SKU before creating a new `[IL Review Pending — claims-il-and-label-keeper]` task, so a re-approval doesn't create a duplicate.
- **2026-05-17** — Externalized from inline asana-pd-manager v1 SKILL.md. Updated SKN-OPS-008 status from "working draft, pending ratification" to "ratified 2026-05-09" per `quality-manager/references/sop-catalog.md`.
