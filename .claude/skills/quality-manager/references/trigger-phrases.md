# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## SOP catalog queries (Job 1)

Read-only. No HITL gate.

- "current revision of SKN-OPS-XXX"
- "what's the latest on SKN-OPS-XXX"
- "is [procedure] ratified"
- "what SOPs are pending ratification"
- "any SOPs due for review"
- "any SOPs due for review in next [N] days"
- "show the SOP catalog"
- "SOP catalog"

## SOP ratification queue (Job 1b)

- "ratify [procedure name]"
- "ratify SKN-OPS-005" (NCR Procedure currently pending)
- "approve the [procedure] draft"
- "what's in the ratification queue"
- "any [SOP Revision Pending] tasks"

Also fires automatically when:
- A `[SOP Revision Pending — quality-manager]` task lands in SJS Quality Management Inbound Staging from any sub-skill.

## Cross-skill state rollup — dashboard (Job 2)

Read-only.

- "what's open in quality"
- "quality dashboard"
- "monthly quality summary"
- "where are we on quality"
- "quality status"
- "give me the quality rollup"
- "catch me up on quality"

Also fires automatically:
- Weekly Monday 9am PT scheduled run (via the `schedule` skill) — posts as Asana project status update on SJS Quality Management.

## Quality-of-service aggregation (Job 3)

Read mostly; threshold-crossing fires task creation.

- "shipping quality this week"
- "QoS rollup"
- "what's the fulfillment quality"
- "any QoS threshold crossings"
- "current QoS metrics"
- "on-time rate this week"

Also fires automatically:
- During weekly rollup (Job 2 fires QoS as a sub-step).
- Threshold detection during rollup auto-stages `[QoS Threshold Crossed]` task per Job 4.

## Cross-cutting task creation (Job 4)

- "audit prep for [retailer]"
- "retailer questionnaire from [retailer]"
- "regulatory inspection prep for [authority]"
- "quality system review"
- "open a cross-cutting task for [topic]"
- "stage a [type] task" (where type is one of the six cross-cutting types)

Also fires automatically:
- SOP annual reviews on Next Review Due dates from catalog.
- Quarterly Q1/Q2/Q3/Q4 quality system reviews on first business day of each quarter.
- Outlook calendar inbound for retailer audits (via outlook-asana-bridge).
- Outlook email inbound from retailer flagged as questionnaire (via outlook-asana-bridge).
- Regulatory inspection notices from regulatory-manager (System C, live).

## SOP annual review (Job 5)

- "SOP annual review for SKN-OPS-XXX"
- "review SKN-OPS-XXX"
- "any SOPs due for annual review"
- "review the [procedure name]"

Also fires automatically on Next Review Due date from catalog.

## Status (cross-cutting)

Read-only.

- "what cross-cutting tasks are open"
- "any [Pending QA Lead] gates open in quality-manager"
- "audit prep status"
- "regulatory inspection status"
- "QoS task queue"
- "ratification queue status"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "open a CAPA on [issue]" | capa-coordinator | CAPA + NCR lifecycle owns there. Cross-cutting tasks can hand off there but never duplicate. |
| "log this complaint" | complaint-and-event-handler | Customer signal intake. |
| "log this OOS" / "OOT on [batch]" | quality-lab-coordinator | Lab classification. |
| "release / hold on [batch]" | batch-lifecycle-tracker | Batch state. |
| "schedule the PET test" | batch-lifecycle-tracker | Stability schedule. |
| "log this late shipment" / "OC3PL daily report" | oc3pl-order-manager | Fulfillment workflow. |
| "place a PO" / "vendor scorecard" | purchasing-manager | Purchase-to-pay. |
| "is this reportable to FDA / MoCRA" / "MoCRA registration" / "Leaping Bunny" / "Prop 65" / "stage the IL on [SKU]" / "stage the [retailer] attestation" | sjs-regulatory-system | System C (live) — reportability, registrations, IL/claim/label, retailer attestations. |
| "branded quality report" / "quality report for Ayesha" | quality-status-reporter (v5.6) | Output generation. |
| "update PLM on [batch / vendor / SKU]" | plm-assistant | PLM is the only writer. |

When a peer skill isn't live yet, the phrase still gets handled gracefully — quality-manager stages a handoff with the documented title prefix and notifies the operator.

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "create a CAPA from this rollup" | Decline. CAPAs open in capa-coordinator. quality-manager can stage a `[CAPA Pending]` handoff to SJS CAPA Log if a sustained QoS pattern warrants root cause work, but the CAPA itself opens there. |
| "ratify [draft] without QA Lead approval" | Decline. SOP ratification is a QA Lead gate. If the QA Lead role-holder needs to change, update `references/role-map.md`. |
| "skip the cross-cutting task QA Lead approval — it's just an audit prep" | Decline. Every cross-cutting task creation is a QA Lead gate. |
| "open an SOP catalog query that ignores pending ratification status" | Pause. Pending ratification is material to the answer. If the query is about historical state, surface that the SOP is currently pending and offer the working draft path instead. |
| "set a custom threshold for [metric]" | Pause. QoS thresholds are defined in `references/qos-thresholds.md`. Threshold changes require QA Lead approval and update both the reference file and any pending QoS tasks. |
| "tell me current QoS rate without checking sources" | Decline. QoS rollup must read the latest data from oc3pl-order-manager + complaint-and-event-handler. Cached values are stale; always pull fresh. |
| "draft SOP from scratch" | Decline. Sub-skills draft procedures; quality-manager owns the ratification cycle. If a procedure is needed for a new domain, the sub-skill that owns the domain drafts it (e.g., a future packaging-quality skill drafts its own procedure). |
