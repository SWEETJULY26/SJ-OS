---
name: oc3pl-order-manager
description: >
  Manage OC3PL daily DTC order operations for AC Brands / Sweet July Skin. Use for
  orders, shipments, fulfillment, Logiwa reports, on-time delivery, late shipments,
  customer order errors, missing or damaged items, returns, RTS, replacement orders, or
  orders blocked pre-ship by an OOS SKU. Triggers: "upload today's Logiwa report", "log
  today's shipments", "any late orders", "weekly summary", "flag an escalation",
  "process this return", "regenerate the dashboard", "what's blocking orders today",
  "show me problem orders", "run the pre-ship hold sync". Owns the daily Logiwa parse,
  the OC3PL Order Management Asana project (incl. pre-ship OOS holds in Escalations),
  and the SJ Shipping Dashboard project (post-ship errors, returns). Hands carrier-side
  issues to logistics-manager, complaints to complaint-and-event-handler, return
  dispositions to inventory-manager. Reads the OC3PL OOS Shortage Sheet's order-level
  tabs daily; SKU-level shortage routing belongs to inventory-manager.
---

# OC3PL Order Manager

This skill manages daily order fulfillment operations for AC Brands / Sweet July Skin,
powered by the Logiwa daily shipment report sent by OC3PL.

---

## Asana surface

Two dedicated Asana projects under the each-skill-gets-its-own-project pattern.
Both are owned by this skill end-to-end.

### OC3PL Order Management

Daily Logiwa report log, escalations on OC3PL-side issues, weekly review,
SOPs. Project: `1214235522292179` ·
https://app.asana.com/0/1214235522292179/list · Team: SJ Ops
(`1202786171817904`).

Sections (GIDs cached):

- ⚙️ SOPs & Templates: `1214235510232195`
- 📋 Daily Report Log: `1214235556157469`
- 📊 Weekly Review: `1214235510232259`
- 🚨 Escalations / Issues: `1214235699359875`

Custom fields: none. Documented queue-state exception — section + date in task
name carry the workflow state. See "Status field default rule" below.

### SJ Shipping Dashboard

DTC consumer order errors, returns, return-to-sender. Operational disposition
log for end-customer order issues. Project: `1206266539116267` ·
https://app.asana.com/0/1206266539116267/list · Team: SJ Ops.

Sections (GIDs cached):

- Errors: `1206266372382518`
- Order Exceptions: `1213031356345787`
- Returns: `1206266372382519`
- Return to Sender: `1206266539116278`
- Completed: `1206266374154293`

Custom fields (already configured, GIDs cached):

- **Shipping Error Type** (multi-enum) — `1206266372382523` · options: Missing
  Item, Incorrect Item, Damaged Item, Incorrect Documentation, Not scanned,
  Never Received, System Error, Same customer, Canceled Order, Carrier
  Misshipment, Failed Delivery (and disabled options preserved)
- **Order Error Type** (enum) — `1206266374154282` · options: Delayed
  Delivery, Address Verification, Marked as Fraud, Duplicate?, Out of Stock,
  Customer Satisfaction, System Error, Input Error
- **Return Status** (multi-enum) — `1206266374154287` · options: Processing,
  Completed, Cancelled, Requested, Exchange
- **Replacement Order Created** (enum) — `1212888379839252` · Yes / No
- **Replacement Order #** (text) — `1212834161229899`
- **Product Collection** (multi-enum) — `1212893884443407` · Ceramics, Skin,
  Drinkware, Apparel, All Other Home

None of these mirror PLM. PLM doesn't track DTC consumer order errors. See
"Status field default rule" below — this is the queue-state exception with
custom fields that classify, not status-mirror.

Always use `asana_get_project_sections` before creating tasks if a section GID
isn't cached above.

## Status field default rule

This skill is the documented queue-state exception. PLM is the source of truth
for vendor + product + batch records, not for DTC consumer order activity. So
no Asana custom field mirrors a PLM column — section moves and (on SJ Shipping
Dashboard) classification fields like Order Error Type and Shipping Error Type
carry the workflow state.

Why this is fine: every Logiwa row already has a definitive ship status from
the report itself, and DTC order errors are a closed-loop disposition workflow
that lives entirely in Asana. The three-field-minimum applies to status-mirror
skills writing back to PLM — this skill doesn't write to PLM at all.

## HITL exception

