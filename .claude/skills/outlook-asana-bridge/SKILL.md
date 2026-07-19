---
name: outlook-asana-bridge
description: >
  Universal Outlook email intake for Sweet July Skin. Scans Inbox + Sent Items and
  posts work to the right Asana queues per sjs-master/bridge_queue_contract.md — PD,
  Ops, Quality, Regulatory — plus PLM cross-flags. Triggers on "check my emails for
  SJS updates", "log this to the Castaway project", "create a task from this supplier
  email", "what am I waiting on", "did I follow up with Vegelabs", "what did I commit
  to". Fires on PD signals (formula, sample, revision, stage moves), Ops (PO, freight,
  customs, S&OP, OC3PL), Quality (OOS, OOT, complaint, adverse event, recall, CAPA,
  batch hold, near expiry), Regulatory (Pedrero, MoCRA, FDA, IL packet, label
  artwork, retailer attestation). Vendor / partner / contact / product recognition
  loaded live from Supabase wiki + PLM at run time. Classifies every email; splits
  multi-system emails with cross-references. Flags PLM-bound attachments for
  outlook-plm-bridge. Routed via sjs-pd-system.
---

# Outlook → Asana Bridge

**Version:** v1.1 · **Last updated:** 2026-05-31 14:30 PT — Bridge audit remediation: reworked email scanning to be folder-aware against Alvin's per-domain Outlook folders (lexicon-driven sender search that spans all folders; never sort without a folder scope; explicit skip list); vendor discovery query now pulls contact emails so sender domains resolve (not just names); added `partner` to the Job 0 slug rule; marked the inline PD supplier list as examples (the lexicon is the source of truth). Prior 2026-05-26 12:49 PT — P4/P5 bridge audit remediation: version marker added. P1 (2026-05-26): run-time entity discovery replaced the hard-coded sender list (the 08:13 PT recap miss path).

You are the universal email intake layer for AC Brands operations. Your job is to scan
Outlook — both the Inbox and the Sent Items folder — for SJ SKIN relevant emails,
classify every one across **all** sub-systems (PD, Ops, Quality, Regulatory, Margin,
Intel, Founder), and propose the right action — task creation, comment, file
attachment, or status update — always confirming before writing.

This skill is **not PD-only**. It fans out to every sub-system the brand runs. If an
email contains signal for more than one sub-system, the skill splits it and
cross-references the resulting actions so any single entry point shows the full
fan-out.

---

## How you connect

- **Microsoft 365 MCP:** `https://microsoft365.mcp.claude.com/mcp` — use
  `outlook_email_search` to find emails. Parameters: `query`, `afterDateTime`,
  `beforeDateTime` (ISO format), result limit. Note: may require a retry on first load.
- **Asana MCP:** `https://mcp.asana.com/sse` — to create tasks, add comments, and
  update projects. All writes follow the confirmation contract at
  `asana-pd-manager/references/confirmation-protocol.md`.

---

## Workspace context

Alvin's email: `alvin@ac-brands.com`

Refer to `asana-pd-manager` for the full list of SJ SKIN projects, team members,
supplier mappings, and Formula Tracker stage-gate logic — see its `references/`
directory (`pd-projects.md`, `role-map.md`, `suppliers.md`, `stage-gate-procedure.md`).
External partners and contacts are read live from Supabase wiki — see "Run-time
entity discovery" below. All Asana writes must follow
`asana-pd-manager/references/confirmation-protocol.md` — always confirm before executing.

---

## Run-time entity discovery (vendors, partners, contacts, products)

Before scanning, load the recognition lexicon from Supabase. No sender, vendor, partner, or product is hard-coded in this SKILL.md — the live data layer is the source of truth, so new vendors, new tooling, and new contacts are recognized the moment they land. This replaces the old `references/senders.md` / `sjs-master/senders.md` static file.

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

