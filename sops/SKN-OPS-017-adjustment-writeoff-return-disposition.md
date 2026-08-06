---
sop_id: SKN-OPS-017
title: Inventory Adjustment, Write-Off, and Return Disposition Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Inventory Adjustment, Write-Off, and Return Disposition Procedure

## 1. Purpose

Define one shared approval pattern for the three ways a position can change outside a normal receipt or shipment: a manual count correction, an expiry or damage write-off, and a return disposition decision. All three change what PLM says is on hand, so all three get the same discipline before they commit.

## 2. Scope

Applies to any manual inventory adjustment, any batch write-off, and any return-material-authorization disposition for Sweet July Skin inventory. Does not cover the routine receiving flow (SKN-OPS-016) or the quality-side decision on a near-expiry batch, which SKN-OPS-007 §7 owns — this procedure covers the operational write-off action that follows that quality call, not the call itself.

## 3. Definitions

- **Adjustment** — a manual correction to on-hand quantity at a location, not tied to a receipt, shipment, or write-off.
- **Write-off** — the removal of a batch from on-hand position due to expiry or damage.
- **Return disposition** — the decision on what happens to a returned unit: sellable (back to on-hand) or quarantined (held in a logical quarantine location, out of sellable position).

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operations** | Approves every adjustment, write-off, and return disposition before it commits. |
| **plm-assistant** | Sole writer of the position change; commits only after Operations approval. |

## 5. Procedure

### 5.1 Three intake paths, one pattern

- **Manual count adjustment** — triggered by a physical count discrepancy or a direct request to correct a SKU's on-hand quantity at a location.
- **Write-off** — triggered by an expired batch, damage found in the field, or a quality-side pull decision (SKN-OPS-007 §7) reaching its operational action.
- **Return disposition** — triggered by a returned unit landing back at the warehouse, whether flagged by order management or discovered directly.

Each path opens its own task type, but all three follow the same shape: stage the write, hold for approval, commit on approval.

### 5.2 Task contents

Every task, regardless of type, carries the quantity involved, the reason, and source evidence — a count sheet, a photo, or return notes. A return disposition task additionally carries a proposed disposition (sellable or quarantined) for Operations to confirm or override.

### 5.3 Approval and commit

Operations reviews and approves. On commit: the adjustment, write-off, or return disposition is written to PLM. A sellable return becomes available on-hand again at the warehouse. A quarantined return sits in a quarantine logical location, out of sellable position. A write-off leaves the position entirely — it does not sit in any location afterward.

## 6. Records

| Record | Where it lives |
|---|---|
| Adjustment task | Inventory management queue, one per correction |
| Write-off task | Inventory management queue, cross-linked to the source batch record |
| Return intake task | Inventory management queue, keyed to the RMA number and SKU |
| Position change | PLM inventory/position tables, committed on approval |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from inventory-manager's working Job 7. | Alvin Belt |
