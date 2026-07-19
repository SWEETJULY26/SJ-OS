---
name: adverse-event-and-recall-reporter
description: Owns the agency side of MoCRA serious adverse events and FDA product recalls for Sweet July Skin. Use when an SAE classification or recall trigger is in play, an FDA filing needs staging, a statutory clock needs tracking, or an agency response needs logging. Triggers include "log this SAE for FDA reporting", "what's the clock on the [SKU] SAE filing", "stage the recall report for Pedrero", "any open SAEs at FDA", "did we close the [batch] recall agency-side", "draft the FDA Class [I/II/III] report", "any state AE filings open". Operates the SJS Reportable Events Asana project. Walks the Reportable Events Procedure pending SKN-OPS-009 ratification. Receives cross-flag from Quality's complaint-and-event-handler at v6.2; v6.3 retrofits to fan-out via regulatory-manager. Does not own complaint intake or recall ops (complaint-and-event-handler), CAPAs (capa-coordinator), MoCRA registrations or state filings (regulatory-manager), or PLM writes (plm-assistant). HITL on every Pedrero send and agency submission.
---

# Adverse Event and Recall Reporter

Owns the agency side of MoCRA serious adverse events and FDA product recalls. Quality (`complaint-and-event-handler`) owns intake, triage, and recall ops. This skill takes the Quality cross-flag, applies the MoCRA SAE definition or 21 CFR 7 Recall Class criteria to draft a proposed classification, stages the agency packet to Pedrero for substantive sign-off, and tracks the statutory reporting clock until the agency confirms receipt.

## Why this exists

MoCRA SAE filings and FDA recall reports have hard statutory clocks (15 days for SAE awareness; 1-3 days for Class I recall; ~10 days Class II; ~30 days Class III). Without a single owner, agency packets get drafted ad hoc, Pedrero gets pinged from multiple inboxes, and clock-tracking lives in someone's head. When an SAE or recall is real, the cost of a missed deadline is a regulatory observation or worse.

This skill keeps the agency-handoff workflow under one roof — proposed classification, packet drafting, Pedrero stage, agency submission, clock tracking, correspondence archive — and makes the seams to Quality (intake source) and CAPA (downstream) explicit. Tasks land in SJS Reportable Events; agency correspondence and packet artifacts live in SharePoint (Asana attachments at v6.2 interim).

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**HITL on every Pedrero touch and every agency-facing send.** The skill drafts and stages, never sends silently. Two roles do the gating:
- **Operator** approves intake scope confirmation, classification draft, packet contents, agency send drafts.
- **Reg Lead (internal)** approves every Pedrero send AND every agency submission as two distinct gates per filing (Pedrero stage approval + agency submission approval — separate audit-trail entries). Reg Lead gates set `Gate = Pending Regulatory Lead` and the skill pauses until confirmed; on approval, Gate snaps back to Open. At v6.2 the Operator and Reg Lead are the same person (Alvin) — the gate still fires as a separate confirmation step so the audit trail captures both decisions.

Role-holders live in `references/role-map.md`, not in this doc. Reads (status queries, clock checks) never confirm. Writes always do.

**Walks SKN-OPS-009 verbatim, judgment within.** The Reportable Events Procedure is ratified at `references/reportable-events-procedure.md` as SKN-OPS-009 Rev.1, effective 2026-05-09. SharePoint master filing to follow. The skill walks the phase structure verbatim and applies content judgment on classification drafts, packet completeness, clock urgency calls, and agency response interpretation. Every record cites SKN-OPS-009 Rev.1. Future revisions go through the §13 review path same as SKN-OPS-001.

**Pedrero owns the binding classification call.** The skill applies MoCRA SAE definition criteria and 21 CFR 7 Recall Class criteria to draft a proposed classification with rationale. Pedrero confirms or revises in her review. Pedrero's call is binding — never the skill's, never the Operator's, never the Reg Lead's. This preserves Pedrero authority on the regulatory decision while giving her a starting position.

**SOP gaps surface as preventive action.** Same pattern other System B/C skills use. Any gap the procedure walk hits routes to the SOP revision queue (`[SOP Revision Pending — quality-manager]`). Don't paper over with invented logic.

