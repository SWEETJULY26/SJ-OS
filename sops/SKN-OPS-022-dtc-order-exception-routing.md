---
sop_id: SKN-OPS-022
title: DTC Order Exception Routing Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# DTC Order Exception Routing Procedure

## 1. Purpose

Define the three-way split that decides who owns a DTC order problem once one surfaces — the fulfillment operator, Logistics, or end-customer intake — so an exception always lands with the party actually able to resolve it, instead of sitting with whoever happened to notice it first.

## 2. Scope

Applies to any exception on a direct-to-consumer order handled through the third-party fulfillment warehouse: a late shipment, a carrier failure, a customer-reported problem, or a return landing back at the warehouse. Does not cover retailer outbound freight or international DTC compliance, which have their own procedures, and does not cover the substantive investigation once routed — this procedure owns the routing decision, not the resolution work on either side of it.

## 3. Definitions

- **OC3PL-side issue** — an exception caused by the fulfillment warehouse itself: a late pick, a WMS glitch, a label printing failure, or the wrong carrier service selected at the warehouse.
- **Carrier-side issue** — an exception caused by the carrier in transit: a lost package, a label fail at carrier scan, an address bounce, a delay beyond standard transit, transit damage, or a claim that needs filing.
- **End-customer signal** — any report from the customer themselves about their order, regardless of underlying cause.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **oc3pl-order-manager** | Owns OC3PL-side exceptions directly. Judges fault and routes carrier-side and end-customer issues onward. Manages the operational disposition (return processing, replacement order creation, RTS handling) in parallel with any customer-facing handoff. |
| **logistics-manager** | Owns carrier-side exceptions once routed — the carrier ticket, the claim, the resolution thread. |
| **complaint-and-event-handler** | Owns end-customer intake and the customer-facing classification and response once routed. |
| **inventory-manager** | Owns the inventory disposition decision (sellable, damaged, discard) once a physical return lands. |

## 5. Procedure

### 5.1 The fault-attribution split

When an order-level problem surfaces, judge which of two categories it falls into before anything routes:

**Stays OC3PL-side:** warehouse picked late, a system glitch in the warehouse's own WMS, label printing failure at the warehouse, or the wrong carrier service selected at the warehouse.

**Routes to Logistics:** the carrier lost the package or reports it lost, a label fail at carrier scan, an address bounce or undeliverable notice, a carrier delay materially beyond standard transit, damage in transit reported by the carrier, or a claim that needs to be filed with the carrier.

The handoff to Logistics stages a task in its outbound escalations queue with status, carrier name, and a link to the related shipment record if one exists. The originating task is commented with a link to the new one and closed out on this side — the two stay cross-referenced, not merged.

### 5.2 End-customer intake

Any report coming from the customer themselves — a missing item, a damaged item, never received, wrong item shipped, or any health concern (which is also an adverse-event trigger) — routes to complaint-and-event-handler as the single intake door for end-customer quality signal, regardless of what the underlying cause turns out to be.

The customer-facing classification and response is complaint-and-event-handler's from that point. The operational disposition — return processing, a replacement order, RTS handling — stays here and runs in parallel, not sequentially: the two tracks don't wait on each other.

### 5.3 Return disposition handoff

When a return, an RTS package, or a replacement order requiring an inventory pull physically lands at the warehouse, the disposition decision (sellable, damaged, or discard) routes to inventory-manager with the SKU, quantity, condition notes, and a link back to the source return task. inventory-manager makes the call and writes any resulting inventory adjustment; the return record itself stays here.

### 5.4 What does not route here

Vendor inbound freight, customs, ASN drafting, and retailer outbound shipments are Logistics' domain from the start, not an exception routed there from DTC order management. SAE classification and any recall trigger belong to complaint-and-event-handler outright, not as a routed exception. A returns-volume pattern that looks like a forecasting signal gets surfaced as a comment to supply planning — it does not become a formal handoff.

## 6. Records

| Record | Where it lives |
|---|---|
| OC3PL-side escalation | OC3PL order management escalations queue |
| Carrier-side handoff | Logistics outbound escalations queue, cross-referenced back to the originating task |
| End-customer complaint | Complaint log, cross-referenced to any parallel operational disposition task |
| Return disposition handoff | inventory-manager task, cross-referenced to the source return task |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from oc3pl-order-manager's working handoff rules to logistics-manager, complaint-and-event-handler, and inventory-manager. | Alvin Belt |
