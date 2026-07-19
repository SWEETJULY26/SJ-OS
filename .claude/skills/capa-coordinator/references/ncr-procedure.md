# Non-Conformance Report (NCR) Procedure — SKN-OPS-005 Rev.1

**SOP Number:** SKN-OPS-005
**Title:** Non-Conformance Report (NCR) Procedure
**Effective Date:** May 9, 2026
**Revision Number:** 1.0
**Prepared by:** Alvin Belt (capa-coordinator skill-side); QA Lead (procedural-side)
**Approved by:** Alvin Belt
**Status:** Ratified 2026-05-09. Drafted 2026-04-29 to fill the gap left by SKN-OPS-001 §5.1–§5.2 (which names the NCR Form in Appendix A without specifying a standalone non-conformance procedure); ratified in-place during the System B post-build review. SharePoint master copy to be filed at `Sweet July/PD/Quality Control & Assurance/SOP/Non-Conformance Report (NCR) Procedure SKN-OPS-005 Rev.1.docx`.

**Owner:** capa-coordinator (skill-side); QA Lead (procedural-side, currently Perrine — technical QA/QC lead)
**Anchors:** SKN-OPS-001 Rev.1 §5.1 (Identification), §5.2 (Investigation), §5.6 (Documentation)

---

## Why this exists

Per SKN-OPS-001 §5.1, every CAPA starts with a Non-Conformance Report. The CAPA SOP describes the NCR as a form (Appendix A) but doesn't define:

- Who can open one (any employee per §4, but with no triage step before the form is filled)
- What fields must be captured beyond "details, date, responsible person"
- What severity classification applies and how it shapes the next step
- Under what conditions an NCR closes without escalating to CAPA
- How long an open NCR can sit before something has to happen

Without this, NCR data is inconsistent, escalation timing drifts, and the audit trail can't show why a non-conformance got the response it got. This procedure closes those gaps.

---

## 1. Scope

Applies to any non-conformance or potential non-conformance at Sweet July Beauty, LLC that affects:

- Product quality, safety, or stability
- Regulatory compliance
- Process integrity (manufacturing, packaging, labeling, distribution, lab, fulfillment, customer service)
- Vendor or supplier output

Does not apply to: customer complaints (those run through complaint-and-event-handler and feed the NCR queue only when a trend or single event meets the criteria below).

---

## 2. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Any employee. Identifies the non-conformance and submits the NCR. |
| **Operator** | Reviews intake, classifies severity, decides whether to escalate to CAPA. Currently Alvin Belt. |
| **QA Lead** | Sign-off on NCR→CAPA conversion. Currently Perrine (technical QA/QC lead). |
| **Department Manager** | Owns the corrective action within their domain once the NCR converts to CAPA. |

Names live in the runtime role map, not in this procedure. As the org evolves, role-holders change without re-issuing the SOP.

---

## 3. Intake

### 3.1 What gets opened

An NCR is opened when any of these is true:

- A product, batch, lot, or component fails an internal spec (visual, sensory, microbial, weight, fill, label).
- Lab results return OOS (out of spec) or OOT (out of trend).
- A vendor delivery fails incoming inspection (wrong material, wrong qty, wrong COA, expired retest date, packaging damage).
- A process deviation occurs — recipe miss, hold-time exceeded, label revision used in error, environmental condition out of band.
- A complaint trend meets the threshold defined by complaint-and-event-handler (3+ same-batch in 30 days, 5+ same-SKU same-type in 30 days).
- A regulatory observation, audit finding, or retailer-flagged issue requires documented response.
- The Operator or QA Lead requests one explicitly.

### 3.2 Required intake fields

Every NCR must capture:

| Field | Notes |
|---|---|
| NCR number | `NCR-YYYY-NNN`, zero-padded sequential by year |
| Date opened | ISO date |
| Reporter | Name + role |
| Source | One of: complaint-trend, lab-OOS, lab-OOT, vendor-receipt, process-deviation, audit-finding, regulatory-observation, internal-flag, direct-open |
| Category | Product, Process, Vendor, Regulatory, Lab, Fulfillment |
| SKU(s) affected | If applicable |
| Batch / lot code(s) | If applicable — links to PLM batch record |
| Vendor | If applicable |
| Description | Plain-language description of what was observed and how |
| Evidence | Links to test results, photos, COAs, complaint task IDs, audit notes |
| Suspected severity | Operator's first read; QA Lead can override at review (see §4) |
| Containment action taken | What was done immediately to prevent further impact (hold, quarantine, stop-ship, recall scoping). Required even if "none yet — pending review" |

Anything material to the audit trail goes into the description or evidence fields. The skill drafts these from the source signal; the Operator approves before commit.

### 3.3 Severity classification

Three bands. The band drives whether and how fast the NCR must convert to CAPA.

**Critical** — Direct safety, recall risk, regulatory exposure, or repeated failure of the same root cause.
- Triggers: medical-intervention SAE, FDA observation, retailer chargeback for safety, repeat NCR on same batch within 12 months
- NCR→CAPA conversion: required, within 5 business days of NCR open