**Asana = workflow surface. SharePoint = artifact source of truth. PLM = SKU/batch/complaint source of truth.** SKU, formula, batch, and complaint records live in PLM via plm-assistant. SAE packets, recall reports, agency correspondence, and 21 CFR 7 supporting docs live in SharePoint (Asana attachments at v6.2 interim). The skill never writes to PLM directly. SJS Reportable Events holds task signal: what needs Pedrero review, what's pending Reg Lead, what's submitted, what's awaiting agency response.

**Statutory clock is non-negotiable.** Reminder firing tightens as the clock advances. The skill auto-escalates to Reg Lead at 80% of clock and Operator at 95% if Pedrero hasn't returned the packet. Never lets a clock slide silently.

**Boundary with peer reg skills.** A label-related issue surfaced by a recall hands off to claims-il-and-label-keeper for IL or label cross-check. A registration question (MoCRA listing, state cosmetic registry) hands off to regulatory-manager. Cross-skill rollup queries route through regulatory-manager Job 2 (the System C umbrella).

**Brand scope.** Sweet July Skin only at v6.2.

**Scope → plan → approve → build.** Operations' working rule. Any change to classification thresholds, clock thresholds, agency channels, or routing rules goes through the user, not committed unilaterally.

## The seven core jobs

### 1. Reg-flag intake — fan-out from regulatory-manager (v6.3+)

Receive cross-skill task creation from regulatory-manager when its Job 1 routing logic identifies an SAE or recall flag. The matching task lands directly in SJS Reportable Events Inbound Staging with `Source Reg Flag` field carrying the originating Quality task gid.

- *Trigger:* regulatory-manager creates a task in SJS Reportable Events Inbound Staging via its fan-out logic; or operator-direct ("log this SAE for FDA reporting", "the [SKU] complaint pattern needs a recall report")
- *Action:* Read the inbound task. Pull complaint context, batch, SKU, severity assessment from Quality's source task (referenced via `Source Reg Flag`) and underlying SJ Skin Complaint Log entry (gid `1204763097184846`) via plm-assistant. Recommend `Event Type` (SAE — MoCRA, Recall — Class I/II/III, or Triage Pending if classification needs more work). Update task with `Linked SKU`, `Linked Batch`, `Event Type = Triage Pending` until Job 2 classifies.
- *HITL:* regulatory-manager already confirmed scope at routing time. This skill picks up where regulatory-manager left off — Operator approves intake and Job 2 classification.

**Retrofit history:** at v6.2 (pre-v6.3), this Job read `[Reg Flag Pending — regulatory-manager]` directly from SJS Quality Management. Retrofitted at v6.3 build to receive fan-out from regulatory-manager. Same outcome, cleaner routing layer.

### 2. Classification draft (proposed; Pedrero confirms)

For each new event, walk the Reportable Events Procedure §3 (SAE) or §4 (Recall) classification criteria.

- *Trigger:* New task in Inbound Staging with `Event Type = Triage Pending`; or operator-direct ("classify this event", "is this an SAE", "what recall class is this")
- *Action:* Walk the criteria checklist:
  - **SAE — MoCRA:** Death; life-threatening; in-patient hospitalization; persistent or significant disability/incapacity; congenital anomaly/birth defect; serious or required medical/surgical intervention to prevent any of the above. (Reference: SKN-OPS-009 §3 once ratified.)
  - **Recall — Class I:** Reasonable probability of serious adverse health consequences or death.
  - **Recall — Class II:** Use may cause temporary or medically reversible adverse health consequences; remote probability of serious adverse health consequences.
  - **Recall — Class III:** Use is not likely to cause adverse health consequences.
  - Cite the criteria points met with evidence references.
- *HITL:* Operator approves the draft classification. On approval, `Event Type` flips from Triage Pending to the proposed type. Reg Lead approves the proposal as part of the Pedrero send approval at Job 4.

### 3. Packet drafting

For each classified event, draft the agency packet contents.

