# Exception review

Shape for one task in the Exceptions section. One per SKU × channel × month
that auto-flagged out of bulk approval.

## Task name

```
EXC [SKU] [channel] [primary trigger]
```

Examples:
- `EXC Castaway Cream UBM variance_20pct`
- `EXC Pava Toner UBM new_launch + auto_adjusted`
- `EXC Soursop Cleanser DTC low_cover`

If multiple triggers fire, name uses the first plus "+ N more" (full list in
the description). Primary trigger order: variance > new_launch > low_cover >
auto_adjusted > vendor_transition.

## Custom fields

- `channel`: `dtc`, `ubm`, `amazon`
- `run_id`: UUID
- `sku`: SKU code
- `exception_reason`: multi-select with all triggers that fired

## Description template

```
TRIGGERS
[Trigger name]: [why fired, with numbers]
[...additional triggers if any]

FORECAST PREVIEW
This run:  [units] for [period]
Last run:  [units] for [period]
Variance: [+/-N%] [+/-N units]

UNDERLYING SIGNAL
[For variance: what drove the change]
[For new_launch: launch date, days since launch]
[For low_cover: current days-of-cover, projected stockout date]
[For auto_adjusted: signal source, factor, math]
[For vendor_transition: vendor in/out, transition window]

CONTEXT
- Days-of-cover today: [N days]
- Open POs covering this SKU: [list with quantities and ETAs]
- Any production scheduled at filler: [yes/no, dates]

OPTIONS
1. ACCEPT — commit forecast as drafted
2. OVERRIDE — set manual override multiplier of [X] for [period]; reason: [text]
3. HOLD — defer this row until next run; nothing commits
4. REJECT — exclude this SKU × channel × month from this run entirely

RECOMMENDED
[One of the four, with reasoning]

REVIEWER
[Operations by default; PD lead + Brand lead if the trigger is new_launch]

NEXT STEP
Resolve in chat: "approve EXC [task id] as [option]" or open the task and
add a decision comment. Once resolved, plm-assistant commits the choice and
this task closes.
```

## Resolution flow

1. Task surfaces in run summary "Exceptions Pulled From Bulk" list
2. Operations (or assigned reviewer) reads, picks an option
3. Resolution writes to the task as a comment + `completed: true`
4. Bulk approval gating clears once all exceptions are resolved
5. plm-assistant commits the resolutions

## Sample populated task

```
EXC Pava Toner UBM new_launch + auto_adjusted

CUSTOM FIELDS
channel: ubm
run_id: 8a3f...
sku: SJS-PT-100
exception_reason: new_launch, auto_adjusted

DESCRIPTION
TRIGGERS
new_launch: 47 days post-launch (under 90-day threshold)
auto_adjusted: -10% direct comp factor from Rhode toner launch on 2026-04-15

FORECAST PREVIEW
This run: 7,200 units for 2026-08
Last run: 8,000 units for 2026-08 (the analogue-driven baseline)
Variance: -10% (-800 units), entirely from auto-adjustment

UNDERLYING SIGNAL
Rhode launched a toner at $40 on 2026-04-15. Same archetype (formula_hero,
ritual band), within direct comp threshold ($42 vs $40 = $2 spread, under $5).
Auto-adjustment of -10% applied for 90 days post-comp-launch (through 2026-07-14).

CONTEXT
- Days-of-cover today: N/A (pre-launch)
- Open POs covering this SKU: HCT bottle PO 2400023 for 8,500 units
- Production scheduled: KDC-One run scheduled 2026-05-22 to 2026-06-05 for
  8,000 units. Adjusting forecast doesn't change current production plan;
  excess goes to safety stock buffer.

OPTIONS
1. ACCEPT — commit 7,200 units. Excess from current PO becomes UBM pipe buffer.
2. OVERRIDE — set multiplier 1.0 (cancel auto-adjustment). Forecast stays at 8,000.
3. HOLD — defer; we'll see Rhode's actual market response next month.
4. REJECT — drop UBM Pava Toner forecast for 2026-08 entirely (not recommended).

RECOMMENDED
Option 1 (ACCEPT). Rhode's launch is a real signal on a directly competitive
SKU. The -10% adjustment is conservative. If Rhode underperforms, we'll see
that in the next sjs-comp-intel update and can lift the adjustment.

REVIEWER
PD lead + Brand lead (new_launch trigger requires PD + brand ratification)

NEXT STEP
Awaiting PD lead and Brand lead sign-off. Resolve in chat or open this task.
```
