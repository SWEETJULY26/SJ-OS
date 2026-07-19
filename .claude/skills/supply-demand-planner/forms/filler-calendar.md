# Filler calendar entry

Shape for one task in the Filler Schedule section. One per filler × SKU ×
month. Internal-facing — Operations shares with fillers in conversation.

## Task name

```
FILL [filler] [SKU] [target month]
```

Examples:
- `FILL KDC-One Castaway Cream 2026-05`
- `FILL Vegelabs Soursop Cleanser 2026-08`

## Custom fields

- `channel`: `n_a` (filler runs serve all channels for the SKU)
- `vendor`: filler name (KDC-One Port Jervis, Vegelabs)
- `recommended_qty`: total batch size in finished units
- `run_id`: UUID
- `sku`: SKU code

## Description template

```
RUN PARAMETERS
Filler: [KDC-One Port Jervis | Vegelabs]
SKU: [SKU code + name]
Target month: [YYYY-MM]
Recommended batch: [N] units
Run-start window: [YYYY-MM-DD] to [YYYY-MM-DD]
Target warehouse arrival: [YYYY-MM-DD]
Filler lead time used: [N] days

DEMAND DRIVING THIS RUN
DTC:    [units] for [period]
UBM:    [units] for [period]
Amazon: [units] for [period]
Total:  [units] (this matches recommended batch ± safety buffer)

BULK STATUS
[ ] Bulk approved (link to Asana PD task or PLM batch record if exists)
[ ] Bulk produced (link to PLM batch record)
[ ] Bulk in place at filler

If any unchecked: linked to PD task [link]; flag to PD lead.

COMPONENT STATUS
For each component in BOM:
- [Component name + vendor]: [units needed] / [units confirmed] / [delivery ETA]
- ...

If any not landed by [run-start − 14 days]: linked to Buy Recommendation [link].

ALIGNMENT NOTES
[Any notes on bulk-to-fill alignment, scrap factor, MOQ rounding, etc.]

SIZING LOGIC
Forecast demand: [N units]
Safety buffer (channel-specific): [+N units]
MOQ adjustment: [if rounded up, by how much]
Final batch size: [N units]

LINKED ARTIFACTS
- Driving forecast plan: Plan A id [UUID]
- Component buy recs: [list of Asana task links]
- PD task for SKU: [link if exists]

CLOSE-OUT
Task closes when filler confirms production start (read from PLM `batches`
record creation). Leftover/excess production becomes inventory buffer.
```

## Lifecycle states

The task moves through these stages (as comments or status updates, not
custom field):

1. **Drafted** — at run staging time
2. **Approved** — after Operations bulk approval
3. **Released** — Operations has shared with the filler in conversation
4. **In production** — filler has confirmed start (PLM batch record created)
5. **Complete** — batch closes (PLM batch_status = closed) and inventory
   reflects in channel_inventory

## Risk surfaces

If at any point a Filler task can't make its target window:
- **Bulk not approved by run-start − 14 days** → escalate to PD lead, flag in
  Risk Watch
- **Component not landed by run-start − 14 days** → escalate to purchasing-
  manager, link the relevant Buy Rec, flag in Risk Watch
- **Filler capacity conflict** (multiple SKUs targeting same week at same
  filler) → flag in Risk Watch with proposed deconfliction (move smaller
  batch one week earlier or later)

## Sample populated task

```
FILL KDC-One Castaway Cream 2026-05

CUSTOM FIELDS
channel: n_a
vendor: KDC-One Port Jervis
recommended_qty: 12,000
run_id: 8a3f...
sku: SJS-CC-50

DESCRIPTION
RUN PARAMETERS
Filler: KDC-One Port Jervis
SKU: SJS-CC-50 Castaway Cream 50ml
Target month: 2026-05
Recommended batch: 12,000 units
Run-start window: 2026-05-15 to 2026-05-29
Target warehouse arrival: 2026-08-01
Filler lead time used: 70 days + 7 transit = 77 days

DEMAND DRIVING THIS RUN
DTC:    1,500 for 2026-08
UBM:    8,000 for 2026-08 (sell-in including UBM launch buffer)
Amazon: 500 for 2026-08
Total:  10,000 + 20% UBM safety buffer = 12,000

BULK STATUS
[x] Bulk approved (PD task [link])
[x] Bulk produced (PLM batch BC-2026-04-12)
[ ] Bulk in place at filler — ETA 2026-05-10

COMPONENT STATUS
- Element 50ml double-wall jar: 12,600 needed / 14,500 ordered / ETA 2026-05-08 ✓
- Impress secondary carton: 12,000 needed / 12,500 ordered / ETA 2026-05-07 ✓
- HCT pump: 12,300 needed / 14,000 in stock at KDC-One ✓

ALIGNMENT NOTES
All components on track. Bulk arrival 2026-05-10 supports run-start 2026-05-15.
No conflicts with other SJS runs at KDC-One in May.

SIZING LOGIC
Forecast demand: 10,000 units (Aug)
Safety buffer (UBM 60d / 30 = 2× monthly UBM portion): +6,000 units
Total recommended: 16,000
MOQ adjustment: capped at 12,000 for May run; remaining 4,000 plus any
top-up demand goes to next monthly run.
Final batch size: 12,000

LINKED ARTIFACTS
- Plan A: [UUID]
- Component buy recs: BUY Element jar (link), BUY Impress carton (link)
- PD task: SJS-CC-50 Castaway Cream Formula Tracker (link)

CLOSE-OUT
Task closes when KDC-One confirms run start (PLM batch record creation).
```
