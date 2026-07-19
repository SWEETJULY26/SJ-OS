---
name: SJS SOP catalog
description: Canonical catalog of every Sweet July Skin SOP plus ratification queue and annual review protocol. Sub-skills query at runtime to confirm current revision before significant writes. quality-manager owns the catalog.
last_updated: 2026-05-09 (SKN-OPS-009 ratified at v6.2 build)
---

# Sweet July Skin SOP Catalog

The runtime source of truth for which SOP revision is current. Sub-skills query this catalog before significant writes (e.g., capa-coordinator confirms SKN-OPS-001 Rev before opening a CAPA; batch-lifecycle-tracker confirms SKN-OPS-007 Rev before drafting a hold record).

---

## 1. Catalog

| SOP Number | Title | Revision | Effective | Status | Skill-side Mirror | Next Review Due |
|---|---|---|---|---|---|---|
| SKN-OPS-001 | CAPA Procedure | 1.0 | 2024-06-30 | Ratified | `capa-coordinator/references/skn-ops-001.md` | 2026-06-30 |
| SKN-OPS-002 | Serious Adverse Event (SAE) | 1.0 | 2024-06-30 | Ratified | (none — owned by complaint-and-event-handler workflow) | 2026-06-30 |
| SKN-OPS-003 | Product Recall | 1.0 | 2024-06-30 | Ratified | (none — owned by complaint-and-event-handler workflow) | 2026-06-30 |
| SKN-OPS-004 | Customer Complaint Handling | 1.0 | 2024-06-30 | Ratified | (none — owned by complaint-and-event-handler workflow) | 2026-06-30 |
| SKN-OPS-005 | Non-Conformance Report (NCR) Procedure | 1.0 | 2026-05-09 | Ratified | `capa-coordinator/references/ncr-procedure.md` | 2027-05-09 |
| SKN-OPS-006 | Lab Quality Procedure | 1.0 | 2026-05-08 | Ratified | `quality-lab-coordinator/references/lab-procedure.md` | 2027-05-08 |
| SKN-OPS-007 | Batch Lifecycle Procedure | 1.0 | 2026-05-08 | Ratified | `batch-lifecycle-tracker/references/batch-lifecycle-procedure.md` | 2027-05-08 |
| SKN-OPS-008 | IL / Claims / Label Procedure | 1.0 | 2026-05-09 | Ratified | `claims-il-and-label-keeper/references/il-claims-label-procedure.md` | 2027-05-09 |
| SKN-OPS-009 | Reportable Events Procedure | 1.0 | 2026-05-09 | Ratified | `adverse-event-and-recall-reporter/references/reportable-events-procedure.md` | 2027-05-09 |

**SharePoint master path:** `Sweet July/PD/Quality Control & Assurance/SOP/`
**SOP & Form Log:** `Sweet July/PD/Quality Control & Assurance/Logs/SOP & Form Log.xlsx`

---

## 2. Catalog query API (how sub-skills use this)

A sub-skill calling quality-manager for a catalog query returns:
- Current revision number
- Effective date
- Skill-side mirror path (or "none — query SharePoint")
- Status (Ratified | Pending ratification | Under annual review | Working draft)

Example queries:
- "current revision of SKN-OPS-001" → "1.0, effective 2024-06-30, ratified, mirror at capa-coordinator/references/skn-ops-001.md"
- "what SOPs are pending ratification" → "SKN-OPS-005 NCR Procedure (drafted by capa-coordinator), pending QA Lead review"
- "any SOPs due for review in next 60 days" → walks the catalog and returns rows where Next Review Due ≤ today + 60 days

---

## 3. Ratification protocol

When a `[SOP Revision Pending — quality-manager]` task lands in SJS Quality Management Inbound Staging:

### 3.1 Intake

1. Read the proposed text from the task description (or the linked skill-side reference file).
2. Confirm authoring sub-skill is identified.
3. Pull current state of the procedure (working draft v0.X, no SOP number assigned, or existing SOP awaiting revision).

### 3.2 Review

QA Lead walks the proposed text. Checks:
- Scope and applicability are correct.
- Roles and responsibilities match current org chart (cross-reference `references/role-map.md`).
- Definitions are unambiguous.
- Procedure steps are walkable end-to-end.
- HITL gates are clearly identified.
- Retention and review cadence specified.
- No conflict with existing ratified SOPs.

