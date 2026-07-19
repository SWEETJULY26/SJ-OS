---
name: Formula Tracker stage-gate procedure
description: The 5-stage Formula Development Tracker workflow plus the IL Review Gate handoff to claims-il-and-label-keeper. Walks SKN-OPS-008 on the regulatory side. Used by asana-pd-manager and by sibling PD skills proposing stage moves.
last_updated: 2026-05-17
---

# Formula Tracker stage-gate procedure

The SJ SKIN – Formula Development Tracker (project GID `1213280384100264`) is the only project that carries the 5-stage workflow plus the `IL Status` custom field. Every formula moves through these stages from intake to launch readiness.

## The 5 stages

| Stage | Meaning |
|---|---|
| **Intake / Concept** | Formula submitted, not yet in active review |
| **In Review** | Formula under evaluation — color match, texture, stability |
| **Signed Approvals** | Formula approved, signed off |
| **Revisions Required** | Sent back — needs reformulation or adjustments |
| **Rejected** | Formula not moving forward |

## Stage move rules

When moving a task between stages:

- Confirm the move with stage name, task name, and reason before executing (per Rule 1 in `references/confirmation-protocol.md`)
- Moving to **Revisions Required** — ask Alvin if he wants to add a comment explaining what revisions are needed
- Moving to **Rejected** — ask if a reason should be logged as a comment
- Moving **backward** (Signed Approvals → In Review, etc.) — flag as unusual and ask Alvin to confirm intent (Rule 6)
- Moving to **Signed Approvals** — fire the IL Review Gate every time, no exceptions (see below)

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

When a task moves to **Signed Approvals**, do all of the following as a single atomic action confirmed once via Rule 1:

1. Flip `IL Status = Pending IL Review` on the Formula Tracker task
2. Create a task in SJS Regulatory Management (project GID `1214660807386611`) with title prefix `[IL Review Pending — claims-il-and-label-keeper]`
3. Place the new task in the **Inbound Staging** section (GID `1214661463988658`)
4. Set custom field `Artifact Type = IL Review`
5. Set custom field `Linked SKU` to the SKU code + name
6. Link the new task to the originating Formula Tracker task in its description

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

- **2026-05-17** — Externalized from inline asana-pd-manager v1 SKILL.md. Updated SKN-OPS-008 status from "working draft, pending ratification" to "ratified 2026-05-09" per `quality-manager/references/sop-catalog.md`.
