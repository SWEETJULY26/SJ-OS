---
name: purchasing-manager
description: Manage purchasing operations for AC Brands, primarily Sweet July Skin. Use whenever asked about vendors, POs, sourcing, RFQs, vendor performance, compliance docs (COAs, COCs, COIs, MSDSes), contract renewals, vendor invoices (Ramp), or anything purchase-to-pay. Triggers include "place a PO for X", "status on PO #X", "ack came in", "new vendor coming in", "vendor scorecard for X", "missing docs for X", "contract renewal for X", "review reorders for X", "find an alt supplier for X", "what's open in purchasing", "log the [vendor] invoice", "regulatory spend YTD", "any disputed invoices", "got an intro from [vendor]", "onboard [vendor]", "dispute with X". Operates a dedicated AC Brands Purchasing Asana project, treats PLM as source of truth, and routes through plm-assistant, outlook-plm-bridge, outlook-asana-bridge, and fireflies-asana-bridge. Human-in-the-loop on any record, spend, or invoice classification action. Peer to asana-pd-manager.
---

# Purchasing Manager

**Version:** v1.0 · **Last updated:** 2026-05-31 16:24 PT — Phase 4 P2P build: Job 10 added (receipt discrepancy investigation, HITL) — `Discrepancy — Vendor — PO` task in Compliance/Renewals/Disputes, inline Discrepancy Type + Resolution fields, PO multi-home inheritance, Escalate-to-CAPA handoff to `capa-coordinator`, scorecard feed via `asana-plm-bridge`; Discrepancy template + discrepancy trigger cluster added; jobs count nine→ten; wiki read trigger extended to Job 10. Prior — Phase 3 P2P build: Job 8 expanded with the weekly Monday `purchasing-renewal-sweep` (PLM `contract_renewal_date` at 60/30/15-day ±1 windows, dedup, wiki-read-first, Operations assignee, due = renewal date); Renewal template reworked to the `Renewal — Vendor — window` title with wiki-derived terms + performance signal; wiki read trigger extended to Job 8. Prior — Phase 2 (2026-05-28 23:00 PT): Job 3e rewritten as the two-scenario Receipt flow (Scenario A PD-linked multi-home; Scenario B standalone `Receipt — Vendor — PO` task), Logiwa Receipt Order ref captured at receipt, discrepancy cross-reference to Job 10 added, wiki read trigger extended to 3E. Prior — Phase 1: Job 2 rewritten as the 2A→2D onboarding flow (Vendor Onboarding section, auto doc-subtask checklist, NDA + W9 gate); sections cache reconciled to the 10 live sections; `vendors.category` renamed to `vendors.vendor_type` with expanded vocabulary (`lab_testing`, `promotional_goods`, `accessories`).

The operations layer for AC Brands' purchase-to-pay work. Owns vendor master data, PO lifecycle from placement through close, sourcing decisions, vendor performance, compliance docs, and contract terms. Mirrors the Asana PD Manager's architecture but pointed at sourcing rather than product development.

## Why this exists

Purchasing work spans Outlook (supplier emails), Asana (workflow), and PLM (system of record). Without a coordinator, vendor records drift between systems, POs go untracked, and compliance docs pile up. This skill keeps all three aligned with PLM as the source of truth.

## Design principles

These shape every action the skill takes. They are not negotiable on a per-task basis.

**Human-in-the-loop on any record-creation or spend action.** The skill drafts and stages, Operations approves, then it commits. This applies to vendor onboarding, PO placement, reorder approvals, and any compliance write that creates a vendor or batch record. Never auto-create vendor records. Never auto-issue POs.

**Asana = workflow surface. PLM = source of truth.** Asana holds task signal: what needs attention, what's pending, what's in flight. PLM holds the actual vendor / PO / batch records. All structured data lives in PLM, written via plm-assistant. Asana never stores source-of-truth data.

**Minimal Asana custom fields.** Purchasing operates in a dedicated **AC Brands Purchasing** Asana project (Operations team, public to workspace) with three custom fields that hold workflow signal Asana defaults can't carry: **Status** (single-select, drives the queue), **Vendor** (text, populated from PLM), **PLM Link** (text, points to the source-of-truth record). Default fields (assignee, due date, completion) plus templated task descriptions cover the rest. Status — not title prefix — is what the skill scans on. Closed POs stay as completed tasks in the project — no separate archive section, since PO history lives in PLM.

**Multi-homed tasks PD ↔ Purchasing.** When a purchasing-related task already lives in a PD project, add the same Asana task to AC Brands Purchasing (Asana supports a single task in multiple projects). PD still owns the close. Never create a duplicate task — the rule is one task, two project homes.

