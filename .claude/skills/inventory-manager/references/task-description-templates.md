# Task Description Templates — Inventory Manager

One template per HITL queue prefix. The skill writes the description; Operations reads it. Keep templates terse — Operations is reviewing many of these in a day.

## [Receive] PO Number — Vendor

```
Receipt — PO {{PO #}} from {{Vendor}}

DELIVERY
- Arrival date: {{date}}
- Carrier: {{carrier}}
- Condition: {{notes — pallet count, damage, seal status}}

LINES (expected vs. received)
- {{SKU/Component}} — expected {{qty}}, received {{qty}}, batch {{batch ID}}
- ...

DOCS
- COA: {{attached / pending}}
- Packing slip: {{attached / missing}}
- Other: {{...}}

PLM STAGING
- Batch entry staged: {{batch ID, expiry, location: OC3PL}}
- Awaiting Operations approval to commit

NEXT
- On commit: hand back to Purchasing → [PO Received — Pending Invoice]
```

## [Position Variance] SKU — Location

```
Three-way variance — {{SKU}} at {{Location}}

POSITIONS
- PLM: {{n}}
- Shopify: {{n}}
- Logiwa: {{n}}

DELTA
- PLM vs Logiwa: {{±n}}
- PLM vs Shopify: {{±n}}
- Shopify vs Logiwa: {{±n}}

CONTEXT
- Last successful sync: {{timestamp per source}}
- Recent movements: {{last 7 days}}
- Open receipts: {{any in-flight}}

PROPOSED CORRECTION
- Adjust PLM to {{source}} value: {{rationale}}
- Awaiting Operations approval
```

## [Low Stock] SKU — Location

```
Low stock — {{SKU}} at {{Location}}

POSITION
- On hand: {{n}}
- Safety stock threshold: {{n}}
- Days of supply at current run rate: {{n}}

CONTEXT
- Last receipt: {{date, qty}}
- Open POs: {{any in-flight}}
- Lead time: {{days}}

ROUTING
- Multi-homed to Purchasing → Reorder Review
- Quantity math owned by future Supply / Demand Planner
```

## [Out of Stock] SKU — Location

```
Out of stock — {{SKU}} at {{Location}}

POSITION
- On hand: 0

CONTEXT
- Last receipt: {{date, qty}}
- Open POs: {{any in-flight}}
- Lead time: {{days}}
- Channel impact: {{Shopify availability, Amazon availability}}

ROUTING
- Multi-homed to Purchasing → Reorder Review (urgent)
```

## [Near Expiry 90d/60d/30d] Batch — SKU

```
Near expiry — Batch {{batch ID}} ({{SKU}})

EXPIRY
- Expiration date: {{date}}
- Days remaining: {{n}}
- Threshold: {{90 / 60 / 30}}d

POSITION
- Quantity remaining in batch: {{n}}
- Location: {{location}}

RECOMMENDATION
- FEFO pull: prioritize this batch in fulfillment
- Write-off candidate at {{date}} if not consumed
```

## [Write-Off Review] Batch — SKU — Reason

```
Write-off review — Batch {{batch ID}} ({{SKU}})

REASON
- {{Expired / Damaged / Quality fail / Other}}
- Evidence: {{photo, COA, count sheet}}

POSITION
- Quantity to write off: {{n}}
- Current location: {{location}}

PLM STAGING
- Write-off entry staged
- Awaiting Operations approval to commit

FINANCIAL FLAG
- Hand to Finance for valuation impact (out of scope here)
```

## [Adjustment Review] SKU — Location — ±Qty

```
Adjustment review — {{SKU}} at {{Location}}

CHANGE
- Direction: {{+ / -}}
- Quantity: {{n}}
- Reason: {{count variance / damage found / system correction / other}}
- Evidence: {{count sheet, photo, source}}

PLM STAGING
- Adjustment entry staged
- Awaiting Operations approval to commit
```

## [Return Intake] RMA Number — SKU — Disposition?

```
Return intake — RMA {{RMA #}} ({{SKU}})

HANDOFF
- From: oc3pl-order-manager
- Physical receipt at OC3PL: {{date}}

CONDITION
- Notes: {{packaging integrity, product state}}
- Photos: {{attached / pending}}

PROPOSED DISPOSITION
- {{Sellable / Quarantine / Write-off}}
- Rationale: {{...}}

PLM STAGING
- Return movement entry staged
- Awaiting Operations approval to commit
```

## [Movement Review] SKU — From → To

```
Movement review — {{SKU}}: {{From}} → {{To}}

TRANSFER
- Quantity: {{n}}
- Batch: {{batch ID}}
- Expected date: {{arrival}}
- Transport owner: {{logistics-manager when v4 ships / vendor / OC3PL outbound}}
- Related PO or transfer order: {{ref}}

PLM STAGING
- Movement entry staged (in-transit pool until arrival)
- Location change commits on arrival confirmation
- Awaiting Operations approval
```

## [OOS Sync Log] Daily

```
OOS Shortage Sync (SKU side) — {{YYYY-MM-DD HH:MM PT}}

TABS PARSED
- overview: {{n rows}}
- shortage_by_sku: {{n rows}}
- open_orders_oos: {{n rows, cross-check only}}

TASK ACTIVITY
- Created: {{n}}
- Updated: {{n}}
- Auto-closed: {{n}}

BY TYPE
- [Out of Stock]: {{n}}
- [Low Stock]: {{n}}
- [Position Variance]: {{n}}

NOTES
- {{Any anomalies — gid drift, fetch retries, PLM mismatch counts}}
- Order-level rows handled by oc3pl-order-manager
```

## [Reconcile] Period

```
Reconciliation — {{week of YYYY-MM-DD}}

SCOPE
- OC3PL three-way diff: PLM vs Shopify vs Logiwa
- Run by: {{schedule / on-demand}}

RESULTS
- SKUs in sync: {{n}}
- Variances opened: {{n}} → see [Position Variance] tasks
- Largest variance: {{SKU, delta}}

PUSH
- Aggregated into the weekly inventory health report
```
