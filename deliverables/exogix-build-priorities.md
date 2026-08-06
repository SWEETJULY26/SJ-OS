# Exogix Build Priorities — Sweet July Automation System

**Prepared by:** Alvin Belt · **Date:** 2026-08-06 · **Status:** Draft, pending Nicole review
**For:** Ash Emmanuel, Ibrahim Mamoon (Exogix AI)
**Context:** Follow-up from the Aug 5 discovery call. Agreed direction is a hybrid system, 70 to 80 percent coded TypeScript backend, Claude API for judgment steps only, Cloudflare email worker for intake, error logging instead of manual catch.

---

## What changed since your audit

Ibrahim cloned the repos before Aug 5. Three things have landed since, and they matter for scoping because they are the spec for the coded layer:

1. **23 ratified SOPs now live in `SJ-OS/sops/` as canonical markdown** (SKN-OPS-001 through 023). The 13 newest cover PD stage-gates, the full purchase-to-pay pipeline, receiving, inventory adjustments, S&OP, freight fault-attribution, retailer ASN, international DTC, and DTC order exceptions. Each one is a written procedure with roles, gates, and defined states. The deterministic 70 to 80 percent you plan to code is already written down here. Build from these, not from the skill prompt files.
2. **The Asana state machine is now data.** `references/architecture/queue_registry.md` holds all eleven Asana queues: project GIDs, sections, state fields, and state-to-section maps, pulled from live Asana. Status fields are authoritative; sections are projections. Your backend can read one registry file instead of parsing eleven skill prompts.
3. **Field designs for the four previously unrulable queues** (CAPA, Quality, Inventory, Logistics) are specced in the same registry.

## How this list is sliced

54 skills are installed. Not all are rebuild targets. Roughly 30 carry pipeline work that belongs in code. The rest are conversational or judgment tools that stay in Claude, or one-off utilities out of scope entirely. Phases below are ordered by what runs most often, burns the most tokens, and touches the most business risk. Phase 1 is the must-have set; later phases are modular additions, matching the modular approach we agreed on.

---

## Phase 1 — Must have: Purchasing + the email intake spine

This is the purchasing process I flagged on the call, plus the intake layer everything else depends on. These are the highest-frequency, highest-token workflows in the system today.

| Skill | What it does | Trigger today | Coded spec (SOPs) |
|---|---|---|---|
| `outlook-asana-bridge` | Scans Outlook inbox + sent, classifies every email, posts tasks to the right Asana queue | Cron, 3x/day, full Claude session | Queue routing per `bridge_queue_contract.md` |
| `outlook-plm-bridge` | Routes PLM-bound emails (PO acks, COAs, test results, invoices) into PLM writes; Ramp invoice capture | Cron, full Claude session | SKN-OPS-015 |
| `purchasing-manager` | PO lifecycle draft to close, vendor records, RFQs, compliance docs | Manual + cron scans | SKN-OPS-010, 012, 013, 014, 015 |
| `plm-assistant` | Sole writer to PLM (Supabase). Everything above writes through it | Called by other skills | Becomes the backend's data-access layer |

**Infrastructure in this phase:** Cloudflare email worker replacing the 20 per-vendor Outlook rules with one global forward; error logging and notification (destination TBD, Asana works); webhook layer for Asana status changes (the approve-to-send flow Ibrahim walked through).

**Where Claude API stays in the loop:** email classification when keyword rules are ambiguous, document extraction (quotes, COAs), drafted vendor-facing replies. All sends gated on human approval via Asana status.

## Phase 2 — Inventory, daily order ops, logistics

The rest of the daily execution layer. Same shape as Phase 1: cron-driven parsing and state movement that should be code.

| Skill | What it does | Trigger today | Coded spec (SOPs) |
|---|---|---|---|
| `oc3pl-order-manager` | Daily Logiwa report parse, DTC fulfillment log, exceptions, pre-ship OOS holds | Daily cron | SKN-OPS-022, 023 |
| `inventory-manager` | On-hand position, receiving, three-way recon (PLM/Shopify/Logiwa), FEFO, write-offs | Manual + scheduled | SKN-OPS-016, 017 |
| `logistics-manager` | Inbound/outbound freight tracking, customs, retailer ASN/EDI, fault attribution | Manual + scheduled | SKN-OPS-019, 020, 021 |
| `supply-demand-planner` | Monthly S&OP run, forecast, buy recommendations | Monthly | SKN-OPS-018 |
| `fireflies-asana-bridge` | Meeting transcripts to Asana actions across all queues | Manual + scheduled | Queue contract |

## Phase 3 — Quality and Regulatory

Fully proceduralized (SKN-OPS-001 through 009) and the highest-stakes domain in the system. This is where Ibrahim's point about probabilistic errors and FDA liability lands hardest, so the value of deterministic code is high, but every phase gate here keeps a human approval. Nothing files to an agency or responds to a customer without sign-off.

Skills: `quality-manager`, `capa-coordinator`, `complaint-and-event-handler`, `batch-lifecycle-tracker`, `quality-lab-coordinator`, `regulatory-manager`, `claims-il-and-label-keeper`, `adverse-event-and-recall-reporter`.

## Phase 4 — Reporters and dashboards

Deterministic render jobs currently burning Claude sessions on cron. Pure code plus a Claude API call for narrative summaries.

Skills: `alvin-daily-status-dashboard` (daily 8am, fans out across 12 skills, the single biggest recurring token cost), `sjs-status-reporter`, `quality-status-reporter`, `regulatory-status-reporter`, `ayesha-weekly-briefing`, `ac-brands-leadership-dashboard` (in build), `ops-status-reporter` (not yet built; build it directly in the new system rather than building it twice).

## Stays in Claude — not part of this scope

Conversational and judgment-heavy work, low frequency, no pipeline shape: `asana-pd-manager` (interactive PD work), `sjs-ingredient-lookup`, the six margin skills, `sjs-comp-intel`, `sjs-retail-intel`, `ac-brands-opportunity-assessment`, `ac-brands-holiday-comms`. The seven router skills (`sjs-master`, `sjs-pd-system`, etc.) are replaced by code routing in the new backend, not rebuilt.

Out of scope entirely: foundation utilities (docx, pdf, pptx, xlsx, excalidraw, theme-factory, mcp-builder, skill-builder, brand-voice, and similar).

## Sequencing notes

1. Phase 1 alone removes most of my daily manual load and most of the token spend. If timeline forces a cut, cut from the bottom, not within a phase.
2. Target: Phases 1 and 2 running before holiday season ramp (October).
3. The queue registry and SOP set are maintained in the repo and will keep evolving. Treat the repo as the spec source, and we should agree on a change-notice convention so process changes flow into the coded system, which was the adaptability point from my vision on the call.
