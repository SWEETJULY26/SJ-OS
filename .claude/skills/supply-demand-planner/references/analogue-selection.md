# Analogue selection for new launches

New SJS launches don't have actuals. Forecasts come from picking an analogue —
an existing SJS SKU or a comp SKU — and applying a ramp curve. Each analogue
gets ratified by the PD lead and Brand lead before the forecast commits. No
standing analogue library; each round is fresh.

## When this applies

- Pre-launch SKU with zero actuals
- Post-launch SKU under 90 days, where trailing velocity is too noisy to trust
- Existing SKU launching on a new channel (e.g., a DTC SKU going live on UBM)

## Picking an analogue

You propose one. The PD lead and Brand lead ratify or counter-propose.

Hierarchy of preference:
1. **Internal SJS analogue** — existing SJS SKU on the same channel with similar
   archetype + price band + hero/accessory designation. Best signal because the
   sales channel and customer base match exactly.
2. **Internal SJS cross-channel** — same SKU on a different channel, scaled by
   channel size factor (DTC vs. UBM index from comp brands, see
   `wholesale-conversion.md`).
3. **External comp SKU** — comp brand SKU with similar archetype + price + retail
   placement. Use sjs-comp-intel for the latest data on the comp SKU. Only use
   if internal options don't exist.

Surface all three options when proposing. Lead with the best fit but flag the
trade-offs. Example proposal:

```
PROPOSED ANALOGUE: Castaway Cream (DTC) for Pava Toner UBM launch
Reasoning: Same archetype (formula_hero, ritual band), same price band ($42),
same launch window. Ramp 60% in M1, 80% in M2, 100% in M3.

ALTERNATIVES:
- Castaway Cream (UBM) — more direct channel match if/when UBM data exists
- Summer Fridays Soft Cleansing Balm (DTC→UBM) — comp signal, similar customer

Need ratification from PD lead and Brand lead before forecast commits.
```

## Ramp curves

Default ramp from launch month forward (apply to analogue's steady-state monthly
velocity):

| Months since launch | DTC ramp | UBM ramp | Amazon ramp |
|---|---|---|---|
| M1 | 60% | 40% | 30% |
| M2 | 80% | 70% | 50% |
| M3 | 100% | 90% | 70% |
| M4 | 110% | 100% | 90% |
| M5 | 105% | 105% | 100% |
| M6+ | 100% | 100% | 100% |

DTC ramps fastest because brand lifts the launch directly. UBM ramps slower
because Ulta sell-through builds with reviews and discovery surface area.
Amazon is slowest because organic ranking takes time.

The M4 + M5 hump on DTC and UBM reflects the launch-PR + halo-into-month-2
pattern that Sweet July's brand engine has produced on past launches. Adjust
in the override field if the launch isn't supported by PR.

These defaults live in `settings` under `sdp_ramp_<channel>_m<NN>` and can be
tuned per round.

## Pre-launch UBM through June 2026

Pre-launch UBM forecast is fully manual. No analogues, no ramps — Operations
sets each SKU × month directly via override JSONB. The skill stages and
surfaces; the numbers come from Operations.

Once UBM has 90 days of post-launch actuals (target: late September 2026), the
ramp method takes over and overrides become exception-only.

## Ratification flow

Every new-launch analogue proposal becomes an Asana task in the Exceptions
section of the S&OP project, assigned to the PD lead, with the Brand lead as
a follower. Format:

```
Task name: [Analogue ratification] [SKU name] [channel] [run_id]
Description:
- Proposed analogue + reasoning
- Alternative options
- Ramp curve to apply
- Forecast preview (M1–M6)

Sub-tasks:
- [ ] PD lead reviews — approve or counter
- [ ] Brand lead reviews — approve or counter
- [ ] Final ratification logged to PLM
```

Forecast doesn't commit until both check off. If they counter-propose, redraft
and re-stage.

## Ratification log

Each ratified analogue gets a one-line log entry in the run summary:

```
[SKU] [channel]: analogue = [analogue SKU/comp], ratified by PD lead and
Brand lead, ramp = M1 [%] / M2 [%] / M3 [%], notes
```

Log entries are not a library. Next round starts fresh. Patterns build
informally over time and feed into Operations judgment, not into a structured
analogue table.
