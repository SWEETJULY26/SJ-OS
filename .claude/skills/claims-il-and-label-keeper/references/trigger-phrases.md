# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## IL review gate intake (Job 1)

Phrases that surface a new IL packet for Pedrero staging.

- "stage the IL on [SKU]"
- "log the new IL version on [SKU]"
- "open an IL review on [SKU]"
- "the [SKU] formula was approved — fire the IL gate"
- "what IL is on the latest [SKU] batch"
- "is there a current IL on [SKU]"

Also fires automatically when:
- A Formula Tracker task in asana-pd-manager flips `IL Status = Pending IL Review` (which fires when Stage moves to Signed Approvals)
- A reformulation event flips `IL Status = IL Reformulated — Re-review Required` on a Formula Tracker task

## Pedrero send (Job 2)

Phrases that stage an Outlook draft to Pedrero. Read-only on the trigger — the send happens on Reg Lead approval after Operator approval of the artifact draft.

- "send the IL on [SKU] to Pedrero"
- "stage the [retailer] attestation for Pedrero"
- "send the new claim on [SKU] to Pedrero"
- "stage the label cross-check for Pedrero"
- "any sends pending Reg Lead"

Also fires automatically at end of Job 1, Job 4 (when label needs reg sign-off), Job 5, Job 6 (attestation pre-submission).

## Pedrero return processing (Job 3)

Phrases that classify a Pedrero reply.

- "Pedrero responded on [SKU]"
- "log Pedrero's IL approval on [SKU]"
- "Pedrero kicked back the [SKU] [artifact]"
- "process the [SKU] Pedrero return"
- "any Pedrero replies waiting"

Also fires automatically when outlook-asana-bridge surfaces a Pedrero reply on a `[*Review*]`-tagged thread.

## Label artwork cross-check + archive (Job 4)

Phrases that trigger an IL match check on incoming artwork.

- "log the new label artwork on [SKU]"
- "did Pedrero sign off on the new [SKU] label"
- "archive the [SKU] [carton/component] artwork"
- "cross-check the [SKU] artwork against current IL"
- "what label version is on [SKU]"

Also fires when:
- outlook-asana-bridge surfaces inbound from a PD designer with artwork attached
- A new label artwork file is dropped into the SharePoint regulatory folder (post-v6.3)

## New-claim sign-off (Job 5)

Phrases that surface a new claim before it ships.

- "review this new claim on [SKU]"
- "is this claim defensible"
- "Pedrero sign-off needed on [claim]"
- "can we say [claim] on [SKU]"
- "new marketing claim on [SKU]"
- "founder wants to add [claim] to packaging"

Also fires when:
- Marketing or PD inbound via outlook-asana-bridge or fireflies-asana-bridge with a new-claim ask

## Retailer attestation response (Job 6)

Phrases that stage an attestation draft.

- "stage the [retailer] attestation for [SKU]"
- "renew the Sephora Clean attestation on [SKU]"
- "draft the Ulta Conscious Beauty response for [SKU]"
- "fill out the Whole Foods questionnaire for [SKU]"
- "Credo attestation due on [SKU]"
- "any attestations pending"

Also fires when:
- A retailer questionnaire arrives via outlook-asana-bridge
- A `Window End` proximity reminder fires on an existing attestation task (60/30/14 days)

## Closeout, renewal tracking (Job 7)

Phrases that close terminal artifacts or fire renewals.

- "close out the [SKU] IL approval"
- "close this attestation"
- "any renewals coming up"
- "what's renewing in the next 30 days"
- "log the [SKU] [retailer] submission"

Also fires automatically:
- On Pedrero approval landing (Job 3 outcome = Approved)
- Scheduled fire at 60/30/14-day proximity to `Window End`
- First business day of each month (renewal sweep)

## Status (cross-cutting)

Read-only. No HITL gate.

