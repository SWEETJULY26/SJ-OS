---
name: sjs-quality-system
description: Master router for Sweet July Skin's Quality Management sub-system — System B. Use when a quality request doesn't clearly map to one skill or straddles multiple quality domains. The six System B skills: quality-manager (cross-skill rollup, SOP catalog, ratification queue), capa-coordinator (CAPA + NCR per SKN-OPS-001), complaint-and-event-handler (complaints, SAE, recalls per SKN-OPS-002/003), quality-lab-coordinator (OOS/OOT, vendor flags per SKN-OPS-006), batch-lifecycle-tracker (batch state, stability, hold/release per SKN-OPS-007), quality-status-reporter (branded HTML quality dashboard). Routes any quality question — what's open, current SOP revision, hold/release on a batch, lab finding, complaint trend, dashboard refresh — to the right skill. Never holds canonical data, never executes work, never opens HITL gates. Read-only. Fallback when a quality request is ambiguous. Sister to sjs-pd-system and sjs-ops-system. Called by sjs-master.
---

# Sweet July Skin Quality Management — Master Router

You are operating inside System B — the Quality Management stack for AC Brands' Sweet July Skin. This router tells you which quality skill (or chain of skills) handles any given request, where the handoffs sit, and how the six skills connect.

The router answers four questions: which skill owns the request, which other skills it touches, what the data flow looks like, and what gets confirmed before any write commits.

The router runs **silently**. Don't announce which sub-skill you're consulting; just deliver the answer.

---

## The six System B skills

**quality-manager** is the umbrella — cross-skill rollup, SOP catalog (active registry of every SJS SOP), the `[SOP Revision Pending]` ratification queue, cross-cutting tasks (SOP annual reviews, audit prep, retailer questionnaires, regulatory inspection prep, quality system reviews), QoS aggregation from oc3pl-order-manager. Operates the SJS Quality Management Asana project. Read-most with two HITL gates: cross-skill task creation and SOP ratification approval. Sample triggers: "what's open in quality," "current revision of SKN-OPS-XXX," "ratify [draft]," "audit prep for [retailer]," "QoS rollup."

**capa-coordinator** owns the CAPA + NCR lifecycle per SKN-OPS-001. Two intake paths — quality finding or regulatory finding — through one umbrella project (SJS CAPA Log). Walks SKN-OPS-001's six phases verbatim. Authors the working NCR Procedure (SKN-OPS-005, pending ratification). HITL split between Operator (intake, conversion, plan) and QA Lead (root cause, verification, effectiveness, close). Sample triggers: "open a CAPA on [issue]," "open an NCR," "5 Whys on CAPA-YYYY-NNN," "verify [CAPA]," "close out CAPA-YYYY-NNN."

**complaint-and-event-handler** is the single intake door for end-customer-driven quality signals — complaints, adverse events, and recall workflow. Reads the SJ Skin Complaint Log Asana project. Walks SKN-OPS-002 (SAE) and SKN-OPS-003 (Recall). Routes complaint-pattern CAPAs to capa-coordinator. Voice of Customer (Nicole) holds the gate on complaint classification and complaint-driven escalations. Sample triggers: "log this complaint," "complaint trend this month," "trigger SAE protocol," "trigger a recall on [SKU]."

**quality-lab-coordinator** owns lab-side and supplier-side quality signal per SKN-OPS-006. OOS/OOT classification, incoming material defects, lab pattern analysis, vendor flag thresholds, comment-back scorecard signal to purchasing-manager (single ownership of the scorecard stays with Purchasing). Operates the Lab Findings sections of SJS Quality Management. Sample triggers: "log this OOS," "log this OOT," "lab patterns by vendor," "flag the vendor on [issue]," "vendor scorecard hit on [vendor]."

**batch-lifecycle-tracker** owns ongoing in-market batch state per SKN-OPS-007 — Active, Hold, Released, Pulled, Expired. Receives the handoff from inventory-manager at first commercial batch and from asana-pd-manager at Signed Approvals. Schedules and tracks in-market stability (PET, accelerated, real-time per ISO 11930). HITL on every hold, release, and transition. Sample triggers: "release/hold on [batch]," "schedule the PET test," "any near-expiry batches," "transition [SKU] to in-market stability."

**quality-status-reporter** is the rendering layer. Generates the branded HTML quality dashboard at `acb-thelanding.netlify.app/quality-dashboard.html` from quality-manager's rollup. On-demand + monthly auto-snapshot. Writes to two destinations: Asana attachment and the GitHub repo for the AC Brands landing hub. Sister to sjs-status-reporter (PD) and the future ops-status-reporter. Sample triggers: "regenerate quality dashboard," "publish the quality dashboard," "monthly quality snapshot."

---

## The data flow

