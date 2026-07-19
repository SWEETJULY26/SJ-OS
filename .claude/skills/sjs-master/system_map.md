# System Map

**Use:** Brand-level inventory of every skill in the Sweet July Skin skills system. The `sjs-master` router uses this to decide where to send a request. Every skill author uses this to know what peers exist and what they own. Org-level skills (and their future router `ac-brands-master`) are out of scope here.

---

## Orchestration principle — compositions over parallel implementations

When an automation, output, or report needs data from multiple tools (Fireflies + Outlook + Asana + PLM), it does not call those tools directly. It activates the relevant **skills** and lets each skill do its tool work, then composes the outputs.

This applies to:
- Daily PD recap (composition of Skills 1, 2, 3, 5, 6)
- Monday weekly briefing (composition of Skills 1, 2, 3, 4, 5, 6)
- Ayesha founder briefing (composition of PD skills + Ops skills)
- Any future scheduled or on-demand multi-source output

Why this matters: each skill encapsulates the right pattern for its tool — Fireflies date-not-keyword, Outlook broad afterDateTime, Asana portfolio sweep, PLM SELECT-then-stage. If a tool pattern needs to change, the skill that owns it is the one place it changes. Compositions automatically benefit.

If a new automation is added and it pulls directly from a tool that an existing skill already covers, the lint pass should flag that as a structural drift.

## Skill systems at a glance

| System | Purpose | Skill count | Router |
|--------|---------|-------------|--------|
| **PD** | Product Development intelligence — Asana, Outlook, Fireflies, PLM bridges, branded outputs | 7 | `sjs-pd-system` |
| **Ops** | Purchasing, inventory, supply/demand, logistics, OC3PL DTC | 5 | `sjs-ops-system` |
| **Margin Architecture** | SKU margin framework, pressure-tests, archetype advisory, walk-away, portfolio review, interactive model | 6 | `sjs-margin-architect` |
| **Comp / Retail Intel** | Competitive teardowns, retail performance, UBM benchmarks | 2 | (no router yet — both skills standalone) |
| **Quality** (System B) | Complaints, adverse events, recalls, CAPAs, lab findings, batch lifecycle, SOP catalog, branded quality dashboard | 6 | `sjs-quality-system` |
| **Regulatory** (System C) | IL review gate, claim sub, label archive, retailer attestations, MoCRA SAE filings, FDA recall reporting, state filings, Leaping Bunny, Pedrero liaison, branded regulatory dashboard | 5 | `sjs-regulatory-system` |
| **Founder briefing** | Weekly Ayesha briefing | 1 | n/a |
| **Holiday Comms** (org-level) | Annual team holiday email cadence — migrates to org router when built | 1 | n/a |
| **Brand** | Sweet July Skin brand guidelines | 1 | n/a |
| **PLM** | Product Lifecycle Management — Supabase | 1 | n/a (called by every system) |
| **Utility** | Ingredient lookup, find/replace, etc. | 2+ | n/a |

---

## PD system (7 skills)

Router: `sjs-pd-system`

| # | Skill | Role |
|---|-------|------|
| 1 | `asana-pd-manager` | Core engine — reads/writes all PD tasks, projects, portfolios |
| 2 | `fireflies-asana-bridge` | Meeting intel → Asana actions |
| 3 | `outlook-asana-bridge` | Email intel → Asana tasks/comments/stage moves |
| 4 | `asana-plm-bridge` | Asana ↔ PLM data sync |
| 5 | `sjs-status-reporter` | Branded outputs — status updates, decks, reports |
| 6 | `outlook-plm-bridge` | Email → direct PLM writes (peer to skill 3) |
| — | `asana-find-replace` | Bulk find-and-replace utility for Asana tasks |

---

## Ops system (5 skills + 4 shared bridges)

Router: `sjs-ops-system`

