---
sop_id: SKN-OPS-013
title: Purchase Order Lifecycle Procedure (Draft to Close)
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Purchase Order Lifecycle Procedure (Draft to Close)

## 1. Purpose

Define the single lifecycle every purchase order walks from draft through close, so a PO is always in exactly one of a defined set of states, the state drives where it sits, and nothing has to be inferred from title text or memory. This is the purchase-to-pay spine everything else in Purchasing hangs off of.

## 2. Scope

Applies to every purchase order placed against a Sweet July Skin vendor, whether triggered by a PD readiness gate (SKN-OPS-012), an approved reorder review, or a manual request. Covers the PO from draft through invoice-matched close, including cancellation, variance handling, and both full and partial receiving. Does not cover vendor onboarding (SKN-OPS-010) or receipt discrepancy investigation, which is its own procedure (SKN-OPS-014) triggered from inside this one.

## 3. Definitions

- **PO task** — the single Asana task representing one purchase order for its entire lifecycle. Status field changes and section moves carry the state; the task is never renamed to reflect status.
- **PD request** — a separate task representing PD's own readiness gate, linked to but never merged with the PO task. See SKN-OPS-012.
- **Header-level variance** — a discrepancy in total quantity, total value, or ETA between what was ordered and what a vendor acknowledgment or invoice states, as opposed to a line-level discrepancy that doesn't move the header totals.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operations** | Reviews every PO draft, approves variance resolutions, approves cancellations, confirms receipts, and owns invoice match through to close. |
| **PD** | Owns the readiness gate that triggers a PD-linked PO placement, per SKN-OPS-012. Never owns the PO task itself. |
| **plm-assistant** | Sole writer of PLM PO, receipt, and batch records; commits every PLM-side state change this procedure calls for. |

## 5. Procedure

### 5.1 PO to place

Triggered by an approved reorder review, an NPI ramp, a manual request, or a PD readiness gate reaching Ready (SKN-OPS-012). The PO is drafted in PLM with line items, quantities, prices, and vendor terms, and the PO task opens for Operations review with status **Draft**, vendor and PLM link populated. If the PO traces to a PD request, the dependency link and the four linked-project/SKU/PLM fields are set in this same action — see SKN-OPS-012 §5.5. Operations reviews the draft; on approval, the PO is sent to the vendor.

### 5.2 PO sent

Triggered when the PO document is confirmed sent to the vendor. PLM status updates to Sent; the task moves into the in-flight queue with status **Sent**.

### 5.3 Acknowledgment received

Triggered when the vendor's acknowledgment is logged. The acknowledgment is compared against the PO at header level — total quantity, total value, ETA. Any drift on those three moves status to **Variance** and returns the task to Operations review. Line-level discrepancies that don't move a header total stay in PLM without triggering a variance. A clean acknowledgment moves status to **Acknowledged**; the task stays in the in-flight queue.

### 5.4 In transit

Triggered by the first shipping or tracking signal. Status moves from Acknowledged to **In Transit**. ETAs sync to PLM; later ETA changes log as a comment rather than a new status change unless the slip is material. The task does not change section at this point — the in-flight queue spans from issue through transit; the section move happens at receipt.

### 5.5 Cancellation

Available from any state prior to receipt, on an operator request or a vendor cancellation. Requires confirmation. On approval: PLM PO status moves to Cancelled, task status moves to **Cancelled**, and the task moves to the closed section. Before marking the task complete, check whether any other system still has open work against it (a PO multi-homed into a SKU project, logistics, or quality) — the last system to finish is the one that completes the task, per the shared task-write contract.

### 5.6 Receipt

The formal handoff where goods land, PO status flips to Received, and the batch record is created in PLM.

**PD-linked PO.** Set the PLM link on the linked PD request so the connection is visible from the PD side, but do not open a second receipt task for an ordinary full receipt — the PO task itself carries the receipt state. On notification: record the receipt reference on the PO task and set status to **Received**; PLM PO status and the batch entry are updated in the same action.

**Standalone PO (no PD link).** No separate receipt task for a single full receipt. The PO task itself carries the receipt: status moves to **Received**, landing in the receiving queue; the receipt reference and counts are recorded on the task; PLM PO status and batch entry update in the same action. The PO task stays in the receiving queue until the invoice clears.

**When a separate receipt task is correct.** Two cases only: **partial receiving**, where the ordered quantity arrives across more than one shipment on different dates or with different batch codes — each partial receipt gets its own task keyed to the PO number plus receipt date, and the PO task stays in the receiving queue until the last partial lands; and **a discrepancy** — a count variance, damage, or missing items opens a task under SKN-OPS-014, which is its own deliverable with its own close, while the receipt task stays open pending the investigation.

### 5.7 Invoice and close

Triggered when an invoice is logged. A three-way match runs against the PO, the receipt, and the invoice. A discrepancy moves status to **Variance** and returns the task to Operations review. A clean match closes the PLM PO, moves status to **Closed**, and moves the task to the closed section. Before marking the task complete, check the multi-home rule from §5.5 — an invoice match on the Purchasing side doesn't mean a linked freight leg or PD-side task is also finished. The invoice is separately logged as a cost-ledger record, which is how vendor cost tracking (SKN-OPS-015) dedups against this match.

## 6. Records

| Record | Where it lives |
|---|---|
| PO state | One Asana task per PO, Draft through Closed |
| PLM PO record | PLM purchase order table, mirrors the Asana state (not a 1:1 vocabulary match — see the caution below) |
| Receipt record(s) | PLM receipt table, one row per receipt event; multiple rows on a partial receiving PO |
| Batch record | Created in PLM at first receipt against the PO |
| Invoice / cost ledger row | PLM vendor invoice table, linked back to the PO for the three-way match |

**Caution.** The Asana status field and the PLM PO status column are not guaranteed to carry identical option sets — some Asana-side states (In Transit, Received, Variance, Dispute, On Hold) have no PLM counterpart in active use. Never write an Asana-only status value into PLM on the assumption it's valid there; confirm the live PLM vocabulary first.

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from purchasing-manager's working Job 3 (PO lifecycle, sub-flows 3a-3f). | Alvin Belt |
