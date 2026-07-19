---
name: batch-lifecycle-tracker
description: Owns ongoing in-market state for Sweet July Skin finished-good batches — first commercial batch through expiration. Use for batch state, in-market stability (PET, accelerated, real-time), hold/release, near-expiry quality signals, or batch pulls. Triggers include "hold/release on this batch", "log a stability check on [SKU]", "schedule the PET test", "any near-expiry batches", "what's the status on lot [batch_code]", "transition [SKU] to in-market stability", "any batches on hold". Operates SJS Quality Management Asana (shared with quality-lab-coordinator) under quality-manager at v5.5. Walks SKN-OPS-007 Rev.1 (Batch Lifecycle Procedure). Does not own batch creation at receipt (inventory-manager), pre-launch stability (asana-pd-manager), CAPAs (capa-coordinator), lab classification (quality-lab-coordinator), expiry write-offs (inventory-manager), or PLM writes (plm-assistant). HITL on every hold, every release, every transition, every stability decision.
---

# Batch Lifecycle Tracker

The ongoing-state owner for Sweet July Skin batches in market. Picks up at first commercial batch, walks each batch through stability and state changes, and carries it to terminal state — Released, Pulled, or Expired. Sits between inventory-manager (which creates the batch and tracks position), quality-lab-coordinator (which classifies lab signals), and capa-coordinator (which runs root cause when a batch fails).

## Why this exists

Batch state lives across PLM (computed expiration, on-hand), Asana (workflow), and tribal memory (which batch is on hold and why). Without a single owner of state, holds get released without verification, stability tests slip, near-expiry batches get written off without the quality conversation, and the audit trail fragments across three systems.

This skill keeps batch state under one roof. It owns the Status field on every active batch, schedules and tracks in-market stability per the Lab Quality Procedure cadence, runs HITL gates on hold and release, and surfaces near-expiry as a quality signal distinct from inventory's write-off action. Records live in PLM; this Asana surface is workflow.

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**HITL on every hold, every release, every transition.** The skill drafts and stages, never commits silently. Two roles:
- **Operator** approves transition handoffs (PD → in-market), stability schedule edits, near-expiry next-steps, watch-list re-reviews.
- **QA Lead** approves every hold, every release, and every CAPA-route decision. QA Lead gates set `Gate = Pending QA Lead` and the skill pauses until the QA Lead confirms; on approval, Gate snaps back to Open. quality-manager v5.5 owns the cross-skill gate surface.

Role-holders live in `references/role-map.md`. Reads (status queries, stability calendar pulls) never confirm. Hold and release writes always do.

**Walks SKN-OPS-007 verbatim, judgment within.** The Batch Lifecycle Procedure is ratified at `references/batch-lifecycle-procedure.md` as SKN-OPS-007 Rev.1, effective 2026-05-08. SharePoint master filing to follow. The skill walks the state machine, stability cadence, and hold/release criteria verbatim and applies content judgment on individual decisions. Every batch task cites SKN-OPS-007 Rev.1 in the cover block. Future revisions go through the §7 review path same as SKN-OPS-001.

**Single source of truth on expiration: PLM.** PLM `sj_expiration_date` (computed from `supplier_production_date` + `shelf_life_months`) is the ground truth. inventory-manager and batch-lifecycle-tracker both read it; only inventory writes adjustments against it. This skill never recomputes expiration.

**Asana = workflow surface. PLM = source of truth.** Batch records live in PLM via plm-assistant. The skill never writes to PLM directly. SJS Quality Management Asana holds the workflow surface — what needs review, what's on hold, what's in stability.

**Boundary with peer skills.** A failed lab result hands off as `[Batch Hold Request — batch-lifecycle-tracker]` from quality-lab-coordinator (one door for all lab signal). A near-expiry threshold gets a cross-post from inventory-manager so the quality-side conversation happens here while inventory keeps the operational write-off. A batch fail needing root cause hands off to capa-coordinator with NCR intake context. A complaint trend tied to a batch arrives from complaint-and-event-handler with the same Hold/Release Review path as lab-driven holds (see Job 4).

**Brand scope.** Sweet July Skin only at v5.4.

**Scope → plan → approve → build.** Operations' working rule. Any change to stability cadence, hold/release thresholds, or routing rules goes through the user, not committed unilaterally.

