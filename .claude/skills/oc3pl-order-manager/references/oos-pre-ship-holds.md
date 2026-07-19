# OOS Pre-Ship Holds — Reference (order side)

OC3PL maintains a daily Google Sheet (*Sweet July - Dashboard*) that lists open orders blocked by an OOS or short SKU and a curated, post-triage Problem Orders list with substitution decisions. Those orders are pre-ship — they haven't fulfilled yet — so the action belongs in this skill, not in SJ Shipping Dashboard (which is post-ship). This skill reads the order-level tabs, opens hold tasks in OC3PL Order Management → 🚨 Escalations / Issues, and stays out of the SKU-level shortage signal (which `inventory-manager` owns via `references/oos-shortage-sheet.md`).

## Source

- **Sheet name:** Sweet July - Dashboard
- **Sheet ID:** `1fnUJ_YmhX_hoWikQQWIH2KSGC9PjX_ZkmZIrgW39Wdc`
- **Access:** Link-shareable. If a fetch returns the *Instructions* tab content (gid=1796822748) instead of data, the share state has changed — pause and ask Alvin to re-enable link viewing before continuing.
- **Cadence:** OC3PL emails Alvin a refresh daily. Once the manual flow is validated, run on a 9am PT cron via the `schedule` skill alongside the daily Logiwa report intake.

## Tab gids

```
tab_gids:
  open_orders_oos: 2108736483      # primary feed for this skill
  problem_orders: 167293822        # post-triage decisions — overrides open_orders_oos when both have the same Order #
  shortage_by_sku: 274330540       # not parsed here — owned by inventory-manager
  overview: 0                      # not parsed here
  instructions: 1796822748         # documentation only — never parsed
```

If a fetch returns documentation-style prose instead of CSV rows, the gids have shifted. Re-discover by reading `https://docs.google.com/spreadsheets/d/{ID}/htmlview` and parsing the tab anchors.

## Fetch mechanics

CSV export URL pattern:

```
https://docs.google.com/spreadsheets/d/1fnUJ_YmhX_hoWikQQWIH2KSGC9PjX_ZkmZIrgW39Wdc/export?format=csv&gid={GID}
```

`curl -sL` handles the 307 redirect to `googleusercontent.com`. WebFetch's summarizer mangles CSV — fetch via curl in Bash and Read the file.

## Tab schemas (this skill)

### All Open Orders for OOS SKUs (gid=2108736483)

| Column | Meaning |
|---|---|
| Client | Brand |
| Order # | Customer order ID |
| SKU | The OOS / short SKU on the order |
| Total # of units per order | Order line total |
| On Hand Inventory | OC3PL's on-hand reading for the SKU at the time of report |
| Total Qty of SKU on the listed order | Quantity of this SKU on this specific order |
| Total QTY Short of that SKU | Aggregate short across all open orders minus on-hand |
| Client Requests | Pre-triage instruction (e.g., partial ship, hold, replace) |
| Replace With Item | Substitute SKU if a swap has been pre-approved |

Drives `🛑 OOS Hold` tasks per row, dedupe by `Order #`.

### Problem Orders (gid=167293822)

| Column | Meaning |
|---|---|
| Client | Brand |
| Customer Order number | Order ID |
| Item Short | The OOS SKU |
| Qty Short | Units short on the order |
| NOTES TO CLIENT | OC3PL's note explaining the issue |
| Client Response | Triaged decision from Ops (replace / hold / partial / cancel) |
| Replace With Item | Decided substitution SKU when applicable |

Curated, post-triage. If an order appears in both *Problem Orders* and *All Open Orders for OOS SKUs*, **Problem Orders wins** — its `Client Response` and `Replace With Item` are the decisions OC3PL needs.

## Asana task routing

