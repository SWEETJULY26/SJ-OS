# Logiwa Receipt Order Report — intake spec

**Use:** How to read the Logiwa receipt order report emails and turn them into PLM receipt rows. Owned by `inventory-manager` Job 2 (Receiving). The email intake itself runs through `outlook-plm-bridge`; this file says what the report means and what to do with it.

**Authored:** 2026-07-31, after PO 100310 was closed while PLM held only 824 of ~5,744 received units. The receipt reports had been arriving since April and nothing consumed them.

---

## The source

Two senders, both live, same payload — Logiwa appears to have migrated senders without retiring the old one. Treat them as one source and match on either:

- `noreply@wmsnotification.com`
- `noreply@wmssystem.logiwa.com`

Subject: `Receipt Order Report for RO#<ro_id> of Sweet July`

Arrives per receipt order, not on a schedule — roughly every few days, clustered when a shipment lands. Unlike the daily DTC shipment report (`oc3pl-order-manager` Job 1) there is no fixed cadence, so a sweep looks back over a window rather than expecting one per day.

## The payload

**The table is inline in the email body.** There is also an attachment carrying the same data, but the body table is enough — parse that and skip the attachment, which the API cannot open anyway.

Columns, in order:

`PUOR_ID · PO CODE · ENTRY DATE · VENDOR · CLIENT · ITEM CODE · ITEM DESCRIPTION · PACK TYPE · PO QUANTITY · RECEIVED · PO DIFFERENCE`

One row per line item. `ITEM CODE` is the SKU and resolves against `products.sku` or `components.sku`. `CLIENT` is always Sweet July; `VENDOR` is the supplier as Logiwa knows them, which will not always match `vendors.name` exactly.

### The trap in this report

**`PO QUANTITY` is the quantity on that receipt order, not the quantity ordered on the PLM PO. `PO DIFFERENCE = 0` means the receipt order was fully received — it does not mean the PLM PO is complete.**

Worked example, RO `100310A - 2nd shipment`, received 2026-07-30: PPFM-005 showed PO QUANTITY 4744, RECEIVED 4744, PO DIFFERENCE 0. PLM PO 100310 orders 5,800 of PPFM-005. Reading that zero as "PO complete" is exactly how the PO got closed with the receipt unrecorded.

Always reconcile against `purchase_order_items.quantity` in PLM, never against the report's own PO QUANTITY column.

## Classifying the RO

The RO id is free text and only sometimes a PO. Three classes, checked in order.

### Class 1 — PO-linked

The RO contains a PLM PO number. Extract the first six-digit run and confirm it exists in `purchase_orders.po_number` before doing anything with it. Real forms seen:

| RO id | PO |
|---|---|
| `100339` | 100339 |
| `100310A - 2nd shipment` | 100310 |
| `Sweet July PO100329` | 100329 |
| `100350 - KAF` | 100350 |

A trailing letter or a "Nth shipment" note means **partial receiving** — several receipt orders against one PO. PLM models this: multiple `po_receipts` rows per PO. Dedupe key is `PO number + receipt date` per `asana_task_contract.md`, and the PO stays in Receiving until the ordered quantity is met across all of them.

Route: `inventory-manager` Job 2. Write the receipt, then hand the PO status flip to `purchasing-manager`.

### Class 2 — Returns and replenishment

RO id starts with `SPY` or `repl-`. Examples: `SPY7350459400513`, `repl-dad18abb-eee3-462d-ab89-599ac04576a6`. These are customer returns and replenishments coming back into the warehouse, not supplier receipts. There is no separate returns report — these are it.

Route: return disposition. `oc3pl-order-manager` owns the customer-side resolution, `inventory-manager` owns the position write. Do not attempt a PO match and do not open anything in Purchasing.

### Class 3 — Named movement, no PO

Neither a resolvable PO number nor a returns prefix. Examples: `Vanity Bags`, `4.3 Move In`, `VanityRumMesh`, `Eye Cream - 2 Master Cases`, `GWP - Pineapple Punch Scarf`. Marketing stock, GWP items, facility moves.

Route: `inventory-manager` Job 3 (location ledger and movements). Position write only, no PO, nothing in Purchasing.

**A six-digit number that does not resolve in `purchase_orders` is Class 3, not Class 1.** Surface it rather than forcing a match — a wrong PO match writes a receipt against someone else's order.

## What to write

Through `plm-assistant`, which is the only writer to PLM.

1. **`po_receipts`** — one row per receipt order: `purchase_order_id`, `received_date` (the ENTRY DATE, or the email's received date if ENTRY DATE is absent).
2. **`po_receipt_items`** — one row per line: `po_receipt_id`, `po_item_id` resolved by matching ITEM CODE to the PO's line SKU, `quantity_received` from the RECEIVED column. This drives `inventory_transactions` on creation.
3. **Reconcile.** Sum `quantity_received` across every receipt for the PO against `purchase_order_items.quantity`.
   - Met → hand to `purchasing-manager` to set the PO task `Status = Received`.
   - Short → the PO is partially received. Leave it in Receiving, note the outstanding quantity, and only open a Job 10 discrepancy when the vendor has declared the shipment complete. A partial receipt mid-shipment is not a discrepancy.
   - Over → variance. Job 10 discrepancy and a vendor conversation.

### Batches cannot come from this report

**The report carries no batch or lot column.** Batch code, production date and shelf life are not in it, so batch records can never be created from the report alone — the operator supplies them. Write the receipt quantities, then raise the batch codes as an open question per the contract's TBD rule.

This matters because `products.quantity_on_hand` is a cached sum of `inventory_transactions`. Receipt rows without batches still move the position, but anything reading batch-level data — FEFO pulls, near-expiry sweeps, `batch-lifecycle-tracker` — stays blind until the batches land. Say so on the task rather than letting it look finished.

## HITL

Operator approves before any PLM write. Report the parse first: RO id, class, matched PO if any, per-line received quantities, the reconciliation verdict against PLM's ordered quantities, and the batch gap. A parse that does not state its class and its PO match verdict has not run this spec.

## Known gaps

- `VENDOR` in the report will not always match `vendors.name`. Resolve against the run-time vendor lexicon and surface a non-match rather than guessing.
- Nothing has consumed these reports historically, so there is a backlog of unrecorded receipts going back to at least April 2026. The reports are still in Outlook; catching up is a separate pass and needs deciding how far back to go.
- PO 100310 is the known-bad case: 824 recorded 2026-07-21, RO 100310A adding 1,000 of PPFM-001 and 4,744 of PPFM-005 on 2026-07-30 never recorded, and 824 + 4,744 leaves 232 short of the 5,800 ordered on PPFM-005. Worth resolving as the first real exercise of this spec.
