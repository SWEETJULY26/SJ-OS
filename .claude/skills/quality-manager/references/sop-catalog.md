---
name: SJS SOP catalog
description: Canonical catalog of every Sweet July Skin SOP plus ratification queue and annual review protocol. Sub-skills query at runtime to confirm current revision before significant writes. quality-manager owns the catalog.
last_updated: 2026-07-29 (reconciled against PLM sop_documents + wiki sop pages; SKN-OPS-005 row and page created, SKN-OPS-008 corrected to Rev 2.0, review dates backfilled)
---

# Sweet July Skin SOP Catalog

> **Reconciled with PLM 2026-07-29.** This catalog and PLM `sop_documents` had drifted: SKN-OPS-005 was ratified here on 2026-05-09 but had no PLM row and no wiki page at all, so for eleven weeks the runtime catalog could not answer "current revision of SKN-OPS-005" while every NCR cited it. SKN-OPS-008 was stale here at Rev 1.0 against PLM's Rev 2.0. `next_review_date` was NULL on all 13 PLM rows, so the Job 1 annual-review sweep had nothing to fire on — with the dates restored, **SKN-OPS-001–004 and all five forms are now 29 days overdue for annual review** (due 2026-06-30). When this file and PLM disagree, treat PLM as runtime truth and fix this file, then check whether a wiki `sop/` page exists too — all three surfaces have to agree.

The runtime source of truth for which SOP revision is current. Sub-skills query this catalog before significant writes (e.g., capa-coordinator confirms SKN-OPS-001 Rev before opening a CAPA; batch-lifecycle-tracker confirms SKN-OPS-007 Rev before drafting a hold record).

---

## 1. Catalog

| SOP Number | Title | Revision | Effective | Status | Canonical text | Skill-side Mirror | Next Review Due |
|---|---|---|---|---|---|---|---|
| SKN-OPS-001 | CAPA Procedure | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-001-capa-procedure.md` | `capa-coordinator/references/skn-ops-001.md` | 2026-06-30 |
| SKN-OPS-002 | Serious Adverse Event (SAE) | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-002-sae-reporting.md` | `complaint-and-event-handler/references/skn-ops-002-sae.md` | 2026-06-30 |
| SKN-OPS-003 | Product Recall | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-003-product-recall.md` | `complaint-and-event-handler/references/skn-ops-003-recall.md` | 2026-06-30 |
| SKN-OPS-004 | Customer Complaint Handling | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-004-customer-complaint-handling.md` | (none — owned by complaint-and-event-handler workflow) | 2026-06-30 |
| SKN-OPS-005 | Non-Conformance Report (NCR) Procedure | 1.0 | 2026-05-09 | Ratified | `sops/SKN-OPS-005-ncr-procedure.md` | `capa-coordinator/references/ncr-procedure.md` | 2027-05-09 |
| SKN-OPS-006 | Lab Quality Procedure | 1.0 | 2026-05-08 | Ratified | `sops/SKN-OPS-006-lab-quality-procedure.md` | `quality-lab-coordinator/references/lab-procedure.md` | 2027-05-08 |
| SKN-OPS-007 | Batch Lifecycle Procedure | 1.0 | 2026-05-08 | Ratified | `sops/SKN-OPS-007-batch-lifecycle.md` | `batch-lifecycle-tracker/references/batch-lifecycle-procedure.md` | 2027-05-08 |
| SKN-OPS-008 | IL / Claims / Label Procedure | 2.0 | 2026-05-12 | Ratified | `sops/SKN-OPS-008-il-claims-label-procedure.md` | `claims-il-and-label-keeper/references/il-claims-label-procedure.md` | 2027-05-12 |
| SKN-OPS-009 | Reportable Events Procedure | 1.0 | 2026-05-09 | Ratified | `sops/SKN-OPS-009-reportable-events-procedure.md` | `adverse-event-and-recall-reporter/references/reportable-events-procedure.md` | 2027-05-09 |
| SKN-OPS-010 | Supplier Onboarding Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-010-supplier-onboarding.md` | `purchasing-manager` Job 2A–2D (inline, no dedicated reference file) | 2027-08-06 |
| SKN-OPS-011 | Formula Development Stage-Gate & IL Review Gate Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-011-formula-stage-gate-il-review.md` | `asana-pd-manager/references/stage-gate-procedure.md` | 2027-08-06 |
| SKN-OPS-012 | PD Readiness → PO Request Handoff Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-012-pd-po-request-handoff.md` | `asana-pd-manager` + `purchasing-manager` Job 3a (inline) | 2027-08-06 |
| SKN-OPS-013 | Purchase Order Lifecycle Procedure (Draft to Close) | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-013-po-lifecycle.md` | `purchasing-manager` Job 3 (inline) | 2027-08-06 |
| SKN-OPS-014 | Receipt Discrepancy Investigation Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-014-receipt-discrepancy-investigation.md` | `purchasing-manager` Job 10 (inline) | 2027-08-06 |
| SKN-OPS-015 | Vendor Invoice Cost Classification & Routing Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-015-vendor-invoice-cost-routing.md` | `purchasing-manager` Job 9 (inline) | 2027-08-06 |
| SKN-OPS-016 | Receiving & Batch Creation Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-016-receiving-batch-creation.md` | `inventory-manager` Job 2 (inline) | 2027-08-06 |
| SKN-OPS-017 | Inventory Adjustment, Write-Off, and Return Disposition Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-017-adjustment-writeoff-return-disposition.md` | `inventory-manager` Job 7 (inline) | 2027-08-06 |
| SKN-OPS-018 | Monthly S&OP Run Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-018-monthly-sop-run.md` | `supply-demand-planner` (inline) | 2027-08-06 |
| SKN-OPS-019 | Inbound Shipment Receipt & Fault-Attribution Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-019-inbound-shipment-fault-attribution.md` | `logistics-manager` Flows A/B (inline) | 2027-08-06 |
| SKN-OPS-020 | Retailer Outbound ASN & Routing Compliance Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-020-retailer-outbound-asn-routing.md` | `logistics-manager` Flows C/G (inline) | 2027-08-06 |
| SKN-OPS-021 | International Outbound DTC Compliance Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-021-international-outbound-dtc-compliance.md` | `logistics-manager` Flow H (inline) | 2027-08-06 |
| SKN-OPS-022 | DTC Order Exception Routing Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-022-dtc-order-exception-routing.md` | `oc3pl-order-manager` (inline) | 2027-08-06 |
| SKN-OPS-023 | Pre-Ship OOS Hold Sync Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-023-pre-ship-oos-hold-sync.md` | `oc3pl-order-manager` (inline) | 2027-08-06 |

