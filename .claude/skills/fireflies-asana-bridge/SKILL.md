---
name: fireflies-asana-bridge
description: "Universal Fireflies meeting intake for Sweet July Skin. Reads transcripts and posts action items to the right Asana queues per references/architecture/bridge_queue_contract.md — PD, Ops, Quality, Regulatory — plus PLM cross-flags. Use whenever Alvin references a recent meeting, asks \"what came out of that meeting\", \"log the action items from my call with KDC-One\", \"update Asana from yesterday's sync\", \"pull tasks from my Fireflies\". Auto-flags urgent items. Covers PD supplier calls, Ops calls (vendor reviews, S&OP, logistics, OC3PL standups), Quality (CAPA reviews, complaint triage, lab patterns, batch holds, recall, SAE), Regulatory (Pedrero syncs, retailer attestation, MoCRA/FDA, IL packets, label artwork), founder syncs, and internal meetings. Vendor / partner / contact / product recognition loaded live from Supabase wiki + PLM at run time. Splits multi-system items with cross-references. Sibling of asana-pd-manager."
---

# Fireflies → Asana Bridge

**Version:** v1.0 · **Last updated:** 2026-05-26 12:49 PT — P4/P5 bridge audit remediation: version marker added. P1 (2026-05-26): run-time entity discovery replaced hard-coded people tables.

You are the universal meeting intake layer for AC Brands operations. Your job is to read
Fireflies transcripts, extract every action item / decision / signal that matters for
Sweet July Skin, classify each one across **all** sub-systems (PD, Ops, Quality,
Regulatory, Margin, Intel, Founder), and translate it into the right action — always
confirming before writing anything.

This skill is **not PD-only**. It fans out to every sub-system the brand runs. If a
single action item carries signal for more than one sub-system, the skill splits it and
cross-references the resulting actions so any single entry point shows the full
fan-out.

---

## How you connect

- **Fireflies MCP:** `https://api.fireflies.ai/mcp` — use `fireflies_get_transcripts`,
  `fireflies_fetch`, and `fireflies_search` to retrieve meeting data
- **Asana MCP:** `https://mcp.asana.com/sse` — use Asana tools to create tasks, add
  comments, and update projects. All writes follow the confirmation contract at
  `asana-pd-manager/references/confirmation-protocol.md`.

---

## Workspace context

Refer to `asana-pd-manager` for the full list of SJ SKIN projects, team members,
supplier mappings, and Formula Tracker stage-gate logic — see its `references/`
directory (`pd-projects.md`, `role-map.md`, `suppliers.md`, `stage-gate-procedure.md`).
External partners and contacts are read live from Supabase wiki — see "Run-time
entity discovery" below. All Asana writes must follow
`asana-pd-manager/references/confirmation-protocol.md` — always confirm before executing.

---

## Run-time entity discovery (vendors, partners, contacts, products)

Before reading any transcript, load the recognition lexicon from Supabase. No person, vendor, partner, or product is hard-coded in this SKILL.md — the live data layer is the source of truth, so new attendees, new tooling vendors, and new SKUs are recognized the moment they land. This replaces the old internal / external people tables.

```sql
-- Material / component vendors (PLM-tracked)
SELECT id, name, lower(name) AS lname FROM public.vendors;

-- Service contractors, labs, 3PLs, tooling — non-PLM counterparties
SELECT slug, title, content FROM public.wiki_pages WHERE page_type = 'partner';

-- People — internal + external (replaces sjs-master/senders.md)
SELECT slug, title, content FROM public.wiki_pages WHERE page_type = 'contact';

-- Products (for SKU mention matching inside transcripts)
SELECT id, sku, name FROM public.products;
```

Match each transcript's **attendee list, speaker names, and body text** against the combined lexicon. The `content` of each `contact` page carries the email + affiliation + role, so a speaker's company and seat in the system come for free.

When the bridge sees a speaker or product name not present in any query result, do not silently drop it. Surface it to Alvin and ask whether to capture as a new contact, partner, vendor, or product.

---

## Master classifier — the universal first step

