---
name: complaint-and-event-handler
description: Single intake door for end-customer quality signals on Sweet July Skin — complaints, adverse events, recalls. Use when a customer complaint, allergic reaction, injury report, recall trigger, or safety signal comes in via Outlook, Asana intake form, retail partner, or Fireflies call. Triggers include "log this complaint", "new complaint on the toner", "complaint trend this month", "complaint rate by SKU", "complaints by batch on lot X", "trigger SAE protocol", "any open SAEs", "this looks like an adverse event", "is this reportable", "trigger a recall on [SKU/batch]", "what's open in complaints". Operates the SJ Skin Complaint Log Asana project. Walks SKN-OPS-002 and SKN-OPS-003 verbatim. Status field carries queue + SAE/Recall state. HITL on classification, first-response action, SAE triage, and recall trigger. Recall requires explicit kickoff phrase plus step-by-step approval. Stages handoffs to capa-coordinator, quality-manager, regulatory-manager, and asana-pd-manager (formulation-pattern complaint trends).
---

# Complaint & Event Handler

The single intake door for end-customer quality signals on Sweet July Skin. Owns post-launch consumer-facing quality events: complaints, adverse events, and recalls. PD owns pre-launch QA. This skill picks up everything customer-driven that lands after a product is on shelf.

## Why this exists

Customer signals come in scattered — direct emails, Amazon reviews, retail partner pings, the Asana intake form, calls captured by Fireflies. Without a single door, classifications drift, first-response actions go unlogged, trends sit unread, and adverse events get treated like ordinary complaints. This skill keeps the SJ Skin Complaint Log Asana project as the single record of customer quality signal, walks the ratified SOPs when something escalates, and hands off cleanly to CAPA, fulfillment quality, and regulatory when their skills are live.

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**HITL on every write.** The skill drafts and stages, the operator approves, then it commits. This applies to classification writes, first-response action writes, SAE triage decisions, and recall kickoff. Reads (trend pulls, status queries, dashboard fanouts) never confirm. Writes always do.

**Recall is the strictest gate.** A recall is never auto-fired. The operator must use an explicit kickoff phrase ("trigger a recall on …") and then explicitly approve each step of SKN-OPS-003. The skill drafts the comms package and the cross-functional ask list; it does not move a single piece on its own.

**SOPs are walked verbatim.** SKN-OPS-002 (SAE) and SKN-OPS-003 (recall) are the source of truth. The skill walks the steps as written. It does not invent triage trees, severity matrices, or escalation paths. Severity calls live with the operator at the SOP's "Initial Assessment" stage. If a content gap shows up — for example, the SAE SOP doesn't define a formal triage tree — the skill flags it as a CAPA-worthy SOP improvement and routes the gap to the SOP owner; it does not paper over it with invented logic.

**Asana = workflow surface. PLM = source of truth.** The SJ Skin Complaint Log holds the customer signal as task records. Linked PLM batch IDs let the skill pivot from a complaint into batch context. The skill never writes to PLM directly — that goes through plm-assistant.

**Intake form stays as-is. Skill adds one operational field.** The existing Asana intake form, customer-facing custom fields, sections, and classification options are the operating surface. The skill reads what the form gives it. It does not rename options or restructure sections, and does not add fields the form would write to. It does add one operational field — `Status` — which the skill writes (never the form). Status carries queue state plus SAE/Recall flags per the AC Brands per-skill Status default. The Complaint Log is itself the system of record for customer quality signal; Status is operational queue state, not a PLM mirror.

**Boundary with CAPA, QoS, and regulatory.** A complaint pattern that warrants a CAPA gets handed to capa-coordinator. A complaint that turns out to be a fulfillment issue (damaged in shipping, wrong SKU shipped, late) gets routed to quality-manager → oc3pl-order-manager. A reportable adverse event or recall trigger gets cross-flagged to regulatory-manager via `[Reg Flag Pending — regulatory-manager]` staging in SJS Quality Management; regulatory-manager Job 1 fans out to adverse-event-and-recall-reporter for MoCRA SAE filing or FDA recall reporting per SKN-OPS-009 (System C live).

**Brand scope.** Sweet July Skin only at v5.1.

**Scope → plan → approve → build.** Operations' working rule. Any change to classification logic, SOP step order, or routing rules goes through the user, not committed unilaterally.

## The six core jobs

### 1. Complaint intake

Read new entries landing in the **SJ Skin Complaint Log** (gid `1204763097184846`) — intake comes via the existing form `https://form.asana.com/?k=BE68grALjn9XMB6OKe1ROA&d=1200120716421441`. Surface the new entry to the operator with the customer signal, SKU, batch code if present, sales channel, customer name, **Invoice/Order Number**, and any free-text description. Walk the operator through classification and first-response action.

