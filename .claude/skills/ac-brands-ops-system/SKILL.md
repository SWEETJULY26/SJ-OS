---
name: ac-brands-ops-system
description: >
  Master router for AC Brands' System 5 — Operations Intelligence — covering Sweet
  July Skin purchase-to-pay, position-keeping, S&OP, freight, and DTC fulfillment.
  Use when an Operations request doesn't clearly map to one skill, straddles
  multiple Ops domains, or when figuring out which Ops skill owns what. The five
  System 5 skills: purchasing-manager (P2P, vendors, RFQs, compliance docs),
  inventory-manager (on-hand, three-way recon, FEFO, returns), supply-demand-
  planner (S&OP, forecast, buy recs), logistics-manager (freight, customs,
  retailer ASN), oc3pl-order-manager (daily DTC, Logiwa parse). Routes any Ops
  question — vendor health, what's on hand, what to buy, where a shipment is,
  today's shipping numbers — to the right skill. Documents the four shared
  bridges Ops calls into and the PLM source-of-truth rule via plm-assistant.
  Fallback when an Ops request is ambiguous or hits multiple skills.
---

# AC Brands Operations Intelligence — Master Router

You are operating inside System 5 — the Operations Intelligence stack for AC
Brands' Sweet July Skin. This router tells you which Ops skill (or chain of
skills) handles any given request, where the handoffs sit, and how the five
skills connect to the bridges and to PLM as the source of truth.

The router answers four questions: which skill owns the request, which other
skills it touches, what the data flow looks like, and what gets confirmed
before any write commits.

---

## The five System 5 skills

**purchasing-manager** owns purchase-to-pay end to end — vendor master records,
RFQs, PO lifecycle from draft through close, vendor performance scorecards,
compliance docs (COA, COC, COI, MSDS), and contract renewals. Operates the AC
Brands Purchasing Asana project. PLM is the source of truth for vendor and PO
records; every write goes through plm-assistant. Sample triggers: "place a PO
for the new Castaway run," "ack came in from Element," "missing COI on KDC-One,"
"contract renewal for Vegelabs," "got an intro from Milinyc — onboard them."

**inventory-manager** owns position-keeping and the location ledger — on-hand
across OC3PL, Shopify, contract manufacturers, in-transit, and (post-launch)
retailer DCs. Handles batch creation on receipt, three-way reconciliation across
PLM, Shopify, and Logiwa, FEFO pulls, near-expiry flags, write-offs, and return
dispositions. Operates the AC Brands Inventory Asana project. Sample triggers:
"what's on hand for the Soursop Serum," "receive PO #1027," "three-way diff this
week," "any near-expiry batches," "RMA came back — disposition this lot."

**supply-demand-planner** is the forecaster and recommender. Runs the monthly
S&OP — SKU × channel × month forecast across DTC, UBM, and Amazon, sets
safety-stock targets and reorder points, recommends finished-good and component
buys, and lays out the fill calendar at KDC-One and Vegelabs. Operates the
Sweet July Skin S&OP Asana project. Recommends; does not execute. Sample
triggers: "run the monthly S&OP," "forecast Pava Toner on UBM," "what should we
buy this month," "explode the BOM for Q3," "stockout risk on the Castaway Cream."

**logistics-manager** tracks every shipment that moves SJS goods or components.
Owns inbound finished-good and component freight from KDC-One, Vegelabs, Allure
Labs, HCT, Element, Impress, and CDW; customs status and duty paid; outbound
retailer freight including UBM and Amazon Vendor — ASN drafts, EDI 856, routing
guide compliance, pallet and label specs; carrier escalations handed off from
oc3pl-order-manager. Sample triggers: "where's the HCT shipment," "ETA on
Vegelabs," "what's stuck in customs," "draft an ASN for Ulta," "FedEx lost the
order — escalate."

**oc3pl-order-manager** runs daily DTC fulfillment from the OC3PL Logiwa
shipment report. Owns the OC3PL Order Management Asana project for the daily
parse, escalations, and weekly review, plus the SJ Shipping Dashboard project
for DTC consumer order errors and returns intake. Hands off carrier-side issues
to logistics-manager, end-customer quality complaints to complaint-and-event-
handler, and physical return receipt to inventory-manager. Sample triggers:
"upload today's Logiwa report," "what were yesterday's numbers," "any late
orders," "customer reported a damaged item," "process this return."

---

## The data flow

The five skills sit on a shared spine. Outlook and Fireflies feed the bridges.
The bridges feed Asana (operational signal) and PLM (records of truth) through
plm-assistant. The five Ops skills read PLM via Supabase SELECT, draft writes,
and commit through plm-assistant on Operations approval. Asana carries the
queue state per skill; each Ops skill has its own dedicated Asana project
under the each-skill-gets-its-own-project pattern.

