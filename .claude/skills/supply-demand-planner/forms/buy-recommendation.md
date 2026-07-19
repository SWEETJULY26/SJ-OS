# Buy recommendation

Shape for one task in the Buy Recommendations section. One per finished-good
or component buy. purchasing-manager picks these up after bulk approval.

## Task name

```
BUY [vendor] [SKU or component name] [qty] [target_ship_by]
```

Examples:
- `BUY Element Packaging — 50ml double-wall jar — 14,500 units — ship by 2026-06-30`
- `BUY KDC-One — Castaway Cream fill — 12,000 units — ship by 2026-08-15`

## Custom fields

- `buy_type`: `finished_good` or `component`
- `channel`: `dtc`, `ubm`, `amazon`, or `n_a` (component buys serving multiple channels)
- `vendor`: vendor name (Element, HCT, Impress, KDC-One, Vegelabs, etc.)
- `recommended_qty`: number
- `target_ship_by`: ISO date
- `run_id`: UUID of the parent S&OP run
- `sku`: SKU code if finished-good; component identifier if component
- `urgency`: `now` (within next 30 days), `next_30`, `next_60`, `next_90`

Custom fields above are required — populate every one. The S&OP landing dashboard ("Buys in flight" + "What needs attention") reads `vendor`, `sku`, `recommended_qty`, and `target_ship_by` from custom fields first. The task-name format in the section above is for human readability in Asana; the dashboard's parser fallback to that name uses whitespace tokenization and won't correctly parse multi-word vendors ("Element Packaging" → "Element"), commas in quantities ("14,500" fails), or em-dash separators. So as long as custom fields are populated, the dashboard renders cleanly regardless of how the task name is styled.

## Tags

- `auto_adjusted` if the underlying forecast received an auto-adjustment this run
- `vendor_transition` if vendor is in active transition

## Description template

```
WHAT
[Vendor] — [SKU / component name]
Quantity recommended: [N]
Unit cost (PLM ref): $[X]
Total spend (estimate): $[total]
Target ship-by: [date]
Target arrival: [date] at [destination — DC, filler, etc.]

WHY
Demand driver:
- [SKU / channel / month rows that drove this buy, with units]
Lead time: [vendor lead time + transit] days
Order-by date: [target_ship_by − lead time]
Coverage: [period this buy covers, e.g. "August 2026 UBM demand + Sep–Oct DTC pull-forward"]

DEPENDENCIES
- Linked Filler task: [link]
- Linked finished-good demand task: [link]
- Other component buys aligned to same filler run: [links]

RISKS
- [Lead time tightness, vendor capacity question, etc., or "None flagged"]

ALL DRIVING FORECAST ROWS
[
  {SKU, channel, month, fg_units, this component's per-unit BOM qty, scrap factor},
  ...
]

NEXT STEP
On bulk approval: purchasing-manager picks up this task and runs P2P workflow.
PO drafts post a sync-back here.
```

## How purchasing-manager consumes this

- Reads task on approval
- Drafts PO in PLM via plm-assistant
- Posts a comment with PO number when PO commits
- Updates this task to "Awaiting ack" status
- Closes when PO is acknowledged by vendor

## Sample populated task

```
BUY Element Packaging — 50ml double-wall jar — 14,500 units — ship by 2026-06-30

CUSTOM FIELDS
buy_type: component
channel: ubm
vendor: Element Packaging
recommended_qty: 14,500
target_ship_by: 2026-06-30
run_id: 8a3f...
sku: COMP-EL-J50
urgency: next_30
TAGS: vendor_transition

DESCRIPTION
WHAT
Element Packaging — 50ml double-wall jar
Quantity recommended: 14,500 (12,000 for Aug fill + 2,500 buffer for Sep top-up)
Unit cost (PLM ref): $1.85
Total spend (estimate): $26,825
Target ship-by: 2026-06-30
Target arrival: 2026-08-01 at KDC-One Port Jervis

WHY
Demand driver:
- Castaway Cream UBM August: 12,000 units sell-in
  → 12,000 × 1 jar/unit = 12,000 jars
  + 5% scrap = 12,600 jars
  + buffer for Sep build = 14,500 jars total
Lead time: 28 days vendor + 7 days transit = 35 days
Order-by date: 2026-05-26
Coverage: August UBM build + early September DTC pull-forward

DEPENDENCIES
- Linked Filler task: KDC-One Castaway Cream August fill
- Driving FG rows: Castaway Cream UBM 2026-08, Castaway Cream UBM 2026-09

RISKS
- Element vendor in active transition to Impress secondary supplier (transition
  start date 2026-09-01). Buy lands before transition; no exposure on this
  order. Surfaced in Risk Watch for visibility.

ALL DRIVING FORECAST ROWS
- Castaway Cream / UBM / 2026-08: 12,000 fg × 1 jar = 12,000 + 5% = 12,600
- Castaway Cream / UBM / 2026-09: 1,800 fg × 1 jar = 1,800 + 5% = 1,890

NEXT STEP
On bulk approval: purchasing-manager picks up this task and runs P2P.
```
