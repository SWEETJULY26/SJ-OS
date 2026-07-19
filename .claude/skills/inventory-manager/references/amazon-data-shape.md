# Amazon Data Shape — v1 Definition

Inventory Manager v1 defines the PLM fields the future Amazon sync will populate. Sync stand-up is a separate effort. Once shipped, Amazon position becomes part of position queries and the weekly health report. Amazon does not get a location record because the sync feeds a per-SKU quantity rather than a physical pool we manage.

## PLM fields

Per SKU:

- `amazon_on_hand` — integer, units physically at Amazon FBA
- `amazon_inbound` — integer, units in transit to Amazon FBA (inbound shipments)
- `amazon_reserved` — integer, units reserved by Amazon for orders, transfers, or processing
- `amazon_unsellable` — integer, units at FBA in unsellable state (damaged, expired, customer-returned)
- `amazon_last_sync` — timestamp, last successful sync from Amazon
- `amazon_sync_status` — enum: `ok` / `stale` / `error`

These fields belong on the SKU record (not the batch record) — Amazon FBA does not surface batch-level data through the standard inventory APIs.

## Sync source (when stand-up ships)

Two viable paths:

- Amazon Seller Central → Reports → Inventory → "Manage FBA Inventory" report, plus the FBA Inbound Shipment report. Polled on a schedule (daily is fine for v1).
- SP-API InventoryEntities resource if API access is set up. Lower latency, more setup overhead.

Pick the simpler one for v1. The schedule and polling logic live with the sync, not in this skill.

## Behavior once sync is live

- Position queries include Amazon quantities alongside OC3PL and other locations
- Out-of-stock at Amazon opens `[Out of Stock] SKU — Amazon` and routes to Purchasing's reorder review
- Low-stock at Amazon (against a configurable Amazon-specific threshold, separate from the Logiwa safety stock report) opens `[Low Stock] SKU — Amazon`
- The weekly health report breaks out Amazon position separately from OC3PL
- Three-way reconciliation (PLM vs. Shopify vs. Logiwa) does not extend to Amazon — Amazon is a separate truth feed, not three-way diffed

## Out of scope for the future sync

- FBA-to-OC3PL transfers (Logistics Manager when v4 ships)
- Multi-pack and bundle SKU mapping (will need a SKU map; v1 sync handles base SKUs only)
- FBA fee analysis (Finance system)
- Amazon DSP and ad spend (Marketing)
- Removal orders and Amazon liquidations (later iteration once volume warrants it)
