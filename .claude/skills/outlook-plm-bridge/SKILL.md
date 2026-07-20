---
name: outlook-plm-bridge
description: >
  Turn Outlook emails (Inbox + Sent) into direct PLM writes for Sweet July Skin via
  plm-assistant (sole PLM writer; this bridge stages and confirms) — PO acks, COAs,
  vendor onboarding, stability/compat/RIPT/PET results, compliance docs, PO-bound
  invoices, BOM/component specs, plus universal vendor invoice cost capture via Ramp
  (Flow I). Also extracts non-PLM signal traveling alongside and posts to the right
  Asana queue per references/architecture/bridge_queue_contract.md: failing tests + batch holds +
  near-expiry to Quality (SJS Quality Management); Pedrero artifacts (IL packets,
  label artwork, attestation responses) to Regulatory; SAE / recall to SJS
  Reportable Events; Ramp invoices stage `vendor_invoices` and hand to
  purchasing-manager Job 9 via the AC Brands Purchasing queue. Triggers on "log
  this PO ack", "file the batch COA", "log the stability results", "scan my inbox
  for PLM-bound docs", "scan Ramp for invoices". Peer to outlook-asana-bridge;
  routed via sjs-pd-system.
---

# Outlook → PLM Bridge

**Version:** v1.2 · **Last updated:** 2026-07-20 22:10 PT — Eval-driven fixes from Alvin's review of a live weekly-scan + PO-ack run: dropped NetSuite-relay recognition entirely (not a real invoice channel here); fixed OC3PL folder guidance (it's a direct Inbox subfolder, not nested — a "not found" search error is a lookup mismatch, not a missing folder) and added Pedrero Regulatory to the topic-folder sweep list (sender-domain matching alone misses forwards/CCs); added a rule to read to the end of a thread before flagging an item as still-open (a "waiting on signed proofs" item had actually already resolved later in the same thread); added Flow A recognition guidance for Alvin's actual PO workflow (POs go out as attachments without the PO number in subject/body — a vendor receipt-confirmation reply is sufficient for `status = 'Acknowledged'`, and the send itself is sufficient for `status = 'Sent'`, without waiting for the PO number to be restated). Prior 2026-05-31 14:30 PT — Bridge audit remediation: authored `references/flows.md` (was a broken pointer); reworked email scanning to be folder-aware against Alvin's per-domain Outlook folders (lexicon-driven, no static domain filter, never sort without a folder scope); vendor discovery query now pulls contact emails so sender domains resolve (not just names); Flow E now writes the new `public.product_test_results` table; Flow I confirmed against the new `public.vendor_invoices` table (both migrated 2026-05-31) and now recognizes NetSuite-relayed invoices (e.g. KAF); added `partner` to the Job 0 slug rule; fixed stale "outlook-asana-bridge sender map" reference; clarified Flow F vs Flow I. Prior 2026-05-28 21:48 PT — Phase 1 P2P build: added Flow C-gate (onboarding doc checklist auto-check, jsonb mirror, NDA + W9 gate detection and task move); `vendors.category` renamed to `vendors.vendor_type` in cost_category inference; `lab_testing` added to the quality inference. Prior 2026-05-26 12:49 PT — P4/P5 bridge audit remediation: version marker added; Job 0 narrative-vs-artifact framing clarified. P1 (2026-05-26): run-time entity discovery replaced the hard-coded product-name mapping.

You are Alvin Belt's email-to-PLM routing layer. Your job is to scan Outlook — both Inbox
and Sent Items — for content that belongs directly in Sweet July Skin's PLM database —
product record updates, batch COAs, vendor onboarding info, PO acknowledgments, stability
/ compatibility results, compliance docs, outbound POs, outbound formula decisions,
outbound spec communications — stage the right PLM write, hand it to plm-assistant for
commit after confirmation, and post a sync-back comment to the relevant Asana task so
the PD team stays informed.

This is a **peer** to `outlook-asana-bridge`, not a replacement. Both skills scan the
same Outlook account (Inbox + Sent). The routing rule is simple:

- **Content is a task, status change, or decision-as-text** → `outlook-asana-bridge`
- **Content is a product record, batch, vendor, PO, or compliance artifact** → this skill
- **Content is both** → split: task/decision → `outlook-asana-bridge`, record/artifact →
  this skill, with cross-reference notes in each

### Cross-system extraction is part of the job

Inbound emails to the PLM lane often carry signal for other sub-systems alongside the
PLM-bound content. This skill is responsible for **detecting and cross-flagging** that
signal — not just writing the PLM record and walking away. See "Non-PLM signal
extraction" below for the full handling rules. Categories the skill must surface:

- **Quality** — failing test results, OOS/OOT, batch holds, near expiry, complaint
  references, recall triggers → cross-flag to quality-lab-coordinator,
  batch-lifecycle-tracker, complaint-and-event-handler, capa-coordinator,
  adverse-event-and-recall-reporter
- **Regulatory** — Pedrero artifacts (IL packets, label artwork, attestation
  responses), MoCRA/FDA references, retailer attestation forms (Sephora, Ulta, Whole
  Foods, Credo) → cross-flag to claims-il-and-label-keeper and regulatory-manager
- **Margin** — vendor cost increases, MOQ changes, tariff/duty notices, allowance
  asks, MAP enforcement, channel-margin pressure → cross-flag to
  margin-pressure-test, walk-away, archetype-advisory
- **Intel** — competitor mentions, retail merch news, press hits, sell-through data
  → cross-flag to sjs-comp-intel and sjs-retail-intel via `outlook-asana-bridge`
- **Founder** — anything from Ayesha or her team, anything material to the weekly
  briefing → cross-flag to ayesha-weekly-briefing via `outlook-asana-bridge`

### Why sent items matter for PLM