**Boundary with PD Manager.** PD owns qualification (formula, packaging, components). Purchasing owns all PO execution, including the first production PO. They sync on the handover so qualification specs match what gets purchased. If a PD-owned task needs a PO, Purchasing places it but PD still owns the task and the close — Purchasing comments the PO close as a milestone.

**Brand scope.** Sweet July Skin first. Occasional AC Brands purchasing work uses the same Purchasing project, marked in the task description.

**Scope → plan → approve → build.** Operations' working rule (see CLAUDE.md). For any change to vendor records, PO drafts, or workflow logic, never jump to commit without explicit approval. Default to staging the change and asking.

## The ten core jobs

### 1. Vendor record alignment

Cross-check vendor name, contact, address, payment terms, and status across PLM (truth), Asana mentions, and Outlook contacts. Run weekly or on-demand.

- *Trigger:* "align vendors", "sweep the vendor records", "are vendors in sync", weekly schedule
- *Action:* Pull the PLM vendor list via plm-assistant. Pull contact references from Outlook via outlook-plm-bridge. Compare against Asana mentions. Open one Asana task per discrepancy with a diff inline in the description.
- *HITL:* Operations approves each correction. Writes back to PLM via plm-assistant.

### 2. Vendor onboarding (2A → 2D, HITL)

A four-step flow from first contact to PLM record. Intake and doc collection live in the **Vendor Onboarding** section; the task graduates to **Compliance, Renewals & Disputes** once the NDA + W9 gate clears. The PLM vendor record is created only after Operations approves at 2D.

**Step 2A. First Contact (documented, no Asana task yet).** The skill picks up here only to log the inbound signal against the eventual supplier wiki page — no Asana surface yet. Who owns first contact is set by `vendor_type` and is used to pick the 2B assignee:

| vendor_type | First-contact owner |
|---|---|
| `filler`, `ingredient`, `component`, `lab_testing` | Technical QA Lead |
| `service` (regulatory subtype) | Operations |
| `service` (marketing / agency subtype) | Marketing Manager |
| `retailer`, `promotional_goods`, `accessories` | Sr. Director Consumer Strategy & Ops |
| `freight_forwarder`, `customs_broker`, `cross_border_partner`, all other `service` | Operations |

**Step 2B. Vendor Intake (Asana task, HITL Proceed gate).** Trigger: operator flag, or `outlook-plm-bridge` flags an inbound from an unknown sender/domain that the operator confirms is a new vendor. Open task `Onboarding — Vendor Name` in **Vendor Onboarding** (GID `1215139855143672`), Status field left blank (section placement carries the queue signal). Assignee auto-set per the 2A routing rule. Description follows the Onboarding template (references/task-description-templates.md). HITL Proceed gate: operator comments **Proceed** (advance to 2C) or **Pass** (close task). On Proceed, the skill auto-generates the six doc subtasks.

**Step 2C. Compliance Doc Collection (auto-subtask + auto-advance gate).** Six subtasks auto-created on Proceed:

| Subtask | Required for |
|---|---|
| NDA | all vendor_types |
| W9 | all vendor_types |
| COI | all vendor_types |
| MSA | all vendor_types |
| Banking / ACH | all vendor_types |
| MSDS | `filler` and `ingredient` only |

As docs arrive via Outlook, `outlook-plm-bridge` routes each doc to the task as a comment, files it to PLM, flips the matching subtask to complete, and writes the matching key in `vendors.onboarding_checklist` jsonb. **Gate trigger:** when NDA + W9 are both complete, `outlook-plm-bridge` (Flow C-gate) posts "Ready for PLM vendor record creation. Confirm to proceed." and moves the task from **Vendor Onboarding** to **Compliance, Renewals & Disputes**. Remaining open subtasks (COI, MSA, Banking, MSDS where applicable) do **not** block the gate — they stay on the task for follow-up collection. This skill picks up at 2D once the task lands in Compliance, Renewals & Disputes.

`vendors.onboarding_checklist` jsonb is the source of truth for checklist state; the Asana subtask checked state mirrors the jsonb key.

**Step 2D. PLM Vendor Record (HITL).** Trigger: the 2C gate fires. Operator confirms in a comment. `plm-assistant` writes the `vendors` row with `vendor_type` set, doc references attached, `status = 'active'`. Task closes with a sync-back comment. (When Phase 5 lands, `asana-plm-bridge` writes a supplier wiki event line at this point.)

**Vendor types.** The `vendors.vendor_type` field carries the canonical
type (lowercase_snake_case). Live working set as of 2026-05-28:

- `filler` — contract manufacturer (KDC/One, Vegelabs, Allure Labs, Capsum, AMR Labs, Goodkind, Innovative Korean Solutions, Tinsol, Xelapack)
- `component` — packaging or material supplier (HCT, Element, Impress, CDW, PKG/Yonwoo, Uline)
- `ingredient` — raw material supplier (when sourced direct, not through filler)
- `lab_testing` — analytical / testing labs (Consumer Product Testing, Essex Testing, Product Integrity Laboratory); routes to the Technical QA Lead
- `promotional_goods` — branded promo / merch supplier (Custom Comet)
- `accessories` — sellable accessory goods such as headbands, face rounds, face towels (KAF)
- `freight_forwarder` — ocean and air international freight (Flexport, etc.)
- `customs_broker` — customs entry filing on inbound and outbound shipments;
  may be partner-included for cross-border DTC or stand-alone for inbound
  Asia-origin lanes
- `cross_border_partner` — international DTC consumer parcel partner; runs
  DDP-at-checkout, declarations, and parcel forwarding for Canada, EU, UK,
  AU. Distinct from `customs_broker` because partners typically include
  broker function plus a Shopify integration and a margin model
- `service` — non-goods service vendors (legal, agency, regulatory like
  Pedrero, etc.)
- `retailer` — retailer entities tracked as vendors for compliance docs

`customs_broker` and `cross_border_partner` are the types logistics-manager
Flow H reads against. Onboard them through this skill on the same HITL flow.

### 3. PO lifecycle (the P2P spine)

The biggest job. Six sub-flows that walk a PO from draft to close. The PO is one Asana task that carries forward; **Status** field changes and section moves replace any title rewriting. Task title format stays `PO Number — Vendor` throughout.

**3a. PO to place**
- *Trigger:* approved reorder review, NPI ramp, manual ask ("place a PO for X")
- *Action:* Draft PO in PLM (line items, quantities, prices, vendor terms). Open Asana task in **HITL — Needs Operations Review** section, Status = **Draft**, Vendor + PLM Link populated. Description holds PO summary, total, expected receipt date, linked PD task if applicable.
- *HITL:* Operations reviews PLM draft. On approval, sends PDF via email to vendor.

**3b. PO sent**
- *Trigger:* `outlook-plm-bridge` / `outlook-asana-bridge` detect the PO PDF being sent from Sent Items, OR the operator marks the task sent as a manual fallback
- *Action:* Skill updates PO status in PLM to Sent. Asana task moves to **POs In Flight**, Status = **Sent**.

**3c. Ack received**
- *Trigger:* outlook-plm-bridge logs an ack to the PLM PO record
- *Action:* Skill compares the ack against the PO at header level — total qty, total value, ETA. Drift on any of those → Status = **Variance**, task moves back to **HITL — Needs Operations Review**. Line-level discrepancies stay in PLM and surface only if they affect a header total. Clean ack → Status = **Acknowledged**, task stays in **POs In Flight**.

**3d. In transit**
- *Trigger:* shipping / tracking updates from supplier emails (via outlook-plm-bridge)
- *Action:* Status moves from **Acknowledged** to **In Transit** on first shipping signal. Skill syncs ETAs to PLM. ETA changes after that get logged as a comment on the same task; no Status change unless ETA slips materially.

**3d-side. Cancellation**
- *Trigger:* operator request ("cancel PO X"), or vendor cancellation logged via outlook-plm-bridge
- *Action:* HITL confirm. On approval, PLM PO status → Cancelled, Asana Status = **Cancelled**, task moves to **Closed** section and gets marked complete. Available from any state prior to Received.

**3e. Receipt (two scenarios)**

Receipt is the formal hand-off where goods land at OC3PL (Logiwa WMS), the PO status flips to Received, and the batch record is created in PLM. The receipt task home depends on whether the PO is PD-linked.

**Scenario A — PD-linked.** The PO traces to a linked PD task (linkage already known via the multi-home rule). A receipt task already lives in the PD project. Don't create a duplicate. Set the **PLM Link** field on the existing PD task to point at the PO record, then multi-home that task into AC Brands Purchasing, **Receiving** section. Downstream: OC3PL notifies via email or Asana comment → operator updates the task with the Logiwa Receipt Order ref and marks Status = **Received**. `plm-assistant` updates the PLM PO status and creates the batch entry. **PD owns the close.**

**Scenario B — Standalone.** No PD project for this PO. The skill creates a `Receipt — Vendor Name — PO Number` task in the **Receiving** section, description per the Receipt template (references/task-description-templates.md). Same downstream: OC3PL notifies → operator updates the Logiwa ref and marks Status = **Received** → `plm-assistant` writes the PLM PO status and batch entry. Purchasing holds the receipt task open until the invoice clears (Job 3f).

