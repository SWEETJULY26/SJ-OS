---
name: quality-manager
description: System B umbrella for Sweet July Skin quality management. Use for cross-skill quality rollup, SOP catalog queries, SOP ratification or annual review, cross-cutting tasks (audits, retailer questionnaires, regulatory inspections, quality system reviews), QoS signal from oc3pl-order-manager, and cadence composition (weekly digest, monthly snapshot, quarterly rollup) for quality-status-reporter. Triggers include "what's open in quality", "quality dashboard", "monthly quality summary", "shipping quality this week", "current revision of SKN-OPS-XXX", "SOPs due for review", "QoS rollup", "compose weekly quality digest", "compose monthly quality rollup", "compose quarterly quality rollup". Owns SJS Quality Management at v5.6. Holds canonical role-map and SOP catalog for System B (capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker). Aggregates rollup; does not run sub-skill workflows. HITL on cross-skill task creation, SOP ratification, and quarterly handoff comments.
---

# Quality Manager

System B's umbrella. Aggregates state across the four sub-skills, owns the SOP catalog and ratification queue, runs cross-cutting tasks that don't fit any single sub-skill, and pulls quality-of-service signal from oc3pl-order-manager. Read-most surface with two HITL gates: cross-skill task creation and SOP ratification approval.

## Why this exists

System B has four sub-skills (capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker) that each own their workflow. Without an umbrella, three things go missing: a single rollup of "what's open in quality," a canonical SOP catalog (which revision is current, what's pending, what's due for annual review), and a home for cross-cutting work that spans multiple sub-skills (audit prep, regulatory inspections, retailer quality questionnaires).

This skill is that umbrella. It doesn't duplicate sub-skill work — it surfaces, catalogs, and coordinates. The branded report generation lives in v5.6 quality-status-reporter, which pulls from this skill's rollup. The cross-system router (PD ↔ Quality ↔ Regulatory) lives in v5.7 ac-brands-quality-system.

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**Read-most by design.** The skill aggregates and surfaces; sub-skills do the workflow writes. Two HITL gates: cross-skill task creation (Operator stages, QA Lead approves) and SOP ratification approval (QA Lead approves; Operator stages from the queue). Everything else is read-only.

**SOP catalog as canonical reference.** The catalog at `references/sop-catalog.md` is the runtime source of truth for which SOP revision is current. Sub-skills query the catalog before significant writes. The catalog mirrors SharePoint state plus skill-side metadata (last review, next-review-due, ratification status, owner role, in-flight drafts).

