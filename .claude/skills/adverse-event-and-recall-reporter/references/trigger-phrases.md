# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## Reg-flag intake from Quality (Job 1)

Phrases that surface inbound `[Reg Flag Pending — regulatory-manager]` items from Quality.

- "any reg flags waiting"
- "log this SAE for FDA reporting"
- "the [SKU] complaint pattern needs a recall report"
- "open a reportable event on [SKU]"
- "what's pending classification"

Also fires automatically when:
- A `[Reg Flag Pending — regulatory-manager]` task lands in SJS Quality Management Inbound Staging
- complaint-and-event-handler stages a confirmed SAE or recall trigger per SKN-OPS-002 / SKN-OPS-003

## Classification draft (Job 2)

Phrases that walk the SAE or recall classification.

- "classify this event"
- "is this an SAE"
- "what recall class is this"
- "walk the MoCRA SAE criteria on [event]"
- "walk the 21 CFR 7 class criteria on [event]"
- "draft the classification on [SKU] [event]"

Also fires automatically when a new task in Inbound Staging has `Event Type = Triage Pending`.

## Packet drafting (Job 3)

Phrases that build the agency packet.

- "draft the SAE packet on [SKU]"
- "build the recall report for [batch]"
- "compose the FDA filing on [event]"
- "draft the state AE on [SKU]"

Also fires automatically when Operator approves classification at Job 2.

## Pedrero send (Job 4)

Phrases that stage the Outlook draft to Pedrero. The send happens on Reg Lead approval.

- "send the [SKU] SAE packet to Pedrero"
- "stage the recall report for Pedrero"
- "send the Class [I/II/III] report to Pedrero"
- "any sends pending Reg Lead"

Also fires automatically at end of Job 3.

## Pedrero return processing (Job 5)

Phrases that classify a Pedrero reply.

- "Pedrero responded on the [SKU] SAE"
- "log Pedrero's recall classification"
- "Pedrero kicked back the [SKU] filing"
- "process the [SKU] Pedrero return"
- "any Pedrero replies waiting"

Also fires automatically when outlook-asana-bridge surfaces a Pedrero reply on a `[*Filing*]`- or `[*Recall*]`-tagged thread.

## Agency submission (Job 6)

Phrases that stage the agency upload. Operator submits manually.

- "submit the [SKU] SAE to FDA"
- "file the recall report"
- "stage the FDA upload on [event]"
- "submit the state AE to [STATE-DOH]"
- "any agency submissions pending Reg Lead"

Also fires automatically when Job 5 outcome = Approved.

## Agency response, statutory clock, closeout (Job 7)

Phrases that track agency response and the statutory clock.

- "any updates from FDA on the [SKU] SAE"
- "what's the clock on the [SKU] SAE filing"
- "any open SAEs at FDA"
- "did we close the [batch] recall agency-side"
- "log the agency acknowledgment on [event]"
- "draft the agency follow-up reply"
- "close the [batch] recall agency-side"

Also fires automatically:
- outlook-asana-bridge surfaces an agency reply
- Statutory clock proximity reminders fire (60% / 80% / 95% MoCRA SAE; hourly past 80% Class I; 50% / 75% / 90% Class III)

## Status (cross-cutting)

Read-only. No HITL gate.

