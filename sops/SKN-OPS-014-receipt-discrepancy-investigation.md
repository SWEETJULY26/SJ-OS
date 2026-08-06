---
sop_id: SKN-OPS-014
title: Receipt Discrepancy Investigation Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Receipt Discrepancy Investigation Procedure

## 1. Purpose

Define the single, consistent path for investigating and resolving any count variance, damage, or missing-items signal discovered when a purchase order's goods are received, so that the resolution — and, where it applies, the escalation into a formal corrective action — happens the same way every time.

## 2. Scope

Applies to any receipt-time discrepancy on a Sweet July Skin purchase order: quantity short or over, physical damage, or missing items. Triggered from inside the receiving step of the PO Lifecycle Procedure (SKN-OPS-013) — this procedure never runs standalone; it always traces back to a specific PO and receipt event. Does not cover carrier-attributable freight issues in transit, which route through logistics (SKN-OPS-019), or a formal CAPA once one opens, which SKN-OPS-001 owns from that point forward.

## 3. Definitions

- **Discrepancy task** — the record of one receipt-time issue on one PO: a count variance, damage, or missing items.
- **Resolution** — the outcome of the investigation, one of four: Vendor Credit, Replacement Shipment, Accepted As-Is, or Escalate to CAPA.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operations** | Investigates every discrepancy, communicates with the vendor, documents findings, and selects the resolution. |
| **logistics-manager** (or OC3PL directly) | Flags a vendor-attributable receipt issue when the discrepancy surfaces at the freight or fulfillment handoff rather than being spotted by Operations directly. |
| **capa-coordinator** | Receives the handoff and opens the formal CAPA when the resolution is Escalate to CAPA. |

## 5. Procedure

### 5.1 Trigger

A discrepancy task opens whenever: logistics flags a vendor-attributable receipt issue (count variance, damage, missing items); OC3PL flags one directly; or Operations opens one manually after spotting a discrepancy on receipt. The receiving task on the PO stays open while the discrepancy is investigated — receiving does not close around an unresolved discrepancy.

### 5.2 Opening the discrepancy

The task carries the PO number, vendor, discrepancy type, and a description of what was found. If the PO carries other homes (for example, a PD-linked project), the discrepancy task joins those same homes so anyone already tracking the PO sees the issue without needing to be told separately. Prior vendor quality history is pulled before drafting, so recurring patterns are visible from the first read rather than discovered later.

### 5.3 Investigation

Operations investigates, communicates directly with the vendor, and documents findings as the investigation proceeds. Nothing about this step is automated — it is a judgment-driven conversation with the vendor, recorded as it happens.

### 5.4 Resolution

Four outcomes, and only these four:

- **Vendor Credit** — the vendor issues a credit against the discrepancy.
- **Replacement Shipment** — the vendor ships replacement goods for the shortfall or damaged units.
- **Accepted As-Is** — the discrepancy is acknowledged but doesn't warrant a vendor remedy; goods are accepted as received.
- **Escalate to CAPA** — the discrepancy is significant enough, or part of a pattern, to warrant a formal corrective action.

### 5.5 CAPA handoff

On Escalate to CAPA, the discrepancy is handed to capa-coordinator with the vendor, PO, batch, damage type, and observed date. capa-coordinator opens the formal CAPA per SKN-OPS-001 and cross-links back to the source discrepancy task — the discrepancy record and the CAPA record stay linked, not merged.

### 5.6 Vendor scorecard feed

On close, regardless of which resolution was chosen, the outcome is logged as an event line on the vendor's own record — this is the same record that vendor performance reviews read from. A pattern of discrepancies against one vendor surfaces here before it would surface anywhere else.

## 6. Records

| Record | Where it lives |
|---|---|
| Discrepancy task | Purchasing queue, cross-homed to any other project the PO already belongs to |
| Resolution | Recorded on the discrepancy task at close |
| CAPA link (if escalated) | Cross-referenced between the discrepancy task and the CAPA record |
| Vendor event history | Vendor's own ledger record, feeding vendor performance reviews |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from purchasing-manager's working Job 10. | Alvin Belt |