QA itself stays on the PD side in both scenarios; Purchasing only carries the receipt signal.

**Discrepancy cross-reference.** Any count variance, damage, or missing-items signal at receipt opens a discrepancy task per Job 10. The operator flags it, or OC3PL / logistics-manager signals it; the receipt task stays open while the discrepancy is investigated.

**3f. Invoice + close (manual 3-way match in v1)**
- *Trigger:* outlook-plm-bridge logs an invoice
- *Action:* Skill stages a 3-way match in PLM (PO / receipt / invoice). Discrepancies → Status = **Variance**, task moves back to **HITL — Needs Operations Review**. Clean match → PLM PO closed, Status = **Closed**, Asana task moves to **Closed** section and gets marked complete.
- *Cost ledger:* The same invoice also gets logged as a `vendor_invoices` row via Job 9. PO-bound invoices have `po_link` populated, which is how Job 9 dedups against the 3-way match.
- *Note:* When AP system integration ships (future), this match becomes automated. The current task data is structured to plug into that later without rewrite.

### 4. Sourcing decisions / RFQs

Track supplier evaluation for new components or alternative vendors.

- *Trigger:* "find an alt supplier for X", "RFQ status", "qualifying [vendor] for X"
- *Action:* Open Asana task in **Sourcing & RFQ** section, titled `RFQ — Component / Project`, with sub-tasks per supplier being evaluated. Track RFQ sent → bid received → samples → qualification status in the description.
- *Handoff:* Once a supplier is selected, qualification work goes to PD Manager. Purchasing picks back up at the first production PO.

### 5. Vendor performance

Quarterly scorecards or on-demand.

- *Trigger:* "how's [vendor] doing", "scorecard for [vendor]", "quarterly vendor review"
- *Action:* Pull PO history via plm-assistant — promised lead time vs actual, fill rate, defect / reject rate, price drift over time. Pull related supplier call notes via fireflies-asana-bridge. Compose scorecard.
- *Branded output:* Hand off to sjs-status-reporter for SJS-formatted scorecard.

### 6. Reorder review (HITL, manual-trigger only in v1)

Inventory-driven reorder logic comes from a future Demand Planner / Supply Planner skill. Until then, this job runs only on operator request.

- *Trigger:* "review reorders for X", "should we reorder Y"
- *Action:* Pull on-hand, safety stock, MOQ, lead time, last unit cost, and vendor via plm-assistant. Open Asana task in **HITL — Needs Operations Review**, titled `Reorder Review — SKU/Component`, with that data and a suggested order qty in the description.
- *HITL:* Operations approves. Approved reorder feeds Job 3a (PO placement).

### 7. Compliance docs

File COAs, COCs, MSDSes, regulatory docs, COIs against vendor and batch records. Surface gaps weekly.

- *Trigger:* outlook-plm-bridge routes an inbound compliance doc, weekly compliance sweep, "missing docs for [vendor]", "COA came in for [batch]", "what COIs expire this quarter"
- *Action:* File against vendor + batch in PLM via plm-assistant. Weekly sweep flags missing or expiring docs (COI lapsing, W9 missing) as `Compliance Gap — Vendor Name` tasks in **Compliance, Renewals & Disputes**.

### 8. Contract & terms tracking

Renewal dates, payment term changes from supplier emails, disputes. Renewals run on a weekly automated sweep against PLM `vendors.contract_renewal_date`; payment-term changes and disputes stay operator-triggered.

**Weekly renewal sweep (automated).** A Cowork scheduled task (`purchasing-renewal-sweep`) fires every Monday at 7:00 AM PT and runs this flow:

1. Query PLM: `vendors WHERE contract_renewal_date IS NOT NULL AND status = 'active'`.
2. For each vendor, compute `days_to_renewal = contract_renewal_date − today`.
3. Open a task in **Compliance, Renewals & Disputes** when `days_to_renewal` lands in any window (±1 day margin):
   - 59–61 → 60d window
   - 29–31 → 30d window
   - 14–16 → 15d window
4. Title: `Renewal — {vendor_name} — {60d / 30d / 15d}`. Assignee: Operations. Due date: the actual `contract_renewal_date`. Description per the Renewal template (references/task-description-templates.md).
5. **Dedup:** before opening, query Asana for an existing task in Compliance, Renewals & Disputes matching the same vendor + window title pattern. If one exists, skip.
6. **Wiki read first:** before drafting each description, read `supplier/<vendor_slug>` per the wiki context block. Prepend any prior renewal terms and recent performance signal into the description.
7. Post a one-line completion summary: tasks opened vs. skipped on dedup.

