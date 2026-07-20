# Outlook → PLM Bridge — Flow reference

Full extraction logic, staged-write SQL, and confirmation-preview formats for each PLM flow. SKILL.md carries the index and the direction map; this file carries the end-to-end detail. Read the matching flow before running it.

**Write rule (applies to every flow):** all INSERT / UPDATE / DELETE shown here is **staged** by this bridge and **committed by `plm-assistant`** after Alvin confirms. SELECTs you may run direct via the Supabase MCP (`project_id: ujkabbffvhpewpbttmmy`) for ID lookups, duplicate checks, and current-value previews. Never call `execute_sql` for a write.

**Schema is live.** Column names below were verified against the PLM on 2026-05-31. If a column looks wrong at run time, SELECT the table definition and trust the database over this file — then flag the drift so this reference gets fixed.

---

## Flow A — Purchase order

**Table:** `purchase_orders` (+ `purchase_order_items` for line detail)
**Key columns:** `po_number` (text), `status`, `po_date`, `requested_ship_date`, `actual_ship_date`, `revision` (int), `vendor_id`, `payment_terms`, `incoterm` (singular), `lead_time` (text), `quote_ref`, `notes_to_vendor`.

**Inbound (vendor acknowledges / updates an existing PO) → UPDATE.**
Extract: PO number, new status, confirmed or revised ship date, any line-item changes.
1. `SELECT id, po_number, status, requested_ship_date FROM purchase_orders WHERE po_number = '<n>'` — resolve the PO and show current values.
2. Stage:
   ```sql
   UPDATE purchase_orders
     SET status = '<new status>',
         requested_ship_date = '<date>',   -- only if the vendor moved it
         actual_ship_date = '<date>'        -- when the vendor confirms it shipped
   WHERE id = '<po uuid>';
   ```

**Outbound (Alvin sends a new PO) → INSERT.** A sent revision or cancellation → UPDATE with `revision = revision + 1`.
Extract: vendor, line items (sku, description, quantity, uom, unit_cost), requested ship date, terms.
1. Next number: `SELECT MAX(po_number::int) + 1 FROM purchase_orders`.
2. Stage the header INSERT + line-item INSERTs as one transaction (CTE pattern — see `plm-assistant`). One-time tooling lines are valid in `purchase_order_items` without a `component_id`.

**Preview:**
```
Flow A — PO #<n> [INSERT/UPDATE]
  Vendor: <name>   Status: <old> → <new>
  Ship date: <old> → <new>
  Lines: <n> (only on INSERT/line change)
  Asana sync-back: <task name or "none">
```

---

## Flow B — Batch / COA

**Table:** `batches`
**Key columns:** `product_id`, `batch_code`, `batch_quantity`, `shelf_life_months`, `supplier_production_date`. The DB trigger computes `sj_expiration_date` and `sj_pull_date` — **stage production date + shelf life only**, never compute the rest yourself.

Almost always inbound. Extract: product, batch code, production date, shelf life (months), quantity.
1. Resolve product (run-time product lookup). Dedup: `SELECT id FROM batches WHERE batch_code = '<code>'`.
2. Stage:
   ```sql
   INSERT INTO batches (product_id, batch_code, batch_quantity, shelf_life_months, supplier_production_date)
   VALUES ('<product uuid>', '<code>', <qty>, <months>, '<date>');
   ```
3. COA PDF → flag for manual upload (attachment handling). The COA itself is not a `vendor_compliance_docs` row; it travels with the batch.

**Preview:**
```
Flow B — INSERT batch <code>
  Product: <name>   Qty: <n>   Production: <date>   Shelf life: <n>mo
  (expiration + pull date auto-computed on commit)
  COA: <filename> — 📎 manual upload
```

---

## Flow C — Vendor onboarding / compliance doc

**Tables:** `vendors`, `vendor_compliance_docs`
**Key columns — vendors:** `name`, `vendor_type`, `website`, `contact_name`, `contact_email`, `order_email`, `status`, `onboarding_checklist` (jsonb), `contract_renewal_date`.
**Key columns — vendor_compliance_docs:** `vendor_id`, `doc_type`, `file_name`, `file_url`, `issue_date`, `expiry_date`, `status`, `revision`, `product_ref`, `superseded_by`.

Existing `doc_type` values in use: `Manufacturing Agreement`, `MSDS`, `Quality Agreement`. Add new types as they arrive (NDA, W9, COI, MSA, Banking/ACH) — match the onboarding checklist keys.

**Inbound (vendor introduces self / sends a compliance doc):** dedup vendor by name; INSERT new vendor or UPDATE existing; INSERT the compliance doc row.
**Outbound (Alvin sends NDA / MSA / W-9 / onboarding kit):** INSERT vendor if new + INSERT `vendor_compliance_docs` row tagged "outbound from AC Brands" in `notes`.