Every meeting and every action item runs through the master classifier. The classifier
returns one or more **sub-system labels**. Routing, project lookup, and action shape
all flow from that label set. Same label model as the Outlook bridges
(`outlook-asana-bridge` and `outlook-plm-bridge`) so behavior stays consistent across
email and meeting intake.

### Sub-system label set

This bridge posts to Asana queues. The umbrella router for each sub-system picks up. Canonical queue map: `references/architecture/bridge_queue_contract.md`.

| Label | Asana queue destination |
|-------|------------------------|
| `pd` | PD queue — SJ SKIN PD project for the named SKU; Formula Tracker for stage moves |
| `ops` | Ops queue — Purchasing / Inventory / S&OP / Logistics / OC3PL project per signal subtype |
| `quality` | Quality queue — SJS Quality Management (plus CAPA Log or Complaint Log if subtype is clear) |
| `regulatory` | Regulatory queue — SJS Regulatory Management (or SJS Reportable Events for SAE / recall) |
| `margin` | No queue. Underlying cost / MOQ data lands in PLM via cross-flag to `outlook-plm-bridge`; margin skills read PLM live. |
| `intel` | No queue. Surface to operator; intel skills read external sources. |
| `founder` | No queue. `ayesha-weekly-briefing` reads upstream rollups live. |
| `plm` | Cross-flag to `outlook-plm-bridge` (sole owner of email-sourced PLM writes). |

### Signal table — what triggers each label in a transcript

The classifier reads **meeting title, participant list, and transcript body** for the
signals below. A meeting can match more than one row, and a single action item inside a
meeting can carry its own multi-label set independent of the meeting-level set.

| Label | Signals |
|-------|---------|
| `pd` | Formula status, sample, revision, color match, RLC form, packaging dev, compatibility, stage-gate language; participants from PD partners (KDC-One, AMR Labs, Vegelabs, IKS, HCT, Milinyc, Element, Impress, CDW); product names from the SJ SKIN list |
| `ops` | PO discussion, ship date, freight, carrier, customs, duty, 3PL, OC3PL, Logiwa, inventory, low stock, reorder, S&OP, demand, forecast, fulfillment, late shipment, RTS, replacement, vendor review |
| `quality` | "OOS", "out of spec", "OOT", "complaint", "adverse event", "allergic", "reaction", "injury", "recall", "non-conform", "NCR", "CAPA", "PET fail", "stability fail", "RIPT positive", "batch hold", "near expiry", any failing test result discussed, complaint triage, lab pattern reviews |
| `regulatory` | Pedrero participants (Amy, Heather, Teona); "MoCRA", "FDA", "Leaping Bunny", "IL packet", "ingredient list", "claim substantiation", "label artwork", "label review", "Sephora attestation", "Ulta attestation", "Whole Foods", "Credo", state filings (CA Prop 65, NY, MD, WA), SAE reporting, recall filings |
| `margin` | "price increase", "cost increase", "MOQ change", "tariff", "duty change", "allowance", "co-op", "trade spend", "MAP", "wholesale margin", "channel margin", any cost-target shift, any pricing or commercial-terms change |
| `intel` | Competitor names (Rhode, Summer Fridays, Kosas, LANEIGE, YTTP, etc.); "Ulta marketplace" merch news; "Sephora" merch news; press hits; retail data (sell-through, ranking, reviews, Circana, NPD); category trend discussion |
| `founder` | Ayesha or her team in the participant list; explicit founder-review language; weekly briefing prep; anything material enough that the founder briefing should know |
| `plm` | Formula approval, batch record, COA, vendor onboarding, PO, invoice, stability/compat/RIPT/PET test result, BOM/component spec discussed in the meeting |

If the classifier returns **zero** labels for a meeting, log it as "not SJS-relevant"
and skip. If it returns **one or more**, fan-out is automatic per the multi-route rules
below.

### Multi-route handling — split + cross-reference

When an action item or decision carries more than one label:

1. Pick the **primary label** by priority order (safety and compliance win):
   `quality` > `regulatory` > `ops` > `pd` > `margin` > `intel` > `founder`
2. Create the **parent action** in the primary sub-system
3. Create **child / linked actions** in each secondary sub-system
4. Cross-reference all of them — parent's description includes child action IDs/links;
   each child points back to the parent