**PD/Ops/DTC batch ratified 2026-08-06.** SKN-OPS-011 through 023 cover Product Development, Purchasing, Inventory, Supply & Demand Planning, Logistics, and DTC/E-comm — the same "document what the skill already runs" pattern used for SKN-OPS-006 through 009, applied outside Quality for the first time. None of these six skills has a dedicated skill-side mirror file the way the Quality skills do; the working procedure text lived inline in each skill's `SKILL.md`, which is what's cited in place of a Skill-side Mirror path above. Whether any of them get a dedicated mirror file, and whether this catalog is the right long-term home for non-Quality SOPs at all, is unresolved — flagged in Open Items below.

**Canonical text moved to `sops/` on 2026-08-04.** Per that decision, `sops/*.md` — not SharePoint, not a Supabase row — is the source of truth for procedure text going forward. The **Skill-side Mirror** column is each skill's operational walk layered on top of the canonical text (job mappings, HITL gates, field maps); it is not a second source of truth and should not drift into restating procedure text the canonical file already owns. **SKN-OPS-001–004 review dates and SKN-OPS-001–003 content are carried forward from the pre-migration text as-is** — the full annual review is deferred until the rest of the SOP set (currently being authored) is populated, not run per-SOP as each one gets touched. SKN-OPS-004's canonical text was reconstructed from skill behavior rather than transcribed from a SharePoint original, and stands as the real version going forward — no reconciliation pass is planned.

**Forms (SKN-F-OPS-NNN).** Five forms sit alongside the procedures in PLM `sop_documents`, all Rev 1.0, effective 2024-06-30, on the same 2026-06-30 review cycle as SKN-OPS-001–004: F-001 CAPA Investigation Template, F-002 SAE Report Form, F-003 SAE Investigation Template, F-004 Root Cause Analysis Tools, F-005 Non-Conformance Report (NCR) Form. They were absent from this catalog until the 2026-07-29 wiki audit.

**SharePoint master path (historical, pre-2026-08-04):** `Sweet July/PD/Quality Control & Assurance/SOP/`
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
- "what SOPs are pending ratification" → "none — all nine SKN-OPS procedures are ratified. Four have no SharePoint master filed yet (005, 006, 007, 009), carried in PLM as the `pending-ratification://` sentinel; that flags an unfiled master, not an unratified SOP."
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

**Deferred per the 2026-08-04 decision:** SKN-OPS-001–004's annual review (already overdue, due 2026-06-30) does not fire per-SOP as each one is touched. It waits until the rest of the SOP set — currently being authored — is populated in `sops/`, then runs as one full review pass across everything at once. Don't open individual `[SOP Annual Review]` tasks for 001–004 in the meantime.

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
- SKN-OPS-001 through SKN-OPS-004 annual review: due 2026-06-30, overdue. Deferred per §4 until the full SOP set is populated in `sops/`, then run as one pass rather than per-SOP.
- **Non-Quality SOPs in a Quality-owned catalog.** SKN-OPS-010 through 023 cover PD, Purchasing, Inventory, Supply/Demand Planning, Logistics, and DTC/E-comm — none of them Quality's domain — but this catalog is the only SOP numbering sequence and ratification protocol that exists anywhere in the repo, so they took the next available slots here rather than starting a second prefix. Whether that's the right long-term home, or whether a separate catalog (owned by, say, an Ops or PD umbrella skill) should exist once one does, is unresolved.
- **None of the six PD/Ops/DTC skills has a dedicated skill-side mirror file.** Unlike the Quality skills (each with its own `references/skn-ops-*.md`), the working procedure text for SKN-OPS-011 through 023 lives inline in each skill's `SKILL.md` body. Whether to externalize each into its own reference file, matching the Quality pattern, is a follow-on decision, not done in this pass.
- Next available slot in the SKN-OPS-NNN sequence is **024**.
