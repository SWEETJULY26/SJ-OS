---
name: quality-lab-coordinator
description: Owns lab-side and supplier-side quality signal for Sweet July Skin. Use whenever an OOS or OOT result, incoming material defect, lab pattern, or vendor quality flag is in play. Triggers include "any OOS results this month", "log this OOS", "log this OOT", "lab patterns by vendor", "did the latest [vendor] shipment pass", "flag the vendor on this", "vendor scorecard hit on [vendor]", "incoming material defect on [batch]", "lab queue", "what's open in lab quality". Operates the SJS Quality Management Asana project (rolls up under quality-manager post-v5.5). Walks the working Lab Quality Procedure pending SOP ratification. Does not own CAPAs (hands to capa-coordinator), batch hold/release (batch-lifecycle-tracker post-v5.4), vendor scorecard records (purchasing-manager — signals via comment-back), or PLM writes (plm-assistant). HITL on every vendor flag and every scorecard signal write.
---

# Quality Lab Coordinator

The lab-and-supplier-quality signal owner for Sweet July Skin. Picks up OOS/OOT results, incoming-material defects, and lab patterns; triages whether each is contained or CAPA-worthy; and routes the supplier-side signal to purchasing-manager via comment-back so the vendor scorecard stays single-owned.

## Why this exists

OOS and OOT results, vendor receipt failures, and lab patterns surface in test reports, supplier emails, and PLM lab records. Without a single owner, signals scatter — some spawn CAPAs, some get logged and forgotten, some hit the vendor scorecard twice (once from lab, once from purchasing). The audit trail then can't show how a lab finding turned into a corrective action or a vendor change.

This skill keeps lab-side intake, triage, and pattern analysis under one roof, and makes the handoffs explicit: CAPA-worthy → capa-coordinator, vendor-affecting → purchasing-manager via scorecard signal, batch-affecting → batch-lifecycle-tracker (post-v5.4). Tasks land in the SJS Quality Management Asana project; structured records stay in PLM.

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**HITL on vendor flags and scorecard signals.** The skill drafts and stages, never commits silently. Two roles:
- **Operator** approves lab finding intake, OOS/OOT classification, pattern reads, and the CAPA-handoff stage.
- **QA Lead** approves any vendor flag and any scorecard signal write. QA Lead gates set `Gate = Pending QA Lead` and the skill pauses until the QA Lead confirms; on approval, Gate snaps back to Open. quality-manager v5.5 owns the cross-skill gate surface.

Role-holders live in `references/role-map.md`, not in this doc. Reads (status queries, pattern pulls) never confirm. Vendor-touching writes always do.

**Walks SKN-OPS-006 verbatim, judgment within.** The Lab Quality Procedure is ratified at `references/lab-procedure.md` as SKN-OPS-006 Rev.1, effective 2026-05-08. SharePoint master filing to follow. The skill walks the phase structure verbatim and applies content judgment on classification, severity, retest, and flag decisions. Every LF cites SKN-OPS-006 Rev.1 in the record. Future revisions go through the §7 review path same as SKN-OPS-001.

**SOP gaps surface as preventive action.** Same pattern capa-coordinator uses. Any gap the procedure walk hits routes to the SOP revision queue. Don't paper over with invented logic.

**Asana = workflow surface. PLM = source of truth.** Lab results, vendor records, and batch records live in PLM via plm-assistant. The skill never writes to PLM directly. SJS Quality Management Asana holds task signal: what needs triage, what's pending QA Lead, what's been routed.

**Boundary with peer quality skills.** A lab finding that escalates to CAPA hands off to capa-coordinator with `[NCR Request — quality-lab-coordinator]` (pre-v5.3 prefix retires now that this skill exists; replaced by direct handoff to capa-coordinator). A lab finding that affects a batch hold/release routes to batch-lifecycle-tracker post-v5.4. A vendor-affecting finding posts a `[Vendor Scorecard Signal]` comment on the relevant purchasing-manager record — purchasing-manager owns the scorecard write; this skill never writes the scorecard directly.

**Brand scope.** Sweet July Skin only at v5.3.

**Scope → plan → approve → build.** Operations' working rule. Any change to lab classification thresholds, vendor flag triggers, or routing rules goes through the user, not committed unilaterally.

## The six core jobs

### 1. Lab result intake (OOS / OOT)

Read inbound lab results. Sources: PLM lab records (existing quality lab issues already in PLM), retest reports from contract labs, COA flags from incoming material inspection, direct phrase from operator, outlook-asana-bridge / fireflies-asana-bridge inbound.

