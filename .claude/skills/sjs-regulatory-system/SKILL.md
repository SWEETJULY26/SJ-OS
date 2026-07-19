---
name: sjs-regulatory-system
description: Master router for Sweet July Skin's Regulatory Management sub-system — System C. Use when a regulatory request doesn't clearly map to one skill or straddles multiple regulatory domains. The five System C skills: regulatory-manager (rollup, registrations, retailer attestation cadence, Pedrero liaison), claims-il-and-label-keeper (IL review gate, claim sub, label archive, retailer attestation responses per SKN-OPS-008), adverse-event-and-recall-reporter (MoCRA SAE, FDA recall, statutory clocks per SKN-OPS-009), regulatory-status-reporter (branded HTML regulatory dashboard). Routes any regulatory question — registrations renewing, SAE clock, recall classification, attestation cadence, Pedrero liaison, dashboard refresh — to the right skill. Never holds canonical data, executes work, or opens HITL gates. Read-only fallback when a regulatory request is ambiguous. Sister to sjs-pd-system, sjs-quality-system, sjs-ops-system. Called by sjs-master.
---

# Sweet July Skin Regulatory Management — Master Router

You are operating inside System C — the Regulatory Management stack for AC Brands' Sweet July Skin. This router tells you which regulatory skill (or chain of skills) handles any given request, where the handoffs sit, and how the five skills connect.

The router answers four questions: which skill owns the request, which other skills it touches, what the data flow looks like, and what gets confirmed before any write commits.

The router runs **silently**. Don't announce which sub-skill you're consulting; just deliver the answer.

---

## The five System C skills

**regulatory-manager** is the umbrella — cross-skill rollup, registrations tracker (MoCRA listings, MoCRA facility registrations, CA Prop 65, CA Fragrance and Flavor Right to Know, CA Toxic-Free Cosmetics Act, NY/WA/OR cosmetic registries, Leaping Bunny Certification, retailer-specific filings, **state packaging laws — CA SB 343 Truth in Recycling Labeling, 19-state packaging toxics cert of compliance, EPR threshold monitoring (CA/OR/CO + 3 incoming states)**, **international markets — Health Canada cosmetic notification, Quebec French-language compliance, pending UK / South Africa**), retailer attestation cadence dashboard, Pedrero liaison surface (cross-skill view of pending/sent/overdue Pedrero work plus engagement-level work — contract renewals, capacity-planning roadmap), **international RP partner liaison (Ecomundo for Canada / EU plus Pedrero alternatives — see `regulatory-manager/references/rp-partners.md`)**, ayesha-weekly-briefing seam for founder-level regulatory signals. Intercepts Quality's `[Reg Flag Pending — regulatory-manager]` queue and fans out to the right sub-skill per Operator-confirmed type. Operates the SJS Regulatory Management Asana project. Read-most with HITL gates: cross-skill task creation, registration writes, attestation reminder edits, fan-out routing decisions. Sample triggers: "what's open in regulatory," "any registrations renewing," "next attestation due," "what's pending with Pedrero," "Canada compliance status," "EPR threshold," "SB 343 Pantone audit," "monthly regulatory summary."

**claims-il-and-label-keeper** owns the pre-launch IL review gate, sustained claim substantiation, label artwork archive, and retailer attestation responses (Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo) per SKN-OPS-008 **Rev.2**. Receives the IL gate trigger from asana-pd-manager when Formula Tracker hits Signed Approvals. Stages every IL packet, claim sub write, attestation response, and label archive entry to Pedrero. At Rev.2 (2026-05-12) the label cross-check runs four passes: IL match, Pantone per CA SB 343, Canada extended-allergens, Quebec French-language. The IL packet at Rev.2 requires a 19-state packaging-toxics certificate of compliance for retailer-distributed SKUs. New-claim sign-off adds §7.4 reformulation claim-bridge gate (Eye Cream / Toner / Power Oil flagged). Operates inside SJS Regulatory Management (shared project with regulatory-manager; lifecycle-state-based sections). HITL on every Pedrero send and every retailer-facing submission. Sample triggers: "stage the IL on [SKU]," "log the new IL version," "what claims do we have on [SKU]," "review this new claim," "stage the [retailer] attestation," "did Pedrero sign off on the new label," "Pantone check on [SKU]," "Canada label review on [SKU]," "Quebec bilingual check on [SKU]," "reformulation claim bridge."