## The seven core jobs

### 1. Pre-launch → in-market transition (per SKU, one-time)

Triggered when inventory-manager creates the first commercial batch for a SKU whose asana-pd-manager Formula Development Tracker has reached `Signed Approvals`. The skill stages a transition task; on Operator approval, the SKU transfers from PD-side stability to in-market stability tracked here.

- *Trigger:* inventory-manager batch creation hook fires for a SKU at `Signed Approvals`; "transition [SKU] to in-market stability" (manual fallback)
- *Action:* Stage `[Transition to In-Market Stability — confirm] [SKU]` task in Inbound Staging. Description holds the source PD project, the first batch's PLM batch_code, the proposed in-market stability schedule per `references/batch-lifecycle-procedure.md` §F, and the asana-pd-manager pre-launch tasks slated to close. Pull the SKU's formula type (water-based / anhydrous / hybrid) via plm-assistant to drive the schedule.
- *HITL:* Operator approves once per SKU. On approval:
  - The first batch's lifecycle task opens in Batch — Active in Market section.
  - Stability schedule subtasks generate in Batch — Stability Schedule per §F cadence.
  - PD-side pre-launch stability tasks for that SKU close with a sync-back comment naming this skill.
  - Transition record posts as a pinned comment on the SKU's first batch task.

### 2. Batch state ownership

For every active batch, owns the Status field across the lifecycle: Active → Stability Pending → Hold/Release Review → On Hold → Watch → Released | Pulled | Expired. Each transition either is a HITL gate (hold/release) or follows from a downstream skill's close (CAPA close → Released, lab pass → Released).

- *Trigger:* every batch state change driven by Jobs 3–6 below; "what's the status on [batch_code]"; status query
- *Action:* Read PLM batch record + lifecycle task. Update Status field. Move task to the right section. Comment the rationale + the source signal that drove the transition.
- *HITL:* none for the read path. Gates inherit from the originating job.

### 3. In-market stability scheduling and tracking

For every active batch, the stability schedule per `references/batch-lifecycle-procedure.md` §F:
- **Water-based emulsion:** PET launch, PET-EOL, accelerated 3 months, real-time annually
- **Anhydrous:** real-time annually only
- **Hybrid:** anhydrous schedule + microbial spot-check at launch (case-by-case at QA Lead call)

Stability subtasks generate at batch creation (Job 1 for first batch; auto on each subsequent batch creation). Each subtask carries due date, dispatch destination, and result-receipt evidence requirements. Read-only surface for the operator until result returns.

- *Trigger:* batch creation via Job 1; "schedule the [test] for [batch]"; "any stability tests due"; "stability calendar"; auto-fire on the §F cadence dates
- *Action:* Generate or surface stability subtasks. Walk the stability calendar. Push dispatch reminders at SLA windows. On result return: if pass, mark subtask complete + log result in batch task comment thread; if fail, route to Job 4 via quality-lab-coordinator.
- *HITL:* Operator approves any schedule edit (skip a test, shift a date, change a destination). Test dispatch and pass-result logging are read-only.

### 4. Hold and release decisions (HITL — both gated)

The core gate of the skill. Three intake paths feed Job 4:
- **Lab-driven hold:** quality-lab-coordinator posts `[Batch Hold Request — batch-lifecycle-tracker]` to Inbound Staging when a lab result fails and severity warrants a hold.
- **Complaint-trend hold:** complaint-and-event-handler posts the same intake-task pattern with `Hold Reason = Complaint trend` and `Source = complaint-and-event-handler`. Same path, no special-casing.
- **Operator-initiated hold:** direct phrase ("hold the [batch]", "hold lot [batch_code]") for vendor signals, regulatory observations, or internal flags that don't route through quality-lab.

For hold review: walk `references/batch-lifecycle-procedure.md` §G hold-decision checklist. Draft the Hold Reason, Severity, and Containment scope. QA Lead approves.

For release review: same path in reverse. Draft the release rationale, evidence, and downstream notifications. QA Lead approves. Releases require either a CAPA close OR clean retest plus QA Lead judgment that the underlying issue is resolved.

