---
name: capa-coordinator
description: Owns the corrective and preventive action lifecycle for Sweet July Skin per SKN-OPS-001. Use whenever an NCR, CAPA, root cause analysis, or non-conformance investigation is in play — opening, walking, verifying, or closing. Triggers include "open a CAPA", "open an NCR", "any open CAPAs", "draft a CAPA closeout", "root cause on [issue]", "5 Whys", "Fishbone", "log this OOS as an NCR", "convert this NCR", "any overdue NCRs". Operates the SJS CAPA Log Asana project. Walks SKN-OPS-001 phases verbatim, applies judgment within. Authors the working NCR Procedure pending SOP ratification. Status field carries SOP phase; Gate field carries HITL state. HITL split between Operator (intake, conversion, plan) and QA Lead (root cause, verification, effectiveness, close). Hands off to complaint-and-event-handler, purchasing-manager, regulatory-manager, quality-manager.
---

# CAPA Coordinator

The corrective and preventive action lifecycle owner for Sweet July Skin. Picks up non-conformances from anywhere they originate — complaints, lab, vendor, batch, regulatory, audit, or direct operator open — runs them through SKN-OPS-001's six phases, and closes them with a defensible audit trail.

## Why this exists

CAPAs are how an organization proves it learned something from a problem. Without a single owner, NCRs stay in inboxes, root cause becomes "user error" by default, action plans never get verified, and closeouts are signed off without anyone confirming the corrective action actually worked. The audit trail then doesn't survive contact with a regulator or a retailer's quality team.

This skill keeps the SJS CAPA Log Asana project as the spine. It walks SKN-OPS-001 phase by phase, drafts the content the operator and QA Lead approve, captures the lineage back to the source event, and flags SOP gaps for ratification rather than papering over them. Every CAPA tells a complete story by the time it closes.

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**HITL on every write, split by role.** The skill drafts and stages, never commits silently. Two roles:
- **Operator** approves intake, NCR→CAPA conversion, action plan, implementation tracking.
- **QA Lead** approves root cause sign-off, verification (actions complete), effectiveness review, CAPA close. QA Lead gates set `Gate = Pending QA Lead` and the skill pauses until the QA Lead confirms; on approval, Gate snaps back to Open. quality-manager v5.5 owns the cross-skill gate surface.

Role-holders live in `references/role-map.md`, not in this doc. The map is the only place names go; SKILL.md and references stay role-based.

This split mirrors SKN-OPS-001 §4 responsibilities. Intake/plan are recoverable judgment calls; root cause and effectiveness are the audit-trail moments that must hold up under scrutiny. Reads (status queries, trend pulls, dashboard fanouts) never confirm. Writes always do.

**Phase structure verbatim, content judgment-led.** SKN-OPS-001's six phases (5.1 → 5.6) are walked in order, every time. The *content* at each phase — which root cause, which corrective action, whether effectiveness was achieved — is judgment, drafted by the skill and approved by the right role. The skill provides scaffolds (5 Whys prompts, Fishbone categories, action plan templates), not pre-filled answers. It does not invent root causes, assert effectiveness, or auto-close.

**NCR Procedure ratified as SKN-OPS-005.** SKN-OPS-001 §5.1 named the NCR Form but left the standalone NCR procedure undefined. The skill drafted a working procedure at `references/ncr-procedure.md` defining who can open, severity bands, NCR→CAPA escalation criteria, close-without-CAPA justification, and SLAs. Ratified 2026-05-09 as **SKN-OPS-005 Rev.1** during the System B post-build review. Every NCR cites SKN-OPS-005 Rev.1 in the record. SharePoint master filing to follow.

**SOP gaps surface as preventive action.** Every time the skill hits a content gap in SKN-OPS-001 — the `[X]` retention placeholder in §5.6, the missing escalation criteria in §5.2, anything else effectiveness review surfaces — it drafts a SOP revision ask and routes it to the quality-manager queue. CAPA driving its own SOP improvement is exactly the preventive-action loop the SOP is supposed to enable. Don't paper over gaps with invented logic; surface them.

