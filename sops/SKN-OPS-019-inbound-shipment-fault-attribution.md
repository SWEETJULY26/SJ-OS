---
sop_id: SKN-OPS-019
title: Inbound Shipment Receipt & Fault-Attribution Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Inbound Shipment Receipt & Fault-Attribution Procedure

## 1. Purpose

Define the inbound shipment lifecycle for both finished goods and components, and — critically — the fault-attribution rule that decides who owns a receipt-side problem once one shows up. Getting this rule wrong sends a vendor-caused problem to the wrong owner or leaves a carrier claim unfiled.

## 2. Scope

Applies to every inbound shipment from a contract filler (finished goods) or a component supplier, from first tracking signal through receipt confirmation. Covers both the routine lifecycle and the receipt-side discrepancy fork. Does not cover the vendor-side investigation and resolution once a discrepancy is attributed to the vendor — that is SKN-OPS-014's procedure, triggered from inside this one.

## 3. Definitions

- **Finished-goods lane** — an inbound shipment from a contract filler destined for the fulfillment warehouse.
- **Component lane** — an inbound shipment of packaging or raw material destined for a filler, not the fulfillment warehouse. More often customs-heavy, since several component suppliers ship from Asia.
- **Carrier-attributable issue** — transit damage, lost cartons, or mishandling — a problem caused in transport, not by the vendor's own packing or fulfillment of the order.
- **Vendor-attributable issue** — a short ship against the PO, wrong items, vendor packing damage, or a quality fail discovered at receipt — a problem caused by the vendor before the shipment left their hands.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operations** | Approves every shipment record, every ETA update, and every fault-attribution judgment before it commits or routes. |
| **purchasing-manager** | Owns the vendor conversation, resolution, and any CAPA escalation for a vendor-attributable discrepancy. |
| **inventory-manager** | Confirms physical landing at receipt and receives the handoff back on close. |

## 5. Procedure

### 5.1 Detection

An inbound shipment is detected one of three ways: a PO-ships signal from the purchase order lifecycle, a carrier ship-notification email, or a tracking number provided directly.

### 5.2 Shipment record

A shipment record is drafted holding the lane (finished-goods or component), the linked PO, carrier, tracking number, ETA, origin (the filler or component supplier), and destination (the fulfillment warehouse for finished goods, the filler itself for components). The record is staged for approval and commits only after Operations signs off.

### 5.3 ETA updates

Subsequent ETA changes from carrier emails are detected, staged, and committed the same way as the original record — nothing about mid-transit tracking bypasses the approval step.

### 5.4 Receipt confirmation and close

On carrier-confirmed delivery and inventory management's confirmation of physical landing, the handoff fires back to inventory management (finished goods) or the filler's own component intake (components), and the shipment closes.

### 5.5 Receipt-side discrepancy fork

When a receipt-side issue surfaces — count variance, damage, or missing items — fault is judged before anything routes further:

**Carrier-attributable** (transit damage, lost cartons, mishandling) stays in Logistics. A carrier ticket opens, the claim runs, and the resolution thread tracks to close.

**Vendor-attributable** (short ship against the PO, wrong items, vendor packing damage, a quality fail found at receipt) is not Logistics' to resolve. The receipt facts — PO reference, receipt reference, discrepancy type, and observed date — hand off to Purchasing, which opens the discrepancy investigation under SKN-OPS-014. Purchasing owns the vendor conversation, the resolution, and any CAPA escalation from that point forward; Logistics steps back once the handoff is made.

### 5.6 Component-specific handling

For a component-lane shipment, customs is more often in play — component suppliers frequently ship from Asia. A component shortfall risk surfaces back to supply planning through the linked component forecast, independent of whether a discrepancy is also in play.

## 6. Records

| Record | Where it lives |
|---|---|
| Shipment record | PLM shipments table, one row per shipment, lane-typed finished-goods or component |
| Discrepancy handoff (if vendor-attributable) | Cross-referenced with the Purchasing discrepancy task opened under SKN-OPS-014 |
| Carrier claim (if carrier-attributable) | Logistics carrier-ticket trail, tracked to close |
| Component shortfall signal (if applicable) | Linked component forecast entry |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from logistics-manager's working Flows A and B, including the receipt-side discrepancy fork. | Alvin Belt |
