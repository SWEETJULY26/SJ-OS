# PLM Database Schema

Generated from the live schema 2026-07-20. This was a genuinely missing file — `plm-assistant/SKILL.md` and `sjs-margin-architect/SKILL.md` both pointed here, but it was never created. Re-generate periodically (`information_schema.columns` + `information_schema.table_constraints` queries below) rather than hand-maintaining, since the schema changes as new tables/columns land.

**Project:** `ujkabbffvhpewpbttmmy` ("SWEETJULY26's Project") — this is PLM. Don't confuse with `ndxatsnrnlbdesridwfq` (Sweet July Business Dashboard, Amazon-only, a separate project).

To regenerate:
```sql
-- columns
SELECT c.table_name, string_agg(c.column_name || ' ' || c.data_type ||
  CASE WHEN c.is_nullable = 'NO' THEN ' NOT NULL' ELSE '' END, ', ' ORDER BY c.ordinal_position) AS columns
FROM information_schema.columns c WHERE c.table_schema = 'public' GROUP BY c.table_name ORDER BY c.table_name;

-- foreign keys
SELECT tc.table_name AS from_table, kcu.column_name AS from_column, ccu.table_name AS to_table, ccu.column_name AS to_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema='public' ORDER BY tc.table_name, kcu.column_name;
```

## Core product/sourcing

| Table | Key columns | FKs |
|---|---|---|
| `products` | id, name, sku, formula_id, barcode, current_phase, priority, target_retail_price, target_cogs, target_margin_pct, max_allowable_cogs, moq, product_status, current_price, product_type, quantity_on_hand, reorder_point/quantity, amazon_asin, amazon_skus | — |
| `components` | id, name, component_type, sku, variant, vendor_id, unit_cost, lead_time_days, cost_status, cost_notes, quantity_on_hand, reorder_point/quantity, hs_code, country_of_origin | vendor_id → vendors |
| `vendors` | id, name, vendor_type, contact_name/email (+ contact2-4), status, onboarding_checklist (jsonb), contract_renewal_date, vendor_code | — |
| `product_vendors` | product_id, vendor_id, is_primary | product_id → products, vendor_id → vendors |
| `vendor_components` | vendor_id, component_id | vendor_id → vendors, component_id → components |
| `bill_of_materials` | id, product_id, component_id, quantity, unit, version_id, unit_cost_override | product_id → products, component_id → components, version_id → bom_versions |
| `bom_versions` | id, product_id, name, status, formula_id | product_id → products |
| `bundle_items` | parent_product_id, child_product_id, quantity | both → products |
| `tech_pack_specs` | product_id, fill_weight(+tolerance/min/max), decoration_method, pantone_colors, certifications_needed | product_id → products |

## Purchasing / receiving

| Table | Key columns | FKs |
|---|---|---|
| `purchase_orders` | id, po_number, po_date, status, vendor_id, ship_to/bill_to, requested_ship_date, actual_ship_date, incoterm, freight/tax/fees_amount | vendor_id → vendors |
| `purchase_order_items` | purchase_order_id, line_number, sku, quantity, unit_cost, product_id, component_id, derived_product_id | → purchase_orders, products, components |
| `po_receipts` | purchase_order_id, received_date, is_cm_receipt — a receiving event; multiple rows per PO = partial receiving | → purchase_orders |
| `po_receipt_items` | po_receipt_id, po_item_id, quantity_received — drives inventory_transactions on creation | → po_receipts, purchase_order_items |
| `vendor_invoices` | vendor_id, invoice_number, amount, cost_category, regulatory_driver, linked_sku_id, po_id, status, ramp_message_id | → vendors, products, purchase_orders |
| `vendor_compliance_docs` | vendor_id, doc_type, issue_date, expiry_date, status, superseded_by | vendor_id → vendors, self-referencing supersede chain |
| `vendor_submissions` | vendor_id, submission_type, status, linked_product_id, linked_component_id | → vendors, products, components |
| `vendor_quality_logs` | vendor_id, log_date, severity, category, resolved | vendor_id → vendors |
| `vendor_score_overrides` | vendor_id, override_score — one row per vendor max, replaces calculated score when present | vendor_id → vendors |

## Inventory / locations

| Table | Key columns | FKs |
|---|---|---|
| `inventory_transactions` | entity_type, entity_id, transaction_type, quantity, location_id, to_location_id — **immutable ledger, never delete, use correcting entries.** quantity_on_hand on products/components is a cached SUM of this table. | → locations |
| `locations` | name, code, location_type, vendor_id, is_default_receiving, status | vendor_id → vendors |
| `location_inventory` | location_id, entity_type, entity_id, quantity — cached on-hand per location per entity, kept in sync by `trg_sync_location_inventory` | location_id → locations |
| `channel_inventory` | product_id, channel, quantity, channel_sku, last_synced_at | product_id → products |
| `inventory_targets` | product_id, channel, safety_stock_days, reorder_point/qty, target_dsi, plan_id — per-SKU × channel safety-stock targets, written by supply-demand-planner, read by inventory-manager. Distinct from channel_inventory (operational state). | → products, forecast_plans |
| `marketing_inventory` | product_id, location_id, quantity — Oakland office marketing-only counts. **Fully decoupled from operational inventory** — never references inventory_transactions/location_inventory/channel_inventory, excluded from recon/forecasting/channel sync. | → products, locations |
| `bulk_stock_adjustments` / `bulk_stock_adjustment_items` | adjustment_number, status, location_id / entity_type, entity_id, expected_qty, actual_qty | → locations |
| `batches` | product_id, batch_code, batch_quantity, shelf_life_months, supplier_production_date, sj_expiration_date, sj_pull_date, po_receipt_id, disposition | → products, po_receipts |