```sql
-- new vendor
INSERT INTO vendors (name, vendor_type, contact_name, contact_email, status)
VALUES ('<name>', '<type>', '<contact>', '<email>', 'active');
-- compliance doc
INSERT INTO vendor_compliance_docs (vendor_id, doc_type, file_name, issue_date, expiry_date, status)
VALUES ('<vendor uuid>', '<type>', '<filename>', '<date>', '<date>', 'active');
```

For onboarding-task checklist auto-check and the NDA+W9 gate move, see the **Flow C-gate** section in SKILL.md (the one place this bridge writes Asana subtask state).

**Preview:**
```
Flow C — Vendor <name> [INSERT/UPDATE] + doc <type>
  Outbound docs: <NDA/MSA/W-9 if Alvin sent them>
  📎 manual upload: <filename>
```

---

## Flow D — Formula approval / rejection with document

**Table:** `products`
**Key column:** `current_phase` (text — Ideation · R&D · Packaging · Sampling · Testing · Production · Launch Ready).

**Inbound (supplier sends signed approval back) → UPDATE phase.**
**Outbound (Alvin sends the decision) → UPDATE phase**, approver = Alvin, decision date = the sent date.
```sql
UPDATE products SET current_phase = '<new phase>',
  notes = notes || E'\n[<date>] Formula <approved/rejected> — approver <name>'
WHERE id = '<product uuid>';
```
Always cross-flag `outlook-asana-bridge` for the Formula Tracker stage move (this bridge does **not** move Asana stage-gate tasks).

**Preview:**
```
Flow D — <product> phase <old> → <new>   approver: <name>
  📨 outlook-asana-bridge cross-flag: Formula Tracker stage move
```

---

## Flow E — Stability / compatibility / RIPT / PET / micro results

**Table:** `product_test_results` (one row per test event — keeps history; links to a batch when the test is batch-level).
**Key columns:** `product_id`, `batch_id` (nullable — null for pre-launch formula-level RIPT/compat), `test_type` (`stability` · `compatibility` · `RIPT` · `PET` · `micro` · `challenge` · `other`), `result` (`pass` · `fail` · `pending` · `conditional`), `test_date`, `checkpoint` (e.g. `T+3mo`, `40C/75RH`), `lab_vendor_id`, `file_name`, `file_url`, `notes`.

Almost always inbound (lab email). Extract: product, test type, result, date, checkpoint, lab, report filename.
```sql
INSERT INTO product_test_results
  (product_id, batch_id, test_type, result, test_date, checkpoint, lab_vendor_id, file_name)
VALUES ('<product uuid>', <batch uuid or NULL>, '<type>', '<result>', '<date>', '<checkpoint>', '<lab uuid>', '<filename>');
```

**Failing result (`result = 'fail'`, or RIPT positive) is the priority case.** The PLM INSERT is the **cross-reference**, not the parent. Open **quality-lab-coordinator** as the parent action (Quality queue), flag URGENT, and cross-flag `outlook-asana-bridge` for the PD task. Report PDF → manual upload.

**Preview:**
```
Flow E — INSERT test result: <product> — <type> — <result>
  Checkpoint: <checkpoint>   Lab: <vendor>   Date: <date>
  [on fail] 🚨 Parent: quality-lab-coordinator (Quality queue) — PLM row is the cross-ref
  📎 manual upload: <report filename>
```

---

## Flow F — Invoice referenced against a PO (inbound only)

Use Flow F **only** for a passing reference to an invoice inside PO correspondence where no cost-ledger row is wanted — e.g. a vendor notes "invoice attached against PO #100336" and you just want the PO comment. **Any invoice you are capturing as a cost record goes to Flow I, not F.** When in doubt, Flow I (it dedups and carries the cost classification).

No dedicated table for a bare reference — note it in the PO's Asana sync-back. Never enter banking details (see SKILL.md confirmation rules).

---

## Flow G — BOM / component spec update

**Table:** `components`
**Key columns:** `name`, `component_type`, `sku`, `vendor_id`, `unit_cost`, `lead_time_days`, `cost_status`, `last_cost_update`, `cost_notes`, `notes`. (Note: there is no MOQ column on `components` — `moq` lives on `products`. Capture a component MOQ change in `cost_notes` and cross-flag margin.)

**Inbound (vendor sends updated quote / cost) → UPDATE cost.**
**Outbound (Alvin sends spec / target cost / revised BOM) → UPDATE** spec fields with a "spec communicated <date>" note.
```sql
UPDATE components
  SET unit_cost = <n>, cost_status = 'confirmed', last_cost_update = now(),
      cost_notes = '<context — quote ref / MOQ change / tariff>'
WHERE id = '<component uuid>';
```
Any margin signal — cost shift, MOQ change, tariff, duty — cross-flags **margin-pressure-test** for the affected SKUs (and **walk-away** if a SKU is already at the floor).