| Skill | Role |
|-------|------|
| `purchasing-manager` | P2P, vendors, RFQs, compliance docs |
| `inventory-manager` | On-hand, three-way recon, FEFO, returns |
| `supply-demand-planner` | S&OP, forecast, buy recommendations |
| `logistics-manager` | Inbound/outbound freight, customs, retailer ASN |
| `oc3pl-order-manager` | Daily DTC order parsing, Logiwa report |

Ops calls into PD bridges for shared work (Outlook/Fireflies sweeps), and `plm-assistant` for all PLM truth.

---

## Margin Architecture (6 skills)

Router / framework: `sjs-margin-architect`

| Skill | Role |
|-------|------|
| `sjs-margin-architect` | Framework reference + fallback router |
| `sjs-margin-pressure-test` | Channel-floor validation per SKU |
| `sjs-margin-walk-away` | Four-path advisory when a SKU breaks floor |
| `sjs-margin-portfolio-review` | Quarterly portfolio sweep + traffic-light report |
| `sjs-margin-archetype-advisory` | Archetype + Standard/Acquisition designation |
| `sjs-margin-interactive-model` | Interactive HTML margin tuning tool |

---

## Comp / Retail Intel (2 skills)

| Skill | Role |
|-------|------|
| `sjs-comp-intel` | Competitive teardowns + monthly trend digests |
| `sjs-retail-intel` | UBM launch benchmarks + cohort positioning |

---

## Quality — System B (6 skills)

Router: `sjs-quality-system`

| # | Skill | Role |
|---|-------|------|
| 1 | `complaint-and-event-handler` | Customer complaints, SAE triage (SKN-OPS-002), recall workflow (SKN-OPS-003), customer-quality intake (SKN-OPS-004) — single intake door for end-customer signal |
| 2 | `capa-coordinator` | CAPA + NCR lifecycle per SKN-OPS-001; authors working NCR Procedure (target SKN-OPS-005) |
| 3 | `quality-lab-coordinator` | Lab-side and supplier-side quality signal — OOS/OOT classification, vendor flag thresholds, scorecard signal-back to purchasing-manager (SKN-OPS-006) |
| 4 | `batch-lifecycle-tracker` | Ongoing in-market batch state — Active, Hold, Released, Pulled, Expired; in-market stability scheduling per ISO 11930 (SKN-OPS-007) |
| 5 | `quality-manager` | System B umbrella — cross-skill rollup, SOP catalog, ratification queue, cross-cutting tasks (audits, retailer questionnaires, regulatory inspections, quality system reviews), QoS aggregation. Owns the SJS Quality Management Asana project. |
| 6 | `quality-status-reporter` | Branded HTML quality dashboard — generates `acb-thelanding.netlify.app/quality-dashboard.html` from quality-manager's rollup; on-demand + monthly auto-snapshot |

**Canonical role-map:** lives in `quality-manager/references/role-map.md`. Sub-skill role-maps reference the canonical one. Operator = Alvin. QA Lead = Perrine (technical gates). Voice of Customer = Nicole Iturbe (customer-side intake gates).

**Canonical SOP catalog:** lives in `quality-manager/references/sop-catalog.md`. Sub-skills query at runtime to confirm current revision before significant writes.

---

## Regulatory — System C (5 skills)

Router: `sjs-regulatory-system`

| # | Skill | Role |
|---|-------|------|
| 1 | `claims-il-and-label-keeper` | Pre-launch IL review gate, sustained claim substantiation, label artwork archive, retailer attestation responses (Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo) per SKN-OPS-008 |
| 2 | `adverse-event-and-recall-reporter` | MoCRA serious adverse event filings (15-day clock), FDA recall reporting (21 CFR 7 Class I/II/III), state AE reports per SKN-OPS-009 |
| 3 | `regulatory-manager` | System C umbrella — cross-skill rollup, registrations tracker (MoCRA, state filings, Leaping Bunny), retailer attestation cadence dashboard, Pedrero liaison surface, ayesha-weekly-briefing seam. Intercepts Quality `[Reg Flag Pending]` and fans out. |
| 4 | `regulatory-status-reporter` | Branded HTML regulatory dashboard — generates `acb-thelanding.netlify.app/regulatory-dashboard.html` from regulatory-manager's rollup; on-demand + monthly auto-snapshot |
| 5 | `sjs-regulatory-system` | System C router |