This skill writes to Asana automatically without a confirmation gate, which
diverges from the standard "writes always need confirmation" rule. The
exception is intentional: the Logiwa report is the source of truth, and the
Asana log is just persistence. There's nothing to approve — Logiwa already
shipped (or didn't).

Where HITL still applies:

- Carrier escalation handoff to logistics-manager (creates a logistics task,
  needs operator confirmation)
- Customer complaint handoff to complaint-and-event-handler (intake door for
  end-customer signals, needs operator confirmation)
- Return disposition handoff to inventory-manager (writes inventory adjustment
  via plm-assistant, needs operator confirmation)
- Closing an open escalation (action, not just persistence)

Reads and dashboards never need confirmation. Auto-logging the daily report
never needs confirmation. Cross-skill handoffs always do.

---

## Daily Workflow

### Step 1 — Parse the Logiwa Report
When a Logiwa Daily Shipment Report (.xlsx) is uploaded, parse all rows. Key columns:
- `Customer Order No` — order identifier
- `Order Date` — when order was placed
- `Shipment Date Time` — when it shipped
- `Item Quantity` — units shipped
- `Carrier` — shipping carrier (e.g. FedEx)
- `Customer`, `Customer City`, `Customer State` — destination info

For each order: **Hours to Ship** = (Shipment Date Time − Order Date) in hours.
- ≤ 24h = on time
- > 24h = late
- Negative = data error → flag it

### Step 2 — Compute KPIs
- **Total Orders Shipped** — row count
- **Total Items Shipped** — sum of Item Quantity
- **Fulfillment Rate** — % of orders with a Shipment Date Time
- **On-Time Delivery Rate** — % with Hours to Ship ≤ 24
- **Avg Ship Time** — mean Hours to Ship
- **Speed Breakdown** — Under 6h / 6–24h / Over 24h buckets

### Step 3 — Log to Asana (OC3PL Order Management)
Create a task in the **📋 Daily Report Log** section. Check first that no task already exists for this date before creating.

**Task name:** `Upload Logiwa Report — MM/DD/YYYY`

**Task notes:**
```
Daily Logiwa Shipment Report — [DATE]

SUMMARY
• Total Orders Shipped: [N]
• Total Items: [N]
• Fulfillment Rate: [X]%
• On-Time Delivery (≤24h): [X]%
• Avg Ship Time: [X] hrs
• Carrier: [carrier(s)]
• Client: [client(s)]

SPEED BREAKDOWN
• ⚡ Under 6h: [N] orders
• ✓ 6–24h: [N] orders
• ⚠ Over 24h: [N] orders

[If any orders are late, list them with order # and hours to ship]
```

Mark the task complete after logging.

### Step 4 — Escalation Check
If **any order exceeds 24 hours** to ship:
- Create a task in the **🚨 Escalations / Issues** section
- Task name: `⚠ Late Shipment — [Order #] — [N]h delay`
- Notes: order number, customer, city/state, hours to ship, recommended action (notify OC3PL same day)
- Leave **incomplete** until resolved

### Step 5 — Generate the Dashboard
**Every daily report triggers a fresh dashboard.** Do not skip this step.

Build the HTML dashboard file using the full spec in the **Dashboard Spec** section below.
Output the file as `OC3PL_Dashboard_[MMDDYYYY].html` and present it to the user via `present_files`.

---

## Daily Pre-Ship Hold Sync (OOS Shortage Sheet — order side)

OC3PL's daily *Sweet July - Dashboard* sheet flags open orders blocked by OOS or short SKUs and a curated Problem Orders list with substitution decisions. Those are pre-ship — they belong to this skill, not to SJ Shipping Dashboard (post-ship). The SKU-level shortage signal (which SKUs are OOS, by how much) belongs to `inventory-manager` and routes to AC Brands Ops Dashboard → Inventory Management — never duplicate that surface here.

Run alongside the daily Logiwa parse, or independently when asked. Eventually scheduled at 9am PT via the `schedule` skill.

### Step A — Fetch the order-level tabs

Pull the two order-level tabs as CSV:

- *All Open Orders for OOS SKUs* (gid=2108736483)
- *Problem Orders* (gid=167293822)

Use the export URL pattern documented in `references/oos-pre-ship-holds.md`. `curl -sL` follows the 307 redirect cleanly.

### Step B — Build the canonical row set

Merge the two tabs by `Order #`. Where an order appears in both, *Problem Orders* wins (it's the post-triage decision); fold its `Client Response` and `Replace With Item` into the row.

### Step C — Open or update Asana tasks

For each canonical row, look up an existing open `🛑 OOS Hold` task in OC3PL Order Management → 🚨 Escalations / Issues by `Order #`:

- Found → update the body with the latest counts, source tab, and decision; update the task name suffix from `awaiting triage` to `decision: [response]` if the row moved into Problem Orders since the last run
- Not found → create a new task with name pattern `🛑 OOS Hold — [Order #] — [SKU] short [N] (awaiting triage|decision: [response])`

Project: OC3PL Order Management `1214235522292179` · Section: 🚨 Escalations / Issues `1214235699359875`. Body template lives in `references/oos-pre-ship-holds.md`.

### Step D — Auto-close cleared rows

For each currently open `🛑 OOS Hold` task, check whether its `Order #` is still present in either tab. Absent for two consecutive runs → mark the task complete and append a sync-back comment naming the run that cleared it.

### Step E — Audit

Append a summary comment to a rolling task in 🚨 Escalations / Issues titled `[Pre-Ship Hold Sync] Daily` (create on first run if missing). Format documented in the reference file.

### HITL on actions

The auto-log HITL exception (Step 3 of the daily Logiwa workflow) does not apply here. Closing a hold or marking a substitution actioned changes a customer outcome — those go through the existing "closing an open escalation" HITL path. The fetch + create/update sync itself runs without prompts.

### Boundary recap

| Where it lives | What goes there |
|---|---|
| inventory-manager → AC Brands Ops Dashboard → Inventory Management | SKU-level OOS / Low Stock / Position Variance from *Shortage by SKU* |
| **this skill → OC3PL Order Management → 🚨 Escalations / Issues** | **Order-level pre-ship holds from *All Open Orders for OOS SKUs* and *Problem Orders*** |
| SJ Shipping Dashboard | Post-ship only — Errors, Order Exceptions, Returns, RTS |

Reference: `references/oos-pre-ship-holds.md`.

---

## Dashboard Spec

The dashboard is a self-contained HTML file that:
1. Pre-loads the current report's data as seed data (already parsed)
2. Accepts future report uploads via drag-and-drop or button (SheetJS client-side parsing)
3. Is fully branded with Sweet July Skin visual identity

### Brand Requirements (ALWAYS APPLY)
Before building the dashboard, load the brand skill:
```
/mnt/skills/user/sweet-july-skin-brand/SKILL.md
```
Then embed fonts via base64 using the pattern in that skill's HTML section.

**Color palette to use:**
| Purpose | Color | Hex |
|---|---|---|
| Background | Bone | `#f4f0e8` |
| Header background | Pava Brown | `#8a665a` |
| Primary text | Dark brown | `#2a1f1a` |
| Headings / KPI A | Good Youth | `#795d50` |
| Accent / KPI B | Irie Power | `#b08a6c` |
| Borders | Pava accent | `#cab29d` |
| Muted text | Castaway | `#978369` |
| Compare Period A | Pava Brown | `#8a665a` |
| Compare Period B | Irie Power | `#b08a6c` |

**Typography:**
- Display / logo / large KPI numbers: `GT America Expanded Medium` — uppercase
- All other text: `Adrianna` (Regular for body, Demibold for labels/headings)
- Never use Google Fonts or system fonts — embed from skill assets

**Brand details:**
- Header: Pava Brown background, white/bone text — `SWEET JULY SKIN · OC3PL`
- Tagline strip below header: bone background, `#bcab83` border, "Everything Irie ·" right-aligned
- Order numbers in table: Pava Brown, bold

### Dashboard Panels

**KPI Row (4 cards, grid):**
- Total Orders Shipped
- On-Time Delivery Rate
- Avg Ship Time
- Total Items Shipped

Each card shows: current value + delta badge (▲/▼ %) when compare is active + period label.

**Date Filter Bar (sticky, below header):**
Period presets: Today · Yesterday · Last 7 Days · Last 30 Days · This Month · This Quarter · This Year · Custom Range

Custom Range opens a date picker dropdown (From / To date inputs + Apply button).

**Compare Toggle:**
- Toggle switch that enables a comparison period row
- Compare options: Previous Period · Previous Month · Previous Quarter · Previous Year
- Active date ranges shown in the compare bar
- When active: KPI cards show A vs B + delta; charts show dual bars (A = Pava Brown, B = Irie Power)

**Charts (3-column grid):**
1. Orders by State — horizontal bar chart; dual bars in compare mode
2. Ship Speed Breakdown — 3 speed buckets (Under 6h / 6–24h / 24h+) + Items per Order distribution
3. Right Panel — Period Summary in single mode; Side-by-Side comparison table with deltas in compare mode

**Brand strip between charts and table:**
Bone background, `#bcab83` border-bottom, tagline text in Castaway color.

**Order Table:**
- Speed filter tabs: All / ⚡ Under 6h / ✓ 6–24h / ⚠ 24h+
- Columns: Period (compare mode only) · Order # · Order Date · Ship Date · Customer · State · Qty · Carrier · Ship Time · Status
- Ship Time badges: green (< 6h) · blue/irie (6–24h) · red/pava (> 24h)
- Order # column: Pava Brown, bold

**Drag & drop:** full-page drop zone for new .xlsx uploads

### Date Logic
- Reference date: use today's actual date (dynamically from `new Date()`)
- Period ranges calculated relative to reference date
- Compare period auto-calculated based on selected mode:
  - Previous Period: equal-length window immediately before Period A
  - Previous Month: full prior calendar month
  - Previous Quarter: prior Q
  - Previous Year: same period, prior year

---

## Weekly Review

Every Friday (or when asked for a weekly summary):
1. Pull all Daily Report Log tasks from the current week
2. Aggregate: total orders, total items, avg fulfillment rate, avg on-time rate, escalations
3. Update the **📊 Weekly Review** section task with the rollup
4. Flag patterns: repeated late carriers, high-volume days, top states by order volume

---

## System integration

Where this skill stops and another picks up. Architecture rule: no skill
duplicates work another skill does. Call the existing skill instead.

### Called by

- `sjs-ops-system` — the System 5 master router routes any daily DTC
  fulfillment, Logiwa report, on-time delivery, late-shipment, missing or
  damaged item, return, or replacement-order question here. The router
  documents OC3PL-vs-Logistics (OC3PL-side vs carrier-side fault) and
  OC3PL-vs-complaint-handler (operational disposition vs end-customer
  intake) boundary cases.

### Hand off to logistics-manager

When a late shipment turns out to be a carrier-side issue, not an OC3PL-side
issue, the escalation moves to logistics-manager's `Outbound — Escalations`
section. Triggers for handoff:

- Carrier lost the package (RIA / lost shipment)
- Label fail at carrier scan
- Address bounce / undeliverable
- Carrier delay beyond standard transit (FedEx ≥ 3 days late on a 2-day
  service)
- Damage in transit reported by carrier
- Claim needs to be filed with the carrier

OC3PL-side issues stay here in the OC3PL Order Management Escalations section:

- Warehouse picked late
- System glitch in OC3PL's WMS
- Label printing fail at OC3PL
- Wrong carrier service selected at OC3PL

Handoff format: stage a logistics-manager task in `Outbound — Escalations`
(GID `1214370392301497`), populate Status (Exception), Vendor / Carrier
(carrier name), and PLM Link if a related shipment record exists. Comment on
the original OC3PL Escalations task linking to the logistics task and close
out on this side.

### Hand off to complaint-and-event-handler

When an end customer reports a problem with their order, that intake belongs
to complaint-and-event-handler — single intake door for all end-customer
quality signals. Triggers for handoff:

- Customer reports missing item
- Customer reports damaged item
- Customer reports never received
- Customer reports wrong item shipped
- Customer reports allergic reaction or any health concern (this is an SAE
  trigger and complaint-and-event-handler walks SKN-OPS-003)

Handoff format: stage a complaint task in the SJ Skin Complaint Log Asana
project via complaint-and-event-handler. The dispositional follow-up — return
processing, replacement order creation, RTS handling — lives in SJ Shipping
Dashboard and stays here. Complaint-and-event-handler classifies and routes
the customer-facing response; this skill manages the operational disposition
in parallel.

### Hand off to inventory-manager

When a return comes back to the warehouse, the inventory disposition decision
(sellable / damaged / discard) belongs to inventory-manager. Triggers for
handoff:

- Return physically received at OC3PL warehouse
- RTS package received
- Replacement order requires inventory pull confirmation

Handoff format: stage an inventory-manager task with the return SKU, quantity,
condition notes, and the source return task link. inventory-manager makes the
disposition call and writes any inventory adjustment via plm-assistant. The
return record itself stays in SJ Shipping Dashboard.

### What this skill does not do

- Vendor inbound freight, customs, ASN drafting, retailer outbound (UBM,
  Amazon Vendor) — that's logistics-manager.
- PLM writes — this skill never touches PLM. Inventory adjustments from
  returns route through inventory-manager → plm-assistant.
- SAE classification or recall trigger — that's complaint-and-event-handler.
- Forecast or demand planning impact from a returns spike — surface a comment
  to supply-demand-planner if a pattern emerges.

### Asana project routing summary

| Task type | Project |
|---|---|
| Daily Logiwa report log | OC3PL Order Management `1214235522292179` |
| OC3PL-side escalation (warehouse, WMS, label fail) | OC3PL Order Management Escalations |
| Pre-ship OOS hold (order blocked by short SKU) | OC3PL Order Management Escalations (`🛑 OOS Hold` task) |
| SKU-level OOS / Low Stock / Position Variance | inventory-manager AC Brands Ops Dashboard → Inventory Management |
| Carrier-side escalation (lost, bounce, claim) | logistics-manager Outbound — Escalations `1214370392301497` |
| Customer order error (DTC consumer, post-ship) | SJ Shipping Dashboard `1206266539116267` |
| End-customer complaint intake | complaint-and-event-handler SJ Skin Complaint Log |
| Return disposition / inventory adjustment | inventory-manager (writes via plm-assistant) |
| Weekly fulfillment review | OC3PL Order Management Weekly Review |

---

## Key Business Rules

| Rule | Value |
|---|---|
| On-time threshold | ≤ 24 hours order-to-ship |
| Fast ship benchmark | < 6 hours |
| Late escalation trigger | > 24 hours |
| Primary carrier | FedEx |
| Primary client | Sweet July / Sweet July Skin |
| Report source | Logiwa Daily Shipment Report (.xlsx) |
| Report frequency | Daily (sent by OC3PL each morning) |

---

## Common Requests

| Request | Action |
|---|---|
| Upload .xlsx / "here are today's orders" | Parse → KPIs → Asana log → escalation check → **generate dashboard** |
| "Log today's report" | Ask for file if missing → run full workflow including dashboard |
| "What were today's numbers?" | Pull latest Daily Report Log task from Asana |
| "Any late orders?" | Filter Hours to Ship > 24 → surface in chat + Escalations section |
| "Weekly summary" | Aggregate this week's log tasks → update Weekly Review task |
| "Update the dashboard" / "regenerate dashboard" | Rebuild full dashboard with latest data |
| "Add an escalation for [order]" | Classify OC3PL-side vs. carrier-side → Create task in 🚨 Escalations section, OR hand off to logistics-manager Outbound — Escalations |
| "Close out [escalation]" | Mark escalation task complete in Asana |
| "Customer says they didn't get their order" | Hand off to complaint-and-event-handler for intake, then mirror disposition in SJ Shipping Dashboard |
| "Log a missing/damaged item from a customer" | Hand off to complaint-and-event-handler first, then create the SJ Shipping Dashboard task with classification fields |
| "Process this return" | Create SJ Shipping Dashboard Return task → hand inventory disposition off to inventory-manager once received |
| "FedEx lost the package" | Hand off to logistics-manager Outbound — Escalations (carrier-side issue, not OC3PL-side) |
| "What's blocking orders today" / "any new OOS orders" / "show me problem orders" | Run the Pre-Ship Hold Sync — fetch the OOS sheet's order tabs, open/update `🛑 OOS Hold` tasks in 🚨 Escalations / Issues |
| "Run the pre-ship hold sync" | Same as above — full sync against the OC3PL OOS Shortage Sheet |

---

## Notes for Claude

- Dashboard is generated on **every** daily report upload — it's part of the standard workflow, not optional
- Always embed brand fonts via base64 — never use Google Fonts in the dashboard
- Check for existing Asana log tasks before creating duplicates
- Logiwa columns may vary — match semantically (order date, ship date, qty)
- Keep reporting tone clean and direct — no fluff
- Negative Hours to Ship = data error, flag it explicitly
- Before creating an escalation, classify: OC3PL-side (warehouse, WMS, label fail) stays in this skill's Escalations section; carrier-side (lost, bounce, claim, transit-time blow-out) hands off to logistics-manager
- An end-customer reporting any order issue is a complaint-and-event-handler intake first; SJ Shipping Dashboard is the operational disposition log, not the customer-facing intake door
- This skill never writes to PLM. Inventory adjustments from returns route through inventory-manager → plm-assistant under HITL
- Pre-ship OOS holds belong here in OC3PL Order Management → 🚨 Escalations / Issues, never in SJ Shipping Dashboard. Shipping Dashboard is post-ship only. SKU-level shortage signals (which SKUs are OOS, by how much) belong to inventory-manager — never duplicate that surface; reference its task instead
- Order-level OOS Pre-Ship Hold Sync details — sheet ID, tab gids, schemas, body template, dedupe and auto-close rules — live in `references/oos-pre-ship-holds.md`