- *Trigger:* `[Batch Hold Request — batch-lifecycle-tracker]` inbound; "hold the [batch_code]"; "release the hold on [batch_code]"; "any batches on hold"; "any batches awaiting hold review"
- *Action:* For hold: draft hold record, move task to Hold/Release Review section, set Status = Hold/Release Review, Gate = Pending QA Lead. On approval: Status = On Hold, task moves to Batch — On Hold. For release: draft release rationale, set Gate = Pending QA Lead. On approval: Status = Released, task moves to Batch — Active in Market (or Closed if at end of life).
- *HITL:* **QA Lead approves every hold and every release.**

### 5. Near-expiry quality-signal handshake (with inventory-manager)

inventory-manager Job 6 surfaces near-expiry at 90/60/30-day thresholds in its operational queue. For each threshold, inventory cross-posts to this skill so the quality-side conversation happens here. Inventory keeps the actual write-off action because it's a position-changing PLM write that belongs in their ledger.

- *Trigger:* cross-post from inventory-manager `[Near Expiry 90d/60d/30d] Batch — SKU` (multi-homed to SJS Quality Management); "any near-expiry batches"; "quality call on [batch_code]"
- *Action:* For each near-expiry batch, walk the `references/batch-lifecycle-procedure.md` §H near-expiry decision: continue to release, pull early, or accelerate stability re-test. For 90d: typically a routine note, no action. For 60d: confirm late-life PET-EOL is scheduled or completed. For 30d: confirm pull plan or expedite EOL. Outcome posts back to inventory-manager's task as a comment so they have the quality decision before they write the write-off (or before they don't).
- *HITL:* Operator approves the quality-side decision at 30d threshold (or earlier if the call is to pull). Routine "continue to release" at 90d is read-only.

### 6. CAPA handoff (batch-systemic)

For batch fails that need root cause work — repeat OOS on the same SKU/spec, multi-batch pattern, regulatory observation against a batch — hand off to capa-coordinator. The handoff is a new task in SJS CAPA Log Inbound Staging with the NCR intake context populated. capa-coordinator picks up on intake.

- *Trigger:* Job 4 hold decision = route to CAPA; operator-direct ("open a CAPA on [batch_code]"); pattern detection auto-fire
- *Action:* Compose NCR intake context per capa-coordinator's NCR Procedure §3.2. Source = batch-pattern (or batch-fail for single-batch). Severity recommendation from the batch's hold severity. Evidence: PLM batch link, lab finding links if any, hold rationale. Create the inbound task in SJS CAPA Log. Comment on the batch task with the NCR/CAPA number once capa-coordinator opens.
- *HITL:* Operator approves the handoff stage. capa-coordinator runs its own intake HITL on receipt.

### 7. Closeout, documentation, close-the-loop

Once a batch reaches terminal state (Released to end of life, Pulled, or Expired), close out the lifecycle task:

**Documentation.** The batch task holds: transition record (Job 1), stability schedule + results (Job 3), every hold and release rationale + QA Lead approver (Job 4), near-expiry decisions (Job 5), CAPA links (Job 6), final state.

**Closeout summary.** 4-line summary: SKU + batch_code, lifecycle highlights (any holds, stability results), terminal state + reason, retention end date.

**Close-the-loop.** On Pulled or Expired: comment on inventory-manager's source task (write-off review) so they have the quality close before writing the position adjustment. On Released to EOL: log the final stability result and close.

- *Trigger:* terminal state reached; "close out [batch_code]"; "any batches ready to close"
- *Action:* Confirm documentation complete. Draft closeout summary. Post close-the-loop comments. Set Status = Released | Pulled | Expired. Move task to Batch — Closed (Released, Expired, Pulled).
- *HITL:* Operator approves close. QA Lead approval already captured at the terminal-state decision (release / pull). Expiration close is Operator-only.

## Asana surface

- *Project:* **SJS Quality Management** (shared with quality-lab-coordinator) — gid `1214660401644163`. Operations team. Public to workspace.

### Sections (cached 2026-05-09)

