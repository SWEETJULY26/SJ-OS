# Email Triage — SJS updates, past 7 days (2026-07-14 to 2026-07-21)

Scanned Inbox (general pass + OC3PL topic-folder sweep + Pedrero Regulatory topic-folder sweep), Sent Items, and Finance. Vendor/contact/product lexicon pulled live from Supabase (`vendors`, `wiki_pages` partner/contact, `products`) before classifying.

**Folder-sweep note (regression check):** `outlook_email_search` with `folderName: "OC3PL"` and `folderName: "Pedrero Regulatory"` both errored `NOT_FOUND` — twice each, including on retry. The folder listing (`mail:///folders/`) confirms both exist directly under Inbox (OC3PL: 575 items, 2 subfolders; Pedrero Regulatory: 56 items, 0 subfolders) — so per the updated guidance this was a lookup-tool mismatch, not a missing folder. Reading each folder directly by ID (`mail:///folders/{id}`) worked on the first try and returned full contents. Net: both topic-folder sweeps were actually attempted and actually completed, not skipped or reported as missing.

- OC3PL folder: sweep succeeded, and this week has real activity (see OPS section below).
- Pedrero Regulatory folder: sweep succeeded, but the folder's most recent message is from 2026-05-19 — nothing new landed there this week. A direct sender search on `pedreroregulatory.com` for the same date range also came back empty, which corroborates the folder result rather than contradicting it. So: correctly swept, correctly zero.

Found 20 SJ SKIN-relevant items this week (12 received, 8 sent). Labels seen: pd:6, ops:11, regulatory:1, quality:0, margin:0, intel:0, founder:1

## 🚨 URGENT / TIME-SENSITIVE

- **From:** danielle@ac-brands.com | **Subject:** Re: Call tomorrow? | **Received:** Jul 20, 22:59 (flagged High importance)
  Labels: founder (internal leadership) — inflammatory/false comments situation, screenshot attached, asking for advice ahead of a call.
  → Not an Asana-queue item per se (internal leadership comms, no vendor/SKU). Flagging for awareness only — no proposed Asana action unless you want it logged somewhere specific.

- **From:** perrinecalvet@milinycbeauty.com / KDC-One team | **Thread:** Re: PJ/Sweet July Skin TB | **Sent:** Jul 17, 14:38 (High importance)
  Labels: `pd`
  → You asked KDC-One (Greg Della Vecchia) whether the RM sent 7/15 was received and for a tentative date. No reply visible in this week's window — 4 business days out. Proposed: check-back task on the KDC-One PD thread, or a follow-up email if you want one drafted.

## 📌 OPS ACTION NEEDED — RECEIVED

- **From:** Danielle@oc3pl.com | **Subject:** RE: Receipt Order: 100310A - 2nd Shipment (Pineapple Punch Face Mask) | Jul 20, 23:24
  Labels: `ops`
  → Comment on the Pineapple Punch Face Mask / OC3PL receiving task: OC3PL flagged they don't see this SKU in Shopify yet — worth a Shopify-side check before the shipment lands.

- **From:** Terrie@oc3pl.com / Danielle@oc3pl.com (OC3PL folder sweep) | Several threads, Jul 14–20:
  - RE: Packing Rules for New Mini/Small DTC Boxes (Jul 14–15)
  - RE: Sweet July - Shipping Profile (Jul 14–15)
  - RE: Order #33194: Address Correction (Jul 14)
  - RE: Problem Orders Report/Ulta Tracking Question (Jul 14)
  Labels: `ops`
  → Routine OC3PL Order Management / SJ Shipping Dashboard activity — packing-rule updates for new mini/small DTC boxes, shipping profile confirmation, an address correction on order #33194, and an Ulta tracking question on the problem-orders report. Propose comments on the corresponding OC3PL tasks if not already logged.

- **From:** danilo@fws-us.com (FWS, under OC3PL) | **Subject:** RE: Discovery Sets - Guava Units in Extensiv | Jul 20, 20:57
  Labels: `ops`
  → FWS confirmed they're out of guava cartons from the prior kitting project and will start separating lip treatments out of the discovery sets. Ciarra is already on this thread. Comment on the relevant OC3PL/kitting task to track the carton reorder.

- **From:** chb@gogocustoms.com | **Subject:** Re: [External] PO #100338 — Soursop Components | Jul 20, 17:49
  Labels: `ops`
  → Customs broker acknowledgment on PO #100338 (Soursop components), noted they'll contact shipping directly. Comment on the PO #100338 task.

