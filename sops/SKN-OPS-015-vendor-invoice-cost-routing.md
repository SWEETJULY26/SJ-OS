---
sop_id: SKN-OPS-015
title: Vendor Invoice Cost Classification & Routing Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Vendor Invoice Cost Classification & Routing Procedure

## 1. Purpose

Define how every vendor invoice across AC Brands gets classified by cost category, routed to the systems that need visibility into that spend, and committed to the cost ledger — so spend is never invisible to the function that should be tracking it, and never committed without a documented sign-off.

## 2. Scope

Applies to every vendor invoice at AC Brands, regardless of vendor type or which function incurred the cost. Covers classification, multi-home routing, PO-bound reconciliation, and dispute handling. Does not cover the three-way PO/receipt/invoice match itself for PO-bound spend, which is SKN-OPS-013 §5.7 — this procedure covers the cost-ledger side of that same invoice, not the PO close.

## 3. Definitions

- **Cost category** — the primary spend domain an invoice is classified into: regulatory, quality, PD, ops, marketing, or general.
- **Regulatory driver** — an independent flag that adds regulatory management as an additional home regardless of cost category, for spend with regulatory significance even when coded elsewhere.
- **Multi-home routing** — placing one invoice task in more than one project so the right function sees the spend, rather than routing to a single owner.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operator** | Confirms classification, multi-home routing, subtask placement (where applicable), and every PLM write. Approves any dispute before it opens. |
| **plm-assistant** | Sole writer of the cost-ledger record; commits only after Operator approval. |

## 5. Procedure

### 5.1 Intake

An invoice is staged from its source (vendor email, direct submission, or a reconciliation sweep) into one task in the vendor invoice queue, with cost category and regulatory driver pre-classified, the document attached, and the PLM link left blank pending commit.

### 5.2 Cost categories

| Category | Covers |
|---|---|
| Regulatory | External regulatory partner retainer and review fees, compliance testing coordination, state filings, registration fees |
| Quality | Lab testing, PET, microbial panels, stability runs |
| PD | Formulation work billed separately from a PO — concept fees, sample rounds, benchtop iterations |
| Ops | Freight (forwarder, broker, parcel), fulfillment, inventory carrying costs not tied to a PO |
| Marketing | Agency retainers, content production, sampling, paid media platform fees |
| General | Fallback — legal, SaaS, banking, anything not covered above |

### 5.3 Regulatory driver override

The regulatory-driver flag is independent of cost category and always adds regulatory management as an additional home when set true — stability and compatibility testing, third-party compliance filings, and reformulation-adjacent testing are the canonical cases. When in doubt, set it true; a false positive costs a glance, a false negative costs regulatory visibility into spend that matters to them.

### 5.4 Multi-home routing

Every invoice homes to the vendor invoice queue plus, by cost category:

| Category | Additional home |
|---|---|
| Regulatory | Regulatory management, always |
| Quality | Quality management, always |
| PD | The SKU's own PD project, when a SKU link exists — as both a project home and a subtask under the SKU's master task, not either/or |
| Ops (freight) | Logistics |
| Ops (fulfillment) | Order management |
| Ops (inventory) | Inventory management |
| Marketing | Vendor-invoice-queue only, unless a dedicated marketing project exists |
| General | Vendor-invoice-queue only |

The routing is drafted per this table and confirmed by the Operator before commit — it is never applied automatically without a look.

### 5.5 The five HITL gates

1. **Classification** — cost category, regulatory driver, and any SKU link are confirmed before any PLM write.
2. **Multi-home** — the Operator confirms which downstream project(s) the task lands in; the routing table drafts it, the Operator approves or overrides.
3. **Subtask placement** (PD case only) — when a SKU link is set, the Operator confirms which master task on the SKU's project the invoice sits under.
4. **PLM write** — the cost-ledger row commits only after Operator approval, in the same transaction as the state field being set.
5. **Dispute trigger** — moving an invoice to Disputed opens a dispute task linking back to the original invoice task and notifies the vendor owner, and requires Operator approval before that branch fires.

### 5.6 State

Invoice state — Pending, Approved, Paid, Disputed, Declined, Void — lives on the invoice task and mirrors the PLM ledger record 1:1. State transitions happen through the PLM write; there are no sub-state sections.

## 6. Records

| Record | Where it lives |
|---|---|
| Invoice task | Vendor invoice queue, multi-homed per §5.4 |
| Cost-ledger row | PLM vendor invoice table, one row per invoice |
| Dispute task (if opened) | Cross-linked to the originating invoice task |
| PO-bound reconciliation link | Set on the ledger row when the invoice is tied to a PO, dedups against the SKN-OPS-013 §5.7 three-way match |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from purchasing-manager's working Job 9. | Alvin Belt |
