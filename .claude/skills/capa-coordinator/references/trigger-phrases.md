# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## NCR intake (Job 1)

Phrases that surface a new non-conformance or push one into the CAPA Log.

- "open an NCR on [issue]"
- "log this OOS as an NCR"
- "log this OOT as an NCR"
- "got a vendor receipt failure on [vendor / lot]"
- "got an audit finding from [retailer / authority]"
- "got a process deviation on [batch / lot]"
- "log this regulatory observation"
- "log this non-conformance"

Also fires automatically when a task lands in SJS CAPA Log Inbound Staging with one of these prefixes:
- `[CAPA Pending — capa-coordinator]` — from complaint-and-event-handler
- ~~`[NCR Request — quality-lab-coordinator]`~~ — retired 2026-05-08 when quality-lab-coordinator v5.3 went live; lab inbound now arrives as direct task creation in SJS CAPA Log Inbound Staging
- `[CAPA Request — batch-lifecycle-tracker]` — from batch lifecycle (pre-v5.4: dropped manually)
- `[CAPA Request — regulatory-manager]` — from regulatory (pre-v6: dropped manually)

Also fires when:
- `outlook-asana-bridge` flags an inbound matching a CAPA pattern (retail partner audit emails, vendor escalations, regulatory observations)
- `fireflies-asana-bridge` flags a CAPA signal in QBR / consultation call transcripts ("Perrine said open a CAPA on…", "Nicole flagged a customer-side issue on…")

## NCR review and decision (Job 2)

Phrases that move an NCR through review.

- "review NCR-YYYY-NNN"
- "any NCRs awaiting review"
- "any open NCRs"
- "convert this NCR to a CAPA"
- "convert NCR-YYYY-NNN to CAPA"
- "close this NCR no CAPA"
- "close NCR-YYYY-NNN — no CAPA needed"
- "hold NCR-YYYY-NNN — need more info"
- "what's the severity on NCR-YYYY-NNN"

## Root cause analysis (Job 3)

Phrases that walk the RCA on an open CAPA.

- "5 Whys on CAPA-YYYY-NNN"
- "Fishbone on CAPA-YYYY-NNN"
- "root cause on [CAPA / issue / batch]"
- "what's the root cause on CAPA-YYYY-NNN"
- "investigation team for CAPA-YYYY-NNN"
- "form the team on CAPA-YYYY-NNN"

## Action plan (Job 4)

Phrases that draft or review the corrective + preventive plans.

- "draft action plan for CAPA-YYYY-NNN"
- "what's the action plan on CAPA-YYYY-NNN"
- "preventive action for CAPA-YYYY-NNN"
- "any open CAPAs without action plans"
- "show me the actions on CAPA-YYYY-NNN"

## Implementation, verification, effectiveness (Job 5)

Phrases that track completion and verify.

- "any open CAPAs in implementation"
- "any overdue actions on open CAPAs"
- "any CAPAs in verification"
- "verify the CAPA on [issue]"
- "verify CAPA-YYYY-NNN"
- "effectiveness review for CAPA-YYYY-NNN"
- "is CAPA-YYYY-NNN effective"
- "any CAPAs in their effectiveness window"

## Closeout (Job 6)

Phrases that close a CAPA and stage handoffs.

- "close out CAPA-YYYY-NNN"
- "draft the closeout for CAPA-YYYY-NNN"
- "ready to close CAPA-YYYY-NNN"
- "any CAPAs ready to close"

## Status (cross-cutting)

Read-only. No HITL gate.

- "what's open in CAPA"
- "what's in the SJS CAPA Log"
- "any open CAPAs"
- "any open CAPAs by vendor [name]"
- "any open CAPAs on [SKU]"
- "any open CAPAs from [source — complaint, lab, batch, regulatory, audit]"
- "CAPA queue status"
- "any overdue NCRs"
- "any [Pending QA Lead] gates open"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "log this complaint" | complaint-and-event-handler | Customer signal intake |
| "trigger a recall on [SKU/batch]" | complaint-and-event-handler | SKN-OPS-003 walk |
| "trigger SAE protocol" | complaint-and-event-handler | SKN-OPS-002 walk |
| "release or hold on this batch" | batch-lifecycle-tracker (v5.4) | Batch decisions |
| "schedule a stability check" | batch-lifecycle-tracker (v5.4) | In-market stability |
| "vendor scorecard hit" | quality-lab-coordinator (v5.3) → purchasing-manager | Vendor scorecard ownership |
| "lab pattern by vendor" | quality-lab-coordinator (v5.3) | Lab-side analysis |
| "shipping quality this week" | quality-manager (v5.5) | QoS dashboard |
| "is this reportable to [authority]" | regulatory-manager (v6) | Reportability assessment |
| "branded quality dashboard" | quality-status-reporter (v5.6) | Output generation |
| "update PLM on [batch / vendor / SKU]" | plm-assistant | PLM is the only writer |

When a peer skill isn't live yet, the phrase still gets handled gracefully — capa-coordinator stages a handoff with the documented title prefix and notifies the operator (see SKILL.md Job 6 / Out of scope).

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "open a CAPA on [batch] without an NCR" | Pause. NCR is the intake event per SKN-OPS-001 §5.1 + SKN-OPS-005. Draft the NCR first, then convert. |
| "this is just a CAPA, skip the NCR" | Same as above — NCR is required. Explain why and draft. |
| "we already had a CAPA on this — open another" | Check `Linked Source Task` and `Root Cause Statement` across recent closed CAPAs. If the same root cause shows up, the existing CAPA reopens at investigation rather than a new CAPA opening. Effectiveness failure path. |
| "auto-close the CAPA, the actions are done" | Decline. Verification + effectiveness review are required QA Lead gates per L2. |
| "skip the QA Lead approval, I'll cover it" | Decline at v5.2. The L2 split is the audit-trail mechanism; collapsing it loses what makes CAPAs defensible. If the QA Lead role-holder needs to change, update the role map. |