**Preview:**
```
Flow G — <component> unit_cost <old> → <new>   origin: <vendor quote / Alvin spec>
  💰 margin cross-flag: <margin-pressure-test / walk-away> (if cost/MOQ/tariff moved)
```

### Flow G sub-pattern — tube/carton SKU assignment vs. artwork proof

The same vendor thread (e.g. KDC tube/carton correspondence) can carry three different kinds of signal that touch different tables. Decide which one you're looking at before acting — don't assume a single email settles everything:

**1. SKU assignment (vendor names a tube SKU, and/or a carton SKU).**
The tube SKU is the one that shows up most often; the carton SKU frequently comes in a *separate*, later email — don't wait for both, and don't treat a tube-only email as incomplete. Update only the component the email actually names:
```sql
UPDATE components SET sku = '<vendor SKU>', notes = notes || E'\n' || 'SKU confirmed <date> — <vendor>'
WHERE id = '<tube or carton component uuid>';
```

**2. Artwork proof (supplier sends a proof; once Alvin/team signs off and it's sent back approved).**
This is a document, not a field — it goes into `public.attachments`, not `components` directly. Existing real convention on this table: `entity_type = 'component'`, `attachment_type = 'file'`, `category = 'Artwork'`.
```sql
INSERT INTO public.attachments
  (entity_type, entity_id, file_name, file_type, storage_path, attachment_type, category, notes, uploaded_by)
VALUES
  ('component', '<component uuid>', '<proof file name>', '<file type>', '<storage path once uploaded>',
   'file', 'Artwork', 'Proof approved <date> — <context>', 'alvin@ac-brands.com');
```
Claude cannot upload the file to Supabase storage directly from this context (see the attachment-upload limitation noted elsewhere in this skill) — stage the INSERT with a placeholder `storage_path` and flag it for Alvin to complete the manual upload, same pattern as other PLM-bound attachments.

**3. Generic BOM / meeting-related update (spec change, cost, timeline note) that isn't a SKU or an artwork proof** — that's the original Flow G cost/spec pattern above, not this sub-pattern.

**Preview:**
```
Flow G (SKU) — <component> sku <old/blank> → <new>   origin: <vendor email>
Flow G (artwork) — <component> artwork proof staged for PLM   origin: <vendor email>
  ⚠️ Manual upload needed — storage_path is a placeholder until the file is actually uploaded
```

---

## Flow H — Asana sync-back (always runs after A–G and I)

After any committed PLM write, post a `📦 PLM Sync` comment on the related Asana task with the diff. Comment-only — Flow C-gate is the sole exception where this bridge changes Asana task state. Format:
```
📦 PLM Sync — <Flow> — <date>
<one-line diff, e.g. "PO #100336 status Acknowledged → Shipped, ship date 2026-06-12">
Source: <email sender>, <date> — "<subject>"
```

---

## Flow I — Vendor invoice intake (Ramp + direct)

**Table:** `vendor_invoices`
**Key columns:** `vendor_id`, `invoice_number`, `invoice_date`, `amount` (numeric 12,2), `currency` (default USD), `cost_category` (`regulatory` · `quality` · `pd` · `ops` · `marketing` · `general`), `regulatory_driver` (bool), `linked_sku_id` (nullable), `po_id` (nullable FK `purchase_orders`), `status` (`staged` · `approved` · `paid` · `disputed` · `void` — default `staged`), `ramp_message_id`, `attachment_filename`, `source_email_subject`, `source_email_date`, `notes`. Unique on `(vendor_id, invoice_number)`.

Recognition, extraction, and classification logic live in SKILL.md (Flow I section). The staged write:
```sql
-- dedup first
SELECT id FROM vendor_invoices WHERE vendor_id = '<v>' AND invoice_number = '<n>';
-- if none, stage:
INSERT INTO vendor_invoices
  (vendor_id, invoice_number, invoice_date, amount, currency,
   cost_category, regulatory_driver, linked_sku_id, po_id,
   ramp_message_id, attachment_filename, source_email_subject, source_email_date)
VALUES ('<v>', '<n>', '<date>', <amount>, 'USD',
   '<category>', <bool>, <sku uuid or NULL>, <po uuid or NULL>,
   '<message-id>', '<filename>', '<subject>', '<timestamp>');
```
Row commits via `plm-assistant` **only after** `purchasing-manager` Job 9 clears the HITL classification + multi-home gate. New `status` defaults to `staged`; Job 9 advances it. If the dedup SELECT returns a row, skip the INSERT and surface `🔁 Duplicate — invoice <n> already logged`.

**Preview:** see the VENDOR INVOICES block in the SKILL.md PLM Triage Report format.