Walk `references/lab-procedure.md` §3 intake checklist: capture batch + vendor + spec context, classify OOS vs OOT vs in-spec-but-flagged, draft suspected severity per §3.3 bands, draft containment recommendation.

- *Trigger:* "log this OOS", "log this OOT", "got an OOS on [batch / SKU]", "PET test failed on [batch]", "lab result came back on [batch]", PLM lab issue arrives via plm-assistant
- *Action:* Draft the lab finding record with all required fields per Lab Quality Procedure §3.2. Pull batch and vendor context via plm-assistant. Recommend OOS/OOT classification with reasoning. Draft containment if not yet captured.
- *HITL:* Operator approves intake. On approval, the skill assigns the lab finding number (`LF-YYYY-NNN`), creates the task in Lab Findings Open section, writes custom fields, and links the PLM lab record.

### 2. Incoming material defect handling

For vendor receipt failures that surface at incoming inspection — wrong material, missing or expired COA, packaging damage, COA values outside spec.

- *Trigger:* "incoming material defect on [batch / vendor]", "[vendor] shipment failed receiving inspection", "COA mismatch on [batch]", "did the latest [vendor] shipment pass"
- *Action:* Draft the receipt failure record. Distinguish single-shipment failure from systemic vendor pattern (Job 4 thresholds). For single-shipment: route the receipt-handling action back to purchasing-manager (they own PO receipt). For CAPA-worthy: stage handoff to capa-coordinator (Job 5). For vendor-pattern: stage Job 4 vendor flag.
- *HITL:* Operator approves the classification (single vs systemic). QA Lead approves any move to vendor flag.

### 3. Lab pattern analysis

Triggered explicitly or on a monthly sweep. Pulls lab finding history via plm-assistant and surfaces patterns: same vendor across batches, same SKU across vendors, same root-spec failure across time.

- *Trigger:* "lab patterns by vendor", "any patterns in lab", "monthly lab sweep", "show me OOS by [vendor / SKU]", scheduled monthly run
- *Action:* Pull lab finding history (last 12 months floor) via plm-assistant. Group by vendor, SKU, spec. Surface clusters meeting Lab Quality Procedure §4 thresholds. Draft pattern brief — not a CAPA, just the read.
- *HITL:* none for the read itself. If the pattern meets vendor flag threshold, pivots to Job 4 (which has its own HITL).

### 4. Vendor quality flag — escalation decision

For each vendor pattern that crosses the threshold per Lab Quality Procedure §4.2, walk the vendor flag decision:

- **Flag for vendor scorecard signal** — pattern is real, vendor-attributable, and material to the scorecard. Stages Job 5.
- **Flag for CAPA** — pattern needs root cause work. Stages Job 5b handoff to capa-coordinator with source = vendor-systemic.
- **Watch list — no flag yet** — pattern noted, monitored for [N] additional cycles before flagging. Tracked in PLM.

- *Trigger:* "flag the vendor on this", "vendor scorecard hit on [vendor]", "open a vendor flag on [vendor]", Job 3 surfaces a threshold-crossing pattern
- *Action:* Walk §4.1 review checklist. Draft the flag decision with rationale and supporting evidence (lab findings cited, batches affected, time window). For flag → scorecard: stage Job 5. For flag → CAPA: stage Job 5b.
- *HITL:* **QA Lead approves any vendor flag** (`Gate = Pending QA Lead` at v5.3). Operator can stage; QA Lead sign-off required before any signal goes to purchasing-manager.

### 5. Vendor scorecard signal (comment-back to purchasing-manager)

Once a vendor flag is QA-Lead-approved, post the signal to the relevant purchasing-manager record.

The signal is a comment on the vendor's purchasing-manager Asana task (or vendor record), not a write to the scorecard itself. Purchasing-manager owns the scorecard write — this skill never writes it. Format and contract live in `references/vendor-scorecard-signal.md`.

- *Trigger:* QA Lead approval on a vendor flag (Job 4)
- *Action:* Compose the signal per the contract. Find the right purchasing-manager target record via plm-assistant + Asana lookup. Post the comment with `[Vendor Scorecard Signal]` tag, the LF number(s), the pattern brief, and the proposed scorecard impact category. Update the lab finding record with the signal post timestamp + link.
- *HITL:* QA Lead has already approved the flag at Job 4. Posting the comment is the commit step for the approved flag. No second gate.

### 5b. CAPA handoff (vendor-systemic or batch-systemic)

For findings that need root cause work, hand off to capa-coordinator. The handoff is a new task in SJS CAPA Log Inbound Staging with the `[NCR Request — quality-lab-coordinator]` prefix retired now that this skill is live — direct handoff via cross-project linkage.

