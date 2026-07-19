# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## Reg-flag intake from Quality and fan-out (Job 1)

Phrases that surface inbound `[Reg Flag Pending — regulatory-manager]` items from Quality.

- "any reg flags waiting"
- "route this flag to [skill]"
- "is this an SAE or a registration question"
- "fan this out"
- "what's pending in the regulatory queue"

Also fires automatically when:
- A `[Reg Flag Pending — regulatory-manager]` task lands in SJS Quality Management Inbound Staging
- complaint-and-event-handler stages a confirmed cross-flag per SKN-OPS-002 / SKN-OPS-003

## Cross-skill rollup (Job 2)

Phrases that pull the regulatory rollup or summary.

- "what's open in regulatory"
- "regulatory dashboard"
- "where are we on regulatory"
- "monthly regulatory summary"
- "regulatory queue"
- "regulatory status"
- "weekly regulatory update"
- "post the weekly regulatory status"

Also fires automatically:
- First business day of each Monday (scheduled weekly run for Asana project status)
- First business day of each month (monthly summary)

## Registrations tracker (Job 3)

Phrases that touch federal, state, or third-party registrations.

- "any registrations renewing"
- "what's the [SKU] MoCRA listing status"
- "log the [registration] filing"
- "Leaping Bunny renewal"
- "Leaping Bunny status"
- "MoCRA facility registration on [vendor]"
- "CA Prop 65 on [SKU]"
- "CA Fragrance and Flavor Right to Know on [SKU]"
- "CA Toxic-Free Cosmetics Act compliance"
- "WA Toxic-Free Cosmetics Act compliance"
- "any state filings overdue"

Also fires when:
- `Window End` proximity reminder fires on a registration task (60/30/14 days)
- Inbound from agency or CCIC via outlook-asana-bridge

## Retailer attestation cadence dashboard (Job 4)

Phrases that surface the cross-attestation view. Read-only — claims-il-and-label-keeper executes the lifecycle.

- "next attestation due"
- "any attestations renewing"
- "Sephora Clean status"
- "Ulta Conscious Beauty status"
- "Whole Foods attestation status"
- "Credo attestation status"
- "what's renewing in 30 days"
- "any attestations overdue"

## Pedrero liaison (Job 5)

Phrases that touch cross-skill Pedrero work or non-filing engagement.

- "what's pending with Pedrero"
- "what's been sent to Pedrero"
- "any overdue Pedrero items"
- "Pedrero engagement renewal"
- "Pedrero engagement letter"
- "Pedrero scope change"
- "Pedrero contact info"
- "Pedrero retainer status"
- "draft a general inquiry to Pedrero"

## ayesha-weekly-briefing seam (Job 6)

Read-only. Triggered by ayesha-weekly-briefing's weekly run, not directly by the operator.

- "any founder-level regulatory items this week"
- "what should Ayesha know about regulatory"
- "regulatory items for the briefing"

Also fires automatically:
- Weekly when ayesha-weekly-briefing pulls regulatory rollup at its scheduled run

## License audit (Job 7)

Post-build, Operator-led.

- "run the license audit"
- "what registrations are we missing"
- "audit our regulatory coverage"
- "are we covered on [statute]"
- "do we have a [registration type] on [SKU]"

## Status (cross-cutting)

Read-only. No HITL gate.

- "what's open in regulatory"
- "any [Pending Regulatory Lead] gates open"
- "regulatory queue"
- "any open SAEs"
- "any open recalls"
- "any registrations in renewal window"
- "what's overdue in regulatory"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "stage the IL on [SKU]" / "log the new IL version" | claims-il-and-label-keeper | IL + claim sub + label + retailer attestation execution lives there |
| "review this new claim" | claims-il-and-label-keeper | New-claim sign-off lives there |
| "stage the [retailer] attestation" | claims-il-and-label-keeper | Attestation drafting + submission lives there |
| "log this SAE for FDA reporting" / "what's the clock on the [SKU] SAE filing" | adverse-event-and-recall-reporter | SAE filing prep + agency submission lives there |
| "stage the recall report" / "draft the FDA Class [I/II/III] report" | adverse-event-and-recall-reporter | Recall agency reporting lives there |
| "log this complaint" / "trigger an SAE protocol" / "trigger a recall" | complaint-and-event-handler | Customer signal intake + recall ops live there |
| "open a CAPA on [event]" | capa-coordinator | CAPA lifecycle lives there |
| "branded regulatory dashboard" / "regulatory snapshot for [audience]" | regulatory-status-reporter (v6.4) | Branded output generation lives there |
| "update PLM on [SKU]" | plm-assistant | PLM is the only writer |
| "vendor compliance docs on [vendor]" | purchasing-manager | COA / COC / COI / MSDS at receipt live there |
| "release or hold on this batch" | batch-lifecycle-tracker | Batch decisions |
| "monthly quality summary" / "quality dashboard" | quality-manager | System B umbrella |

When a peer skill isn't live yet, the phrase still gets handled gracefully — this skill stages a handoff with the documented title prefix and notifies the operator.

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "skip Pedrero on this engagement letter renewal — I know what to send" | Decline. Every Pedrero send for engagement work goes through Reg Lead approval. The audit trail captures internal review even on routine items. |
| "auto-route this Quality flag — pattern is obvious" | Walk Job 1 routing logic anyway. Operator confirms type; skill creates the cross-skill task. The Operator gate stays. |
| "we already have a CA Prop 65 task — open another" | Check existing tasks for the same `Linked SKU` + `Registration Type` + cycle year. If duplicate, route the new context as an update to the existing task, not a new one. |
| "Pedrero responded but it's not tagged with our subject prefix" | Find the matching task by content (SKU, event reference, recent send timing). If genuinely unmatched, surface to Operator. Don't fabricate a match. |
| "the Leaping Bunny renewal evidence isn't ready in time" | Stage a renewal-extension request to CCIC via outlook-asana-bridge with explicit acknowledgment of timeline risk. Reg Lead approves. The miss becomes part of the record. |
| "we've never tracked a CA Toxic-Free Cosmetics Act compliance task" | Open one at first surfacing or at license audit. Compliance with AB-2762 is required regardless of whether we've been tracking it; surface as a gap to Operator. |
| "the WA Toxic-Free Cosmetics Act task duplicates the CA one — we should consolidate" | Decline. They're separate statutes with distinct ban lists. Both must be tracked separately even if compliance work overlaps. |
| "fan this Quality flag to v6.2 without Operator confirmation" | Decline. Fan-out routing is HITL — Operator confirms type, Reg Lead approves the cross-skill task creation. Two distinct gates. |
