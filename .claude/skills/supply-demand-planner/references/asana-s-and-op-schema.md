# Asana S&OP project schema

The Sweet July Skin S&OP project (GID `1214347479282044`) is the Asana write
target for this skill. Team: SJ Ops (`1202786171817904`). All write paths
land here.

## Sections

Six sections, in order:

1. **Monthly Run** — parent task per S&OP cycle. One task per run named
   `[YYYY-MM] S&OP Run`. Subtasks: run summary text, one-pager link, bulk
   approval status, links to all child Buy Recs / Filler entries / Exceptions
   for that run.
2. **Buy Recommendations** — one task per finished-good or component buy. Custom
   field `buy_type` distinguishes (`finished_good` vs. `component`). Picked up
   by purchasing-manager on approval.
3. **Filler Schedule** — one task per filler × SKU × month with recommended
   batch size, target run-start window, and bulk-to-fill alignment notes.
   Internal-facing — not sent to fillers from this skill.
4. **Exceptions** — one task per SKU × channel × month that auto-flagged out
   of bulk approval. Reviewer-assigned (Operations default; PD lead + Brand
   lead for new-launch ratifications).
5. **Risk Watch** — open monitoring tasks across runs. Stockout risk, overstock
   risk, vendor transition flags, packaging lead-time risk. Carries between
   runs until closed.
6. **Archive** — closed runs, resolved risks, ratified exceptions. Historical
   reference.

## Section GIDs (real, smoke-tested 2026-04-28)

| Section | GID |
|---|---|
| Monthly run | `1214374670198667` |
| Buy Recommendations | `1214374670198668` |
| Filler Schedule | `1214374670198669` |
| Exceptions | `1214374670198670` |
| Risk Watch | `1214374670198671` |
| Archive | `1214374670198672` |

Note: an empty default "Untitled section" (`1214347479282072`) sits at the top
of the project — Asana created it automatically. Ignore or delete; the skill
never writes there.

## Custom field GIDs (real, smoke-tested 2026-04-28)

Nine custom fields. Eight are project-scoped. One — Sales Channel — is a
shared org-level field used across other Asana projects.

| Field | Field GID | Type | Options (label / GID) |
|---|---|---|---|
| Buy Type | `1214374670198642` | enum | Finished Good `1214374670198643`, Component `1214374670198644` |
| Sales Channel | `1208152716721482` | enum (org-shared) | Amazon `1208152716721485`, SJ Oakland `1208152716721486`, Web Store `1208152716721487`, UBM `<TBD on first read>` |
| Vendor | `1214375949849118` | text | — |
| Recommended Qty | `1214374670198647` | number | — |
| Target Ship By | `1214374670198649` | date | — |
| Run ID | `1214374670198651` | text | — |
| SKU | `1213879801597825` | text | — |
| Urgency | `1214374670198654` | enum | Now `1214374670198655`, Next 30 `1214374670198656`, Next 60 `1214374670198657`, Next 90 `1214374670198658` |
| Exception Reason | `1214374670198660` | multi_enum | Variance `1214374670198661`, New Launch `1214374670198662`, Low Cover `1214374670198663`, Auto Adjusted `1214374670198664`, Vendor Transition `1214374670198665` |

UBM was added to Sales Channel after the smoke test. The skill reads its
option GID on first run and caches it.

## Sales Channel mapping (org-shared field)

Sales Channel is reused across Asana — its options are not S&OP-specific.
The skill maps internal channel identifiers to Asana display values:

| Internal (forecast_lines.channel) | Asana Sales Channel option |
|---|---|
| `dtc` | Web Store |
| `ubm` | UBM |
| `amazon` | Amazon |
| `n_a` (run-summary tasks, vendor-only filler) | leave unset |

`SJ Oakland` is irrelevant to forecasting — the skill never writes it and
ignores it on read.

## Title Case mapping

Asana dropdown values are Title Case for readability. The skill uses
lowercase_snake internally (matches PLM and reference files). Mapping:

| Internal | Asana display |
|---|---|
| `finished_good` | Finished Good |
| `component` | Component |
| `now` | Now |
| `next_30` | Next 30 |
| `next_60` | Next 60 |
| `next_90` | Next 90 |
| `variance` | Variance |
| `new_launch` | New Launch |
| `low_cover` | Low Cover |
| `auto_adjusted` | Auto Adjusted |
| `vendor_transition` | Vendor Transition |

When reading Asana for run reconciliation, lowercase the option name and
replace spaces with underscores before matching against PLM data.

## Tags

Two workspace-level tags (confirmed exist in workspace `ac-brands.com`):
- `vendor_transition` — applied to any task tied to a SKU × component undergoing
  vendor transition during the run window
- `auto_adjusted` — applied to any task whose underlying forecast received an
  auto-adjustment this run

## Write patterns

### Monthly Run task

```
Name: [YYYY-MM] S&OP Run
Section: Monthly Run
Description: Run summary (forms/monthly-run-summary.md)
Custom fields: run_id, sku=N/A
Subtasks: Bulk Approval Status, One-Pager Link, Exceptions Bundle Link
```

### Buy Recommendation task

```
Name: BUY [vendor] [SKU or component] [qty] [target_ship_by]
Section: Buy Recommendations
Description: Math + signal + dependencies (forms/buy-recommendation.md)
Custom fields: buy_type, channel, vendor, recommended_qty, target_ship_by, run_id, sku, urgency
Tags: auto_adjusted (if applicable), vendor_transition (if applicable)
```

### Filler Schedule task

```
Name: FILL [filler] [SKU] [target month]
Section: Filler Schedule
Description: Batch size, run-start window, bulk-to-fill notes (forms/filler-calendar.md)
Custom fields: channel, vendor (=filler), recommended_qty, run_id, sku
```

### Exception task

```
Name: EXC [SKU] [channel] [trigger]
Section: Exceptions
Description: Triggers, current vs. prior, recommended action (forms/exception-review.md)
Custom fields: channel, run_id, sku, exception_reason
Assigned: Operations (or PD lead + Brand lead for new launches)
```

### Risk Watch task

```
Name: RISK [risk type] [SKU or vendor]
Section: Risk Watch
Description: Risk type, signal, mitigation, owner
Custom fields: channel, run_id, sku, urgency
Tags: vendor_transition (if applicable)
```

## Cross-skill linking

When the S&OP skill creates a Buy Recommendation, purchasing-manager is the
downstream owner. Task gets a comment with a link to the relevant
purchasing-manager Asana project (when that project exists per the
"each skill gets its own Asana project" convention).

When the S&OP skill creates a Risk Watch task tied to inventory, inventory-
manager is the downstream owner. Same comment-link pattern.

## Archive policy

When all child tasks of a Monthly Run are closed (Buy Recs handed off,
Exceptions resolved, Filler Schedule executed), the Monthly Run task moves
to Archive section. Risk Watch tasks stay in Risk Watch until individually
resolved — they're cross-run by design.
