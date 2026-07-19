# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## Lab finding intake (Job 1)

Phrases that surface a new OOS, OOT, or in-spec flag.

- "log this OOS"
- "log this OOT"
- "got an OOS on [batch / SKU]"
- "got an OOT on [batch / SKU]"
- "PET test failed on [batch]"
- "stability fail on [batch]"
- "lab result came back on [batch]"
- "open a lab finding on [batch / SKU]"
- "log this lab result"

Also fires automatically when:
- A PLM lab issue arrives via plm-assistant with a fail / OOS / OOT classification
- `outlook-asana-bridge` flags an inbound from a contract lab matching a lab-finding pattern
- `fireflies-asana-bridge` flags a lab finding signal in QBR / consultation calls

## Incoming material defect (Job 2)

Phrases that surface a vendor receipt failure.

- "incoming material defect on [batch / vendor]"
- "[vendor] shipment failed receiving inspection"
- "COA mismatch on [batch]"
- "COA missing on [batch]"
- "did the latest [vendor] shipment pass"
- "rejected the receipt on [PO / batch]"
- "packaging damage on [vendor] shipment"

Also fires when purchasing-manager surfaces a receipt-failure signal that needs lab-side classification.

## Pattern analysis (Job 3)

Phrases that pull the lab pattern read.

- "lab patterns by vendor"
- "any patterns in lab"
- "any patterns this month"
- "monthly lab sweep"
- "show me OOS by [vendor / SKU]"
- "show me OOT by [vendor / SKU]"
- "lab finding history for [vendor]"
- "anything trending in lab"

Also fires automatically:
- First business day of each month (scheduled monthly run)
- Every new LF (auto-fires a quick pattern check against same vendor / SKU / spec)

## Vendor flag — escalation decision (Job 4)

Phrases that walk the vendor flag review.

- "flag the vendor on this"
- "vendor scorecard hit on [vendor]"
- "open a vendor flag on [vendor]"
- "should we flag [vendor]"
- "any vendor flags pending review"
- "review the [vendor] flag"

## Vendor scorecard signal — comment-back (Job 5)

Read-only on triggers — the post happens on QA Lead approval of a vendor flag (Job 4 → Job 5 pipeline).

- "post the scorecard signal on [vendor]"
- "send the scorecard hit to purchasing"
- "any scorecard signals pending"
- "did the [vendor] signal go out"

## CAPA handoff (Job 5b)

Phrases that hand a lab finding to capa-coordinator for root cause work.

- "open a CAPA on this lab finding"
- "open a CAPA on LF-YYYY-NNN"
- "hand this off to capa"
- "this needs root cause"

The handoff also fires automatically when Job 4 decision = flag for CAPA.

## Closeout (Job 6)

Phrases that close a lab finding and post close-the-loop.

- "close out LF-YYYY-NNN"
- "close this lab finding"
- "any lab findings ready to close"
- "[CAPA-YYYY-NNN closed — close the lab finding]" (auto from capa-coordinator on CAPA close)

## Status (cross-cutting)

Read-only. No HITL gate.

- "what's open in lab quality"
- "lab queue"
- "any open OOS"
- "any open OOT"
- "any lab findings on watch list"
- "any vendor flags pending QA Lead"
- "lab quality status"
- "any overdue lab findings"
- "any [Pending QA Lead] gates open in lab"
- "any open lab findings on [vendor]"
- "any open lab findings on [SKU]"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "open an NCR on [issue]" | capa-coordinator | NCR + CAPA lifecycle owns there. Quality-lab can stage the intake context but capa-coordinator opens. |
| "open a CAPA on [batch]" | capa-coordinator | Same — CAPA opening lives there. |
| "log this complaint" | complaint-and-event-handler | Customer signal intake |
| "release or hold on this batch" | batch-lifecycle-tracker (v5.4) | Batch decisions |
| "schedule a stability check" | batch-lifecycle-tracker (v5.4) | In-market stability |
| "update the [vendor] scorecard" | purchasing-manager | Scorecard records live there. Quality-lab signals via comment, doesn't write. |
| "place a PO" / "PO status" / "vendor onboarding" | purchasing-manager | Purchase-to-pay |
| "is this reportable to [authority]" | regulatory-manager (v6) | Reportability assessment |
| "shipping quality this week" | quality-manager (v5.5) | QoS dashboard |
| "branded quality dashboard" | quality-status-reporter (v5.6) | Output generation |
| "update PLM on [batch / vendor / SKU]" | plm-assistant | PLM is the only writer |

When a peer skill isn't live yet, the phrase still gets handled gracefully — quality-lab-coordinator stages a handoff with the documented title prefix and notifies the operator.

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "skip the QA Lead approval — flag the vendor anyway" | Decline at v5.3. The QA Lead gate on vendor flags is the audit-trail mechanism; collapsing it loses what makes the scorecard signal defensible. If the QA Lead role-holder needs to change, update the role map. |
| "this OOS is fine — close it without retest or CAPA" | Pause. OOS by definition fails spec; close path requires either retest, watch list with rationale, or CAPA handoff. Operator can choose any of those, but plain close is not an option. |
| "auto-flag the vendor — pattern is obvious" | Walk Job 4 §4.3 review checklist anyway. Skill stages the decision; QA Lead still approves. |
| "open a lab finding without a batch" | Pause. LF requires batch or component lot for retention and audit-trail purposes. If truly batch-less (vendor-systemic across batches), use the Pattern classification path. |
| "we already had a CAPA on this — open another" | Check `Linked CAPA` on recent LFs. If the same root cause shows up, route the new LF as an effectiveness-failure signal to the existing CAPA rather than opening a new one. |
| "the contract lab made a mistake — toss this result" | Decline outright. Lab-error signal goes through the retest path (§5) so the trail captures both the original result and the retest. Tossing destroys the audit trail. |
