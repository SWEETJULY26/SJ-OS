# Outlook → Asana Bridge — "Allure Labs flagged a PET fail on Castaway Cream"

## Email search result: no matching email found

I searched Outlook (Inbox + Sent Items, all folders) for this and came up empty:

- `query: "Castaway Cream PET fail"` and `query: "PET fail"` — no hits tied to Castaway Cream or Allure Labs.
- `sender: allurelabs` — 10+ results, all from Brett Daly, Priyanka Kulkarni, Orlando Perez, and Brianna at Allure Labs, but every thread is about **Coffee Fix Eye Cream** (COA requests, coffee RM procurement) and packaging (tube requests, unit carton destroy list, inventory reports). Nothing about Castaway Cream or a PET (long-term stability) test failure.
- `sender: amrlabs` — this is the vendor actually tied to Castaway Cream in Asana (formula 7576C), but their recent threads are about Pava Toner POs and Coffee Peptide Eye Cream samples, not a PET fail either.

One more thing worth flagging before I log anything: **Allure Labs doesn't appear to be Castaway Cream's manufacturer.** Per the vendor lexicon and Asana, Castaway Cream Daily Moisturizer runs through **AMR Labs**. Allure Labs' relationship with us is Coffee Fix Eye Cream and related packaging. So either the sender in this request is off, or this is a new/undocumented Allure Labs touchpoint on Castaway Cream I haven't seen land yet. Worth double-checking with whoever flagged this before it goes in the log — I don't want to open a lab-finding record against the wrong vendor.

Since no real email backs this up, here's the classification and routing I'd apply if the scenario is accurate as described — so you can sanity-check the logic even though nothing's been pushed.

---

## Classification

**Labels:** `quality`, `pd`, `plm`
**Primary (safety wins the parent slot):** `quality`
**Secondary:** `pd` (comment on the PD-side product task), `plm` (cross-flag for product/batch test fields)

Signal: "PET fail" = failing long-term/shelf-life stability test result → hits the `quality` row in the signal table directly ("PET fail," any failing test result) and the received-email action-shape row "Lab result — failing (OOS/OOT/RIPT positive/PET fail/stability fail)."

---

## Confirmation preview — NOT executed (read-only run)

### Parent action — Quality queue
**Project:** SJS Quality Management (`1214660401644163`)
**Owner:** quality-lab-coordinator
**Proposed action:** Open a new lab-finding task (or, if Alvin confirms Allure Labs is in fact tied to a Castaway Cream lot, log directly against the existing stability record):

- **Task name:** `[Lab Finding] Castaway Cream — PET fail (Allure Labs)`
- **Section:** Batch — Stability Schedule (same section as the existing PET testing task, gid `1213487706215947`, "Perform PET Testing for Toner, Cleanser, Irie Power Oil, Castaway Cream, Soursop Vit C, and Good Youth Serum to Support Shelf-Life Extension")
- **Custom fields to set:**
  - Classification: OOT (or OOS, depending on which spec the PET result missed — needs confirmation)
  - Severity: Major (default assumption for a stability fail on an in-market SKU — confirm with QA Lead)
  - Source: `lab-OOT` (or `lab-OOS`)
  - Linked SKU: Castaway Cream Daily Moisturizer (SKU `165005171992`)
  - Linked Vendor: Allure Labs (**flagged above as a mismatch — needs Alvin's confirmation**)
  - Linked Batch: likely batch `875502` — the only active in-market Castaway Cream batch tracked in `[Batch Lifecycle] Castaway Cream — 875502` (gid `1214667239475040`, AMR Labs formula 7576C, produced 2025-05-28, expires 2027-05-28) — needs confirmation against whatever lot Allure Labs actually tested
  - Gate: Pending QA Lead (root cause / classification call per SKN-OPS-006 §3.3)
  - SOP Reference: SKN-OPS-007 (batch lifecycle / stability)
- **Description:** `Source: Email from Allure Labs — "[subject]" (date). Allure Labs flagged a PET (long-term stability) test fail on Castaway Cream. Cross-refs: PD task comment [link], PLM cross-flag [link].`

### Child action — PD queue
**Comment on:** `[Batch Lifecycle] Castaway Cream — 875502` (gid `1214667239475040`) and/or the PET testing task (gid `1213487706215947`)
**Content:** `📧 From: Allure Labs, [date] — PET fail flagged on Castaway Cream. See parent lab-finding task [link] in SJS Quality Management for classification and next steps.`

### Child action — PLM cross-flag
`⚙️ PLM Bridge: Route the PET test result to outlook-plm-bridge to update the product's test-result fields (batch `875502` if confirmed) and log the failing stability data point against the PLM batch record `0cf9c60d-39c1-4406-a5dc-49b5195da3b4`.`

### Cross-references
All three actions above reference each other: the parent Quality task links to the PD comment and the PLM flag; the PD comment links back to the parent; the PLM flag notes the source Quality task gid.

---

## What I need from you before I push anything

1. **Confirm the vendor.** Is Allure Labs actually running PET/stability testing on Castaway Cream, or is this AMR Labs (the vendor on record for that SKU)? I don't want the Linked Vendor field wrong on a quality record.
2. **Confirm the batch.** Batch `875502` is the only active in-market Castaway Cream batch in the tracker — is that the lot that failed, or a different one not yet backfilled into Asana/PLM?
3. **Confirm severity/classification** (OOS vs. OOT, Major vs. Critical) once you have the actual lab report — I defaulted to OOT/Major as a placeholder, not a determination.

Say "push it" (with any corrections above) and I'll create the parent task, post the two child actions, and cross-flag PLM.
