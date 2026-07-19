# Cross-cutting Task Templates

quality-manager creates tasks that don't fit any single sub-skill. These six task types live in the Cross-cutting Tasks section of SJS Quality Management. Every cross-cutting task creation is a QA Lead gate.

---

## 1. SOP Annual Review

**Trigger:** auto on Next Review Due date from `references/sop-catalog.md`; "SOP annual review for [SOP]"; "any SOPs due for review".

**Task title:** `[SOP Annual Review] SKN-OPS-NNN [Title] — Due [YYYY-MM-DD]`

**Custom field values:**
- `Cross-cutting Type` = SOP Annual Review
- `SOP Reference` = SKN-OPS-NNN
- `Status` = Pending
- `Gate` = Pending QA Lead

**Description template:**

```
Annual review of SKN-OPS-NNN [Title] — Rev [current], effective [date]

Walk the §4.1 review checklist from references/sop-catalog.md:
1. Still in scope — does this SOP still apply to current operations?
2. Still accurate — procedure steps still walkable as written?
3. Roles current — match references/role-map.md?
4. Aligned with current operations — current SKUs, contract labs, vendors, retailers?
5. No CAPA-flagged gaps — query capa-coordinator for open or recently closed CAPAs flagging this SOP.

Outcome (one of):
- Reviewed — no change → update catalog Next Review Due to [today + 1 year]
- Reviewed — minor revision → bump to Rev.X.1, walk abbreviated ratification
- Reviewed — major revision → return to authoring sub-skill for new revision draft

Source: references/sop-catalog.md
```

**On QA Lead approval of outcome:**
- No change: update catalog, close task.
- Minor revision: update mirror file + .docx + SharePoint, update catalog with new Rev, close task.
- Major revision: open `[SOP Revision Pending]` queue task for the new revision draft, close this review task with rationale.

---

## 2. Audit Prep

**Trigger:** Operator-direct ("audit prep for [retailer]"); auto on retailer audit calendar (read from Outlook calendar via outlook-asana-bridge).

**Task title:** `[Audit Prep] [Retailer / Authority] — Audit [YYYY-MM-DD]`

**Custom field values:**
- `Cross-cutting Type` = Audit Prep
- `Status` = Pending
- `Gate` = Pending QA Lead

**Description template:**

```
Audit: [Retailer / Authority]
Audit date: YYYY-MM-DD
Lead time: [N business days]
Audit scope: [QA program / cosmetic GMP / specific product line / supplier audit / other]

Documentation to assemble:
- [ ] SOP suite current revisions (pull from references/sop-catalog.md)
- [ ] Recent CAPAs (last 12 months) — query capa-coordinator
- [ ] Stability records for in-market batches — query batch-lifecycle-tracker
- [ ] Customer complaint summary — query complaint-and-event-handler
- [ ] Vendor compliance docs — query purchasing-manager
- [ ] Lab finding records (last 12 months) — query quality-lab-coordinator
- [ ] Training records — currently held by [TBD; SKN-OPS-001 §6 references training but no skill owns the records]
- [ ] [Audit-specific items — fill in based on retailer's questionnaire]

Pre-audit walkthrough: [date — typically 5-10 business days before audit]
Owner: [role + name]
Backup: [role + name]
```

**Subtasks:** create one per documentation line item above with owners and due dates.

---

## 3. Retailer Quality Questionnaire

**Trigger:** Operator-direct ("retailer questionnaire from [retailer]"); auto on outlook-asana-bridge inbound flagged as quality-related from a known retailer sender.

**Task title:** `[Retailer Questionnaire] [Retailer] — Received [YYYY-MM-DD]`

**Custom field values:**
- `Cross-cutting Type` = Retailer Questionnaire
- `Status` = Pending
- `Gate` = Pending QA Lead

**Description template:**

```
Retailer: [Retailer name]
Source: [Outlook inbound | direct request | retailer portal]
Received: YYYY-MM-DD
Due back to retailer: YYYY-MM-DD
Sections requested:
- [ ] [Section 1 from questionnaire]
- [ ] [Section 2]
- [ ] [Section 3]

For each section: which sub-skill or SOP holds the answer.
Owner: [role + name]
Approver before send: QA Lead

Originating email or portal link: [paste]
```

**On QA Lead approval of completed questionnaire:**
- Send back to retailer (via outlook-asana-bridge or direct).
- Comment on this task with send timestamp and reply tracking.
- Close task when retailer confirms receipt or 14 days post-send (whichever first).

---

## 4. Regulatory Inspection Prep

**Trigger:** Operator-direct ("regulatory inspection prep for [authority]"); auto on regulatory-manager inbound flagged. Coordinates with sjs-regulatory-system (System C, live) for the regulatory side of the prep.

**Task title:** `[Regulatory Inspection] [Authority] — Inspection [YYYY-MM-DD or TBD]`

