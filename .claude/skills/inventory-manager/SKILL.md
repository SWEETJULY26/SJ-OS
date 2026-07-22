---
name: inventory-manager
description: Manage inventory operations for AC Brands, primarily Sweet July Skin. Use for on-hand position, receiving against POs, location movements, three-way reconciliation across PLM/Shopify/Logiwa, low-stock or OOS signals, near-expiry batches, FEFO pulls, write-offs, return dispositions, adjustments, or weekly health. Triggers include "what's on hand for X", "where's our stock", "receive PO #X", "three-way diff", "low stock alerts", "what's near expiry", "write-off review", "RMA came back", "adjust stock for X", "move SKU X from A to B", "weekly inventory health", "pull the OOS sheet", "run the shortage sync". Owns the multi-location ledger across OC3PL, Shopify, contract manufacturers, in-transit, and retailer DCs. Operates the AC Brands Ops Dashboard Inventory Management section in Asana, PLM as source of truth, and routes through plm-assistant, outlook-plm-bridge, outlook-asana-bridge, fireflies-asana-bridge. HITL on writes. Peer to purchasing-manager.
---

# Inventory Manager

The operations layer for AC Brands' inventory position-keeping, receiving, and location ledger. Owns batch creation on receipt, multi-location movement records, channel position reconciliation, and exception surfacing for low-stock and expiry. Mirrors the Purchasing Manager's architecture but pointed at position rather than purchase-to-pay.

## Why this exists

Inventory truth lives across Logiwa, Shopify, PLM, contract manufacturers, and (post-Ulta) retailer DCs. Those positions drift. Receiving is the moment a PO becomes stock and needs to land cleanly in PLM. Without a coordinator, batches get missed, locations go stale, and exceptions don't reach Purchasing or Finance in time. This skill keeps the position straight and the exceptions routed.

## Design principles

These shape every action the skill takes. They are not negotiable on a per-task basis.

**Human-in-the-loop on any write that changes a position.** The skill drafts and stages, Operations approves, then it commits. This applies to receipts (batch creation), location movements, manual adjustments, write-offs, and return dispositions. Reads, queries, and exception flagging are free.

**Asana = workflow surface. PLM = source of truth.** Asana holds task signal: what needs attention, what's pending, what's in flight. PLM holds the actual batch records, locations, and movement entries. All structured data lives in PLM, written via plm-assistant. Asana never stores source-of-truth data.

**No new Asana custom fields.** Inventory operates in the AC Brands Ops Dashboard → Inventory Management section using default Asana fields (assignee, due date, completion) plus templated task descriptions for structured detail. Title prefixes mark HITL queues.

**Multi-homed tasks across PD ↔ Purchasing ↔ Inventory.** When an inventory task overlaps another domain, add the same Asana task to both project sections rather than creating a duplicate. One task, multiple project homes, one owner. PD owns PD-side close. Purchasing owns purchasing-side close. Inventory owns inventory-side close.

**Boundary with Purchasing Manager.** Purchasing carries POs through draft, ack, and in-transit. Inventory picks up at receive — opens the receive task, stages the batch entry in PLM, commits on Operations approval, hands back to Purchasing for invoice and 3-way match.

**Boundary with OC3PL Order Manager.** OC3PL Order Manager owns outbound shipment KPIs from the daily Logiwa shipment report and full RMA processing for customer returns. When return stock physically lands back at OC3PL, OC3PL Order Manager hands the receive to Inventory, which records the return movement and decides disposition.

**Boundary with Logistics Manager (future v4).** Logistics owns physical transportation between locations — carrier, BOL, ETA, arrival confirmation. Inventory owns the location ledger entry. A stock transfer from OC3PL to an Ulta DC is logistics' move; the location change in PLM is inventory's commit on arrival confirmation.

**Brand scope.** Sweet July Skin first. Occasional AC Brands inventory work uses the same Inventory Management section, marked in the task description.

**Scope → plan → approve → build.** Operations' working rule (see CLAUDE.md). For any change to position, location, or workflow logic, never jump to commit without explicit approval. Default to staging the change and asking.

## The nine core jobs

### 1. Position keeping