- "what's open in regulatory"
- "what's pending with Pedrero"
- "any IL reviews waiting"
- "any returned items needing action"
- "what attestations are active"
- "what claims do we have on [SKU]"
- "what's the current IL version on [SKU]"
- "what label artwork is archived for [SKU]"
- "any [Pending Regulatory Lead] gates open"
- "regulatory queue"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "is this reportable to FDA" | regulatory-manager (v6.3) for routing → adverse-event-and-recall-reporter (v6.2) for the actual filing | Reportability classification + filing live there |
| "log this SAE" / "trigger an SAE filing" | adverse-event-and-recall-reporter (v6.2) | SAE owns there. Pre-v6.2, route via complaint-and-event-handler's existing flag prefix |
| "trigger a recall" | complaint-and-event-handler runs ops; adverse-event-and-recall-reporter (v6.2) handles agency side | Recall has an explicit kickoff phrase |
| "log this complaint" | complaint-and-event-handler | Customer signal intake |
| "open a CAPA on this label issue" | capa-coordinator | CAPA opening lives there. claims-il-and-label-keeper can stage NCR intake context but capa-coordinator opens. |
| "MoCRA registration on [SKU]" | regulatory-manager (v6.3) | Registrations + state filings live there. Pre-v6.3, stage as `[Reg Flag Pending — regulatory-manager]` comment on this skill's task |
| "Prop 65 on [ingredient]" | regulatory-manager (v6.3) | State filings owner |
| "vendor compliance docs on [vendor]" | purchasing-manager | COA / COC / COI / MSDS at receipt live there |
| "place a PO" / "PO status" | purchasing-manager | Purchase-to-pay |
| "release or hold on this batch" | batch-lifecycle-tracker | Batch decisions |
| "release the next batch with new IL" | batch-lifecycle-tracker (batch decision) ↔ this skill (IL version archive) — both involved | Batch picks up the IL version from this skill but the hold/release decision lives there |
| "branded regulatory dashboard" | regulatory-status-reporter (v6.4) | Output generation |
| "update PLM on [SKU]" | plm-assistant | PLM is the only writer |
| "draft formula evidence for [claim]" | asana-pd-manager | Pre-launch claim evidence generation lives in PD |

When a peer skill isn't live yet, the phrase still gets handled gracefully — claims-il-and-label-keeper stages a handoff with the documented title prefix and notifies the operator.

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "skip the Pedrero review on this IL — it's a tiny tweak" | Decline. Every IL change goes through Pedrero per the procedure. The skill has no judgment on what's a tiny tweak; that's exactly the call Pedrero is paid to make. |
| "send the attestation directly to Sephora — skip Pedrero" | Decline. Every retailer-facing submission requires Pedrero pre-flight per the procedure. |
| "approve this claim — Pedrero already verbally OK'd it on the call" | Pause. Verbal approval doesn't archive. Stage the claim to Pedrero with subject `[Claim Sign-Off — confirming verbal OK on call]` and ask for written confirmation. |
| "the Sephora deadline is tomorrow — skip Reg Lead approval" | Decline at v6.1. The Reg Lead gate is the audit-trail mechanism. If urgency is real, the Reg Lead can approve in 60 seconds; the gate stays. |
| "the printer already printed with the wrong IL — just archive it" | Pause. Archive captures truth, but a print-with-wrong-IL is a live regulatory issue that stages a separate Pedrero send + likely a label correction sticker plan. The archive entry references the issue task. |
| "we never had a claim sub file for [SKU] but it's been on shelves for 6 months" | Pause. Stage the retroactive sub work: pull every claim from current packaging, build the sub file, stage to Pedrero for retroactive sign-off. Surface to Operator that we've been operating without sub coverage. |
| "the IL on the carton matches but the IL on the inner component doesn't" | Treat as drift. Archive the matching artwork, flag the mismatched one, route to Job 2 for Pedrero call (likely a printer-side error). |
| "Pedrero replied on the wrong thread / out of band" | Find the matching task, log the reply as a comment manually, and update the field state. Surface to Operator that the bridge missed it (auto-tagging may need a tweak). |
| "two new claims at once on the same SKU" | One task per claim per SKU. Don't bundle — claim sub evidence is per-claim, and Pedrero replies are per-claim. |
| "we got the IL approval but the formula tracker stage hadn't moved to Signed Approvals" | Pause. Don't write the IL Approved state until the upstream Formula Tracker stage matches. Surface to Operator — likely a Formula Tracker bookkeeping miss. |
