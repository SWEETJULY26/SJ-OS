# Filler calendar method

The skill produces a recommended monthly fill calendar at KDC-One (skincare)
and Vegelabs (cleansing/body). Internal-facing — the calendar lives in the
S&OP project's Filler Schedule section. The skill does not talk to fillers.
Operations shares the calendar with each filler in conversation as needed.

## Filler scope

- **KDC-One Port Jervis** — skincare formulas: serums, creams, eye treatments,
  toners, lip treatments. Default lead time 70 days (`sdp_filler_kdc_one_lead_time_days`).
- **Vegelabs** — cleansing balms, body care, oil-forward formulas. Default
  lead time 60 days (`sdp_filler_vegelabs_lead_time_days`).

Other fill partners (Allure Labs, Milinyc Beauty) are out of v3 scope. Surface
as Risk Watch if a SKU is being filled at a non-default partner so Operations
sees the gap.

## What the calendar contains

Per filler × SKU × month, three pieces of information:

1. **Recommended batch size** — usually one production run per SKU per month at
   a size keyed off forecast demand × (target_dsi/30) plus safety-stock days.
   See "Sizing logic" below.
2. **Target run-start window** — the date range when filling should kick off
   to land at the right inventory month. Computed as
   `target_inventory_date − filler_lead_time_days`.
3. **Bulk-to-fill alignment notes** — has the bulk material arrived at the
   filler? Are components in place? Any blockers from purchasing or QC?

## Sizing logic

For finished-good demand `D(SKU, channel, month)`:

```
total_monthly_demand = sum over channels of D(SKU, ch, month)
batch_target_units = total_monthly_demand × (1 + safety_stock_buffer)
```

Where `safety_stock_buffer` is `safety_stock_days / 30`. Default UBM safety
buffer is 60/30 = 2.0× monthly demand on UBM-active SKUs. DTC is 45/30 = 1.5×.

If a SKU produces below the filler's MOQ at calculated batch size, round up
to MOQ and surface the over-produce in the Filler task description — purchasing
sees it as a multi-month supply. Default to checking with the PD lead if the
over-produce is more than 3× monthly demand.

If a SKU produces above the filler's max batch size, split into multiple runs
within the month. Each run gets its own Filler Schedule task.

## Run-start window math

```
target_inventory_in_warehouse_date = first day of target_month
filler_run_start = target_inventory_in_warehouse_date − filler_lead_time
                  − transit_buffer (default 7 days)
```

Express the run-start as a window: `[filler_run_start − 14 days, filler_run_start]`.
The window absorbs filler scheduling slack.

If the run-start window falls in the past (forecast was set too late), surface
a Risk Watch task: "Late forecast — [SKU] for [target month] cannot make
filler lead time. Earliest available month: [computed]."

## Bulk-to-fill alignment

Before staging a Filler Schedule task, the skill checks:

- Is the bulk formula approved and produced?
  - If not, link to the relevant Asana PD task and flag in description
- Are all components in place at the filler?
  - Run BOM explosion → check inventory_targets and channel_inventory at
    each component vendor's "in transit to filler" location
  - Flag any component not landed by `filler_run_start − 14 days`
- Are there any open QC tasks tied to the SKU?
  - Quality-manager v5 will own the read; for now, flag a manual check

Flags surface in the Filler Schedule task description, never block staging.
Operations sees them and decides.

## Cross-filler dependencies

When a SKU's BOM has multiple bulks (rare for SJS but possible), align run
windows. Document the chain explicitly:

```
Castaway Cream — KDC-One fill
  Bulk arrives: 2026-08-10 from KDC-One bulk room
  Filler run-start: 2026-08-15 to 2026-08-29
  Target warehouse: 2026-10-01 (UBM Q4 demand)
```

## Recommended calendar shape

Output a month-by-month grid by filler:

```
KDC-One — May 2026
- Castaway Cream: 12,000 units, run-start 2026-05-15 to 2026-05-29
  Bulk: confirmed in place
  Components: Element jar 12,500 confirmed; Impress secondary 12,000 in transit
  Target: 2026-08-01 inventory for UBM launch buffer
- Pava Toner: 8,000 units, run-start 2026-05-22 to 2026-06-05
  Bulk: confirmed in place
  Components: HCT bottle 8,500 confirmed; Impress secondary 8,000 in transit
  Target: 2026-08-01 inventory for UBM launch buffer

Vegelabs — May 2026
- Soursop Cleanser: 6,000 units, run-start 2026-05-20 to 2026-06-03
  Bulk: confirmed in place
  Components: HCT tottle 6,500 confirmed; Impress secondary 6,000 in transit
  Target: 2026-07-15 inventory for UBM launch
```

Component quantities use a small over-buffer (default 5%) for filler scrap.

## How this flows downstream

- Filler tasks live in S&OP project as visibility for Operations
- Buy Recommendation tasks for the components that need to land before each run
  cross-link to the relevant Filler tasks
- purchasing-manager pulls Buy Recs and runs P2P, sees which Filler tasks the
  buy supports
- Filler tasks close when production confirms (read from PLM `batches` once
  batch records land)
