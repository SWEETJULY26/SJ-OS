---
sop_id: SKN-OPS-016
title: Receiving & Batch Creation Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Receiving & Batch Creation Procedure

## 1. Purpose

Define how a purchase order's goods arrival becomes a batch record in PLM — the handoff point where Purchasing's paperwork becomes physical inventory with a batch identity. This is the procedure that closes the loop opened at PO placement (SKN-OPS-013).

## 2. Scope

Applies to every receipt of goods against a Sweet July Skin purchase order at the third-party warehouse. Picks up from a PO in transit and ends with a batch record committed to PLM and the PO status flipped to Received. Does not cover the PO lifecycle itself (SKN-OPS-013), receipt discrepancies (SKN-OPS-014), or the quality-side batch lifecycle that begins once the batch exists (SKN-OPS-007).

## 3. Definitions

- **Receipt Order Report** — the warehouse's own record of a specific receiving event, the primary source document for this procedure. Its "PO difference = 0" reading means that specific receiving event was fully received — it says nothing about whether the PO overall is complete, since a PO can receive across more than one report.
- **Batch identifier** — the lot or batch code assigned to the received goods. The Receipt Order Report carries no batch column; batch identifiers always come from the receiving operator, never inferred from the report.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operations** | Reviews every receive task, confirms batch identifiers and condition notes, approves the batch entry before commit. |
| **plm-assistant** | Sole writer of the batch record; commits only after Operations approval. |

## 5. Procedure

### 5.1 Trigger

A receiving event starts on the primary signal — the warehouse's Receipt Order Report for a specific receipt order — or on a direct goods-received notification, an operator marking a PO received, or an explicit request to check for receipt reports.

### 5.2 Reading the source document

The Receipt Order Report carries line-level detail per receipt order. Two things about it matter enough to call out explicitly: it reports per receiving event, not per PO, so a fully-received report does not by itself mean the PO is complete if more than one shipment is expected; and it carries no batch column at all, so batch identifiers are always supplied by the receiving operator rather than read off the report.

### 5.3 Opening the receive task

A receive task opens holding the PO summary, expected versus received quantities by line, condition notes, batch identifiers, and any compliance-document reference (such as a certificate of analysis) attached to the shipment.

### 5.4 Batch staging and commit

The batch entry is staged in PLM and held for Operations approval. On approval: the batch record is created, supporting documents are attached, the receive task closes with a sync-back comment, and the purchase order's status is set to Received — which is what moves the PO into the receiving queue. The status field is what carries this state; the PO task is never moved by a manual section drag.

## 6. Records

| Record | Where it lives |
|---|---|
| Receive task | Inventory management queue, one per receiving event |
| Batch record | PLM batch table, created on this procedure's commit |
| PO status | Set to Received on the linked purchase order task |
| Compliance documents | Attached to the batch record |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from inventory-manager's working Job 2. | Alvin Belt |