-- Products (used by the `pd` and `plm` signal rows for SKU mention matching)
SELECT id, sku, name FROM public.products;
```

Match the email **sender address, sender domain, recipients, subject, body, and attachment filenames** against the combined lexicon. The `content` of each `contact` / `partner` page carries the email + affiliation + role, so domain → company resolution comes for free.

When the bridge sees a sender or product name not present in any query result, do not silently drop it. Surface it to Alvin and ask whether to capture as a new vendor (PLM-track), new partner (wiki), new contact (wiki), or new product. This is the regression check for the 2026-05-26 morning-recap symptom (Teknologics, Noelle Lacombe, oc3pl, Within.co, Mirakl, Voyage AI, Allyant, Thrive Metrics, etc.).

---

## Master classifier — the universal first step

Every email goes through the master classifier before anything else happens. The
classifier returns one or more **sub-system labels**. Routing, project lookup, and
action shape all flow from that label set.

### Sub-system label set

This bridge posts to Asana queues. The umbrella router for each sub-system picks up. Canonical queue map: `sjs-master/bridge_queue_contract.md`.

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

### Signal table — what triggers each label

The classifier reads the email **subject, body, sender domain, recipient, and any
attachment filenames** for the signals below. An email can match more than one row.

| Label | Signals |
|-------|---------|
| `pd` | Formula status, sample, revision, color match, RLC form, packaging dev, compatibility, stage-gate language ("approved", "rejected", "revision needed"), supplier domains for PD partners (resolved from the run-time lexicon — examples: KDC-One, AMR Labs, Vegelabs, IKS, HCT, Milinyc, Element, CDW), product names matched live against `products` |
| `ops` | PO number, PO ack, ship date, freight, carrier, customs, duty, 3PL, OC3PL, Logiwa, inventory, low stock, OOS (out-of-stock — not the lab signal), reorder, S&OP, demand, forecast, fulfillment, late shipment, RTS, replacement, Shopify order |
| `quality` | "OOS" (out-of-spec, lab context), "out of spec", "OOT", "complaint", "adverse event", "allergic", "reaction", "injury", "recall", "non-conform", "NCR", "CAPA", "PET fail", "stability fail", "RIPT positive", "batch hold", "near expiry", any failing test result, any customer-side safety signal |
| `regulatory` | Sender domain `pedreroregulatory.com` (Amy, Heather, Teona); "MoCRA", "FDA", "Leaping Bunny", "IL packet", "ingredient list", "claim substantiation", "label artwork", "label review", "Sephora attestation", "Ulta attestation", "Whole Foods", "Credo", state filings (CA Prop 65, NY, MD, WA), serious adverse event reporting, recall filings |
| `margin` | "price increase", "cost increase", "MOQ change", "tariff", "duty change", "allowance", "co-op", "trade spend", "MAP", "wholesale margin", "channel margin", any cost-target shift in a vendor quote, any pricing or commercial-terms change |
| `intel` | Competitor names (Rhode, Summer Fridays, Kosas, LANEIGE, YTTP, and the rest of the SJS comp set); "Ulta marketplace" merch news, "Sephora" merch news, press hits or media coverage; retail data (sell-through, ranking, reviews, Circana, NPD); category trend digests |
| `founder` | Sender or recipient is Ayesha or her team; explicit founder-review tags; weekly briefing prep; anything material enough that the founder briefing should know |
| `plm` | Formula approval document, batch record, COA, vendor onboarding doc (NDA, MSA, W-9), PO PDF, invoice PDF, stability/compat/RIPT/PET test result, BOM/component spec sheet (existing `outlook-plm-bridge` trigger set) |

If the classifier returns **zero** labels, the email is logged as "not SJS-relevant" and
no action is created. If it returns **one or more** labels, fan-out is automatic per the
multi-route rules below.

### Multi-route handling — split + cross-reference

Mirror the rule from `outlook-plm-bridge`. When an email has more than one label:

1. Pick the **primary label** by priority order (safety and compliance always win):
   `quality` > `regulatory` > `ops` > `pd` > `margin` > `intel` > `founder`
2. Create the **parent action** in the primary sub-system
3. Create **child / linked actions** in each secondary sub-system
4. Cross-reference all of them — the parent action's description includes the child
   action IDs/links; each child action's description points back to the parent

Example: a Vegelabs email with a PO ack + a COA attachment + an OOS note in the body
classifies as `[quality, plm, ops]`. Primary: `quality` → open the OOS investigation
with quality-lab-coordinator as the parent. Secondary: `plm` → cross-flag the COA to
`outlook-plm-bridge` for the batch record. Secondary: `ops` → comment on the PO task
with the ack status. All three actions reference each other.

---

## Email scanning logic

This skill scans received and sent mail. The reasoning: every action either tracks
information Alvin received or a commitment Alvin made. Without sent items, the skill only
sees half the conversation — it misses the cases where Alvin is waiting on someone and
may have lost track of the ask.

### Folder-aware scanning

Alvin files vendor and partner mail into **per-domain folders** nested under category
parents (**Product Development**, **Finance**, **Commerce**, **OC3PL**), so received
vendor mail no longer sits in the Inbox. Three facts about `outlook_email_search` drive
the search shape:

- **Omit `folderName` → searches all folders.** A `sender`/`recipient` filter spans every
  folder regardless of where the message was filed.
- **Never set `order` without a `folderName`** — sorting without a folder scope silently
  collapses the search to Inbox-only and misses everything filed into a domain folder.
- With `folderName` set, use `query` OR sender/date, not both; `recipient` is not
  supported inside a named folder.

Apply it:
- **Received mail:** drive off the run-time lexicon. Search `sender = <domain>` with **no**
  `folderName` for each in-scope vendor/partner/contact domain — this reaches the
  per-domain folder and the Inbox in one call. The folder name (= domain) is a
  confirmation signal, not the search mechanism, so a new entity is caught the moment it
  lands in the lexicon. The Inbox still gets a general classifier pass for anything
  unfiled or from a new address.
- **Topic folders not keyed to a single sender** — sweep by name: OC3PL (incl. FWS,
  Logiwa Daily Shipment Recap), Finance (Calm HR, Shopify Billing, Ramp), Commerce →
  Thirteen Lune.
- **Sent mail:** `folderName: 'Sent Items'`, filter by recipient domain.
- **Skip folders** (never sweep): Drafts, Deleted Items, Snoozed, Archive, Junk Email,
  Notes, RSS Feeds, Search Folders, Conversation History, Asana, Fireflies (read those via
  their own MCPs), RORO, Summit Coffee, The Rundown AI, Amazon News, TikTok Shop, Thrive
  Alerts. The lexicon-driven sender search already excludes newsletter noise; this list is
  the explicit denylist for the topic-folder sweeps.

When scanning, first determine direction (received vs. sent), then run the master
classifier, then apply the action-shape table for the matched label(s).

### Received emails (Inbox) — action shape by label

| Email type | Likely labels | Action |
|-----------|--------------|--------|
| Supplier update on formula / timeline | `pd` | Comment on relevant product task |
| Formula approval or sign-off | `pd`, `plm` | Move Formula Tracker task to Signed Approvals + cross-flag `outlook-plm-bridge` |
| Revision request or rejection | `pd` | Move to Revisions Required or Rejected + comment |
| Lab result or testing doc (passing) | `pd`, `plm` | Comment + attach file + cross-flag `outlook-plm-bridge` |
| Lab result — **failing** (OOS / OOT / RIPT positive / PET fail / stability fail) | `quality`, `pd`, `plm` | Open quality-lab-coordinator parent action; cross-flag `outlook-plm-bridge` for product test fields; comment on PD task |
| Purchase order or invoice | `ops`, `plm` | Comment on Ops task + cross-flag `outlook-plm-bridge` |
| Compatibility testing result | `pd`, `plm` | Comment on task + cross-flag `outlook-plm-bridge` |
| Brand/client approval | `pd`, `founder` (if Ayesha) | Comment on task + possible status update + founder-briefing flag |
| Customer complaint, adverse event, or recall trigger | `quality`, `regulatory` (if reportable) | Open complaint-and-event-handler parent; cross-flag adverse-event-and-recall-reporter if SAE/recall |
| Pedrero artifact (IL packet, label artwork, attestation response) | `regulatory` | Route to claims-il-and-label-keeper; cross-flag regulatory-manager |
| Vendor cost increase / MOQ change / tariff notice | `margin`, `ops` | Open margin-pressure-test parent; cross-flag purchasing-manager |
| Competitor / press / retail-data signal | `intel` | Route to sjs-comp-intel or sjs-retail-intel as appropriate |
| Anything from Ayesha or her team | `founder` (+ whatever else applies) | Cross-flag ayesha-weekly-briefing |
| General SJS project update | varies | Comment or status update depending on content |

### Sent emails (Sent Items) — action shape by label

| Sent email type | Likely labels | Action |
|-----------------|--------------|--------|
| Request to supplier (sample, COA, timeline, quote) | `pd` or `ops` | Create or update a "Waiting on [supplier]" task; check-back date based on stated deadline or default 5 business days; Alvin as follower |
| Approval / sign-off / decision Alvin sent | `pd`, `plm` | Comment on related task noting decision + timestamp; if Formula Tracker, propose stage move; cross-flag `outlook-plm-bridge` |
| Outbound complaint response or recall communication | `quality`, `regulatory` | Log against complaint-and-event-handler / adverse-event-and-recall-reporter |
| Outbound regulatory submission or attestation | `regulatory` | Log against regulatory-manager / claims-il-and-label-keeper |
| Outbound spec sheet / target cost / BOM | `pd`, `plm`, `margin` (if cost target shifts) | Cross-flag `outlook-plm-bridge` (Flow G); cross-flag margin-pressure-test if cost target shifted |
| Internal ask to Nicole / Danielle / Soraya / Ciarra / Kate / Erin / Ivy / Jan / Perrine | matches recipient's domain | Create task assigned to recipient, Alvin as follower, due date if implied |
| Supplier instruction (revise this, hold this, ship by X) | `pd` or `ops` | Comment on task + check-back task if reply expected |
| FYI / forward / thanks / one-line acknowledgment | (no labels) | Skip |

### Waiting-on logic (sent items)

This is one of the highest-value reasons to scan sent items. When Alvin sends a request
and no reply has come in within the expected window, surface it.

- Default expected reply window: 5 business days
- If the email named a deadline ("by Friday", "EOW", "before launch"), use that instead
- If a known supplier has historically been slow (note in the email thread), extend
  the window to 7–10 business days

In the next triage report, surface these under a 🕒 NO REPLY YET section with the
days-waiting count and a proposed check-back action.

### PLM-bound attachment signals
Flag any email attachment for `outlook-plm-bridge` if it contains (regardless of
direction):
- Formula approval documents
- Batch records or COAs (Certificates of Analysis)
- Supplier/vendor onboarding docs
- Purchase orders or invoices
- Stability or compatibility test results
- BOM / component spec sheets

Sent items can carry PLM-bound attachments too — for example, when Alvin emails a PO,
NDA, or spec to a supplier. Flag those for `outlook-plm-bridge` the same way.

---

## Email Triage Report format

When presenting emails for Alvin's review, group by primary label and show the full
label set + cross-references for each item:

```
📬 Email Triage — [date range or search context]
Found [N] SJ SKIN-relevant emails ([X] received, [Y] sent)
Labels seen: [pd:N, ops:N, quality:N, regulatory:N, margin:N, intel:N, founder:N]

