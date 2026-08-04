---
sop_id: SKN-OPS-007
title: Batch Lifecycle Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-05-08
next_review_date: 2027-05-08
---

# Batch Lifecycle Procedure

## 1. Why this exists

Batch state lives across PLM, Asana, and tribal memory. SKN-OPS-001 governs corrective action after a batch fails; SKN-OPS-006 governs classification of a lab result. Neither defines the state machine a batch walks from production through expiration, when to schedule in-market stability tests, what evidence releases a held batch, how near-expiry signal splits between operational write-offs and quality-side decisions, or the handshake from pre-launch to in-market stability. Without this, hold reasons drift, releases happen on memory, stability tests slip silently, and the audit trail can't show who decided what when. This procedure closes those gaps.

## 2. Scope

Applies to every Sweet July Beauty, LLC finished-good batch from first commercial production through terminal state: batch state ownership, in-market stability scheduling and result tracking, hold and release decisions, near-expiry quality-side decisions, and the pre-launch → in-market handoff.

Does not apply to: pre-launch stability (kept by the PD formula tracker), batch creation at receipt or on-hand quantity (inventory management), expired write-offs (inventory management), lab result classification (SKN-OPS-006 owns OOS/OOT severity), the CAPA lifecycle itself (SKN-OPS-001), customer complaint intake or trends (SKN-OPS-004), or component-batch tracking (raw materials and packaging).

## 3. Roles

| Role | Responsibility |
|---|---|
| **Operator** | Reviews transition handoffs, drafts hold/release records, surfaces near-expiry decisions, owns close. |
| **QA Lead** | Approves every hold, every release, and every CAPA-route decision. Same holder as the CAPA and lab-quality QA Lead gates. |
| **Voice of Customer** | Advisor on complaint-trend holds and customer-driven CAPAs. |
| **Department Manager** | Owns containment within their domain when a hold opens, resolved by Hold Reason. |

## 4. Batch State Machine

Every batch sits in one state at a time. Each transition is an audit-trail moment.

- **Active** — healthy batch in distribution; default state from transition until a signal moves it.
- **Stability Pending** — a stability test is scheduled but not yet returned; active for distribution purposes, flagged for the calendar.
- **Hold/Release Review** — awaiting sign-off on either opening a hold or granting a release; transient.
- **On Hold** — sign-off approved hold in effect; distribution stopped, investigation in progress.
- **Watch** — flagged for monitoring, not held; used for a lab finding that didn't escalate, a late-life pattern, or marginal evidence; re-reviewed monthly.
- **Released** — returned to distribution after a hold cleared, or held through natural end-of-life; terminal for the lifecycle record.
- **Pulled** — removed from distribution before natural end-of-life; triggers a separate write-off path.
- **Expired** — statutory expiration date reached; terminal, auto-derived from the batch record.

## 5. Pre-Launch → In-Market Transition

### 5.1 Trigger