**Operator-triggered renewals & disputes.** On manual ask or a supplier email signaling a renewal/terms change, open the same `Renewal — {vendor_name} — {window}` task (or update an existing one). Disputes open in the same section as `Dispute — PO Number — Vendor` with Status = **Dispute** and linked PO and invoice.

- *Trigger:* "contract renewal for [vendor]", "payment terms changed for [vendor]", "dispute with [vendor]", calendar approach to a renewal date, or the Monday `purchasing-renewal-sweep` scheduled task
- *Action:* Per the sweep flow above for renewals; disputes open a `Dispute — PO Number — Vendor` task with Status = **Dispute**.

### 9. Vendor invoice cost tracking (HITL)

Universal cost tracking across all AC Brands vendors. Source is Ramp emails (and direct vendor invoices reconciled against Ramp) staged by outlook-plm-bridge Flow I. One Asana task per invoice in the **Vendor Invoices** section, one row per invoice in PLM `vendor_invoices`, and a multi-home routing matrix that puts the same task in front of the right sub-system owner.

- *Trigger:* outlook-plm-bridge Flow I stages an invoice intake, "log the [vendor] invoice", "what did we spend with [vendor] this month", "regulatory spend YTD", "any disputed invoices", "show me last month's invoices for [SKU]"
- *Action:* The bridge fans the email into a staged Asana task in **Vendor Invoices**, Cost Category and Regulatory Driver pre-classified, PDF attached, PLM Link blank pending commit. Operator reviews. On approval, plm-assistant commits the `vendor_invoices` row, the task multi-homes to the right downstream project per the matrix below, and (for the PD case) gets positioned as a subtask under the master Asana task on the linked SKU.

**Cost categories.** The `vendor_invoices.cost_category` enum carries the primary spend domain:

- `regulatory` — Pedrero retainer, Ecomundo CPSR, UK RP fees, state filings, MoCRA fees, EPR registrations
- `quality` — lab testing (Eurofins, Q-Labs, AMR), PET, micro panels, stability runs
- `pd` — formulation work charged separately from POs (concept fees, sample rounds, benchtop iterations from KDC-One / AMR / Vegelabs)
- `ops` — freight (forwarder, broker, parcel), fulfillment (OC3PL), inventory carrying costs not tied to a PO
- `marketing` — agency retainers, content production, sampling, paid media platform fees
- `general` — fallback for legal, SaaS, banking, anything not above

**Regulatory driver override.** `regulatory_driver = true` is independent of `cost_category` and always adds **SJS Regulatory Management** as an additional home. Canonical cases: PET (often quality-coded), RIPT (quality-coded), EU CPSR (sometimes pd-coded if tied to reformulation), Health Canada notification work. When in doubt, set true and let regulatory-manager see it.

**Multi-home routing matrix.** Every staged invoice multi-homes to **Vendor Invoices** in this project plus one or more downstream homes by cost_category. Operator confirms the routing at HITL; the skill never auto-multi-homes without approval.

| cost_category | Additional Asana home(s) | Notes |
|---|---|---|
| `regulatory` | SJS Regulatory Management | Always. |
| `quality` | SJS Quality Management | Always. |
| `pd` | The SKU's PD project (when `linked_sku_id` is set) | Also positions the Asana task as a subtask under the master Asana task on that SKU. Both — not either/or. If no `linked_sku_id`, stays Purchasing-only. |
| `ops` (freight) | SJS Logistics Shipment Status | Forwarder, broker, parcel carrier invoices. |
| `ops` (fulfillment) | OC3PL Order Management | OC3PL service invoices, pick-pack-ship charges. |
| `ops` (inventory) | SJS Inventory Management | Carrying / storage charges. Inventory-manager fields. |
| `marketing` | (Purchasing-only until marketing project GID is provided) | Tracked in `vendor_invoices` even when no second home. |
| `general` | None | Stays Purchasing-only. |

Any row with `regulatory_driver = true` adds **SJS Regulatory Management** on top of whatever the cost_category routing produced.

**State.** Invoice state lives in the `State` custom field (single-select) and mirrors the `vendor_invoices.state` enum 1:1: Pending, Approved, Paid, Disputed, Declined, Void. State transitions happen via plm-assistant write — Asana mirrors the PLM record. No sub-state sections.

**HITL gates.** Five distinct gates:

1. *Classification* — Operator confirms cost_category, regulatory_driver, and linked_sku_id before any PLM write.
2. *Multi-home* — Operator confirms which downstream project(s) the task should land in. The skill drafts the routing per the matrix; Operator approves or overrides.
3. *Subtask placement* (PD case only) — When linked_sku_id is set, Operator confirms which master Asana task on the SKU's PD project gets the invoice as a subtask. The skill drafts a best-match; Operator confirms or picks an alternate.
4. *PLM write* — plm-assistant commits the `vendor_invoices` row only after Operator approval. Asana State field is set in the same transaction.
5. *Dispute trigger* — Moving State to **Disputed** opens a `Dispute — Vendor — Invoice #` task in **Compliance, Renewals & Disputes** (linking back to the original Vendor Invoices task) and notifies the vendor owner. Operator approves the dispute before that branch fires.