## 📌 PD ACTION NEEDED — RECEIVED

- **From:** priyanka@allurelabs.com (Allure Labs) | **Subject:** RE: SWEET JULY unit carton | Jul 21, 02:06
  Labels: `pd`
  → Reply to Ciarra's follow-up (below) — Priyanka says she missed the earlier email and will work on it with her team. This is a reply to an outstanding ask, not yet a resolution. Propose a comment on the relevant carton/packaging task noting the delay and that Allure Labs is now engaged.

- **From:** KCooper@ulta.com | **Subject:** RE: Sweet July Skin - Coffee Fix Peptide Eye Cream | Jul 20, 21:21
  Labels: `pd` + `regulatory`-adjacent (retail listing, not a Pedrero item)
  → Ulta says they're still missing valid offer data to push the Coffee Fix Peptide Eye Cream listing live, looping in Bensi and Stephanie. Propose a comment on the Coffee Fix Eye Cream / Ulta listing task — this is blocking go-live.

## 📤 ACTION NEEDED — SENT (commitments Alvin made)

- **To:** KDC-One (Brenda/Greg + team) | **Subject:** Re: Sweet July | Sent Jul 17, 19:08
  Labels: `pd`
  → You approved F&A with exceptions: correct brand name to "Sweet July" (not "Sweet July Skincare"), add a scannable UPC barcode, and confirm SKU. Propose a check-back task — reply expected by ~Jul 24 (5 business days) if no confirmation lands first.

- **To:** chb@gogocustoms.com, aoh@pkggroup.com, mresca/bzengewald@iks-usa.com, ciarra, nicole | **Subject:** Re: Deposit Invoice for Sweet July PO# 100310 (Production Order) | Sent Jul 17, 17:39
  Labels: `ops`, `plm`
  → You asked to be notified once the shipment lands so it can be booked with the 3PL. ⚙️ PLM Bridge: deposit invoice/prepacking lists attachment — route via `outlook-plm-bridge`.

- **To:** Brian@summitcoffee.com | **Subject:** Re: Jamaica Blue Mountain Coffee – Reorder for Sweet July Skin Production | Sent Jul 16, 16:44
  Labels: `pd`
  → Ingredient reorder acknowledged; you confirmed you'd inform the team and lab. No action needed — appears resolved.

- **To:** aldemarco@hctusa.com, nicole, gdvecchia@kdc-one.com, dgreco@hctusa.com, tflynn@kdc-one.com, adavila@hctusa.com, perrinecalvet | **Subject:** Re: Lip Treatment Color match samples - Tube & UC | Sent Jul 16 & Jul 20
  Labels: `pd`
  → Color-match sample approval thread with HCT/KDC-One, confirmed correct on both turns. No action needed — resolved.

- **To:** danilo@fws-us.com, Orders/John/Larissa@fws-us.com | **Subject:** Re: Pull Request — Sweet July Skin | Sent Jul 20, 17:54
  Labels: `ops`
  → You asked FWS to pull and ship ground-day to three named addresses (skincare list + apparel for two). FWS confirmed tracking numbers will follow once processed (received reply same thread, Jul 20 18:34). No action needed — in progress on their end.

- **To:** ciarra@ac-brands.com | **Subject:** Ops Download, Alvin x Ciarra | Sent Jul 20, 17:20–17:21 (x3, likely a send retry)
  Labels: internal — no Asana queue
  → Setting up 3x/week working sessions to hand off day-to-day Ops execution to Ciarra. No vendor/SKU action; flagging as founder-adjacent context only if you want it noted in a handoff/succession doc.

## ⚙️ PLM FLAGS

- Deposit invoice + prepacking lists for PO# 100310 (Sweet July, sent Jul 17 to gogocustoms/PKG Group/IKS) — route via `outlook-plm-bridge`.

## 🕒 NO REPLY YET

- **To:** KDC-One (Greg Della Vecchia) | Re: PJ/Sweet July Skin TB | Sent Jul 17 | Days waiting: ~4 business days
  → Checking on RM received 7/15 and a tentative date. Propose a check-back task or follow-up draft.

- **To:** KDC-One (Brenda + team) | Re: Sweet July (F&A corrections) | Sent Jul 17 | Days waiting: ~4 business days
  → Waiting on confirmation of brand name correction, UPC, and SKU. Propose a check-back task.

---
Which should I push? (say "all", list numbers, or "skip")