**External regulatory partner:** Pedrero Regulatory (Amy Pedrero principal, Heather Folkes and Teona Bebia secondary). Canonical contact card lives in `regulatory-manager/references/pedrero-contacts.md`. All substantive regulatory review flows through Pedrero via Outlook.

**Canonical role-map:** lives in `regulatory-manager/references/role-map.md`. Sub-skill role-maps reference the canonical one. Operator + Reg Lead = Alvin. QA Lead = Perrine (consult). Voice of Customer = Nicole Iturbe (consult on attestations).

**SOPs walked:** SKN-OPS-008 (IL/Claims/Label), SKN-OPS-009 (Reportable Events). Both ratified 2026-05-09 and live in the quality-manager catalog.

---

## Founder briefing

| Skill | Role |
|-------|------|
| `ayesha-weekly-briefing` | Weekly briefing for Ayesha — Slide 5 (Ops) and Slide 6 (PD, co-owned with Nicole) |

---

## Holiday Comms (org-level)

| Skill | Role |
|-------|------|
| `ac-brands-holiday-comms` | Annual auto-send team holiday emails. Org-level skill — fires from `sjs-master` until the org-tier `ac-brands-master` ships, at which point it migrates. |

---

## Brand

| Skill | Role |
|-------|------|
| `sweet-july-skin-brand` | Sweet July Skin brand guidelines — fonts, colors, voice |

**Rule:** Every output-producing skill defers to this for canonical brand spec. No skill carries its own copy.

---

## PLM

| Skill | Role |
|-------|------|
| `plm-assistant` | The only path for PLM writes. Owns schema + audit log + commit. Called by every system. |

---

## Utility

| Skill | Role |
|-------|------|
| `sjs-ingredient-lookup` | Ingredient master list lookup |
| `asana-find-replace` | Bulk find-and-replace across Asana projects |
| `skill-creator` | Build / improve / measure skills |

---

## Cross-system handoffs

These are the wires between systems. Each one needs explicit logic in the master router and (where the trigger lives) in the originating skill.

### PD → Margin

| Trigger | Calls |
|---------|-------|
| Concept approval (Asana stage move) | `sjs-margin-archetype-advisory` then `sjs-margin-pressure-test` |
| Pressure-test fail | `sjs-margin-walk-away` |
| Quarter end | `sjs-margin-portfolio-review` (pulls signed-off SKUs from past 90 days) |

### PD → Ops

| Trigger | Calls |
|---------|-------|
| Formula moves to Signed Approvals | `purchasing-manager` (production PO) |
| Signed product approaches launch window | `supply-demand-planner` (forecast + buy plan) |
| Production wraps | `inventory-manager` (FG receipt + recon) |
| FG ships | `logistics-manager` (inbound) |

### PD → Retail Intel

| Trigger | Calls |
|---------|-------|
| SKU heads to UBM listing | `sjs-retail-intel` (cohort positioning + price ladder) |

### Quality → PD (reverse)

| Trigger | Calls |
|---------|-------|
| Complaint trend on a SKU | `asana-pd-manager` (open formulation review task) |
| CAPA root cause = formulation | `asana-pd-manager` (open reformulation task) |
| Recall trigger | PD owns formulation path forward |

### Comp Intel → PD (reverse)

| Trigger | Calls |
|---------|-------|
| Monthly trend digest with category shift | Surface to Perrine (PD owner), Alvin (PD admin), and Soraya (Marketing Manager) as pipeline input via `sjs-status-reporter`; Nicole consults |

### PD → Founder briefing

| Trigger | Calls |
|---------|-------|
| Weekly portfolio sweep | `ayesha-weekly-briefing` reads from PD portfolio |

### Brand dependency

Every output skill across every system defers to `sweet-july-skin-brand` for fonts, colors, voice. No exceptions.
