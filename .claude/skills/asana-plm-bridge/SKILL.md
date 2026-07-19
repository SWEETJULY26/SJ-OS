---
name: asana-plm-bridge
description: >
  Bidirectional sync between Asana PD projects and Sweet July Skin's PLM system. Use
  whenever Alvin wants to push Asana data into PLM or surface PLM data back into
  Asana — "log this formula approval to PLM", "the Sorrel lip treatment was approved
  — update the PLM record", "push this batch info from Asana to PLM", "add this
  vendor to PLM", "what's the PLM status on the Castaway Cream", "surface the PLM
  formula data back into the Asana task", "sync Asana and PLM for the Pava Toner".
  Also triggers when sibling PD skills flag a ⚙️ PLM Bridge item. plm-assistant is
  the sole PLM writer; this bridge stages and confirms. While syncing, extracts
  cross-system signal and posts to the right Asana queue per
  sjs-master/bridge_queue_contract.md — Quality (failing tests, batch holds,
  near-expiry, complaints) and Regulatory (Pedrero artifacts, attestation responses,
  expiring compliance docs). PLM → Asana surface-back includes Quality and Regulatory
  flags, not just stock and phase. Sibling of asana-pd-manager in the PD system.
---

# Asana ↔ PLM Bridge

**Version:** v1.0 · **Last updated:** 2026-05-31 16:54 PT — P2P Phase 5: added **Flow 5** (purchasing Asana state → `supplier/<slug>` wiki ledger; five triggers — 2C gate, 2D vendor commit, 3E receipt close, 6C discrepancy resolve, 4B renewal close). Ledger-style entries consistent with Job 0, `last_source = 'plm/asana'` (reconciled from the plan's `asana-plm-bridge` default to avoid source-tag drift), `last_source_ref` = purchasing task GID. Documented carve-out: Flow 5 trigger 2 may create a supplier page for an email-less purchasing-only vendor. Prior — P4/P5 bridge audit remediation: added artifact-ledger Job 0 (wiki write-back); version marker added. P1 (2026-05-26): run-time entity discovery replaced the hard-coded product-name mapping.

You are the data routing layer between Asana projects and Sweet July Skin's PLM system for AC Brands operations.
Your job is to move the right data in both directions — from Asana into PLM records, and from
PLM back into Asana tasks — always confirming before writing to either system.

---

## How you connect

- **Asana MCP:** `https://mcp.asana.com/sse` — read task data, comments, and attachments;
  post sync-back comments after a PLM write lands
- **Supabase MCP:** `https://mcp.supabase.com/mcp` — **SELECTs only** against the PLM
  database using `project_id: ujkabbffvhpewpbttmmy`. Use SELECT to look up product IDs,
  check for duplicates, and pull current values for UPDATE previews.
- **plm-assistant** — the only path for PLM writes. INSERT, UPDATE, and DELETE all route
  through plm-assistant. You stage the write (build the proposed SQL, get Alvin's
  confirmation, format the preview); plm-assistant validates against schema, commits, and
  returns the audit-log entry.

You never call `execute_sql` for INSERT / UPDATE / DELETE directly. If you find yourself
about to, stop — that's a build-pattern violation. Hand off to plm-assistant.

---

## Run-time entity discovery (vendors, partners, contacts, products)

Before any flow runs, load the recognition lexicon from Supabase. No entity is hard-coded in this SKILL.md — vendors, partners, contacts, and products all come from the live data layer so new entities are recognized the moment they land.

```sql
-- Material / component vendors (PLM-tracked)
SELECT id, name, lower(name) AS lname FROM public.vendors;

-- Service contractors, labs, 3PLs, tooling — non-PLM counterparties
SELECT slug, title, content FROM public.wiki_pages WHERE page_type = 'partner';

-- People — internal + external (replaces sjs-master/senders.md)
SELECT slug, title, content FROM public.wiki_pages WHERE page_type = 'contact';

-- Products (replaces the old hard-coded Asana→PLM name mapping)
SELECT id, sku, name FROM public.products;
```

Use the combined name set when matching Asana task titles, comments, and mentions. When the bridge encounters a name not in any of these queries, treat it as a new entity and surface to Alvin for capture rather than silently dropping it.

---

## The five data flows

### Flow 1: Formula approval → PLM
**Trigger:** A task in the Formula Development Tracker moves to Signed Approvals,
or Skills 2/3 flag a formula approval.

What to do:
1. Read the Asana task for: product name, formula number, revision number, supplier,
   approval date, any approval document noted
2. Find the matching product in PLM (direct SELECT):
   `SELECT id, name, sku FROM products WHERE name ILIKE '%[product]%'`
3. Stage the approval write — phase update on the product record, plus an approval note;
   if a new batch is implied, prompt Alvin to log it as a separate Flow 3
4. Show Alvin the preview, get confirmation, then hand the staged write to plm-assistant
   to commit

```
⚙️ PLM Sync — Formula Approval
Asana task: [task name]
Formula #: [number] | Revision: [#] | Supplier: [name]
Approved: [date]

→ PLM action: Update [product name] phase to [phase] + log approval note
Proceed?
```

### Flow 2: Supplier / vendor info → PLM
**Trigger:** A new supplier is mentioned in Asana tasks or comments, or an existing
supplier's contact info or status changes.

What to do:
1. Check if vendor already exists (direct SELECT):
   `SELECT id, name FROM vendors WHERE name ILIKE '%[supplier]%'`
2. If new → stage an INSERT on `vendors` with name, vendor_type, contact info if available
3. If existing → stage an UPDATE with changed fields only
4. Stage a `product_vendors` link if the relationship isn't already recorded (SELECT first
   to avoid duplicates)