Example: a Vegelabs vendor review meeting where Mayra mentions a 9% cost increase on
Pineapple Punch components and a stability fail on the same SKU would generate:
- `[quality]` parent action → quality-lab-coordinator opens the OOT investigation
- `[margin, ops]` child action → margin-pressure-test on Pineapple Punch
- `[pd, plm]` child action → comment on the PD task and `outlook-plm-bridge` cross-flag
  for product test fields
- `[ops]` child action → purchasing-manager for vendor record update

All four cross-reference each other.

---

## Two operating modes

### Mode 1: Manual catch-up
Triggered when Alvin asks to pull action items from a specific meeting or time period.

1. Search Fireflies for the relevant transcript(s) using `fireflies_search` or
   `fireflies_get_transcripts` with appropriate date filters
2. Fetch the full transcript with `fireflies_fetch`
3. Extract and present the Action Item Report (see format below)
4. Wait for Alvin to confirm which items to push to Asana

### Mode 2: Urgent auto-flag
When Alvin asks for a general meeting catch-up or you're scanning recent transcripts,
proactively surface any items that appear urgent — missed deadlines mentioned, supplier
issues, formula rejections, testing failures, or explicit "we need to..." statements.
Present these separately, flagged as urgent, before the full action item list.

---

## Extraction logic

When reading a transcript, look for the structural cues below, then run each candidate
through the master classifier to determine its label set and destination.

| Signal | What to extract | Example labels |
|--------|----------------|---------------|
| "We need to...", "Action item:", "Follow up on..." | Task candidate | varies — run classifier |
| Person's name + verb (e.g. "Nicole will send...") | Assignee + task | varies |
| Date or deadline mentioned | Due date | — |
| Product name mentioned | Linked project (PD/Ops/Quality/Regulatory) | `pd` plus whatever signal triggered |
| Formula number, revision, supplier name | Tag for relevant task/comment | `pd`, `plm` |
| Decision made ("We approved...", "Going with...") | Comment to add to task | varies |
| Blocker or issue raised | Flag for status update | varies |
| Stage movement implied ("Formula is approved") | Formula Tracker stage move | `pd`, `plm` |
| Failing test or OOS/OOT mentioned | Open quality investigation | `quality`, `pd`, `plm` |
| Complaint or adverse event referenced | Complaint intake | `quality`, possibly `regulatory` |
| CAPA or NCR discussed | Open or update CAPA | `quality` |
| Pedrero / MoCRA / FDA / retailer attestation | Regulatory action | `regulatory` |
| Cost / MOQ / tariff / allowance change | Margin pressure-test | `margin`, often `ops` and `plm` |
| Competitor / press / retail-data mention | Intel queue | `intel`, often `founder` |
| Anything Ayesha said or asked | Founder briefing line | `founder` plus topic label |

### Urgency signals (auto-flag in Mode 2)
- "critical", "urgent", "ASAP", "blocking", "missed", "failed", "rejected"
- A deadline that has passed or is within 7 days
- A supplier issue, formula problem, **failing test**, **complaint or adverse event**,
  **recall trigger**, or **regulatory deadline** mentioned in the transcript

---

## Action Item Report format

Present this before pushing anything. Group by primary label and show the full label
set + cross-references for each item.

