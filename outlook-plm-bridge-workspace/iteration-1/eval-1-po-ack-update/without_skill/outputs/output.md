# Task: Update PO #100336 in PLM from KDC-One PO ack email

## What I checked

**Outlook (Inbox + Sent Items):**
- Searched for "KDC-One PO 100336", "PO 100336 acknowledgment", "100336" (two pages of results), and sender `kdc-one` combined with `acknowledg`.
- No email was found that reads as a PO acknowledgment for PO #100336 specifically. The closest hits are a 2026-05-18 recap email from Greg Della Vecchia (gdvecchia@kdc-one.com) confirming receipt of POs 100330–100333 (Sorrel, Fig, Jamaican Cherry, Coffee Fix) — that thread does not mention 100336. No message in the mailbox references 100336 by number at all.
- Conclusion: **I could not find a real email that is "the KDC-One PO ack" for PO #100336.** It may not have arrived yet, may be in a mailbox I don't have access to, or the PO number in the request may not match what's in the inbox.

**PLM (Supabase project `ujkabbffvhpewpbttmmy`, table `purchase_orders`):**
- PO #100336 exists. Current record:
  - Status: `Sent`
  - PO date: 2026-04-22
  - Vendor: KDC/One (Port Jervis) — contact Greg Della Vecchia, gdvecchia@kdc-one.com
  - Project ref: "Lip Treatments"
  - Requested ship date: 2026-05-08, lead time 2 weeks
  - Quote ref: GV26-007
  - Notes to vendor: "One-time tooling purchase for Norden filling line at KDC Port Jervis facility. Ship-to TBD — confirming with Greg Della Vecchia."
  - Line items: (1) Norden Holder Insert Pucks, qty 1 EA @ $2,000; (2) Norden Heating/Cooling Rings, qty 1 EA @ $2,500.
  - Last updated: 2026-04-22 20:15 UTC (same day as creation — no update since, and status has stayed at "Sent," i.e. no ack has been logged against it yet).

## Best-effort proposed update (since no matching ack email was found)

Given the request describes "the KDC-One PO ack just came in," the expected real-world content of that ack — and the PLM update I'd propose once the actual email is located — is:

**Field: `status`**
- From: `Sent`
- To: `Acknowledged` (or `Confirmed`, matching whatever status vocabulary PLM uses one step past "Sent" — the `purchase_orders` table doesn't expose a full enum here, so confirm the exact value before writing)

**Field: `updated_at`**
- Bump to current timestamp on write.

**Possible additional fields an ack typically carries, to capture if present in the actual email once found:**
- Vendor-confirmed ship date (may override or supplement `requested_ship_date` of 2026-05-08)
- Vendor PO/order confirmation number (KDC-One side reference)
- Any price or quantity delta from the two tooling line items above
- Attachment (the ack document itself) — would be filed against this PO record

## Not done (per constraints)

- No write was made to Supabase/PLM — this is read-only research plus a proposal.
- No Asana write was made or attempted.
- Before actually applying the status change, the real acknowledgment email should be located (check with Greg Della Vecchia at KDC-One directly, or confirm the mailbox/folder being searched is complete) so the proposed update reflects what the vendor actually confirmed rather than an assumption.
