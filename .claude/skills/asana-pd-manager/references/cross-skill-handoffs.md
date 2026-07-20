---
name: PD cross-skill handoffs
description: Every wire between asana-pd-manager and a skill outside the PD system — outbound triggers PD fires, plus inbound reverse-handoffs PD receives from Quality, Regulatory, Margin, Intel, Ops, and Founder briefing. Sourced from references/architecture/system_map.md.
last_updated: 2026-05-17
---

# Cross-skill handoffs

Every PD ↔ non-PD wire. Canonical inventory lives in `references/architecture/system_map.md` "Cross-system handoffs" section. This file is the PD-side filter — only the rows that involve asana-pd-manager.

## Outbound — handoffs PD triggers

### PD → Regulatory

| Trigger in PD | Calls | Action |
|---|---|---|
| Signed Approvals stage move on Formula Tracker | `claims-il-and-label-keeper` | IL Review Gate. Flip `IL Status = Pending IL Review`, stage inbound task in SJS Regulatory Management. See `references/stage-gate-procedure.md`. |
| Annual PD roadmap review | `regulatory-manager` (Pedrero capacity planning) | Surface portfolio capacity ask so Pedrero engagement scope aligns with PD pipeline. |

### PD → Margin

| Trigger in PD | Calls | Action |
|---|---|---|
| Concept approval (early stage move on Formula Tracker) | `sjs-margin-archetype-advisory` then `sjs-margin-pressure-test` | Stage archetype + Standard/Acquisition designation, then run channel-floor pressure-test. |
| Pressure-test fail | `sjs-margin-walk-away` | Stage four-path advisory. Flag via task comment on the SKU project. |
| Quarter end | `sjs-margin-portfolio-review` | Past-90-day signed SKUs flow into the portfolio sweep. |

### PD → Ops

| Trigger in PD | Calls | Action |
|---|---|---|
| Formula moves to Signed Approvals | `purchasing-manager` | Production PO trigger. Cross-flag PD task. |
| Signed product approaches launch window | `supply-demand-planner` | Forecast and buy plan trigger. |
| Production wraps | `inventory-manager` | FG receipt and three-way recon. |
| FG ships | `logistics-manager` | Inbound freight tracking. |

### PD → Retail Intel

| Trigger in PD | Calls | Action |
|---|---|---|
| SKU heads to UBM listing | `sjs-retail-intel` | Cohort positioning and price ladder. |

### PD → PLM

| Trigger in PD | Calls | Action |
|---|---|---|
| Signed Approvals stage move | `asana-plm-bridge` Flow 1 | Phase update on product record + approval note. asana-plm-bridge stages, plm-assistant commits. |
| Vendor/supplier info change captured in PD | `asana-plm-bridge` Flow 2 | Stage vendor INSERT / UPDATE. |
| Batch info captured in PD task comment | `asana-plm-bridge` Flow 3 | Stage batch INSERT. |

### PD → Founder briefing

| Trigger in PD | Calls | Action |
|---|---|---|
| Weekly portfolio sweep | `ayesha-weekly-briefing` | Reads from PD portfolio. PD does not write to founder briefing directly — the briefing pulls. |

## Inbound — reverse-handoffs PD receives

### Quality → PD

| Originating skill | Trigger | asana-pd-manager action |
|---|---|---|
| `complaint-and-event-handler` | Complaint trend on a SKU | Open formulation review task in the SKU project. |
| `capa-coordinator` | CAPA root cause = formulation | Open reformulation task in the SKU project. Cross-flag PD Lead (Perrine). |
| `complaint-and-event-handler` / `adverse-event-and-recall-reporter` | Recall trigger | PD owns formulation path forward. Open recovery task. |
| `batch-lifecycle-tracker` | First commercial batch | Close production task, link batch GID in description. |

### Regulatory → PD

| Originating skill | Trigger | asana-pd-manager action |
|---|---|---|
| `claims-il-and-label-keeper` | IL Approved sync-back | Comment lands on the Formula Tracker task; `IL Status` flips to `IL Approved`; PD launch flow unblocks. |
| `claims-il-and-label-keeper` | IL Returned for Reformulation | `IL Status` flips, PD opens reformulation task on the SKU project. |
| `regulatory-manager` | Pedrero capacity flag | Surface capacity status on PD portfolio status update. |

### Comp Intel → PD

| Originating skill | Trigger | asana-pd-manager action |
|---|---|---|
| `sjs-comp-intel` | Monthly trend digest with category shift | Surface via `sjs-status-reporter` to Perrine (PD Lead), Alvin (Operator), Soraya (Marketing); Nicole consults. |

## Inbound writes from PD peers (same-system)

The other PD skills all write into asana-pd-manager rather than acting as cross-system handoffs:

- `fireflies-asana-bridge` — meeting action items proposed as PD tasks / comments / stage moves. Follow `references/confirmation-protocol.md`.
- `outlook-asana-bridge` — email-sourced PD writes. Same confirmation protocol.
- `asana-plm-bridge` — sync-back comments on PD tasks after PLM writes land.
- `outlook-plm-bridge` — `📦 PLM Sync` sync-back comments on PD tasks.

## Update protocol

When `references/architecture/system_map.md` adds, removes, or changes a cross-system handoff that involves PD, mirror the change here. Bump `last_updated`. If the change shifts a Rule (e.g., a new HITL gate), also update `references/confirmation-protocol.md`.
