📦 PLM Triage — July 13–20, 2026 (last 7 days)
Found 17 PLM-bound emails (14 received, 3 sent), plus 19 Ramp invoice notifications reviewed for Flow I.

🚨 URGENT
None. No failing test results, no launch-critical ship date slips, no batch inside the 30-day pull window, no compliance doc expiring within 30 days.

📋 PURCHASE ORDERS (Flow A)
• 📥 e.reyes@elementpackaging.com | RE: [External] PO #100338 — Soursop Components (7/15, 7/15, 7/17)
  → PO #100338 (Soursop Vitamin C Serum components, status "Sent") — customs broker (GOGO) coordinating cargo drop-off at Ningbo CFS (UPDATE: logistics note / status)
  → Asana sync-back: Soursop Vitamin C Serum PD task

• 📥 e.reyes@elementpackaging.com | RE: [External] SJS Pava Toner / PO# 100346 - PAVA TONER (7/15)
  → PO #100346 (Pava Toner, status "Sent") — goods ready 7/30, packing list + commercial invoice attached, transportation mode needs Alvin's confirmation (UPDATE: ship date/status)
  → 📎 Attach manually to PLM: packing list + commercial invoice (from Element Packaging, 7/15)
  → Asana sync-back: Pava Toner PD task

• 📥 e.chien@elementpackaging.com | RE: [External] SJS Pava Toner / PO# 100346 (7/13)
  → PO #100346 — Element needs a second signed PPS (production part specification) for their records (UPDATE: doc-outstanding note)
  → Asana sync-back: Pava Toner PD task

• 📤 alvin@ac-brands.com → GOGO Customs / pkggroup.com / iks-usa.com | Re: Deposit Invoice for Sweet July PO# 100310 (Production Order) (7/17)
  → PO #100310 (status "Acknowledged") — deposit invoice referenced inbound to Alvin's coordination with broker; Alvin asked to be notified on landing for 3PL booking. Invoice reference only — no cost capture in this thread (Flow F note on PO #100310, not a Flow I write)
  → Asana sync-back: none identified (no active PD task match surfaced)

📋 FORMULA / ARTWORK APPROVALS (Flow D)
• 📤 alvin@ac-brands.com → braya@kdc-one.com, perrinecalvet@milinycbeauty.com, gdvecchia@kdc-one.com, callen@kdc-one.com, yesantos@kdc-one.com | Re: Sweet July (7/17)
  → SKU LTP-001 (Lip Treatment — Pineapple Punch) — Alvin approved F&A (Filled & Assembly spec) with exceptions: shipper not yet approved, brand name correction ("Sweet July" not "Sweet July Skincare"), UPC barcode field needed, SKU field needs correction. This is a conditional approval, not a clean sign-off (UPDATE product record: F&A status = approved-with-corrections, approver = Alvin, decision date = 2026-07-17)
  → Cross-flag to `outlook-asana-bridge`: no stage move — corrections are still outstanding, task should stay in current stage until KDC returns the corrected F&A

• 📥 braya@kdc-one.com | RE: Sweet July (7/14)
  → Discussion of batch-code convention (last digit of batch code = number of batches filled) — a documentation/scheme clarification, not a batch event. No PLM write proposed; noted for context only.

📋 COMPONENT / BOM UPDATES (Flow G)
• 📥 gdvecchia@kdc-one.com | Re: Pineapple Punch Lip Treatment PO & BOM update (7/14)
  → Pineapple Punch Lip Treatment (LTP-001) — KDC confirmed receipt of a BOM update Alvin sent; content of the actual BOM change lives in Alvin's outbound message (not captured in this search window — recommend pulling the original outbound BOM email if not already logged)
  → Asana sync-back: Pineapple Punch Lip Treatment PD task

