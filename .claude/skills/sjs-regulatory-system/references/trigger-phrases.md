# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file expands by intent for browsability. The router fires when any of these patterns hit; routing-table.md says where the request goes.

## IL / Claim / Label work (claims-il-and-label-keeper)

- "stage the IL on [SKU]"
- "log the new IL version on [SKU]"
- "what IL is on the latest [SKU] batch"
- "is there a current IL on [SKU]"
- "review this new claim on [SKU]"
- "is this claim defensible"
- "Pedrero sign-off needed on [claim]"
- "stage the [retailer] attestation for [SKU]"
- "renew the Sephora Clean attestation on [SKU]"
- "draft the Ulta Conscious Beauty response for [SKU]"
- "fill out the Whole Foods questionnaire for [SKU]"
- "Credo attestation due on [SKU]"
- "log the new label artwork on [SKU]"
- "did Pedrero sign off on the new [SKU] label"
- "archive the [SKU] [carton/component] artwork"
- "what claims do we have on [SKU]"

## SAE / Recall / State AE (adverse-event-and-recall-reporter)

- "log this SAE for FDA reporting"
- "what's the clock on [SKU] SAE filing"
- "stage the recall report for Pedrero"
- "draft the FDA Class [I/II/III] report"
- "submit the [SKU] SAE to FDA"
- "file the recall report"
- "any open SAEs at FDA"
- "any open recalls"
- "did we close the [batch] recall agency-side"
- "log the agency acknowledgment on [event]"
- "draft the agency follow-up reply"
- "state AE filing on [SKU]"
- "classify this event"
- "is this an SAE"
- "what recall class is this"

## Registrations / Pedrero liaison / cross-skill rollup (regulatory-manager)

### Registrations
- "any registrations renewing"
- "what's the [SKU] MoCRA listing status"
- "MoCRA facility registration on [vendor]"
- "CA Prop 65 on [SKU]"
- "CA Fragrance and Flavor Right to Know on [SKU]"
- "CA Toxic-Free Cosmetics Act compliance"
- "WA Toxic-Free Cosmetics Act compliance"
- "Leaping Bunny renewal" / "Leaping Bunny status"
- "any state filings overdue"

### Retailer attestation cadence (cross-attestation view; lifecycle execution lives in claims-il-and-label-keeper)
- "next attestation due"
- "any attestations renewing"
- "[Sephora/Ulta/Whole Foods/Credo] attestation status"
- "what's renewing in 30 days"

### Pedrero liaison
- "what's pending with Pedrero"
- "what's been sent to Pedrero"
- "any overdue Pedrero items"
- "Pedrero engagement renewal"
- "Pedrero engagement letter"
- "Pedrero scope change"
- "Pedrero contact info"
- "Pedrero retainer status"
- "draft a general inquiry to Pedrero"

### Fan-out from Quality
- "any reg flags waiting"
- "route this flag to [skill]"
- "fan this out"

### License audit (post-build)
- "run the license audit"
- "what registrations are we missing"
- "audit our regulatory coverage"
- "are we covered on [statute]"

## Branded dashboard / snapshot (regulatory-status-reporter)

- "regenerate regulatory dashboard"
- "rebuild the regulatory dashboard"
- "push the regulatory dashboard"
- "publish the regulatory dashboard"
- "monthly regulatory snapshot"
- "snapshot the regulatory dashboard"
- "create monthly regulatory archive"
- "branded regulatory update for [audience]"
- "regulatory update for the team"

## Cross-skill / ambiguous — to regulatory-manager

Read-only. No HITL gate.

- "what's open in regulatory"
- "regulatory status"
- "monthly regulatory summary"
- "where are we on regulatory"
- "any regulatory concerns"
- "give me the regulatory rollup"
- "regulatory dashboard now"
- "any [Pending Regulatory Lead] gates open"

## Boundary — out of System C

| Phrase pattern | Routes to |
|---|---|
| "PD work" / formula / signed approval / branded PD update | sjs-pd-system |
| "place a PO" / vendor performance / inventory / S&OP / shipping | sjs-ops-system |
| "open a CAPA" / "open an NCR" / "log this OOS" / "log this complaint" / "trigger SAE protocol" / "branded quality update" | sjs-quality-system |
| "leadership dashboard" / cross-system dashboard | future leadership-dashboard |