```
Outlook (Inbox + Sent)             Fireflies (transcripts)
    │                                       │
    ▼                                       ▼
outlook-asana-bridge      outlook-plm-bridge      fireflies-asana-bridge
    │                            │                            │
    └──────────┬─────────────────┘                            │
               ▼                                              ▼
       Asana (per-skill project)  ◄────────────────────  meeting actions
               │                                              │
               │                                              │
   ┌───────────┼───────────┬───────────┬───────────┬──────────┘
   ▼           ▼           ▼           ▼           ▼
 purchasing  inventory  supply-demand  logistics  oc3pl-order
 -manager    -manager   -planner       -manager   -manager
   │           │           │            │           │
   └───────────┴────┬──────┴────────────┴───────────┘
                    ▼
              asana-plm-bridge ──► plm-assistant ──► PLM (Supabase)
                                                     ujkabbffvhpewpbttmmy
```

PLM is the source of truth for vendor, PO, batch, component, and product
records. plm-assistant is the only writer. No Ops skill bypasses it — even the
shortest path (an outbound PO email landing in PLM via outlook-plm-bridge) goes
through plm-assistant for the actual INSERT or UPDATE. Asana is the workflow
surface, never the source-of-truth store.

---

## Routing logic

Most Operations requests resolve to one skill. The decisions below cover the
single-skill cases, then the ambiguous cases where two skills could answer, and
finally the multi-skill chains that show up around month-close, S&OP runs, and
launch readiness.

### Single-skill triggers

| Request shape | Skill |
|---|---|
| Anything about vendors, POs, RFQs, compliance docs, payment terms | purchasing-manager |
| Anything about on-hand position, receiving, three-way recon, FEFO, near-expiry, returns disposition | inventory-manager |
| Anything about forecasts, S&OP, safety stock, what to buy, fill calendar, BOM explosion | supply-demand-planner |
| Anything about shipment ETAs, customs, duty, retailer ASN, EDI 856, routing guides, carrier escalations | logistics-manager |
| Anything about daily DTC numbers, Logiwa report, customer order errors, RMAs, damaged-item reports | oc3pl-order-manager |

### Ambiguous cases — decision rules

**purchasing-manager vs. supply-demand-planner.** Recommendation lives with
SDP; execution lives with Purchasing. "What should we buy" is SDP. "Place the
PO for that buy" is Purchasing. SDP drafts buy recommendations as Asana tasks
in the S&OP project's Buy Recommendations section; Purchasing picks them up on
approval and runs the actual P2P workflow. If the request mixes both — "buy
2,000 units of toner this month" — start with SDP for the demand signal, hand
off to Purchasing for the PO.

**inventory-manager vs. supply-demand-planner.** Inventory owns short-range
fulfillment burn-down (1–8 weeks, current position vs. target). SDP owns
everything beyond that horizon and every target inventory monitors against. A
low-stock signal sits with Inventory until it needs sequencing — at that point
Inventory routes it through S&OP for buy timing.

**inventory-manager vs. purchasing-manager.** Receiving is the seam. Purchasing
carries a PO through Draft → Sent → Acknowledged → In Transit. Inventory picks
up at the goods-received signal — opens the receive task, stages the batch in
PLM, commits on Operations approval. Purchasing then moves its PO to Received
and carries it through invoice and three-way match to Closed.

**logistics-manager vs. inventory-manager.** Logistics owns the move; Inventory
owns the location ledger entry. A transfer from OC3PL to an Ulta DC is
Logistics' shipment record; the inventory location change in PLM is Inventory's
commit on arrival confirmation.

**logistics-manager vs. oc3pl-order-manager.** OC3PL Order Manager owns the
daily DTC outbound numbers from the Logiwa report and customer-reported errors.
Carrier-side issues — lost shipment, RIA, label fail, address bounce, claims —
hand off to Logistics. Returns split: customer return reported (RMA) lives with
OC3PL Order Manager; physical receipt of returned stock at OC3PL hands off to
Inventory for disposition; carrier issues with the return shipment hand off to
Logistics.

**oc3pl-order-manager vs. complaint-and-event-handler.** OC3PL Order Manager
owns operational order errors — wrong item, missing item, damaged in transit
where the cause is fulfillment or carrier. Customer quality complaints — adverse
reaction, allergic event, product safety — hand off to complaint-and-event-
handler regardless of how they came in.

### Multi-skill chains