| Source row | Task name pattern | Project | Section | Dedupe key |
|---|---|---|---|---|
| Open Orders for OOS SKUs (no Problem Orders match) | `🛑 OOS Hold — [Order #] — [SKU] short [N] (awaiting triage)` | OC3PL Order Management `1214235522292179` | 🚨 Escalations / Issues `1214235699359875` | `Order #` |
| Problem Orders | `🛑 OOS Hold — [Order #] — [SKU] short [N] (decision: [response])` | OC3PL Order Management `1214235522292179` | 🚨 Escalations / Issues `1214235699359875` | `Order #` |

Single section. No new section in Asana. The Problem Orders match upgrades the task name and body in place — the task carries the latest triage state.

## Task body template

```
OOS Pre-Ship Hold — Order {{Order #}}

SOURCE
- Sheet: OC3PL OOS Shortage Sheet
- Tab: {{All Open Orders for OOS SKUs | Problem Orders}}
- Run: {{YYYY-MM-DD}}

ORDER
- Customer: {{customer if available}}
- Channel: {{Shopify | wholesale | other}}
- Order total units: {{n}}
- Blocked SKU: {{SKU}} — qty on this order: {{n}}, qty short on this order: {{n}}

POSITION (sheet view)
- On Hand Inventory at OC3PL: {{n}}
- Aggregate short across all open orders for this SKU: {{n}}

TRIAGE
- Client request (pre-decision): {{from open_orders_oos — partial | hold | replace | cancel | blank}}
- Client response (post-decision): {{from problem_orders if present}}
- Replace with: {{substitute SKU if approved}}
- Notes to client: {{free-text from sheet}}

ACTION
- {{Cancel | Partial-ship | Substitute with [SKU] | Hold pending replenishment}}
- Once OC3PL acts, mark this task complete and update the sheet

CROSS-LINKS
- Inventory signal for {{SKU}}: see inventory-manager [Out of Stock] / [Low Stock] / [Position Variance] task in AC Brands Ops Dashboard → Inventory Management
```

## Re-run behavior

- Look up existing open `🛑 OOS Hold` tasks by `Order #` before creating new ones. Update the body with the latest tab source (Problem Orders overrides), counts, and decision. Do not duplicate.
- Auto-complete tasks whose `Order #` is absent from both order-level tabs for two consecutive runs. Append a sync-back comment naming the run that cleared it.
- If the sheet shows a decided substitution (`Replace With Item` populated, `Client Response` non-blank), include that decision in the task name suffix so a glance at the section shows what's still awaiting triage versus what's ready to ship.

## HITL

The auto-write rule for the daily Logiwa report does not extend here. These tasks affect customer outcomes — substitution, partial ship, cancel — and need an Operations confirmation per the existing HITL exception note in this skill ("Closing an open escalation"). The sync itself runs without prompts; closing a hold (or marking a substitution as actioned) requires confirmation.

## Run output

```
OOS Pre-Ship Holds — {{YYYY-MM-DD HH:MM PT}}
Tabs: open_orders_oos {{n rows}} • problem_orders {{n rows}}
Tasks: created {{n}}, updated {{n}}, auto-closed {{n}}
By state: awaiting triage {{n}} • decided (replace) {{n}} • decided (cancel) {{n}} • decided (partial) {{n}} • decided (hold) {{n}}
```

When run unattended, append the same summary as a comment on a rolling task in 🚨 Escalations / Issues titled `[Pre-Ship Hold Sync] Daily`.

## Boundaries

- This skill never writes to PLM. SKU-level inventory adjustments stay with `inventory-manager`.
- This skill never edits the sheet. OC3PL owns it. Substitution decisions are entered manually in the sheet so OC3PL sees them.
- Carrier-side issues (lost, bounce, claim) still route to `logistics-manager` Outbound — Escalations. An OOS Hold is not a carrier issue.
- End-customer complaints about an order still route to `complaint-and-event-handler` first.
- Post-ship order errors (Errors, Order Exceptions, Returns, RTS) stay in SJ Shipping Dashboard — this section is pre-ship only.