**adverse-event-and-recall-reporter** owns the agency side of MoCRA serious adverse events and FDA product recalls per SKN-OPS-009. Receives cross-flag from Quality via regulatory-manager fan-out. Drafts proposed classifications (MoCRA SAE definition criteria, 21 CFR 7 Class I/II/III), stages packets to Pedrero, tracks statutory clocks (15-day SAE, 1-3 day Class I, ~10 day Class II, ~30 day Class III), submits filings (MedWatch, FDA recall portal, state DOH channels). Operates SJS Reportable Events Asana project (gid 1214660834583706). HITL on every Pedrero send and every agency submission as two distinct gates per filing. Sample triggers: "log this SAE for FDA reporting," "what's the clock on the [SKU] SAE filing," "stage the recall report for Pedrero," "any open SAEs at FDA," "did we close the [batch] recall agency-side."

**regulatory-status-reporter** is the rendering layer. Generates the branded HTML regulatory dashboard at `acb-thelanding.netlify.app/regulatory-dashboard.html` from regulatory-manager's rollup. On-demand + monthly auto-snapshot. **Seven KPI sections at v6.6:** Reportable Events (with statutory clock bars), Pedrero (cross-skill rollup), Retailer Attestations + Active Registrations, IL + Label Artwork, **State Packaging Laws (SB 343 Pantone audit, 19-state toxics certs, EPR threshold monitor)**, **International Markets (Canada compliance with extended-allergens countdown, UK / South Africa pending)**, **Reformulation Claim-Bridge Watch (Eye Cream / Toner / Power Oil)**. Writes to two destinations: Asana attachment and the GitHub repo for the AC Brands landing hub. Sister to quality-status-reporter, sjs-status-reporter, and the future ops-status-reporter. Sample triggers: "regenerate regulatory dashboard," "publish the regulatory dashboard," "monthly regulatory snapshot."

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
   ┌───────────┼─────────────────────────┐
   ▼           ▼                         ▼
 claims-      adverse-event-       regulatory-
 il-and-      and-recall-          manager
 label-       reporter             (umbrella +
 keeper       (SJS Reportable      registrations +
 (SJS Reg     Events)              Pedrero liaison)
 Mgmt)         │                         │
   │           └────────────┬────────────┘
   └────────────────────────┤
                            ▼
                     plm-assistant ──► PLM (Supabase)
                            │
                            ▼
                  regulatory-manager rollup
                            │
                            ▼
                  regulatory-status-reporter
                            │
                            ▼
                 acb-thelanding.netlify.app
                 /regulatory-dashboard.html
