# Lab Quality Procedure — SKN-OPS-006 Rev.1

**SOP Number:** SKN-OPS-006
**Title:** Lab Quality Procedure
**Effective Date:** May 8, 2026
**Revision Number:** 1.0
**Prepared by:** Alvin Belt (quality-lab-coordinator skill-side); QA Lead (procedural-side)
**Approved by:** Alvin Belt
**Status:** Ratified 2026-05-08. Original draft authored same day, ratified in-place. SharePoint master copy to be filed at `Sweet July/PD/Quality Control & Assurance/SOP/Lab Quality Procedure SKN-OPS-006 Rev.1.docx`.

**Owner:** quality-lab-coordinator (skill-side); QA Lead (procedural-side, currently Perrine — technical QA/QC lead)
**Anchors:** SKN-OPS-001 Rev.1 (CAPA escalation), capa-coordinator NCR Procedure §3.3 (severity bands — kept aligned)

---

## Why this exists

The ratified SOP suite handles the back end of the quality response (CAPA, NCR, recall, complaint, SAE) but not the front end where lab and supplier signals first arrive. Without a lab procedure:

- OOS and OOT classification is ad-hoc — the line between "retest" and "open NCR" lives in operator memory.
- Vendor flag thresholds drift — three OOS events in three months might trigger a scorecard signal, or might not, depending on who is asked.
- COA mismatch handling has no documented retest path.
- Lab pattern analysis has no defined cadence or threshold.

This procedure closes those gaps so lab signal converts to action consistently.

---

## 1. Scope

Applies to any lab-driven, supplier-driven, or material-driven quality signal at Sweet July Beauty, LLC affecting:

- Finished good lab results (PET, accelerated stability, real-time stability, microbial, chemistry retest)
- Component or raw material incoming inspection results (COA review, visual, functional)
- Vendor systemic quality patterns (across batches, time, or SKUs)

Does not apply to:
- Customer complaints (complaint-and-event-handler).
- Pre-launch stability that hasn't transitioned to in-market (asana-pd-manager).
- Batch hold/release decisions (batch-lifecycle-tracker post-v5.4).
- The CAPA itself once a lab finding escalates (capa-coordinator).

---

## 2. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Any employee, contract lab, or vendor that surfaces a lab finding. |
| **Operator** | Reviews intake, classifies the finding, decides between retest, watch, vendor flag, or CAPA handoff. Currently Alvin Belt. |
| **QA Lead** | Sign-off on any vendor flag and any scorecard signal write. Currently Perrine (technical QA/QC lead). |
| **Voice of Customer** | Manages quality intake from the customer perspective. Advisor on lab findings tied to customer-driven signal. Currently Nicole Iturbe (Senior Director, Consumer Strategy & Operations). |

Names live in the runtime role map, not in this procedure. As the org evolves, role-holders change without re-issuing the SOP.

---

## 3. Intake

### 3.1 What gets opened

A lab finding (LF) is opened when any of these is true:

- A lab result returns OOS (out of spec) on any spec listed in the batch's PLM record.
- A lab result returns OOT (out of trend) — within spec but trending toward a limit, or shifting from prior batches in a way that needs attention.
- An incoming material inspection fails (wrong material, wrong qty, COA missing or expired, COA values outside spec, packaging damage that affects the material).
- A retest is requested on a previously OOS or OOT result.
- A pattern across recent lab findings (Job 3 in SKILL.md) crosses §4.2 thresholds.
- The Operator or QA Lead requests one explicitly.

### 3.2 Required intake fields

Every LF must capture:

| Field | Notes |
|---|---|
| LF number | `LF-YYYY-NNN`, zero-padded sequential by year |
| Date opened | ISO date |
| Reporter | Name + role (or contract lab name) |
| Source | One of: lab-OOS, lab-OOT, vendor-receipt, vendor-systemic, batch-pattern, COA-mismatch, internal-flag, direct-open |
| Classification | OOS, OOT, Incoming Defect, Pattern, In-Spec Flag (see §3.3) |
| SKU(s) affected | If applicable |
| Batch / lot code(s) | Required for FG results; required for component receipts |
| Vendor | Required for component / vendor-driven findings |
| Spec(s) affected | The internal spec(s) the finding is measured against |
| Result | The actual measured value(s) and the spec value(s) |
| Description | Plain-language description of what was observed |
| Evidence | Links to test reports, COAs, photos, PLM lab record |
| Suspected severity | Operator's first read; QA Lead can override |
| Containment recommendation | Hold the batch, quarantine the material, retest, no action — drafted at intake |

The skill drafts these from the source signal; the Operator approves before commit.

### 3.3 Classification

Five categories. The category drives the next-step branch.

**OOS (out of spec).** Result is outside the documented spec range. Escalation: Major or Critical severity by default. Always either retests or hands off as NCR to capa-coordinator.

**OOT (out of trend).** Result is within spec but materially different from prior batches' results, or trending toward a limit. Escalation: Minor by default; can shift to Major if the trend points toward a near-term spec failure. Retest path or watch list.

**Incoming Defect.** Vendor receipt failed inspection (wrong material, missing/expired COA, COA values outside spec, packaging damage). Severity per §3.4 vendor severity bands. Routes to either single-shipment handling (back to purchasing-manager) or vendor flag (Job 4) depending on pattern.

**Pattern.** Multi-event finding surfaced from Job 3. Severity reflects the worst single event in the pattern. Routes to vendor flag (Job 4) by default.

**In-Spec Flag.** Result is in spec but something else was off (test ran late, contract lab process deviation, sample integrity question). Logged for completeness; usually closes-no-CAPA after retest confirms.

### 3.4 Severity bands

Three bands, aligned with the NCR Procedure §3.3 so escalations to CAPA carry forward cleanly.

**Critical** — Direct safety, recall risk, regulatory exposure, or repeat root cause.
- Triggers: pathogen positive, preservative system failure, container integrity failure causing safety risk, repeat OOS on the same spec for the same SKU within 12 months
- Path: hand off to capa-coordinator within 5 business days. Containment: hold the batch immediately.

**Major** — Quality or compliance impact that doesn't directly threaten safety but cannot be absorbed without action.
- Triggers: full-batch OOS on a non-safety spec, vendor systemic deviation across 3+ batches, missed claim verification, COA-to-result mismatch material to the spec
- Path: hand off to capa-coordinator within 10 business days. Containment: hold or quarantine pending decision.

**Minor** — Isolated, contained, no recurrence pattern, no compliance exposure.
- Triggers: single OOT, single COA value within spec but with documentation gap, single packaging damage with material salvageable
- Path: retest, watch list, or close after Operator approval. CAPA handoff optional.

The bands are guidelines. Severity reads should err high.

---

## 4. Pattern analysis and vendor flag thresholds

### 4.1 Cadence

- **Monthly sweep.** First business day of each month, the skill pulls the prior 12 months of LFs and runs the §4.2 threshold check.
- **On-demand.** Any operator query that hits Job 3 triggers a pattern read.
- **Auto-fire on intake.** Every new LF triggers a quick pattern read against the same vendor / SKU / spec to catch fast clusters.

### 4.2 Threshold check

A pattern crosses the vendor-flag threshold when any of these is true:

- **Vendor cluster:** 3+ LFs on the same vendor within 90 days, regardless of SKU.
- **SKU cluster on a single vendor:** 2+ LFs on the same SKU + same vendor within 90 days.
- **Spec cluster:** 3+ LFs on the same spec across any vendor or SKU within 60 days (signals a possible upstream / shared-component issue).
- **Severity weighted:** any 1 Critical or 2 Major LFs on the same vendor in 12 months.

When a threshold crosses, Job 3 surfaces the pattern; Job 4 (vendor flag review) walks the decision.

### 4.3 Vendor flag review checklist

Before drafting any flag decision, the Operator confirms:

1. Is the cluster real, or is it a single root cause showing up multiple times in records? (Same shipment counted twice = not a cluster.)
2. Is the issue vendor-attributable, or could it be Sweet July's spec, sampling, or process? Don't flag a vendor for a problem we caused.
3. Has containment been confirmed for each LF in the cluster?
4. Is there an existing vendor flag or open CAPA already covering this pattern? Don't double-flag.
5. Has purchasing-manager seen any related signal already (incoming inspection rejection, shipping issue)? Cross-check before flagging.

### 4.4 Flag decision branches

Three valid endpoints:

**A. Flag for vendor scorecard signal.** Pattern is real, vendor-attributable, and material to the scorecard. Job 5 posts the comment-back to purchasing-manager.

**B. Flag for CAPA.** Pattern needs root cause work. Job 5b stages the NCR intake context for capa-coordinator. Source = vendor-systemic (or vendor-receipt for incoming-only patterns).

**C. Watch list — no flag yet.** Pattern noted but not yet at threshold for action, or marginal evidence. Tracked for [N=2] additional monthly cycles before re-review. If the watch resolves (no new LFs in the next 2 cycles), closes.

The skill drafts the decision and rationale; QA Lead approves any A or B at v5.3.

---

## 5. Retest path (OOS / OOT)

When classification is OOS or OOT and the Operator decides retest is warranted:

1. Document the retest reason on the LF (sample integrity question, suspected lab error, expected drift, vendor request).
2. Pull a fresh sample per the Lab Sample Pulling working note (TBD; flagged for §7 revision once authored).
3. Send to the same lab or a confirming lab. Capture the lab name and request ID on the LF.
4. When retest result returns:
   - **Retest passes** — log result, classify as In-Spec Flag, Operator decides watch or close.
   - **Retest fails** — original classification stands; severity may shift up; CAPA handoff path engages.

Retest is not a workaround. If a retest passes but the Operator suspects sampling or lab variability, the finding still stays on the watch list — the pattern check is what converts watch into flag.

---

## 6. Documentation and retention

Every LF — open, closed, watch-list, or handed off — generates a record retained per SKN-OPS-001 §5.6 retention floor: 3 years post-batch-expiration.

Records live as Asana tasks in SJS Quality Management. Custom fields capture the structured intake, classification, severity, source, and decision. Comments capture the working notes. Attachments hold evidence (test reports, COAs, photos, PLM lab record links).

PLM holds the source-of-truth lab record; the LF Asana task carries the Asana-side workflow surface and links to the PLM record.

---

## 7. SLAs

| Action | SLA |
|---|---|
| LF intake review | 2 business days for Critical, 5 for Major, 10 for Minor |
| Retest dispatch (when chosen) | 3 business days for Critical, 7 for Major, 14 for Minor |
| Vendor flag review (Job 4) | 5 business days from pattern surfacing |
| Scorecard signal post (Job 5) | 1 business day from QA Lead approval |
| CAPA handoff (Job 5b) | Critical within 5 business days, Major within 10, Minor within 15 |
| Watch list re-review | Monthly sweep |

The skill surfaces overdue LFs in status queries and on the dashboard rollup post-v5.5.

---

## 8. Revision history

| Revision | Date | Notes |
|---|---|---|
| 1.0 | 2026-05-08 | Initial ratification. Drafted and ratified in-place during quality-lab-coordinator v5.3 build. SOP & Form Log entry to be added at SharePoint filing. |

Annual review per SKN-OPS-001 §7 pattern. All revisions approved by the QA Manager.

---

## 9. Known content gaps (flagged for §7 revision queue)

| Gap | Section | Skill workaround |
|---|---|---|
| Lab Sample Pulling working note | §5 | Draft TBD; flagged for ratification once authored |
| Vendor flag threshold tuning | §4.2 | Defaults set 2026-05-08; revisit after 2 quarters of data |
| Watch list re-review window | §4.4 | Default N=2 monthly cycles; revisit after first watch resolves |
| Retest authority | §5 | Operator-initiated; QA Lead approval required for any retest at a different lab than original |

These gaps do not block intake. They get bundled into the SOP revision task on first run.