Cross-channel on-hand surfacing across all modeled locations. Pull from PLM as source of truth, cross-reference Logiwa and Shopify for OC3PL position, surface positions at contract manufacturers and retailer DCs as recorded in PLM.

- *Trigger:* "what's on hand for [SKU]", "where's our stock", "show position by location", "how much [product] do we have at [location]", "give me a position snapshot"
- *Action:* Pull positions via plm-assistant. For the Shopify location specifically, call `mcp__Shopify__get-inventory-levels` directly (live read, not routed through PLM) and label it as the Shopify-reported figure alongside PLM's. Compose response with on-hand, allocated, available, broken out by location and by batch where relevant.
- *HITL:* none — read-only.

### 2. Receiving (PO closeout)

Picks up from Purchasing's `[PO In Transit]`. On goods arrival notification, opens the receive task, stages a batch entry in PLM, hands back to Purchasing on commit.

- *Trigger:* outlook-plm-bridge logs goods received notification, the operator marks a PO received, "log the receipt for PO #X", "PO #X arrived"
- *Action:* Open Asana task `[Receive] PO Number — Vendor` in Inventory Management. Description holds PO summary, expected vs. received quantities by line, condition notes, batch identifiers, COA reference if attached. Stage batch entry in PLM via plm-assistant.
- *HITL:* Operations approves the batch. On commit, plm-assistant creates the batch records, attaches docs, closes the receive task with a sync-back comment, and the Purchasing task moves to `[PO Received — Pending Invoice]`.

### 3. Location ledger and movements

Records every movement between any two modeled locations as a PLM movement entry. Logistics Manager (when v4 ships) calls into this skill on arrival confirmation to commit the location change.

- *Trigger:* "move [SKU] from [A] to [B]", "[Vendor] is shipping us X units", "samples just shipped to [retailer]", logistics-manager arrival confirmation, "what's in transit"
- *Action:* Open Asana task `[Movement Review] SKU — From → To`. Description holds source, destination, quantity, batch, expected date, related PO or transfer order, transport responsible party.
- *HITL:* Operations approves the commit. On approval, plm-assistant writes the location change and the movement entry. Pre-arrival movements show as "in-transit" position; on arrival the destination becomes the active location.

### 4. Three-way reconciliation

Diff PLM vs. Shopify vs. Logiwa per SKU at OC3PL. On-demand and weekly with the health report.