```

PLM is the source of truth for SKUs, batches, formulas, complaints. plm-assistant is the only writer. No System C skill bypasses it. Asana is the workflow surface; SJS Regulatory Management (gid 1214660807386611) and SJS Reportable Events (gid 1214660834583706) carry queue state. Artifacts (IL packets, claim sub evidence, label files, attestation drafts, registration filings, agency correspondence, Pedrero correspondence) live in SharePoint at `Sweet July/Regulatory/` once stood up; Asana attachments at v6.1/v6.2 interim until v6.3 SharePoint migration.

The SOP catalog (lives in quality-manager, mirrors SharePoint at `Sweet July/PD/Quality Control & Assurance/SOP/`) holds System C SOPs (SKN-OPS-008 IL/Claims/Label, SKN-OPS-009 Reportable Events) alongside System B SOPs. Sub-skills query the catalog at runtime to confirm current revision before significant writes.

Pedrero Regulatory (Amy Pedrero principal, Heather Folkes and Teona Bebia secondary) is the external reviewer across System C. Canonical contact card lives in `regulatory-manager/references/pedrero-contacts.md`.

---

## Bridge intake — queue contract

The four bridges (`outlook-asana-bridge`, `fireflies-asana-bridge`, `outlook-plm-bridge`, `asana-plm-bridge`) write regulatory-relevant signal into specific Asana projects. System C picks up from those projects on its own cadence — the bridges do not call regulatory skills directly.

Regulatory queue destinations:

| Asana destination | Picked up by |
|---|---|
| SJS Regulatory Management (gid `1214660807386611`) | `regulatory-manager` (umbrella rollup, intake staging) |
| SJS Reportable Events (gid `1214660834583706`) | `adverse-event-and-recall-reporter` |
| IL / Claims / Label sections of SJS Regulatory Management | `claims-il-and-label-keeper` |
| PLM `public.*` tables (SKU, batch, formula records) | `plm-assistant` writes; bridge posts sync-back |

A regulatory signal that originates in a Pedrero email or partner transcript lands in the right project automatically; `regulatory-manager` Job 1 intercepts `[Reg Flag Pending]` and fans out to the right sub-skill. Canonical map: `sjs-master/bridge_queue_contract.md`.

---

## Routing logic

### Single-sub-skill queries — direct forward

Phrase clearly names a sub-domain. Forward straight to the owning skill.

| Phrase pattern | Routes to |
|---|---|
| "stage the IL on [SKU]" / "log the new IL version" / "review this new claim" / "stage the [retailer] attestation" / "did Pedrero sign off on the new label" / "claim sub on [SKU]" / "label artwork archive" / "Pantone check on [SKU]" / "SB 343 check on [SKU]" / "Canada label review on [SKU]" / "Quebec bilingual check on [SKU]" / "reformulation claim bridge on [SKU]" | claims-il-and-label-keeper |
| "log this SAE for FDA reporting" / "what's the clock on [SKU] SAE" / "stage the recall report" / "draft the FDA Class [I/II/III] report" / "any open SAEs" / "any open recalls" / "submit the [SKU] SAE to FDA" / "state AE filing" | adverse-event-and-recall-reporter |
| "any registrations renewing" / "MoCRA listing status" / "MoCRA facility registration" / "CA Prop 65" / "CA Fragrance and Flavor Right to Know" / "CA Toxic-Free Cosmetics Act" / "WA Toxic-Free Cosmetics Act" / "Leaping Bunny renewal" / "what's pending with Pedrero" / "any reg flags waiting" / "Pedrero engagement renewal" / "next attestation due" / "Canada compliance status" / "Health Canada notification on [SKU]" / "EPR threshold" / "SB 343 Pantone audit" / "19-state packaging toxics cert" / "what's pending with Ecomundo" / "RP partner [country]" / "send the PD roadmap to Pedrero" | regulatory-manager |
| "regenerate regulatory dashboard" / "publish the regulatory dashboard" / "monthly regulatory snapshot" / "branded regulatory update" / "regulatory update for the team" | regulatory-status-reporter |

### Cross-skill or ambiguous — to regulatory-manager

Phrase asks about regulatory state generally, or touches multiple sub-skills. Always to regulatory-manager — regulatory-manager owns the canonical rollup.

- "what's open in regulatory"
- "regulatory status"
- "monthly regulatory summary"
- "where are we on regulatory"
- "any regulatory concerns"
- "give me the regulatory rollup"
- "regulatory dashboard now" (read-only summary path; "regenerate" goes to regulatory-status-reporter)

### Boundary phrases — out of System C

Listed for clarity so the router knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "PD work" / formula / signed approval / branded PD update | sjs-pd-system | PD scope, not Reg |
| "place a PO" / vendor performance / inventory / S&OP / shipping | sjs-ops-system | Ops scope, not Reg |
| "open a CAPA" / "open an NCR" / "log this OOS" / "log this complaint" / "trigger SAE protocol" / "branded quality update" | sjs-quality-system | Quality scope, not Reg (Quality cross-flags Reg via `[Reg Flag Pending — regulatory-manager]`; that lands in regulatory-manager Job 1, not here directly) |
| "leadership dashboard" / cross-system dashboard | future leadership-dashboard | Cross-system aggregator |
| "branded regulatory update for [external audience]" | regulatory-status-reporter (with sweet-july-skin-brand applied) | Renderer + brand styling |

---

## Cross-system handshakes

The handshakes that fire from System C to other systems. The router orchestrates the handoff; the destination system owns its leg.

### Regulatory ← Quality

| Trigger | Calls |
|---|---|
| Confirmed SAE per SKN-OPS-002 | Quality complaint-and-event-handler stages `[Reg Flag Pending — regulatory-manager]` in SJS Quality Management; regulatory-manager Job 1 fans out to adverse-event-and-recall-reporter |
| Confirmed recall per SKN-OPS-003 | Same fan-out path; regulatory-manager routes to adverse-event-and-recall-reporter |
| State AE report needed | Same fan-out path |
| Regulatory inspection prep | quality-manager cross-cutting task references regulatory-manager |

### Regulatory ← PD

| Trigger | Calls |
|---|---|
| Formula reaches Signed Approvals on Formula Tracker | asana-pd-manager flips `IL Status = Pending IL Review` and creates `[IL Review Pending — claims-il-and-label-keeper]` task in SJS Regulatory Management Inbound Staging |
| Formula reformulation | asana-pd-manager flips `IL Status = IL Reformulated — Re-review Required`; claims-il-and-label-keeper re-fires the IL gate |
| New claim from PD or marketing | claims-il-and-label-keeper Job 5 stages to Pedrero |

### Regulatory → PD

| Trigger | Calls |
|---|---|
| IL approved by Pedrero | claims-il-and-label-keeper sync-back comment to asana-pd-manager Formula Tracker; PD can finalize component and carton artwork |
| IL returned for reformulation | claims-il-and-label-keeper sync-back with Pedrero rationale; PD restarts formula loop |

### Regulatory → Quality

| Trigger | Calls |
|---|---|
| SAE or recall outcome warrants CAPA | adverse-event-and-recall-reporter stages NCR intake context in SJS CAPA Log Inbound Staging with `Source = regulatory-observation` |
| Recall affects in-market batches | adverse-event-and-recall-reporter stages `[Batch Hold Request — batch-lifecycle-tracker]` for affected batches |
| Recall surfaces a label-related issue | adverse-event-and-recall-reporter cross-flags claims-il-and-label-keeper |

### Regulatory ← Ops

| Trigger | Calls |
|---|---|
| Vendor compliance docs at incoming inspection (COA, COC, COI, MSDS) | purchasing-manager handles intake; regulatory-manager reads when an audit needs cross-skill compliance docs |
| Distribution data for recall reports | adverse-event-and-recall-reporter reads oc3pl-order-manager for DTC + retailer breakdown |

### Regulatory → Founder briefing

| Trigger | Calls |
|---|---|
| Regulatory state for weekly Ayesha briefing | ayesha-weekly-briefing pulls from regulatory-manager rollup per Founder Filter rule #5 (SAE in flight, recall in flight, statutory clock breach risk, attestation overdue or imminent, Pedrero engagement issues, regulatory landscape change) |

---

## What this router never does

- Hold canonical data (Pedrero contacts live in regulatory-manager pedrero-contacts.md; role-map lives in regulatory-manager role-map; SOPs live in quality-manager catalog; product/batch/formula records live in PLM)
- Open tasks
- Write to sub-skill projects
- Write to PLM
- Run HITL gates (sub-skills own their own gates)
- Route brand-level intent (sjs-master concern)
- Route cross-system intent that doesn't start in Regulatory (other system routers handle their own)

---

## Read these at runtime

When activated, pull current state from:

- `references/routing-table.md` — full trigger → sub-skill table with edge cases
- `references/sub-skill-summary.md` — one-paragraph profile of each of the four sub-skills
- `references/trigger-phrases.md` — grouped trigger library

The canonical role-map and Pedrero contact card live in regulatory-manager (`regulatory-manager/references/role-map.md` and `regulatory-manager/references/pedrero-contacts.md`). The SOP catalog lives in quality-manager. Sub-skill role-maps reference the canonical regulatory-manager one. The router defers to those — it does not duplicate.

---

## When to fire this router

Fire when any of these are true:

- The request crosses two or more System C sub-skills ("the SAE we filed last month surfaced a label issue, what's the latest")
- The right sub-skill is ambiguous from the prompt
- The request is generic about regulatory state ("what's open in regulatory")
- The phrase clearly names a sub-domain — forward directly per the routing table

When the request clearly belongs to one System C skill, defer silently. Don't announce the routing.

When the request is brand-level (cross-system), defer to sjs-master. This router only handles within-System-C routing.

---

## Out of scope (v6.5)

- Canonical data of any kind
- Task creation
- Workflow execution
- HITL gates
- PLM writes
- Cross-system routing (sjs-master concern)
- Brand-level routing (sjs-master concern)
- Working procedure / SOP — routing is infrastructure
