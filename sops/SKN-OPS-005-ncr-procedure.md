---
sop_id: SKN-OPS-005
title: Non-Conformance Report (NCR) Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-05-09
next_review_date: 2027-05-09
---

# Non-Conformance Report (NCR) Procedure

## 1. Why this exists

Per SKN-OPS-001 §5.1, every CAPA starts with a Non-Conformance Report. SKN-OPS-001 describes the NCR as a form (Appendix A) but doesn't define who can open one beyond "any employee," what fields it must capture beyond "details, date, responsible person," what severity classification applies, when an NCR can close without escalating to CAPA, or how long an open NCR can sit before something has to happen. Without those answers, NCR data is inconsistent, escalation timing drifts, and the audit trail can't show why a non-conformance got the response it got. This procedure closes those gaps and anchors to SKN-OPS-001 §5.1 (Identification), §5.2 (Investigation), and §5.6 (Documentation).

## 2. Scope

Applies to any non-conformance or potential non-conformance at Sweet July Beauty, LLC affecting product quality, safety, or stability; regulatory compliance; process integrity (manufacturing, packaging, labeling, distribution, lab, fulfillment, customer service); or vendor/supplier output.

Does not apply to customer complaints, which run through SKN-OPS-004 and feed the NCR queue only when a trend or single event meets the criteria in §3.1 below.

## 3. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Any employee. Identifies the non-conformance and submits the NCR. |
| **Operator** | Reviews intake, classifies severity, decides whether to escalate to CAPA. |
| **QA Lead** | Sign-off on NCR→CAPA conversion. |
| **Department Manager** | Owns the corrective action within their domain once the NCR converts to CAPA. |

## 4. Intake

### 4.1 What gets opened

An NCR is opened when any of the following is true:

- A product, batch, lot, or component fails an internal spec (visual, sensory, microbial, weight, fill, label).
- Lab results return OOS (out of spec) or OOT (out of trend).
- A vendor delivery fails incoming inspection (wrong material, wrong quantity, wrong COA, expired retest date, packaging damage).
- A process deviation occurs — recipe miss, hold-time exceeded, wrong label revision used, environmental condition out of band.
- A complaint trend meets threshold (3+ same-batch complaints in 30 days, or 5+ same-SKU same-type complaints in 30 days).
- A regulatory observation, audit finding, or retailer-flagged issue requires documented response.
- The Operator or QA Lead requests one explicitly.

### 4.2 Required intake fields

| Field | Notes |
|---|---|
| NCR number | `NCR-YYYY-NNN`, zero-padded sequential by year |
| Date opened | ISO date |
| Reporter | Name + role |
| Source | complaint-trend, lab-OOS, lab-OOT, vendor-receipt, process-deviation, audit-finding, regulatory-observation, internal-flag, or direct-open |
| Category | Product, Process, Vendor, Regulatory, Lab, or Fulfillment |
| SKU(s) affected | If applicable |
| Batch / lot code(s) | If applicable |
| Vendor | If applicable |
| Description | Plain-language description of what was observed and how |
| Evidence | Test results, photos, COAs, complaint task IDs, audit notes |
| Suspected severity | Operator's first read; QA Lead can override at review |
| Containment action taken | What was done immediately to prevent further impact — required even if "none yet — pending review" |

### 4.3 Severity classification

Three bands drive whether and how fast the NCR must convert to CAPA. Bands are guidelines; when in doubt, classify up — an unnecessary CAPA costs less than a missed one.

**Critical** — direct safety, recall risk, regulatory exposure, or repeated failure of the same root cause. Triggers: medical-intervention SAE, FDA observation, retailer chargeback for safety, repeat NCR on same batch within 12 months. NCR→CAPA conversion required within 5 business days.

**Major** — quality or compliance impact that doesn't directly threaten safety but cannot be absorbed without action. Triggers: full-batch OOS, vendor systemic deviation, missed labeling claim, single-batch complaint cluster. NCR→CAPA conversion required within 10 business days.

**Minor** — isolated, contained, no recurrence pattern, no compliance exposure. Triggers: single-unit cosmetic defect, one-off process miss already corrected, single complaint with no batch linkage. NCR→CAPA conversion not required by default; Operator and QA Lead can escalate, or the NCR closes per §6.

## 5. Review and Escalation Decision

Once intake is complete, the Operator reviews the NCR — this is the concrete version of what SKN-OPS-001 §5.2 calls "QA reviews the NCR form to determine the need for a CAPA."

### 5.1 Review checklist

1. Is the description specific enough that a third party could understand what happened? If not, request more detail from the Reporter first.
2. Is the severity classification consistent with §4.3? Adjust if needed.
3. Is there an existing open CAPA covering this root cause? If yes, link the NCR to it as additional evidence rather than opening a duplicate.
4. Does this NCR fit a pattern across recent closed NCRs? If yes, escalation may be required even if this single instance reads Minor.
5. Has containment been confirmed? If not, drive containment first — the NCR review can wait.

### 5.2 Decision branches

**A. Convert to CAPA** — required for Critical and Major; permitted for Minor. Assigns a CAPA number and walks SKN-OPS-001 §5.2 through §5.6.

**B. Close — No CAPA** — permitted for Minor only. Requires a justification stating why no CAPA, what containment closed the loop, and whether trend monitoring continues. This justification is the audit-trail artifact if a regulator or retailer later asks why this didn't get a CAPA.

**C. Hold for more information** — a temporary state with a date-bounded ask back to the Reporter or a supporting team. A hold extending past 10 business days auto-flags for QA Lead attention.

NCR→CAPA conversion requires QA Lead sign-off — that is the audit-trail gate.

## 6. NCR Closed — No CAPA

Used for Minor NCRs where containment is judged sufficient. The justification must include: why no CAPA (tied to §4.3), what containment resolved the issue, confirmation this isn't part of a pattern (citing recent NCRs reviewed), and the reviewer (role + name).

Closed-No-CAPA NCRs are reviewed monthly by the Operator and quarterly by the QA Lead. If a pattern surfaces across closed NCRs that should have been CAPAs, an after-the-fact CAPA can be opened referencing the pattern.

## 7. Documentation and Retention

Every NCR — open, closed-no-CAPA, or converted-to-CAPA — generates a record retained per SKN-OPS-001 §5.6, floor of 3 years post-batch-expiration (ISO 22716).

## 8. SLAs

| Action | SLA |
|---|---|
| NCR review (intake → decision) | 5 business days Critical, 10 Major, 15 Minor |
| Hold-state escalation | 10 business days uninterrupted before auto-flag |
| Critical NCR→CAPA conversion | 5 business days from NCR open |
| Major NCR→CAPA conversion | 10 business days from NCR open |
| Closed-No-CAPA monthly review | First business day of each month |

## 9. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-05-09 | Initial ratification. Drafted 2026-04-29 to fill the gap SKN-OPS-001 §5.1–§5.2 left open; ratified in-place during the System B post-build review. | Alvin Belt |