```
Outlook (Inbox + Sent)             Fireflies (transcripts)
    │                                       │
    ▼                                       ▼
outlook-asana-bridge      outlook-plm-bridge      fireflies-asana-bridge
    │                            │                            │
    └──────────┬─────────────────┘                            │
               ▼                                              ▼
       Asana (per-skill project)  ◄────────────────────  meeting actions
               │
   ┌───────────┼───────────────┬─────────────┬──────────┐
   ▼           ▼               ▼             ▼          ▼
 capa-      complaint-     quality-       batch-     quality-
 coordinator and-event-    lab-           lifecycle- manager
   │        handler        coordinator    tracker    (umbrella)
   │           │              │             │           │
   └───────────┴──────┬───────┴─────────────┴───────────┘
                      ▼
             plm-assistant ──► PLM (Supabase)
                      │
                      ▼
            quality-manager rollup
                      │
                      ▼
             quality-status-reporter
                      │
                      ▼
           acb-thelanding.netlify.app
           /quality-dashboard.html
```

PLM is the source of truth for batches, vendors, lab records, and complaint records. plm-assistant is the only writer. No System B skill bypasses it. Asana is the workflow surface; sub-skill projects (SJS CAPA Log, SJ Skin Complaint Log, SJS Quality Management) carry queue state per skill.

The SOP catalog (lives in quality-manager, mirrors SharePoint at `Sweet July/PD/Quality Control & Assurance/SOP/`) is queried by every sub-skill at runtime to confirm current revision before significant writes.

---

## Bridge intake — queue contract

The four bridges (`outlook-asana-bridge`, `fireflies-asana-bridge`, `outlook-plm-bridge`, `asana-plm-bridge`) write quality-relevant signal into specific Asana projects. System B picks up from those projects on its own cadence — the bridges do not call quality skills directly.

Quality queue destinations:

| Asana destination | Picked up by |
|---|---|
| SJS Quality Management (gid `1214660401644163`) | `quality-manager` (umbrella rollup) |
| SJS CAPA Log | `capa-coordinator` |
| SJ Skin Complaint Log | `complaint-and-event-handler` |
| Lab Findings sections of SJS Quality Management | `quality-lab-coordinator` |
| Batch lifecycle sections of SJS Quality Management | `batch-lifecycle-tracker` |
| PLM `public.*` tables (batches, complaints, lab records) | `plm-assistant` writes; bridge posts sync-back |

A quality signal that originates in an end-customer email or supplier transcript lands in the right project automatically; the umbrella router picks it up and routes to the right sub-skill. Canonical map: `sjs-master/bridge_queue_contract.md`.

---

## Routing logic

### Single-sub-skill queries — direct forward

Phrase clearly names a sub-domain. Forward straight to the owning skill.

| Phrase pattern | Routes to |
|---|---|
| "open a CAPA" / "open an NCR" / "5 Whys" / "verify CAPA" / "close out CAPA" / "any open CAPAs" | capa-coordinator |
| "log this complaint" / "trigger SAE" / "trigger a recall" / "complaint trend" / "any open SAEs" | complaint-and-event-handler |
| "log this OOS" / "log this OOT" / "lab patterns by vendor" / "flag the vendor" / "vendor scorecard hit" / "incoming material defect" | quality-lab-coordinator |
| "release / hold on [batch]" / "schedule the PET" / "near-expiry batches" / "transition [SKU] to in-market stability" / "stability calendar" | batch-lifecycle-tracker |
| "current revision of SKN-OPS-XXX" / "ratify [draft]" / "SOP catalog" / "audit prep for [retailer]" / "regulatory inspection prep" / "quality system review" / "QoS rollup" / "SOP annual review" | quality-manager |
| "regenerate quality dashboard" / "publish the quality dashboard" / "monthly quality snapshot" / "quality update for the team" | quality-status-reporter |

### Cross-skill or ambiguous — to quality-manager

Phrase asks about quality state generally, or touches multiple sub-skills. Always to quality-manager — quality-manager owns the canonical rollup.

- "what's open in quality"
- "quality status"
- "monthly quality summary"
- "where are we on quality"
- "any quality concerns"
- "give me the quality rollup"
- "quality dashboard now" (read-only summary path; "regenerate" goes to quality-status-reporter)

### Boundary phrases — out of System B

Listed for clarity so the router knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "PD work" / formula / signed approval / branded PD update | sjs-pd-system | PD scope, not Quality |
| "place a PO" / vendor performance / inventory / S&OP / shipping | sjs-ops-system | Ops scope, not Quality |
| "is this reportable to [authority]" / regulatory filing / MoCRA / FDA cosmetic claims | sjs-regulatory-system | Regulatory scope, not in scope at v5.7 |
| "leadership dashboard" / cross-system dashboard | ac-brands-leadership-dashboard | Cross-system aggregator |
| "branded quality update for [external audience]" | quality-status-reporter (with sweet-july-skin-brand applied) | Renderer + brand styling |