- *Trigger:* "reconcile inventory", "three-way diff", "are we in sync", weekly health report run
- *Action:* Pull PLM position via plm-assistant, Logiwa position per existing sync, and Shopify position via a direct live call to `mcp__Shopify__get-inventory-levels` (do not read Shopify's number back out of PLM — PLM's existing Shopify figure may itself be stale; see the open architecture question logged in `decisions/log.md` 2026-07-22 re: PLM's separate Shopify API sync). Diff per SKU across the three. Variance over the configured tolerance opens `[Position Variance] SKU — Location`. Description holds the three numbers, deltas, batch breakdown, and last sync timestamps — including which of the three sources (PLM's own Shopify-sync figure vs. this skill's direct MCP read) each Shopify number came from, until the architecture question resolves.
- *HITL:* Operations decides correction direction. On approval, plm-assistant adjusts PLM to truth — which usually means trusting Logiwa as physical reality, but may mean trusting PLM if the sync drifted in the other direction.

### 5. Low-stock and out-of-stock signal routing

Ingests the Logiwa "Sweet July Safety Stock Report" via outlook-plm-bridge. Surfaces SKUs at or below threshold and zero-on-hand SKUs as Asana tasks. Routes both to Purchasing's reorder review queue via multi-homing.

- *Trigger:* outlook-plm-bridge logs an inbound safety stock report, "show low stock", "what's out of stock"
- *Action:* Parse safety stock data into PLM via plm-assistant. SKUs at or below threshold open `[Low Stock] SKU — Location`, multi-homed to Purchasing's section. SKUs at zero open `[Out of Stock] SKU — Location`, also multi-homed.
- *Note:* Inventory does not compute reorder quantities. Quantity math waits for the future Supply / Demand Planner skill.
- *Companion feed:* Job #9 (OOS Shortage Sheet sync) drives the same prefixes from OC3PL's daily Google Sheet, reconciled against PLM `channel_inventory.computed` before tasks land. Order-level pre-ship holds from the same sheet are owned by `oc3pl-order-manager`, not this skill.

### 6. Expiry and FEFO surfacing

Flags batches at 90/60/30-day thresholds. Produces FEFO pull recommendations on request. Surfaces write-off candidates after expiry.

- *Trigger:* batch-expiry sweep (weekly with health report or on-demand), "what's near expiry", "FEFO pull for [SKU]", "what's expired"
- *Action:* Pull batch expiry from PLM via plm-assistant. 90d/60d/30d thresholds open `[Near Expiry 90d/60d/30d] Batch — SKU` tasks. Expired batches open `[Write-Off Review] Batch — SKU — Reason: Expired`.
- *Cross-post (post-v5.4):* On every near-expiry task (90/60/30d), multi-home the task into SJS Quality Management so batch-lifecycle-tracker handles the quality-side decision (continue to release, schedule late-life test, pull plan, expedite EOL) per Batch Lifecycle Procedure §7. inventory-manager keeps ownership of the operational write-off action because it's a position-changing PLM write. batch-lifecycle posts the quality call back as a comment before any write-off fires.
- *Note:* Push of FEFO order to Logiwa stays out of scope in v1. Inventory surfaces the recommended pull order; OC3PL acts on it.

### 7. Adjustments, write-offs, and return dispositions (HITL)

Three intake paths, one approval pattern. Manual count adjustments, expiry/damage write-offs, and RMA disposition all stage a PLM write that requires Operations approval.

- *Trigger:* "adjust stock for [SKU] by [N]", "write off the [batch]", "RMA #X came back", oc3pl-order-manager hands a return receive
- *Action:* Open the matching task — `[Adjustment Review] SKU — Location — ±Qty`, `[Write-Off Review] Batch — SKU — Reason`, or `[Return Intake] RMA Number — SKU — Disposition?`. Description holds quantity, reason, source evidence (count sheet, photo, RMA notes), proposed disposition for returns.
- *HITL:* Operations approves. On commit, plm-assistant writes the adjustment, write-off, or return disposition. Sellable returns become available on-hand at OC3PL. Quarantined returns sit in a Quarantine logical location. Write-offs leave the position.

### 8. Weekly inventory health report

Aggregates position by location, exceptions outstanding, near-expiry counts, low-stock and out-of-stock counts, reconciliation deltas, and movement volume. Hands off to sjs-status-reporter for the branded SJS-formatted output.

- *Trigger:* "weekly inventory health", scheduled weekly run, "give me the inventory rollup"
- *Action:* Pull aggregates via plm-assistant. Cross-check OC3PL with the latest reconciliation. Pull headline counts from the OOS Shortage Sheet *Overview* tab (units short for open orders). Compose summary. Hand off to sjs-status-reporter.
- *Branded output:* sjs-status-reporter applies SJS brand to the final report.

### 9. OOS shortage sheet sync (SKU side)

Ingests the SKU-level tabs of OC3PL's daily Google Sheet (*Sweet July - Dashboard*) — *Overview* and *Shortage by SKU* — and reconciles them against PLM `channel_inventory.computed` before opening any task. A sheet shortage that PLM disagrees with is a variance, not a Purchasing trigger. This is the first inventory job designed to run unattended; the sync path takes no user prompts.

The order-level tabs (*All Open Orders for OOS SKUs*, *Problem Orders*) are owned by `oc3pl-order-manager` — that skill lands the order-level pre-ship hold tasks. This skill reads the *All Open Orders* tab only as a cross-check on on-hand mismatches, not to create order tasks.

- *Trigger:* "pull the OOS sheet", "run the shortage sync", "what's blocking orders today", "process today's shortage feed", or scheduled daily run via the `schedule` skill at 9am PT
- *Action:* Fetch the SKU-side tabs as CSV via the live export URL. Reconcile *Shortage by SKU* against PLM. Open `[Out of Stock]`, `[Low Stock]`, or `[Position Variance]` tasks per SKU per the rules in `references/oos-shortage-sheet.md`. Re-runs update existing tasks by dedupe key; rows absent for two runs auto-close.
- *HITL:* none on the sync itself — HITL stays at the Asana task review (e.g., approving a Position Variance correction). The skill never writes back to the sheet.
- *Audit trail:* Every run appends a summary comment to a rolling `[OOS Sync Log] Daily` task in Inventory Management.
- *Reference:* Sheet ID, tab gids, schemas, reconciliation rule, and routing table all live in `references/oos-shortage-sheet.md`.

## Asana surface

- *Project:* AC Brands Ops Dashboard (GID to be confirmed on first run)
- *Section:* Inventory Management — single section, no subsections
- *Custom fields:* none new — defaults only (assignee, due date, completion)
- *Detail home:* templated task descriptions (see references/task-description-templates.md)

### HITL queue title prefixes

These prefixes mark tasks pending Operations review or signal status. The skill scans the Inventory Management section for these when asked "what's open in inventory":

- `[Receive]` — PO arrived, batch creation pending
- `[Position Variance]` — three-way diff variance (HITL)
- `[Low Stock]` — at or below safety stock from Logiwa report
- `[Out of Stock]` — zero on-hand
- `[Near Expiry 90d/60d/30d]` — expiry threshold
- `[Write-Off Review]` — pending write-off
- `[Adjustment Review]` — pending manual adjustment
- `[Return Intake]` — RMA pending disposition
- `[Movement Review]` — pending location commit
- `[Reconcile]` — periodic reconciliation result
- `[OOS Sync Log]` — rolling daily audit of the OOS shortage sheet sync (one task, comments append)

## Locations modeled in v1

- OC3PL — physical warehouse, position fed by Logiwa
- Shopify — channel reflection of OC3PL stock; modeled as its own location to catch sync drift between Logiwa, Shopify, and PLM
- In-transit — pre-arrival pool for inbound and inter-location movements
- Quarantine — receipts and returns awaiting QA or disposition
- Retailer DCs — empty in v1, populated as Ulta and others go live (Fall 2026)
- Contract manufacturers — KDC-One, Vegelabs, AMR Labs, IKS, Allure Labs, Element Packaging, HCT, Impress Packaging, CDW, Milinyc Beauty

Amazon position is tracked as a quantity field per SKU rather than as a location. Sync stand-up ships separately. See references/amazon-data-shape.md for the v1 data shape definition.

## Calls and integrations

The skill goes through other skills for source access wherever one exists. Only Asana access is direct, matching the asana-pd-manager and purchasing-manager pattern (peer orchestrators each own their own Asana surface). Bridge intake follows the queue contract at `references/architecture/bridge_queue_contract.md` — bridges post into the AC Brands Inventory project; this skill picks up.

**Reads via:**
- plm-assistant — positions, batches, locations, movements, components
- outlook-plm-bridge — inbound supplier emails routed to PLM (goods received notifications, COAs attached to receipts, the Logiwa safety stock report)
- outlook-asana-bridge — inbound signal that belongs in workflow rather than PLM
- fireflies-asana-bridge — call action items related to inventory
- Asana — direct read of own tasks in Ops Dashboard → Inventory Management, plus multi-homed tasks
- OC3PL OOS Shortage Sheet — direct CSV fetch from a link-shareable Google Sheet (see references/oos-shortage-sheet.md)
- Shopify — direct live read via `mcp__Shopify__get-inventory-levels` for Job 1 (position keeping) and Job 4 (three-way reconciliation). Added 2026-07-22 to replace inferring the Shopify number from whatever PLM's separate Shopify API sync last landed. That PLM↔Shopify API sync still exists and still feeds the landing hub inventory dashboard — this direct MCP read is additive, not a replacement for it yet. Whether the API sync is still needed now that the MCP connector exists is an open architecture question, logged in `decisions/log.md` 2026-07-22, not resolved here.

**Writes via:**
- plm-assistant — all PLM writes (batch creation, location changes, movement entries, adjustments, write-offs, return dispositions)
- Asana — direct (task creation, comments, status, multi-homing)
- sjs-status-reporter — branded output (weekly inventory health report)

**Called by:**
- `sjs-ops-system` — the System 5 master router routes any
  on-hand-position, receipt, three-way-recon, FEFO, expiry, return-disposition,
  or weekly-inventory-health question here. The router documents
  Inventory-vs-SDP and Inventory-vs-Logistics boundary cases.
- `supply-demand-planner` — at run staging, the planner reads
  `inventory-manager`'s current on-hand totals for forecast cover math;
  exposed via plm-assistant SELECT (no direct call needed, but documented
  here for clarity)
- `oc3pl-order-manager` — return-to-stock receipts hand off the
  sellable / damaged / discard disposition decision to this skill
- `logistics-manager` — landed shipments hand off receipt-side processing
  (PO closeout, batch creation) to this skill

**Never duplicates:**
- oc3pl-order-manager (outbound shipment KPIs and RMA processing — Inventory picks up at the return-to-stock receive)
- purchasing-manager (PO work pre-receipt and invoice 3-way match — Inventory picks up at receive and hands back at receive close)
- plm-assistant (all PLM writes go through it)
- the bridges (inbound email and call routing)

## Out of scope (v1)

- Reorder quantity math (future Supply / Demand Planner)
- Allocation optimization across retailers (future Supply / Demand Planner)
- Physical transport — carrier, BOL, ETA tracking (future Logistics Manager)
- Cycle-count workflow ownership (count results can be ingested as adjustments; full workflow is a later iteration)
- FEFO push to Logiwa (Inventory surfaces the pull order; OC3PL acts on it)
- Financial inventory valuation and reserves (Finance system)
- Amazon sync stand-up (data shape defined here, sync ships separately)
- Pre-launch readiness report (consolidated into the weekly health report for v1)
- 3PL onboarding / new warehouse setup

## First-run setup

On first invocation:

1. Verify the AC Brands Ops Dashboard has an Inventory Management section. If it doesn't, propose adding it, await approval, then add via Asana API.
2. Verify PLM has location records for OC3PL, Shopify, In-transit, Quarantine, and the named contract manufacturers (KDC-One, Vegelabs, AMR Labs, IKS, Allure Labs, Element Packaging, HCT, Impress Packaging, CDW, Milinyc Beauty). Propose creating any missing.
3. Confirm outlook-plm-bridge is routing on the "Sweet July Safety Stock Report" subject. Propose updating the rule if not.
4. Cache project GID and section GID for future runs.

## Trigger phrases

See references/trigger-phrases.md for the grouped trigger library.

## Task description templates

See references/task-description-templates.md for the templated descriptions per task type.

## Amazon data shape

See references/amazon-data-shape.md for the PLM field definitions the future Amazon sync will populate.

## OOS shortage sheet

See references/oos-shortage-sheet.md for the OC3PL sheet ID, tab gids, schemas, PLM reconciliation rule, and Asana routing table that drive Job #9.

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant pages from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as bridge skills process emails and meetings — reading them first gives this skill institutional memory about suppliers and SKUs without re-scanning raw sources.

### Which pages to read

- Named supplier or vendor → `'supplier/' || public.wiki_slugify(vendor_name)`
- Named product or SKU (where the request names a SKU) → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`

Vendor pages carry lead times, commercial terms, open POs, quality flags, and document trail. SKU pages carry velocity history, safety-stock context, and demand signals.

### Read query

```sql
-- Single supplier by slug (preferred — full-text search drops short acronyms like "KDC")
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));

-- Content-term sweep across suppliers (use for terms like "lead time", "MOQ", "tariff")
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_page_type => 'supplier', p_query => '{term}', p_limit => 3);
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before generating its response — read it the way a person reads a briefing document before a meeting.

### Write-back (stale pages only)

If a page is stale or `source_count = 0` and live queries produced genuine new signal not already in the wiki, update the page:

```sql
UPDATE wiki_pages
SET content = '{updated synthesized content}',
    source_count = source_count + 1,
    last_source = 'manual',
    last_source_ref = 'retrieval-skill-writeback',
    updated_at = now()
WHERE slug = '{slug}';
```

Only on genuine new signal. Never on every read.

### What this skill does NOT do

- Does not create new wiki pages (bridge skills own all wiki writes)
- Does not write to wiki on every invocation — only on genuine stale updates
- Does not replace live Asana, Supabase, or PLM queries for current task state