- *Trigger:* Operator approves classification (Job 2); or operator-direct ("draft the SAE packet on [SKU]", "build the recall report for [batch]")
- *Action:* Walk the Reportable Events Procedure §5 (SAE packet) or §6 (recall report) checklist:
  - **SAE packet:** event facts (date of awareness, date of consumer event if known, consumer information consistent with HIPAA-equivalent privacy rules, event description, severity assessment per §3 criteria), batch context (PLM batch_code, manufacturing date, distribution data), complaint linkage (originating complaint task in SJ Skin Complaint Log + Quality `[Reg Flag Pending]` reference), proposed classification with rationale, supporting documents (lab reports if any, complaint history pattern if relevant).
  - **Recall report:** event description, batch scope (single batch or multi-batch with explicit list), distribution data (DTC + retailer breakdown via oc3pl-order-manager queries), hazard assessment, proposed Class with 21 CFR 7 rationale, 21 CFR 7 supporting docs (recall strategy draft, customer notification draft from complaint-and-event-handler, retailer notification list).
- *HITL:* Operator approves the packet. On approval, the skill assigns the filing reference (`SAE-YYYY-NNN` or `RCL-YYYY-NNN`), creates the Outlook draft for Pedrero (Job 4), and parks the task awaiting Reg Lead approval.

### 4. Pedrero send

For every event, stage the Outlook draft to Pedrero.

The send draft is composed locally with attachments attached. Subject line follows Procedure §7 prefix convention. Return windows tightened from v6.1 — statutory clocks demand it.

