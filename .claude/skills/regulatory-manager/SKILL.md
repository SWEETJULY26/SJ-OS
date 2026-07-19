---
name: regulatory-manager
description: System C umbrella for Sweet July Skin regulatory management. Use for cross-skill regulatory rollup, registrations tracker (MoCRA, state filings, state packaging laws, EPR, Leaping Bunny, Canada / international markets), retailer attestation cadence, Pedrero + international RP partner liaison, monthly + quarterly regulatory cost rollup from vendor_invoices, ayesha-weekly-briefing founder signals. Triggers include "what's open in regulatory", "regulatory dashboard", "next attestation due", "any registrations renewing", "what's pending with Pedrero", "Canada compliance", "EPR threshold", "monthly regulatory spend", "quarterly regulatory rollup", "Pedrero spend YTD", "any disputed regulatory invoices". Owns SJS Regulatory Management Asana project. Intercepts Quality's [Reg Flag Pending — regulatory-manager] queue and fans out. Reads vendor_invoices via Supabase SELECT for cost rollups; never writes PLM. HITL on cross-skill task creation, registration writes, attestation reminders, fan-out routing.
---

# Regulatory Manager

System C umbrella. Mirrors quality-manager (System B) in shape — doesn't run a sub-skill workflow; surfaces state across all System C sub-skills, owns registrations and retailer attestation cadence, intercepts Quality's `[Reg Flag Pending — regulatory-manager]` queue and fans out, runs the Pedrero liaison surface, and feeds ayesha-weekly-briefing for founder-level signals.

