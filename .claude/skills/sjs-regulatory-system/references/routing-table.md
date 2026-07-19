# Routing table — full trigger → sub-skill map with edge cases

The router's canonical intent → destination map. Edge cases at the bottom.

## Direct forward — phrase clearly names a sub-domain

### claims-il-and-label-keeper

| Phrase pattern | Notes |
|---|---|
| "stage the IL on [SKU]" | Normal IL gate intake (manual operator path; Formula Tracker hook also fires automatically) |
| "log the new IL version on [SKU]" | Same as above; explicit version log |
| "what IL is on the latest [SKU] batch" | Read-only IL version query |
| "is there a current IL on [SKU]" | Read-only |
| "review this new claim on [SKU]" | Job 5 new-claim sign-off |
| "is this claim defensible" | Same |
| "Pedrero sign-off needed on [claim]" | Same |
| "stage the [retailer] attestation for [SKU]" | Job 6 attestation drafting |
| "renew the Sephora Clean attestation on [SKU]" | Same |
| "draft the Ulta Conscious Beauty response for [SKU]" | Same |
| "fill out the Whole Foods questionnaire for [SKU]" | Same |
| "Credo attestation due on [SKU]" | Same |
| "log the new label artwork on [SKU]" | Job 4 label cross-check + archive |
| "did Pedrero sign off on the new [SKU] label" | Same |
| "archive the [SKU] [carton/component] artwork" | Same |
| "cross-check the [SKU] artwork against current IL" | Same |
| "what label version is on [SKU]" | Read-only |
| "what claims do we have on [SKU]" | Read-only claim sub query |
| "Pantone check on [SKU]" / "SB 343 check on [SKU]" | Job 4 Pass 2 (Rev.2) — CA SB 343 Pantone audit on label artwork |
| "Canada label review on [SKU]" / "Canada extended-allergens check on [SKU]" | Job 4 Pass 3 (Rev.2) — Canada extended-allergens artwork check; fires for Canada-bound SKUs |
| "Quebec bilingual check on [SKU]" / "Quebec French-language review on [SKU]" | Job 4 Pass 4 (Rev.2) — Quebec dual-language artwork check; fires for Quebec-bound SKUs |
| "reformulation claim bridge on [SKU]" / "can we keep the [SKU] clinical claims after reformulation" | Job 5 §7.4 (Rev.2) — reformulation claim-bridge gate |
| "do we have a 19-state toxics cert for [supplier]" / "request the toxics cert from [vendor]" | Job 1 IL gate intake (Rev.2 IL packet element) |

### adverse-event-and-recall-reporter

| Phrase pattern | Notes |
|---|---|
| "log this SAE for FDA reporting" | Operator-direct intake (also fires automatically when regulatory-manager fan-out lands a confirmed SAE) |
| "what's the clock on [SKU] SAE filing" | Job 7 statutory clock query |
| "stage the recall report for Pedrero" | Job 4 Pedrero send |
| "draft the FDA Class [I/II/III] report" | Job 3 packet drafting |
| "submit the [SKU] SAE to FDA" | Job 6 agency submission |
| "file the recall report" | Same |
| "any open SAEs at FDA" | Read-only status |
| "any open recalls" | Same |
| "did we close the [batch] recall agency-side" | Same |
| "log the agency acknowledgment on [event]" | Job 7 agency response |
| "draft the agency follow-up reply" | Same |
| "state AE filing on [SKU]" | State AE per CA/NY/WA/OR |
| "classify this event" | Job 2 classification draft |
| "is this an SAE" | Same |
| "what recall class is this" | Same |

### regulatory-manager

| Phrase pattern | Notes |
|---|---|
| "any registrations renewing" | Job 3 registrations tracker |
| "what's the [SKU] MoCRA listing status" | Same |
| "MoCRA facility registration on [vendor]" | Same |
| "CA Prop 65 on [SKU]" | Same |
| "CA Fragrance and Flavor Right to Know on [SKU]" | Same |
| "CA Toxic-Free Cosmetics Act compliance" | Same |
| "WA Toxic-Free Cosmetics Act compliance" | Same |
| "Leaping Bunny renewal" / "Leaping Bunny status" | Same |
| "any state filings overdue" | Same |
| "CA SB 343 Pantone audit" / "SB 343 status" / "where are we on the Pantone sweep" | State packaging laws — registrations tracker |
| "19-state packaging toxics cert" / "where are the supplier toxics certs" | Same |
| "EPR threshold" / "EPR status" / "are we under the EPR threshold" / "EPR registration" | Same (monitoring item under threshold; activates when 80% of $5M global / $1M CA in-state) |
| "Canada compliance status" / "Canada extended-allergens" / "Health Canada notification on [SKU]" / "where are we with Ecomundo" | International markets — registrations tracker + RP partner liaison |
| "Quebec compliance" / "Quebec French-language portfolio sweep" | Same (cross-flags to claims-il-and-label-keeper §6 Pass 4) |
| "UK regulatory" / "South Africa regulatory" | International markets — capacity-planning-only until activated |
| "what's pending with Ecomundo" / "any overdue Ecomundo items" / "RP partner [country]" | Pedrero liaison surface — RP partner section |
| "Pedrero capacity planning" / "send the PD roadmap to Pedrero" | Pedrero liaison surface — annual capacity planning |
| "next attestation due" | Job 4 attestation cadence dashboard |
| "any attestations renewing" | Same |
| "[Sephora/Ulta/Whole Foods/Credo] attestation status" | Same |
| "what's pending with Pedrero" | Job 5 Pedrero liaison |
| "what's been sent to Pedrero" | Same |
| "any overdue Pedrero items" | Same |
| "Pedrero engagement renewal" | Same |
| "Pedrero scope change" | Same |
| "Pedrero contact info" | Same |
| "any reg flags waiting" | Job 1 fan-out queue |
| "route this flag to [skill]" | Same |
| "run the license audit" | Job 7 post-build license audit |
| "what registrations are we missing" | Same |

