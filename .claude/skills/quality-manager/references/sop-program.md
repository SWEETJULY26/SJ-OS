---
name: SJS SOP program — shared process
description: The single ratification protocol, annual review protocol, and numbering policy every function's SOP catalog follows. quality-manager owns this process; each function (Quality, Regulatory, PD, Ops) owns its own catalog table listing only its own SOPs. This file holds the process; it holds no SOP rows itself.
last_updated: 2026-08-06
---

# Sweet July Skin SOP program — shared process

Quality owns the SOP *process* for the whole company — how a working procedure gets ratified, how it gets reviewed annually, and how numbers get assigned — so that process is defined once, here, rather than once per function. What Quality does not own anymore is every function's catalog: each function keeps its own table of its own SOPs, in its own umbrella skill's `references/`, following this process.

## Catalogs by function

| Function | Catalog | Numbers |
|---|---|---|
| Quality (System B) | `quality-manager/references/sop-catalog.md` | SKN-OPS-001–007 |
| Regulatory (System C) | `regulatory-manager/references/sop-catalog.md` | SKN-OPS-008–009 |
| PD | `asana-pd-manager/references/sop-catalog.md` | SKN-OPS-011–012 |
| Ops (Purchasing, Inventory, S&OP, Logistics, DTC/OC3PL) | `sjs-ops-system/references/sop-catalog.md` | SKN-OPS-010, 012–023 |

SKN-OPS-012 (PD Readiness → PO Request Handoff) is joint — it has a real owner on both sides (PD gates readiness, Purchasing gates the order), so it's listed in both the PD and Ops catalogs rather than forced into one. That is the one deliberate overlap; every other SOP number appears in exactly one catalog.

This split happened 2026-08-06, the same day the PD/Ops/DTC batch (SKN-OPS-011–023) was ratified. Before that, one catalog (this one) held every SOP in the company, Quality's own and everyone else's, because Quality's catalog was the only ratification protocol and numbering sequence that existed anywhere in the repo. It still is the only one — this program doc is that same protocol, just no longer bundled with Quality's own catalog table.

---

## 1. Ratification protocol

When a `[SOP Revision Pending — <owning umbrella>]` task lands in the owning function's own staging queue (Quality: SJS Quality Management Inbound Staging; other functions: their own project's staging, once one exists):

### 1.1 Intake

1. Read the proposed text from the task description (or the linked skill-side reference file).
2. Confirm the authoring sub-skill is identified.
3. Pull current state of the procedure (working draft v0.X, no SOP number assigned, or existing SOP awaiting revision).

### 1.2 Review

The function's own gate-holder (Quality: QA Lead; other functions: whoever holds that function's equivalent sign-off — see that function's own role-map) walks the proposed text. Checks:
- Scope and applicability are correct.
- Roles and responsibilities match the current org chart (cross-reference that function's own role-map).
- Definitions are unambiguous.
- Procedure steps are walkable end-to-end.
- HITL gates are clearly identified.
- Retention and review cadence specified.
- No conflict with any existing ratified SOP, in any catalog — check across all four, not just the owning function's own.

### 1.3 Approval

The gate-holder approves or returns. On approval:

1. **Assign SOP number.** Next available in the single, company-wide SKN-OPS-NNN sequence — check this program doc's own count of the last number assigned, not just the owning catalog, since the sequence spans all four catalogs. Currently the next open slot is **024**.
2. **Set revision and effective date.** Initial ratification = Rev.1, effective = today's date.
3. **Write the canonical text to `sops/SKN-OPS-NNN-<slug>.md`.** This is the source of truth per the 2026-08-04 decision — not a skill-side mirror file, not SharePoint, not a PLM row.
4. **Update the skill-side reference file, if one exists,** to point at the new canonical file rather than restating its content.
5. **Update the authoring skill's `SKILL.md`** — replace "working draft, pending ratification" language with "Walks SKN-OPS-NNN" language.
6. **Update the owning function's own catalog table** (§1 catalog of that function's `sop-catalog.md`) with the new row. Set Next Review Due = effective date + 1 year.
7. **Close the queue task** with a comment citing the ratified SOP number.
8. **Comment back on the originating sub-skill task** if applicable.