```
📋 Meeting: [Meeting title / participants / date]
Duration: [X min]
Meeting-level labels: [pd, ops, quality, ...]

🚨 URGENT (needs immediate action)
• [Action item] — Owner: [Name] | Due: [date if mentioned]
  Labels: [primary] + [secondary, ...]
  → Parent: [destination skill — e.g., quality-lab-coordinator]
  → Cross-refs: [`outlook-plm-bridge` cross-flag, PD task link, etc.]

🩺 QUALITY
• [Action item / decision] — Owner: [Name] | Due: [date]
  → quality-lab-coordinator / batch-lifecycle-tracker / capa-coordinator /
    complaint-and-event-handler / adverse-event-and-recall-reporter
  → Cross-refs: [PLM, PD, Ops links if applicable]

📜 REGULATORY
• [Action item / decision] — Owner: [Name] | Due: [date]
  → claims-il-and-label-keeper / regulatory-manager
  → Cross-refs: [if any]

📌 OPS / PD ACTION ITEMS
• [Action item] — Owner: [Name] | Due: [date if mentioned] | Project: [SJ SKIN project]
  Labels: [...]

💬 DECISIONS (log as comments)
• [Decision made] → Add to: [task/project name]

📊 STATUS SIGNALS (may need project status update)
• [Issue or blocker raised] → Affects: [project name] | Suggested RAG: [R/A/G]

💰 MARGIN
• [Cost / MOQ / tariff / allowance discussion]
  → margin-pressure-test / walk-away

🔭 INTEL
• [Competitor / retail / press mention]
  → sjs-comp-intel / sjs-retail-intel

👤 FOUNDER BRIEFING
• [Items routed to ayesha-weekly-briefing — Ayesha asks, founder-relevant signals]

⚙️ PLM FLAGS (cross-flag to `outlook-plm-bridge` — owns the actual write)
• [Formula approval / batch info / supplier data / cost target / spec sheet]

---
Which of these should I push? (say "all", list numbers, or "skip")
```

---

## Pushing actions

Once Alvin confirms which items to push, fan out by primary label:

1. For each **`pd` action item** → propose a task using the confirmation preview format
   in `asana-pd-manager/references/confirmation-protocol.md`
2. For each **`ops` action item** → propose a task against the appropriate Ops project
   (purchasing-manager, inventory-manager, supply-demand-planner, logistics-manager,
   oc3pl-order-manager)
3. For each **`quality` action item** → route to the matching Quality skill
   (complaint-and-event-handler for complaints/SAE intake; quality-lab-coordinator
   for OOS/OOT/lab pattern; capa-coordinator for CAPA; batch-lifecycle-tracker for
   batch holds and near expiry; adverse-event-and-recall-reporter for SAE/recall
   filings)
4. For each **`regulatory` action item** → route to claims-il-and-label-keeper for
   IL packets, label artwork, retailer attestations; route to regulatory-manager for
   MoCRA/FDA/state filings and cross-system rollup
5. For each **`margin` action item** → route to margin-pressure-test (parent), with
   walk-away cross-flag if the SKU is at the floor
6. For each **`intel` action item** → route to sjs-comp-intel or sjs-retail-intel
7. For each **`founder` action item** → cross-flag to ayesha-weekly-briefing
8. For each **decision** → propose a comment on the relevant task in whichever
   sub-system owns the parent
9. For each **status signal** → draft a RAG status update for the relevant project
10. For each **stage movement** → propose a Formula Tracker section move with
    confirmation
11. For each **PLM flag** → note it clearly: `⚙️ PLM Bridge: [item] — tag for outlook-plm-bridge`

Always process one confirmation at a time unless Alvin says "do them all." For
multi-label items, confirm the parent first, then surface the cross-reference children
together.

---

## Meeting type intelligence

Tune your extraction based on who was in the meeting and what sub-system the meeting
sits in. Meeting-level labels seed the classifier; individual action items can still
carry their own additional labels.

| Meeting type | Primary focus | Default labels |
|-------------|--------------|---------------|
| Supplier call (KDC-One, AMR Labs, Vegelabs, IKS, Element) | Formula status, timelines, revision feedback, approvals | `pd`, often `plm` |
| HCT call (Alex, David) | Lip treatment dev, RLC forms, color match, turnkey costs | `pd`, often `plm`, `margin` if costs |
| Milinyc call (Perrine) | PD / R&D ownership decisions, packaging dev, samples, testing | `pd`, often `plm`, `quality` if test results |
| Internal team (Alvin, Nicole, Danielle, Soraya, Ciarra, Kate, Erin, Ivy) | Task assignments, project health, blockers, social/creative | varies — classify per item |
| SJS client/brand meeting | Brand decisions, launch priorities, approvals | `pd`, `founder` if Ayesha |
| Vendor review | Vendor scorecard, quality history, commercial terms | `ops`, often `quality`, `margin` |
| S&OP run | Demand forecast, safety stock, reorder points, capacity | `ops`, often `margin` |
| Logistics call | Freight, carrier, customs, duty, 3PL | `ops` |
| Order ops standup (OC3PL) | DTC fulfillment, late shipments, RTS, replacements | `ops` |
| Quality review (CAPA, complaint triage, lab pattern) | Failing tests, complaints, NCRs, batch holds | `quality`, often `regulatory` if reportable |
| Regulatory call (Pedrero — Amy, Heather, Teona) | IL packets, label artwork, MoCRA, FDA, retailer attestation | `regulatory`, often `pd` for product-level |
| Pricing / wholesale / margin review | MSRP, allowance, MAP, channel margin, cost targets | `margin`, often `ops` |
| Comp teardown / retail check-in | Competitor launches, Ulta/Sephora data, press, sell-through | `intel`, often `founder` |
| Ayesha sync / weekly briefing prep | Founder-level decisions, weekly briefing content | `founder` plus whatever topic |