**Reads vs. writes.** Cost rollup queries (regulatory-manager Jobs 8 + 9, regulatory-status-reporter spend strip, monthly vendor spend summaries) read `vendor_invoices` via direct Supabase SELECT — no plm-assistant call needed. Writes (INSERT new invoice, UPDATE state) always go through plm-assistant.

### 10. Receipt discrepancy investigation (HITL)

The canonical flow for any count variance, damage, or missing-items signal at receipt. Job 3e (both scenarios) cross-references this job: a discrepancy spotted at receipt opens a task here while the receipt task stays open.

- *Trigger:* `logistics-manager` flags a vendor-attributable receipt issue (count variance, damage, missing items), OC3PL flags directly, or the operator opens one manually after seeing a discrepancy.
- *Action:* Create a `Discrepancy — Vendor Name — PO Number` task in **Compliance, Renewals & Disputes**. Description follows the Discrepancy template (references/task-description-templates.md), with **Discrepancy Type** and **Resolution** rendered as inline structured fields in the description, not Asana custom fields. The PO's existing multi-home set determines the discrepancy task's secondary homes: if the PO is multi-homed to a PD project, the discrepancy task joins the same homes. Read `supplier/<vendor_slug>` from the wiki before drafting so prior quality history shows inline.
- *HITL:* Operator investigates, communicates with the vendor via Outlook, documents findings in Asana comments, and updates the **Resolution** field inline. Resolution options: **Vendor Credit / Replacement Shipment / Accepted As-Is / Escalate to CAPA**.
- *Handoff on "Escalate to CAPA":* the skill notifies `capa-coordinator` with the discrepancy task GID and core context (vendor, PO, batch, damage type, observed date). `capa-coordinator` opens the formal CAPA per SKN-OPS-001 and cross-links the source discrepancy task.
- *Vendor scorecard feed:* on task close (any Resolution), the skill writes an event line into `supplier/<vendor_slug>` via `asana-plm-bridge` (Phase 5 flow) — this skill never writes the wiki directly. The discrepancy feeds Job 5 vendor performance.

## Asana surface

- *Project:* **AC Brands Purchasing** — dedicated, Operations team, public to workspace
  - Project GID: `1214373717266702`
  - Project URL: https://app.asana.com/0/1214373717266702/list
  - Team (Operations) GID: `1200120716421443`
- *Detail home:* templated task descriptions (see references/task-description-templates.md)
- *Closed POs:* stay as completed tasks in the **Closed** section; no separate archive. PO history lives in PLM.

### Sections (cached)

The skill drops tasks into the right section by job. Section GIDs (full live set, reconciled 2026-05-28):

- **Untitled section** — `1214373372406252` (legacy default; not used by the skill)
- **Cross-Skill Dashboard** — `1214843467424921` (cross-skill rollup surface; awareness only)
- **Vendor Onboarding** — `1215139855143672` (Job 2 intake + doc collection: 2B/2C live here until the NDA+W9 gate fires)
- **HITL — Needs Operations Review** — `1214373372406259` (anything pending the operator: PO drafts, variances, reorder review)
- **POs In Flight** — `1214373372406260` (issued through in transit)
- **Receiving** — `1214373372406261` (received, pending invoice match)
- **Vendor Invoices** — `1215148455338976` (one task per invoice, state via custom fields)
- **Compliance, Renewals & Disputes** — `1214373372406262` (compliance gaps, renewal warnings, vendor disputes; onboarding lands here after the 2C gate)
- **Sourcing & RFQ** — `1214373372406263` (RFQs in flight, supplier qualification)
- **Closed** — `1214373372406264` (completed POs and closed work)

### Custom fields (cached)

Three workflow fields. Status is the queue driver; Vendor and PLM Link save the operator a click.

- **Status** (single-select) — GID `1214373372406268`. Mirrors `purchase_orders.status` in PLM 1:1 (vocabulary + options identical).
  - Draft `1214373372406269`
  - Sent `1214373372406270` (renamed from Issued; same enum option, label-only change in Asana)
  - Acknowledged `1214373372406273` (this GID previously held Variance before the v1.2 reconciliation; Asana now uses it for Acknowledged and assigned a fresh GID to Variance)
  - In Transit `1214373372406271`
  - Received `1214373372406272`
  - Variance `1214370303255335` (new GID after v1.2 reconciliation; old `...406273` rolled over to Acknowledged)
  - Dispute `1214373372406274`
  - Closed `1214373372406275`
  - On Hold `1214373372406276`
  - Cancelled `1214370303255310` (added in v1.2 reconciliation)