### regulatory-status-reporter

| Phrase pattern | Notes |
|---|---|
| "regenerate regulatory dashboard" | Job 1 live dashboard refresh |
| "rebuild the regulatory dashboard" | Same |
| "push the regulatory dashboard" | Same |
| "publish the regulatory dashboard" | Same |
| "monthly regulatory snapshot" | Job 2 month-end archive |
| "snapshot the regulatory dashboard" | Same |
| "create monthly regulatory archive" | Same |
| "branded regulatory update for [audience]" | Job 1 with brand styling |
| "regulatory update for the team" | Job 3 read-only summary (or Job 1 if regenerate intent) |

## Cross-skill or ambiguous — to regulatory-manager

Always to regulatory-manager. The router never aggregates.

- "what's open in regulatory"
- "regulatory status"
- "monthly regulatory summary"
- "where are we on regulatory"
- "any regulatory concerns"
- "give me the regulatory rollup"
- "regulatory dashboard now" (read-only summary path; "regenerate" goes to regulatory-status-reporter)
- "monthly regulatory update for Ayesha" (read-only summary that the briefing can pull from)

## Boundary phrases — out of System C

Listed for clarity so the router knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "PD work" / formula / signed approval / branded PD update | sjs-pd-system | PD scope |
| "place a PO" / vendor performance / inventory / S&OP / shipping | sjs-ops-system | Ops scope |
| "open a CAPA" / "open an NCR" / "log this OOS" / "log this complaint" / "trigger SAE protocol" / "branded quality update" | sjs-quality-system | Quality scope (Quality cross-flags Reg via `[Reg Flag Pending — regulatory-manager]`; that lands at regulatory-manager Job 1, not here directly) |
| "leadership dashboard" / cross-system dashboard | future leadership-dashboard | Cross-system aggregator |
| "branded regulatory update for [external audience]" | regulatory-status-reporter (with sweet-july-skin-brand applied) | Renderer + brand styling |

When a peer system isn't live, the router stages a graceful fallback: tells the operator the query needs that system, suggests a workaround, doesn't fake the routing.

## Edge cases the router should handle

| Pattern | Behavior |
|---|---|
| "is this an SAE — should we file" | Fan-out path: classification draft is adverse-event-and-recall-reporter Job 2; binding call is Pedrero. Router forwards to v6.2; v6.2 walks the criteria and stages to Pedrero. |
| "we got the IL approval but Formula Tracker stage hadn't moved" | claims-il-and-label-keeper Job 3 pause case. Router forwards; v6.1 surfaces the bookkeeping mismatch to Operator. |
| "Pedrero verbally said we don't need to file the SAE" | adverse-event-and-recall-reporter Job 5 §5.2 no-verbal-only-opinions rule. Router forwards; v6.2 stages written confirmation send. |
| "skip the Pedrero review on this — it's a tiny tweak" | Decline at any sub-skill. Every Pedrero touch goes through Reg Lead approval. |
| "the recall might affect more batches than originally scoped" | adverse-event-and-recall-reporter handles Linked Batch field update + recall report re-stage. Router forwards. |
| "CA Toxic-Free Cosmetics Act vs CA AB-2762" | Same statute (AB-2762 is the bill number for CA Toxic-Free Cosmetics Act). Router treats as the same registration; regulatory-manager's `Registration Type` enum has the canonical name. |
| "WA Toxic-Free Cosmetics Act vs CA Toxic-Free Cosmetics Act" | Distinct statutes (WA SB-5703 vs CA AB-2762) with different ban lists. Router forwards both to regulatory-manager as separate Registration Type values. |
| "request crosses Quality + Reg + PD" | Surface to operator. Router can stage handoff to multiple system routers but the chain belongs to sjs-master. |
