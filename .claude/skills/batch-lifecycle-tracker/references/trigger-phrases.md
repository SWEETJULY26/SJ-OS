# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## Pre-launch → in-market transition (Job 1)

Phrases that surface a SKU's first commercial batch and stage the transition.

- "transition [SKU] to in-market stability"
- "[SKU] is ready to launch — start the lifecycle"
- "start in-market stability for [SKU]"

Also fires automatically when:
- inventory-manager creates a batch with `batch_quantity` over the SKU's sample threshold
- AND asana-pd-manager Formula Development Tracker has the SKU at `Signed Approvals`

## Batch state queries (Job 2)

Read-only. No HITL gate.

- "what's the status on lot [batch_code]"
- "what's the status on batch [batch_code]"
- "any batches active for [SKU]"
- "any batches on hold"
- "any batches in stability"
- "any batches on watch"
- "batch state for [SKU]"
- "lifecycle on [batch_code]"

## Stability scheduling and tracking (Job 3)

Phrases that surface, schedule, or update stability work.

- "schedule the [test] for [batch_code]"
- "schedule PET-EOL for [batch_code]"
- "stability calendar"
- "any stability tests due"
- "stability schedule for [SKU]"
- "log stability result for [batch_code]"
- "PET passed for [batch_code]"
- "skip the [test] on [batch_code]" — Operator approval required
- "shift the [test] date for [batch_code] to [date]" — Operator approval required

Also fires automatically:
- Auto-fire on §5.1 cadence dates (PET-launch at production, PET-EOL at expiration - X months, accelerated at +3 months, real-time annually)
- Dispatch reminder fires 5 business days before due

## Hold and release decisions (Job 4)

Phrases that walk the hold or release decision.

- "hold the [batch_code]"
- "hold lot [batch_code]"
- "hold [batch_code] for [reason]"
- "release the hold on [batch_code]"
- "release [batch_code]"
- "any holds awaiting QA Lead"
- "any releases awaiting QA Lead"
- "review the hold on [batch_code]"
- "draft a release for [batch_code]"

Also fires automatically when:
- quality-lab-coordinator posts `[Batch Hold Request — batch-lifecycle-tracker]` (lab-driven)
- complaint-and-event-handler posts the same intake pattern with `Hold Reason = Complaint trend`
- regulatory-manager (post-v6) posts `[Batch Hold Request — batch-lifecycle-tracker]` for regulatory observations

## Near-expiry quality-side decisions (Job 5)

Phrases that surface the quality call on near-expiry batches.

- "any near-expiry batches"
- "quality call on [batch_code]"
- "what's the call on [batch_code] at 30 days"
- "should we pull [batch_code]"
- "expedite EOL for [batch_code]"

Also fires automatically when:
- inventory-manager Job 6 surfaces 90/60/30-day thresholds (cross-post arrives via multi-home to SJS Quality Management)

## CAPA handoff (Job 6)

Phrases that hand a batch to capa-coordinator for root cause work.

- "open a CAPA on [batch_code]"
- "this needs root cause"
- "hand [batch_code] off to capa"
- "the [SKU] has a pattern — open a CAPA"

Also fires automatically when:
- Job 4 hold decision = route to CAPA
- Repeat OOS or OOT detection on the same SKU + spec within 12 months

## Closeout (Job 7)

Phrases that close a batch lifecycle task.

- "close out [batch_code]"
- "[batch_code] is at EOL — close it"
- "any batches ready to close"

Also fires automatically when:
- Terminal state reached (Released to EOL, Pulled with write-off complete, or Expired)

## Status (cross-cutting)

Read-only. No HITL gate.

- "what's open in batch lifecycle"
- "batch lifecycle queue"
- "any [Pending QA Lead] gates open in lifecycle"
- "any open holds by [SKU]"
- "any batches on watch list"
- "stability calendar this month"
- "transitions pending"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "log this OOS" / "OOT on [batch]" | quality-lab-coordinator | Lab classification owns there. Lab finding can hand off here as `[Batch Hold Request]`. |
| "open a CAPA on [issue]" / "open an NCR" | capa-coordinator | CAPA + NCR lifecycle owns there. |
| "log this complaint" | complaint-and-event-handler | Customer signal intake. Trend signals can hand off here. |
| "receive PO [number]" / "create batch on receipt" | inventory-manager | Batch creation at receipt. |
| "write off [batch]" / "FEFO pull" | inventory-manager | Position-changing PLM writes. |
| "what's the on-hand for [SKU]" | inventory-manager | Quantity queries. |
| "place a PO" / "vendor scorecard" | purchasing-manager | Purchase-to-pay. |
| "is this reportable to [authority]" | regulatory-manager (v6) | Reportability assessment. |
| "branded batch report" | quality-status-reporter (v5.6) | Output generation. |
| "shipping quality this week" | quality-manager (v5.5) | QoS dashboard. |
| "update PLM on [batch / vendor / SKU]" | plm-assistant | PLM is the only writer. |
| "stability test on a pre-launch formula" | asana-pd-manager | Pre-launch stability stays there. |

When a peer skill isn't live yet, the phrase still gets handled gracefully — batch-lifecycle-tracker stages a handoff with the documented title prefix and notifies the operator.

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "release [batch_code] without QA Lead approval" | Decline. The QA Lead gate on releases is the audit-trail mechanism; collapsing it loses what makes the lifecycle defensible. If the QA Lead role-holder needs to change, update the role map. |
| "auto-release the batch — the CAPA closed" | Walk Job 4 §6.3 release review checklist anyway. Skill stages the release; QA Lead still approves. |
| "hold the batch but keep distribution to [retailer]" | Containment scope can be narrow per §6.2 ("specific lane / retailer / channel"). Document the carve-out explicitly in the hold record. |
| "skip stability for this batch" | Decline at v5.4 unless QA Lead approves the skip per `references/batch-lifecycle-procedure.md` §5.2 every-other-batch criteria. |
| "transition [SKU] before Signed Approvals" | Decline. The PD trigger is the audit anchor for why this batch is in-market vs sample. If a manual override is needed, surface to QA Lead first. |
| "open a lifecycle task on a sample batch" | Pause. Lifecycle tasks are for commercial batches. Sample batches stay in PD-side stability tracking. If `batch_quantity` is at the threshold edge (100-500), surface for QA Lead call. |
| "we already pulled this batch — close it" | Confirm via plm-assistant that inventory-manager has the write-off staged or complete. Don't close the lifecycle ahead of the inventory action — leaves position out of sync. |