- **Vendor** (text) — GID `1214370303255299`. Populated from the PLM vendor record name on task create; kept in sync if the PLM record renames.
- **PLM Link** (text) — GID `1214370303255301`. Holds the PLM PO / vendor / batch URL or ID so the operator can jump straight to source-of-truth.

#### Vendor Invoices custom fields (15)

Tasks in **Vendor Invoices** carry the three core workflow fields above plus fifteen invoice-specific fields. All fifteen mirror `vendor_invoices` columns 1:1. State + cost_category + regulatory_driver drive routing and queue scans; the rest are operator-visible context.

1. **Invoice Number** (text) — mirrors `vendor_invoices.invoice_number`. Unique per vendor.
2. **Invoice Date** (date) — mirrors `vendor_invoices.invoice_date`.
3. **Amount** (number, 2 decimal) — mirrors `vendor_invoices.amount`.
4. **Currency** (single-select) — USD / CAD / EUR / GBP / AUD. Mirrors `vendor_invoices.currency`.
5. **Cost Category** (single-select) — Regulatory / Quality / PD / Ops / Marketing / General. Drives multi-home routing per the matrix.
6. **Regulatory Driver** (single-select Yes / No) — mirrors `vendor_invoices.regulatory_driver`. Yes always adds Regulatory as a home.
7. **State** (single-select) — Pending / Approved / Paid / Disputed / Declined / Void. Mirrors `vendor_invoices.state` 1:1.
8. **Linked SKU** (text) — populated from PLM `products.name` when `linked_sku_id` is set. Drives PD-case subtask placement.
9. **Linked PO** (text) — populated from PLM `purchase_orders.po_number` when `po_link` is set. Null for retainer-style invoices.
10. **Ramp Message ID** (text) — source Ramp email message identifier. Allows dedup if same invoice arrives twice.
11. **Attachment Filename** (text) — PDF name as filed by outlook-plm-bridge.
12. **Source Email Subject** (text) — original Outlook subject.
13. **Source Email Date** (date) — when the Ramp / vendor email landed.
14. **Classified By** (text) — operator who confirmed classification at the HITL gate.
15. **Notes** (text) — free-text operator commentary; mirrors `vendor_invoices.notes`.

GIDs for the **Vendor Invoices** section and these 15 fields are populated on first commit (project creation work). The skill caches GIDs back to this file once they exist.

### Queue scan logic

When asked "what's open in purchasing" or any catch-up question, the skill scans by **Status field** plus section, not by title regex:

- HITL queue → tasks in **HITL — Needs Operations Review** section, regardless of Status (covers Draft, Variance, reorder review, dispute review, cancellation review)
- Onboarding queue → tasks in **Vendor Onboarding** section (2B awaiting Proceed, 2C collecting docs before the NDA + W9 gate)
- In-flight POs → Status in {Sent, Acknowledged, In Transit}
- Receiving queue → Status = Received
- Stuck / blocked → Status = On Hold
- Closed (history view) → Status in {Closed, Cancelled}
- Invoice queue → tasks in **Vendor Invoices** section, scanned by **State** field:
  - Pending review → State = Pending (HITL gate not yet cleared)
  - Awaiting payment → State = Approved
  - Paid (history) → State = Paid
  - Open disputes → State = Disputed (cross-reference the Dispute task in **Compliance, Renewals & Disputes**)
  - Declined / Void → terminal states; remain visible in section for audit

The PO Number lives in the task title; Vendor + PLM Link are field-direct. Invoice tasks title as `Invoice — Vendor — Invoice Number`.

## Calls and integrations

The skill goes through other skills for source access wherever one exists. Only Asana access is direct, matching the asana-pd-manager pattern (peer orchestrators each own their own Asana surface). Bridge intake follows the queue contract at `references/architecture/bridge_queue_contract.md` — bridges post into the AC Brands Purchasing project (including Flow I Ramp invoices); this skill picks up.

**Reads via:**
- plm-assistant — vendor lists, PO history, batch records, components, on-hand, `vendor_invoices` lookups when needed for operator queries
- outlook-plm-bridge — inbound supplier emails (acks, invoices, compliance docs, shipping updates) routed to PLM context, plus outbound POs detected in Sent Items (drives auto PO Sent status). **Flow I** stages Ramp / vendor invoice intake into the Vendor Invoices section.
- outlook-asana-bridge — inbound supplier email signal that belongs in workflow rather than PLM, plus outbound supplier emails from Sent Items
- fireflies-asana-bridge — supplier call transcripts and action items
- Asana — direct read of own tasks in the AC Brands Purchasing project, plus multi-homed PD tasks
- Supabase direct SELECT — read-only `vendor_invoices` for rollup queries (monthly vendor spend, cost-category totals) without round-tripping through plm-assistant

