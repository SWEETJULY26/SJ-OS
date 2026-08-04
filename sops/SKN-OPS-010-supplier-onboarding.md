---
sop_id: SKN-OPS-010
title: Supplier Onboarding Procedure
revision: "1"
status: draft
owner: Alvin Belt, VP of Operations
effective_date: null
next_review_date: null
---

# Supplier Onboarding Procedure

## 1. Purpose

This procedure defines how AC Brands identifies, records, and activates a new Sweet July Skin supplier, from first contact through full vendor status in the PLM. It exists to make sure every supplier that touches product, packaging, or the supply chain has a complete record before AC Brands transacts with them, and that the record is created the same way every time regardless of who receives the introduction.

## 2. Scope

Applies to any new external supplier of components, materials, finished goods, packaging, labor, or services to Sweet July Skin, however AC Brands first makes contact with them: direct outreach, RFQ response, referral from an existing partner, or introduction by a broker or contractor. Does not cover onboarding of AC Brands employees or contractors, and does not cover changes to an existing active vendor's contact information, which is handled as a standard PLM update rather than an onboarding event.

## 3. Definitions

- **Onboarding status** — the vendor lifecycle state in PLM, either `onboarding` or `active`.
- **Onboarding checklist** — the six-item compliance document set tracked per vendor: NDA, W9, COI, MSA, Banking, MSDS.
- **Compliance-active gate** — the point at which NDA and W9 are both on file and the vendor is cleared to move out of the Vendor Onboarding queue.
- **Broker introduction** — a case where a third party (a PD contractor, agency, or existing partner) connects AC Brands directly with a new supplier's own contact, with or without a preceding formal RFQ.
- **Sole PLM writer** — `plm-assistant`, the only path by which any record in the PLM database is created, updated, or deleted.

## 4. Responsibilities

- **Operator** (Alvin Belt, VP of Operations) — runs intake from the first supplier email, confirms the staged PLM vendor record, and gives final sign-off on activation.
- **PD / Ops team** — collects compliance documents from the new supplier and tracks them against the checklist in Asana.
- **VP of Operations** — approves the vendor's move from onboarding to active status.

## 5. Procedure

### 5.1 Trigger

Onboarding starts the moment a new supplier is identified, by any of the following: a referral or introduction email, an inbound RFQ reply, or a broker (for example, a PD contractor) connecting the Operator directly with the vendor's own contact. All three count as onboarding kickoff. A formal RFQ is not a precondition.

### 5.2 Intake

The first supplier-side email in the thread, whether it is the introduction itself or the vendor's own reply, is the source record. Capture: company name, primary contact name, email, and phone, any secondary contact, mailing address, website, and vendor type (packaging, filler or ingredient, lab or testing, service, freight, or other).

### 5.3 PLM vendor record creation

The vendor record is staged by the `outlook-plm-bridge` skill (Flow C) and committed by `plm-assistant`, the sole writer to PLM, into the `vendors` table. Status starts as `onboarding`. The `onboarding_checklist` field initializes with NDA, W9, COI, MSA, and Banking all `false`, plus MSDS `false` only when `vendor_type` is `filler` or `ingredient`. No write happens without the Operator confirming the staged preview first.

### 5.4 Compliance document collection

Progress is tracked as an Asana task in the Vendor Onboarding section, mirroring the same six-item checklist used in PLM. As each document lands (NDA, W9, COI, MSA, Banking, MSDS), the matching Asana subtask is marked complete and `vendors.onboarding_checklist` is updated to match. The jsonb field in PLM is the source of truth; the Asana subtask state mirrors it, not the other way around.

### 5.5 Gate to compliance-active

Once NDA and W9 are both on file, the vendor is ready for full activation and the onboarding task moves to the Compliance, Renewals & Disputes section. Any remaining items (COI, MSA, Banking, MSDS where applicable) do not block this move. They stay open on the vendor record and are chased separately.

### 5.6 Commercial artifacts

Quotes, RFQ responses, and cost sheets are logged by reference in the vendor's PLM notes and in the wiki artifact ledger, but the files themselves are stored in SharePoint, in the vendor's supplier folder, not in Supabase storage. Once a document is filed in SharePoint, the PLM note and wiki entry should carry the link to it.

### 5.7 Wiki layer entry

Every PLM vendor create or update automatically generates or appends to that supplier's wiki page (slug `supplier/<vendor-name>`) as a factual, ledger-style artifact trail. This step is standing and automatic. It is part of the onboarding workflow by default, run immediately after the PLM write in the same session, and does not require a separate request each time.

### 5.8 Activation

Status flips from `onboarding` to `active` once compliance documents clear (NDA and W9 at minimum, the full checklist for regulated vendor types) and either a purchase order or a confirmed sample or line trial commitment exists.

### 5.9 Ownership

The Operator runs intake, PLM staging, and confirmation. The PD or Ops team collects compliance documents. The VP of Operations approves final activation.

## 6. Records

| Record | Where it lives |
|---|---|
| Vendor master record | `public.vendors` (PLM), one row per supplier, status `onboarding` to `active` |
| Onboarding checklist state | `vendors.onboarding_checklist` (jsonb), mirrored by Asana subtasks in the Vendor Onboarding section |
| Compliance documents | `vendor_compliance_docs` (PLM) plus SharePoint supplier folder |
| Commercial artifacts (quotes, RFQs, cost sheets) | SharePoint supplier folder, referenced by link in vendor notes |
| Supplier wiki page | `public.wiki_pages`, slug `supplier/<vendor-name>`, ledger-style artifact trail |
| Audit trail | `public.audit_logs`, automatic on every vendor insert or update |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | (unreleased) | Initial draft. | Alvin Belt |