| Request | Chain |
|---|---|
| Run the monthly S&OP and place the buys | supply-demand-planner → purchasing-manager |
| Receive a PO and update the position | purchasing-manager → inventory-manager |
| Inbound shipment lands at KDC-One, then ships to OC3PL | logistics-manager → inventory-manager |
| Ulta PO comes in — draft the ASN and ship | logistics-manager → oc3pl-order-manager (for outbound coordination) |
| Daily DTC numbers + carrier escalation on a lost order | oc3pl-order-manager → logistics-manager |
| Customer return arrives at OC3PL | oc3pl-order-manager → inventory-manager (for disposition) |
| Low-stock flag triggers a buy | inventory-manager → supply-demand-planner → purchasing-manager |
| Vendor compliance lapse (expired COI) blocks a PO | purchasing-manager owns the lapse; inventory-manager flags any open receipts at risk |
| Branded Ops summary for the founder | any chain → sjs-status-reporter |

---

## Cross-skill handoff map

The handoffs below are the load-bearing transitions. Each one moves a record
or signal from one skill's queue to another's. None of these are duplicated
work — Asana supports a single task in multiple projects, and the rule is one
task, two project homes, one owner per side.

oc3pl-order-manager → logistics-manager. Carrier-side issues from the daily
DTC parse — lost shipment, RIA, label fail, address bounce, claims. OC3PL Order
Manager opens the Asana task in its own project, comments the carrier specifics,
and adds the same task to the Logistics project. Logistics owns the carrier
escalation; OC3PL Order Manager owns the customer-side resolution.

oc3pl-order-manager → complaint-and-event-handler. End-customer quality signals
— allergic reaction, injury, product safety. OC3PL Order Manager flags the
intake; complaint-and-event-handler walks SKN-OPS-002 and SKN-OPS-003.

oc3pl-order-manager → inventory-manager. Physical return receipt. Customer
return arrives at OC3PL; OC3PL Order Manager logs the RMA close; Inventory picks
up the receive movement and decides disposition (restock, write-off, vendor
return).

logistics-manager → inventory-manager. Receipt confirmation. Logistics tracks
the shipment to the dock; Inventory commits the location ledger entry on arrival
confirmation and stages the batch entry in PLM.

supply-demand-planner → purchasing-manager. Buy recommendations. SDP drafts
each buy in the S&OP project's Buy Recommendations section with vendor, quantity,
target ship-by, and rationale. Purchasing picks them up on approval and runs
the P2P workflow.

inventory-manager → supply-demand-planner. Low-stock and target-breach signals.
Inventory flags any SKU below safety stock or trending toward stockout in the
S&OP project's Risk Watch section. SDP produces the buy at the next run.

purchasing-manager → inventory-manager. PO close at receipt. Purchasing moves
the PO to Status = Received; Inventory takes the receive task and commits the
batch.

Any Ops skill → sjs-status-reporter. Branded outputs — status updates, founder
briefings, launch readiness reports, executive summaries. The five Ops skills
write operational signal; sjs-status-reporter formats it for SJS brand
guidelines.

---

## Bridges and foundation

The four shared bridges are how Operations content gets into Asana and PLM.
Operations skills do not query Outlook or Fireflies directly — they call the
bridges. The bridges are documented in their own SKILL.md files; this section
covers what Operations uses them for.

**outlook-asana-bridge.** Turns supplier and partner email content — both
inbound and from Sent Items — into Asana tasks, comments, and queue moves
inside the right Ops project. Used by every Ops skill: a vendor ack lands as a
Purchasing task, a carrier ship-notification lands as a Logistics task, an OC3PL
escalation email lands as an OC3PL Order task. The bridge flags PLM-bound
attachments for outlook-plm-bridge so records and tasks split cleanly.

**outlook-plm-bridge.** Turns supplier and partner email content into direct
PLM writes through plm-assistant — PO acknowledgments (Flow A), batch COAs
(Flow B), vendor onboarding (Flow C), formula approvals (Flow D), test results
(Flow E), invoices (Flow F), BOM and component spec updates (Flow G). Posts a
sync-back comment on the related Asana task (Flow H) so the Ops queue sees
what changed in PLM. Used heavily by purchasing-manager (vendor and PO
records), inventory-manager (batch records), and logistics-manager (shipment
documentation).

**fireflies-asana-bridge.** Turns meeting transcripts into Ops Asana actions.
Vendor reviews, S&OP runs, logistics calls, order ops standups all generate
action items this skill converts to Asana tasks against the appropriate Ops
project. Used when a meeting decision needs to commit to an Ops queue.

**asana-plm-bridge.** Syncs Asana-known data into PLM and surfaces PLM data
back into Asana. Used when a record originates in Asana — a formula approval
captured in a PD task, a vendor contact added during a meeting note — and needs
to land in the PLM record. Operations uses this less than the Outlook bridges
because most Ops records originate in supplier email, not in Asana.