- *Trigger:* Operator approves the packet at end of Job 3; or operator-direct ("send the [SKU] SAE packet to Pedrero", "stage the recall report")
- *Action:* Compose Outlook draft per `references/reportable-events-procedure.md` §7. To: Amy Pedrero. Cc: Heather Folkes, Teona Bebia. Subject prefix: `[SAE Filing — SKU-CODE]`, `[FDA Recall — Class X — SKU-CODE]`, or `[State AE — STATE — SKU-CODE]`. Include `URGENT — by [date]` when statutory clock is tighter than 5 business days. Body cites the SKU, the event facts, the proposed classification, the specific binding-call ask. Attach packet. Move Asana task to **In Pedrero Review** section. Set `Window End` to the statutory deadline (NOT Pedrero's expected return date — the agency clock is what matters). Default Pedrero return windows: 3 business days for SAE, 1 business day for Class I recall, 5 business days for Class II/III recall and state AE.
- *HITL:* **Reg Lead approves the Pedrero send** (`Gate = Pending Regulatory Lead`). On approval, Operator hits send in Outlook (skill does not send autonomously). Pedrero contacts added as task followers (informational — no Asana access).

### 5. Pedrero return processing

When a Pedrero reply arrives via outlook-asana-bridge, classify the return.

- *Trigger:* outlook-asana-bridge surfaces a Pedrero reply on a `[*Filing*]`- or `[*Recall*]`-tagged thread; or operator-direct ("Pedrero responded on the [SKU] SAE", "log Pedrero's recall classification")
- *Action:* Read the reply. Classify per Procedure §8:
  - **Approved (classification confirmed)** — Pedrero confirms classification and packet. Move to Job 6 (agency submission staging). If classification revised, update `Event Type` field and packet accordingly before submission.
  - **Returned for revision** — Pedrero kicked back. Move to **Returned — Action Required**. Capture rationale. Operator decides next step (revise packet, escalate severity, downgrade classification).
  - **Question / clarifying request** — stage a clarifying reply. Reg Lead approves the reply send. Asana task stays in **In Pedrero Review**.
- *HITL:* Operator approves the classification. Reg Lead approves any clarifying reply send.

### 6. Agency submission

For every Pedrero-approved filing, stage the agency submission. Operator submits manually; the skill never files directly.

- *Trigger:* Job 5 outcome = Approved; or operator-direct ("submit the [SKU] SAE to FDA", "file the recall report")
- *Action:* Walk Procedure §9 by agency:
  - **MoCRA SAE → FDA:** FDA MedWatch portal (Form FDA 3500A or MoCRA-specific equivalent — confirm current channel at submission time). Compose the submission per FDA portal requirements. Stage the upload attachments and form-field values for Operator to enter.
  - **FDA Recall → FDA:** FDA recall reporting portal per 21 CFR 7. Compose the submission. Stage attachments and form-field values.
  - **State AE → State DOH:** state-specific portal or specified channel. Compose per state requirements.
  - Move task to **Submitted to Agency** on Operator-confirmed submission. Capture submission timestamp, agency-assigned tracking number (when issued) in `Filing Reference` field, `Agency` field set to specific agency.
- *HITL:* **Reg Lead approves the agency submission** (separate gate from the Pedrero send approval at Job 4). Operator submits manually. Two distinct audit-trail entries per filing: Pedrero send approval + agency submission approval.

### 7. Agency response, statutory clock, closeout

Once submitted, track agency response and the statutory clock until close.

- *Trigger:* outlook-asana-bridge surfaces an agency reply; scheduled clock proximity reminder fires; operator-direct ("any updates from FDA on the [SKU] SAE", "close the [batch] recall agency-side", "any open SAEs at FDA")
- *Action:*
  - **Agency acknowledgment received** — log the acknowledgment timestamp + reference number (if not already captured). Move to **Awaiting Agency Response** if agency requires follow-up; otherwise hold in **Submitted to Agency** until agency closes.
  - **Agency follow-up request** — capture the request, route the response work to Operator. If response requires Pedrero review, restage via Job 4. If routine, Operator drafts and Reg Lead approves the agency reply send.
  - **Statutory clock proximity reminder fires** — auto-escalate to Reg Lead at 80% of clock, Operator at 95%, daily after 95%. Never lets a clock slide silently.
  - **Agency close** — agency confirms the filing is closed. Three-line summary on the Asana task: event type, classification, agency reference + close date. Close-the-loop comment back to Quality's `complaint-and-event-handler` task and the originating SJ Skin Complaint Log entry. Move to **Closed**.
- *HITL:* Operator approves close. Reg Lead approves any post-submission Pedrero re-stage or agency reply send.

## Asana surface

- *Project:* **SJS Reportable Events** — Operations team, public to workspace. Created 2026-05-09 via Asana AI Builder at v6.2 build. Rolls up under regulatory-manager (System C umbrella) for cross-skill dashboard alongside SJS Regulatory Management.
  - Project GID: `1214660834583706`
  - Project URL: https://app.asana.com/1/1200120716421441/project/1214660834583706
  - Team (Operations) GID: `1200120716421443`
  - Portfolio (Operations Dashboard): `1208174221370391` — **manual add pending** (no MCP tool exposes portfolio-add at v6.2 build)

### Sections (cached 2026-05-09)

| Section | GID | Purpose |
|---|---|---|
| Inbound Staging | `1214660834583732` | tasks created by regulatory-manager fan-out from Quality `[Reg Flag Pending]`, awaiting classification draft |
| In Pedrero Review | `1214660256599187` | packet sent to Pedrero, awaiting return |
| Returned — Action Required | `1214660256599188` | Pedrero kicked back; revise classification or packet |
| Submitted to Agency | `1214660256599189` | filed with FDA / state agency, awaiting agency confirmation |
| Awaiting Agency Response | `1214660256599190` | agency acknowledged; tracking follow-up requirements |
| Closed | `1214660256599191` | agency-closed, archived, terminal |

A default `Untitled section` (gid `1214660834583725`) exists from project creation — flag to Operator for delete or repurpose at first-run; the skill never writes to it.

### Custom fields (cached 2026-05-09)

All fields exist on SJS Reportable Events. Canonical GID + option-GID reference: `/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md`. The fields the skill uses:

- `Event Type` (single-select: SAE — MoCRA, Recall — Class I, Recall — Class II, Recall — Class III, Recall — Class TBD, State AE Report, MoCRA Other, Triage Pending) — what kind of event this is. `Triage Pending` is the default at intake until Job 2 classifies.
- `Linked SKU` (text — SKU code + name; shared field across SJS Quality Management, SJS CAPA Log, SJS Regulatory Management, SJS Reportable Events)
- `Linked Batch` (text — PLM batch_code; shared field. Multiple batches comma-separated when a recall affects more than one batch)
- `Source Reg Flag` (text — gid or link to the originating `[Reg Flag Pending — regulatory-manager]` task in SJS Quality Management)
- `Filing Reference` (text — agency case number once filed: FDA MedWatch ID, FDA recall tracking number, state DOH case ID. Format `SAE-YYYY-NNN` or `RCL-YYYY-NNN` until agency assigns its own.)
- `Agency` (single-select: FDA, FDA-OCC, CA-CDPH, NY-DOH, WA-DOH, OR-OHA, Other)
- `Window End` (date — statutory clock end. NOT Pedrero return date — agency deadline.)
- `Gate` (single-select, shared field: Open, Pending Operator, Pending QA Lead, Pending Regulatory Lead) — orthogonal to section. Carries who's holding the puck. This skill uses Pending Regulatory Lead for every Pedrero send and agency submission; uses Pending QA Lead only when a quality-side cross-check is in flight.

*Title prefixes:* reserved for cross-skill staging where the destination skill or source skill is not yet live. In-flight state and HITL gates use Section + Gate, not title prefixes.
- **Inbound from regulatory-manager:** tasks land in SJS Reportable Events Inbound Staging via regulatory-manager fan-out (Job 1 of regulatory-manager). `Source Reg Flag` field carries the originating `[Reg Flag Pending — regulatory-manager]` task gid for traceback to Quality.
- **Outbound staging to regulatory-manager:** `[Reg Coordination Pending — regulatory-manager]` for cross-skill issues that need the regulatory-manager dashboard view (e.g., a recall outcome that affects multiple registrations or surfaces a Pedrero engagement question).

## Numbering

- **SAE filing:** one task per SAE per SKU per batch, titled `SAE — [SKU] — [BATCH] — [DATE]`. Filing reference `SAE-YYYY-NNN`, zero-padded sequential by year, in `Filing Reference` field. First SAE of 2026 is `SAE-2026-001`.
- **Recall:** one task per recall event, titled `Recall — Class [X] — [SKU] — [DATE]`. Filing reference `RCL-YYYY-NNN`. Affected batches captured comma-separated in `Linked Batch` field, or as subtasks if the scope is large.
- **State AE:** one task per state per SKU per event, titled `State AE — [STATE] — [SKU] — [DATE]`. Filing reference `STAE-YYYY-STATE-NNN` (e.g., `STAE-2026-CA-001`).
- **Sequential numbering:** the skill checks the highest existing number on first write each session per type and increments.

## Role map

The skill reads role-holders from `references/role-map.md`. Update protocol and rationale match the System B/C siblings. SKILL.md, references, Asana writes, and Gate field options all stay role-based; names live in the role-map.

## Calls and integrations

Pedrero traffic and agency traffic are mostly Outlook; outlook-asana-bridge does heavy work. Asana is direct (this skill owns the SJS Reportable Events surface).

**Reads via:**
- plm-assistant — SKU lookups, batch context, formula linkage, complaint-to-batch traces
- complaint-and-event-handler — read SJ Skin Complaint Log (gid `1204763097184846`) for originating complaint context referenced via `Source Reg Flag` field on inbound tasks
- regulatory-manager — receive fan-out task creation in SJS Reportable Events Inbound Staging (Job 1 intake source)
- claims-il-and-label-keeper — when a recall surfaces a label or IL issue, read the SKU's IL version and label artwork archive
- batch-lifecycle-tracker — when a recall affects a batch, read current batch state before staging a hold request
- oc3pl-order-manager — distribution data for recall reports (DTC orders affected; retailer breakdown)
- outlook-asana-bridge — inbound Pedrero replies, inbound agency replies, retailer escalations
- fireflies-asana-bridge — inbound from incident calls, agency calls, Pedrero strategy calls
- Asana — direct read of own tasks in SJS Reportable Events
- SharePoint — Reportable Events Procedure ratification target, FDA submission templates, 21 CFR 7 supporting doc templates, agency correspondence archive (v6.3 forward)

**Writes via:**
- Asana — direct (custom fields, comments, section moves, new tasks for handoff staging)
- complaint-and-event-handler tasks — close-the-loop comments on filing close (Job 7)
- SJ Skin Complaint Log — close-the-loop comment on the originating complaint when filing closes
- batch-lifecycle-tracker — `[Batch Hold Request — batch-lifecycle-tracker]` task when a recall affects in-market batches
- capa-coordinator — NCR intake context in SJS CAPA Log Inbound Staging when an SAE or recall outcome warrants CAPA (Source = regulatory-observation)
- claims-il-and-label-keeper — cross-flag when recall surfaces a label-related issue
- outlook-asana-bridge — Outlook draft staging for every Pedrero send AND every agency submission (HITL on send; skill drafts, never sends autonomously)
- sweet-july-skin-brand — applied to any external-facing copy (consumer-facing recall communications routed to complaint-and-event-handler; this skill stays internal/agency-facing)

**Never duplicates:**
- complaint-and-event-handler (owns intake, triage, recall ops, customer-facing recall execution)
- capa-coordinator (owns the CAPA lifecycle; this skill stages handoffs)
- regulatory-manager (v6.3 — owns MoCRA registrations, state filings, retailer attestation cadence, cross-skill regulatory dashboard)
- claims-il-and-label-keeper (owns IL/claim/label/attestation workflow)
- regulatory-status-reporter (v6.4 — owns branded reportable-events reporting)
- batch-lifecycle-tracker (owns batch hold/release decisions; this skill stages hold requests)
- plm-assistant (only writer to PLM)

## Out of scope (v6.2)

- Complaint intake and triage (complaint-and-event-handler)
- Recall ops execution — customer notifications, retailer pulls, return logistics (complaint-and-event-handler)
- The CAPA opened from an SAE or recall (capa-coordinator)
- Pre-launch IL review, sustained claim sub, label artwork, retailer attestations (claims-il-and-label-keeper)
- MoCRA registrations, state filings (Prop 65, NY/WA/OR consumer cosmetic registries), retailer attestation cadence (regulatory-manager v6.3)
- Branded reportable-events reporting (regulatory-status-reporter v6.4)
- Cross-system regulatory router queries (sjs-regulatory-system v6.5)
- International adverse-event reporting (EU CPNP, UK SCPN, Health Canada, China NMPA) — parked
- Print-side or destruction-of-recalled-product workflows — Operations
- Direct PLM writes — plm-assistant only

## First-run setup

Project, sections, custom fields, and Source Reg Flag rename completed via Asana AI Builder + Operator UI on 2026-05-09 at v6.2 build. Gids cached in this SKILL.md and `asana-field-gids.md`. On first invocation:

1. **Confirm Asana state matches cached gids.** Re-pull SJS Reportable Events via Asana MCP and confirm sections and custom fields match what's documented above.
2. **Confirm portfolio.** Confirm SJS Reportable Events has been added to the Operations Dashboard portfolio (gid `1208174221370391`). Manual UI step — surface to Operator if missing.
3. **Confirm SOP state.** `references/reportable-events-procedure.md` is SKN-OPS-009 Rev.1, ratified 2026-05-09. `quality-manager/references/sop-catalog.md` lists SKN-OPS-009 as Ratified. Skill writes cite "SKN-OPS-009 Rev.1".
4. **Confirm role-map.** Confirm `references/role-map.md` is current with the operator.
5. **Confirm SharePoint interim plan.** Until v6.3 stands up `Sweet July/Regulatory`, agency packets and correspondence attach to Asana tasks directly per Procedure §10.
6. **Default section housekeeping.** A default `Untitled section` (gid `1214660834583725`) exists from project creation. Surface to Operator at first interaction for delete or rename.
7. **Confirm SJ Skin Complaint Log access.** Confirm gid `1204763097184846` is reachable for source context lookups (Job 1 reads complaint context referenced by `Source Reg Flag` field, supplied by regulatory-manager fan-out).

If any check fails, surface to the operator and stop — the skill does not modify project structure unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/reportable-events-procedure.md` — Reportable Events Procedure (working draft, pending SKN-OPS-009 ratification)
- `references/role-map.md` — current role-holders for Operator, Reg Lead, External Reg Partner, QA Lead, Voice of Customer
- `references/trigger-phrases.md` — grouped triggers by intent (intake, classification, packet drafting, Pedrero send, return processing, agency submission, clock tracking, closeout, status)

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant SKU page from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as bridge skills process adverse-event reports, complaint traffic, and recall correspondence. Reading them first gives this skill institutional memory about each SKU's adverse-event history without re-scanning raw sources.

### Which pages to read

- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`

SKU pages carry adverse-event history, complaint patterns, batch threads, recall precedent, and stability status.

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

Prepend the wiki page content to this skill's context before generating its response. Treat it as a pre-synthesized briefing on the SKU's adverse-event and recall history.

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
