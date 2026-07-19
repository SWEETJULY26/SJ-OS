# Exception thresholds

Bulk approval is the default for an S&OP run — Operations reviews the summary and
approves the full set in one shot. Exception logic auto-pulls SKUs that need
individual review out of the bulk and lists them for one-by-one decision.
Bulk approval doesn't clear until exceptions are handled.

Defaults live in `settings`. Tunable.

## Triggers

A SKU × channel × month exceptions out of bulk approval if any of the following
are true:

| Trigger | Default threshold | Settings key |
|---|---|---|
| Forecast change vs. prior month's locked forecast | ≥20% | `sdp_exception_variance_pct` (0.20) |
| New launch | <90 days post-launch date | `sdp_exception_new_launch_days` (90) |
| Days of cover at current burn | <60 | `sdp_exception_low_cover_days` (60) |
| Auto-adjustment fired this run | any | (built-in) |
| Vendor transition starts within window | next 60 days | `sdp_exception_vendor_transition_window_days` (60) |

If two or more triggers fire on the same SKU, the exception task lists all of
them — the SKU still only gets one task per run.

## What "this run" means for auto-adjustment

Auto-adjustments that newly fire this run trigger an exception. Auto-adjustments
that fired in a prior run and are still in window do not — they were already
approved. The skill tracks `auto_adjustments_applied` per SKU × channel × month
in run history (notes JSON on the forecast_line) and only flags new ones.

## What "vendor transition starts within window" means

If the SKU's PLM record (or a component the SKU relies on) has a vendor
transition with `transition_start_date` between today and today + 60 days,
exception fires. The exception task lists the transitioning vendor, the
incoming vendor, and the lead-time delta. Buy decisions depend on which
side of the transition the buy lands on.

## Exception task shape

Each exception writes one Asana task in the Exceptions section of the S&OP
project. Format in `forms/exception-review.md`. Key fields:

- Triggers fired (one or more from the list above)
- Forecast preview (current run vs. prior run)
- Recommended action (accept, override, hold, reject this row)
- Reviewer (Operations by default; PD lead + Brand lead for new-launch ratifications)
- Linked plan_id, run_id, product_id

Once Operations makes a decision, the task closes. When all exceptions in a run
are closed, the bulk approval can clear and writes commit to PLM.

## Tuning thresholds

Thresholds will tighten or loosen based on operating experience. Suggested
review cadence: revisit after the first three monthly runs. If too many
SKUs trip on a single trigger, raise that threshold; if too many slip
through bulk that should have been caught, lower it.

When a threshold changes, log the change in the run summary header so the
S&OP run history reads correctly: "Exception variance threshold raised from
20% to 25% on 2026-08-15 due to natural seasonality variance on holiday SKUs."

## What does NOT trigger an exception

- Forecast for an existing SKU within ±20% — bulk only
- Auto-adjustments that re-fire from a prior run still in window — bulk only
- Days of cover ≥60 — bulk only
- Routine reorder point recalcs — bulk only
- Any read-only operation — no approval required at all
