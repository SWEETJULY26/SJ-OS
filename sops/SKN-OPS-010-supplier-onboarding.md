---
sop_id: SKN-OPS-010
title: Supplier Onboarding Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
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
- **First-contact owner** — whoever the vendor type routes to at step 5.1 (see the routing table): Technical QA Lead, Marketing Manager, Sr. Director Consumer Strategy & Ops, or Operations. Owns the earliest contact and the Proceed/Pass call at intake.
- **PD / Ops team** — collects compliance documents from the new supplier and tracks them against the checklist in Asana.
- **VP of Operations** — approves the vendor's move from onboarding to active status.

## 5. Procedure

### 5.1 First contact and routing (documented, no task yet)

Onboarding starts the moment a new supplier is identified — a referral or introduction email, an inbound RFQ reply, or a broker (for example, a PD contractor) connecting the Operator directly with the vendor's own contact. All three count as onboarding kickoff; a formal RFQ is not a precondition. At this stage the signal is logged against the eventual supplier wiki page only — no Asana task exists yet.

Who owns first contact, and therefore who the intake task in §5.2 gets assigned to, is set by vendor type:

| Vendor type | First-contact owner |
|---|---|
| Filler, ingredient, component, lab testing | Technical QA Lead |
| Service (regulatory subtype) | Operations |
| Service (marketing / agency subtype) | Marketing Manager |
| Retailer, promotional goods, accessories | Sr. Director Consumer Strategy & Ops |
| Freight forwarder, customs broker, cross-border partner, all other service | Operations |

### 5.2 Vendor intake (task opens, Proceed/Pass gate)

The first supplier-side email in the thread, whether it is the introduction itself or the vendor's own reply, is the source record. An onboarding task opens in the Vendor Onboarding queue, assigned per the §5.1 routing table. Capture: company name, primary contact name, email, and phone, any secondary contact, mailing address, website, and vendor type (filler, component, ingredient, lab testing, promotional goods, accessories, freight forwarder, customs broker, cross-border partner, or other service).

The first-contact owner comments either **Proceed** (advance to compliance doc collection) or **Pass** (close the task — this vendor doesn't move forward). Proceed auto-generates the six compliance-document subtasks.

### 5.3 Compliance document collection

Six subtasks track the checklist: NDA, W9, COI, MSA, Banking/ACH (required for every vendor type), and MSDS (required only for filler and ingredient types). As each document lands, the matching subtask is marked complete and `vendors.onboarding_checklist` is updated to match. The jsonb field in PLM is the source of truth; the Asana subtask state mirrors it, not the other way around.

### 5.4 Gate to compliance-active

Once NDA and W9 are both on file, the vendor is ready for full activation and the onboarding task moves to the Compliance, Renewals & Disputes section. Any remaining items (COI, MSA, Banking, MSDS where applicable) do not block this move — they stay open on the vendor record and are chased separately. This is the trigger for the PLM vendor record write in §5.5.

### 5.5 PLM vendor record creation

The vendor record is staged and committed by `plm-assistant`, the sole writer to PLM, into the `vendors` table once the §5.4 gate fires. Status starts as `onboarding`. The `onboarding_checklist` field initializes with NDA, W9, COI, MSA, and Banking all `false`, plus MSDS `false` only when vendor type is filler or ingredient. No write happens without the Operator confirming the staged preview first.

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
| 1 | 2026-08-06 | Initial ratification. Added the §5.1 vendor-type first-contact routing table and the Proceed/Pass intake gate, reconciled against purchasing-manager Job 2A–2D; renumbered §5.3–5.5 into correct sequence (doc collection → gate → PLM write). | Alvin Belt |