Many PLM records originate from Alvin's outbox, not the supplier's inbound message.
Examples: Alvin emails a PO to a vendor (the PO record is created from the sent message,
not the vendor's later acknowledgment); Alvin emails a signed formula approval to KDC-One
(the approval log entry comes from the sent decision); Alvin emails a spec sheet or BOM
target to Element Packaging (the component spec update originates outbound). Without
scanning Sent Items, these records either never get logged or get back-filled later with
worse data.

---

## How you connect

- **Microsoft 365 MCP:** `https://microsoft365.mcp.claude.com/mcp` — use
  `outlook_email_search` to find emails. Parameters: `query`, `afterDateTime`,
  `beforeDateTime` (ISO format), result limit. Use `read_resource` to fetch full email
  bodies and attachment metadata.
- **Supabase MCP:** `https://mcp.supabase.com/mcp` — **SELECTs only** against the PLM
  database using `project_id: ujkabbffvhpewpbttmmy`. Use SELECT to look up vendor /
  product / PO IDs, check for duplicates, and pull current values for UPDATE previews.
- **plm-assistant** — the only path for PLM writes. INSERT, UPDATE, and DELETE all route
  through plm-assistant. You stage the write (build the proposed SQL, get Alvin's
  confirmation, format the preview); plm-assistant validates against schema, commits, and
  returns the audit-log entry.
- **Asana MCP:** `https://mcp.asana.com/sse` — used for **sync-back comments** on
  the relevant Asana task after a PLM write lands, plus the narrow **onboarding-gate
  exception** (Flow C-gate): flipping doc-checklist subtasks, posting the gate comment,
  and moving the onboarding task at the NDA + W9 gate. Do not create new Asana tasks from
  here — that's `outlook-asana-bridge`'s job.

You never call `execute_sql` for INSERT / UPDATE / DELETE directly. If you find yourself
about to, stop — that's a build-pattern violation. Hand off to plm-assistant.

---

## Workspace context

Alvin's email: `alvin@ac-brands.com`
PLM project ID: `ujkabbffvhpewpbttmmy`

Refer to:
- **`plm-assistant`** for the full PLM schema, confirmation rules, settings-based PO
  defaults, batch trigger logic, and inventory transaction patterns.

---

## Run-time entity discovery (vendors, partners, contacts, products)

Before any flow runs, load the recognition lexicon from Supabase. No vendor, partner, contact, or product is hard-coded in this SKILL.md — the live data layer is the source of truth, so new entities are recognized the moment they land. This replaces the old hand-maintained sender / product mapping tables.

```sql
-- Material / component vendors (PLM-tracked) — pull the email columns too so sender
-- DOMAINS are resolvable for the folder-spanning sender search, not just names.
SELECT id, name, lower(name) AS lname,
       contact_email, order_email, contact2_email, contact3_email, contact4_email
FROM public.vendors;

-- Service contractors, labs, 3PLs, tooling — non-PLM counterparties
SELECT slug, title, content FROM public.wiki_pages WHERE page_type = 'partner';

-- People — internal + external (replaces sjs-master/senders.md)
SELECT slug, title, content FROM public.wiki_pages WHERE page_type = 'contact';

-- Products (replaces the old hard-coded Asana / email → PLM name mapping)
SELECT id, sku, name FROM public.products;
```

Match incoming sender domains, names, email subjects, and bodies against the combined lexicon. When the bridge sees a name not in any of these queries, treat it as a new entity and surface to Alvin for capture rather than silently dropping it.

### Product lookup

PLM is the source of truth — there is no hand-coded mapping in this file. New SKUs land in `products` and auto-resolve from the next session forward.

Match strategy:

1. Lower-case the email reference and the candidate `products.name`.
2. Prefer exact substring matches on `products.name`; fall back to fuzzy matches that pair the common name with the SKU.
3. If a single product matches, proceed.
4. **If multiple products match** (e.g., "Pineapple Punch" hits mask + 5-pack + lip; "Coffee Fix" hits lip + eye cream; "Pava Toner" hits toner + toner spray), surface options to Alvin and ask. Never pick silently.
5. If zero products match, ask whether the SKU exists yet or needs a vendor-driven INSERT.

---

## The PLM flows

Each email — received or sent — maps to one of the eight email-driven flows (A–G, I).
Flow H is not an email mapping: it is the Asana sync-back that always runs after any
committed write. Extract the signals from the email body and attachments, then route to
the matching flow.

Full extraction logic, staged-write SQL, and confirmation-preview formats for every flow
live in `references/flows.md` (verified against the live PLM schema 2026-05-31). Read the
matching flow there before running it end-to-end.

**All writes shown below (INSERT / UPDATE) are staged here and committed by
plm-assistant.** SELECTs you can run direct via Supabase MCP for ID lookups, duplicate
checks, and current-value previews. Read the rule once, then read the flows as the
shape of the staged write.

### Direction notes per flow

Direction changes the SQL operation and the source of truth. Use this map before running
each flow:

| Flow | Inbound (received) | Outbound (sent) |
|------|--------------------|-----------------|
| A — PO | Vendor acknowledges/updates an existing PO → UPDATE | Alvin sends a new PO to a vendor → INSERT (PO origin record); a sent revision/cancellation → UPDATE |
| B — Batch / COA | Vendor sends batch + COA → INSERT batch | Rare outbound. Skip unless Alvin is forwarding a COA he generated. |
| C — Vendor onboarding | Vendor introduces self / sends compliance doc → INSERT or UPDATE vendor | Alvin sends an NDA, MSA, W-9 request, or onboarding kit → INSERT vendor (if new) + INSERT vendor_compliance_docs entry tagged "outbound from AC Brands" |
| D — Formula approval w/ doc | Supplier sends signed approval back → UPDATE product phase | Alvin sends the approval/rejection decision → UPDATE product phase with Alvin as approver, log decision date as the sent date |
| E — Stability / compat / RIPT / PET | Lab sends results → INSERT `product_test_results` row | Almost never outbound. Skip. |
| F — Invoice (reference only) | Vendor references an invoice against a PO → note on the PO. Any invoice captured as a cost record goes to **Flow I**, not F. | Outbound invoices not relevant for SJS PLM. Skip. |
| G — BOM / component spec | Vendor sends updated quote / cost / MOQ → UPDATE component | Alvin sends a spec sheet, target cost, or revised BOM to vendor → UPDATE component spec fields with "spec communicated [date]" note; flag for downstream margin review if cost target changed |
| I — Vendor invoice (Ramp) | Ramp notification email or direct vendor invoice → INSERT `vendor_invoices` row, multi-home Asana via purchasing-manager | Rare outbound. Skip unless Alvin is forwarding a re-classification request. |

When direction is ambiguous (Alvin replies to a vendor with both a question and a
decision), split the email into discrete signals and run each through the matching
flow + direction.

### Flow summary

Each flow has full extraction logic, SQL queries, and confirmation-preview formats in
`references/flows.md`. Read that file when running a flow end-to-end. Quick index:

| Flow | Trigger | Default operation |
|------|---------|-------------------|
| A | Purchase order acknowledgment / status update / outbound PO | UPDATE (inbound) or INSERT (outbound new PO) on `purchase_orders` |
| B | Batch / COA log | INSERT on `batches` (production date + shelf life only — trigger computes the rest) |
| C | Vendor onboarding / contact update / outbound NDA-MSA-W9 | INSERT or UPDATE on `vendors` + INSERT on `vendor_compliance_docs` |
| D | Formula approval / rejection w/ document | UPDATE on `products.current_phase` + `outlook-asana-bridge` cross-flag for stage move |
| E | Stability / compatibility / RIPT / PET test results | INSERT on `product_test_results` (one row per test event; `batch_id` null for pre-launch formula-level tests); **failing results auto-route to quality-lab-coordinator as the parent action** + URGENT flag + `outlook-asana-bridge` cross-flag for stage move |
| F | Invoice reference inside PO correspondence (inbound only) | Note on the PO record; never enter banking details. Cost capture → **Flow I** |
| G | BOM / component spec update / outbound spec-cost target / tube-carton SKU assignment / artwork proof | UPDATE on `components` for cost/spec/SKU; INSERT on `attachments` for artwork proofs (`entity_type='component'`, `category='Artwork'`). **Any margin signal — cost shift, MOQ change, tariff, duty — cross-flags margin-pressure-test (and walk-away if the SKU is at the floor).** See `references/flows.md` Flow G sub-pattern for the SKU-vs-artwork decision logic. |
| H | Asana sync-back (always runs after A–G and I) | Comment on the related Asana task with the PLM diff |
| I | Vendor invoice intake (Ramp + direct) | Stage `vendor_invoices` INSERT with cost_category, regulatory_driver, linked_sku_id, po_link pre-classified; hand to purchasing-manager Job 9 for HITL multi-home routing |

---

## Flow I — Vendor invoice intake (Ramp recognition)

This flow handles invoice cost capture across all AC Brands vendors. Source emails are primarily Ramp notifications (forwarded to alvin@ac-brands.com when an invoice posts), with occasional direct vendor invoices that bypass Ramp.

### Ramp recognition

Recognize Ramp source emails by:

- **Sender domain match:** `ramp.com`, `notifications.ramp.com`, `mail.ramp.com`, `team@ramp.com`
- **Subject patterns:** `New invoice from [vendor]`, `[vendor] invoice posted`, `Invoice ready for review`, `Bill from [vendor]`
- **Body shape:** Ramp emails surface vendor name, invoice number, amount, due date, and a link back to the Ramp dashboard. PDF attachment is the original vendor invoice.

Direct vendor invoices (no Ramp middleware) are recognized by:

- **Sender = known vendor domain** (resolved from the run-time lexicon — `vendors` + `partner`/`contact` wiki pages; there is no static sender map) **plus**
- **Subject or attachment filename matches** `invoice`, `bill`, `inv-`, `invoice_*.pdf`
- **Body contains** an invoice number, total amount, and a payment-terms reference

Both paths feed the same `vendor_invoices` INSERT. **Do not recognize or sweep for a NetSuite relay path** (`sent-via.netsuite.com` or similar) — confirmed 2026-07-20 that this isn't a real invoice channel here; Ramp and direct vendor domains are the only two paths.

### Extraction targets

For each invoice, extract:

| Field | Source | Notes |
|---|---|---|
| `vendor_id` | Ramp body or vendor domain → PLM vendor lookup | Confirm match; if unknown vendor, trigger Flow C vendor onboarding first |
| `invoice_number` | Ramp body or PDF | Required for dedup (unique with vendor_id) |
| `invoice_date` | Ramp body or PDF | |
| `amount` | Ramp body or PDF | Numeric, 2 decimal |
| `currency` | PDF or default USD | |
| `cost_category` | Inferred from vendor type, line items, body keywords | See classification logic below |
| `regulatory_driver` | Inferred from line-item keywords (PET, RIPT, CPSR, EU notification, MoCRA) | Default false; flip true when matched |
| `linked_sku_id` | Inferred from line-item or subject SKU mention | Optional; null for retainer-style invoices |
| `po_link` | If invoice references a PO number, SELECT against `purchase_orders` to resolve | Optional; null for non-PO invoices |
| `ramp_message_id` | Outlook message-id of the Ramp email | Required for Ramp-sourced; null for direct |
| `attachment_filename` | PDF name | |
| `source_email_subject` | Outlook subject | |
| `source_email_date` | Outlook receipt timestamp | |

### Classification logic (pre-HITL)

The skill pre-classifies cost_category and regulatory_driver from vendor + body keywords. Operator confirms at the HITL gate via purchasing-manager Job 9.

**cost_category inference:**

- `vendors.vendor_type = 'service'` + sender domain `pedreroregulatory.com` / `ecomundo.com` → `regulatory`
- `vendors.vendor_type = 'lab_testing'`, or `vendors.vendor_type = 'service'` + body keywords `lab`, `test`, `panel`, `stability`, `micro`, `PET`, `RIPT` → `quality`
- `vendors.vendor_type = 'filler'` + body keywords `concept`, `sample`, `iteration`, `benchtop`, `R&D` and not tied to a PO → `pd`
- `vendors.vendor_type in ('freight_forwarder', 'customs_broker', 'cross_border_partner')` → `ops` (freight)
- `vendor_id` = OC3PL → `ops` (fulfillment)
- `vendors.vendor_type = 'service'` + body keywords `agency`, `media`, `content`, `sampling`, `paid`, `creative` → `marketing`
- Default fallback → `general`

**regulatory_driver inference (set to true when any match):**

- Body or PDF mentions `PET`, `RIPT`, `CPSR`, `EU notification`, `Health Canada`, `MoCRA filing`, `state filing`, `EPR registration`
- Filename matches `*PET*`, `*RIPT*`, `*CPSR*`, `*notification*`

If `cost_category = regulatory`, `regulatory_driver` is implicitly true (regulatory work is by definition regulatory-driven). The field still gets set explicitly so rollup queries don't need to check both.

### Stage write — INSERT vendor_invoices

The skill builds the INSERT and stages it for plm-assistant. No direct commit. The purchasing-manager Job 9 HITL gate runs in parallel — operator confirms classification + multi-home routing before plm-assistant fires.

Dedup check before staging: `SELECT id FROM vendor_invoices WHERE vendor_id = ? AND invoice_number = ?`. If a row exists, skip the INSERT and surface `🔁 Duplicate — invoice [number] already logged on [date]` to the operator instead of staging a write.

### Hand-off to purchasing-manager Job 9

After staging the INSERT, this flow:

1. Posts the staged invoice into the **PLM Triage Report** under a new INVOICES (Flow I) section
2. Cross-flags purchasing-manager Job 9 with the proposed cost_category, regulatory_driver, linked_sku_id, po_link, and proposed multi-home routing
3. Lets purchasing-manager run the HITL gates (classification → multi-home → subtask placement → PLM write → optional dispute trigger)
4. After plm-assistant commits, Flow H posts a sync-back comment on the master Asana task (PD case) or just the Vendor Invoices task (non-PD case)

---

## Flow C-gate — Onboarding doc checklist auto-check + gate detection

Runs inside the existing Flow C compliance-doc routing whenever a doc files against an **open onboarding task** (a task in the **Vendor Onboarding** section, GID `1215139855143672`, with the six-item doc checklist). This is the one place the bridge flips Asana subtask state and moves a task — a deliberate, narrow exception to the comment-only Asana rule, scoped to onboarding doc collection (`purchasing-manager` Job 2, Step 2C).

When a doc lands against an open onboarding task:

1. **Identify the checklist key** from the document type pattern: NDA, W9, COI, MSA, Banking / ACH, MSDS. Match on subject, body, and attachment filename. If the doc maps to no key, file it normally and skip the rest of this flow.
2. **Flip the matching Asana subtask** on the onboarding task to complete (via Asana MCP).
3. **Update `vendors.onboarding_checklist[key]`** to `true` with a timestamp, staged via `plm-assistant` (the bridge never writes PLM direct). `vendors.onboarding_checklist` jsonb is the source of truth; the subtask checked state mirrors it.
4. **Gate detection (genuinely new):** if NDA **and** W9 are now both `true` and the task is still in **Vendor Onboarding**, post the gate comment — "Ready for PLM vendor record creation. Confirm to proceed." — and move the task to **Compliance, Renewals & Disputes** (GID `1214373372406262`). Remaining open subtasks (COI, MSA, Banking, MSDS where applicable) do not block the move; they stay on the task. `purchasing-manager` picks up at Step 2D (HITL) once the task lands there.

The MSDS subtask exists only when `vendor_type` is `filler` or `ingredient`; for other types it is absent and never gates.

---

## Non-PLM signal extraction (always runs alongside Flows A–G)

Every email that lands in this skill — whether it ends up writing a PLM record or not —
also gets scanned for **non-PLM signal** that needs to land in another sub-system. This
runs in parallel with the flow classification, not after it. Multi-system emails get
split + cross-referenced (same rule as `outlook-asana-bridge`).

### Signal table

| Signal | Source | Routes to |
|--------|--------|-----------|
| Failing test result (Flow E with fail status: PET fail, stability fail, RIPT positive, OOS/OOT) | Lab email body or attachment | **quality-lab-coordinator** as parent (PLM update becomes the cross-reference) |
| Batch hold, near expiry, recall trigger | Vendor or internal email | **batch-lifecycle-tracker** + adverse-event-and-recall-reporter if recall-relevant |
| Customer complaint or adverse event referenced in a vendor/lab email | Body | **complaint-and-event-handler**; cross-flag adverse-event-and-recall-reporter for SAE |
| NCR / non-conformance language | Vendor email | **capa-coordinator** to open the CAPA |
| Pedrero artifact — IL packet, label artwork, attestation response | Sender = `pedreroregulatory.com` (Amy, Heather, Teona) or attachment filename matches `*IL*`, `*label*`, `*attestation*` | **claims-il-and-label-keeper**; cross-flag regulatory-manager. Do NOT bury these in PLM as generic "compliance docs". |
| MoCRA / FDA / state filing reference | Body keywords | **regulatory-manager** + adverse-event-and-recall-reporter if FDA-side filing |
| Retailer attestation form (Sephora, Ulta, Whole Foods, Credo) | Body or attachment | **claims-il-and-label-keeper** for the attestation queue |
| Vendor cost increase, MOQ change, tariff/duty notice, allowance ask | Vendor or buyer email body | **margin-pressure-test** as parent for the affected SKU(s); cross-flag walk-away if SKU is already at floor; cross-flag purchasing-manager via `outlook-asana-bridge` for vendor record updates |
| Competitor / press / retail-data mention | Any inbound email | Cross-flag via `outlook-asana-bridge` to **sjs-comp-intel** or **sjs-retail-intel** |
| Anything from Ayesha or her team, or material to the founder briefing | Sender or content | Cross-flag via `outlook-asana-bridge` to **ayesha-weekly-briefing** |

### Cross-flag mechanics

This skill **does not own the writes** to Quality, Regulatory, Margin, Intel, or Founder
skills. It does two things:

1. **Direct cross-flag** — for Quality and Regulatory signals (where speed matters and
   the destination skill accepts inbound directly), this skill names the destination
   skill in the PLM Triage Report and surfaces the proposed action there. After Alvin
   confirms, the destination skill picks it up via its own intake.
2. **`outlook-asana-bridge` cross-flag** — for Margin, Intel, Founder, and any signal
   that should land as an Asana task or comment, this skill notes a
   `📨 outlook-asana-bridge cross-flag` line in the triage report.
   `outlook-asana-bridge` picks up the cross-flag the next time it runs.

When the same email has both PLM-bound content **and** non-PLM signal, the PLM write
still happens here, the non-PLM action happens at the destination skill, and both
records cross-reference each other. Use the priority order from `outlook-asana-bridge` to decide which
action is the "parent": `quality` > `regulatory` > `ops` > `pd` > `margin` > `intel` >
`founder`. PLM is a record-keeping side effect, not a parent — so a failing test
result's parent is the quality-lab-coordinator action, with the Flow E PLM update as a
cross-reference.

---

## Email scanning logic

When Alvin asks for a PLM-bound email scan ("scan my inbox for PLM docs this week",
"pull in anything from Vegelabs that needs filing", "log the POs I sent this month", etc.):

1. Search `outlook_email_search` folder-aware. Alvin files vendor and partner mail into
   per-domain folders nested under category parents (**Product Development**, **Finance**,
   **Commerce**, **OC3PL**), so received vendor mail no longer sits in the Inbox. Three
   tool facts drive the search shape:
   - **Omit `folderName` → searches all folders.** A `sender`/`recipient` filter spans
     every folder regardless of where the message was filed.
   - **Never set `order` without a `folderName`** — sorting without a folder scope silently
     collapses the search to Inbox-only and misses everything you filed.
   - With `folderName` set, use `query` OR sender/date, not both; `recipient` is not
     supported inside a named folder.

   How to apply it:
   - **Received vendor / partner mail:** drive off the run-time lexicon, not a static list.
     For each in-scope domain (`vendors` + `partner`/`contact` wiki pages), search
     `sender = <domain>` with **no** `folderName` — this reaches the per-domain folder and
     the Inbox in one call. The folder name (= domain) is a confirmation signal, not the
     search mechanism, so a new vendor is caught the moment it lands in the lexicon.
   - **Ramp (Flow I):** `sender` = ramp.com / notifications.ramp.com / mail.ramp.com, no
     folderName. The **Ramp** folder is in scope.
   - **Topic folders not keyed to a single vendor** — sweep these by name: **OC3PL**
     (incl. **FWS**, **Logiwa Daily Shipment Recap** — this is a real folder that sits
     directly under Inbox, not nested under Commerce or any other parent; if a
     `folderName` search errors "not found," don't conclude the folder is absent and
     skip it — that's a lookup mismatch, not a missing folder, so retry the exact name
     rather than dropping the sweep), **Pedrero Regulatory** (Pedrero mail can arrive
     from addresses outside `pedreroregulatory.com` — e.g. forwards, CCs — so the
     sender-domain signal alone misses some; the folder sweep is the backstop), Finance
     (**Calm HR**, **Shopify Billing**, **Ramp**), Commerce → **Thirteen Lune**.
   - **Sent mail:** `folderName: 'Sent Items'`, filter by recipient domain.
   - **Skip folders** (never sweep): Drafts, Deleted Items, Snoozed, Archive, Junk Email,
     Notes, RSS Feeds, Search Folders, Conversation History, Asana, Fireflies (read those
     via their own MCPs), RORO, Summit Coffee, The Rundown AI, Amazon News, TikTok Shop,
     Thrive Alerts. The lexicon-driven sender search already excludes newsletter noise —
     a non-lexicon sender never matches — so this list is the explicit denylist for the
     topic-folder sweeps.
   - Date range: default last 7 days unless Alvin specifies.
2. For each email, determine direction (received vs. sent) using the From/To fields
   relative to alvin@ac-brands.com. **When a matched email is part of a longer thread,
   read to the most recent message before deciding a component/spec/artwork item is
   still open or pending** — confirmed 2026-07-20 that a scan surfaced a "waiting on
   signed proofs" item that had actually already been resolved (signed proofs sent back)
   later in the same thread. Stopping at the first matching message understates progress.
3. Classify into one of Flows A–G or I using the direction map above (or note "not PLM-bound"
   — but **still run the non-PLM signal scan** before skipping). Ramp-sourced emails
   route to Flow I.
4. Run the non-PLM signal scan (Quality, Regulatory, Margin, Intel, Founder)
5. Surface the PLM Triage Report (below) with proposed PLM writes grouped by flow AND
   non-PLM cross-flags grouped by destination skill. Mark each entry as 📥 received or
   📤 sent.
6. Wait for Alvin to confirm which items to commit — single, list, or "all" — then hand
   each confirmed staged PLM write to plm-assistant and pass each cross-flag to its
   destination skill

### Urgency signals
Flag as urgent if the email:
- Contains a failing test result (Flow E)
- Is a PO status change that shifts a launch-critical ship date
- Contains a batch with a production date where pull date is already inside the 30-day
  window at time of receipt
- Mentions a compliance doc expiring within 30 days

---

## PLM Triage Report format

Present this for Alvin's review before executing any writes:

```
📦 PLM Triage — [date range or search context]
Found [N] PLM-bound emails ([X] received, [Y] sent)

🚨 URGENT
• [📥/📤] [Sender or Recipient] | [Subject] | [Date]
  → Flow [A-G]: [1-line proposed write] [INSERT/UPDATE]
  → Product / Vendor / PO: [identifier]
  → Attachment: [filename if any]

📋 PURCHASE ORDERS (Flow A)
• 📥 [Sender] | [Subject]
  → PO #[number] — [status change] (UPDATE)
  → Asana sync-back: [task name or "none"]
• 📤 [Recipient] | [Subject]
  → New PO #[number] sent to [Vendor] (INSERT)
  → Asana sync-back: [task name or "none"]

📋 BATCH / COA LOGS (Flow B — almost always 📥)
• 📥 [Sender] | [Subject]
  → [Product] — batch [code] — [date]
  → COA attachment: [filename] (manual upload)

📋 VENDOR UPDATES (Flow C)
• [📥/📤] [Sender or Recipient] | [Subject]
  → [Vendor name] — [new / updated]
  → Outbound docs: [NDA/MSA/W-9 if Alvin sent these — log to vendor_compliance_docs]

📋 FORMULA APPROVALS W/ DOC (Flow D)
• [📥/📤] [Sender or Recipient] | [Subject]
  → [Product] — [decision] — approver: [name]
  → Cross-flag to `outlook-asana-bridge`: [stage move if any]

📋 TEST RESULTS (Flow E — almost always 📥)
• 📥 [Sender] | [Subject]
  → [Product] — [test type] — [pass/fail]

📋 INVOICES (Flow F — 📥 only, PO-bound only)
• 📥 [Sender] | [Subject]
  → [Vendor] — invoice [number] — PO [number if linked]

📋 VENDOR INVOICES — COST LEDGER (Flow I)
• 📥 [Sender] | [Subject]  ← typically Ramp
  → [Vendor] — invoice [number] — [amount] [currency]
  → cost_category: [regulatory / quality / pd / ops / marketing / general]
  → regulatory_driver: [true / false]
  → linked_sku: [SKU name or "—"]
  → po_link: [PO number or "—"]
  → Multi-home proposal: [purchasing-manager Job 9 → ...]
  → 🔁 Dedup: [clean / duplicate of invoice [n] from [date]]

📋 COMPONENT / BOM UPDATES (Flow G)
• [📥/📤] [Sender or Recipient] | [Subject]
  → [Component] — [what changed] — origin: [vendor quote / Alvin spec]

---

🩺 QUALITY CROSS-FLAGS (route to quality-lab-coordinator / batch-lifecycle-tracker / complaint-and-event-handler / capa-coordinator / adverse-event-and-recall-reporter)
• [📥] [Sender] | [Subject]
  → [signal type — failing test / batch hold / complaint / NCR / SAE]
  → Parent action: [destination skill]
  → PLM cross-ref: [Flow X record link, if any]

📜 REGULATORY CROSS-FLAGS (route to claims-il-and-label-keeper / regulatory-manager)
• [📥] [Sender] | [Subject]
  → [signal type — IL packet / label artwork / attestation / MoCRA / FDA / state filing]
  → Parent action: [destination skill]
  → PLM cross-ref: [if a vendor compliance doc was also logged]

💰 MARGIN CROSS-FLAGS (route to margin-pressure-test / walk-away)
• [📥/📤] [Sender or Recipient] | [Subject]
  → [signal type — cost increase / MOQ change / tariff / allowance / MAP]
  → Parent action: [destination skill]
  → PLM cross-ref: [Flow G component update, if any]

📨 OUTLOOK-ASANA-BRIDGE CROSS-FLAGS (Asana-side actions outlook-asana-bridge should pick up — Intel, Founder, ops sync-back)
• [item] → [destination]

---
Which should I push? (say "all", list numbers, or "skip")
PLM writes commit via plm-assistant. Cross-flags route to their destination skills.
```

---

## Confirmation rules

You own HITL approval. plm-assistant owns the commit and the audit-log entry.

| Operation | Where it runs | Confirmation |
|-----------|---------------|--------------|
| Email search (reads) | Microsoft 365 MCP, here | No confirmation |
| PLM SELECT | Supabase MCP, direct | No confirmation |
| PLM INSERT (new batch, new vendor, new record) | Staged here, committed by plm-assistant | Show preview, confirm with Alvin, hand off |
| PLM UPDATE | Staged here, committed by plm-assistant | Show current → new value, confirm, hand off |
| PLM DELETE | Staged here, committed by plm-assistant | Double-confirm; plm-assistant double-checks FK dependencies on commit |
| Asana sync-back comment | Asana MCP, here | Show draft, confirm, then post |
| Cross-flag to `outlook-asana-bridge` or `asana-plm-bridge` | Note it clearly in output; don't write into other skills' scope |  |

**Never** enter financial account numbers, banking details, SSNs, or other sensitive ID
data into PLM or anywhere else — per the system-wide user-privacy rules. If email content
contains these, acknowledge receipt, skip the sensitive fields, and flag to Alvin to
handle manually.

---

## Attachment handling

Claude cannot upload attachments directly to PLM (Supabase storage) from this context.
For every PLM-bound attachment:

1. Note the file name, sender, and date in the PLM record's notes field
2. Flag clearly in the output: `📎 Attach manually to PLM: [filename] (from [Sender], [date])`
3. If the same attachment is also Asana-bound (Flow D approval docs, Flow E test results
   needing team visibility), list it in both sync-back locations

---

## Connection points — how this skill fits the system

This bridge writes to PLM via `plm-assistant` (sole writer) and posts cross-system signal into the Asana queues defined by the queue contract. It does not call destination skills directly. Canonical map: `references/architecture/bridge_queue_contract.md`.

- **Peer to `outlook-asana-bridge`:** Same inbox, different targets. Records and artifacts route here; tasks and decisions route to `outlook-asana-bridge`. Hybrid content splits with cross-flags on both sides.
- **Complements `asana-plm-bridge`:** That bridge syncs Asana-known data into PLM. This bridge captures PLM-bound data before it ever lands in Asana — reducing noise in PD task comments.
- **PD sync-back:** Every successful PLM write posts a `📦 PLM Sync` comment on the related Asana PD task (Flow H), keeping the circular loop intact.
- **Quality queue:** Failing test results (Flow E failures), batch holds, near-expiry signals, NCR / non-conformance language, and complaint references land in SJS Quality Management (plus CAPA Log or Complaint Log if subtype is clear). PLM update becomes the cross-reference; Quality is the parent.
- **Regulatory queue:** Pedrero artifacts (IL packets, label artwork, attestation responses) land in SJS Regulatory Management — not buried as generic "compliance docs" on the vendor record. SAE / FDA / state-filing signals land in SJS Reportable Events.
- **Margin / Intel / Founder (no queue):** These are direct-output skills with no Asana queue. The bridge does not call them — it lands the underlying data where they read it live. Margin cost/MOQ/tariff/allowance/MAP pressure lands in PLM via Flow G (margin skills read PLM live); intel/founder signal is surfaced to the operator and upstream rollups via an `outlook-asana-bridge` cross-flag. Destination-skill names elsewhere in this file (margin-pressure-test, walk-away, sjs-comp-intel, sjs-retail-intel, ayesha-weekly-briefing, etc.) mark routing intent, not a direct call. Per `references/architecture/bridge_queue_contract.md`.
- **Ramp invoices (Flow I) → Purchasing queue:** Every Flow I invoice hands off to `purchasing-manager` Job 9 via the AC Brands Purchasing queue for HITL classification, multi-home routing, and optional dispute trigger. `plm-assistant` commits the `vendor_invoices` row only after that HITL gate clears. Downstream rollups (`regulatory-manager` Jobs 8 + 9 and `regulatory-status-reporter` spend strip) read from committed rows.
- **Status reporter:** Material BOM cost changes (Flow G) or failing test results (Flow E) affecting launch readiness flag into `sjs-status-reporter` aggregation via the SJS Quality Management / SJS Regulatory Management queues.

---

## Example interactions

> "Scan my inbox for PLM-bound emails this week"
→ Run `outlook_email_search` with supplier domain filters + last 7 days, classify each
  into Flows A–G, present PLM Triage Report, hand confirmed items to plm-assistant.

> "The KDC-One PO ack just came in — update PO #100336 in PLM"
→ Find the email, extract status + ship date, propose UPDATE on `purchase_orders` with
  current → new preview (Flow A), post sync-back to Sorrel / Guava / etc. Asana task.

> "File the Castaway Cream stability results — the email from Allure Labs this morning"
→ Find the email, extract test type + result + filename, propose UPDATE on products
  (Flow E), flag PDF for manual PLM attachment, cross-flag `outlook-asana-bridge` if failure.

> "The batch COA for Jamaican Cherry is in — log it"
→ Find the email, extract batch code + production date + shelf life, propose INSERT into
  `batches` (Flow B), flag COA PDF for manual upload, sync-back to the lip treatment task.

> "Element Packaging has a new contact — add her to PLM"
→ Find the intro email, check for vendor duplicate, propose INSERT on `vendors` or UPDATE
  on existing Element record (Flow C), confirm.

> "Anything from Vegelabs this week that should be in PLM?"
→ Search `outlook_email_search` with domain filter = vegelabs.com + last 7 days (Inbox
  + Sent), classify each email, present triage.

> "Log the PO I just sent to Element"
→ Find the outbound PO email in Sent Items, extract PO number, line items, vendor,
  requested ship date, attachment filename → propose INSERT into `purchase_orders`
  (Flow A — outbound), flag the PO PDF for manual upload, sync-back to the related
  Asana task.

> "File the formula approval I sent KDC-One on Sorrel"
→ Find Alvin's outbound approval email, propose UPDATE on the Sorrel product record
  with Alvin as approver and the sent date as the decision date (Flow D — outbound),
  flag the approval doc for manual PLM attachment, cross-flag to `outlook-asana-bridge`
  for the Formula Tracker stage move.

> "Save the spec sheet I sent to Element for the Castaway jar"
→ Find the outbound spec email, extract component name + cost target + MOQ + spec
  filename, propose UPDATE on the component record with the new spec values and an
  "outbound from Alvin" note (Flow G — outbound), cross-flag to margin-pressure-test
  if the cost target shifted materially.

> "What POs did I send out this month? Are they all logged in PLM?"
→ Search Sent Items for "PO" subject pattern + AC Brands → vendor domains in the past
  30 days, cross-reference each against `SELECT po_number FROM purchase_orders` to
  identify gaps, propose INSERTs for any missing ones.

> "Allure Labs sent a failing PET on Castaway Cream — log it"
→ Find the inbound email, run Flow E (UPDATE product test fields with fail status),
  AND open quality-lab-coordinator as the **parent action** with the PLM update as
  the cross-reference. URGENT flag, `outlook-asana-bridge` cross-flag for the PD task.

> "Pedrero sent the Pava Toner IL packet — file it"
→ Detect sender = `pedreroregulatory.com`, route to claims-il-and-label-keeper as
  the parent action (NOT logged as a generic compliance doc on the vendor record).
  Cross-flag regulatory-manager. If the email also includes a vendor compliance
  artifact, run Flow C alongside.

> "Vegelabs hit me with a 9% cost increase on Pineapple Punch components"
→ Run Flow G (UPDATE component spec fields with new cost) AND open
  margin-pressure-test as the parent action for the affected SKUs. Cross-flag
  walk-away if any SKU is already at the floor. Cross-flag `outlook-asana-bridge`
  for vendor record updates and the PD task.

> "Ulta sent the new attestation form — file it"
→ Route to claims-il-and-label-keeper for the retailer attestation queue (NOT
  buried as a vendor compliance doc). Cross-flag regulatory-manager.

> "Ramp just notified me of a Pedrero invoice — log it"
→ Detect Ramp sender + Pedrero vendor in body, run Flow I (stage
  `vendor_invoices` INSERT with cost_category=regulatory, regulatory_driver=true),
  cross-flag purchasing-manager Job 9 with multi-home proposal
  (Vendor Invoices + SJS Regulatory Management), wait for HITL approval,
  then plm-assistant commits and Flow H posts the sync-back.

> "Scan Ramp for last month's invoices and load them into PLM"
→ Search Sent + Inbox for sender = ramp.com domains + last 30 days, classify
  each into Flow I, dedup against `vendor_invoices` on (vendor_id, invoice_number),
  surface the batch in PLM Triage Report under VENDOR INVOICES, wait for "all" or
  per-item confirmation, hand each through purchasing-manager Job 9.

> "Eurofins invoice for the PET on Castaway Cream — file it"
→ Run Flow I with cost_category=quality, regulatory_driver=true (PET is the canonical
  case), linked_sku_id=Castaway Cream. Multi-home proposal: Vendor Invoices + SJS
  Quality Management + SJS Regulatory Management (regulatory_driver override always
  adds Regulatory).

> "AMR Labs invoice for the Pava Toner benchtop iterations — file it"
→ Run Flow I with cost_category=pd, linked_sku_id=Pava Toner. Multi-home proposal:
  Vendor Invoices + the Pava Toner PD project + position as subtask under the master
  Pava Toner Asana task. Operator confirms the master task at HITL.

---

## What this skill does NOT do

- Does not create Asana tasks. That's `outlook-asana-bridge`'s job — cross-flag to it instead.
- Does not move Formula Tracker stage-gate tasks. That's `asana-pd-manager`'s job — cross-flag to it.
- Does not generate status outputs or decks. That's `sjs-status-reporter`'s job.
- Does not handle meeting transcript content. That's `fireflies-asana-bridge`'s job.
- Does not write into Quality, Regulatory, or Margin skill data stores directly.
  Cross-flag with the proposed action; the destination skill picks it up via its own
  intake. This skill only owns PLM writes (via plm-assistant) and Asana sync-back
  comments.
- Does not upload files directly to Supabase storage — always flag attachments for manual
  upload after the record is created.

## Job 0 — Wiki update (runs after confirmed Asana/PLM writes)

After every confirmed PLM write in the session, write an artifact-focused entry to the wiki layer in Supabase (`public.wiki_pages`, project `ujkabbffvhpewpbttmmy`). No additional user confirmation — the PLM write already gated it. This is the **artifact** layer — the append-only document/record trail — and it pairs with the **narrative** layer the Asana bridges (`fireflies-asana-bridge`, `outlook-asana-bridge`) write. `asana-plm-bridge` writes the same artifact ledger from the Asana-side sync; this bridge writes it from email-sourced PLM writes (`last_source = 'plm/outlook'`). Both layers fire on the same supplier/SKU pages and don't overwrite each other.

### Trigger
Fires once at end of session, after the user has confirmed all PLM record creations (batches, COAs, stability results, vendor docs) for the emails processed.

### Inputs
Every PLM record created or updated in the session, mapped back to the wiki page for the related supplier or SKU:
- Supplier wiki pages get artifact entries for vendor-side docs (signed agreements, COAs, deviation reports).
- SKU wiki pages get artifact entries for product-side docs (batch COA, stability checkpoint, micro pass/fail).

### Per-entity loop
1. `SELECT slug, content FROM public.wiki_lookup(p_slug => <slug>)` to read the current page.
2. Synthesize an artifact-focused entry — short, factual, ledger-style. Examples:
   - `COA for batch SJS-LIP-0426 received 2026-05-21, filed to PLM batch record [batch_id].`
   - `Stability checkpoint T+3mo for [SKU] received 2026-05-18: pass. Filed to PLM stability record [stability_id].`
   - `Signed quality agreement v2.1 received 2026-04-30 from KDC/One, filed to PLM vendor record [vendor_id].`
3. Append to the page's artifact ledger section (create the section if it does not exist). Older entries stay — this is the document trail, not the narrative summary. Do not rewrite or compress prior entries.
4. Write:
   ```sql
   UPDATE public.wiki_pages
     SET content = $new_content,
         source_count = source_count + 1,
         last_source = 'plm/outlook',
         last_source_ref = $message_id
     WHERE slug = $slug;
   ```
No manual audit log write needed — the `audit_wiki_pages` trigger on `wiki_pages` fires automatically on INSERT/UPDATE/DELETE and writes a full before/after diff to `public.audit_logs` with `entity_type = 'wiki_pages'`.

### Slug construction

Always derive the slug via `public.wiki_slugify(text)` — never hand-roll a regex. The function does: lowercase, replace `[^a-z0-9]+` with single dash, trim leading/trailing dashes. Source string depends on `page_type`:

| page_type | Source | Slug expression |
|---|---|---|
| `supplier` | `vendors.name` | `'supplier/' \|\| public.wiki_slugify(v.name)` |
| `sku` | `coalesce(products.sku, products.name)` | `'sku/' \|\| public.wiki_slugify(coalesce(p.sku, p.name))` |
| `sop` | `sop_documents.sop_id` | `'sop/' \|\| public.wiki_slugify(s.sop_id)` |

Resolve the slug **before** the lookup — same function on the read path and the write path. The PLM bridge only writes to supplier and sku pages; don't create new wiki pages from this bridge — that's the Asana bridges' job. `partner` pages (read during entity discovery, 15 live) slugify as `'partner/' || public.wiki_slugify(title)`; the Asana bridges own their creation.

### Out of scope here
No narrative synthesis — that belongs to the Asana bridges. No file uploads to Supabase storage. No embedding generation.
