# Component-level demand explosion

Finished-good forecasts explode through the BOM into component-level demand
so purchasing-manager has a real components-by-month buy plan for HCT,
Element Packaging, Impress Packaging, and the rest.

The skill mirrors PLM's existing scenario model: paired plans where the base
plan holds the finished-good forecast and the paired plan holds the exploded
component forecast.

## Paired plan model

Two `forecast_plans` rows per S&OP run:

```
Plan A (base): bundle_explosion_enabled = false
  - Holds finished-good forecast in forecast_lines (one row per SKU × channel × period)

Plan B (paired): bundle_explosion_enabled = true, paired_plan_id = Plan A.id
  - Holds exploded component forecast in component_forecast_entries
  - Computed from Plan A's finished-good forecast × BOM quantities
```

Plan A is the read for sales-side forecast. Plan B is the read for purchasing
component buys. They're linked so that any change to Plan A re-explodes into
Plan B in the next run.

## Explosion math

For each finished-good forecast row:

```
fg_units(SKU, channel, period) → forecast_lines.forecast_units
                                  + monthly_demand_overrides
                                  × auto_adjustment_factor

For each component in BOM(SKU):
  component_units(component, period) +=
    fg_units(SKU, channel, period)
    × bom_quantity(SKU, component)
    × (1 + scrap_factor(component))
```

Sum across all SKUs that consume each component. `scrap_factor` defaults to
0.05 (5% buffer) for components, can be tuned per component in PLM
(field: `components.scrap_factor` — to be added if Operations wants tunable scrap).

## Lead-time shift

Component demand shifts earlier than finished-good demand by the filler lead
time + filler-side QC buffer:

```
component_target_at_filler = fg_target_warehouse_date − filler_lead_time − 7 days
component_buy_lead_time = component_vendor_lead_time + transit
component_order_by = component_target_at_filler − component_buy_lead_time
```

The skill writes the `component_order_by` date into Plan B's
`component_forecast_entries.target_order_date` field.

## What gets written

Per component × period:

```
plan_id (Plan B id),
component_id,
period_start,
period_end,
component_units (after scrap),
target_order_date,
notes (links back to all SKUs and channels that drove this number)
```

`notes` carries the trail: "Driven by Castaway Cream UBM (8,000 units), Pava
Toner UBM (4,000 units), Soursop Cleanser DTC (2,000 units). Target at filler
2026-08-15. Vendor lead 28 days. Order by 2026-07-18."

## How purchasing-manager reads

After Plan B writes commit, purchasing-manager reads `component_forecast_entries`
filtered by:

- `target_order_date` within the next 90 days (configurable via purchasing-
  manager's own settings)
- Not already covered by an open PO (purchasing-manager joins against
  purchase_orders to check coverage)

The result is a components-by-month buy plan keyed off real demand, not
historical run rates.

## Tracking volume rolls

When a new run produces Plan B with different numbers than the prior run's
Plan B, surface the deltas in the run summary so purchasing-manager knows
to re-evaluate open POs:

```
COMPONENT FORECAST DELTAS THIS RUN
HCT 30ml glass dropper bottle:
  Aug 2026: 12,000 → 14,500 (+2,500). Earlier launch ramp.
  Sep 2026: 8,000 → 7,200 (−800). Pulling back on Pava Toner DTC after
    weak retail-intel benchmark.
Element 50ml double-wall jar:
  No change.
```

Deltas above 10% on any component × month trigger a Risk Watch task tagged
with the affected vendor.

## Manual override on components

The skill doesn't support component-level manual overrides in v3. If Operations
needs to force a buy that doesn't match exploded demand, that goes through
purchasing-manager directly (not S&OP).

## What lives in PLM, what lives in this skill

- PLM owns: the BOM tables, scrap factors, vendor lead times, plan and entry
  data, all the math results
- This skill owns: the explosion logic at run time (drafts, stages, hands to
  plm-assistant for commit), the delta narrative in the run summary, the
  Risk Watch flagging