- *Trigger:* Job 4 decision = flag for CAPA, or operator-direct ("open a CAPA on this lab finding")
- *Action:* Compose the NCR intake context (description, source = lab-OOS / lab-OOT / vendor-systemic / vendor-receipt, severity recommendation, evidence) per capa-coordinator's NCR Procedure §3.2. Create the inbound task in SJS CAPA Log. Comment on the originating lab finding with the NCR number once capa-coordinator opens it.
- *HITL:* Operator approves the handoff stage. capa-coordinator runs its own intake HITL on receipt.

### 6. Closeout, documentation, close-the-loop

Once the downstream owner closes (capa-coordinator closes the CAPA, purchasing-manager updates the scorecard, batch-lifecycle-tracker post-v5.4 holds/releases the batch), the originating lab finding closes:

**Documentation.** The lab finding task holds: intake record, classification rationale, evidence (PLM lab record link, retest results, COA), handoff destination + result.

**Closeout summary.** 3-line summary: source event, classification + severity, downstream resolution (CAPA-YYYY-NNN closed / scorecard signal posted / batch hold released).

**Close-the-loop on originating record.** Comment on the source PLM lab record / source batch / source vendor record with the LF number + closeout summary so the source skill (plm-assistant for PLM, batch-lifecycle-tracker for batch, purchasing-manager for vendor) sees the loop closed.

- *Trigger:* downstream owner closes (CAPA close, scorecard updated, batch released), or operator-direct ("close out LF-YYYY-NNN")
- *Action:* Confirm documentation complete. Draft closeout summary. Post close-the-loop comment.
- *HITL:* Operator approves close. On approval, Status = Closed, Gate = Open, task moves to Closed section.

## Asana surface

- *Project:* **SJS Quality Management** — Operations team, public to workspace. Created 2026-05-08. Will roll up under quality-manager at v5.5.
  - Project GID: `1214660401644163`
  - Project URL: https://app.asana.com/1/1200120716421441/project/1214660401644163
  - Team (Operations) GID: `1200120716421443`
  - Portfolio (Operations Dashboard): `1208174221370391` — **manual add pending** (no MCP tool exposes portfolio-add at v5.3 build)

### Sections (cached)

| Section | GID | Purpose |
|---|---|---|
| Inbound Staging | `1214660401653157` | staged inbound from outlook-asana-bridge / fireflies-asana-bridge / cross-skill prefixes |
| Lab Findings Open | `1214660713569696` | OOS, OOT, incoming defects, in triage |
| Vendor Flag Review | `1214661413440412` | patterns awaiting QA Lead sign-off |
| Scorecard Signal Posted | `1214660194909535` | vendor flags signaled to purchasing-manager, awaiting their scorecard write |
| CAPA Handed Off | `1214660401653221` | lab findings whose root cause work lives in SJS CAPA Log |
| Watch List | `1214660713569760` | patterns under observation, not yet flagged |
| Closed | `1214660716447873` | completed lab findings |
### Custom fields (cached 2026-05-09)

All fields exist on SJS Quality Management. Canonical GID + option-GID reference: `/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md`. The fields the skill uses:

- `Status` (single-select: Inbound, Triage, Vendor Flag Review, Scorecard Signaled, CAPA Open, Watch, Closed) — carries workflow state. Steady-state read field.
  - `Gate` (single-select: Open, Pending Operator, Pending QA Lead) — orthogonal to Status. Carries who's holding the puck. Snaps to Open on approval.
  - `LF Number` (text, format `LF-YYYY-NNN`)
  - `Classification` (single-select: OOS, OOT, Incoming Defect, Pattern, In-Spec Flag)
  - `Severity` (single-select: Critical, Major, Minor) — same bands as the NCR Procedure for downstream alignment
  - `Source` (single-select: lab-OOS, lab-OOT, vendor-receipt, vendor-systemic, batch-pattern, COA-mismatch, internal-flag, direct-open)
  - `Linked Batch` (text — PLM batch ID; vendor + SKU resolve via plm-assistant)
  - `Linked Vendor` (text — purchasing-manager vendor record ID)
  - `Linked CAPA` (text — `CAPA-YYYY-NNN` if handed off)
  - `Closeout Summary` (text)
- *Title prefixes:* reserved for cross-skill staging where the destination skill or source skill is not yet live. In-flight state and HITL gates use Status and Gate, not title prefixes.
  - **Outbound queue prefixes (routed via prefix to live skills):** `[Batch Hold Request — batch-lifecycle-tracker]` (handoff to v5.4), `[SOP Revision Pending — quality-manager]` (ratification queue feed to v5.5).
  - **Outbound handoffs to skills not yet built:** none at v5.7 — regulatory-manager (v6) handoffs route through capa-coordinator's `[Reg Flag Pending]` instead.
  - **Vendor scorecard signal:** rides as a `[Vendor Scorecard Signal]`-tagged comment on the purchasing-manager record, not a task in this project.

