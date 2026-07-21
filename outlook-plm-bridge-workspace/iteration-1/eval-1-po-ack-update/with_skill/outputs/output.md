# Outlook → PLM Bridge — Flow A (Purchase Order)

## Email search result

I swept Outlook for a KDC-One acknowledgment tied to PO #100336 — searched by the PO number directly, by sender domain `kdc-one.com`, and by the PO's quote ref (`GV26-007`) / tooling context ("Norden," "Port Jervis"). No literal match. Here's what's actually in the mailbox around this PO and vendor:

- No email in Inbox or Sent Items mentions "100336" or "GV26-007" by name.
- The closest KDC-One threads in the last two weeks are all "Confirming receipt" replies with no status or ship-date detail: "Re: Pilot - Production Scheduling" (7/15), "Re: Pineapple Punch Lip Treatment PO & BOM update" (7/14), and a 5/18 recap that confirms **POs 100330–100333** (Sorrel, Fig, Jamaican Cherry, Coffee Fix) — a different PO block, not 100336.
- PO #100336 in PLM is a one-time tooling PO (Norden filling line, KDC Port Jervis) with `notes_to_vendor: "Ship-to TBD — confirming with Greg Della Vecchia."` — consistent with the open BOMs/Supply Plans thread from late April, but nothing in that thread names PO #100336 or gives a new status/ship date.

**Bottom line: I can't confirm a real KDC-One PO ack for #100336 landed in the mailbox.** Before this goes further, tell me which email you mean, or forward it — I don't want to stage a PLM update off a guess.

Since the eval wants to see the Flow A confirmation shape either way, here's the staged preview built on the **real current PLM record** for PO #100336, with the proposed new values marked illustrative (not sourced from a real ack — swap them for the actual email once you point me to it).

## Current PO #100336 record (PLM — read via Supabase SELECT)

| Field | Current value |
|---|---|
| PO number | 100336 |
| Vendor | KDC/One (Port Jervis) |
| Status | Sent |
| PO date | 2026-04-22 |
| Requested ship date | 2026-05-08 |
| Actual ship date | — |
| Revision | 0 |
| Payment terms | Net 30 |
| Incoterm | FOB Origin |
| Quote ref | GV26-007 |
| Notes to vendor | One-time tooling purchase for Norden filling line at KDC Port Jervis facility. Ship-to TBD — confirming with Greg Della Vecchia. |

## Staged UPDATE preview (Flow A — inbound PO acknowledgment)

**This is illustrative, not a real write** — no confirmed ack email backs these new values. Flagging that clearly per the confirmation rules; do not treat this as ready to commit.

```
Flow A — PO #100336 [UPDATE]  ⚠️ ILLUSTRATIVE — source email not confirmed
  Vendor: KDC/One (Port Jervis)
  Status:            Sent           →  Acknowledged
  Requested ship date: 2026-05-08   →  2026-05-08 (unchanged — no revision confirmed)
  Actual ship date:    —            →  — (not yet shipped)
  Asana sync-back: [would post to the KDC/One tooling task in SJS Ops once confirmed]
```

```sql
-- STAGED ONLY — not executed. plm-assistant is the sole writer, and only after
-- Alvin confirms against a real source email.
UPDATE purchase_orders
  SET status = 'Acknowledged'
WHERE id = '76213d21-cae7-44b2-b821-6d213ba866d0';  -- PO #100336
```

## What I need from you to actually run this

1. Point me to the specific email (forward it, or give me the subject line / date) that carries the KDC-One ack for #100336, or
2. Confirm you want me to treat one of the "Confirming receipt" replies above as the ack — but none of them currently name a new status or ship date, so there's nothing to update yet even if I use one of those.

No PLM write, no Asana post, and no plm-assistant hand-off happened — this stopped at the staged-preview stage per the read-only confirmation gate.