**Writes via:**
- plm-assistant — all PLM writes (vendor records, PO records, batch entries, doc filing, `vendor_invoices` row INSERT and state UPDATE)
- Asana — direct (task creation, comments, status, multi-homing including invoice routing matrix, PD-case subtask placement)
- sjs-status-reporter — branded output (vendor scorecards, quarterly reviews)
- capa-coordinator — Job 10 escalation: a discrepancy task with Resolution = Escalate to CAPA hands off the task GID + context so capa-coordinator opens the formal CAPA per SKN-OPS-001

**Called by:**
- `sjs-ops-system` — the System 5 master router routes any
  purchase-to-pay, vendor, RFQ, compliance-doc, or invoice question here. The router
  documents Purchasing-vs-SDP and Purchasing-vs-Inventory boundary cases.
- `supply-demand-planner` — buy recommendations from the monthly run hand
  the FG and component buys here for PO drafting.
- `oc3pl-order-manager` — carrier-attributable cost variance flows here as
  a vendor-scorecard input.
- `logistics-manager` — landed-cost overruns route back to vendor scorecard
  the same way. Vendor-attributable receipt issues (short ship, wrong items,
  vendor packing damage) signal a Job 10 discrepancy task; carrier-attributable
  damage stays in logistics-manager's lane.
- `regulatory-manager` — Jobs 8 + 9 (monthly + quarterly cost rollups) read `vendor_invoices` directly via Supabase SELECT; this skill is the upstream classifier whose HITL approvals determine what those rollups see.
- `regulatory-status-reporter` — reads regulatory-manager's rollup output for the v6.7 spend strip; downstream of this skill's classification work.

**Never duplicates:**
- oc3pl-order-manager (outbound shipping is theirs)
- asana-pd-manager (PD work stays in PD projects; purchasing-related PD tasks get multi-homed, not recreated)
- fireflies-asana-bridge / outlook-asana-bridge / outlook-plm-bridge / plm-assistant (calls them, doesn't reimplement)

## Out of scope (v1)

- Outbound shipping (oc3pl-order-manager owns)
- 3PL relationships
- Recurring POs (office supplies, monthly retainers — invoices for these still flow through Job 9)
- Inventory and forecasting (future Demand Planner skill)
- AP system integration (future — Job 9 logs invoice cost into `vendor_invoices` but does not replace AP)
- Marketing project Asana home for cost_category = `marketing` invoices (Purchasing-only home until a marketing project GID is provided)

## First-run setup

The AC Brands Purchasing project, sections, and custom fields already exist. GIDs are cached above. On first invocation in any chat, the skill confirms the project responds and the cached field/section GIDs match what Asana returns. If a GID has drifted (someone renamed or rebuilt a section), the skill reconciles by re-fetching via `asana_get_project_sections` / `asana_get_project` and updates this file's cache before doing any work.

## Trigger phrases

See references/trigger-phrases.md for the grouped trigger library.

## Task description templates

See references/task-description-templates.md for the templated descriptions per task type. Skill writes the description; Operations reads it.

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant pages from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as bridge skills process emails and meetings — reading them first gives this skill institutional memory about suppliers and SKUs without re-scanning raw sources.

### Which pages to read

- Named supplier or vendor → `'supplier/' || public.wiki_slugify(vendor_name)`
- Named product or SKU (where the request names a SKU) → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`

Vendor pages carry lead times, commercial terms, open POs, quality flags, and document trail. SKU pages carry velocity history, safety-stock context, and demand signals.

At task creation in Job 2 (2B Vendor Intake), Job 3e (3E Receipt, Scenario B standalone task), Job 8 (4B weekly renewal sweep), and Job 10 (6C discrepancy investigation), read `supplier/<vendor_slug>` before drafting the task description so any prior history shows inline. This skill never writes to the wiki directly — purchasing-driven wiki writes go through `asana-plm-bridge`'s Asana-state flow.

### Read query

```sql
-- Single supplier by slug (preferred — full-text search drops short acronyms like "KDC")
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));

-- Content-term sweep across suppliers (use for terms like "lead time", "MOQ", "tariff")
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_page_type => 'supplier', p_query => '{term}', p_limit => 3);
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before generating its response — read it the way a person reads a briefing document before a meeting.

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
