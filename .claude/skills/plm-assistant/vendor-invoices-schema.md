# vendor_invoices schema reference

PLM Supabase project: `ujkabbffvhpewpbttmmy`. Migration script: `01_vendor_invoices_migration.sql`. Created 2026-05-12.

## Purpose

One row per vendor invoice. Universal cost ledger across AC Brands vendors. Source: Ramp emails ingested by outlook-plm-bridge Flow I, plus direct vendor invoices reconciled against Ramp. Reads via Supabase SELECT by regulatory-manager Jobs 8 + 9, regulatory-status-reporter v6.7 spend strip, purchasing-manager, and ayesha-weekly-briefing.

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | uuid PK | Generated via `gen_random_uuid()` |
| `vendor_id` | uuid FK | References `public.vendors(id)`. `on delete restrict` — invoices block vendor deletion |
| `invoice_number` | text NOT NULL | Vendor-issued invoice number. Unique per `(vendor_id, invoice_number)` |
| `invoice_date` | date NOT NULL | Date on the invoice itself, not the email or ingestion date |
| `amount` | numeric(12,2) | Check constraint `amount >= 0` |
| `currency` | text | Default `'USD'` |
| `cost_category` | enum | `regulatory` / `quality` / `pd` / `ops` / `marketing` / `general` |
| `regulatory_driver` | boolean | Default `false`. Flips `true` when spend is driven by regulatory requirement regardless of `cost_category` |
| `linked_sku_id` | uuid FK | References `public.products(id)`. `on delete set null`. Optional |
| `po_link` | uuid FK | References `public.purchase_orders(id)`. `on delete set null`. Null for retainer-style invoices |
| `state` | enum | `pending` / `approved` / `paid` / `disputed` / `declined` / `void` |
| `ramp_message_id` | text | Source Ramp email message identifier. Enables dedup |
| `attachment_filename` | text | Original invoice filename |
| `attachment_url` | text | Storage URL (Supabase Storage or Asana attachment URL) |
| `notes` | text | Free-text. Operator notes from classification HITL |
| `source_email_subject` | text | Captured at ingestion for traceability |
| `source_email_date` | timestamptz | Captured at ingestion |
| `classified_by` | text | Skill or user that classified. e.g., `outlook-plm-bridge`, `purchasing-manager`, `alvin@ac-brands.com` |
| `classified_at` | timestamptz | When the classification HITL gate cleared |
| `created_at` | timestamptz | Auto-set on insert |
| `updated_at` | timestamptz | Auto-updated via `trg_vendor_invoices_updated_at` trigger |
| `created_by` | text | Default `'outlook-plm-bridge'`. Tracks ingestion source skill |

## Constraints

- PK on `id`
- Unique `(vendor_id, invoice_number)` — same vendor cannot issue two invoices with the same number
- FK to `vendors(id)` restricted (cannot orphan invoices by deleting a vendor)
- FK to `products(id)` set-null (SKU retirement does not nuke invoice history)
- FK to `purchase_orders(id)` set-null (PO deletion does not nuke invoice history)
- Check `amount >= 0`

## Indexes

Single-column:
- `idx_vendor_invoices_vendor_id` — vendor-level rollup
- `idx_vendor_invoices_invoice_date` — date-range filtering
- `idx_vendor_invoices_cost_category` — category-level rollup
- `idx_vendor_invoices_regulatory_driver` — partial index `where regulatory_driver = true` for fast OR clause
- `idx_vendor_invoices_linked_sku_id` — partial, `where linked_sku_id is not null` — per-SKU rollup
- `idx_vendor_invoices_po_link` — partial, `where po_link is not null` — PO reconciliation
- `idx_vendor_invoices_state` — state-based queue filters
- `idx_vendor_invoices_ramp_message_id` — partial, `where ramp_message_id is not null` — dedup on ingestion

Composite (rollup hot path):
- `idx_vendor_invoices_regulatory_rollup (invoice_date, cost_category, regulatory_driver)` — designed for regulatory-manager Jobs 8 + 9 and the v6.7 spend strip query: `WHERE (cost_category='regulatory' OR regulatory_driver=true) AND invoice_date BETWEEN ... AND ...`

## Trigger

`trg_vendor_invoices_updated_at` — BEFORE UPDATE on each row, sets `updated_at = now()`. Function: `public.vendor_invoices_set_updated_at()`.

## RLS

Enabled. Policy:
- `vendor_invoices_read_all` — `for select using (true)` — anon and authenticated can read
- No INSERT/UPDATE/DELETE policies — only service_role bypasses RLS for writes. plm-assistant uses service_role server-side; Netlify Functions read using publishable key + the read-all policy.

## Read patterns by consumer

| Consumer | Query shape |
|---|---|
| outlook-plm-bridge Flow I (dedup check on ingestion) | `select id from vendor_invoices where ramp_message_id = $1 limit 1` |
| outlook-plm-bridge Flow I (invoice-number dedup) | `select id from vendor_invoices where vendor_id = $1 and invoice_number = $2 limit 1` |
| purchasing-manager Job 9 (queue scan) | `select * from vendor_invoices where state in ('pending') order by invoice_date desc` |
| purchasing-manager Vendor Invoices section render | `select * from vendor_invoices where vendor_id = $1 order by invoice_date desc limit 50` |
| regulatory-manager Job 8 (monthly rollup) | `select cost_category, sum(amount) as total, count(*) as n from vendor_invoices where (cost_category='regulatory' OR regulatory_driver=true) and invoice_date >= $start and invoice_date < $end and state in ('approved','paid') group by cost_category` |
| regulatory-manager Job 9 (quarterly QoQ/YoY) | same shape, multi-quarter ranges, plus per-SKU breakdown via `group by linked_sku_id` |
| regulatory-status-reporter v6.7 spend strip | Calls Netlify Function `sjs-regulatory-rollup` with the `spend` block, which runs the Job 8 + Job 9 queries server-side |
| ayesha-weekly-briefing | regulatory-manager Job 8 output (founder filter: only variance signals >20% MoM or single invoices >$10k) |

## Write patterns

All writes go through `plm-assistant` per the single-writer rule. Two patterns:

1. **Insert from outlook-plm-bridge Flow I:** after Operator approves classification HITL, `plm-assistant` inserts the row with `created_by='outlook-plm-bridge'` and `state='pending'`. Approval/payment state transitions come separately.

2. **State update from purchasing-manager Job 9:** after Operator confirms approval, payment, or dispute, `plm-assistant` updates `state` and stamps `classified_by`/`classified_at` if classification was finalized.

No bulk inserts. No direct API writes from any other skill.

## Future considerations (not in v1 migration)

- Multi-currency conversion at rollup time — current rollups assume USD; international vendor invoices in CAD/EUR/GBP will need a conversion layer (FX rate at invoice_date, not query time).
- Invoice line-item table (`vendor_invoice_lines`) — current schema treats one invoice as one cost record. If we need line-item categorization (one Ramp invoice split across regulatory + quality lines), add a child table and migrate the `cost_category` / `regulatory_driver` / `linked_sku_id` columns to the line level.
- Allocation split — when one invoice covers work for multiple SKUs (e.g., Pedrero retainer covering full portfolio), an allocation table would let one invoice fan out to N SKUs by share.

These deferrals are noted in CHANGES.md and tracked outside the v1 build.