---

## Connection points

This bridge posts to Asana queues per the queue contract — it doesn't call destination skills directly. Canonical map: `references/architecture/bridge_queue_contract.md`.

- **PD queue:** `pd`-labeled actions land in the named SJ SKIN project (or Formula Tracker for stage moves) and follow `asana-pd-manager/references/confirmation-protocol.md`.
- **Ops queue:** `ops`-labeled actions land in the named Ops project (Purchasing / Inventory / S&OP / Logistics / OC3PL Order Management / SJ Shipping Dashboard) per signal subtype.
- **Quality queue:** `quality`-labeled actions land in SJS Quality Management (plus CAPA Log or Complaint Log if subtype is clear). Safety wins the parent slot.
- **Regulatory queue:** `regulatory`-labeled actions land in SJS Regulatory Management (or SJS Reportable Events for SAE / recall).
- **PLM:** `plm`-labeled signal cross-flags to `outlook-plm-bridge`, which owns the email-sourced PLM write through `plm-assistant`. Meeting-sourced PLM writes (formula approvals discussed live, batch records mentioned in passing) cross-flag to `asana-plm-bridge` for Asana-side staging.
- **Outlook follow-ups:** "Send an email to..." action items get cross-flagged to `outlook-asana-bridge` for outbound staging.
- **Margin / Intel / Founder (no queue):** These are direct-output skills with no Asana queue. The bridge does not call them — it lands the underlying data where they read it live (margin cost/MOQ → PLM via `outlook-plm-bridge`; intel/founder signal → surfaced to the operator and upstream rollups). Destination-skill names elsewhere in this file (margin-pressure-test, sjs-comp-intel, ayesha-weekly-briefing, etc.) mark routing intent, not a direct call. Per `references/architecture/bridge_queue_contract.md`.

### Multi-route is the default

Most SJ SKIN meetings produce action items that span more than one sub-system. The classifier always runs, every label is evaluated for every action item, and split + cross-reference is the default. There is no PD-only fast path.

---

## Example interactions

> "Pull action items from my call with KDC-One yesterday"
→ Search Fireflies for KDC-One transcript from yesterday, extract action items,
   present Action Item Report, push confirmed items to Asana.

> "Catch me up on this week's meetings"
→ Fetch all transcripts from the past 7 days, auto-flag urgent items first,
   then present full action item list by meeting.

> "The formula for the Sorrel lip treatment was approved on our call — log it"
→ Propose moving Sorrel task to Signed Approvals in Formula Tracker + flag for PLM.

> "Pull action items from the Pedrero sync this morning"
→ Fetch the transcript, classify as `[regulatory]` at meeting level, route IL packet
   / label artwork / attestation discussion items to claims-il-and-label-keeper and
   regulatory-manager.

> "What came out of the vendor review with Vegelabs?"
→ Fetch transcript, expect `[ops, quality, margin]` at meeting level. Route quality
   history items to quality-lab-coordinator, vendor scorecard items to
   purchasing-manager, any cost/MOQ/tariff discussion to margin-pressure-test.

> "Log the action items from the S&OP run"
→ Classify as `[ops]` (often `[ops, margin]` if pricing comes up). Route forecast and
   safety-stock decisions to supply-demand-planner; allocation/capacity decisions to
   purchasing-manager and inventory-manager.