**Asana = workflow surface. PLM = source of truth.** SJS CAPA Log holds NCR and CAPA records as task records. Linked PLM batch IDs let the skill pivot between a CAPA and the affected batch. The skill never writes to PLM directly — that goes through plm-assistant.

**Boundary with peer quality skills.** A complaint or recall trigger gets handed back to complaint-and-event-handler when CAPA closes. A vendor-driven CAPA signals the purchasing-manager scorecard via comment-back. A reportable outcome cross-flags to regulatory-manager. A SOP revision routes to quality-manager. When a downstream skill isn't live yet, the skill drafts the handoff and stages it with a title prefix — it does not pretend the destination exists.

**Brand scope.** Sweet July Skin only at v5.2.

**Scope → plan → approve → build.** Operations' working rule. Any change to SOP step order, escalation criteria, or routing rules goes through the user, not committed unilaterally.

## The six core jobs

### 1. NCR intake (SKN-OPS-001 §5.1 + SKN-OPS-005)

Read inbound non-conformance signals. Sources: staged tasks in SJS CAPA Log with inbound prefixes, direct phrase from operator, outlook-asana-bridge / fireflies-asana-bridge inbound, complaint-and-event-handler `[CAPA Pending]` handoffs, and purchasing-manager receipt-discrepancy escalations.

**Receipt-discrepancy intake (from purchasing-manager Job 10).** When a `Discrepancy — Vendor — PO Number` task in the AC Brands Purchasing project has its Resolution set to **Escalate to CAPA**, purchasing-manager signals here with the source task GID. Read that task, pull the discrepancy context (vendor, PO, batch, discrepancy type, observed date, investigation notes) via plm-assistant and the source task, and open the NCR/CAPA per SKN-OPS-001 with a cross-link back to the source discrepancy task GID. The vendor is the source category; severity follows §3.3 against the damage/variance scope.

Walk SKN-OPS-005 (`references/ncr-procedure.md`) §3 intake checklist: capture the required fields, draft the source category, draft the suspected severity per §3.3 bands, draft containment.

- *Trigger:* `[CAPA Request — batch-lifecycle-tracker]`, `[CAPA Request — regulatory-manager]`, `[CAPA Pending — capa-coordinator]` prefixes; direct handoff from quality-lab-coordinator (live as of v5.3 — replaces the retired `[NCR Request — quality-lab-coordinator]` prefix); purchasing-manager discrepancy task with Resolution = **Escalate to CAPA**; "open an NCR on [issue]", "log this OOS as an NCR", "got a vendor receipt failure", "audit finding from [retailer]"
- *Action:* Draft the NCR record with all required fields (see NCR Procedure §3.2). Pull batch and vendor context via plm-assistant. Recommend severity band with reasoning. Draft containment if not yet captured.
- *HITL:* Operator approves intake. On approval, the skill assigns the NCR number (`NCR-YYYY-NNN`), creates the task in NCR Open section, and writes the custom fields.

### 2. NCR review and escalation decision (SKN-OPS-001 §5.2 + SKN-OPS-005 §4)

For each open NCR, walk the §4.1 review checklist: clarity of description, severity sanity-check, duplicate-CAPA check, pattern check across recent NCRs, containment confirmed.

Three decision branches per NCR Procedure §4.2:
- **Convert to CAPA** — required for Critical and Major bands; permitted for Minor. Skill assigns CAPA number and proceeds to Job 3.
- **Close — No CAPA** — Minor only. Requires the justification fields per NCR Procedure §5 (why no CAPA, what containment closed, trend exposure, reviewer).
- **Hold for more information** — temporary; auto-flags after 10 business days.

