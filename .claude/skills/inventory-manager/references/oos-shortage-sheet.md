# OOS Shortage Sheet — Reference (SKU side)

OC3PL maintains a daily Google Sheet that flags out-of-stock and short SKUs and the open orders blocked by them. This skill reads only the SKU-level tabs to drive position signals into Asana. The order-level tabs (*All Open Orders for OOS SKUs* and *Problem Orders*) belong to `oc3pl-order-manager` — see that skill's `references/oos-pre-ship-holds.md`. The sheet is **not** a write target — PLM stays canonical.

## Source

- **Sheet name:** Sweet July - Dashboard
- **Sheet ID:** `1fnUJ_YmhX_hoWikQQWIH2KSGC9PjX_ZkmZIrgW39Wdc`
- **Access:** Link-shareable. If a fetch returns the *Instructions* tab content (gid=1796822748) instead of data, the share state has changed — pause and ask Alvin to re-enable link viewing before continuing.
- **Cadence:** OC3PL emails Alvin a refresh daily. Once this skill stabilizes, run on a 9am PT cron via the `schedule` skill.

## Tab gids

```
tab_gids:
  overview: 0                      # parsed for headline weekly health count only
  shortage_by_sku: 274330540       # primary feed for this skill
  open_orders_oos: 2108736483      # owned by oc3pl-order-manager — used here only as a cross-check signal
  problem_orders: 167293822        # owned by oc3pl-order-manager — not parsed here
  instructions: 1796822748         # documentation only — never parsed
```

If a fetch returns documentation-style prose instead of CSV rows, the gids have shifted. Re-discover by reading `https://docs.google.com/spreadsheets/d/{ID}/htmlview` and parsing the tab anchors.

## Fetch mechanics

CSV export URL pattern (one fetch per tab):

```
https://docs.google.com/spreadsheets/d/1fnUJ_YmhX_hoWikQQWIH2KSGC9PjX_ZkmZIrgW39Wdc/export?format=csv&gid={GID}
```

`curl -sL` (or any client that follows redirects) handles the 307 to `googleusercontent.com` automatically. WebFetch's summarizer mangles CSV output — prefer `curl` via Bash and Read the file rather than asking the WebFetch model to relay rows.

## Tab schemas (this skill)

### Overview (gid=0)

| Column | Meaning |
|---|---|
| Client | Brand (Sweet July Skin) |
| Total Units Short for Open Orders | Headline number — total units short across all open OOS-blocked orders |

Used for the headline count in the weekly inventory health report. No tasks generated.

### Shortage by SKU (gid=274330540)

| Column | Meaning |
|---|---|
| Client | Brand |
| SKU | The OOS / short SKU |
| Total Units Short Per SKU | Total units short across all open orders for this SKU |

Drives `[Out of Stock]`, `[Low Stock]`, or `[Position Variance]` tasks per SKU after PLM reconciliation (see below).

### All Open Orders for OOS SKUs (gid=2108736483) — cross-check only

This tab is owned by `oc3pl-order-manager`. This skill reads it only to compare its `On Hand Inventory` column against PLM `channel_inventory.computed`. If they diverge by more than ±2 units for any SKU, open a `[Position Variance]` task — the position bug needs to land before any Purchasing trigger fires.

## Reconciliation rule against PLM

For each row in *Shortage by SKU*:

1. Pull `channel_inventory.computed` for that SKU at OC3PL via `plm-assistant`. Never use `products.quantity_on_hand` for finished goods — that field is not the source of truth.
2. Decide the task type:
   - Sheet says zero AND PLM `computed = 0` → `[Out of Stock]`
   - Sheet says zero AND PLM `computed > 0` → `[Position Variance]` (the data is wrong somewhere — don't trigger Purchasing on a phantom shortage)
   - Sheet says short-but-not-zero AND PLM `computed` at or below safety stock → `[Low Stock]`
   - Sheet says short-but-not-zero AND PLM `computed` above safety stock → log only, no task
3. Cross-check using *All Open Orders for OOS SKUs* `On Hand Inventory` column for the same SKU. If it differs from PLM `computed` by more than ±2 units, open `[Position Variance]` regardless of the *Shortage by SKU* result.

## Asana task routing

| Source row | Asana prefix | Section | Multi-home | Dedupe key |
|---|---|---|---|---|
| Shortage by SKU (zero, PLM agrees) | `[Out of Stock]` | Inventory Management | Purchasing → Reorder Review | `SKU + location` |
| Shortage by SKU (at/below safety stock) | `[Low Stock]` | Inventory Management | Purchasing → Reorder Review | `SKU + location` |
| Shortage by SKU or *All Open Orders* on-hand mismatch | `[Position Variance]` | Inventory Management | — | `SKU + location` |

Order-level rows (blocked orders, substitution decisions) are not this skill's surface. They route through `oc3pl-order-manager`.

## Re-run behavior

- Look up existing open tasks by dedupe key before creating new ones. Update the body with the latest counts, age, and notes. Do not create duplicates.
- Close a task automatically when its dedupe key is absent from the sheet for two consecutive runs. Append a sync-back comment noting which run cleared it.
- Position Variance tasks never auto-close — they need an Operations decision.

## Run output

Print a summary every run:

```
OOS Shortage Sync (SKU side) — {{YYYY-MM-DD HH:MM PT}}
Tabs: overview {{n rows}} • shortage_by_sku {{n rows}} • open_orders_oos {{n rows, cross-check only}}
Tasks: created {{n}}, updated {{n}}, auto-closed {{n}}
By type: [Out of Stock] {{n}} • [Low Stock] {{n}} • [Position Variance] {{n}}
```

When run unattended via `schedule`, append the same summary as a comment on a single rolling Asana task in Inventory Management titled `[OOS Sync Log] Daily` so Operations has a single audit trail.

## Boundaries

- This skill never edits the sheet. OC3PL owns it.
- This skill does not open order-level tasks. `oc3pl-order-manager` reads the same sheet and lands `🛑 OOS Hold` tasks in OC3PL Order Management → 🚨 Escalations / Issues.
- Reorder quantity math stays out of scope (deferred to `supply-demand-planner`).