**Post-build update — 2026-05-12 (Pedrero touchbase).** Registrations scope expanded to cover state packaging laws (CA SB 343 Pantone-for-recycling, 19-state packaging toxics certificate of compliance, EPR per state with revenue-threshold monitoring) and international markets (Health Canada cosmetic notification, Quebec French-language compliance) — see `references/state-packaging-laws.md` and `references/canada-compliance.md`. Pedrero liaison surface adds international RP partner liaison (Ecomundo and Pedrero's preferred alternatives — see `references/rp-partners.md`) and a capacity-planning seam for Pedrero (12-18 month PD roadmap with ~24 active projects, sent annually at engagement-letter renewal).

## Why this exists

System C had two sub-skills shipped (claims-il-and-label-keeper at v6.1, adverse-event-and-recall-reporter at v6.2). Quality (`complaint-and-event-handler`) drops `[Reg Flag Pending — regulatory-manager]` tasks into Quality. Without an umbrella, those flags get read directly by sub-skills (which works pre-v6.3 but creates fragile direct couplings), the registrations tracker has no home, retailer attestation cadence has no cross-skill view, and Pedrero liaison work scatters across sub-skill tasks. Founder-level regulatory signal doesn't surface in ayesha-weekly-briefing.

This skill closes those gaps. Tasks land in SJS Regulatory Management; structured records stay in Asana plus SharePoint (no new PLM tables per system-c-regulatory-scope.md decision I).

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**HITL on cross-skill task creation, registration writes, and attestation reminder edits.** The skill drafts and stages, never commits silently. Two roles do the gating:
- **Operator** approves intake scope confirmation, fan-out routing, registration draft contents.
- **Reg Lead (internal)** approves any cross-skill task creation, every registration write, every attestation reminder edit, every Pedrero engagement letter renewal, every fan-out routing decision. At v6.3 the Operator and Reg Lead are the same person (Alvin) — the gate still fires as a separate confirmation step so the audit trail captures both decisions.

Role-holders live in `references/role-map.md`, not in this doc. Reads (status queries, rollup pulls, Pedrero "what's pending") never confirm. Writes always do.

**No SOP — coordinator pattern.** regulatory-manager doesn't get its own ratified SOP. Mirrors quality-manager (System B). Operates per existing System C SOPs (SKN-OPS-008 IL/Claims/Label, SKN-OPS-009 Reportable Events) plus this build memo. The skill is cross-cutting infrastructure, not a workflow that needs a documented procedure.

**Asana = workflow surface. SharePoint = artifact source of truth. PLM = SKU/batch/formula source of truth.** SKU and batch records live in PLM via plm-assistant. Registration filings, agency correspondence, retailer attestation evidence, Pedrero correspondence live in SharePoint at `Sweet July/Regulatory/` (precondition; out-of-band Ops setup). v6.1/v6.2 interim Asana attachments migrate to SharePoint at v6.3 build per `references/sharepoint-pointer.md`. SJS Regulatory Management holds task signal: what needs Pedrero review, what's renewing, what's pending Reg Lead, who to talk to.

**Boundary with sub-skills — read-most, fan-out-only.** This skill never executes sub-skill workflows. Cross-skill rollup is a read of sub-skill state; fan-out is task creation in the receiving sub-skill's project. Sub-skills retain ownership of their own intake and lifecycle.

**Pedrero liaison only — never substantive review.** Pedrero (Amy Pedrero principal, Heather Folkes and Teona Bebia secondary) does all substantive review across System C. This skill manages engagement-level Pedrero work: contact card, "what's pending/sent/overdue" rollups, engagement letter renewals, scope changes, general inquiries. Filing-specific Pedrero work stays with the originating sub-skill.

**Brand scope.** Sweet July Skin only at v6.3.

**Scope → plan → approve → build.** Operations' working rule. Any change to fan-out routing rules, registration scope, attestation cadence rules, or Pedrero engagement protocol goes through the user, not committed unilaterally.

## The nine core jobs

### 1. Reg-flag intake from Quality and fan-out

Subscribe to `[Reg Flag Pending — regulatory-manager]` queue in SJS Quality Management. On each flag, Operator confirms type; skill routes to the right destination.

- *Trigger:* `[Reg Flag Pending — regulatory-manager]` lands in SJS Quality Management Inbound Staging; or operator-direct ("any reg flags waiting", "route this flag to [skill]")
- *Action:* Read source task. Pull complaint/event context, batch, SKU, severity from Quality's task and underlying SJ Skin Complaint Log entry (gid `1204763097184846`) via plm-assistant. Recommend type per:

| Flag type (Operator-confirmed) | Routes to |
|---|---|
| SAE — MoCRA | adverse-event-and-recall-reporter (creates new task in SJS Reportable Events Inbound Staging) |
| Recall (any Class) | adverse-event-and-recall-reporter |
| State AE Report | adverse-event-and-recall-reporter |
| Registration question (MoCRA listing, state cosmetic registry, Toxic-Free Cosmetics Act compliance) | this skill's own registrations queue |
| Retailer attestation issue | claims-il-and-label-keeper |
| IL or claim or label question | claims-il-and-label-keeper |
| Pedrero liaison question (general inquiry, contract, scope) | this skill's Pedrero Liaison surface |
| Other / unclear | Operator manually triages; no autoroute |

- *HITL:* Operator confirms each routing decision. Reg Lead approves any cross-skill task creation. Two distinct gates per fan-out (`Gate = Pending Operator` for routing call; `Gate = Pending Regulatory Lead` for the resulting cross-skill task creation).

**v6.2 retrofit at v6.3 build:** adverse-event-and-recall-reporter Job 1 source flips from direct read of Quality to receiving fan-out from this skill. Retrofit lands in `adverse-event-and-recall-reporter/SKILL.md` Job 1 at v6.3 build.

### 2. Cross-skill rollup (weekly Asana status + on-demand summary)

Pull state from all System C sub-skills plus this skill's own surface; publish as Asana project status update on SJS Regulatory Management. Respond to on-demand summary queries.

**What rolls up:**
- claims-il-and-label-keeper state (IL versions in flight, claim sub renewals due, label artwork pending cross-check, retailer attestations pending)
- adverse-event-and-recall-reporter state (open SAEs, open recalls, statutory clocks at 60% / 80% / 95%, agency follow-up windows)
- Own registrations tracker (active, renewal window, overdue)
- Own Pedrero liaison (what's pending, what's been sent, what's overdue per sub-skill)

**Cadence:**
- Weekly: every Monday by default, posted as Asana project status (RAG color, summary, next steps). Manual trigger anytime.
- On-demand: text summary in chat plus optional structured Asana comment on a specified task.

- *Trigger:* "what's open in regulatory", "regulatory dashboard", "where are we on regulatory", "next attestation due", "any open SAEs", "any registrations renewing", "monthly regulatory summary", scheduled Monday run
- *Action:* Pull state from each sub-skill via Asana reads; compose the rollup; post as Asana project status (weekly) or render text summary (on-demand). v6.4 handoff: regulatory-status-reporter generates the branded HTML dashboard rendering this rollup.
- *HITL:* none for the read itself.

### 3. Registrations tracker

Own the active registrations + renewal cadence for federal, state, and third-party items.

**Registration scope:**
- MoCRA cosmetic product listings (FDA registration of every SKU)
- MoCRA facility registrations (KDC-One, Vegelabs, Allure Labs, others)
- CA Prop 65
- CA Fragrance and Flavor Right to Know Act (CA SB-312 — disclosure of designated fragrance/flavor ingredients to CDPH per SKU)
- CA Toxic-Free Cosmetics Act (CA AB-2762 — banned-ingredient compliance)
- NY consumer cosmetic registry
- WA Toxic-Free Cosmetics Act (WA SB-5703 — separate from the CA statute, broader ban list, phased compliance through 2025-2026)
- OR cosmetic registry
- Leaping Bunny Certification (CCIC — third-party cruelty-free certification; tracked here because cadence behaves like a registration and ties to retailer attestations)
- Retailer-specific filings if retailer requires beyond attestation
- FDA color additive listings if applicable; FDA OTC monograph filings if any SKU goes OTC

**Dual-state Toxic-Free Cosmetics Act compliance:** both CA AB-2762 and WA SB-5703 have distinct banned-ingredient lists. SJS must comply with both. License audit (Job 7) confirms current ingredient panel against both lists.

**State packaging laws (added 2026-05-12 — see `references/state-packaging-laws.md`):**
- **CA SB 343 — Truth in Recycling Labeling.** Pantone color rules govern whether a recycling symbol can appear on packaging; dark Pantones fall outside the approved gradient. Per-SKU check against the gradient. Affects every SJS primary and secondary component plus sample units. Outcome per SKU: artwork compliant, lighten Pantone, or remove recycling symbol.
- **19-state packaging toxics — 100 ppm heavy metals certificate of compliance.** Many components-side suppliers (Elements ACT, HCT, etc.) issue these on request. Heavily enforced at Target / Walmart and major retailers; less so at DTC. Required attachment on the IL packet for retailer-distributed SKUs at v6.6 via claims-il-and-label-keeper §3 update.
- **Extended Producer Responsibility (EPR).** Live in Oregon (2025), California, Colorado; three more states joining 2026. Companies register with Circular Action Alliance (CAA), report packaging weight + material + units sold per state, pay sliding-scale fees. **SJS exempt under thresholds** at v6.6 build (CA: $1M in-state sales / general: $5M global sales). Tracked as a monitoring item only — auto-flags Operator when SJS sales projections approach threshold per the 3-year plan. CA initial-fee deadline 2026-05-31 for 2023 data (monitoring only; not actionable for SJS at current scale).

**International markets (added 2026-05-12 — see `references/canada-compliance.md`):**
- **Canada — Health Canada cosmetic notification.** Required for any cosmetic shipped to Canada including C2C / direct-to-consumer. SJS has shipped ~50/year since 2023 launch without notifications; three customs holds experienced. Regulations now require a Canadian entity or RP to file. Engaged Ecomundo (existing agreement, annual fee model) or Pedrero-recommended alternative — see `references/rp-partners.md`.
- **Canada — extended cosmetic allergens.** New labeling rule effective 2026-07-31. Sephora Canada will not accept SKUs missing the extended-allergen disclosure after 2026-07-31. Existing SKUs already on the Canadian market have until 2028 (Sephora exception aside).
- **Canada — Quebec French-language compliance.** All inscriptions on packaging (not just mandatory statements) must appear in both English and French for SKUs distributed in Quebec. Perrine handles French translation.
- **UK, South Africa — pending.** Not yet active; tracked here so Pedrero capacity planning surfaces them when the roadmap firms up.

- *Trigger:* "any registrations renewing", "what's the [SKU] MoCRA listing status", "log the [registration] filing", "Leaping Bunny renewal", inbound from regulatory authority via outlook-asana-bridge, scheduled `Window End` proximity reminder
- *Action:* Walk the registration walk per `Registration Type`. Draft the filing or renewal packet. For agency filings, hand off to Pedrero via Job 5. For non-agency items (Leaping Bunny is third-party, not an agency), Operator + Reg Lead manage internally.
- *HITL:* Operator approves the filing draft. Reg Lead approves any agency-facing or CCIC-facing send. Reg Lead approves every registration record write.

### 4. Retailer attestation cadence dashboard

Own the cross-attestation view of Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo. claims-il-and-label-keeper executes the lifecycle per SKN-OPS-008 §8; this skill surfaces the rollup.

- *Trigger:* "next attestation due", "any attestations renewing", "Sephora Clean status", "what's renewing in 30 days", scheduled `Window End` proximity reminder rollup
- *Action:* Read claims-il-and-label-keeper's attestation tasks across SJS Regulatory Management. Surface in the Cross-Skill Dashboard section as a pinned status. No duplicate task creation — claims-il-and-label-keeper owns the workflow; this is a view.
- *HITL:* none for reads. Reg Lead approves any cross-skill escalation task creation when an attestation is overdue (e.g., `[REG-CROSS] Sephora Clean attestation 14d overdue — escalation`).

### 5. Pedrero liaison surface

Cross-skill view of Pedrero work plus non-filing Pedrero engagement (contract renewals, scope changes, general inquiries).

**What lives here:**
- Pedrero contact card — pulled from `references/pedrero-contacts.md` (canonical home; sub-skill role-maps reference)
- "What's pending with Pedrero" — cross-skill rollup of open Pedrero tasks across claims-il-and-label-keeper and adverse-event-and-recall-reporter
- "What's been sent to Pedrero" — sent-to-Pedrero rollup (audit trail surface)
- "What's overdue" — overdue Pedrero return rollup with statutory-clock tightening from adverse-event-and-recall-reporter
- Pedrero engagement-letter renewal task (annual cadence; first renewal date confirmed at first-run with Operator)
- Pedrero scope-change discussions (when SJS adds new retailer, new SKU class, new geography that affects engagement scope)
- **Pedrero capacity-planning seam (added 2026-05-12).** Annual export of the SJS 12-18 month PD roadmap (~24 active projects at 2026-05-12) to Pedrero ahead of engagement-letter renewal so Pedrero can size review capacity. Runs alongside the engagement-letter renewal task; sourced from asana-pd-manager portfolio reads.
- **International RP partner liaison (added 2026-05-12).** Mirror of the Pedrero liaison shape, scoped to country-specific responsible-person partners. Contact catalog and engagement state live in `references/rp-partners.md`. Current entry: Ecomundo (Canada / EU notifications, existing agreement on annual-fee model). Pedrero introduces additional partners as country scope expands. The skill tracks pending/sent/overdue per partner the same way it tracks Pedrero.

- *Trigger:* "what's pending with Pedrero", "what's been sent to Pedrero", "any overdue Pedrero items", "Pedrero engagement renewal", "Pedrero contact info", "what's pending with Ecomundo", "send the PD roadmap to Pedrero"
- *Action:* For rollup queries, read across sub-skills. For engagement work, draft locally; stage Pedrero send via Job 4 of claims-il-and-label-keeper or adverse-event-and-recall-reporter Job 4 if the engagement work ties to a specific filing. For pure engagement (annual letter renewal, capacity planning roadmap, general inquiry, RP partner correspondence), Operator drafts; Reg Lead approves; outlook-asana-bridge stages send. For international RP partner traffic that crosses a filing (Health Canada notification, EU CPNP, etc.), pattern matches Pedrero: this skill manages engagement-level work, filing-specific work routes to the originating sub-skill.
- *HITL:* Reg Lead approves every Pedrero send and every RP partner send for engagement work. Operator hits send manually.

### 6. ayesha-weekly-briefing seam

Surface founder-level regulatory signals into the weekly briefing.

**Founder-level signals:**
- MoCRA SAE filing in flight or recent (within 30 days)
- FDA recall in flight or recent (within 60 days)
- Statutory clock breach risk (any filing >80% of clock without Pedrero return)
- Retailer attestation overdue or imminent (within 30 days of renewal window)
- Pedrero engagement issues (overdue retainer, scope change, contract renewal)
- New regulatory landscape change (MoCRA implementation update, new state cosmetic regulation, retailer attestation criteria revision, Toxic-Free Cosmetics Act enforcement update)
- Canada compliance gate at 60/30/14-day proximity to 2026-07-31 Sephora deadline; any new customs hold on a Canada-bound shipment
- EPR sales-threshold proximity (auto-fires when 12-month-trailing or projected sales reach 80% of $5M global / $1M in-state CA)
- New state packaging law action (CA SB 343 Pantone fail on a SKU, missing 100 ppm toxics cert at a retailer audit)
- New international market scope add (Pedrero introduces an RP partner for a new country)

- *Trigger:* ayesha-weekly-briefing pulls regulatory rollup at its weekly scheduled run; or operator-direct ("any founder-level regulatory items this week")
- *Action:* Compose the founder filter from sub-skill state plus own registrations and Pedrero state. Surface as "Regulatory" subsection in the briefing.
- *HITL:* none for reads. The briefing surfaces; Operator and Founder act on the signals separately.

### 7. License/certification audit (post-build, Operator-led)

Once v6.3 is live, the skill helps Operator run the team license audit to load the full inventory of active SJS registrations, state filings, federal filings, and third-party certifications.

- *Trigger:* operator-direct ("run the license audit", "what registrations are we missing", "audit our regulatory coverage")
- *Action:* Walk the `Registration Type` enum. For each type, query: do we have an active filing? When does it renew? Where's the evidence? Surface gaps. Help Operator draft the discovery questions for the team.
- *HITL:* every registration record created from audit findings is a Reg Lead gate.

**Seeded items at first invocation (already known at v6.3 build):**
- **CA Fragrance and Flavor Right to Know Act** — migrate from existing Asana task `1211320433655582` (currently in AC Brands PD + Ops Dashboard → Rollover/Risks, overdue from 2025-09-30). Set `Registration Type = CA Fragrance and Flavor Right to Know`, populate context, close originating task with comment-back.
- **Leaping Bunny renewal** — load with `Registration Type = Leaping Bunny Certification`, `Filing Cycle = Annual`, `Window End = 2026-07-10`. The 60-day reminder fires 2026-05-11; skill flags as imminent.

**Seeded items added post-build (2026-05-12 Pedrero touchbase):**
- **Canada extended-allergens compliance** — `Canada — Extended Allergens — 2026` in Registrations — Renewal Window. `Registration Type = Health Canada Notification`, `Filing Cycle = Per-Product-Launch`, `Window End = 2026-07-31`. 60-day reminder fires 2026-06-01. Tied to Sephora Canada acceptance cutoff. Status starts as `Inbound Staging — Pedrero scoping RP partner` (Ecomundo or alternative); flips to `In Pedrero Review` once RP partner is engaged.
- **Health Canada cosmetic notification — backlog** — one task per active in-market SJS SKU shipped to Canada since 2023. Set `Registration Type = Health Canada Notification`, `Filing Cycle = Per-Product-Launch`. Status `Inbound Staging`; Operator works through with Pedrero / Ecomundo. Customs-hold history attaches as evidence.
- **Quebec French-language compliance — portfolio sweep** — one parent task `Quebec French-Language Compliance — Portfolio Sweep — 2026`, subtasks per SKU. `Registration Type = Quebec French-Language Compliance`. Triggers a label cross-check in claims-il-and-label-keeper for any SKU not yet bilingual.
- **CA SB 343 Pantone audit — portfolio sweep** — one parent task `CA SB 343 — Pantone Audit — 2026`, subtasks per primary and secondary component plus Z Pack sample units. `Registration Type = CA SB 343 Recycling Labeling`. Heather Folkes at Pedrero supplies the approved Pantone gradient; Alvin supplies artwork Pantones. Outcome per SKU: pass, lighten, or remove recycling symbol.
- **19-state packaging toxics — certificate of compliance sweep** — one parent task `Packaging Toxics — 19 State — Cert of Compliance — 2026`, subtasks per active component supplier (Elements ACT, HCT, Impress, CDW, etc.). `Registration Type = Packaging Toxics — 19 State`. Pedrero (Heather) supplies request verbiage for vendors. Closed when every active component supplier has issued a current cert.
- **EPR threshold monitor** — single task `EPR — Threshold Monitor — Annual`. `Registration Type = EPR — Monitoring`. No filing; auto-checks trailing-12 and forecast sales against $5M global / $1M in-state CA. Fires founder signal at 80% of threshold. Revisit at every 3-year-plan refresh per Operator decision at 2026-05-12 touchbase.
- **Pedrero engagement-letter renewal + capacity planning** — engagement-letter renewal already lives in Pedrero Liaison section; at v6.6 it gets a sibling task `Pedrero — Capacity Planning Roadmap Send — Annual`. Annual send of the 12-18 month PD roadmap (~24 active projects at 2026-05-12) so Amy can size review capacity. Sourced from asana-pd-manager portfolio reads.

### 8. Monthly regulatory cost rollup

Read `vendor_invoices` directly via Supabase SELECT, aggregate the prior month's regulatory spend, surface as a three-way rollup: Asana project status comment, regulatory-status-reporter spend strip feed, ayesha-weekly-briefing data source.

**Source.** `vendor_invoices` populated by outlook-plm-bridge Flow I, committed via plm-assistant after purchasing-manager Job 9's HITL gates. This skill reads only — no writes.

**Scope filter.** Rollup totals include every row where `cost_category = 'regulatory'` OR `regulatory_driver = true`. The composite index `idx_vendor_invoices_regulatory_rollup (invoice_date, cost_category, regulatory_driver)` exists for exactly this hot path.

**Aggregations:**

- **Total spend** — sum(amount) USD-normalized for the calendar month.
- **By cost_category** — six buckets even though regulatory_driver pulls in quality, pd, ops, and marketing rows. Surfaces where regulatory cost is hiding outside the regulatory bucket.
- **By vendor** — top 5 vendors by spend that month. Pedrero, Ecomundo, Eurofins, Q-Labs, AMR Labs typically.
- **PET / RIPT / CPSR / Notification split** — sub-aggregation for regulatory_driver rows, parsed from `notes` or `attachment_filename` keywords. Used for capacity-planning conversations with Pedrero.
- **Disputed total** — sum(amount) where `state = 'disputed'` for cross-flag context.

**Cadence.** First business day of the month covers the prior calendar month. Scheduled via the existing sjs-regulatory-morning-sweep / sjs-regulatory-weekly-digest pattern — add monthly cron alongside.

**Three surfaces:**

1. **Asana project status comment.** On the SJS Regulatory Management project, post a monthly status with rollup totals, vendor breakdown, and any disputed-invoice flags. Comment, not status update (status is the weekly RAG; this is a separate monthly post).
2. **regulatory-status-reporter feed.** v6.7 spend strip reads this rollup via the existing Netlify Function pattern (sjs-regulatory-rollup.js extended with a monthly spend block). No new function — extend the existing one.
3. **ayesha-weekly-briefing data source.** Briefing's Regulatory subsection pulls the trailing-12 trend from this rollup; not the full breakdown. Founder-level signal: month-over-month variance > 25%, disputed-invoice count, or single-vendor spike > 40% of monthly total.

- *Trigger:* "monthly regulatory spend", "what did we spend on regulatory last month", "Pedrero spend YTD", "any disputed regulatory invoices", scheduled first-business-day monthly run
- *Action:* Direct Supabase SELECT against `vendor_invoices` with the regulatory scope filter. Compose three rollup outputs (Asana comment, feed for regulatory-status-reporter, briefing data). No writes outside the Asana comment.
- *HITL:* none — read-only operation. The comment posts after Operator confirmation only on first monthly run (to validate format); subsequent monthly runs auto-post.

### 9. Quarterly regulatory cost rollup

Same shape as Job 8, calendar-quarter window, deeper analysis. Surfaces alongside the quarterly portfolio reviews (sjs-margin-portfolio-review cadence) so regulatory spend has a parallel cadence-aligned view.

**Scope filter.** Same as Job 8 (`cost_category = 'regulatory'` OR `regulatory_driver = true`) over the prior calendar quarter.

**Aggregations on top of Job 8 base:**

- **Quarter-over-quarter variance** — current quarter vs. prior quarter total spend, by cost_category bucket.
- **Year-over-year variance** — current quarter vs. same quarter prior year (for 2026 onward — 2026-Q2 vs. 2025-Q2, etc.).
- **Per-SKU regulatory cost** — when `linked_sku_id` is set, sum by SKU. Feeds margin pressure-test conversations: a SKU carrying $40K of quarterly regulatory cost is a different unit-economics question than one carrying $4K.
- **Country split** (where parseable from notes / vendor) — US, Canada, EU, UK, Other. Surfaces international expansion cost growth.

**Cadence.** First business day after quarter close (Apr 1 for Q1, Jul 1 for Q2, Oct 1 for Q3, Jan 2 for Q4). Scheduled alongside the monthly cron.

**Three surfaces (same as Job 8 plus one):**

1. **Asana project status comment** — quarterly post with full breakdown and variance commentary.
2. **regulatory-status-reporter feed** — v6.7 spend strip's quarterly tooltip drill-down reads from this rollup.
3. **ayesha-weekly-briefing data source** — first weekly briefing after quarter close surfaces the QoQ headline as a founder signal.
4. **sjs-status-reporter handoff** — when Alvin runs the quarterly review deck, this rollup feeds the regulatory spend slide. Hand off via the standard sjs-status-reporter data source pattern.

- *Trigger:* "Q[N] regulatory spend", "quarterly regulatory rollup", "regulatory cost by SKU this quarter", "international regulatory cost split", scheduled quarterly run
- *Action:* Direct Supabase SELECT with quarter window + scope filter. Compose three (or four) surface outputs. Hand off the quarterly slide data to sjs-status-reporter when invoked for the quarterly review deck.
- *HITL:* none for the read. Operator confirms format on first quarterly run; subsequent quarterly runs auto-post.

## Asana surface

- *Project:* **SJS Regulatory Management** — Operations team, public to workspace. Created 2026-05-09 at v6.1 build (claims-il-and-label-keeper); regulatory-manager takes ownership at v6.3.
  - Project GID: `1214660807386611`
  - Project URL: https://app.asana.com/1/1200120716421441/project/1214660807386611
  - Team (Operations) GID: `1200120716421443`
  - Portfolio (Operations Dashboard): `1208174221370391` — **manual add pending** (no MCP tool exposes portfolio-add at v6.3 build)

### Sections (cached 2026-05-09)

| Section | GID | Purpose |
|---|---|---|
| Inbound Staging | `1214661463988658` | (v6.1) new IL packets, new claims, attestation drafts, label artwork inbound + (v6.3) Operator-confirmed Quality reg flags awaiting fan-out |
| In Pedrero Review | `1214661463988659` | (v6.1) sent to Pedrero, awaiting return |
| Returned — Action Required | `1214661463988660` | (v6.1) Pedrero kicked back; internal action needed |
| Active / In-Effect | `1214661463988661` | (v6.1) approved IL versions, active claim sub files, archived label artwork, submitted attestations |
| Renewal Window | `1214661463988662` | (v6.1) 60/30/14-day windows on attestations, IL re-review, registrations |
| Closed | `1214661463988663` | (v6.1) superseded, expired, terminal |
| Registrations — Active | `1214660230826186` | (v6.3) current active filings per agency per SKU |
| Registrations — Renewal Window | `1214660230826187` | (v6.3) coming due; driven by Window End. Same 60/30/14-day reminder pattern as v6.1 attestations |
| Pedrero Liaison | `1214660230826188` | (v6.3) non-filing-specific Pedrero engagement work |
| Cross-Skill Dashboard | `1214660230826189` | (v6.3) non-task project section pinned with the rollup as a status update; same pattern as quality-manager `SOP Catalog` |

### Custom fields (cached 2026-05-09)

All v6.1 fields exist on SJS Regulatory Management. Canonical GID + option-GID reference: `/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md`. Three v6.3 fields pending Operator UI add at first-run (see `asana-field-gids.md` "Pending — added at v6.3 first-run setup" subsection).

**v6.1 fields the skill uses (already cached):**
- `Artifact Type` (single-select) — values include `Registration / Filing` and `Pedrero Liaison`, both reused at v6.3 with no change
- `Linked SKU` (text — shared across SJS Quality Management, SJS CAPA Log, SJS Regulatory Management, SJS Reportable Events)
- `Linked Batch` (text — shared field, same gid across projects)
- `Version / Reference` (text — registration filing ID, Leaping Bunny cert number, etc.)
- `Retailer / Agency` (single-select) — includes `FDA`, `CA`, `NY`, `WA`, `OR`, `Leaping Bunny`, `Other`, `N/A`
- `Window End` (date — renewal/re-review date)
- `Gate` (single-select, shared field) — uses `Pending Regulatory Lead` for cross-skill writes; uses `Pending QA Lead` only for cross-cutting overlaps with Quality

**v6.3 fields (cached 2026-05-09):**
- `Registration Type` (single-select, gid `1214660230826190`, 13 values) — see `asana-field-gids.md` for full option gids. Operator added `Credo Clean` and `Sephora Clean` as explicit retailer-cert values instead of generic `Retailer-Specific`. NY Cosmetic Registry not in current option set; add if SJS launches in NY. Two values carry whitespace typos (`OR Cosmetic Registry` leading space; `CA Toxic-Free Cosmetics Act` trailing space) — flagged for cleanup but functional.
- `Filing Cycle` (single-select, gid `1214660230826205`, 5 values: One-time, Continuous, Per-Product-Launch, `Biennial,` (trailing comma typo), Annual)
- `Pedrero Engagement` — **not yet added.** Skill operates degraded on Pedrero Liaison section tasks: engagement type lives in description free-text until field is added.

**Post-build field additions (2026-05-12, pending Operator UI add):**
- `Registration Type` — new option values to add: `CA SB 343 Recycling Labeling`, `Packaging Toxics — 19 State`, `EPR — California`, `EPR — Oregon`, `EPR — Colorado`, `EPR — Monitoring`, `Health Canada Notification`, `Quebec French-Language Compliance`. Operator adds via Asana UI before any of the new seeded tasks land; skill falls back to `Retailer-Specific` plus descriptive title until the option exists.
- `RP Partner` (proposed, single-select) — new field to mirror `Pedrero Engagement` for non-Pedrero RP partners. Values: `Pedrero`, `Ecomundo`, `Other`. Defer add until the second non-Pedrero RP relationship lands; until then, partner name lives in description.

*Title prefixes:*
- **Inbound from Quality (read-only):** `[Reg Flag Pending — regulatory-manager]` — read from SJS Quality Management; this skill creates downstream tasks per §1 fan-out, never modifies the Quality source task
- **Outbound cross-skill staging:** `[REG-CROSS]` for cross-skill tasks that span multiple System C skills (e.g., `[REG-CROSS] FDA inspection prep`, `[REG-CROSS] Sephora Clean attestation 14d overdue — escalation`)

## Numbering

- **Registration:** one task per registration per agency per SKU per cycle, titled `[REGISTRATION TYPE] — [SKU] — [YEAR]` (e.g., `MoCRA Listing — CST-CRM — 2026`, `CA Prop 65 — CST-CRM — 2026`).
- **MoCRA Facility Registration:** one task per facility per cycle, titled `MoCRA Facility — [VENDOR] — [YEAR]` (e.g., `MoCRA Facility — Vegelabs — 2026`).
- **Leaping Bunny:** annual renewal, titled `Leaping Bunny — Renewal — [YEAR]`. First load: `Leaping Bunny — Renewal — 2026` with `Window End = 2026-07-10`.
- **Pedrero Liaison:** one task per engagement item, titled `Pedrero — [ENGAGEMENT TYPE] — [DATE]` (e.g., `Pedrero — Engagement Letter Renewal — 2026-08-01`).
- **Cross-skill task:** title prefix `[REG-CROSS]` plus descriptive suffix.

## Role map

The skill reads role-holders from `references/role-map.md`. regulatory-manager becomes the canonical home of the System C role definition; sub-skill role-maps (claims-il-and-label-keeper, adverse-event-and-recall-reporter) reference it. Update protocol and rationale match the System B sibling pattern.

## Calls and integrations

Cross-skill rollup is read-most. Pedrero traffic is mostly Outlook; outlook-asana-bridge does heavy work. Asana is direct (this skill owns the SJS Regulatory Management surface at v6.3).

**Reads via:**
- claims-il-and-label-keeper — IL/claim/label/attestation task state in SJS Regulatory Management; rollup composition for cross-skill dashboard
- adverse-event-and-recall-reporter — SAE/recall task state in SJS Reportable Events (gid `1214660834583706`); statutory clock surface for ayesha-weekly-briefing
- complaint-and-event-handler — `[Reg Flag Pending — regulatory-manager]` queue in SJS Quality Management; SJ Skin Complaint Log (gid `1204763097184846`) for source context on fan-out
- quality-manager — SOP catalog query (current revision of System C SOPs SKN-OPS-008, SKN-OPS-009)
- asana-pd-manager — Pedrero contact catalog source per system-c-regulatory-scope.md decision K
- plm-assistant — SKU lookups for registration scope, batch context for filing-affected SKUs
- Supabase direct SELECT — read-only `vendor_invoices` for Jobs 8 + 9 monthly + quarterly cost rollups. No round-trip through plm-assistant for reads; writes are out of scope for this skill.
- purchasing-manager — upstream classifier; this skill's rollups see only invoices that purchasing-manager Job 9 HITL-approved and plm-assistant committed
- outlook-asana-bridge — inbound Pedrero replies on engagement work; inbound retailer/regulatory authority correspondence on registration items
- fireflies-asana-bridge — inbound from regulatory strategy calls, Pedrero strategy calls, retailer compliance calls
- Asana — direct read of own tasks in SJS Regulatory Management
- SharePoint — `Sweet July/Regulatory/` folder per `references/sharepoint-pointer.md`

**Writes via:**
- Asana — direct (custom fields, comments, section moves, new tasks for fan-out and registrations)
- adverse-event-and-recall-reporter via task creation in SJS Reportable Events Inbound Staging (fan-out per §1)
- claims-il-and-label-keeper via task creation in SJS Regulatory Management (fan-out per §1; same project, different sections)
- ayesha-weekly-briefing — exposes regulatory rollup as a data source per `ayesha-weekly-briefing/SKILL.md` data sources block (seam installed at v6.3 build)
- outlook-asana-bridge — Outlook draft staging for Pedrero engagement work (HITL on send; skill drafts, never sends autonomously)

**Never duplicates:**
- claims-il-and-label-keeper (owns IL/claim/label/attestation lifecycle per SKN-OPS-008)
- adverse-event-and-recall-reporter (owns SAE/recall agency filings per SKN-OPS-009)
- regulatory-status-reporter (v6.4 — owns branded HTML dashboard rendering and snapshot outputs)
- complaint-and-event-handler (owns customer complaint intake; cross-flags here via `[Reg Flag Pending — regulatory-manager]`)
- quality-manager (owns SOP catalog, cross-skill quality dashboard)
- plm-assistant (only writer to PLM)

## Out of scope (v6.3)

- Branded HTML regulatory dashboard rendering — regulatory-status-reporter v6.4
- Cross-system regulatory router queries — sjs-regulatory-system v6.5
- Sub-skill workflow execution (claims-il-and-label-keeper and adverse-event-and-recall-reporter own their own intake and lifecycle)
- Substantive regulatory review or filing drafting (Pedrero, Ecomundo, or country-specific RP partner owns)
- International expansion outside Canada (UK, South Africa, EU) — tracked for capacity planning only; activates when Pedrero introduces an RP partner and Operator confirms scope
- Direct PLM writes — plm-assistant
- Drafting agency packets (adverse-event-and-recall-reporter owns)
- Drafting attestation responses (claims-il-and-label-keeper owns)
- Authoring SOPs (System C SOPs ratified at v6.1 / v6.2; this skill operates per existing suite)
- HTML dashboard, CSS, JS, Netlify Function, `data/links.json` edit on `acb-thelanding` — regulatory-status-reporter v6.4 deliverable

## First-run setup

Project, v6.1 sections, v6.1 custom fields stood up at v6.1 build (2026-05-09). regulatory-manager takes ownership at v6.3. New v6.3 sections + fields require Operator UI add before first task write. On first invocation:

1. **Confirm Asana state matches cached gids.** Re-pull SJS Regulatory Management via Asana MCP and confirm v6.1 sections + fields match what's documented above.
2. **Confirm v6.3 Asana setup.** v6.3 sections + Registration Type + Filing Cycle fields cached as of 2026-05-09. Pedrero Engagement field not yet added — flag to Operator if Pedrero Liaison section tasks need engagement-type categorization beyond description free-text.
3. **Re-pull on field/section changes.** If sections or fields change post-build, re-pull via Asana MCP and update `asana-field-gids.md` plus this SKILL.md.
4. **Confirm portfolio.** Confirm SJS Regulatory Management is on Operations Dashboard portfolio (gid `1208174221370391`). Manual UI step.
5. **Confirm SharePoint folder.** Confirm `Sweet July/Regulatory/` exists per `references/sharepoint-pointer.md`. If missing, surface to Operator and pause attachment migration; v6.1/v6.2 interim Asana attachments stay on Asana tasks until folder exists.
6. **Confirm role-map.** Confirm `references/role-map.md` is current with the operator. Check that sub-skill role-maps (claims-il-and-label-keeper, adverse-event-and-recall-reporter) point to this skill as canonical System C role home.
7. **Seed CA Fragrance and Flavor Right to Know.** Migrate task `1211320433655582` from AC Brands PD + Ops Dashboard → Rollover/Risks into SJS Regulatory Management Registrations — Active. Set `Artifact Type = Registration / Filing`, `Registration Type = CA Fragrance and Flavor Right to Know`, populate context (overdue from 2025-09-30 — load with prior overdue state visible). Comment-back on originating task pointing to new home; close originating task. **HITL:** Operator approves migration; Reg Lead approves the close comment.
8. **Seed Leaping Bunny renewal.** Create task `Leaping Bunny — Renewal — 2026` in Registrations — Renewal Window. Set `Artifact Type = Registration / Filing`, `Registration Type = Leaping Bunny Certification`, `Retailer / Agency = Leaping Bunny`, `Filing Cycle = Annual`, `Window End = 2026-07-10`. 60-day reminder fires 2026-05-11; skill flags as imminent on first invocation. **HITL:** Reg Lead approves task creation.
9. **Confirm v6.2 retrofit landed.** Read `adverse-event-and-recall-reporter/SKILL.md` Job 1; confirm source has flipped from direct read of Quality to fan-out from this skill.
10. **Confirm ayesha-weekly-briefing seam landed.** Read `ayesha-weekly-briefing/SKILL.md` data sources block; confirm regulatory-manager is listed as a data source and the founder filter has a "Regulatory" category.

If any check 1-10 fails, surface to the operator and stop — the skill does not modify project structure or shipped sibling skills unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/role-map.md` — current role-holders for Operator, Reg Lead, External Reg Partner, QA Lead, Voice of Customer; canonical System C role-map home
- `references/trigger-phrases.md` — grouped triggers by intent (intake/fan-out, rollup, registrations, attestation cadence, Pedrero liaison, ayesha seam, license audit, status)
- `references/pedrero-contacts.md` — canonical Pedrero contact card (Amy Pedrero principal, Heather Folkes and Teona Bebia secondary); sub-skill role-maps reference this file
- `references/sharepoint-pointer.md` — SharePoint regulatory folder structure pointer at `Sweet July/Regulatory/`; v6.1/v6.2 attachment migration plan
- `references/rp-partners.md` — canonical international RP partner catalog (Ecomundo and Pedrero-recommended alternatives); mirrors `pedrero-contacts.md` shape. Added 2026-05-12.
- `references/state-packaging-laws.md` — CA SB 343 Pantone gradient rules, 19-state packaging toxics certificate of compliance with retailer enforcement notes, EPR state-by-state status with thresholds and deadlines. Added 2026-05-12.
- `references/canada-compliance.md` — Canada Health Canada cosmetic notification scope, extended-allergens deadline 2026-07-31 with Sephora cutoff, Quebec French-language requirement, Canadian-entity / RP requirement, customs-hold history. Added 2026-05-12.

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant pages from `public.wiki_pages`. Wiki pages are synthesized regulatory briefings that compound as bridge skills process Pedrero emails, IL packets, attestation responses, and meeting traffic. Reading them first gives this skill institutional memory about each SKU's regulatory state and the Pedrero artifact trail.

### Which pages to read

- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`
- Pedrero (always, when work is regulatory in nature) → `'supplier/pedrero-regulatory'`

SKU pages carry regulatory status, IL review history, claim substantiation notes, and label versions. The Pedrero page carries the artifact trail, open items, and filing history.

### Read query

```sql
-- SKU page
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'sku/' || public.wiki_slugify('{sku_code_or_product_name}'));

-- Pedrero (always)
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/pedrero-regulatory');
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before generating its response. Treat the SKU page as the regulatory case file and the Pedrero page as the active correspondence trail.

### Write-back (stale pages only)

If a page is stale or `source_count = 0` and live queries produced genuine new regulatory signal not already in the wiki, update the page:

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
