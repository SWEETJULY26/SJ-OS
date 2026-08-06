---
sop_id: SKN-OPS-021
title: International Outbound DTC Compliance Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# International Outbound DTC Compliance Procedure

## 1. Purpose

Define the compliance gate a cross-border direct-to-consumer parcel must clear before it ships — declaration accuracy, duty posture, and a filed regulatory reference — since an international DTC parcel fails on customs and regulatory grounds, not on carrier performance, and that failure mode needs its own procedure rather than being handled as a routine domestic shipment.

## 2. Scope

Applies to any Sweet July Skin direct-to-consumer parcel shipping to a non-US destination. Canada is the live market at ratification; the EU, UK, and Australia sit behind it and are brought into scope market by market as each is activated. Does not cover retailer outbound freight (SKN-OPS-020) or domestic DTC fulfillment, and does not cover the regulatory filing itself — that substantive work sits with the external regulatory partner and, once live, regulatory management; this procedure owns the shipping-side gate, not the filing.

## 3. Definitions

- **DDP (delivered duty paid)** — the shipper pays duties and taxes upfront; the consumer sees no surprise charge at delivery.
- **DDU (delivered duty unpaid)** — the consumer pays duties and taxes at delivery.
- **Regulatory filing reference** — the on-file confirmation that a required cross-border cosmetic notification (CNF for Canada, CPNP for the EU when active) has been filed for the shipped product.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Logistics** | Owns the cross-border partner relationship and the DDP-versus-DDU posture per market. Runs declaration accuracy enforcement and verifies the regulatory filing reference is on file before a parcel ships. |
| **External regulatory partner / regulatory management** | Owns the regulatory filing itself. Not the shipping gate — the filing that gate checks for. |
| **oc3pl-order-manager** | Surfaces the non-US destination order on the daily fulfillment report as the primary trigger. |
| **complaint-and-event-handler** | Routes a customer complaint rooted in a customs or duty experience back into this procedure. |

## 5. Procedure

### 5.1 Trigger

Three sources: a non-US destination order surfaced on the daily fulfillment report, a customs authority failure notice (held, refused, returned, abandoned) landing from the destination country, or a customer complaint about an unexpected duty charge routing back from complaint intake.

### 5.2 Shipment record

An international outbound DTC shipment record is drafted and staged for approval, separate from a domestic shipment record, because its failure mode and required fields are different.

### 5.3 Declaration accuracy enforcement

The customs declaration is checked against the cross-border partner's own template for accuracy before the parcel ships. A declaration error is the single most common cause of a held or refused international parcel, and this check exists specifically to catch it before the parcel leaves rather than after a customs authority flags it.

### 5.4 Duty posture confirmation

The shipment's duty posture (DDP or DDU) is confirmed against the standing market policy for that destination country. Posture is a per-market policy decision, not a per-shipment judgment call — it is set once per market and every shipment to that market follows it.

### 5.5 Regulatory filing gate

Before the parcel ships, the required regulatory filing reference for that market is verified on file. No parcel ships to a market requiring a filing (Canada's CNF today; the EU's CPNP once that market is active) without that reference confirmed present. This is a hard gate, not a best-effort check.

### 5.6 Failure handling

A customs authority failure (held, refused, returned, or abandoned) is logged against the shipment record, and the root cause — declaration error, posture mismatch, or missing filing — is identified before the lane resumes shipping to that destination. A duty-related customer complaint routes back through complaint intake and is cross-referenced to the shipment record here.

## 6. Records

| Record | Where it lives |
|---|---|
| International shipment record | PLM international outbound DTC table, one row per parcel |
| Duty posture per market | Standing policy reference, applied to every shipment to that market |
| Regulatory filing reference | Confirmed on file before ship, cross-referenced to the shipment record |
| Customs failure log | Logged against the shipment record when a failure occurs |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from logistics-manager's working Flow H (international outbound DTC consumer parcels). | Alvin Belt |