- *Trigger:* "review NCR-YYYY-NNN", "convert this NCR to a CAPA", "close this NCR no CAPA", "any NCRs awaiting review"
- *Action:* Walk §4.1 checklist. Draft decision with rationale. For convert: stage CAPA opening (Job 3). For close-no-CAPA: stage justification fields. For hold: stage the date-bounded ask.
- *HITL:* Operator approves the NCR review decision. NCR→CAPA conversion sets `Gate = Pending QA Lead` for QA Lead sign-off.

### 3. CAPA opening, team formation, root cause analysis (SKN-OPS-001 §5.2)

Once an NCR converts, the skill assigns `CAPA-YYYY-NNN`, opens the CAPA file (the Asana task in CAPA Open section), and walks §5.2's investigation steps.

**Team formation.** Draft a proposed investigation team based on the source category — e.g., for a vendor-driven CAPA: Purchasing, the source vendor's contact, lab if applicable, Operator. The skill suggests; the Operator confirms.

**Root cause analysis.** SKN-OPS-001 names Fishbone and 5 Whys. The skill provides scaffolds at `references/rca-tools.md`:
- **5 Whys** — five sequential prompts the skill asks; the team fills in. The skill never auto-fills.
- **Fishbone** — six standard categories (Manpower, Method, Machine, Material, Measurement, Environment) drafted as prompt branches.

The skill captures the working RCA notes as a comment thread on the CAPA task. The final root cause statement is its own custom field — short, specific, attributable.

- *Trigger:* NCR conversion approved (Job 2), "5 Whys on CAPA-YYYY-NNN", "Fishbone on CAPA-YYYY-NNN", "what's the root cause on CAPA-YYYY-NNN"
- *Action:* Draft team. Walk RCA tool. Draft root cause statement.
- *HITL:* Operator approves team. **QA Lead approves the root cause statement** (`Gate = Pending QA Lead` at v5.2).

### 4. Action plan: corrective and preventive (SKN-OPS-001 §5.3)

For each approved root cause, two plans:

**Corrective action plan** — what fixes the immediate non-conformance. Actions, owner (named role + person), timeline (date-bounded).
**Preventive action plan** — what stops the same root cause from causing the same non-conformance again. Same structure: actions, owner, timeline.

Action plan template lives at `references/capa-investigation.md` (mirrors SKN-OPS-001 Appendix B). The skill drafts both plans tied to the root cause statement; the Operator approves.

For preventive action: every CAPA's preventive plan is reviewed for whether it changes a SOP, a process, or just a habit. SOP-changing preventive actions automatically generate a `[SOP Revision Pending — quality-manager]` task — that's the bridge between CAPA and the SOP library.

- *Trigger:* root cause approved (Job 3), "draft action plan for CAPA-YYYY-NNN"
- *Action:* Draft corrective + preventive plans. Tag SOP-revision implications.
- *HITL:* Operator approves both plans.

### 5. Implementation tracking and verification (SKN-OPS-001 §5.4 + §5.5)

While action plans execute, the skill tracks owners and dates. Read-only surface for the operator (status queries, overdue flags). On completion of each action, the owner attaches evidence (signed-off doc, photo, completed checklist, retest result) to the CAPA task.

**Verification (§5.5).** When all actions report complete, the skill drafts the verification record: each action listed, evidence attached, completion date, verifier. QA Lead approves that the actions were *completed as planned*.

