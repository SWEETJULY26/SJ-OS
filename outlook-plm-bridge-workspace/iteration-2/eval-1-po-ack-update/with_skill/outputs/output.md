# PO #100336 — KDC-One ack → PLM staged update

## Current record (Supabase SELECT, read-only)

```
purchase_orders
  id: 76213d21-cae7-44b2-b821-6d213ba866d0
  po_number: 100336
  status: Sent
  po_date: 2026-04-22
  requested_ship_date: 2026-05-08
  actual_ship_date: NULL
  vendor_id: ea2f6d63-375b-499f-8c0e-c7ee877f1733  → vendors."KDC/One (Port Jervis)"
```

Line items on this PO: **Norden Heating/Cooling Rings** and **Norden Holder Insert Pucks** — one-time tooling, not a flavor/FG line. That matters, because it's why a literal-text search never had a shot: this is a tooling PO, not one of the flavor POs (100322, 100328–100332) that got their numbers spelled out in later correspondence.

## What the old literal-PO-number search would have found

Nothing. I ran `outlook_email_search` for the string "100336" across the whole mailbox (Inbox + Sent) — one hit, and it's a fuzzy/relevance match on an unrelated email, not an actual occurrence of "100336" in the body or an attachment name. The literal-match approach would have come back empty and stalled here.

## What the new vendor + timing + attachment approach found

Pulled all KDC-One correspondence (sender/recipient domain `kdc-one.com`) bracketing the PO's creation date (2026-04-22) instead of grepping for the number. The relevant thread is the recurring "Sweet July Skin Lip Treatments – BOMs & Supply Plans" punch list Alvin and Greg Della Vecchia (KDC-One, Sales Project Manager) were bouncing back and forth that week:

- **2026-04-21 / 04-22 / 04-24** — Greg's open-items list carries the line: *"Tooling Quote (see attached) – PO needed this week."* This is the ask that becomes PO 100336 (tooling for the pilot line — matches the Norden rings/pucks on the line items).
- **2026-04-27, 8:13pm ET** — Greg's updated punch list (gdvecchia@kdc-one.com, "Re: Sweet July Skin Lip Treatments – BOMs & Supply Plans") closes that line out: *"Tooling Quote (see attached) – PO needed this week. **Attached. Confirming receipt.**"*

No other item in that list gets a plain close-out like this — the next line down is explicitly "Open still pending," so the contrast is clear. This one reads as a closed, no-open-question receipt confirmation, sitting right in the PO's creation window, on the exact tooling item the PO covers.

**Under the old rule** (wait for the PO number to be restated, or a new ship date confirmed), this would not have counted — Greg never types "100336," and no new ship date is given.

**Under the new rule**, a receipt-confirmation-style reply is sufficient on its own. This qualifies: vendor + rough timing + attachment context all line up, and the language ("Confirming receipt," no follow-up question) is exactly the pattern the new rule is built to catch. **So yes — the new recognition rule changes the outcome here.** Nothing else in the window reads as a cleaner ack for this PO; a few nearby emails ("Confirming receipt of the revised BOMs," "Confirmed receipt of POs 100330–100333...") are close in time but are explicitly about the flavor BOMs/POs, not the tooling line.

One honest caveat: this confirmation lives inside a running shared punch-list email rather than a standalone "got the PO" reply. I'm treating it as sufficient per the new rule (vendor, timing, and attachment all point at this PO, and the line is explicitly closed out with "confirming receipt"), but it's a softer signal than a dedicated one-line reply would be — worth a gut check from Alvin before commit.

## Staged write (Flow A — not yet committed)

```sql
UPDATE purchase_orders
  SET status = 'Acknowledged'
WHERE id = '76213d21-cae7-44b2-b821-6d213ba866d0';
```

**Preview**

```
Flow A — PO #100336 [UPDATE]
  Vendor: KDC/One (Port Jervis)   Status: Sent → Acknowledged
  Ship date: 2026-05-08 → unchanged (vendor didn't restate or revise it)
  Source: gdvecchia@kdc-one.com, 2026-04-27 — "Re: Sweet July Skin Lip Treatments - BOMs & Supply Plans" (punch-list line: "Tooling Quote ... Attached. Confirming receipt.")
  Asana sync-back (Flow H, on commit): 📦 PLM Sync — PO #100336 status Sent → Acknowledged — source as above
```

No PLM write and no Asana write have been made. This is staged for your review — confirm and I'll hand it to plm-assistant to commit, then post the sync-back comment.