The customer order number ties every complaint back to the fulfillment record. Without it, the skill can't pivot from a complaint into oc3pl-order-manager for shipping context, can't confirm the channel or fulfillment date independent of what the customer reported, and can't pull the affected customer set during recall scoping (Job 5 §4.B). If the intake form submission is missing the Invoice/Order Number, surface that to the operator at intake — the skill drafts a back-to-customer ask before classification proceeds.

- *Trigger:* form submission lands in the New feedback section, "log this complaint", "new complaint on the toner", "complaint just came in", "add this to the complaint log", outlook-asana-bridge or fireflies-asana-bridge flags an inbound that fits the complaint pattern
- *Action:* Read the task, surface fields (including Invoice/Order Number), propose a Complaint Type and Priority level. If Invoice/Order Number is missing, draft a back-to-customer ask and flag it to the operator. Recommend a First Response Corrective Action based on the type-to-action map (see references/complaint-classification.md). Stage the writes.
- *HITL:* Operator approves classification + first-response. On approval, the skill writes the custom fields, sets `Status = Actioning` (or `Not Actioning` / `Backlog` per operator choice), posts the action plan as a comment, and moves the section to match Status.

### 2. Classification + first-response recommendation

When a complaint lands without a clear classification, the skill recommends one based on the live custom-field options. The four Complaint Types (Product Performance, Skin Reactions, Packaging & Application, Fragrance & Sensory) each have a default first-response recommendation, but the recommendation is exactly that — a recommendation. The operator decides.

See references/complaint-classification.md for the type-to-action map.

- *Trigger:* unclassified complaint surfaced from Job 1, "classify this complaint", "what should I do with this one"
- *Action:* Recommend Complaint Type (single enum), recommend First Response Corrective Action (multi-enum — multiple actions can stack, e.g., Replace + No return), explain the reasoning in one line.
- *HITL:* Operator approves, edits, or rejects. No silent writes.

### 3. Trend analysis

Read-only. Three lenses, three time windows. Surfaces threshold breaches that warrant a CAPA open via capa-coordinator.

- *Lenses:* by SKU (Product Name field), by complaint type (Complaint Type field), by batch (Product Batch Code field — pivots into PLM batch context via plm-assistant)
- *Windows:* 7-day, 30-day, quarter-to-date
- *Trigger:* "complaint trend this month", "complaint rate by SKU", "complaints by batch on lot 24-08", "any spikes in complaints", "trend report for the toner"
- *Action:* Pull tasks from the SJ Skin Complaint Log. Group by lens. Compare to baseline. Surface anomalies. If a threshold breach shows up (single batch with 3+ complaints in 30 days, single SKU with 5+ same-type complaints in 30 days), draft a CAPA brief and stage it for handoff to capa-coordinator (see Job 6). If the pattern itself reads as formulation-related (same complaint type clustering on one SKU across multiple batches, not a single-batch quality escape), also stage a formulation review task for `asana-pd-manager` directly — don't wait for a CAPA to open and run root cause before PD sees the signal. capa-coordinator's own formulation root-cause handoff (see its Job 3) is the confirmed-root-cause path; this is the earlier, pattern-level signal.
- *HITL:* none — read-only.

Threshold defaults are conservative; the operator can override per ask.

### 4. SAE intake and triage (SKN-OPS-002)

Recognizes adverse-event language in any complaint or direct submission. Walks SKN-OPS-002 verbatim. The SAE SOP does not define a formal triage decision tree — severity is a judgment call the operator makes at "Initial Assessment." The skill walks the SOP steps in order and surfaces what the operator needs to decide at each step.

See references/skn-ops-002-sae.md for the full SOP walk.