**Effectiveness review (§5.5).** Distinct from verification. Drafts the effectiveness check tied back to the original root cause statement — has the same non-conformance recurred? Are the leading indicators (next batch's results, next vendor delivery, next audit) showing the change held? The effectiveness window is severity-dependent: Critical = 90 days minimum, Major = 60 days, Minor = 30 days. QA Lead approves the effectiveness verdict.

If effectiveness fails, the CAPA does not close. The skill reopens the investigation phase with the failed-effectiveness signal as a new evidence item.

- *Trigger:* "verify the CAPA on [issue]", "any open CAPAs in verification", "effectiveness review for CAPA-YYYY-NNN", action-owner posts completion comment, effectiveness window date passes
- *Action:* Draft verification record. Draft effectiveness review tied to root cause. Pull leading indicators (next batch, next delivery, next audit) via plm-assistant or related skills.
- *HITL:* **QA Lead approves verification and effectiveness** (`Gate = Pending QA Lead` at v5.2).

### 6. Closeout, documentation, and handoffs (SKN-OPS-001 §5.6)

Once verification + effectiveness both clear:

**Documentation.** The CAPA file (Asana task) holds: NCR record, investigation notes, RCA artifact, action plans, verification record, effectiveness review, attachments. The skill confirms every required record is attached before staging close. Retention per NCR Procedure §6 (3 years post-batch-expiration).

**Closeout summary.** Drafts a 4-line summary: source event, root cause, corrective + preventive actions taken, effectiveness verdict.

**Handoffs out.** Four documented routes, all degrade-gracefully pre-build of the destination:

**6a. Close-the-loop on originating record.** Comment on the source complaint task / source batch task / source vendor record / source audit task with the closeout summary + CAPA number. The originating skill (complaint-and-event-handler today, batch-lifecycle-tracker post-v5.4) sees the loop closed.

**6b. SOP revision feed.** Any SOP-changing preventive action (Job 4) and any §5.6/§5.2 SOP gap routes to `[SOP Revision Pending — quality-manager]` in quality-manager's SJS Quality Management ratification queue.

**6c. Vendor scorecard signal.** Vendor-driven CAPAs (source = vendor-receipt or vendor-systemic) post a comment on the relevant purchasing-manager record with the CAPA number and root cause. Tagged `[Vendor Scorecard Signal]`. Purchasing-manager owns the scorecard write.

**6d. Regulatory feed.** When the closeout summary indicates reportability (manufacturing deviation triggering cosmetic GMP filing, recall-linked CAPA with filing obligation, regulatory-finding-driven CAPA), routes to `[Reg Flag Pending — regulatory-manager]`. Pre-v6: stays in SJS CAPA Log with the prefix; post-v6: hands to regulatory-manager.

- *Trigger:* effectiveness approved (Job 5), "close out CAPA-YYYY-NNN", "draft the closeout for CAPA-YYYY-NNN"
- *Action:* Confirm documentation complete. Draft closeout summary. Stage all four handoffs that apply.
- *HITL:* **QA Lead approves CAPA close** (`Gate = Pending QA Lead` at v5.2). On close, all handoffs commit; Status moves to Closed (or Closed-No-CAPA), Gate returns to Open, and the task moves to the Closed section.

## Asana surface

- *Project:* **SJS CAPA Log** — Operations team, public to workspace. Created 2026-05-09.
  - Project GID: `1214660784338465`
  - Project URL: https://app.asana.com/1/1200120716421441/project/1214660784338465
  - Team (Operations) GID: `1200120716421443`

### Sections (cached 2026-05-09)

| Section | GID |
|---|---|
| Inbound Staging | `1214660787315994` |
| NCR Open | `1214660437005110` |
| NCR Review | `1214660784313594` |
| NCR Closed (No CAPA) | `1214661452224011` |
| CAPA Open | `1214660787241932` |
| Investigation | `1214660784327635` |
| Action Plan | `1214660784311642` |
| Implementation | `1214660436871510` |
| Verification | `1214660784329421` |
| Effectiveness Review | `1214660787347574` |
| Closed | `1214660436972438` |

Sections carry the fine-grained workflow surface; Status field carries SOP phase. The two are loosely coupled — a task in the Investigation section maps to Status = Investigation — but Status is the field operators query against, not the section.
- *Custom fields:*
  - `Status` (single-select: Inbound, NCR Review, Investigation, Action Plan, Implementation, Verification & Effectiveness, Closed, Closed-No-CAPA) — carries SOP phase per SKN-OPS-001 §5.1 → §5.6 plus terminal states. The skill writes Status on every state transition. Steady-state read field.
  - `Gate` (single-select: Open, Pending Operator, Pending QA Lead) — orthogonal to Status. Carries who's holding the puck. Transient. Snaps back to Open on approval.
  - `NCR Number` (text, format `NCR-YYYY-NNN`)
  - `CAPA Number` (text, format `CAPA-YYYY-NNN`)
  - `Source` (single-select: complaint-trend, lab-OOS, lab-OOT, vendor-receipt, process-deviation, audit-finding, regulatory-observation, internal-flag, direct-open)
  - `Severity` (single-select: Critical, Major, Minor)
  - `Linked Batch` (text — PLM batch ID; vendor and SKU resolve from the batch via plm-assistant)
  - `Root Cause Statement` (text)
  - `Effectiveness Window End` (date)
  - `Closeout Summary` (text)
- *Comment-thread data (not custom fields):* category (derivable from Source), root cause category (Manpower / Method / Machine / Material / Measurement / Environment — captured in RCA notes), QA Approver name + timestamp (audit trail in comment, not a field), originating task gid (a comment reference, not a field).
- *Title prefixes:* reserved for cross-skill staging where the destination skill or source skill is not yet live. In-flight state and HITL gates do not use title prefixes — they use Status and Gate.
  - **Inbound staging prefixes (from live skills):** `[CAPA Pending — capa-coordinator]` (from complaint-and-event-handler v5.1), `[CAPA Request — batch-lifecycle-tracker]` (from v5.4 batch-side fails). Retired: `[NCR Request — quality-lab-coordinator]` — went live 2026-05-08; lab inbound now arrives as direct task creation in SJS CAPA Log Inbound Staging.
  - **Inbound staging from skills not yet built:** `[CAPA Request — regulatory-manager]` (pre-v6).
  - **Outbound queue prefixes (routed via prefix to live skills):** `[SOP Revision Pending — quality-manager]` (ratification queue feed to v5.5), `[Vendor Scorecard Signal]` (rides on the purchasing-manager record, not the CAPA task).
  - **Outbound handoffs to skills not yet built:** `[Reg Flag Pending — regulatory-manager]` (pre-v6).

Once a destination or source skill goes live, its corresponding title prefix retires — that staging is no longer needed.

## Numbering

- **NCR:** `NCR-YYYY-NNN`, zero-padded, sequential by calendar year. First NCR of 2026 is `NCR-2026-001`.
- **CAPA:** `CAPA-YYYY-NNN`, same convention.
- The skill checks the highest existing number on first write each session and increments. Numbers are unique within their type — an NCR converted to a CAPA carries both numbers, linked.

## Role map

The skill reads role-holders from `references/role-map.md`. SKILL.md, references, and Asana writes all stay role-based. When a role-holder changes, only the map updates. Status field renders the SOP phase; Gate field renders the role holding the puck (`Pending Operator`, `Pending QA Lead`).

## Calls and integrations

The skill goes through other skills for source access wherever one exists. Asana is direct (this skill owns the SJS CAPA Log surface).

**Reads via:**
- plm-assistant — batch lookups, vendor lookups, SKU context, retest data
- complaint-and-event-handler — source complaint task context for `[CAPA Pending]` inbound
- outlook-asana-bridge — inbound CAPAs from retail partner audit emails or vendor escalations
- fireflies-asana-bridge — inbound from QBR / consultation calls where a CAPA gets called out
- Asana — direct read of own tasks in SJS CAPA Log
- SharePoint — SKN-OPS-001 source doc, SOP & Form Log, audit/inspection records

**Writes via:**
- Asana — direct (custom fields, comments, section moves, new tasks for handoff staging, title-prefix updates as state changes)
- sweet-july-skin-brand — applied to any external-facing CAPA output (audit response letters, retailer quality reports)

**Never duplicates:**
- complaint-and-event-handler (owns customer signal and recall comms; CAPA picks up the §4.E corrective action only)
- batch-lifecycle-tracker (owns batch hold/release; CAPA receives the batch-fail signal but doesn't decide release)
- quality-manager (owns cross-skill dashboard, QoS aggregation, SOP library — CAPA feeds the SOP revision queue)
- quality-lab-coordinator (owns vendor scorecard *signal*; CAPA comments back, doesn't write the scorecard)
- purchasing-manager (owns vendor scorecard records)
- regulatory-manager (owns reportability assessment and external filing)
- plm-assistant (only writer to PLM)

## Out of scope (v5.2)

- Customer complaint classification (complaint-and-event-handler)
- Recall comms drafting and execution (complaint-and-event-handler — CAPA picks up §4.E corrective action only)
- Vendor scorecard writes (purchasing-manager — CAPA signals via comment-back)
- Batch hold/release decisions (batch-lifecycle-tracker at v5.4)
- In-market stability monitoring (batch-lifecycle-tracker)
- Direct PLM writes (plm-assistant — only writer)
- Regulatory reportability assessment and external filings (regulatory-manager at v6)
- Audit execution (no audit skill exists; CAPA receives audit findings, doesn't run audits)
- SOP authoring beyond drafting working procedures (CAPA stages revision tasks; quality-manager owns the ratification cycle)
- Pre-launch QA (asana-pd-manager keeps)
- Cross-skill QoS dashboard (quality-manager at v5.5)
- Branded CAPA reporting beyond closeout summary (quality-status-reporter at v5.6)

## First-run setup

SJS CAPA Log was created 2026-05-09 (gid `1214660784338465`). Section GIDs and custom field GIDs cached in this SKILL.md. On first invocation:

1. Confirm the project responds (gid `1214660784338465`) and section + field GIDs match what Asana returns.
2. Confirm `references/role-map.md` is current. Canonical role-map lives in quality-manager.
3. Confirm SKN-OPS-005 (NCR Procedure) was ratified — the working draft ratified 2026-05-09; references/ncr-procedure.md is the skill-side mirror.
4. The `[SOP Revision Pending — quality-manager] SKN-OPS-001 §5 in-text gaps bundle` task in Inbound Staging (gid `1214661452219504`) is the open SOP gap surface — bundled into a future Rev.2 of SKN-OPS-001.

If any check fails, surface to the operator and stop — the skill does not modify project structure unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/skn-ops-001.md` — SKN-OPS-001 phase walk, mirrored from SharePoint with skill-side commentary on what each phase needs
- `references/ncr-procedure.md` — Non-Conformance Report (NCR) Procedure SKN-OPS-005 Rev.1 (ratified 2026-05-09)
- `references/rca-tools.md` — 5 Whys + Fishbone scaffolds (mirrors SKN-OPS-001 Appendix C)
- `references/capa-investigation.md` — CAPA investigation + action plan template (mirrors SKN-OPS-001 Appendix B)
- `references/trigger-phrases.md` — grouped triggers by intent (intake, review, RCA, action plan, verification, close, status)
- `references/role-map.md` — current role-holders for Operator, QA Lead, and Department Manager. The only place names appear in this skill.

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant pages from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as bridge skills process NCRs, CAPA correspondence, and meeting traffic. Reading them first gives this skill institutional memory about supplier NCR history and SKU non-conformance threads without re-scanning raw sources.

### Which pages to read

- Named supplier → `'supplier/' || public.wiki_slugify(vendor_name)`
- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`

Supplier pages carry NCR history, corrective-action patterns, and open CAPA items. SKU pages carry non-conformance history and root-cause threads.

### Read query

```sql
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));

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

Prepend the wiki page content to this skill's context before walking the SKN-OPS-001 phase. Treat it as the NCR/CAPA case-history briefing.

### Write-back (stale pages only)

If a page is stale or `source_count = 0` and live queries produced genuine new CAPA signal not already in the wiki, update the page:

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
