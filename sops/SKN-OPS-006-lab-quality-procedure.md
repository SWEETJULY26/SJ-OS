---
sop_id: SKN-OPS-006
title: Lab Quality Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-05-08
next_review_date: 2027-05-08
---

# Lab Quality Procedure

## 1. Why this exists

The ratified SOP suite handles the back end of the quality response (CAPA, NCR, recall, complaint, SAE) but not the front end where lab and supplier signals first arrive. Without this procedure, OOS/OOT classification is ad-hoc, vendor flag thresholds drift by who's asked, COA mismatches have no documented retest path, and lab pattern analysis has no defined cadence. This procedure closes those gaps. It anchors to SKN-OPS-001 (CAPA escalation) and keeps its severity bands aligned with the NCR Procedure (SKN-OPS-005 §3.3).

## 2. Scope

Applies to any lab-driven, supplier-driven, or material-driven quality signal at Sweet July Beauty, LLC: finished-good lab results (PET, accelerated stability, real-time stability, microbial, chemistry retest); component or raw material incoming inspection (COA review, visual, functional); and vendor systemic quality patterns across batches, time, or SKUs.

Does not apply to customer complaints (SKN-OPS-004), pre-launch stability that hasn't transitioned to in-market, batch hold/release decisions (SKN-OPS-007), or the CAPA itself once a lab finding escalates (SKN-OPS-001).

## 3. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Any employee, contract lab, or vendor surfacing a lab finding. |
| **Operator** | Reviews intake, classifies the finding, decides between retest, watch, vendor flag, or CAPA handoff. |
| **QA Lead** | Sign-off on any vendor flag and any scorecard signal write. |
| **Voice of Customer** | Advisor on lab findings tied to customer-driven signal. |

## 4. Intake

### 4.1 What gets opened

A Lab Finding (LF) is opened when: a lab result returns OOS (out of spec) against any spec on the batch's record; a result returns OOT (out of trend) — in spec but trending toward a limit or shifting from prior batches; an incoming material inspection fails; a retest is requested on a prior OOS/OOT; a pattern across recent findings crosses the §5.2 thresholds; or the Operator/QA Lead requests one explicitly.

### 4.2 Required intake fields

| Field | Notes |
|---|---|
| LF number | `LF-YYYY-NNN`, zero-padded sequential by year |
| Date opened | ISO date |
| Reporter | Name + role, or contract lab name |
| Source | lab-OOS, lab-OOT, vendor-receipt, vendor-systemic, batch-pattern, COA-mismatch, internal-flag, or direct-open |
| Classification | OOS, OOT, Incoming Defect, Pattern, or In-Spec Flag (§4.3) |
| SKU(s) affected | If applicable |
| Batch / lot code(s) | Required for finished-good results; required for component receipts |
| Vendor | Required for component/vendor-driven findings |
| Spec(s) affected | The internal spec(s) measured against |
| Result | Measured value(s) and the spec value(s) |
| Description | Plain-language description of what was observed |
| Evidence | Test reports, COAs, photos, lab record link |
| Suspected severity | Operator's first read; QA Lead can override |
| Containment recommendation | Hold the batch, quarantine material, retest, or no action |

### 4.3 Classification

**OOS (out of spec)** — outside the documented spec range. Major or Critical by default. Always either retests or hands off as an NCR (SKN-OPS-001).

**OOT (out of trend)** — within spec but materially different from prior batches, or trending toward a limit. Minor by default; can shift Major if the trend points toward near-term failure.

**Incoming Defect** — vendor receipt failed inspection. Severity per §4.4. Routes to single-shipment handling or a vendor flag depending on pattern.

**Pattern** — multi-event finding. Severity reflects the worst single event. Routes to vendor flag by default.

**In-Spec Flag** — in spec, but something else was off (test ran late, lab process deviation, sample integrity question). Logged for completeness; usually closes no-CAPA after a confirming retest.

