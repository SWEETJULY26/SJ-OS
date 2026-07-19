# Trigger phrases — grouped by intent

The router activates on quality-related intent that doesn't clearly map to one sub-skill. SKILL.md and `routing-table.md` hold the canonical decision logic; this file is the working library grouped by what the operator is trying to do.

---

## Generic quality state (cross-skill — to quality-manager)

Read-only. No HITL. Routes to quality-manager Job 2 (rollup composition).

- "what's open in quality"
- "quality status"
- "where are we on quality"
- "monthly quality summary"
- "any quality concerns"
- "give me the quality rollup"
- "catch me up on quality"
- "quality dashboard now" (read-only — for "regenerate" use the dashboard trigger group)

---

## CAPA / NCR (to capa-coordinator)

Lifecycle work per SKN-OPS-001 + working NCR Procedure.

- "open a CAPA on [issue]"
- "open an NCR"
- "log this OOS as an NCR"
- "5 Whys on CAPA-YYYY-NNN"
- "Fishbone on CAPA-YYYY-NNN"
- "what's the root cause on [CAPA / batch]"
- "draft action plan for CAPA-YYYY-NNN"
- "verify CAPA-YYYY-NNN"
- "effectiveness review for CAPA-YYYY-NNN"
- "close out CAPA-YYYY-NNN"
- "any open CAPAs" / "any open NCRs" / "any overdue NCRs"
- "any [Pending QA Lead] gates open in CAPA"

---

## Customer complaints, SAE, recalls (to complaint-and-event-handler)

Customer-side intake per SKN-OPS-002 + SKN-OPS-003 + SKN-OPS-004.

- "log this complaint"
- "got a customer complaint about [SKU]"
- "complaint trend this month"
- "complaint rate by SKU"
- "trigger SAE protocol"
- "got an allergic reaction report"
- "any open SAEs"
- "trigger a recall on [SKU / batch]"
- "what's the customer feedback on [SKU]"
- "complaint pattern review"

---

## Lab signal — OOS, OOT, vendor (to quality-lab-coordinator)

Lab-side classification per SKN-OPS-006.

- "log this OOS"
- "log this OOT"
- "got an OOS on [batch / SKU]"
- "PET test failed on [batch]"
- "stability fail on [batch]"
- "lab result came back on [batch]"
- "incoming material defect on [batch / vendor]"
- "COA mismatch on [batch]"
- "did the latest [vendor] shipment pass"
- "lab patterns by vendor"
- "any patterns this month"
- "flag the vendor on this"
- "vendor scorecard hit on [vendor]"

---

## Batch state, stability, hold/release (to batch-lifecycle-tracker)

Batch lifecycle per SKN-OPS-007.

- "release the [batch]"
- "hold the [batch]"
- "hold lot [batch_code]"
- "release [batch_code]"
- "release the hold on [batch_code]"
- "schedule the PET test for [batch]"
- "schedule [test] for [batch_code]"
- "stability calendar"
- "any stability tests due"
- "what's the status on lot [batch_code]"
- "lifecycle on [batch_code]"
- "any near-expiry batches"
- "transition [SKU] to in-market stability"
- "any batches on hold" / "any batches in stability" / "any batches on watch"

---

## SOP catalog, ratification, annual review (to quality-manager)

System B umbrella concerns.

- "current revision of SKN-OPS-XXX"
- "is [procedure] ratified"
- "what SOPs are pending ratification"
- "any SOPs due for review"
- "any SOPs due for review in next [N] days"
- "SOP catalog"
- "ratify [procedure name]"
- "ratify SKN-OPS-005"
- "approve the [procedure] draft"
- "SOP annual review for SKN-OPS-XXX"

---

## Cross-cutting work (to quality-manager)

Audit prep, regulatory inspections, retailer questionnaires, quarterly reviews, QoS.

- "audit prep for [retailer]"
- "retailer questionnaire from [retailer]"
- "regulatory inspection prep for [authority]"
- "quality system review"
- "shipping quality this week"
- "QoS rollup"
- "current QoS metrics"
- "any QoS threshold crossings"

---

## Quality dashboard — generation (to quality-status-reporter)

Output writes only.

- "regenerate quality dashboard"
- "rebuild the quality dashboard"
- "publish the quality dashboard"
- "push the quality dashboard"
- "deploy the quality dashboard"
- "monthly quality snapshot"
- "snapshot the quality dashboard"
- "branded quality update for [audience]"
- "quality update for the team"
- "is the quality dashboard live"

---

## Boundary phrases — out of System B

The router defers to other systems on these.

| Phrase pattern | Routes to |
|---|---|
| "PD work" / "formula approval" / "signed approvals" / "branded PD update" | sjs-pd-system |
| "place a PO" / "vendor performance" / "what's on hand" / "S&OP" / "shipping" | sjs-ops-system |
| "is this reportable to FDA / MoCRA" / "MoCRA registration" / "Leaping Bunny" / "Prop 65" / "CA or WA Toxic-Free Cosmetics Act" / "CA Fragrance and Flavor Right to Know" / "stage the IL on [SKU]" / "stage the [retailer] attestation" | sjs-regulatory-system |
| "leadership dashboard" / "executive view" | ac-brands-leadership-dashboard |
| "weekly briefing" / "Slide 5 for Ayesha" | ayesha-weekly-briefing |
| "update PLM on [batch / vendor]" | plm-assistant |

---

## Edge case routing

| Pattern | Behavior |
|---|---|
| "open a CAPA on this complaint" | complaint-and-event-handler logs the originating event; capa-coordinator opens the CAPA. Both are involved. |
| "open a CAPA on this OOS" | quality-lab-coordinator classifies first; if Job 4 decision = CAPA route, capa-coordinator picks up. Don't skip classification. |
| "release the batch — the CAPA closed" | batch-lifecycle-tracker for the release decision. capa-coordinator close is the precondition. |
| "complaint may be a regulatory issue" | complaint-and-event-handler walks SKN-OPS-002 if SAE; on confirmation stages `[Reg Flag Pending — regulatory-manager]`. regulatory-manager fans out to adverse-event-and-recall-reporter for agency filing per SKN-OPS-009. |
| "vendor flag based on a CAPA closeout" | quality-lab-coordinator stages the flag; comment-back to purchasing-manager for the scorecard write. |
| "SOP question on [topic]" | quality-manager catalog first to identify SOP, then forward to owning skill if procedural. |
| "the dashboard is broken" | quality-status-reporter for page issue; quality-manager if data is wrong. |

---

## Silent operation

The router runs silently. Don't announce "I'll route this to capa-coordinator" — just deliver the answer. The operator doesn't need to see the routing layer; they need the answer.

When a sub-skill is unavailable or the data isn't there, surface that fact directly without referencing the router.