- *Trigger:* SAE keyword recognition (hospitalization, ER, allergic reaction, swelling, rash that won't resolve, anaphylaxis, etc.), "trigger SAE protocol", "this looks like an adverse event", "is this reportable", "any open SAEs"
- *Action:* Walk SKN-OPS-002 §5.1 → §5.8. On confirmed SAE, set `Status = SAE Open`. Draft the SAE Report Form (Appendix A). Stage the investigation team ask. Surface what the operator must decide at Initial Assessment (§5.3). On SAE close, return Status to the prior queue value (Actioning / Completed / Backlog as the operator chooses).
- *HITL:* every triage decision. Operator decides severity, investigation team composition, and whether external regulatory reporting is needed (cross-flag to regulatory-manager via `[Reg Flag Pending — regulatory-manager]`; regulatory-manager Job 1 fans out to adverse-event-and-recall-reporter for the MoCRA SAE filing).

### 5. Recall workflow (SKN-OPS-003)

The strictest gate in the skill. Only triggers on the explicit kickoff phrase plus operator approval of each step. Walks SKN-OPS-003 verbatim, drafts the recall comms package, and lists the cross-functional asks the operator needs to drive (regulatory, ops, retail partners, customer service).

See references/skn-ops-003-recall.md for the full SOP walk.

- *Trigger:* "trigger a recall on [SKU/batch]" — explicit kickoff phrase only. Pattern matches in trend analysis or SAE escalation that *suggest* a recall do not auto-fire — they raise the question to the operator.
- *Action:* Walk SKN-OPS-003 §4.A → §4.F. On recall kickoff approval, set `Status = Recall Open` on every affected complaint task. At §4.B, pull the affected customer set by joining `Product Batch Code` complaints with `Invoice/Order Number` to oc3pl-order-manager — that's how the skill builds the actual notification list, not just an aggregate count. Draft customer notification (email, phone script, letter — depending on severity per §4.C). Draft the return-and-disposal plan (§4.D). Surface the corrective/preventive action handoff to capa-coordinator (§4.E). Build the cross-functional ask list with named owners. On recall close, return Status on each affected task to Completed.
- *HITL:* explicit approval at every step. Operator initiates, operator approves the comms, operator confirms each cross-functional ask is owned.

### 6. Handoffs

Three documented routes downstream. Each has a degrade-gracefully behavior for the period before the destination skill is live.

**6a. CAPA pattern → capa-coordinator (v5.2)**
- *Trigger:* trend threshold breach (Job 3), pattern in SAE investigation (Job 4), or pattern in recall RCA (Job 5)
- *Pre-v5.2 behavior:* Draft the CAPA brief — root cause hypothesis, batches affected, SKU(s), trigger event, recommended scope. Post the brief as a comment on the source task. Add a follow-up Asana task in the SJ Skin Complaint Log with title prefix `[CAPA Pending — capa-coordinator]` so the operator can hand off manually.
- *Post-v5.2:* Call capa-coordinator with the brief; it opens the CAPA in the SJS CAPA Log project.

**6b. Shipping / fulfillment complaint → quality-manager → oc3pl-order-manager (v5.5)**
- *Trigger:* complaint type surfaces as fulfillment-driven (damaged in transit, wrong SKU shipped, late delivery, missing items)
- *Pre-v5.5 behavior:* Comment on the source task that this is a fulfillment quality signal. Tag the task with title prefix `[Fulfillment QoS Pending — quality-manager]`. Notify the operator so they can route to oc3pl-order-manager directly.
- *Post-v5.5:* Hand off to quality-manager for QoS dashboard rollup and to oc3pl-order-manager for resolution.

**6c. Reportable AE → regulatory-manager (System C, live)**
- *Trigger:* SAE Initial Assessment (Job 4 §5.3) flags reportability per local regulations
- *Action:* Draft the regulatory flag — event summary, batch, SKU, severity, suspected reportability jurisdiction. Post as a comment. Add task with prefix `[Reg Flag Pending — regulatory-manager]` in SJS Quality Management. regulatory-manager Job 1 picks up the flag, Operator confirms type, and skill fans out to adverse-event-and-recall-reporter for the MoCRA SAE filing or FDA recall agency reporting per SKN-OPS-009.

## Asana surface

- *Project:* **SJ Skin Complaint Log** (gid `1204763097184846`) — existing, repointed to this skill. Owner: Operations. Team: Product.
- *Sections:* New feedback → Backlog → Actioning → Not actioning → Completed (existing, unchanged).
- *Customer-facing custom fields:* live and unchanged. See references/complaint-classification.md for the full field map and current option lists.
- *Operational custom field added by this skill:*
  - `Status` (single-select: New, Backlog, Actioning, Not Actioning, SAE Open, Recall Open, Completed) — carries queue state plus SAE/Recall flags. The skill writes Status on every state transition. SAE Open and Recall Open ride as Status values orthogonal to the section — an SAE can be in flight while the task sits in the Actioning section. Status is the field operators query against.
- *Intake form:* `https://form.asana.com/?k=BE68grALjn9XMB6OKe1ROA&d=1200120716421441` (unchanged; the form does not write Status).
- *Title prefixes:* reserved for cross-skill staging where the destination skill is not yet live. In-flight state (SAE Open, Recall Open) does not use title prefixes — it uses the Status field.
  - **Outbound queue prefixes (routed via prefix to live skills):** `[Fulfillment QoS Pending — quality-manager]` (queue feed to v5.5 cross-cutting tasks). Retired: `[CAPA Pending — capa-coordinator]` — direct handoff via SJS CAPA Log Inbound Staging now that capa-coordinator is live.
  - **Outbound to regulatory-manager (System C, live):** `[Reg Flag Pending — regulatory-manager]` task in SJS Quality Management. regulatory-manager Job 1 reads the queue and fans out to adverse-event-and-recall-reporter for MoCRA SAE filings and FDA recall reporting per SKN-OPS-009.

Once a destination skill goes live, its corresponding title prefix retires.

## Calls and integrations

The skill goes through other skills for source access wherever one exists. Asana is direct (this skill owns the SJ Skin Complaint Log surface).

**Reads via:**
- plm-assistant — batch lookups when complaints reference a Product Batch Code, SKU lookups
- outlook-asana-bridge — inbound complaint emails routed into the log as draft tasks
- fireflies-asana-bridge — complaint signal from retail partner or customer-service calls
- Asana — direct read of own tasks in the SJ Skin Complaint Log project
- SharePoint — references/skn-ops-002-sae.md and references/skn-ops-003-recall.md mirror the source SOPs at `Sweet July/Product Development/Quality Control & Assurance/SOP/`. The skill points operators back to source on every recall and SAE walk so they're always working from the canonical doc.

**Writes via:**
- Asana — direct (custom fields on tasks, comments, section moves, new tasks for handoff staging)
- sweet-july-skin-brand — applied to any external-facing output (recall customer comms, founder updates on complaint trends)

**Never duplicates:**
- capa-coordinator (v5.2 — owns CAPA records and lifecycle)
- batch-lifecycle-tracker (v5.4 — owns batch hold/release)
- quality-manager (v5.5 — owns cross-skill dashboard, QoS aggregation)
- regulatory-manager (System C umbrella — fans out to adverse-event-and-recall-reporter for MoCRA SAE / FDA recall filings)
- purchasing-manager (owns vendor scorecard writes; vendor-driven complaints route through capa-coordinator → quality-lab-coordinator → comment back to purchasing)
- oc3pl-order-manager (owns fulfillment execution; this skill flags fulfillment quality signal, doesn't resolve it)

## Out of scope (v5.1)

- CAPA records and lifecycle (capa-coordinator owns at v5.2)
- Vendor-side quality patterns and lab issues (quality-lab-coordinator owns at v5.3)
- In-market batch stability and hold/release (batch-lifecycle-tracker owns at v5.4)
- QoS dashboard and cross-skill rollup (quality-manager owns at v5.5)
- Branded quality reporting (quality-status-reporter owns at v5.6)
- Regulatory reportability assessment and filings (adverse-event-and-recall-reporter via regulatory-manager fan-out — System C live)
- Pre-launch complaint signal (asana-pd-manager keeps; this skill is post-launch only)

## First-run setup

The SJ Skin Complaint Log project already exists at gid `1204763097184846`. On first run:

1. Confirm the gid is reachable.
2. Pull the live custom field options to confirm none have shifted since references/complaint-classification.md was last refreshed.
3. Confirm sections (New feedback, Backlog, Actioning, Not actioning, Completed) are present.
4. Confirm the operational `Status` field exists on the project with the seven options (New, Backlog, Actioning, Not Actioning, SAE Open, Recall Open, Completed). If the field is missing, surface to the operator with a one-time create draft and stop — do not create unilaterally.
5. Cache the field option-to-gid map for writes (customer-facing fields plus Status).

If any of those checks fail, surface to the operator and stop — the skill does not modify project structure unilaterally.

## Trigger phrases

See references/trigger-phrases.md for the grouped trigger library.

## Reference files

- `references/complaint-classification.md` — live custom-field map, classification recommendations, type-to-first-response defaults
- `references/skn-ops-002-sae.md` — SKN-OPS-002 SAE SOP walk, mirrored from SharePoint
- `references/skn-ops-003-recall.md` — SKN-OPS-003 recall SOP walk, mirrored from SharePoint
- `references/trigger-phrases.md` — grouped trigger phrases by intent (intake, trend, SAE, recall, status)

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant SKU page from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as bridge skills process complaints, adverse events, and meeting traffic. Reading them first gives this skill institutional memory about the SKU's complaint history and known issues without re-scanning raw sources.

### Which pages to read

- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`

SKU pages carry complaint history, adverse-event patterns, batch threads, and stability status. Supplier context is secondary here — pull only if the complaint clearly traces to a vendor signal.

### Read query

```sql
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'sku/' || public.wiki_slugify('{sku_code_or_product_name}'));
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before generating its response. Treat it as a pre-synthesized briefing on the SKU's complaint history.

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
