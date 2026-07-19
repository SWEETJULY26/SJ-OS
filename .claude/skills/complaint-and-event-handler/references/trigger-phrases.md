# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## Intake (Job 1)

Phrases that surface a new complaint or push one into the log.

- "log this complaint"
- "new complaint on the [SKU]"
- "complaint just came in"
- "add this to the complaint log"
- "customer just emailed about [issue]"
- "got a complaint from [channel]"
- "[customer name] reached out about [issue]"

Also fires automatically when:
- A new submission lands in the `New feedback` section of the SJ Skin Complaint Log (via Asana watch).
- `outlook-asana-bridge` flags an inbound that matches the complaint pattern (subject lines, sender domain heuristics).
- `fireflies-asana-bridge` flags a complaint signal in a retail partner or customer-service call transcript.

## Classification (Job 2)

Phrases that ask the skill to recommend or commit a classification.

- "classify this complaint"
- "what should I do with this one"
- "what's the right action for [task]"
- "is this Skin Reactions or Performance"
- "any unclassified complaints"

## Trend analysis (Job 3)

Read-only. No HITL gate. Fires on:

- "complaint trend this month"
- "complaint rate by SKU"
- "complaints by batch on lot [code]"
- "complaints on the [SKU] this quarter"
- "any spikes in complaints"
- "trend report for [SKU]"
- "show me the [SKU] complaint history"
- "are we seeing a pattern on [batch]"
- "what's the complaint rate on Amazon vs Web Store"

## SAE (Job 4)

SKN-OPS-002 walk. HITL on every triage step.

Direct triggers:
- "trigger SAE protocol"
- "this looks like an adverse event"
- "is this reportable"
- "any open SAEs"
- "open an SAE on [SKU/batch]"
- "walk SKN-OPS-002 on [event]"

Keyword triggers (the skill scans complaint descriptions and surfaces a possible SAE for operator confirmation):
- hospitalization, hospitalized
- ER, emergency room
- anaphylaxis, anaphylactic
- swelling, severe swelling
- blistering, blisters
- scarring
- infection, infected
- "had to see a doctor"
- "sent me to the hospital"
- "couldn't breathe"
- "EpiPen"

Keyword match never auto-opens an SAE — it surfaces the question to the operator.

## Recall (Job 5)

SKN-OPS-003 walk. Strictest gate in the skill.

**Kickoff phrase (required, exact pattern):**
- "trigger a recall on [SKU]"
- "trigger a recall on lot [batch code]"
- "trigger a recall on [SKU] batch [batch code]"
- "initiate recall for [SKU/batch]"

The kickoff phrase must include both the action and the target. Vague references ("we should recall something") do not fire — the skill responds with a request for specifics.

**Soft surfacing (the skill raises the question, operator decides):**
- Trend analysis threshold breach on Skin Reactions
- SAE escalation pointing to a batch defect
- Pattern across multiple batches of the same SKU
- Vendor flag from quality-lab-coordinator (post-v5.3)

In all soft-surfacing cases, the skill phrases it as: "This pattern would warrant considering a recall under SKN-OPS-003. Want to walk it?" Operator decides.

## Status (cross-cutting)

Read-only. No HITL gate. Fires on:

- "what's open in complaints"
- "any unclassified complaints"
- "complaint queue status"
- "what's in the SJ Skin Complaint Log"
- "what's in Actioning right now"
- "any open SAEs" (also Job 4)
- "any open recalls"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "open a CAPA on [issue]" | capa-coordinator (v5.2) | CAPA records and lifecycle |
| "vendor scorecard hit" | quality-lab-coordinator (v5.3) → purchasing-manager | Vendor-side quality |
| "release or hold on this batch" | batch-lifecycle-tracker (v5.4) | Batch decisions |
| "shipping quality this week" | quality-manager (v5.5) | QoS dashboard |
| "is this reportable to FDA / MoCRA" | sjs-regulatory-system → adverse-event-and-recall-reporter | Reportability classification + agency filing per SKN-OPS-009 |
| "branded quality dashboard" | quality-status-reporter (v5.6) | Output generation |

When a peer skill isn't live yet, this skill still picks up the intent so nothing falls on the floor — it stages a handoff and notifies the operator (see SKILL.md Job 6).
