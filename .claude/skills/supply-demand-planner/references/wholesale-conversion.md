# Wholesale: sell-through to sell-in conversion

UBM and Amazon forecasts are sell-through (units consumers buy from the
retailer). Production decisions need sell-in (units the retailer buys from
us). The skill carries a per-channel conversion using DSI / WOS targets.

## The math

```
sell_in_units(period) =
    sell_through_units(period)
    × (1 + (target_dsi_days_post − target_dsi_days_pre) / 30)
    + opening_pipe_change(period)
```

In plain language: sell-in equals sell-through, plus or minus the change in
retailer days-of-supply, plus or minus the change in distribution-center
opening pipe.

For steady state where DSI is held constant, sell-in approximately equals
sell-through. The conversion matters most at:
- Initial pipe fill (pre-launch buy to seed retailer DCs)
- Promotional events (retailer pulls extra units for promo coverage)
- Seasonal builds (Q4 holiday DSI usually ramps to 90+ days)

## Channel defaults

Stored in `settings`:

| Channel | Target DSI | Pipe seed (launch) | Notes |
|---|---|---|---|
| UBM | 90 days (`sdp_default_target_dsi_ubm`) | 90 days × 30 SKUs in target stores × estimated weekly velocity | Standard prestige skincare DSI |
| Amazon | 60 days (`sdp_default_target_dsi_amazon`) | 60 days × estimated weekly velocity at Amazon FBA | Amazon optimizes to lower DSI |
| DTC | N/A (fulfillment-day inventory) | N/A | DTC ships on order — no pipe |

Override per SKU × channel is possible by writing to `inventory_targets.target_dsi`.

## Pipe seed for UBM launch

Pre-launch UBM pipe is the largest sell-in event in 2026. The math:

```
pipe_seed_units =
    target_doors × estimated_weekly_velocity × pipe_weeks
```

Where:
- `target_doors` is the number of physical Ulta locations carrying the SKU at
  launch (provided by Ulta's planning team)
- `estimated_weekly_velocity` is the analogue-derived weekly per-door velocity
  (see `analogue-selection.md`)
- `pipe_weeks` is `target_dsi / 7` plus 2 weeks for distribution-center
  in-transit (default 14 weeks for UBM at 90-day DSI)

Example: 800 doors × 0.5 units/week/door × 14 weeks = 5,600 units pipe seed
for a hero SKU at launch. Verify against actual Ulta planning input each round.

## Conversion in monthly forecast

The skill applies conversion at forecast-line write time. For UBM forecast
lines:

```
forecast_lines (channel='ubm') stores SELL-THROUGH units.
At BOM explosion time, the skill multiplies by (1 + dsi_change_factor) before
exploding through to component_forecast_entries.
```

Where `dsi_change_factor` is computed monthly based on the change in target
DSI. For most months in steady state, `dsi_change_factor = 0` and sell-in ≈
sell-through. For promo months and pipe builds, the factor is positive.

## Promotional pulls

If a UBM promo is on the calendar (e.g., 21 Days of Beauty, Fall Haul, Holiday
Beauty Bash), the retailer pulls additional inventory in the weeks leading up
to the event. Default pull factor: +30% on sell-in for the month containing
the event start.

Promo dates feed in from sjs-retail-intel and surface in the run summary as
auto-adjustment-equivalent flags.

## UBM ships through Shopify and OC3PL

UBM orders flow through the same Shopify store and the same OC3PL fulfillment
that DTC uses. Both end up as consumer-address shipments in Logiwa. The Shopify
sales-channel attribute (Web Store = DTC, UBM = UBM) is the only layer that
separates them — and **Logiwa does not carry that attribute through on order
import**. Once an order hands off to OC3PL, channel is lost.

This means Shopify is the sole authoritative source for the DTC/UBM split.
Logiwa data is SKU-level positional only and cannot be channel-attributed
between DTC and UBM.

## Actuals sources (corrected)

| Channel | Sell-in actuals source | Sell-through actuals source |
|---|---|---|
| DTC | Shopify orders (Web Store, status=fulfilled) | Same — DTC is direct |
| UBM | Shopify orders (UBM, status=fulfilled) | Manual CSV upload from Ulta |
| Amazon | Logiwa shipments to Amazon FCs (ship-to destination identifies the channel — no sales-channel tag needed) | Manual CSV from Seller Central |

Amazon stays Logiwa-sourced because Amazon FC ship-to addresses are
self-identifying — channel is in the destination, not in a tag. UBM does not
have that property because UBM ships to consumer addresses, the same as DTC.

This is a sell-in proxy until EDI 852/867 is wired for UBM and an Amazon API
integration lands (both deferred to v3.1+).

## Sell-in vs. sell-through divergence flag

When UBM sell-in (Shopify orders attributed to UBM, fulfilled) and UBM
sell-through (Ulta CSV) diverge meaningfully over a rolling 4-week window,
the skill flags a Risk Watch task: "UBM pipe is building / drawing down —
check stocking plan." The comparison is Shopify-UBM-shipped vs. Ulta CSV.
Logiwa is not part of this comparison — it cannot tell UBM from DTC.

## What the skill does not do

- Doesn't ingest Ulta retailer data via EDI (manual CSV)
- Doesn't manage opening pipe at every retailer DC (assumes consolidated DC view)
- Doesn't handle returns or chargebacks (sell-through actuals already net these out)
- Doesn't model promotional cannibalization at the SKU level (assumes promo
  pull equals incremental sell-through)