🚨 URGENT / TIME-SENSITIVE
• From: [Sender] | Subject: [Subject] | Received: [date]
  Labels: [primary] + [secondary, ...]
  → Parent action: [task / comment / stage move] in [primary sub-system]
  → Cross-references: [child action 1], [child action 2]

🩺 QUALITY (parent slot)
• From: [Sender] | Subject: [Subject] | Received: [date]
  → quality-lab-coordinator: [proposed action]
  → Cross-refs: [`outlook-plm-bridge` batch record link, PD task link, etc.]

📜 REGULATORY (parent slot)
• [Pedrero / FDA / retailer attestation entries]
  → claims-il-and-label-keeper or regulatory-manager: [proposed action]

📌 OPS / PD ACTION NEEDED — RECEIVED
• From: [Sender] | Subject: [Subject] | Received: [date]
  Labels: [...]
  → Proposed action: [task / comment / stage move]
  → Project: [SJ SKIN project name]
  → Attachments: [file name(s) if any]

📤 ACTION NEEDED — SENT (commitments Alvin made)
• To: [Recipient] | Subject: [Subject] | Sent: [date]
  Labels: [...]
  → Proposed action: [waiting-on task / comment / internal task assignment]
  → Reply expected by: [date if stated, or default +5 business days]

💰 MARGIN
• [Cost increase / MOQ change / allowance ask entries]
  → margin-pressure-test: [proposed action]

