# Auto-adjustment rules

Forecasts auto-adjust based on signals from sjs-comp-intel and sjs-retail-intel.
Every adjustment surfaces in the run summary with signal source, signal date,
math applied, and before/after numbers. Bulk approval covers all of them; any
single one can be rejected from the exception list before bulk approval clears.

Defaults live in `settings` under `sdp_auto_adjust_*` keys. Tune in PLM, not
in the skill.

## Adjustment library

| Signal | Factor | Window | Settings keys |
|---|---|---|---|
| Direct comp launch (same archetype + price band) | -10% on overlapping SJS SKU | 90 days post-launch | `sdp_auto_adjust_direct_comp_factor` (-0.10), `sdp_auto_adjust_direct_comp_days` (90) |
| Indirect comp launch (adjacent archetype or different price band) | -5% on overlapping SJS SKU | 60 days post-launch | `sdp_auto_adjust_indirect_comp_factor` (-0.05), `sdp_auto_adjust_indirect_comp_days` (60) |
| sjs-retail-intel benchmark above expectation | +5% on next 90 days | 90 days from signal | `sdp_auto_adjust_retail_above_factor` (0.05), `sdp_auto_adjust_retail_above_days` (90) |
| sjs-retail-intel benchmark below expectation | -10% on next 90 days | 90 days from signal | `sdp_auto_adjust_retail_below_factor` (-0.10), `sdp_auto_adjust_retail_below_days` (90) |
| Vendor transition in flight | hold flat (no auto-adjustment), flag risk | duration of transition | `sdp_auto_adjust_vendor_transition_hold` (true) |

## How factors compose

Multiple signals can fire on the same SKU × channel × month. Compose
multiplicatively:

```
auto_adjustment_factor =
  (1 + direct_comp_factor)^direct_comp_active
  × (1 + indirect_comp_factor)^indirect_comp_active
  × (1 + retail_above_factor)^retail_above_active
  × (1 + retail_below_factor)^retail_below_active
```

`*_active` is 1 if the signal is in window, 0 otherwise. Vendor transition
hold short-circuits everything: if true, factor = 1.0 and a Risk Watch task
gets staged.

Cap composed adjustment at -25% / +15% to prevent runaway swings from compound
signals. If the cap binds, surface that explicitly in the run summary.

## What counts as a "direct" vs. "indirect" comp

sjs-comp-intel classifies its launches. The skill reads that classification.
For reference:

- **Direct:** same archetype (formula_hero, ritual_hero, accessory, bundle) AND
  same MSRP band (within ±$5). Example: Rhode launches a $42 toner → direct
  hit on Pava Toner.
- **Indirect:** same archetype, different price band; or adjacent archetype,
  same band. Example: Summer Fridays launches a $58 cleansing balm (different
  band) → indirect hit on the SJS cleansing balm.

If sjs-comp-intel hasn't classified, default to indirect. Surface the
classification gap in the run summary so Operations can override.

## What counts as "above/below expectation" on retail

sjs-retail-intel produces a quarterly benchmark vs. the cohort. The skill reads
the binary classification:

- **Above expectation:** SJS sell-through index > cohort median + 1 std dev
- **Below expectation:** SJS sell-through index < cohort median − 1 std dev
- **In line:** between bounds → no adjustment

The benchmark fires once per quarter. Adjustment runs for the next 90 days
from publication date.

## Vendor transition

When a SKU's PLM record has an active vendor transition (e.g., HCT → Impress
mid-launch), forecast holds flat at last locked level. Reasoning: forecast
shifts are noise during transitions; downstream buy decisions need stability
to align with new lead times. Risk Watch task captures the transition status.

Once transition closes (new vendor's first PO is acknowledged), normal
auto-adjustments resume.

## Signal staleness

If a signal hasn't refreshed in 30+ days, mark it stale in the run summary
but still apply. Stale signals are flagged so Operations can request a refresh
from sjs-comp-intel or sjs-retail-intel before locking the run.

## Run summary entry shape

Every auto-adjustment fires one line in the run summary:

```
[SKU] [channel] [month]: auto-adj [factor]
  Source: [comp-intel | retail-intel] | Signal date: [YYYY-MM-DD]
  Window: [N days remaining]
  Before: [units] | After: [units] | Delta: [+/-N units]
  Reject? [link]
```

If user clicks Reject on a single line, that adjustment removes from the
forecast and re-stages with adjustment factor 1.0 for that SKU × month.