• 📥 katie@consolidateddesign.com | QUOTE: Sweet July x JULY UC Combo (7/15)
  → Component quote for uncoated packaging on Soursop (Serum) UC, Pava Toner UC, Rum Cake Lip Treatment UC (CAD#4437, #4436, + one more) — proposes UPDATE on component records with quoted cost/CAD refs, pending Alvin sending art + PO
  → No material cost shift stated yet (quote stage) — no margin cross-flag until a firm cost lands

• 📥 katie@consolidateddesign.com | Re: SJS Secondary Packaging, Finish Transition (7/14)
  → Secondary packaging finish transition affecting multiple Lip Treatment SKUs (Lychee, Guava, Essential, Rum Cake uncoated + associated Tinted Lip Treatments) — component spec/finish change in planning; no firm spec numbers to write yet
  → Asana sync-back: Lip Treatment Discovery / packaging PD task

• 📥 aldemarco@hctusa.com / dgreco@hctusa.com | RE: Lip Treatment Color match samples - Tube & UC (7/13, 7/14 x2, 7/16 x3, 7/17)
  → Tube-ready dates confirmed: Lychee 7/31, Guava 8/07, Essential [date cut off in body] — proofs sent for Jamaican Cherry, Fig, Sorrel (tinted lip treatments) for Alvin's sign-off; CofC (Certificate of Conformance) for tubes delivered to KDC's Greg Della Vecchia on 7/15
  → No firm component-spec value change to write yet (dates/samples, not a spec update) — recommend re-checking after Alvin returns signed proofs
  → Asana sync-back: Tinted Lip Treatment (Jamaican Cherry / Fig / Sorrel) PD tasks + Lychee/Guava/Essential/Rum Cake UC tasks

📋 VENDOR UPDATES (Flow C)
• 📥 jdayen@kdc-one.com | Client services contact (7/20)
  → New KDC/One contact, Jessica Dayen (Director, Sales — Specialty Beauty), introducing herself. KDC/One already exists in PLM as a vendor — proposes adding Jessica as a new contact_email slot on the existing vendor record (UPDATE, not INSERT)
  → Alvin has already replied (thumbs-up reaction) — low urgency

📋 TEST RESULTS (Flow E)
None this week. No lab result emails (pass/fail) landed in the window.

📋 INVOICES — PO-bound reference only (Flow F)
• 📤 (see PO #100310 entry above under Purchase Orders — deposit invoice referenced, no cost capture proposed here)

📋 VENDOR INVOICES — COST LEDGER (Flow I)
• 📥 amcgeough@essextesting.com | ETC Invoices S277-60823-60825-1 Sweet July: RIPT Sweet July panel 26354 (7/13)
  → Essex Testing — RIPT panel invoice, direct vendor email with attachment
  → cost_category: quality (lab_testing vendor + RIPT keyword) · regulatory_driver: true (RIPT match)
  → linked_sku: — (not stated in summary; attachment likely specifies)
  → po_link: — (not a PO-bound invoice)
  → 🔁 Dedup: clean — no matching invoice_number in `vendor_invoices`
  → Multi-home proposal: Vendor Invoices + SJS Quality Management + SJS Regulatory Management

• 📥 communications@ramp.com | Approval needed: Bill for Essex Testing Clinic, Inc. — 8 distinct invoice numbers (S277-60823-1, -931-1, -932-1 ×2, -933-1, -934-1, -935-1, -936-1 ×2) spanning 7/13–7/17
  → Same vendor/category as above: cost_category quality, regulatory_driver true (RIPT test house)
  → 🔁 Dedup: clean against `vendor_invoices` for all checked numbers — none currently logged
  → Note: several of these subject lines repeat (60932-1, 60936-1 each appear twice with slightly different timestamps) — likely Ramp re-sends, not separate invoices. Recommend de-duplicating by invoice number before staging, not by email count.
  → Multi-home proposal: Vendor Invoices + SJS Quality Management + SJS Regulatory Management

• 📥 communications@ramp.com | Approval needed: Bill for KA&F Group, LLC #20926768 (7/15)
  → Matches vendor "KAF" in PLM (contact: adam@kafhome.com)
  → cost_category: general (no vendor_type on file to refine further — flag for Alvin to confirm KAF's vendor_type) · regulatory_driver: false
  → 🔁 Dedup: clean
  → Multi-home proposal: Vendor Invoices (purchasing-manager Job 9 to confirm SKU/PO link, if any)

• 📥 communications@ramp.com | Approval needed: Bill for Orange County 3PL #17074 (7/17)
  → Matches partner "OC3PL" (wiki partner page, not a PLM vendor record)
  → cost_category: ops (fulfillment) · regulatory_driver: false
  → 🔁 Dedup: clean
  → Multi-home proposal: Vendor Invoices + OC3PL Order Management (ops)

• 📥 communications@ramp.com | Bills for Studebaker Brackett PLLC, Erin Entrup, LACY REDWAY INC., WILHELMINA INTERNATIONAL INC., a Hotels.com memo request, a TikTok Ads spend alert, and a funds-issued notice for "Apple" (various dates 7/14–7/20)
  → None of these senders/payees match a PLM vendor, partner, or contact in the run-time lexicon. Per the entity-discovery rule, these are new/unrecognized entities rather than automatic non-matches — surfacing rather than dropping:
    - Studebaker Brackett PLLC — reads as a law firm (legal spend, likely out of PLM scope entirely)
    - Erin Entrup — reads as a person/contractor, not a PLM vendor
    - LACY REDWAY INC. — unrecognized; could be a new vendor or a talent/agency payment — needs Alvin's call before any PLM action
    - WILHELMINA INTERNATIONAL INC. — unrecognized; reads as a modeling/talent agency (marketing spend), likely out of PLM scope
  → No PLM write staged for any of these — flagging only. If any of these are genuinely PD/Ops vendors, say so and I'll route through Flow C (new vendor) before Flow I can log the invoice.

📨 OUTLOOK-ASANA-BRIDGE CROSS-FLAGS
• Nicole Iturbe's $1,040 TikTok Ads spend alert (Ramp, 7/15) → marketing spend signal, not PLM-bound → outlook-asana-bridge / sjs-comp-intel-adjacent, for awareness only.
• "Ops Download, Alvin x Ciarra" recurring session setup (Sent Items, 7/20) → internal Ops handoff cadence, not PLM-bound → no action here.
• S&OP invite, SJS Builder Session invites, Nicole 1:1 (Sent Items, 7/15–7/17) → recurring internal meetings, not PLM-bound → no action here.

---

🩺 QUALITY CROSS-FLAGS
None beyond the Essex Testing RIPT invoices already logged under Flow I above (regulatory_driver true covers the cross-reference — no separate failing-result signal this week).

📜 REGULATORY CROSS-FLAGS
None. No Pedrero, MoCRA/FDA, or retailer-attestation emails landed in the window.

💰 MARGIN CROSS-FLAGS
None with a firm number attached. The Consolidated Design West UC quote (Flow G above) is cost-relevant but is still at the quote stage — no committed cost shift to trigger margin-pressure-test yet. Flag for a second pass once Alvin sends art + PO and CDW returns firm pricing.

---

Notes on scan coverage:
- Sender-domain sweep covered all 21 vendors with a contact_email on file, plus the 15 partner wiki pages with identifiable domains, plus Ramp. No email traffic found this week for: AMR Labs, Capsum, Innovative Korean Solutions, Consumer Product Testing, Impress Communications, Vegelabs, Xelapack, Pedrero Regulatory, Eurofins. Uline, Tinsol, KDC/One (Chem-Aid), and Product Integrity Laboratory have no contact_email on file, so no domain search could run for them — recommend adding contact emails to the vendor record if mail from them needs to be caught automatically.
- Attempted a NetSuite-relay sweep (`sent-via.netsuite.com`) — no hits this week.
- Attempted an `OC3PL` folder sweep by name — that folder name isn't recognized in this mailbox (tool returned "Folder with name OC3PL not found"). OC3PL-related signal was instead caught via the Ramp Orange County 3PL invoice and would need a corrected folder name to sweep directly next time.
- Sent Items was swept and returned 43 total matches for the week; the first 25 (newest-first) were reviewed in full. The remaining ~18 are older in the week and mostly recurring-meeting or personal-admin threads (Apple trade-in, HR check-ins) based on the pattern of what surfaced — recommend a follow-up pass if you want the tail end double-checked for anything PLM-bound.
- No Pedrero, Finance-folder (Calm HR / Shopify Billing), or Commerce → Thirteen Lune topic-folder sweeps were run by folder name this pass, since sender-domain coverage across the vendor/partner lexicon already reached Ramp and the relevant vendor traffic; a named-folder sweep can be added if you want belt-and-suspenders coverage.

---

Which should I push? (say "all", list numbers, or "skip")
PLM writes commit via plm-assistant. Cross-flags route to their destination skills.

Nothing was written to PLM, Asana, or anywhere else in this pass — this is the triage report only, per your read-only review request. Once you tell me which items to push, I'll stage each confirmed write and hand it to plm-assistant.