- "what's open in reportable events"
- "any open SAEs"
- "any open recalls"
- "what's the clock on [event]"
- "any [Pending Regulatory Lead] gates open"
- "any agency submissions pending"
- "reportable events queue"
- "any state AE filings open"
- "did Pedrero respond on [event]"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "log this complaint" | complaint-and-event-handler | Customer signal intake lives there |
| "trigger an SAE protocol" / "SAE protocol on [event]" | complaint-and-event-handler runs SAE intake/triage per SKN-OPS-002; this skill picks up after the cross-flag | Intake/triage upstream; agency filing here |
| "trigger a recall" / "initiate recall" | complaint-and-event-handler runs recall ops per SKN-OPS-003; this skill handles agency reporting | Recall ops upstream; agency filing here |
| "open a CAPA on this SAE" | capa-coordinator | CAPA opening lives there. This skill stages NCR intake context post-SAE/recall outcome. |
| "MoCRA registration on [SKU]" | regulatory-manager (v6.3) | Registrations live there. Pre-v6.3, stage as `[Reg Flag Pending — regulatory-manager]` in Quality. |
| "Prop 65 on [ingredient]" | regulatory-manager (v6.3) | State filings owner |
| "stage the IL on [SKU]" / "log the new IL version" | claims-il-and-label-keeper | IL + claim sub + label + retailer attestation lives there |
| "release or hold on this batch" | batch-lifecycle-tracker | Batch decisions. This skill stages a `[Batch Hold Request — batch-lifecycle-tracker]` when a recall affects in-market batches. |
| "vendor compliance docs on [vendor]" | purchasing-manager | COA / COC / COI / MSDS at receipt live there |
| "branded reportable events report" | regulatory-status-reporter (v6.4) | Output generation |
| "update PLM on [event]" | plm-assistant | PLM is the only writer |
| "draft the customer-facing recall communication" | complaint-and-event-handler | Consumer-facing recall execution lives there. This skill is internal/agency-facing. |

When a peer skill isn't live yet, the phrase still gets handled gracefully — this skill stages a handoff with the documented title prefix and notifies the operator.

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "skip the Pedrero review on this SAE — it's clearly minor" | Decline. Every reportable event goes through Pedrero per the procedure. The skill has no judgment on what's clearly minor — that's exactly the binding call Pedrero is paid to make. |
| "submit the SAE directly to FDA — skip Pedrero" | Decline. Every agency submission requires Pedrero pre-flight per the procedure. |
| "the FDA deadline is tomorrow — skip Reg Lead approval" | Decline. The Reg Lead gate is the audit-trail mechanism. If urgency is real, Reg Lead can approve in 60 seconds; the gate stays. |
| "Pedrero said the SAE doesn't need to be filed — close it" | Pause. Pedrero's call is binding, but it must be in writing. Stage written confirmation send: `[CONFIRMING — SAE Classification — SKU-CODE — Pedrero verbal opinion that filing not required]`. Hold the task in Returned — Action Required until written confirmation lands. |
| "auto-classify Class III — pattern is obvious" | Walk the §4 criteria anyway. Skill stages the proposal; Pedrero confirms. |
| "open a reportable event without a complaint linkage" | Pause. Reportable events trace to a source signal (complaint, lab finding, internal observation). If truly no source, capture the originating signal explicitly in `Source Reg Flag` field — but flag to Operator that audit-trail completeness depends on linking back to source. |
| "we missed the 15-day MoCRA SAE clock — how do we proceed" | Don't hide the miss. Stage a late-filing packet to Pedrero with explicit acknowledgment of clock breach, rationale for delay, and recommended remediation per Procedure §11. The miss becomes part of the record. |
| "FDA replied on a thread that doesn't match a known filing" | Find the matching task by Filing Reference or batch context. If genuinely unmatched, stage as a new inbound to Operator. Don't fabricate a match. |
| "two complaints look like the same SAE — combine them" | Pause. Per Procedure §3.2, each consumer event with potentially serious outcome gets its own SAE filing unless Pedrero confirms aggregation criteria are met. Default: separate filings. Operator + Pedrero confirm any combination. |
| "the recall might affect more batches than originally scoped" | Update `Linked Batch` field with all affected batches. Re-stage the recall report to Pedrero with the updated scope (Job 4). Update each affected batch via batch-lifecycle-tracker hold request. |
| "agency requested additional information after submission" | Capture the request on the task. If response requires Pedrero review, restage via Job 4. If routine, Operator drafts and Reg Lead approves the agency reply send. Never bypass the Reg Lead gate on agency-facing replies. |