**Asana = workflow surface. PLM = source of truth (sub-skills' domain).** This skill writes Asana project status updates, cross-cutting tasks, and SOP catalog entries. PLM reads happen via plm-assistant when needed for QoS or audit context.

**Boundary with sub-skills — no duplication.** A complaint trend already in complaint-and-event-handler doesn't get re-opened here. A vendor scorecard signal already routed through quality-lab-coordinator doesn't get re-flagged. This skill surfaces what's already in flight and creates only the cross-cutting work that doesn't fit anywhere else.

**Boundary with v5.6 quality-status-reporter.** This skill produces the rollup data and weekly Asana project status. v5.6 generates the branded PDF/PPTX/HTML reports and pushes them to the System B reporting hub. v5.6 reads this skill's rollup; this skill never generates branded output.

**Brand scope.** Sweet July Skin only at v5.6.

**Scope → plan → approve → build.** Operations' working rule. Any change to SOP catalog logic, QoS thresholds, or cross-cutting task types goes through the user, not committed unilaterally.

## The eight core jobs

### 1. SOP catalog + ratification queue (Job 1)

Maintains an active catalog of every Sweet July Skin SOP plus the ratification queue for in-flight drafts. The catalog table lives at `references/sop-catalog.md` and renders as a pinned task in the SOP Catalog section of SJS Quality Management.

**Catalog scope (current state at v5.5 build):**

| SOP Number | Title | Revision | Effective | Ratification Status | Skill-side Mirror | Next Review Due |
|---|---|---|---|---|---|---|
| SKN-OPS-001 | CAPA Procedure | 1.0 | 2024-06-30 | Ratified | capa-coordinator/references/skn-ops-001.md | 2026-06-30 |
| SKN-OPS-002 | SAE Procedure | 1.0 | 2024-06-30 | Ratified | (none) | 2026-06-30 |
| SKN-OPS-003 | Recall Procedure | 1.0 | 2024-06-30 | Ratified | (none) | 2026-06-30 |
| SKN-OPS-004 | Customer Complaint Handling | 1.0 | 2024-06-30 | Ratified | (none) | 2026-06-30 |
| SKN-OPS-005 | Non-Conformance Report (NCR) Procedure | 1.0 | 2026-05-09 | Ratified | capa-coordinator/references/ncr-procedure.md | 2027-05-09 |
| SKN-OPS-006 | Lab Quality Procedure | 1.0 | 2026-05-08 | Ratified | quality-lab-coordinator/references/lab-procedure.md | 2027-05-08 |
| SKN-OPS-007 | Batch Lifecycle Procedure | 1.0 | 2026-05-08 | Ratified | batch-lifecycle-tracker/references/batch-lifecycle-procedure.md | 2027-05-08 |
| SKN-OPS-008 | IL / Claims / Label Procedure | 1.0 | 2026-05-09 | Ratified | claims-il-and-label-keeper/references/il-claims-label-procedure.md | 2027-05-09 |
| SKN-OPS-009 | Reportable Events Procedure | 1.0 | 2026-05-09 | Ratified | adverse-event-and-recall-reporter/references/reportable-events-procedure.md | 2027-05-09 |

- *Trigger:* "current revision of SKN-OPS-XXX", "what SOPs are pending ratification", "SOP catalog", "what's the latest on [SOP]", auto-pinned task lives in SOP Catalog section
- *Action:* Read the catalog. Sub-skill queries return the current revision + skill-side mirror path. Pending ratification queries surface the in-flight drafts and their queue position.
- *HITL:* none for reads.

**Ratification queue (Job 1b):**

The `[SOP Revision Pending — quality-manager]` task queue lives in SJS Quality Management Inbound Staging. Queue is empty as of 2026-05-09 — all in-flight ratifications closed. Future entries arrive as sub-skills draft new procedures or surface SOP gaps.

For each task in the queue: read the proposed text, route to QA Lead for review, capture revision history, publish to SharePoint master, update the catalog.

- *Trigger:* `[SOP Revision Pending — quality-manager]` task lands; "ratify [procedure name]"; "approve the [procedure] draft"
- *Action:* Walk `references/sop-catalog.md` §3 ratification protocol. Stage QA Lead review. On approval: assign Rev number, set effective date, write SharePoint master via the user (manual step — SharePoint MCP is read-only), update catalog row, comment-back on the originating sub-skill's task.
- *HITL:* **QA Lead approves every ratification.** Gate set on the ratification task itself.

### 2. Cross-skill state rollup (Job 2)

The dashboard surface. Reads each sub-skill's Asana surface plus PLM batch state, composes the System B rollup, posts as Asana project status, returns on-demand summary.

**Weekly project status update:**

- Posted as Asana project status on SJS Quality Management every Monday at 9am PT (via the `schedule` skill).
- Format: RAG color, summary, next steps, blockers.
- Sources:
  - capa-coordinator → SJS CAPA Log (counts by Status, Pending QA Lead gates open, overdue actions)
  - complaint-and-event-handler → SJ Skin Complaint Log (open complaints by category, trends crossing threshold, SAE or recall flags)
  - quality-lab-coordinator → SJS Quality Management Lab Findings sections (open OOS/OOT, vendor flags pending, scorecard signals posted)
  - batch-lifecycle-tracker → SJS Quality Management Batch sections (active batches, holds, releases pending, near-expiry calls)
  - QoS aggregation → see Job 3
  - Pending ratifications → see Job 1
- Composition: aggregate counts + the 3-5 highest-priority items operator should know about.

**On-demand summary:**

- Triggers: "what's open in quality", "quality dashboard", "monthly quality summary", "where are we on quality"
- Output: text summary in chat, optionally posted as a comment on a specified task
- Read-only.

- *Trigger:* weekly schedule (Monday 9am PT); on-demand phrases above
- *Action:* Pull state from each sub-skill via Asana direct read. Compose rollup. Post or return.
- *HITL:* none.

### 3. Quality-of-service aggregation (Job 3)

Pulls fulfillment quality signal from oc3pl-order-manager and surfaces it in the rollup. Threshold-crossing signals open `[QoS Threshold Crossed]` tasks in the QoS Signal section.

**Sources (read via oc3pl-order-manager):**

- OC3PL Order Management Asana project → 📋 Daily Report Log section — pull latest task for: On-Time Delivery Rate, Fulfillment Rate, Avg Ship Time
- SJ Shipping Dashboard (gid `1206266539116267`) — pull counts of: Errors, Order Exceptions, Returns, RTS over rolling 30 days
- complaint-and-event-handler → SJ Skin Complaint Log filtered to fulfillment-related complaint categories — pull rolling 30 days

**Default thresholds (per `references/qos-thresholds.md`):**

| Metric | Threshold | Action |
|---|---|---|
| On-Time Delivery Rate | < 95% (rolling 7 days) | Open `[QoS Threshold Crossed] On-Time` task |
| Fulfillment Rate | < 99% (rolling 7 days) | Open `[QoS Threshold Crossed] Fulfillment` task |
| Damage rate (returns + RTS attributed to damage) | > 0.5% of orders shipped (rolling 30 days) | Open `[QoS Threshold Crossed] Damage` task |
| Missing/incorrect rate | > 1% of orders shipped (rolling 30 days) | Open `[QoS Threshold Crossed] Missing` task |
| Fulfillment-related complaint trend | > 3% of orders shipped (rolling 30 days) | Open `[QoS Threshold Crossed] Complaint` task |

- *Trigger:* weekly rollup (Job 2 fires this); "shipping quality this week"; "QoS rollup"; "what's the fulfillment quality"; auto-fire on threshold detection during rollup
- *Action:* Read the metrics. Compare against thresholds. Surface in the rollup. For threshold-crossings: stage a `[QoS Threshold Crossed]` task per Job 4 cross-cutting task pattern.
- *HITL:* QA Lead approves any QoS-threshold task creation. Read of the metrics is gateless.

### 4. Cross-cutting task creation (Job 4)

The skill creates tasks that don't fit any single sub-skill. Five task types per `references/cross-cutting-tasks.md`:

| Type | Trigger | HITL |
|---|---|---|
| SOP Annual Review | Auto on next-review-due date from §1 catalog | Operator stages, QA Lead approves on creation |
| Audit Prep | Operator-direct ("audit prep for [retailer]"); auto on retailer audit calendar (read from Outlook) | Operator stages, QA Lead approves |
| Retailer Quality Questionnaire | Operator-direct ("retailer questionnaire from [retailer]"); auto on outlook-asana-bridge inbound flagged | Operator stages, QA Lead approves |
| Regulatory Inspection Prep | Operator-direct ("regulatory inspection prep for [authority]"); auto on regulatory-manager inbound (System C live) | Operator stages, QA Lead approves; coordinates with sjs-regulatory-system for the regulatory side |
| Quality System Review | Quarterly schedule | Operator stages, QA Lead approves |

Plus the `[QoS Threshold Crossed]` tasks from Job 3 are a sixth type with QA Lead approval on creation.

- *Trigger:* phrases above; auto-fires on calendar dates and inbound bridges
- *Action:* Compose task description per the template in `references/cross-cutting-tasks.md`. Stage in Cross-cutting Tasks section.
- *HITL:* **QA Lead approves every cross-cutting task creation.** Gate = Pending QA Lead at stage; snaps to Open on approval.

### 5. SOP annual review (Job 5)

Auto-fires on the next-review-due date from the catalog. Drafts a review task with the SOP's current revision attached, walks the §7 review checklist, and either marks the SOP reviewed-no-change (extends next-review-due by 1 year) or routes to ratification queue (Job 1b) with proposed revisions.

- *Trigger:* auto on next-review-due date; "SOP annual review for [SOP]"; "any SOPs due for review"
- *Action:* Compose review task. Walk §7 checklist (still in scope, still accurate, role-holders current, in line with current operations, no in-flight CAPAs flagging gaps in this SOP). Draft outcome.
- *HITL:* **QA Lead approves the review outcome.** If reviewed-no-change: catalog update only. If revision proposed: routes to Job 1b ratification queue.

### 6. Weekly digest composition (Job 6)

Named wrapper around the Job 2 rollup logic. Returns the weekly digest payload defined in `references/cadence-composition-spec.md` §1 on a stable contract so cadence callers (the `sjs-quality-weekly-digest` scheduled task and `quality-status-reporter`) consume the same data shape every run.

This is a wrapper, not a divergent path. Future changes to Job 2's sourcing or composition propagate to Job 6 by definition — if the two ever drift, Job 6 is wrong.

**Sources (same as Job 2):**
- capa-coordinator → CAPA + NCR state, Pending QA Lead gates
- complaint-and-event-handler → open complaints, trend-break flags, SAE/recall counts
- quality-lab-coordinator → open OOS/OOT, vendor flags pending, scorecard signals
- batch-lifecycle-tracker → active batches, holds, near-expiry, stability tests due
- Job 3 QoS aggregation → metrics + thresholds crossed
- Job 1 catalog → SOPs pending ratification, SOPs due for review within 30 days

- *Trigger:* `sjs-quality-weekly-digest` scheduled task; on-demand "compose weekly quality digest"
- *Action:* Pull state from each source. Compose the §1 payload. Return to caller.
- *HITL:* none — read-only composition.

### 7. Monthly operational rollup (Job 7)

Net new. Produces current-month vs. prior-month operational metrics with signed deltas and trend direction for the Monthly tab on `quality-dashboard.html`. Operational only — no cost rollup, no `vendor_invoices` query (regulatory cost rollup is regulatory-manager Jobs 8 and 9).

Trend direction uses a 5% deadband: `delta / max(abs(prior), 1) * 100`. If absolute value ≤ 5%, trend = `flat`. Otherwise `up` or `down` based on sign. Lower-is-better metrics (complaints, OOS, OOT, holds) keep raw directional trend; narrative composition flips interpretation.

On first cadence run with no prior-period data: count metrics default to 0, percentage/QoS fields stay `null`, delta computed from `current − prior`, trend forced to `flat`. No special first-run branch downstream.

Narratives (`what_drove_the_month`, `notable_signals`, `watch_items_for_next_month`) are 1–3 sentences each, composed from the month's highest-priority items. Operator can override before push.

- *Trigger:* `sjs-quality-monthly-snapshot` scheduled task (first business day of month — rolls up the prior calendar month); on-demand "compose monthly quality rollup"
- *Action:* Compute current + prior month metrics per `references/cadence-composition-spec.md` §2. Compute deltas + trend per the deadband rule. Compose narratives. Return payload to caller.
- *HITL:* none — read-only composition.

### 8. Quarterly operational rollup (Job 8)

Net new. Same metric set as Job 7 over a quarterly window, plus quarterly-only fields (SOP annual review cycle progress, audits completed/planned, retailer questionnaire activity, regulatory inspections) and four narratives — including `founder_signal_for_ayesha_briefing`, a 1–2 sentence pull-out for the Ayesha weekly briefing source pool (empty string if no founder-level signal surfaced).

Operational only — no cost rollup, no handoff to `vendor_invoices`.

Stages two draft handoff comments per `references/cadence-composition-spec.md` §3:
- `sjs-status-reporter` running log
- `ayesha-weekly-briefing` source pool

Both stay in draft state until the Operator approves. They post only on explicit approval.

Same first-run-with-no-priors behavior as Job 7 (counts → 0, percentages → null, trend → flat).

- *Trigger:* `sjs-quality-quarterly-rollup` scheduled task (first business day of Jan/Apr/Jul/Oct — rolls up the prior calendar quarter); on-demand "compose quarterly quality rollup"
- *Action:* Compute quarterly metrics + variance per §3. Compose quarterly-only fields and narratives. Stage the two handoff comments in draft state. Return payload to caller.
- *HITL:* **Operator approves the two handoff comments before they post.** No gate on the composition itself.

## Asana surface

- *Project:* **SJS Quality Management** (gid `1214660401644163`) — owned by quality-manager at v5.6. Operations team. Public to workspace.

### Sections (cached 2026-05-09)

| Section | GID | Origin |
|---|---|---|
| Inbound Staging | `1214660401653157` | v5.3 |
| Lab Findings Open | `1214660713569696` | v5.3 |
| Vendor Flag Review | `1214661413440412` | v5.3 |
| Scorecard Signal Posted | `1214660194909535` | v5.3 |
| CAPA Handed Off | `1214660401653221` | v5.3 |
| Watch List | `1214660713569760` | v5.3 |
| Closed | `1214660716447873` | v5.3 |
| Batch — Active in Market | `1214660393603698` | v5.4 |
| Batch — Stability Schedule | `1214660393603699` | v5.4 |
| Batch — Hold/Release Review | `1214660393603700` | v5.4 |
| Batch — On Hold | `1214660700812912` | v5.4 |
| Batch — Watch | `1214660700812911` | v5.4 |
| Batch — Closed (Released, Expired, Pulled) | `1214660700812913` | v5.4 |
| Cross-cutting Tasks | `1214660700812914` | v5.5 — Job 4 task home |
| SOP Catalog | `1214660700812917` | v5.5 — pinned catalog task lives here |
| QoS Signal | `1214660700812918` | v5.5 — Job 3 threshold-crossed tasks |

### Custom fields (cached 2026-05-09)

All fields exist on SJS Quality Management. Canonical GID + option-GID reference: `/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md`. New v5.5 fields below; v5.3/v5.4 fields reused.

**New for v5.5:**
- `Cross-cutting Type` (single-select: SOP Annual Review, Audit Prep, Retailer Questionnaire, Regulatory Inspection, Quality System Review, QoS Threshold Crossed, Other)
- `SOP Reference` (text — `SKN-OPS-NNN` pointing to a catalog entry)
- `QoS Metric` (single-select: On-time delivery, Fulfillment, Damage, Missing/incorrect, Complaint trend, Other)
- `Threshold Crossed` (text — actual value vs threshold)
- `Catalog Status` (single-select: Ratified, Pending ratification, Under annual review, Working draft) — used on SOP Catalog tasks

**Reused fields:** `Status`, `Gate`, `Severity`, `Closeout Summary`, `Linked CAPA`.

### Title prefixes

- **Inbound staging from sub-skills:** `[SOP Revision Pending — quality-manager]` (already in use from v5.2-v5.4)
- **Outbound to regulatory-manager:** `[Reg Flag Pending — regulatory-manager]` for cross-cutting work that surfaces a regulatory question. regulatory-manager Job 1 picks up and fans out to the right System C sub-skill.

## Role map

The skill reads role-holders from `references/role-map.md`. **This is the canonical role-map for System B.** Sub-skill role-maps reference this one at runtime.

## Calls and integrations

quality-manager is read-most. Most calls are reads against sub-skill Asana surfaces and oc3pl-order-manager.

**Reads via:**
- capa-coordinator (Asana SJS CAPA Log) — CAPA + NCR state, Pending QA Lead gates, SOP gap signals
- complaint-and-event-handler (Asana SJ Skin Complaint Log gid `1204763097184846`) — open complaints, trends, SAE/recall flags
- quality-lab-coordinator (Asana SJS Quality Management Lab Findings sections) — open LFs, vendor flags, scorecard signals
- batch-lifecycle-tracker (Asana SJS Quality Management Batch sections) — active batches, holds, releases, near-expiry decisions
- oc3pl-order-manager (Asana OC3PL Order Management → 📋 Daily Report Log; SJ Shipping Dashboard gid `1206266539116267`) — QoS metrics
- plm-assistant — batch context, SKU context for cross-cutting tasks (audit prep, retailer questionnaires)
- SharePoint — SOP master copies (read-only via MCP at v5.6; ratification publish is manual)
- outlook-asana-bridge — inbound retailer questionnaires, regulatory inspection notices
- fireflies-asana-bridge — QBR transcripts where quality work gets called out
- Asana — direct read of SJS Quality Management

**Writes via:**
- Asana — direct (project status updates, cross-cutting tasks, SOP catalog updates, QoS threshold tasks)
- SharePoint — SOP master publish is currently manual (read-only MCP); the skill drafts the .docx via local script and surfaces for the user to drag into SharePoint

**Called by:**
- quality-status-reporter (v5.6) — reads this skill's rollup as primary input for branded reports
- ac-brands-quality-system (v5.7) — the System B router routes any quality intent here when ambiguous

**Never duplicates:**
- capa-coordinator (owns CAPA + NCR; this skill surfaces but doesn't open)
- complaint-and-event-handler (owns customer signal; this skill surfaces but doesn't intake)
- quality-lab-coordinator (owns lab classification; this skill surfaces but doesn't classify)
- batch-lifecycle-tracker (owns batch state; this skill surfaces but doesn't decide)
- oc3pl-order-manager (owns fulfillment data; this skill aggregates the metrics)
- plm-assistant (only writer to PLM)
- quality-status-reporter (owns branded output; this skill produces rollup data only)

## Out of scope (v5.6)

- Sub-skill task creation (each sub-skill owns its own intake)
- SOP authoring (sub-skills draft procedures; this skill owns the ratification cycle, not the drafting)
- Branded report generation — quality-status-reporter at v5.6
- Cross-system router (PD ↔ Quality ↔ Regulatory) — ac-brands-quality-system at v5.7 + System A peers + pending System C
- Regulatory reportability assessment — adverse-event-and-recall-reporter (System C, live)
- SharePoint master publish (currently manual; SharePoint MCP is read-only)
- Direct PLM writes — plm-assistant
- Cross-brand quality coordination (Sweet July Skin only at v5.6)

## First-run setup

SJS Quality Management exists (gid `1214660401644163`); all 16 sections cached above; all 20 custom fields cached as of 2026-05-09. On first invocation:

1. Confirm the project responds and section + field GIDs match what Asana returns.
2. Confirm `references/role-map.md` is current. Sub-skill role-maps reference this canonical role-map.
3. Confirm OC3PL Order Management Asana project and SJ Shipping Dashboard (gid `1206266539116267`) are reachable for QoS pulls.
4. Confirm SOP Catalog pinned task (gid `1214661441506629`) is in the SOP Catalog section and pinned.
5. Confirm the weekly Monday 9am PT project status update is scheduled via the `schedule` skill (deferred — register on first run if not already).
6. Confirm SJS Quality Management is in the Operations Dashboard portfolio (gid `1208174221370391`) — manual UI step at v5.6 build.

If any check fails, surface to the operator and stop — the skill does not modify project structure unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/sop-catalog.md` — canonical SOP catalog + ratification protocol + annual review checklist
- `references/cross-cutting-tasks.md` — templates for the 5 cross-cutting task types (audit prep, retailer questionnaire, regulatory inspection prep, quality system review, SOP annual review) plus QoS threshold task
- `references/qos-thresholds.md` — QoS metric definitions + threshold defaults + source-field mappings
- `references/cadence-composition-spec.md` — payload contract for Jobs 6, 7, 8 (weekly digest, monthly rollup, quarterly rollup)
- `references/trigger-phrases.md` — grouped triggers by intent
- `references/role-map.md` — canonical role-map for System B (Operator, QA Lead, Voice of Customer)

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant pages from `public.wiki_pages`. Wiki pages are synthesized quality briefings that compound as bridge skills process emails, meetings, and lab traffic. Reading them first gives this skill institutional memory about vendor scorecards, batch patterns, and complaint history without re-scanning raw sources.

### Which pages to read

- Named supplier → `'supplier/' || public.wiki_slugify(vendor_name)`
- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`

Supplier pages carry vendor scorecard signals, open quality flags, and OOS/OOT history. SKU pages carry complaint history, batch patterns, stability status, and known issues.

### Read query

```sql
-- Single supplier or SKU by slug (preferred for named entities — full-text search drops short acronyms)
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));

SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'sku/' || public.wiki_slugify('{sku_code_or_product_name}'));

-- Content-term sweep (e.g. "stability", "OOS", "complaint pattern")
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_page_type => 'sku', p_query => '{term}', p_limit => 3);
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before generating its response. Treat it as a pre-synthesized briefing on the supplier or SKU at hand.

### Write-back (stale pages only)

If a page is stale or `source_count = 0` and live queries produced genuine new quality signal not already in the wiki, update the page:

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
