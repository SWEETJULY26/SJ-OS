# Supabase (PLM) — connection reference

**Mechanism:** MCP (`mcp__Supabase__*`)
**Auth:** Connected via MCP.

Two Supabase projects exist — don't confuse them:

| Project | ID | Purpose |
|---|---|---|
| **PLM** | `ujkabbffvhpewpbttmmy` | Product Lifecycle Management — vendors, products, batches, POs, BOM, inventory, forecasting, logistics, quality, brand assets, wiki. 55 tables. This is the one "PLM" means everywhere else in this AIOS. |
| **Sweet July Business Dashboard** | `ndxatsnrnlbdesridwfq` | Amazon-specific — FBA/AWD inventory, order velocity, sales/traffic. 12 tables. Separate from PLM; don't cross-query. |

## PLM — key tables

- `products`, `vendors`, `components`, `bill_of_materials`, `product_vendors`, `vendor_components` — core PD/sourcing data
- `purchase_orders`, `purchase_order_items`, `po_receipts`, `po_receipt_items` — P2P
- `batches`, `inventory_transactions` (immutable ledger — never delete, use correcting entries), `location_inventory`, `channel_inventory`
- `attachments` — polymorphic file metadata (`entity_type`/`entity_id` link to any table). Real in-use convention: `entity_type='component'`, `attachment_type='file'|'link'`, `category='Artwork'|'Spec Sheet'|'Testing & QA'|'Safety & Compliance'` etc. — check existing distinct values before inventing a new category.
- `wiki_pages` — the "recognition layer": `page_type` in `contact` (44 rows), `sku` (40), `supplier` (21), `partner` (15), `sop` (13). Queried live by skills instead of duplicating vendor/contact/SKU lists into static files.
- `audit_logs` — heavily used (5,600+ rows), confirms this PLM is in daily production use, not a shell.
- Several tables are schema-ready but still empty: `outbound_orders`, `shipments`, `retailer_compliance_specs`, `inventory_targets`, `vendor_invoices` — meaning those flows (retailer POs, logistics tracking, vendor invoice capture) are built but not yet operationally turned on.

## Common query patterns

**Check a table's shape before writing to it:**
```sql
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '<table>' ORDER BY ordinal_position;
```

**Check existing convention values before inventing new ones (e.g. attachment categories, entity types):**
```sql
SELECT DISTINCT entity_type, attachment_type, category FROM public.attachments ORDER BY 1,2,3;
```

**Recognition-layer lookups** (used at runtime by `sjs-master` and the four bridges, not read from static files):
```sql
SELECT id, name FROM public.vendors;
SELECT id, sku, name FROM public.products;
SELECT slug, title, content FROM public.wiki_pages WHERE page_type='supplier';
SELECT slug, title, content FROM public.wiki_pages WHERE page_type='partner';
SELECT slug, title, content FROM public.wiki_pages WHERE page_type='contact';
```

## Write discipline

`plm-assistant` is the **sole PLM writer** — every other skill stages a proposed write and hands it to `plm-assistant`, or (for `outlook-plm-bridge`) writes directly but follows the same confirm-then-execute discipline. Never ingest banking details or financial account numbers into PLM.

## Where the deeper structure lives

- `.claude/skills/outlook-plm-bridge/references/flows.md` — the full Flow A–I extraction logic and SQL patterns for every inbound/outbound PLM write type
- `references/architecture/system_map.md` — which skill owns which PLM interaction
