# Forecast math

Pragmatic, debuggable arithmetic. No regression, no Holt-Winters, no ML. Every
number you commit to the run summary needs to be traceable to one of three
inputs: trailing velocity, seasonality factor, or a manual override.

## The base formula

For a given SKU × channel × month:

```
forecast_units(m) =
  trailing_velocity(SKU, channel)
  × seasonality_factor(SKU, channel, month)
  × manual_override_multiplier(SKU, channel, month)
  × auto_adjustment_factor(SKU, channel, month)
```

Default multipliers are 1.0. If nothing has been overridden and no auto-adjustment
fires, the forecast is `trailing_velocity × seasonality_factor`.

## Trailing velocity

Take the last 90 days of actuals from the channel's authoritative source:
- DTC: Shopify orders attributed to **Web Store** sales channel, status=fulfilled
- UBM: Shopify orders attributed to **UBM** sales channel, status=fulfilled.
  UBM orders flow Shopify → OC3PL → Logiwa to consumer addresses, the same as
  DTC. The Shopify sales-channel tag is the only attribute that separates them
  — and **Logiwa does not carry that tag through on order import**. Once an
  order hands off to OC3PL, channel is lost. Shopify is the sole authoritative
  source for the DTC/UBM split.
- Amazon: Logiwa shipments to Amazon FCs (ship-to destination self-identifies
  the channel — no tag needed)

DTC and UBM share Shopify and OC3PL. Never read raw Shopify totals without
filtering by sales channel, and never try to read DTC vs. UBM out of Logiwa
— Logiwa cannot tell them apart. Logiwa data is SKU-level positional only
between DTC and UBM and serves as a cross-check on total OC3PL volume, not
as a channel-attributable source.

Compute average daily units shipped over the trailing 90 days, exclude any
day flagged as a stockout (zero shipments while marked OOS in inventory),
multiply by 30 to get monthly velocity.

For SKUs with less than 90 days of history (post-launch but not at steady
state), use weeks-since-launch and the analogue ramp curve from
`analogue-selection.md` instead of trailing velocity.

For pre-launch SKUs (no actuals), use 100% analogue method until the first
30 days of actuals are in.

## Seasonality factor

Per channel, per month, stored in `settings` under
`sdp_seasonality_<channel>_m<NN>` (planned — set to 1.0 today, learn over
the first full year of UBM and Amazon actuals).

Approach for the first year:
- DTC: use Shopify-derived monthly indices from prior years if available
- UBM: assume 1.0 baseline, observe and revise after Q3 2026 (first quarter
  post-launch)
- Amazon: assume 1.0 baseline, revise after Q4 2026

When you set seasonality factors in settings, surface them in the run summary
so Operations can see what was applied.

## Manual override

Operations (or PD lead and Brand lead for new launches) can set an override
multiplier per SKU × channel × month. Stored in
`forecast_lines.monthly_demand_overrides` JSONB.

Example: a hero launch with planned PR push in October pushes `2026-10` to
1.4× baseline. JSONB shape:

```json
{
  "2026-10": {"multiplier": 1.4, "reason": "PR push", "set_by": "operations", "set_at": "2026-04-27"},
  "2026-11": {"multiplier": 1.2, "reason": "halo into November", "set_by": "operations", "set_at": "2026-04-27"}
}
```

Override is the loudest signal. Anything overridden ignores trailing velocity
seasonality math but still receives auto-adjustments (auto-adjustment factor
multiplies on top of override).

## Auto-adjustment factor

Computed at run time from comp-intel and retail-intel signals. See
`auto-adjustment-rules.md` for the factor library and time windows.

Auto-adjustments are bundled into bulk approval but each one surfaces in the
run summary so Operations can reject any individually.

## Sanity checks at run time

Before staging the forecast for approval, run these checks and surface any
that fail:

- Forecast variance vs. last month's locked forecast >20% (exception flag)
- Forecast units negative (math error — investigate before staging)
- Forecast for a SKU on a channel that's not in `sdp_active_channels`
  (config error)
- New launch SKU with no analogue ratified (block run, escalate to PD lead and Brand lead)
- Forecast horizon under six months on a SKU with packaging lead time over
  five months (purchasing risk flag — surface in Risk Watch)

## Output shape

Each forecast row written to `forecast_lines`:

```
plan_id, product_id, channel, period_start, period_end,
forecast_units, monthly_demand_overrides (JSONB),
notes (run_id + adjustment trail), created_at
```

Period grain is monthly. `period_start` is the first of the month;
`period_end` is the last day. Channel is one of `dtc`, `ubm`, `amazon`.