5. Show Alvin the preview, get confirmation, then hand off to plm-assistant to commit

### Flow 3: Batch / production data → PLM
**Trigger:** A task comment or attachment in Asana contains batch codes, production
dates, quantities, or COA references.

What to do:
1. Extract: product name, batch code, production date, quantity, shelf life if mentioned
2. Find the product_id in PLM (direct SELECT)
3. Check if batch already exists (direct SELECT):
   `SELECT id FROM batches WHERE batch_code = '[code]'`
4. If new → stage an INSERT on `batches` (production date + shelf life only —
   expiration and pull date are computed by trigger inside plm-assistant's commit)
5. Show Alvin the preview, get confirmation, hand off to plm-assistant; it commits and
   returns the created record for sync-back to Asana

```
⚙️ PLM Sync — New Batch
Product: [name] | Batch code: [code]
Production date: [date] | Shelf life: [X months]
Source: Asana task "[task name]"

→ PLM will compute: Expiration date + Pull date automatically
Proceed?
```

### Flow 4: PLM → Asana (surface back)
**Trigger:** Alvin asks "what's the PLM status on [product]" while in an Asana context,
or a PLM update is relevant to an active Asana task.

What to do:
1. Query PLM directly via SELECT for: current_phase, product_status, quantity_on_hand,
   active batches, linked vendors
2. Format as a concise summary and propose adding it as a comment to the relevant
   Asana task — so the info lives in both places
3. Flag if anything in PLM is concerning (expired batch, low stock, vendor issue)

This flow has no PLM writes — reads go direct, the only write is the Asana comment.

```
📦 PLM Status — [Product name]
Phase: [current_phase] | Status: [product_status]
Stock: [quantity_on_hand] units
Active batches: [N] | Nearest pull date: [date]
Vendor: [supplier name]

🩺 Quality flags: [batch holds, near expiry, failing tests, open complaints — or "none"]
📜 Regulatory flags: [expiring compliance docs, open IL/label reviews, attestation gaps]
💰 Margin flags: [components flagged for margin review, SKUs near floor]
⚙️ Operational flags: [stock below reorder, late vendors, missing COAs]

→ Post this as a comment on Asana task "[task name]"?
→ Open downstream actions for any fired flags?
```

### Flow 5: Purchasing Asana state → supplier wiki ledger

**Trigger:** A lifecycle state change in the **AC Brands Purchasing** project (GID `1214373717266702`), fired by `purchasing-manager`. Five events, all writing to `supplier/<vendor_slug>`:

| # | Source event (purchasing-manager job) | Ledger line to append |
|---|---|---|
| 1 | 2C onboarding gate fires (NDA + W9 both checked; task moves Vendor Onboarding → Compliance, Renewals & Disputes) | `Onboarding doc gate cleared YYYY-MM-DD. NDA + W9 received.` |
| 2 | 2D vendor commit (PLM `vendors` row created) | `PLM vendor record created YYYY-MM-DD. Category: {vendor_type}. Filed to vendor record {vendor_id}.` |
| 3 | 3E receipt task closes (Status = Received) | `Receipt closed YYYY-MM-DD on PO {po_number}. Logiwa ref {ref}. Units received: {qty}.` |
| 4 | 6C resolution set on a discrepancy task | `Discrepancy on PO {po_number} resolved YYYY-MM-DD. Type: {type}. Resolution: {resolution}.` |
| 5 | 4B renewal task closes | `Renewal {60d/30d/15d} closed YYYY-MM-DD. Outcome: {renewed / renegotiated / churned}.` |

What to do:

1. Resolve the slug: `'supplier/' || public.wiki_slugify(vendor_name)` — same function on read and write (see Slug construction under Job 0).
2. `SELECT slug, content FROM public.wiki_lookup(p_slug => <slug>)`.
3. Append the ledger line to the page's artifact-ledger section (these are factual ledger entries, not narrative — narrative stays with the Outlook/Fireflies bridges). Older entries stay; never rewrite or compress.
4. Write via the Job 0 `UPDATE` mechanics: bump `source_count`, set `last_source = 'plm/asana'`, `last_source_ref = <purchasing_task_gid>`. No manual audit row — the `audit_wiki_pages` trigger fires automatically.

**Page existence.** Triggers 1, 3, 4, 5 write back to an existing supplier page or skip if none exists (the page lands once an Outlook/Fireflies bridge runs against the vendor). **Trigger 2 is the one documented exception to the no-create rule:** a vendor onboarded purely through purchasing may have no prior email/meeting trail, so if `wiki_lookup` returns nothing at the 2D vendor commit, create the `supplier/<slug>` page with this ledger line as its first entry. In practice onboarding docs arrive through `outlook-plm-bridge`, which usually creates the page first; trigger 2's create-if-missing is the fallback for the email-less case only.

**No HITL.** Each event is already gated by the confirmed purchasing-manager action that fired it. This flow has no separate confirmation — same as Job 0.

**Source-tag note.** The P2P build plan's Phase 5 default named `last_source = 'asana-plm-bridge'`; reconciled in-place to `'plm/asana'` to match this skill's existing Job 0 / audit convention and avoid source-tag drift. `last_source_ref` (the purchasing task GID) is what distinguishes a purchasing-driven write from a PD-driven one.

---

## Handling ⚙️ PLM Bridge flags

When `asana-pd-manager`, `fireflies-asana-bridge`, `outlook-asana-bridge`, or
`outlook-plm-bridge` tag an item with `⚙️ PLM Bridge:`, treat it as an incoming routing
request. Read the flag, identify which Flow (1–4) applies, and execute that flow's
steps. If the flag is ambiguous, ask Alvin which flow to apply.

---

## Cross-system signal extraction

While reading Asana for sync (Flows 1–3) or pulling PLM data back (Flow 4), also scan
for non-PLM signal and cross-flag the right destination skill. Same label model as the
Outlook and Fireflies bridges. Multi-system items split + cross-reference (priority:
`quality` > `regulatory` > `ops` > `pd` > `margin` > `intel` > `founder`).

### Asana → PLM direction (Flows 1–3) — what to look for in source task/comments

| Signal in Asana task or comment | Routes to |
|---------------------------------|-----------|
| Failing test result, OOS/OOT, RIPT positive, PET fail, stability fail | quality-lab-coordinator |
| Batch hold, near expiry, recall trigger | batch-lifecycle-tracker; adverse-event-and-recall-reporter if recall |
| Customer complaint or adverse event mention | complaint-and-event-handler |
| NCR / non-conformance language | capa-coordinator |
| Pedrero artifact, IL packet, label artwork, retailer attestation form | claims-il-and-label-keeper; cross-flag regulatory-manager |
| MoCRA / FDA / state filing reference | regulatory-manager |
| Cost shift, MOQ change, tariff, allowance ask, MAP enforcement | margin-pressure-test; walk-away if SKU at floor |
| Competitor / press / retail-data mention | sjs-comp-intel or sjs-retail-intel via `outlook-asana-bridge` |
| Anything from Ayesha or material to founder briefing | ayesha-weekly-briefing via `outlook-asana-bridge` |

The PLM write still happens here. The non-PLM action happens at the destination skill.
Both records cross-reference each other.

### PLM → Asana direction (Flow 4) — what to surface back

When pulling PLM data, the Asana sync-back comment includes more than stock and phase:

- **Quality flags:** active batch holds, near-expiry batches (pull date inside 30 days),
  failing test results on file, open complaints linked to the SKU
- **Regulatory flags:** expiring compliance docs (vendor or product), open IL or label
  reviews, retailer attestation gaps
- **Margin flags:** components flagged for margin review (recent cost shift, MOQ change,
  tariff change), SKUs at or near floor
- **Operational flags:** stock below reorder point, late vendor deliveries, missing
  COAs on recent batches

Format these as a flagged section under the PLM status summary. If any flag fires,
also propose opening or updating the matching action in the relevant sub-system skill
(e.g., a near-expiry batch surfaces back as both an Asana comment AND a
batch-lifecycle-tracker action).

---

## Product lookup

Use the universal `products` SELECT loaded in "Run-time entity discovery" to resolve any product name. PLM is the source of truth — there is no hand-coded mapping in this file. New SKUs land in `products` and auto-resolve from the next session forward.

Match strategy:

1. Lower-case the Asana project / task name and the candidate `products.name`.
2. Prefer exact substring matches on `products.name`. Fall back to fuzzy matches that pair the common name with the SKU.
3. If a single product matches, proceed.
4. **If multiple products match** (e.g., "Pineapple Punch" hits the mask, the 5-pack, and the lip treatment; "Coffee Fix" hits the lip and the eye cream; "Pava Toner" hits the toner and the toner spray), surface the options to Alvin and ask which one. Never pick silently.
5. If zero products match, ask whether the SKU exists yet or needs a vendor-driven INSERT (Flow 2).

---

## Confirmation rules

You own HITL approval. plm-assistant owns the commit and the audit-log entry.

- **Asana reads:** No confirmation needed
- **PLM SELECTs (direct via Supabase MCP):** No confirmation needed
- **PLM INSERTs (new batch, new vendor):** Stage the write, show preview, confirm with
  Alvin, hand to plm-assistant to commit
- **PLM UPDATEs:** Stage the write, show current → new value, confirm, hand to
  plm-assistant to commit
- **PLM DELETEs:** Same as UPDATEs but with a stronger warning; plm-assistant double-checks
  for FK dependencies on its end as well
- **Asana comments (surfacing PLM data back):** Confirm before posting; you write Asana
  directly

---

## Connection points

This bridge stages PLM writes (sole writer is `plm-assistant`) and posts sync-back comments to Asana PD tasks. Cross-system signal it extracts while syncing follows the queue contract — it posts to the target system's Asana queue rather than calling destination skills directly. Canonical map: `sjs-master/bridge_queue_contract.md`.

- **PLM writes:** All four Flows stage SQL through `plm-assistant`. Reads (SELECT) run direct against Supabase. The bridge never calls `execute_sql` for INSERT / UPDATE / DELETE.
- **Inbound from Asana:** Formula Tracker stage moves to Signed Approvals trigger Flow 1; email-sourced approval / batch / supplier signal flagged by the two Outlook bridges and meeting-sourced signal flagged by `fireflies-asana-bridge` trigger Flows 1–3.
- **PD sync-back:** Flow 4 posts PLM status summaries (phase, stock, batches, vendors, plus Quality / Regulatory / Margin flags) back to the originating Asana PD task as a comment.
- **Cross-system signal extracted during sync:** Quality flags → Quality queue (SJS Quality Management). Regulatory flags → Regulatory queue (SJS Regulatory Management). Margin flags → PLM (margin skills read PLM live; no Asana queue for them). Ops, Intel, Founder follow the same queue contract.
- **PLM Bridge flags from siblings:** When a sibling PD skill flags ⚙️ PLM Bridge on a task, that's this bridge's pickup signal.
- **Purchasing-surface ledger (Flow 5):** `purchasing-manager` lifecycle state changes in the AC Brands Purchasing project — onboarding gate cleared (2C), vendor record created (2D), receipt closed (3E), discrepancy resolved (6C/Job 10), renewal closed (4B) — fire Flow 5 to write a ledger line to the `supplier/<slug>` wiki page. `purchasing-manager` never writes the wiki directly; all purchasing-driven wiki writes land here.
- **Margin / Intel / Founder (no queue):** These are direct-output skills with no Asana queue. The bridge does not call them — it lands the underlying data where they read it live (margin cost/MOQ → PLM; intel/founder signal → surfaced to the operator and upstream rollups). Destination-skill names elsewhere in this file (margin-pressure-test, walk-away, sjs-comp-intel, ayesha-weekly-briefing, etc.) mark routing intent, not a direct call. Per `sjs-master/bridge_queue_contract.md`.

---

## Example interactions

> "The Sorrel lip treatment formula was approved — sync it to PLM"
→ Read Asana task, SELECT the PLM product, stage the phase update + approval note,
  confirm, hand to plm-assistant to commit (Flow 1).

> "Log the new KDC-One batch info from the Jamaican Cherry task to PLM"
→ Extract batch data from Asana task comments, SELECT for product_id, stage the batch
  INSERT, confirm, hand to plm-assistant (Flow 3).

> "What's the PLM status on the Castaway Cream — post it to the Asana task"
→ SELECT directly, format summary, propose posting as comment on Asana task (Flow 4 —
  no PLM write, reads go direct).

> "We're working with a new lab — add them to PLM as a vendor"
→ SELECT to check for duplicates, stage the vendor INSERT with available info, confirm,
  hand to plm-assistant (Flow 2).

> "Sync the Castaway Cream batch from the Asana task to PLM — also there's a hold note
  in the comments"
→ Run Flow 3 (batch INSERT) AND open batch-lifecycle-tracker for the hold; cross-flag
  quality-lab-coordinator if the hold note references a failing test. Both records
  cross-reference each other.

> "What's the PLM status on the Pava Toner — and post it"
→ SELECT product, stock, batches, vendor — but also pull failing tests, near-expiry
  batches, expiring compliance docs, components flagged for margin review. Surface
  all of those in the sync-back comment (Flow 4 — extended). Propose downstream
  actions for any fired flags.

> "Push the Vegelabs cost update from the Pineapple Punch task to PLM"
→ Run Flow 2 (vendor/component update) AND cross-flag margin-pressure-test for the
  affected SKU. Cross-flag walk-away if the SKU is already at the floor.

---

## Wiki context (runs before live queries)

Before syncing Asana task state to PLM, read the relevant SKU and supplier pages from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as sibling bridge skills process emails and meetings. Reading them first gives this skill phase history and formula context that makes the sync decision cleaner — what's changing now sits in the arc of what's already happened.

### Which pages to read

- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`
- Named supplier → `'supplier/' || public.wiki_slugify(vendor_name)`

SKU pages carry phase history, formula context, and prior PLM writes. Supplier pages carry the document trail and open quality/regulatory flags.

### Read query

```sql
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'sku/' || public.wiki_slugify('{sku_code_or_product_name}'));

SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live PLM lookups. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to outlook-/fireflies- bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before deciding the Asana↔PLM sync. The PLM write still goes through `plm-assistant`; the wiki page just makes sure the write reflects the full arc.

### Write-back happens in Job 0, not here

This section is **read-only** — it loads wiki context before the sync decision. The wiki *write* lives in **Job 0** (below), which appends an artifact-ledger entry after a confirmed PLM commit. As a PLM bridge, this skill writes **artifacts** (the document/record trail), not narrative — narrative synthesis belongs to the Asana bridges (`fireflies-asana-bridge`, `outlook-asana-bridge`). Both layers fire on the same pages; they don't overwrite each other.

### What this skill does NOT do (read layer)

- Does not create new wiki pages — Job 0 only appends to existing supplier/SKU pages; page creation belongs to the Asana bridges. **One exception:** Flow 5 trigger 2 (purchasing 2D vendor commit) may create a `supplier/<slug>` page if a purchasing-onboarded vendor has no prior email/meeting trail. No other trigger creates pages.
- Does not write narrative synthesis to the wiki — that's the Asana bridges' layer
- Does not replace live Asana or PLM queries for current task and PLM state

---

## Job 0 — Wiki update (artifact ledger; runs after confirmed PLM writes)

After every confirmed PLM write in the session, append an artifact-focused entry to the wiki layer in Supabase (`public.wiki_pages`, project `ujkabbffvhpewpbttmmy`). No additional user confirmation — the PLM write already gated it. (Job 0 covers PD-side PLM writes from Flows 1–3. Purchasing-surface lifecycle events — onboarding gate, vendor commit, receipt close, discrepancy resolve, renewal close — are written by **Flow 5** using the same `UPDATE` mechanics and the same `last_source = 'plm/asana'` tag.) This is the traceability layer that pairs with the narrative layer the Asana bridges write, and it matches the artifact-ledger pattern in `outlook-plm-bridge`. The difference is only the source: this bridge's records originate from Asana-side sync, so `last_source = 'plm/asana'`.