## Forecasting / supply planning

| Table | Key columns | FKs |
|---|---|---|
| `forecast_plans` | name, year, monthly_revenue_targets (jsonb), bundle_explosion_enabled — one per annual demand/supply cycle | — |
| `forecast_lines` | plan_id, product_id, annual_units, price_override, active_months (jsonb), vendor_id, transition_vendor_id/month, channel — one row per SKU per plan | → forecast_plans, products, vendors |
| `component_forecast_entries` | plan_id, component_id, month, planned_qty | → forecast_plans, components |
| `supply_plan_entries` | plan_id, forecast_line_id, month, planned_qty, po_id, vendor_id | → forecast_plans, forecast_lines, purchase_orders, vendors |

## Logistics / retail

| Table | Key columns | FKs |
|---|---|---|
| `outbound_orders` | retailer, retailer_po, ship_window_start/end, status — retailer POs SJS receives (Ulta UBM, Amazon Vendor, Sephora). Owned by logistics-manager. Currently empty (feature built, not yet live). | — |
| `retailer_compliance_specs` | retailer_name, version, asn_format, pallet_spec, label_spec — per-retailer routing guide extract, one row per version. Currently empty. | — |
| `shipments` | lane_type, po_id, outbound_order_id, batch_id, carrier, tracking_number, current_status, customs_status, landed_cost_line — core shipment record across inbound FG/component/outbound retailer/DTC escalation lanes. Drives landed cost rollup into sjs-margin-architect. Currently empty. | → purchase_orders, outbound_orders, batches |
| `logiwa_shipments` | shipment_order_code, customer, carrier, item_skus, shipping_weight — daily DTC fulfillment data | — |
| `shipping_monthly_metrics` | year, month, channel, on_time_delivery_rate, order_defect_rate | — |
| `quality_qos_signals` | period_label, threshold_crossed_count, on_time_delivery_rate — QoS snapshots pushed from shipping dashboard | — |

## Quality / regulatory

| Table | Key columns | FKs |
|---|---|---|
| `product_test_results` | product_id, batch_id, test_type, result, checkpoint, lab_vendor_id | → products, batches, vendors |
| `cost_change_logs` | product_id, previous_cogs, new_cogs, change_drivers (array), margin_impact_pct, decision_required | product_id → products |
| `sop_documents` | sop_id, title, revision, status, sharepoint_url, extracted_text, search_vector | — |

## Content / brand / knowledge

| Table | Key columns | FKs |
|---|---|---|
| `wiki_pages` | slug, page_type (contact/sku/supplier/partner/sop), title, content, embedding, search_vector — the recognition layer, queried live instead of static files | → products, vendors, sop_documents |
| `brand_assets` | asset_name, filename, asset_type, is_cover, is_archived, file_url — tagged for landing hub browse/search | — |
| `product_copy` | product_id, slug, core/shopify/amazon/retailers (jsonb) — marketing copy per channel, source of truth for customer-facing product names | product_id → products |
| `product_copy_photos` | product_copy_id, field_key, storage_path | product_copy_id → product_copy |
| `attachments` | entity_type, entity_id, file_name, storage_path, attachment_type, category — polymorphic file metadata. Real in-use categories: Artwork, Spec Sheet, Testing & QA, Safety & Compliance, Invoice, Quote, Asana Project, Other. | — |

## System / integration

| Table | Key columns |
|---|---|
| `audit_logs` | entity_type, entity_id, action, changed_fields (jsonb), user_email — heavily used (5,600+ rows) |
| `notifications` / `notification_preferences` | user_id, event_type, record_type/id, message, read |
| `pd_dashboard_runs` | run_date, rag_color, payload (jsonb) — one row per EOD reconciliation run; payload holds the 8-section recap |
| `graph_tokens` / `graph_ingest_log` | Microsoft Graph OAuth + per-message ingest log for the logiwa-mailbox-poller Edge Function. `graph_tokens` is service-role only, never expose to anon. |
| `integration_settings` / `settings` / `user_roles` / `user_dashboard_configs` | key/value config and per-user role/dashboard state |

## Not yet populated (schema exists, feature not operationally live)

`outbound_orders`, `retailer_compliance_specs`, `shipments`, `inventory_targets`, `vendor_invoices`, `vendor_submissions`, `component_forecast_entries`, `vendor_score_overrides` — all have real schema and real FK relationships but zero or near-zero rows as of 2026-07-20. Don't assume these flows are live just because the tables exist.