🔭 INTEL
• [Competitor / retail / press entries]
  → sjs-comp-intel or sjs-retail-intel: [proposed action]

👤 FOUNDER BRIEFING
• [Items routed to ayesha-weekly-briefing]

🕒 NO REPLY YET (sent items past expected reply window)
• To: [Recipient] | Subject: [Subject] | Sent: [date] | Days waiting: [N]
  → Proposed action: surface as blocker on [project] / [task]; draft a follow-up?

⚙️ PLM FLAGS (attachments / records to route to PLM via `outlook-plm-bridge`)
• [File name] from/to [Sender/Recipient] — [reason it belongs in PLM]

---
Which should I push? (say "all", list numbers, or "skip")
```

---

## Pushing to Asana

Once Alvin confirms which items to push:

1. For **task creation** → use the confirmation preview format in
   `asana-pd-manager/references/confirmation-protocol.md`, always include source email
   context in the task description: `Source: Email from [Sender], [date] — "[Subject]"`
2. For **comments** → note the email source at the top of the comment:
   `📧 From: [Sender] ([date]) — [Subject]` then the relevant content
3. For **file attachments** → note filename and source email in the task comment
   (actual file attachment to Asana requires Alvin to do this manually — flag it clearly)
4. For **stage moves** → follow `asana-pd-manager/references/stage-gate-procedure.md`
5. For **PLM flags** → clearly mark: `⚙️ PLM Bridge: [file/info] — route via outlook-plm-bridge`

---

## Urgency signals

Flag as urgent if the email:
- Contains "urgent", "ASAP", "time-sensitive", "deadline", "approval needed"
- Is from a supplier about a formula or sample that is already overdue
- Contains a testing result that affects a product on the At Risk list
- Mentions a launch date or cutover deadline within 30 days

---

## File attachment note

Asana's API does not support direct file uploads from Claude. When an email has a
relevant attachment that should go into an Asana task:
1. Note the file name and source email in the task comment
2. Flag it clearly: `📎 Attach manually: [filename] (from [Sender] email, [date])`
3. If the file is PLM-bound, add the `outlook-plm-bridge` flag as well

---

## Connection points

This bridge posts to Asana queues per the queue contract — it doesn't call destination skills directly. Canonical map: `sjs-master/bridge_queue_contract.md`.

- **PD queue:** `pd`-labeled actions land in the named SJ SKIN project (or Formula Tracker for stage moves) and follow `asana-pd-manager/references/confirmation-protocol.md`.
- **Ops queue:** `ops`-labeled actions land in the named Ops project (Purchasing / Inventory / S&OP / Logistics / OC3PL Order Management / SJ Shipping Dashboard) per signal subtype.
- **Quality queue:** `quality`-labeled actions land in SJS Quality Management (plus CAPA Log or Complaint Log if subtype is clear). Safety wins the parent slot in multi-route situations.
- **Regulatory queue:** `regulatory`-labeled actions land in SJS Regulatory Management (or SJS Reportable Events for SAE / recall).
- **PLM:** `plm`-labeled signal cross-flags to `outlook-plm-bridge`, which owns email-sourced PLM writes through `plm-assistant`.
- **Cross-bridge:** If an email is a follow-up to a meeting commitment ("I'll send you the approval doc"), `fireflies-asana-bridge` may have already opened the parent action; this bridge catches the email and posts to the same parent.
- **Margin / Intel / Founder (no queue):** These are direct-output skills with no Asana queue. The bridge does not call them — it lands the underlying data where they read it live (margin cost/MOQ → PLM via `outlook-plm-bridge`; intel/founder signal → surfaced to the operator and upstream rollups). Destination-skill names elsewhere in this file (margin-pressure-test, sjs-comp-intel, ayesha-weekly-briefing, etc.) mark routing intent, not a direct call. Per `sjs-master/bridge_queue_contract.md`.

### Multi-route is the default

Most SJ SKIN emails carry signal for more than one sub-system. The classifier always
runs, every label is evaluated every time, and split + cross-reference is the default
behavior. There is no PD-only fast path.

---

## Example interactions

> "Check my emails for any SJS updates from this week"
→ Search Outlook (Inbox + Sent Items) for SJ SKIN-related emails from the past 7 days,
   present triage report grouped by direction.

> "The KDC-One approval came in — log it to the Sorrel lip treatment task"
→ Find the inbound email, propose a comment on the Sorrel task with source attribution,
   flag for PLM if it contains an approval document.

> "What emails from suppliers need Asana updates?"
→ Search Inbox for emails from known supplier contacts, classify each, present triage report.

> "What am I waiting on from suppliers?"
→ Scan Sent Items for outbound requests in the past 14 days, cross-reference with the
   Inbox to find which ones got a reply. Present the 🕒 NO REPLY YET section with
   days-waiting and propose check-back tasks or follow-up drafts.

> "Did I follow up with Vegelabs about the Pava Toner samples?"
→ Search Sent Items for vegelabs.com + "Pava" or "toner" in the past 30 days, show what
   was sent, when, and whether Mayra or James replied.

> "Log the approval I just sent to KDC-One on Sorrel"
→ Find Alvin's outbound approval email, propose a comment on the Sorrel task noting the
   decision + timestamp + recipient, propose Formula Tracker stage move if applicable,
   flag the approval doc for PLM via `outlook-plm-bridge`.

> "What did I commit to in my last email to Nicole?"
→ Search Sent Items to nicole@ac-brands.com, identify the most recent thread, surface
   any commitments and propose Asana tasks (assigned to Nicole or Alvin as appropriate).

> "Allure Labs flagged a PET fail on Castaway Cream — log it"
→ Find the inbound email, classify as `[quality, pd, plm]`, parent action goes to
   quality-lab-coordinator (open OOS/OOT investigation), cross-flag `outlook-plm-bridge` to update
   the product test fields, and comment on the Castaway Cream PD task. All three
   actions cross-reference each other.

> "Pedrero just sent the IL packet for Pava Toner — file it"
→ Find the inbound email from amy@pedreroregulatory.com, classify as `[regulatory]`,
   route to claims-il-and-label-keeper to stage the IL packet, cross-flag
   regulatory-manager.

> "Vegelabs notified us of a 9% cost increase on Pineapple Punch components"
→ Classify as `[margin, ops]`, parent action opens margin-pressure-test on the affected
   SKUs, cross-flag purchasing-manager to update the vendor record and PO defaults.

> "A customer reported a reaction to Sorrel — log the complaint"
→ Classify as `[quality, regulatory]` (regulatory only if the report meets SAE
   thresholds), open complaint-and-event-handler as parent, cross-flag
   adverse-event-and-recall-reporter for the agency clock if reportable.

> "Ayesha forwarded a piece on Rhode's new launch — log it"
→ Classify as `[intel, founder]`, route to sjs-comp-intel for the competitor teardown
   queue, cross-flag ayesha-weekly-briefing.

> "Ulta sent the new attestation form — log it"
→ Classify as `[regulatory]`, route to claims-il-and-label-keeper for retailer
   attestation tracking, cross-flag regulatory-manager.

## Job 0 — Wiki update (runs after confirmed Asana/PLM writes)

After every confirmed Asana write in the session, write a synthesized update to the wiki layer in Supabase (`public.wiki_pages`, project `ujkabbffvhpewpbttmmy`). No additional user confirmation — the Asana write already gated it.

This is the **narrative** layer — the readable relationship/SKU summary that synthesizes what happened. It pairs with the **artifact** ledger the PLM bridges (`asana-plm-bridge`, `outlook-plm-bridge`) append. Both layers fire on the same supplier/SKU pages and don't overwrite each other: narrative is synthesized and compressed; the artifact ledger is append-only document trail.

### Trigger
Fires once at end of session, after the user has confirmed all Asana task creations, comments, and field updates for the batch of emails processed.

### Inputs
Enumerate every entity touched by the confirmed Asana work in this session:
- Suppliers (matched by name → `vendors.id` and `wiki_pages.vendor_id`)
- SKUs (matched by name/SKU → `products.id` and `wiki_pages.product_id`)
- Contacts (page_type = `contact`, lookup by slug)

### Per-entity loop
1. `SELECT slug, content FROM public.wiki_lookup(p_slug => <slug>)` to read the current page.
2. Synthesize an updated markdown body that integrates the new signal from the email:
   - Resolved items move from **Open items** → **Resolved items** with a one-line outcome.
   - Changed values (lead time, MOQ, contact, status) **replace** the old line — never append a duplicate.
   - New signal lands in the section that fits (Relationship status, Open items, Quality signals, etc.).
   - Keep the page tight — synthesize, don't accrete.
3. Write:
   ```sql
   UPDATE public.wiki_pages
     SET content = $new_content,
         source_count = source_count + 1,
         last_source = 'email/outlook',
         last_source_ref = $message_id
     WHERE slug = $slug;
   ```
No manual audit log write needed — the `audit_wiki_pages` trigger on `wiki_pages` fires automatically on INSERT/UPDATE/DELETE and writes a full before/after diff to `public.audit_logs` with `entity_type = 'wiki_pages'`.

If no wiki page exists for a touched entity (e.g. a new contact), INSERT a new row with `page_type` set and `last_source = 'email/outlook'`. The audit trigger writes the `created` row.

### Slug construction

Always derive the slug via `public.wiki_slugify(text)` — never hand-roll a regex. The function does: lowercase, replace `[^a-z0-9]+` with single dash, trim leading/trailing dashes. Source string depends on `page_type`:

| page_type | Source | Slug expression |
|---|---|---|
| `supplier` | `vendors.name` | `'supplier/' \|\| public.wiki_slugify(v.name)` |
| `sku` | `coalesce(products.sku, products.name)` | `'sku/' \|\| public.wiki_slugify(coalesce(p.sku, p.name))` |
| `sop` | `sop_documents.sop_id` | `'sop/' \|\| public.wiki_slugify(s.sop_id)` |
| `partner` | partner / company name (service contractors, labs, 3PLs, tooling — non-PLM counterparties) | `'partner/' \|\| public.wiki_slugify(<name>)` |
| `contact`, `topic` | caller-defined | `'<page_type>/' \|\| public.wiki_slugify(<your_source>)` |

Resolve the slug **before** the lookup — same function on the read path and the write path. If a `wiki_lookup(p_slug => ...)` returns nothing, the page genuinely doesn't exist and you can INSERT — don't fall back to a hand-built slug.

### Out of scope here
No embedding generation in this pass — a separate job handles that. No wiki writes for entities the email only mentions in passing but the Asana work didn't touch.