**Custom field values:**
- `Cross-cutting Type` = Regulatory Inspection
- `Status` = Pending
- `Gate` = Pending QA Lead

**Description template:**

```
Authority: [FDA | MoCRA | state regulator | international authority]
Inspection type: [scheduled | for-cause | surprise | response to specific complaint]
Notice received: YYYY-MM-DD
Inspection date: [YYYY-MM-DD or TBD]
Lead time: [N business days, or "no advance notice"]
Inspection scope: [cosmetic GMP / labeling / safety / specific product / other]

Documentation to assemble:
- [ ] Cosmetic GMP records per ISO 22716
- [ ] SOP suite current revisions
- [ ] CAPA log (last 24 months)
- [ ] Adverse event records — query complaint-and-event-handler for SAE history
- [ ] Recall records (if any)
- [ ] Stability records
- [ ] Manufacturing records — pull from PLM via plm-assistant
- [ ] Vendor and supplier audit records
- [ ] Training records
- [ ] [Authority-specific requirements]

Legal review: [required? — typically yes for FDA / MoCRA]
Communications protocol: [who speaks to inspector, who records, who escalates]
Post-inspection: any 483 / observation response within [authority's specified window]

Owner: [role + name]
Legal lead: [TBD]
```

---

## 5. Quality System Review

**Trigger:** Quarterly schedule (first business day of Jan / Apr / Jul / Oct); "quality system review".

**Task title:** `[Quality System Review] Q[X] [YYYY]`

**Custom field values:**
- `Cross-cutting Type` = Quality System Review
- `Status` = Pending
- `Gate` = Pending QA Lead

**Description template:**

```
Quarterly cross-skill quality state review.

Sections:
1. CAPA volume and outcomes — counts by source, by severity, by closure outcome (effective vs partially effective vs not effective). Pull from capa-coordinator.
2. NCR volume and conversion rate — what % of NCRs converted to CAPAs vs closed-no-CAPA. Pull from capa-coordinator.
3. Lab findings volume — by classification (OOS, OOT, Incoming Defect, Pattern), by severity. Pull from quality-lab-coordinator.
4. Vendor scorecard signals — how many fired, by vendor. Pull from quality-lab-coordinator + purchasing-manager.
5. Batch hold / release count — by Hold Reason. Pull from batch-lifecycle-tracker.
6. Customer complaint volume — by category, trend signals fired, recall triggers (if any). Pull from complaint-and-event-handler.
7. QoS metrics — quarterly averages on On-Time, Fulfillment, Damage, Missing/incorrect, Complaint trend.
8. SOP catalog state — ratifications completed, annual reviews completed, gaps surfaced.
9. Cross-cutting work — audits, retailer questionnaires, regulatory inspections this quarter.
10. Top 3-5 quality risks for next quarter.

Outcome: composed quarterly summary. Posted as Asana project status update + handed to v5.6 quality-status-reporter (when live) for branded quarterly report.
```

---

## 6. QoS Threshold Crossed

**Trigger:** Job 3 detects a metric crossing threshold per `references/qos-thresholds.md`.

**Task title:** `[QoS Threshold Crossed] [Metric] — [Actual] vs [Threshold]`

**Custom field values:**
- `Cross-cutting Type` = QoS Threshold Crossed
- `QoS Metric` = [On-time delivery / Fulfillment / Damage / Missing/incorrect / Complaint trend]
- `Threshold Crossed` = [actual value vs threshold]
- `Status` = Pending
- `Gate` = Pending QA Lead

**Description template:**

```
QoS metric crossed threshold.

Metric: [name]
Actual: [value]
Threshold: [value]
Window: [rolling 7d | rolling 30d]
Source: [OC3PL Daily Report Log task gid | SJ Shipping Dashboard count | complaint-and-event-handler trend]

Trend (last 4 windows):
- [Window 1: value]
- [Window 2: value]
- [Window 3: value]
- [Window 4 (current): value]

Suggested next step:
- For On-time / Fulfillment: hand off to oc3pl-order-manager for OC3PL escalation conversation.
- For Damage / Missing/incorrect: hand off to complaint-and-event-handler for customer-side trend analysis + oc3pl-order-manager for fulfillment-side root cause.
- For Complaint trend: hand off to complaint-and-event-handler for §4 trend review.
- If pattern persists 2+ windows: stage a CAPA handoff to capa-coordinator with source = QoS-threshold.
```

**HITL:** QA Lead approves the suggested next step. Operator owns execution.

---

## 7. General notes

- Every cross-cutting task carries `Gate = Pending QA Lead` at creation. Operator drafts, QA Lead approves on creation.
- Operator owns execution after approval. The skill doesn't drive execution.
- On close: closeout summary in `Closeout Summary` field, task moves to Closed section (the existing `Closed` section serves all sub-skills).
- Cross-cutting tasks don't multi-home unless they need a sub-skill's surface (e.g., a CAPA handoff from a QoS task multi-homes to SJS CAPA Log Inbound Staging).