### Trigger
Fires once at end of session, after Alvin has confirmed all PLM record writes (formula-approval phase updates, vendor INSERT/UPDATEs, batch INSERTs) staged by Flows 1–3 and committed by `plm-assistant`. Flow 4 is read-only (no PLM write) and does not trigger Job 0.

### Inputs
Every PLM record created or updated in the session, mapped back to the wiki page for the related supplier or SKU:
- Supplier wiki pages get artifact entries for vendor-side records (new vendor record, product_vendors link, contact/status change).
- SKU wiki pages get artifact entries for product-side records (formula-approval phase move, new batch, COA reference).

### Per-entity loop
1. `SELECT slug, content FROM public.wiki_lookup(p_slug => <slug>)` to read the current page.
2. Synthesize an artifact-focused entry — short, factual, ledger-style. Examples:
   - `Formula approval logged 2026-05-26 for [SKU]: phase → Signed Approvals, rev [n], approver [name]. Filed to PLM product record [product_id].`
   - `New batch SJS-LIP-0526 logged 2026-05-26 from Asana task [task_gid], production date 2026-05-20. Filed to PLM batch record [batch_id].`
   - `Vendor record updated 2026-05-26 for [vendor]: [field] changed. Filed to PLM vendor record [vendor_id].`
3. Append to the page's artifact ledger section (create the section if it does not exist). Older entries stay — this is the document trail, not the narrative summary. Do not rewrite or compress prior entries.
4. Write:
   ```sql
   UPDATE public.wiki_pages
     SET content = $new_content,
         source_count = source_count + 1,
         last_source = 'plm/asana',
         last_source_ref = $asana_task_gid_or_plm_record_id
     WHERE slug = $slug;
   ```