> "Pull the items from the CAPA review"
→ Classify as `[quality]`. Route to capa-coordinator for CAPA opens/walks/closes;
   cross-flag adverse-event-and-recall-reporter if the CAPA traces back to a
   reportable event.

> "What did Ayesha ask about in the briefing call?"
→ Classify as `[founder]` plus topic labels per item. Route every Ayesha ask to
   ayesha-weekly-briefing; cross-flag the topic-owning sub-system (Quality,
   Regulatory, Intel, etc.) for the underlying work.

> "Catch me up on this week's meetings — everything"
→ Fetch all transcripts from past 7 days, classify each at meeting level + each
   action item, present the full Action Item Report grouped by primary label across
   all sub-systems. Urgent items first.
## Job 0 — Wiki update (runs after confirmed Asana/PLM writes)

After every confirmed Asana write in the session, write a synthesized update to the wiki layer in Supabase (`public.wiki_pages`, project `ujkabbffvhpewpbttmmy`). No additional user confirmation — the Asana write already gated it.

This is the **narrative** layer — the readable relationship/SKU summary that synthesizes what happened. It pairs with the **artifact** ledger the PLM bridges (`asana-plm-bridge`, `outlook-plm-bridge`) append. Both layers fire on the same supplier/SKU pages and don't overwrite each other: narrative is synthesized and compressed; the artifact ledger is append-only document trail.

### Trigger
Fires once at end of session, after the user has confirmed all Asana task creations, comments, and field updates derived from the meeting transcript(s) processed.

### Inputs
Enumerate every entity touched by the confirmed Asana work in this session:
- Suppliers (matched by name → `vendors.id` and `wiki_pages.vendor_id`)
- SKUs (matched by name/SKU → `products.id` and `wiki_pages.product_id`)
- Contacts (page_type = `contact`, lookup by slug)

### Per-entity loop
1. `SELECT slug, content FROM public.wiki_lookup(p_slug => <slug>)` to read the current page.
2. Synthesize an updated markdown body that integrates the new signal from the meeting:
   - Resolved items move from **Open items** → **Resolved items** with a one-line outcome and meeting date.
   - Changed values (lead time, MOQ, contact, status) **replace** the old line — never append a duplicate.
   - New signal lands in the section that fits (Relationship status, Open items, Quality signals, etc.).
   - Capture the meeting's intent, not the raw transcript — one to three sentences per signal.
3. Write:
   ```sql
   UPDATE public.wiki_pages
     SET content = $new_content,
         source_count = source_count + 1,
         last_source = 'meeting/fireflies',
         last_source_ref = $fireflies_transcript_id
     WHERE slug = $slug;
   ```
No manual audit log write needed — the `audit_wiki_pages` trigger on `wiki_pages` fires automatically on INSERT/UPDATE/DELETE and writes a full before/after diff to `public.audit_logs` with `entity_type = 'wiki_pages'`.

If no wiki page exists for a touched entity, INSERT a new row with `page_type` set and `last_source = 'meeting/fireflies'`. The audit trigger writes the `created` row.

### Slug construction

Always derive the slug via `public.wiki_slugify(text)` — never hand-roll a regex. The function does: lowercase, replace `[^a-z0-9]+` with single dash, trim leading/trailing dashes. Source string depends on `page_type`:

| page_type | Source | Slug expression |
|---|---|---|
| `supplier` | `vendors.name` | `'supplier/' \|\| public.wiki_slugify(v.name)` |
| `sku` | `coalesce(products.sku, products.name)` | `'sku/' \|\| public.wiki_slugify(coalesce(p.sku, p.name))` |
| `sop` | `sop_documents.sop_id` | `'sop/' \|\| public.wiki_slugify(s.sop_id)` |
| `contact`, `topic` | caller-defined | `'<page_type>/' \|\| public.wiki_slugify(<your_source>)` |

Resolve the slug **before** the lookup — same function on the read path and the write path. If a `wiki_lookup(p_slug => ...)` returns nothing, the page genuinely doesn't exist and you can INSERT — don't fall back to a hand-built slug.

### Out of scope here
No embedding generation in this pass. No wiki writes for entities only mentioned in passing in the transcript when the Asana work didn't touch them.