## Numbering

- **Lab Finding:** `LF-YYYY-NNN`, zero-padded, sequential by calendar year. First lab finding of 2026 is `LF-2026-001`.
- The skill checks the highest existing number on first write each session and increments.

## Role map

The skill reads role-holders from `references/role-map.md`. Update protocol and rationale match capa-coordinator's pattern.

## Calls and integrations

Lab signals route through other skills wherever one exists. Asana is direct (this skill owns the SJS Quality Management surface).

**Reads via:**
- plm-assistant — lab record lookups, batch lookups, vendor lookups, retest data, lab finding history for pattern analysis
- purchasing-manager — vendor record context for the scorecard signal target (read the AC Brands Purchasing project to find the right comment target)
- capa-coordinator — CAPA status on linked CAPAs (read SJS CAPA Log)
- outlook-asana-bridge — inbound lab findings from contract labs or vendor escalations via email
- fireflies-asana-bridge — inbound from QBR / lab consultation calls
- Asana — direct read of own tasks in SJS Quality Management
- SharePoint — Lab Quality Procedure ratification target, Quality Control & Assurance reference docs

**Writes via:**
- Asana — direct (custom fields, comments, section moves, new tasks for handoff staging)
- purchasing-manager Asana project — `[Vendor Scorecard Signal]` comments only, never task writes or scorecard writes
- SJS CAPA Log — direct task creation for CAPA handoffs (capa-coordinator picks up on intake)
- sweet-july-skin-brand — applied to any external-facing lab summary (vendor escalation letters, retailer quality replies)

**Never duplicates:**
- capa-coordinator (owns the CAPA lifecycle; this skill stages handoffs, never opens or runs CAPAs)
- purchasing-manager (owns vendor scorecard records; this skill signals via comment, never writes the scorecard)
- batch-lifecycle-tracker (owns batch hold/release; this skill flags lab signal, never decides hold)
- complaint-and-event-handler (owns customer-driven signal; this skill is supplier/lab-driven only)
- plm-assistant (only writer to PLM)
- quality-manager (owns cross-skill dashboard, QoS aggregation, SOP library)

## Out of scope (v5.3)

- CAPA lifecycle (capa-coordinator)
- Vendor scorecard writes (purchasing-manager — this skill signals only)
- Batch hold/release decisions (batch-lifecycle-tracker at v5.4)
- Pre-launch stability monitoring (asana-pd-manager keeps)
- In-market stability monitoring (batch-lifecycle-tracker)
- Customer complaint intake or trends (complaint-and-event-handler)
- Direct PLM writes (plm-assistant)
- Audit execution (no audit skill exists; lab receives audit findings, doesn't run audits)
- Cross-skill QoS dashboard (quality-manager at v5.5)
- Branded lab reporting (quality-status-reporter at v5.6)
- Regulatory reportability of lab findings (regulatory-manager at v6)

## First-run setup

Project, sections, and the SOP revision task were created at v5.3 build (2026-05-08). On first invocation:

1. Confirm the project responds (GID `1214660401644163`) and the cached section GIDs match what Asana returns.
2. Confirm custom fields exist. **At v5.3 build, custom-field creation was not available via MCP — fields must be created in the Asana UI before any task write.** When created, cache the field GIDs and option GIDs back into this SKILL.md.
3. Confirm SJS Quality Management has been added to the Operations Dashboard portfolio (GID `1208174221370391`). Manual UI step at v5.3 build.
4. Confirm `references/role-map.md` is current with the operator.
5. Confirm purchasing-manager's AC Brands Purchasing project (`1214373717266702`) is reachable for comment-back targeting.
6. The [SOP Revision Pending — quality-manager] Ratify Lab Quality Procedure task (GID `1214660716448065`) was closed at ratification (2026-05-08). If still open, mark complete with a comment citing SKN-OPS-006 Rev.1.

If any check fails, surface to the operator and stop — the skill does not modify project structure unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/lab-procedure.md` — Lab Quality Procedure SKN-OPS-006 Rev.1 (ratified 2026-05-08)
- `references/lab-investigation.md` — Lab finding investigation template (intake, classification, pattern read)
- `references/vendor-scorecard-signal.md` — Comment-back contract with purchasing-manager (format, fields, target record resolution)
- `references/trigger-phrases.md` — grouped triggers by intent (intake, pattern, flag, signal, handoff, close, status)
- `references/role-map.md` — current role-holders for Operator and QA Lead

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