### 3.3 Approval

QA Lead approves or returns. On approval:

1. **Assign SOP number.** Next available in the SKN-OPS-NNN sequence (currently SKN-OPS-010 is the next slot after SKN-OPS-009 Reportable Events Procedure ratified 2026-05-09).
2. **Set revision and effective date.** Initial ratification = Rev.1, effective = today's date.
3. **Update the skill-side reference file.** Replace "working draft, pending ratification" header with a numbered-SOP header that mirrors SKN-OPS-001 style. Add revision history table.
4. **Update SKILL.md** of the authoring skill — replace "Working procedure pending ratification" design principle text with "Walks SKN-OPS-NNN verbatim" language.
5. **Generate SharePoint master.** Build .docx via local script (see `/tmp/build_skn_ops_*.py` precedents — SKN-OPS-006 and SKN-OPS-007 have working scripts). Drag into SharePoint master path manually (SharePoint MCP is read-only at v5.5).
6. **Update SOP & Form Log.xlsx.** Add row with SOP number, title, Rev, effective date.
7. **Update this catalog (§1 above).** Move from "Pending ratification" to "Ratified". Set Next Review Due = effective date + 1 year.
8. **Close the queue task** with a comment citing the ratified SOP number.
9. **Comment-back on originating sub-skill task** if applicable.

### 3.4 Returns

If QA Lead returns the draft for revision:
- Comment on the queue task with specific revision asks.
- Authoring sub-skill updates the working draft.
- Re-stage the queue task when ready.

---

## 4. Annual review protocol

For each SOP, an annual review fires automatically on Next Review Due date. Drafts a `[SOP Annual Review — SKN-OPS-NNN]` task in Cross-cutting Tasks section.

### 4.1 Review checklist

QA Lead walks:
1. **Still in scope** — does this SOP still apply to current operations? Any scope drift since last revision?
2. **Still accurate** — are the procedure steps still being walked as written? Any gaps that surfaced via in-flight CAPAs flagging this SOP?
3. **Roles current** — do the roles in the SOP match `references/role-map.md`?
4. **Aligned with current operations** — does the SOP reflect current SKU portfolio, current contract labs, current vendor base, current retailers?
5. **No CAPA-flagged gaps** — query capa-coordinator for any open or recently closed CAPAs that surfaced gaps in this SOP. Address before extending review window.

### 4.2 Outcomes

Three valid outcomes:

**A. Reviewed — no change.** SOP is current and accurate. QA Lead approves no-change. Update catalog: Next Review Due = today + 1 year. Close review task.

**B. Reviewed — minor revision.** Small edits (typo fixes, role-holder updates that don't change procedure steps, clarifications). QA Lead approves Rev.X.1 (e.g., Rev.1 → Rev.1.1). Walk §3 ratification protocol abbreviated (no new SOP number, just revision bump). Update catalog row.

**C. Reviewed — major revision.** Procedure steps change, scope changes, or new sections added. QA Lead returns to authoring sub-skill for revision drafting. Routes to ratification queue per §3 as a new revision (Rev.X+1). Update catalog: Status = Under annual review until ratification completes.

### 4.3 HITL

QA Lead approves the review outcome. Operator stages the review task and walks the checklist; QA Lead is the commit gate.

---

## 5. Numbering policy

- SKN-OPS-NNN, zero-padded to three digits.
- Sequential by ratification order (not by topic or scope).
- Working drafts that haven't ratified don't yet hold a number. Once ratified, they take the next available slot.
- Numbers don't get reassigned. If a SOP is retired, its number stays retired.

---

## 6. Asana representation

This catalog renders in Asana as a pinned task in the SOP Catalog section of SJS Quality Management. The pinned task description carries the §1 catalog table. Updates to the table happen at every ratification, every annual review, every status change.

The pinned task GID is cached in SKILL.md after first-run setup.

---

## 7. Open items

- SKN-OPS-001 §5 in-text gaps (effectiveness review window not specified, retention period `[X]` placeholder, RCA tool selection criteria absent): SKN-OPS-005 closes the effectiveness window gap; the retention placeholder and RCA tool selection criteria stay open. Bundle into a future Rev.2 of SKN-OPS-001 when authored.
- SKN-OPS-001 through SKN-OPS-004 annual review: due 2026-06-30. Will fire as `[SOP Annual Review]` cross-cutting tasks per §4.