**Major** — Quality or compliance impact that doesn't directly threaten safety but cannot be absorbed without action.
- Triggers: full-batch OOS, vendor systemic deviation, missed labeling claim, single-batch complaint cluster
- NCR→CAPA conversion: required, within 10 business days

**Minor** — Isolated, contained, no recurrence pattern, no compliance exposure.
- Triggers: single-unit cosmetic defect, one-off process miss already corrected, single complaint with no batch linkage
- NCR→CAPA conversion: not required by default. Operator + QA Lead can decide to escalate; if they don't, the NCR closes per §5.

The bands are guidelines. Severity reads should err high — when in doubt, classify up. The cost of an unnecessary CAPA is lower than the cost of a missed one.

---

## 4. Review and escalation decision

Once intake is complete, the Operator reviews the NCR. SKN-OPS-001 §5.2 says "QA reviews the NCR form to determine the need for a CAPA." This procedure makes that review concrete.

### 4.1 Review checklist

The Operator checks (then routes to QA Lead for the conversion decision):

1. Is the description specific enough that a third party could understand what happened? If not, request more detail from the Reporter before deciding.
2. Is the severity classification consistent with the criteria in §3.3? Adjust if needed.
3. Is there an existing open CAPA covering this root cause? If yes, link the NCR to that CAPA as additional evidence — do not open a duplicate.
4. Is there a pattern across recent closed NCRs that this one fits? If yes, escalation may be required even if this single instance is Minor.
5. Has containment been confirmed? If not, drive containment first; the NCR can wait.

### 4.2 Decision branches

Three valid endpoints from review:

**A. Convert to CAPA** — required for Critical and Major; permitted for Minor. The skill assigns a CAPA number (`CAPA-YYYY-NNN`) and walks SKN-OPS-001 §5.2 (form team) → §5.3 (action plan) → §5.4 (implementation) → §5.5 (verification & effectiveness) → §5.6 (documentation).

**B. Close — No CAPA** — permitted for Minor only. Requires a justification field captured on the NCR record stating: why no CAPA, what containment closed the loop, whether trend monitoring will continue. The justification is the audit-trail artifact when a regulator or retailer asks why this didn't get a CAPA.

**C. Hold for more information** — temporary state. The NCR sits open with a date-bounded ask back to the Reporter or to a supporting team (lab, vendor, retailer). If the hold extends past 10 business days, it auto-flags for QA Lead attention.

The skill drafts the decision and rationale; the Operator approves. NCR→CAPA conversion requires QA Lead (Perrine) sign-off — that's the audit-trail gate.

---

## 5. NCR Closed — No CAPA

Used for Minor NCRs where the Operator + QA Lead determine the corrective action embedded in containment is sufficient. The justification field must include:

- **Why no CAPA** — explicit reasoning tied to §3.3 severity criteria
- **What containment resolved** — what was done at intake and why it closes the loop
- **Trend exposure** — confirmation that this isn't part of a pattern (cite recent NCRs reviewed)
- **Reviewer** — who signed off (role + name)

Closed-No-CAPA NCRs are reviewed monthly by the Operator and quarterly by the QA Lead. If a pattern shows up across closed NCRs that should have been CAPAs, the skill surfaces it and an after-the-fact CAPA can be opened referencing the pattern.

---

## 6. Documentation and retention

Every NCR — open, closed-no-CAPA, or converted-to-CAPA — generates a record retained per SKN-OPS-001 §5.6. Retention floor: 3 years post-batch-expiration (ISO 22716). The SKN-OPS-001 §5.6 `[X]` placeholder is one of the SOP §7 revision items this procedure flags on first run.

Records live as Asana tasks in the SJS CAPA Log project. Custom fields capture the structured intake, severity, source, category, decision, and conversion link. Comments capture the working notes. Attachments hold evidence (photos, COAs, lab reports, audit observations).

---

## 7. SLAs

| Action | SLA |
|---|---|
| NCR review (intake → decision) | 5 business days for Critical, 10 for Major, 15 for Minor |
| Hold-state escalation | 10 business days uninterrupted before auto-flag |
| Critical NCR→CAPA conversion | 5 business days from NCR open |
| Major NCR→CAPA conversion | 10 business days from NCR open |
| Closed-No-CAPA monthly review | First business day of each month |

The skill surfaces overdue NCRs in status queries and on the dashboard rollup post-v5.5.

---

## 8. Revision history

| Revision | Date | Notes |
|---|---|---|
| 1.0 | 2026-05-09 | Initial ratification. Drafted 2026-04-29 during capa-coordinator v5.2 build to fill the gap left by SKN-OPS-001 §5.1–§5.2; ratified in-place after System B post-build review. SOP & Form Log entry to be added at SharePoint filing. Closes the L4 SOP-gap flag for SKN-OPS-001 §5.2. |

Annual review per SKN-OPS-001 §7 pattern. All revisions approved by the QA Manager.