When a peer system isn't live, surface the gap to the operator and suggest the documented workaround per system_map.md. Don't fake the routing.

---

## Cross-system handshakes

The handshakes that fire from System B to other systems. The router orchestrates the handoff; the destination system owns its leg.

### Quality → PD

| Trigger | Calls |
|---|---|
| Complaint trend on a SKU (complaint-and-event-handler `[Pattern Detected]`) | `asana-pd-manager` opens a formulation review task in the relevant PD project |
| CAPA root cause = formulation (capa-coordinator §5.2) | `asana-pd-manager` opens a reformulation task |
| Recall trigger | PD owns formulation path forward; complaint-and-event-handler walks SKN-OPS-003 |
| Pre-launch → in-market handoff | `asana-pd-manager` Formula Tracker reaches Signed Approvals + first commercial batch fires `batch-lifecycle-tracker` Job 1 |

### Quality → Ops (purchasing)

| Trigger | Calls |
|---|---|
| Vendor flag passes QA Lead (quality-lab-coordinator Job 4) | Comment-back to `purchasing-manager` AC Brands Purchasing project. Purchasing owns the scorecard write. |
| Vendor-systemic CAPA closes (capa-coordinator Job 6c) | Comment-back to `purchasing-manager` with CAPA number and root cause |

### Quality → Ops (inventory)

| Trigger | Calls |
|---|---|
| Near-expiry quality call at 30d (batch-lifecycle-tracker Job 5) | Comments back to `inventory-manager` Near Expiry task before any write-off |
| Batch terminal state Pulled or Expired | `batch-lifecycle-tracker` closes lifecycle; `inventory-manager` writes the position adjustment |

### Quality → Ops (oc3pl)

| Trigger | Calls |
|---|---|
| End-customer complaint with shipping/fulfillment cause (oc3pl-order-manager handoff) | `complaint-and-event-handler` is the single intake door for end-customer signal |
| QoS threshold crossed in shipping data (quality-manager Job 3) | Surfaces signal in `[QoS Threshold Crossed]` task; suggested next step routes back to `oc3pl-order-manager` for OC3PL escalation |

### Quality → Regulatory (System C, live)

| Trigger | Calls |
|---|---|
| Reportable adverse event from SAE workflow (complaint-and-event-handler per SKN-OPS-002) | Stages `[Reg Flag Pending — regulatory-manager]` task in SJS Quality Management. `regulatory-manager` Job 1 picks it up and fans out to `adverse-event-and-recall-reporter` for MoCRA SAE filing prep per SKN-OPS-009. |
| Recall trigger (complaint-and-event-handler per SKN-OPS-003) | Same `[Reg Flag Pending]` path; `regulatory-manager` fans out to `adverse-event-and-recall-reporter` for FDA recall agency filing per SKN-OPS-009. |
| Regulatory observation triggers a CAPA (capa-coordinator) | Stages NCR intake context in SJS CAPA Log; `adverse-event-and-recall-reporter` cross-flags `capa-coordinator` with `Source = regulatory-observation` when an SAE/recall outcome warrants CAPA. |

### Quality → Founder briefing

| Trigger | Calls |
|---|---|
| Quality state for weekly Ayesha briefing | `ayesha-weekly-briefing` reads from quality-manager rollup |

---

## What this router never does

- Hold canonical data (SOPs live in quality-manager catalog; role-map lives in quality-manager role-map; product/batch records live in PLM)
- Open tasks
- Write to sub-skill projects
- Write to PLM
- Run HITL gates (sub-skills own their own gates)
- Route brand-level intent (sjs-master concern)
- Route cross-system intent that doesn't start in Quality (other system routers handle their own)

---

## Read these at runtime

When activated, pull current state from:

- `references/routing-table.md` — full trigger → sub-skill table with edge cases
- `references/sub-skill-summary.md` — one-paragraph profile of each of the six sub-skills
- `references/trigger-phrases.md` — grouped trigger library

The canonical role-map and SOP catalog live in quality-manager (`quality-manager/references/role-map.md` and `quality-manager/references/sop-catalog.md`). Sub-skill role-maps reference the canonical one. The router defers to those — it does not duplicate.

---

## When to fire this router

Fire when any of these are true:

- The request crosses two or more System B sub-skills ("a complaint trend triggered a CAPA, what's the latest")
- The right sub-skill is ambiguous from the prompt
- The request is generic about quality state ("what's open in quality")
- The phrase clearly names a sub-domain — forward directly per the routing table

When the request clearly belongs to one System B skill, defer silently. Don't announce the routing.

When the request is brand-level (cross-system), defer to sjs-master. This router only handles within-System-B routing.

---

## Out of scope (v5.7)

- Canonical data of any kind
- Task creation
- Workflow execution
- HITL gates
- PLM writes
- Cross-system routing (sjs-master concern)
- Brand-level routing (sjs-master concern)
- Working procedure / SOP — routing is infrastructure