### 1.4 Returns

If the gate-holder returns the draft for revision:
- Comment on the queue task with specific revision asks.
- The authoring sub-skill updates the working draft.
- Re-stage the queue task when ready.

---

## 2. Annual review protocol

For each SOP, an annual review fires automatically on its Next Review Due date, drafting a `[SOP Annual Review — SKN-OPS-NNN]` task in that function's own cross-cutting tasks surface.

**Standing deferral.** SKN-OPS-001–004 (overdue since 2026-06-30) and SKN-OPS-011–023 (ratified 2026-08-06, so not yet due but batched anyway) do not fire individually. The full review across every SOP in every catalog runs once, together, after the SOP set currently being authored across all four functions is done populating — not per-SOP as each one happens to come up for review. Each function's own catalog carries this deferral note against its own affected rows; this program doc is where the rule itself lives.

### 2.1 Review checklist

The gate-holder walks:
1. **Still in scope** — does this SOP still apply to current operations? Any scope drift since last revision?
2. **Still accurate** — are the procedure steps still being walked as written? Any gaps surfaced via in-flight CAPAs or discrepancies flagging this SOP?
3. **Roles current** — do the roles in the SOP match that function's own role-map?
4. **Aligned with current operations** — does the SOP reflect the current SKU portfolio, vendor base, retailers, and channel mix?
5. **No flagged gaps** — query capa-coordinator (Quality-side root cause) or the relevant discrepancy log (Ops-side) for any open or recently closed issue that surfaced a gap in this SOP. Address before extending the review window.

### 2.2 Outcomes

Three valid outcomes:

**A. Reviewed — no change.** SOP is current and accurate. Gate-holder approves no-change. Update the owning catalog: Next Review Due = today + 1 year. Close the review task.

**B. Reviewed — minor revision.** Small edits (typo fixes, role-holder updates that don't change procedure steps, clarifications). Gate-holder approves Rev.X.1 (e.g., Rev.1 → Rev.1.1). Walk §1 abbreviated (no new SOP number, just a revision bump). Update the owning catalog row.

**C. Reviewed — major revision.** Procedure steps change, scope changes, or new sections are added. Gate-holder returns to the authoring sub-skill for revision drafting. Routes to the ratification queue per §1 as a new revision (Rev.X+1). Update the owning catalog: Status = Under annual review until ratification completes.

### 2.3 HITL

The gate-holder approves the review outcome. The Operator stages the review task and walks the checklist; the gate-holder is the commit gate.

---

## 3. Numbering policy

- SKN-OPS-NNN, zero-padded to three digits, **one sequence shared across every function** — not four independent sequences. A SOP's number says nothing about which function owns it; the catalogs-by-function table above is what maps number to owner.
- Sequential by ratification order, not by topic, scope, or function. A PD SOP and an Ops SOP ratified back to back take consecutive numbers regardless of domain.
- Working drafts that haven't ratified don't yet hold a number. Once ratified, they take the next available slot company-wide.
- Numbers don't get reassigned. If a SOP is retired, its number stays retired.
- **Whoever ratifies next must check this program doc for the current next-open-slot, not just their own catalog** — the risk this exists to prevent is two functions both assuming "010" or "024" is free because neither checked the other's catalog.

---

## 4. Catalog query API (how sub-skills use this)

A sub-skill querying its own function's catalog for a SOP's status returns:
- Current revision number
- Effective date
- Canonical text path (`sops/SKN-OPS-NNN-*.md`)
- Skill-side mirror path (or "none — procedure text is inline in SKILL.md")
- Status (Ratified | Pending ratification | Under annual review | Working draft)

A sub-skill querying about a SOP number **outside its own function** should read that function's catalog directly — the catalogs-by-function table above says where. There is no single combined query surface across all four catalogs beyond this program doc's own table; if that becomes a recurring need, it's worth building, but it isn't built today.