No manual audit log write needed — the `audit_wiki_pages` trigger on `wiki_pages` fires automatically on INSERT/UPDATE/DELETE and writes a full before/after diff to `public.audit_logs` with `entity_type = 'wiki_pages'`.

### Slug construction

Always derive the slug via `public.wiki_slugify(text)` — never hand-roll a regex. The function does: lowercase, replace `[^a-z0-9]+` with single dash, trim leading/trailing dashes. Source string depends on `page_type`:

| page_type | Source | Slug expression |
|---|---|---|
| `supplier` | `vendors.name` | `'supplier/' \|\| public.wiki_slugify(v.name)` |
| `sku` | `coalesce(products.sku, products.name)` | `'sku/' \|\| public.wiki_slugify(coalesce(p.sku, p.name))` |

Resolve the slug **before** the lookup — same function on the read path and the write path. This bridge only writes to supplier and sku pages; don't create new wiki pages from here — that's the Asana bridges' job. If `wiki_lookup` returns nothing, skip the artifact write for that entity (the page will exist after an Asana bridge runs). The sole carve-out is Flow 5 trigger 2 (purchasing 2D vendor commit), which may create the `supplier/<slug>` page for an email-less, purchasing-only vendor.

### Out of scope here
No narrative synthesis — that belongs to the Asana bridges. No file uploads to Supabase storage. No embedding generation (the `wiki-embed-backfill` cron handles it).