### 4.4 Severity bands

Aligned with SKN-OPS-005 §3.3 so escalations to CAPA carry forward cleanly.

**Critical** — pathogen positive, preservative system failure, container integrity failure causing safety risk, repeat OOS on the same spec/SKU within 12 months. Hands off to CAPA within 5 business days; containment holds the batch immediately.

**Major** — full-batch OOS on a non-safety spec, vendor systemic deviation across 3+ batches, missed claim verification, material COA-to-result mismatch. Hands off within 10 business days; containment holds or quarantines pending decision.

**Minor** — single OOT, single COA documentation gap with in-spec value, single salvageable packaging defect. Retest, watch list, or close after Operator approval; CAPA handoff optional.

## 5. Pattern Analysis and Vendor Flag Thresholds

### 5.1 Cadence

Monthly sweep on the first business day of each month (prior 12 months of findings against the §5.2 thresholds), plus on-demand and auto-fire-on-intake pattern reads against the same vendor/SKU/spec.

### 5.2 Threshold check

A pattern crosses the vendor-flag threshold when: 3+ findings on the same vendor within 90 days regardless of SKU; 2+ findings on the same SKU + vendor within 90 days; 3+ findings on the same spec across any vendor or SKU within 60 days; or any 1 Critical or 2 Major findings on the same vendor in 12 months.

### 5.3 Vendor flag review checklist

Before drafting a flag decision, confirm: the cluster is real (not one shipment counted twice); the issue is vendor-attributable, not Sweet July's own spec, sampling, or process; containment is confirmed for each finding in the cluster; no existing vendor flag or open CAPA already covers this pattern; and purchasing has not already surfaced related signal.

### 5.4 Flag decision branches

**A. Flag for vendor scorecard signal** — pattern is real, vendor-attributable, material to the scorecard.

**B. Flag for CAPA** — pattern needs root cause work; routes as an NCR with source vendor-systemic (or vendor-receipt for incoming-only patterns).

**C. Watch list — no flag yet** — noted but not yet at threshold, or marginal evidence. Tracked for two additional monthly cycles before re-review; closes if it resolves.

QA Lead approves any A or B decision.

## 6. Retest Path (OOS / OOT)

When the Operator decides a retest is warranted: document the retest reason (sample integrity, suspected lab error, expected drift, vendor request); pull a fresh sample; send to the same lab or a confirming lab, capturing lab name and request ID. On return — **pass**: log result, classify In-Spec Flag, Operator decides watch or close; **fail**: original classification stands, severity may shift up, CAPA handoff engages.

A retest is not a workaround: if it passes but sampling or lab variability is suspected, the finding stays on the watch list.

## 7. Documentation and Retention

Every finding — open, closed, watch-list, or handed off — generates a record retained per SKN-OPS-001 §5.6, floor of 3 years post-batch-expiration.

## 8. SLAs

| Action | SLA |
|---|---|
| LF intake review | 2 business days Critical, 5 Major, 10 Minor |
| Retest dispatch (when chosen) | 3 business days Critical, 7 Major, 14 Minor |
| Vendor flag review | 5 business days from pattern surfacing |
| Scorecard signal post | 1 business day from QA Lead approval |
| CAPA handoff | Critical within 5 business days, Major within 10, Minor within 15 |
| Watch list re-review | Monthly sweep |

## 9. Known gaps carried to next revision

| Gap | Section | Notes |
|---|---|---|
| Lab Sample Pulling working note | §6 | Not yet authored |
| Vendor flag threshold tuning | §5.2 | Defaults set 2026-05-08; revisit after 2 quarters of data |
| Watch list re-review window | §5.4 | Default 2 monthly cycles; revisit after first watch resolves |
| Retest authority | §6 | Operator-initiated; QA Lead approval required for a different lab than the original |

## 10. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-05-08 | Initial ratification. Drafted and ratified in-place. | Alvin Belt |