**plm-assistant.** The only writer to PLM. Every System 5 write — vendor
record, PO, batch, location movement, forecast line, inventory target — goes
through plm-assistant. Reads can be Supabase SELECT direct; writes never are.
The PLM project ID is `ujkabbffvhpewpbttmmy` (Supabase).

---

## Confirmation rule

Reads and research run without confirmation across all five Ops skills. Every
write needs Operations approval before commit. The skill drafts and stages,
Operations approves, plm-assistant commits.

This applies uniformly to vendor onboarding, PO placement, batch creation on
receipt, location movements, manual adjustments, write-offs, return
dispositions, forecast updates, target resets, buy recommendations, shipment
record creation, and any Asana write that creates a task or moves a queue
state. The S&OP run is the one place bulk approval applies — every write in
the run bundles into a single approval, with auto-flagged exceptions reviewed
individually before the bulk clears.

Sensitive content rules carry across the system. Banking details, financial
account numbers, and government IDs never write to PLM, even when they appear
in vendor onboarding emails. The bridges strip them out of any draft before
plm-assistant sees the staged write.

---

## When you can't tell which Ops skill to use

Default to the spine. If the request is about money going out, start with
purchasing-manager. If it's about stuff sitting somewhere, start with
inventory-manager. If it's about what to buy and when, start with supply-demand-
planner. If it's about something in motion, start with logistics-manager. If
it's about today's DTC numbers or a customer order, start with oc3pl-order-
manager.

If the request still doesn't resolve cleanly, start with the skill that owns
the originating signal — where the request first lands in Outlook, Fireflies,
or the daily Logiwa report — and let the handoff map carry it forward.

If the request ends in a deliverable for the founder, the brand team, or a
retailer, the final step is always sjs-status-reporter.

---

## System integration

**Calls into:** outlook-asana-bridge, outlook-plm-bridge, fireflies-asana-
bridge, asana-plm-bridge (the four shared bridges); plm-assistant (sole PLM
writer); sjs-status-reporter (branded output); complaint-and-event-handler
(end-customer quality signals from oc3pl-order-manager); sjs-comp-intel and
sjs-retail-intel (signals into supply-demand-planner auto-adjustments).

**Called by:** Operations directly through any trigger phrase; future System 6
(Quality Management) and System 7 (Regulatory) skills as they come online; the
PD router (sjs-pd-system) when a PD request crosses into Ops territory.

**Doesn't duplicate:** PD task management (asana-pd-manager handles PD
projects); margin work (sjs-margin-architect family); retail and competitive
intel (sjs-retail-intel, sjs-comp-intel); branded formatting (sjs-status-
reporter); founder briefings (ayesha-weekly-briefing); holiday comms (ac-
brands-holiday-comms). The router stays in the Ops lane and hands off
otherwise.

---

## Workspace and project context

| Surface | Identifier |
|---|---|
| Asana workspace | AC Brands (`ac-brands.com`) |
| Asana team | SJ Ops (`1202786171817904`) |
| PLM project | Supabase `ujkabbffvhpewpbttmmy` |
| Brand in scope | Sweet July Skin (occasional cross-brand work flagged in task descriptions) |
| Active sales channels | DTC, UBM, Amazon (Sephora not yet active) |
| Key launch | Ulta Beauty Marketplace, June 2026 |

Each Ops skill operates a dedicated Asana project. References for the cached
project, section, and custom-field GIDs live inside each skill's own SKILL.md
and references files — the router does not duplicate them.

---

## Reference pointers

- `purchasing-manager/SKILL.md` — full purchase-to-pay job list, Status
  field options, vendor and PO write patterns
- `inventory-manager/SKILL.md` — position-keeping, receiving, recon, FEFO,
  return disposition flows
- `supply-demand-planner/SKILL.md` — monthly S&OP run mechanics; nine custom
  fields and S&OP project schema
- `logistics-manager/SKILL.md` — seven freight flows, retailer compliance,
  customs, escalation paths
- `oc3pl-order-manager/SKILL.md` — daily Logiwa parse, two Asana projects,
  weekly review structure
- `plm-assistant/SKILL.md` — PLM write monopoly, caller list, RLS rules
- `outlook-asana-bridge/SKILL.md`, `outlook-plm-bridge/SKILL.md`,
  `fireflies-asana-bridge/SKILL.md`, `asana-plm-bridge/SKILL.md` — the four
  shared bridges Ops calls into

System 6 (Quality Management — quality-manager) and System 7 (Regulatory —
regulatory-manager) are next in the build queue. When those skills land, the
router picks them up as additional callers without restructuring.
