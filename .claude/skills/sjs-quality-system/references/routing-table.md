# Routing table — full

The router's decision table for every System B intent. SKILL.md holds the canonical short version; this file is the working library with edge cases and tiebreakers.

---

## 1. Direct forwards (single sub-skill)

### → capa-coordinator

| Trigger phrase | Notes |
|---|---|
| "open a CAPA on [issue / batch / vendor]" | Standard CAPA intake |
| "open an NCR on [issue]" | NCR is the intake event per SKN-OPS-001 §5.1 |
| "log this OOS as an NCR" | OOS-driven NCR — capa-coordinator owns intake; if the OOS hasn't been classified yet, route to quality-lab-coordinator first |
| "log this vendor receipt failure as an NCR" | Vendor-receipt NCR |
| "log this audit finding from [retailer]" | Audit-finding NCR |
| "5 Whys on CAPA-YYYY-NNN" / "Fishbone on CAPA-YYYY-NNN" | RCA tools |
| "what's the root cause on CAPA-YYYY-NNN" | RCA query |
| "draft action plan for CAPA-YYYY-NNN" | Action plan |
| "verify the CAPA on [issue]" / "verify CAPA-YYYY-NNN" | Verification phase |
| "effectiveness review for CAPA-YYYY-NNN" | Effectiveness phase |
| "close out CAPA-YYYY-NNN" / "ready to close CAPA-YYYY-NNN" | Closeout |
| "any open CAPAs" / "any open NCRs" / "any overdue NCRs" | Status query |
| "any [Pending QA Lead] gates open in CAPA" | Gate query |

### → complaint-and-event-handler

| Trigger phrase | Notes |
|---|---|
| "log this complaint" / "got a customer complaint about [SKU]" | Standard complaint intake |
| "complaint trend this month" / "complaint rate by SKU" | Trend query |
| "trigger SAE protocol" / "got an allergic reaction report" | SAE workflow per SKN-OPS-002 |
| "any open SAEs" | SAE status |
| "trigger a recall on [SKU / batch]" | Recall workflow per SKN-OPS-003 — always requires explicit kickoff phrase + approval |
| "what's the customer feedback on [SKU]" | Customer-side query |
| "complaint pattern review" | Pattern detection |

### → quality-lab-coordinator

| Trigger phrase | Notes |
|---|---|
| "log this OOS" / "got an OOS on [batch]" | Lab classification — OOS path |
| "log this OOT" / "got an OOT on [batch]" | Lab classification — OOT path |
| "PET test failed on [batch]" / "stability fail on [batch]" | Lab fail intake |
| "lab result came back on [batch]" | Lab result intake |
| "incoming material defect on [batch / vendor]" | Vendor receipt failure |
| "COA mismatch on [batch]" | COA-driven NCR path |
| "did the latest [vendor] shipment pass" | Receipt status query |
| "lab patterns by vendor" / "any patterns this month" | Pattern analysis |
| "flag the vendor on this" / "open a vendor flag on [vendor]" | Vendor flag review |
| "vendor scorecard hit on [vendor]" | Scorecard signal staging |

### → batch-lifecycle-tracker

| Trigger phrase | Notes |
|---|---|
| "release the [batch]" / "hold the [batch]" / "hold lot [batch_code]" | Hold/release decision |
| "release [batch_code]" / "release the hold on [batch_code]" | Release decision |
| "schedule the PET test for [batch]" / "schedule [test] for [batch_code]" | Stability scheduling |
| "stability calendar" / "any stability tests due" | Stability query |
| "what's the status on lot [batch_code]" / "lifecycle on [batch_code]" | Batch state query |
| "any near-expiry batches" | Near-expiry quality call |
| "transition [SKU] to in-market stability" | PD → in-market handoff |
| "any batches on hold" / "any batches in stability" / "any batches on watch" | Status queries |

### → quality-manager

| Trigger phrase | Notes |
|---|---|
| "current revision of SKN-OPS-XXX" / "is [procedure] ratified" | SOP catalog query |
| "what SOPs are pending ratification" | Ratification queue query |
| "any SOPs due for review" / "SOP annual review for SKN-OPS-XXX" | Annual review |
| "ratify [procedure name]" / "ratify SKN-OPS-005" | Ratification approval flow |
| "SOP catalog" | Catalog read |
| "audit prep for [retailer]" | Cross-cutting task — Audit Prep |
| "retailer questionnaire from [retailer]" | Cross-cutting task — Retailer Questionnaire |
| "regulatory inspection prep for [authority]" | Cross-cutting task — Regulatory Inspection. Coordinates with `sjs-regulatory-system` (System C) which owns the regulatory side of the inspection prep. |
| "quality system review" | Cross-cutting task — Quality System Review (quarterly) |
| "shipping quality this week" / "QoS rollup" / "current QoS metrics" | QoS aggregation |
| "any QoS threshold crossings" | QoS query |

### → quality-status-reporter

| Trigger phrase | Notes |
|---|---|
| "regenerate quality dashboard" / "rebuild the quality dashboard" | Job 1 trigger |
| "publish the quality dashboard" / "push the quality dashboard" | Commit-and-push |
| "monthly quality snapshot" / "snapshot the quality dashboard" | Job 2 trigger |
| "branded quality update for [audience]" | On-demand generation with brand styling |
| "quality update for the team" | Read-only summary path |
| "is the quality dashboard live" | Status query |