Fires the first time both hold for a SKU: the formula has reached final sign-off in the PD tracker, and the first commercial batch has been created (batch quantity exceeds the SKU's sample threshold — default 100 units, tunable per SKU by the QA Lead).

### 5.2 What gets staged

A transition-confirmation record is drafted holding: the source PD project reference; the first batch's code, quantity, production date, and expiration date; formula type (water-based / anhydrous / hybrid, which drives the §6.1 stability schedule); the proposed in-market stability schedule; and the list of pre-launch tasks slated to close at transition.

### 5.3 Approval

One-time approval per SKU per launch. On approval: the first batch's lifecycle record opens at Active; stability schedule items generate per §6; pre-launch stability tasks close with a sync-back note. Subsequent batches for the same SKU enter directly at Active without repeating this step.

### 5.4 Edge cases

If the formula never reached sign-off, no transition fires and the exception is surfaced. If batch quantity sits between 100 and 500 units, the sample-threshold call goes to the QA Lead. A SKU launching multiple variants from one PD project transitions each variant independently on its own first batch.

## 6. Stability Scheduling

### 6.1 Cadence by formula type (anchored in ISO 11930)

| Formula type | Examples | Cadence |
|---|---|---|
| Water-based emulsion | Toner, serum, cream, lotion | PET at launch, PET-EOL, accelerated stability at 3 months, real-time stability annually |
| Anhydrous | Balm, oil, lip oil, lip balm, body oil | Real-time stability annually only — no PET (no preservative system to test) |
| Hybrid (W/O, O/W with low water, lip treatments with water content) | Some lip treatments, certain salves | Anhydrous schedule plus a microbial spot-check at launch |

### 6.2 Per-batch vs every-other-batch

Every batch is tested by default, including re-runs on each new batch. Once a SKU has 3 consecutive clean batches (PET launch, PET-EOL where applicable, accelerated, real-time annual all passing), the schedule can shift to every-other-batch at QA Lead discretion. Any fail re-tightens to per-batch.

### 6.3 Result handling

**Pass** — subtask marked complete, result logged. No sign-off gate on a pass.

**Fail** — routes through the Lab Quality Procedure (SKN-OPS-006), which classifies, runs the retest path if warranted, and, if the result warrants it, initiates a hold request under §7.

## 7. Hold and Release Decisions

### 7.1 Hold review checklist

Before drafting a hold: confirm the source signal is documented (lab finding, complaint trend, vendor signal, regulatory observation, internal flag); confirm severity is consistent with the source (lab severity per SKN-OPS-006 §4.4; complaint-trend severity per SKN-OPS-004 thresholds); establish containment scope (whole batch, single distribution lane, specific retailer or channel); identify the affected position (on-hand by location, in-transit, allocated to retailer orders); and confirm no existing hold or open CAPA already covers the issue.

### 7.2 Hold record fields

Hold Reason, Source, Severity (aligned with SKN-OPS-005 §4.3), Containment scope, Affected position, Date of hold, Approving QA Lead (role, name, timestamp).

### 7.3 Release review checklist

Before drafting a release: confirm the underlying issue is resolved (CAPA closed effective, retest passed clean, complaint pattern broken, regulatory observation resolved); confirm there's evidence the issue won't recur on this batch specifically; confirm the original Hold Reason is still the only release barrier; and confirm downstream notifications are staged.

### 7.4 Release record fields

Release rationale, Resolution path, Evidence, Downstream notifications, Approving QA Lead (role, name, timestamp).

### 7.5 Sign-off

QA Lead approves every hold and every release without exception.

## 8. Near-Expiry Quality-Side Decisions

Inventory management surfaces near-expiry at 90/60/30-day thresholds and cross-posts each threshold here for the quality-side conversation; inventory keeps the operational write-off action.

**90-day** — routine note, typically no action.

**60-day** — confirm late-life PET-EOL is scheduled or completed (water-based) or real-time annual is current (anhydrous). If not scheduled, stage the missing test.

**30-day** — confirm pull plan or expedite end-of-life. Default is a pull plan citing remaining on-hand position; alternative is an expedited final stability test if shelf-life math allows. This decision posts back to inventory management before any write-off.

**Past-expiration** — the batch's state auto-flips to Expired and the lifecycle record closes; inventory handles the position write-off. No further quality-side decision needed — the call was made at the 30-day threshold or earlier.

## 9. CAPA Handoff

Routes to CAPA (SKN-OPS-001) for: repeat OOS or OOT on the same SKU + spec within 12 months; a multi-batch pattern with the same fail signature; a regulatory observation against a batch; or any Critical-severity lab fail by default. The originating batch moves to On Hold until the CAPA closes, then re-routes to Hold/Release Review for the release decision.

## 10. Closeout and Retention

Every batch record closes at terminal state, holding: the transition record, the full stability schedule and every result, every hold and release rationale with approving QA Lead and timestamp, near-expiry decisions per threshold, CAPA links if any, and a closeout summary. Retention: 3 years post-batch-expiration per SKN-OPS-001 §5.6 and ISO 22716.

## 11. SLAs

| Action | SLA |
|---|---|
| Transition handoff stage | 2 business days from trigger |
| Stability subtask dispatch reminder | 5 business days before due |
| Hold review | 1 business day Critical, 3 Major, 5 Minor |
| Release review | 3 business days from evidence-complete |
| Near-expiry 30-day decision | 5 business days from cross-post |
| CAPA handoff stage | Critical within 5 business days, Major within 10, Minor within 15 |
| Closeout | 5 business days from terminal state |

## 12. Known gaps carried to next revision

| Gap | Section | Notes |
|---|---|---|
| Sample threshold for "first commercial batch" | §5.1 | Default 100 units; tunable per SKU |
| Contract lab destinations per SKU | §6 | Captured per SKU at QA Lead config |
| Every-other-batch shift criteria | §6.2 | Default 3 consecutive clean batches; QA Lead can tighten or loosen |
| 30-day pull-vs-EOL default | §8 | Default pull plan; QA Lead can flip to EOL-default per SKU |
| Voice of Customer gate scope | §3 | Refined at next revision |

## 13. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-05-08 | Initial ratification. Drafted and ratified in-place. | Alvin Belt |
