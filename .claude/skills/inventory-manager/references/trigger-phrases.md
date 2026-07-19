# Trigger Phrases — Inventory Manager

Grouped by intent. The skill's frontmatter description carries the canonical trigger set for routing; this file is the longer reference for ambiguous phrasings the operator might use day-to-day.

## Position queries

- "what's on hand for [SKU]"
- "how much [product] do we have"
- "where's our stock"
- "where is [SKU] right now"
- "show position by location"
- "give me a position snapshot"
- "how much [SKU] is at [location]"
- "what do we have at [contract manufacturer]"
- "Shopify says we have X — is that right"
- "what's the inventory position for [SKU]"

## Receiving

- "log the receipt for PO #X"
- "PO #X arrived"
- "[Vendor] just delivered"
- "received the order from [vendor]"
- "the [component] came in"
- "log the goods received"
- "PO #X is in"
- "we got the shipment from [vendor]"
- "create the batch for the [vendor] receipt"

## Location movements

- "move [SKU] from [A] to [B]"
- "[Vendor] is shipping us X units"
- "transfer [N] units of [SKU] to [destination]"
- "samples just shipped to [retailer]"
- "we're sending stock to Ulta DC"
- "stock arrived at [location]"
- "what's in transit"
- "what's in transit from [vendor]"
- "log the transfer to [contract manufacturer]"

## Reconciliation

- "reconcile inventory"
- "three-way diff"
- "are we in sync"
- "PLM vs Shopify vs Logiwa"
- "show position variances"
- "where are we drifting"
- "is OC3PL aligned with Shopify"
- "run the recon"

## Low / out of stock

- "show low stock"
- "what's at or below safety stock"
- "what's out of stock"
- "low stock alerts"
- "what's running low"
- "when did we last get the safety stock report"
- "process the safety stock report"

## OOS shortage sheet sync (SKU side)

- "pull the OOS sheet"
- "run the shortage sync"
- "process today's shortage feed"
- "sync the shortage dashboard"
- "did the OOS sync run"

(Order-level phrasings — "what's blocking orders today", "show me problem orders" — route to `oc3pl-order-manager`.)

## Expiry / FEFO

- "what's near expiry"
- "what expires in the next 90 days"
- "FEFO pull for [SKU]"
- "what's expired"
- "show me write-off candidates"
- "near-expiry sweep"
- "any batches aging out"

## Adjustments, write-offs, returns

- "adjust stock for [SKU] by [N]"
- "write off the [batch]"
- "RMA #X came back"
- "the [batch] is damaged"
- "found [N] more units in count"
- "log the count variance"
- "return came in from [customer]"
- "what's the disposition on RMA #X"
- "send [batch] to quarantine"

## Health report

- "weekly inventory health"
- "give me the inventory rollup"
- "inventory health for the week"
- "send the inventory report to Sweet July"
- "what's the state of inventory"
- "inventory snapshot for the founder briefing"

## What's open in inventory

- "what's open in inventory"
- "what needs my approval in inventory"
- "show me the inventory queue"
- "any HITL items in inventory"