---

## 2. Cross-skill / ambiguous → quality-manager

These trigger quality-manager Job 2 (rollup composition).

| Trigger phrase | Why quality-manager |
|---|---|
| "what's open in quality" | Generic — quality-manager owns the rollup |
| "quality status" / "where are we on quality" | Generic state |
| "monthly quality summary" | quality-manager Job 2 weekly rollup is the composition path |
| "any quality concerns" | Cross-skill — needs aggregation |
| "give me the quality rollup" | Direct rollup ask |
| "quality dashboard now" | Read-only summary path (regenerate path goes to quality-status-reporter) |
| "catch me up on quality" | Aggregation ask |

---

## 3. Out-of-System-B routing

These look quality-adjacent but belong elsewhere.

| Trigger phrase | Routes to | Why |
|---|---|---|
| "PD work" / "formula approval" / "signed approvals" | sjs-pd-system | PD scope |
| "place a PO" / "vendor performance" / "what's on hand" | sjs-ops-system | Ops scope |
| "weekly Logiwa report" / "OC3PL daily" | sjs-ops-system → oc3pl-order-manager | Fulfillment workflow |
| "is this reportable to FDA / MoCRA" | sjs-regulatory-system → adverse-event-and-recall-reporter | SAE/recall reportability classification |
| "MoCRA registration" / "INCI compliance" / "Leaping Bunny renewal" / "Prop 65" / "CA Fragrance and Flavor Right to Know" / "CA or WA Toxic-Free Cosmetics Act" | sjs-regulatory-system → regulatory-manager | Registrations + state filings |
| "leadership dashboard" / "executive cross-system view" | ac-brands-leadership-dashboard | Cross-system aggregator |
| "weekly briefing" / "Slide 5 for Ayesha" | ayesha-weekly-briefing | Founder briefing |
| "branded PD update" / "PD status for the team" | sjs-status-reporter | PD-side rendering |

---

## 4. Edge cases

| Pattern | Behavior |
|---|---|
| "open a CAPA on this complaint" | Stage in capa-coordinator with `[CAPA Pending — capa-coordinator]` from complaint-and-event-handler. Both skills involved; complaint-and-event-handler logs the originating event, capa-coordinator runs the CAPA. |
| "release the batch — the CAPA closed" | Routes to batch-lifecycle-tracker for the release decision. capa-coordinator close is the precondition. |
| "open a CAPA on this OOS" | Two-step: quality-lab-coordinator first (classify OOS, run retest path if warranted), then if Job 4 decision = CAPA route, capa-coordinator picks up the staged NCR intake context. Don't skip the lab classification step. |
| "did we ratify the lab procedure" | Routes to quality-manager (catalog query). Answer: yes, SKN-OPS-006 Rev.1 effective 2026-05-08. |
| "did we ratify the batch procedure" | Routes to quality-manager. Answer: yes, SKN-OPS-007 Rev.1 effective 2026-05-08. |
| "did we ratify the NCR procedure" | Routes to quality-manager. Answer: not yet — working draft pending in queue. |
| "we have a complaint trend that may be a regulatory issue" | Two-step: complaint-and-event-handler walks SKN-OPS-002 if SAE / SKN-OPS-003 if recall; on confirmation, stages `[Reg Flag Pending — regulatory-manager]`. regulatory-manager Job 1 fans out to adverse-event-and-recall-reporter for the agency filing per SKN-OPS-009. |
| "open a vendor flag on a vendor based on a CAPA closeout" | Routes to quality-lab-coordinator. Note: the actual scorecard write stays with purchasing-manager via comment-back. |
| "what does our SOP say about [topic]" | Routes to quality-manager (catalog query) to identify which SOP. Then forward to the owning skill if the answer requires walking the procedure. |
| "merge two CAPAs that are duplicates" | Routes to capa-coordinator. Skill-side decision per Procedure §5.2. |
| "the dashboard is broken" | Routes to quality-status-reporter for the page issue; if the data is wrong, route to quality-manager to check rollup. |

---

## 5. Tiebreakers

When two skills could plausibly own the request:

1. **Lab signal vs. CAPA.** Lab classification (OOS/OOT severity, retest decision) goes to quality-lab-coordinator; root cause work goes to capa-coordinator. The router walks the lab path first; CAPA opens only when classification surfaces a CAPA-worthy pattern.
2. **Complaint vs. CAPA.** Customer signal intake goes to complaint-and-event-handler; trend-driven CAPA goes to capa-coordinator. Always classify the complaint first.
3. **Batch hold vs. CAPA.** Batch state decision goes to batch-lifecycle-tracker; root cause goes to capa-coordinator. The hold can land before the CAPA opens; both can be in flight at once.
4. **SOP question — which SOP.** Routes to quality-manager catalog first to identify the SOP. If the question is procedural ("how do we walk §5.2"), then forward to the owning skill.
5. **Cross-cutting work vs. sub-skill work.** SOP annual reviews, audit prep, retailer questionnaires, regulatory inspection prep, quality system reviews are quality-manager work. Sub-skill task creation stays with sub-skills.
6. **Read vs. write on dashboard.** Read-only summary ("what's open") goes to quality-manager (rollup). Write/regenerate ("publish") goes to quality-status-reporter.