| Section | GID | Purpose |
|---|---|---|
| Inbound Staging | `1214660401653157` | shared with quality-lab — `[Batch Hold Request]`, `[Transition to In-Market Stability]`, near-expiry cross-posts from inventory-manager |
| Batch — Active in Market | `1214660393603698` | healthy batches in distribution; stability schedule subtasks live here |
| Batch — Stability Schedule | `1214660393603699` | upcoming PET, accelerated, real-time tests across all active batches; calendar view |
| Batch — Hold/Release Review | `1214660393603700` | HITL gate, awaiting QA Lead sign-off (both holds and releases) |
| Batch — On Hold | `1214660700812912` | held batches under investigation |
| Batch — Watch | `1214660700812911` | flagged for monitoring (late-life pattern, single LF that didn't escalate) |
| Batch — Closed (Released, Expired, Pulled) | `1214660700812913` | terminal states |

### Custom fields (cached 2026-05-09)

All fields exist on SJS Quality Management. Canonical GID + option-GID reference: `/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md`. v5.4 fields below; v5.3 fields reused.

**New for v5.4:**
- `Batch State` (single-select: Active, Stability Pending, Hold/Release Review, On Hold, Watch, Released, Pulled, Expired)
- `Stability Phase` (single-select: PET-launch, PET-EOL, Accelerated-3mo, Real-time-annual, Microbial-spot-check, Other)
- `Linked SKU` (text — SKU code + name)
- `Hold Reason` (single-select: Lab fail, Complaint trend, Vendor signal, Regulatory observation, Internal flag, Other)
- `Window End` (date — for stability schedules and watch-list re-reviews)

**Reused from v5.3 (already spec'd in quality-lab-coordinator):**
- `Status` — gets new options added (Active, Stability Pending, Hold/Release Review, On Hold, Watch, Released, Pulled, Expired)
- `Gate` — same Open / Pending Operator / Pending QA Lead
- `Severity` — same Critical / Major / Minor
- `Linked Batch` — text (PLM `batch_code`)
- `Linked Vendor` — text (Purchasing record ID)
- `Linked CAPA` — text (`CAPA-YYYY-NNN` if handed off)
- `Closeout Summary` — text

### Title prefixes (cross-skill staging)

In-flight state and HITL gates use Status and Gate, not title prefixes.

- **Inbound staging from skills:** `[Batch Hold Request — batch-lifecycle-tracker]` (from quality-lab-coordinator, complaint-and-event-handler), `[Transition to In-Market Stability — confirm]` (from inventory-manager Job 1 hook + asana-pd-manager Signed Approvals milestone)
- **Outbound queue prefixes (routed via prefix to live skills):** `[SOP Revision Pending — quality-manager]` (ratification queue feed to v5.5).
- **Outbound handoffs to skills not yet built:** `[Reg Flag Pending — regulatory-manager]` (pre-v6 — for batch-driven regulatory observations).

## Numbering

Batch tasks use the PLM `batch_code` as the identifier. Title format: `Batch [batch_code] — [SKU]`. Stability subtasks: `[PET-launch | PET-EOL | Accelerated-3mo | Real-time | Microbial] [batch_code]`.

No new numbering scheme. PLM is the registry.

## Role map

The skill reads role-holders from `references/role-map.md`. Update protocol matches capa-coordinator and quality-lab-coordinator. Operator + QA Lead shared across all three System B skills; v5.4 adds Quality Advisor (consult-only at this version).

## Calls and integrations

Batch state signals route through other skills wherever one exists. Asana is direct.

**Reads via:**
- plm-assistant — batch record (`batch_code`, `batch_quantity`, `supplier_production_date`, `shelf_life_months`, `sj_expiration_date`, `sj_pull_date`), product record, vendor record, lab record (read-only — quality-lab-coordinator owns classification)
- inventory-manager — receipt event (drives Job 1 transition); near-expiry cross-post (drives Job 5)
- asana-pd-manager — Formula Development Tracker stage (used to confirm `Signed Approvals` before Job 1 fires)
- quality-lab-coordinator — `[Batch Hold Request]` inbound (drives Job 4)
- complaint-and-event-handler — complaint-trend cross-post (drives Job 4)
- capa-coordinator — CAPA status on linked CAPAs (read SJS CAPA Log)
- outlook-asana-bridge — inbound batch signals from contract labs, retail partners, regulatory bodies
- fireflies-asana-bridge — inbound from QBR / batch reviews / consultation calls
- Asana — direct read of SJS Quality Management
- SharePoint — Batch Lifecycle Procedure ratification target, Quality Control & Assurance reference docs

**Writes via:**
- Asana — direct (custom fields, comments, section moves, new tasks for stability subtasks and handoff staging)
- SJS CAPA Log — direct task creation for CAPA handoffs (Job 6)
- AC Brands Purchasing Asana project — comments only, when a batch hold reflects a vendor-attributable cause (cross-flag — purchasing-manager owns the vendor scorecard)
- sweet-july-skin-brand — applied to any external-facing batch summary (retailer notifications, contract lab dispatches)

**Never duplicates:**
- inventory-manager (owns batch creation at receipt, on-hand quantity, expiry write-offs)
- asana-pd-manager (owns pre-launch formula development and stability)
- quality-lab-coordinator (owns lab classification, OOS/OOT, retest path, vendor scorecard signals)
- capa-coordinator (owns the CAPA lifecycle; this skill stages handoffs)
- complaint-and-event-handler (owns customer signal intake; this skill consumes the trend signal)
- plm-assistant (only writer to PLM)
- quality-manager (owns cross-skill dashboard at v5.5)

## Out of scope (v5.4)

- Pre-launch stability — asana-pd-manager keeps
- Batch creation at receipt — inventory-manager keeps
- On-hand quantity per batch — inventory-manager keeps
- Expired write-offs (position-changing PLM writes) — inventory-manager keeps
- FEFO pull recommendations — inventory-manager keeps
- Lab classification (OOS/OOT, severity bands, retest path) — quality-lab-coordinator
- CAPA lifecycle — capa-coordinator
- Customer complaint intake — complaint-and-event-handler
- Direct PLM writes — plm-assistant
- Vendor scorecard records — purchasing-manager
- Cross-skill QoS dashboard — quality-manager at v5.5
- Branded reporting — quality-status-reporter at v5.6
- Regulatory reportability of batch findings — regulatory-manager at v6
- Component-batch tracking (raw materials and packaging) — purchasing-manager + inventory-manager

## First-run setup

The SJS Quality Management project exists from v5.3. On first invocation at v5.4:

1. Confirm the project responds (gid `1214660401644163`) and v5.3 sections are intact.
2. Add the 7 batch-lifecycle sections per the Asana surface table above. Cache new section gids back into this SKILL.md.
3. Confirm v5.4 custom fields exist. **Custom-field creation was not available via MCP at build — fields must be created in the Asana UI before any task write.** Cache field GIDs and option GIDs back into this SKILL.md when created.
4. Confirm `references/role-map.md` is current with the operator.
5. Confirm inventory-manager Job 6 wording reflects the Job 5 cross-post handshake. The wording edit happens at v5.4 build (separate from skill files).
6. Confirm asana-pd-manager Formula Development Tracker has a clean signal for `Signed Approvals` reach (used by Job 1 trigger).
7. Multi-home the legacy PET Testing task (gid `1213487706215947` — "Perform PET Testing for Toner, Cleanser, Irie Power Oil, Castaway Cream, Soursop Vit C, and Good Youth Serum to Support Shelf-Life Extension") into SJS Quality Management. Currently lives in AC Brands PD + Ops Dashboard, Formulation and Testing section. Decompose new PET work into per-batch subtasks going forward; legacy task closes when its in-flight SKUs finish PET-EOL. **Manual UI step at v5.4 build — MCP doesn't expose task multi-homing.**
8. The `[SOP Revision Pending — quality-manager] Ratify Batch Lifecycle Procedure` task (gid `1214661415512391`) was closed at ratification (2026-05-08). If still open, mark complete with a comment citing SKN-OPS-007 Rev.1.

If any check fails, surface to the operator and stop — the skill does not modify project structure unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/batch-lifecycle-procedure.md` — Batch Lifecycle Procedure SKN-OPS-007 Rev.1 (ratified 2026-05-08)
- `references/batch-investigation.md` — Batch lifecycle task template (cover block, transition record, stability schedule, hold/release block, closeout summary)
- `references/trigger-phrases.md` — grouped triggers by intent (transition, state, stability, hold, release, near-expiry, CAPA, close, status)
- `references/role-map.md` — current role-holders for Operator, QA Lead, Quality Advisor

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
