---
sop_id: SKN-OPS-020
title: Retailer Outbound ASN & Routing Compliance Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Retailer Outbound ASN & Routing Compliance Procedure

## 1. Purpose

Define how an outbound retailer shipment gets its advance ship notice and routing request drafted, sent, and tracked to delivery confirmation — the lane that gates a wholesale or retail-vendor launch, since a retailer will not accept a non-compliant shipment.

## 2. Scope

Applies to any outbound shipment to a wholesale or retail-vendor partner (a retailer's own distribution center or vendor portal) once a retailer purchase order has arrived. Does not cover DTC consumer parcels (domestic or international), inbound shipments, or carrier escalations on an already-shipped outbound order, which route through their own procedures.

## 3. Definitions

- **ASN (advance ship notice)** — the structured shipment notification a retailer requires ahead of or alongside a delivery, formatted to that retailer's own specification.
- **Routing request** — the request to the retailer (or their designated carrier) for shipment routing instructions, required by most retailers before freight moves.
- **Retailer compliance spec** — the structured, PLM-held extraction of a retailer's routing guide: lead time, ASN format, pallet spec, label spec and placement, hazmat rule, and overage tolerance.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operations or Order Ops** | Reviews and sends the ASN and routing request; tracks delivery confirmation to close. |
| **Logistics** | Drafts the ASN and routing request against the retailer's structured compliance spec; stages both for review. |

## 5. Procedure

### 5.1 Trigger

Fires when a retailer purchase order arrives, or on an explicit request to prepare an outbound shipment to a retailer.

### 5.2 Drafting against the compliance spec

The retailer's structured compliance spec — not the routing guide PDF directly — is read to draft the ASN in the retailer's required format. The routing-request email is drafted alongside it. Both are staged, never sent automatically.

### 5.3 Review and send

Operations or Order Ops reviews both drafts and sends. The send is picked up and logged as a shipment record, lane-typed as retailer-outbound.

### 5.4 Tracking to close

Delivery confirmation is tracked back from the retailer's distribution center. The shipment closes once delivery is confirmed as posted.

### 5.5 Keeping the compliance spec current

When a retailer's routing guide is updated — a new lead time, a changed ASN format, a new overage tolerance — the guide is parsed for what changed and the structured compliance spec is updated to match. The source PDF is retained for reference; the structured spec is what every ASN draft is checked against going forward. Enforcement always runs against the structured spec, never against the PDF directly.

## 6. Records

| Record | Where it lives |
|---|---|
| Retailer compliance spec | PLM retailer compliance spec table, one row per retailer, structured fields |
| Routing guide source document | SharePoint logistics folder, retained as the reference the structured spec was extracted from |
| Shipment record | PLM shipments table, lane-typed retailer-outbound |
| ASN and routing-request drafts | Staged in the Logistics project pending send |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from logistics-manager's working Flow C (outbound retailer ASN and routing) and Flow G (retailer compliance spec management). | Alvin Belt |
