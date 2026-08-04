---
sop_id: SKN-OPS-009
title: Reportable Events Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-05-09
next_review_date: 2027-05-09
---

# Reportable Events Procedure

## 1. Why this exists

MoCRA serious adverse events and FDA product recalls carry hard statutory clocks — 15 days for SAE awareness; 1–3 days for a Class I recall; roughly 10 days for Class II; roughly 30 days for Class III. Without a documented procedure, agency packets get drafted ad hoc in inconsistent formats, Pedrero gets pinged from multiple inboxes with no single thread per filing, clock-tracking lives in someone's head, and classification becomes inconsistent from one Operator to the next. This procedure closes those gaps: every reportable event walks the same intake-to-close workflow, with proposed classification, binding Pedrero sign-off, agency submission, and statutory clock tracking. Anchors: SKN-OPS-001 §5.6 (retention), SKN-OPS-002 (SAE intake), SKN-OPS-003 (recall ops).

## 2. Scope

Applies to any Sweet July Beauty, LLC reportable event: MoCRA serious adverse events meeting the SAE definition; FDA product recalls (Class I, II, III per 21 CFR 7); state adverse event reports (CA, NY, WA, OR); and MoCRA-specific recall reporting.

Does not apply to: customer complaint intake or triage (SKN-OPS-004, SKN-OPS-002); recall ops execution — customer notification, retailer pulls, return logistics (SKN-OPS-003); the CAPA opened from an SAE or recall (SKN-OPS-001); pre-launch IL review, claim sub, label artwork, or retailer attestations (SKN-OPS-008); MoCRA registrations or state cosmetic registries; or international adverse-event reporting.

## 3. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Quality, on the cross-flag from a complaint, or the Operator on direct intake. |
| **Operator** | Confirms scope at intake, drafts proposed classification, drafts packet contents, drafts Pedrero send, drafts agency submission, submits the agency filing manually after Reg Lead approval. |
| **Reg Lead** | Internal sign-off authority. Approves every Pedrero send and every agency submission as two distinct gates per filing — separate audit-trail entries even when held by the same person as Operator. |
| **External Reg Partner** | All substantive regulatory review including binding classification calls. Pedrero Regulatory: Amy Pedrero principal, Heather Folkes and Teona Bebia secondary. No internal authority. |
| **QA Lead** | Consult-only on overlapping quality issues. |
| **Voice of Customer** | Consult-only on SAE classification where customer narrative interpretation matters. |

## 4. MoCRA SAE Classification

### 4.1 Definition criteria

A consumer event is a serious adverse event under MoCRA if it results in any of: death; a life-threatening experience; in-patient hospitalization; a persistent or significant disability or incapacity; a congenital anomaly or birth defect; an infection requiring medical or surgical intervention to prevent any of the above; or any serious or important medical event that, on reasonable medical judgment, jeopardizes health or requires intervention to prevent any of the above.

### 4.2 One event, one filing

Each consumer event with a potentially serious outcome gets its own SAE filing. Aggregating across consumers requires Pedrero confirmation that aggregation criteria are met.

### 4.3 Classification draft

A draft proposes whether the event meets the SAE definition (yes / no / Pedrero call required), the criteria points cited, and evidence references. Pedrero's call is binding.

## 5. FDA Recall Classification (21 CFR 7)

### 5.1 Class definitions

| Class | Definition |
|---|---|
| **I** | Reasonable probability the violative product causes serious adverse health consequences or death. |
| **II** | May cause temporary or medically reversible adverse health consequences, or the probability of serious consequences is remote. |
| **III** | Not likely to cause adverse health consequences. |

### 5.2 Reporting timeline expectations

Class I: 1–3 days from awareness. Class II: roughly 10 days. Class III: roughly 30 days. These are operational targets — the binding statutory trigger depends on the specific defect and FDA correspondence, and Pedrero confirms the binding window per case.

### 5.3 Classification draft

A draft proposes the class with rationale, the 21 CFR 7 criteria points cited, and evidence references. Pedrero's call is binding.

## 6. SAE Packet Contents

Date of awareness; date of the consumer event if known; consumer information handled under HIPAA-equivalent privacy rules; event description (verbatim plus a summarized fact set); severity assessment per §4.1; batch context; the complaint linkage; proposed classification with rationale; supporting documents; and a plain-language reg ask confirming the classification.

## 7. Recall Report Contents

Event description; batch scope (single or explicit multi-batch list); distribution data (DTC and retailer breakdown, specific SKUs and quantities); hazard assessment; proposed class with 21 CFR 7 rationale; supporting docs (recall strategy draft, customer notification draft, retailer notification list); and a plain-language reg ask confirming the class.

## 8. Pedrero Send Mechanics

Subject prefixes by filing type: `[SAE Filing — SKU-CODE]`, `[FDA Recall — Class X — SKU-CODE]`, `[State AE — STATE — SKU-CODE]`, `[MoCRA Recall — SKU-CODE]`, with `URGENT — by [date]` whenever the statutory clock is tighter than 5 business days.

Default return windows: SAE (MoCRA) 3 business days; Recall Class I 1 business day; Class II and III 5 business days; State AE 5 business days. Pedrero's on-call expectation for SAE and Class I recall is same-day acknowledgment with full review inside the window; a miss triggers the §12 escalation path.

Sends are never automated — drafted and staged, sent manually after Reg Lead approval, moving the record to **In Pedrero Review** with the outbound timestamp captured.

## 9. Pedrero Return Processing

**Approved (classification confirmed)** — moves to agency submission staging (§10), updating the event type and packet first if the classification was revised.

**Returned for revision** — moves to Returned — Action Required with rationale captured; Operator decides the next step.

**Question / clarifying request** — a clarifying reply is staged and Reg Lead-approved; the record stays In Pedrero Review.

Verbal opinions from a call are never acted on alone — a written confirmation send is staged (`[CONFIRMING — ... — Pedrero verbal opinion]`), particularly critical for any opinion that an event does *not* meet the SAE definition or that a recall does *not* require reporting.

## 10. Agency Submission

Filing channels: MoCRA SAE via the FDA MedWatch portal (Form FDA 3500A or MoCRA-specific equivalent, confirmed current at submission time); FDA recall via the FDA recall reporting portal per 21 CFR 7, including the recall strategy submission; state AE reports via each state's own consumer cosmetic adverse-event channel (CA, NY, WA, OR).

The packet and form-field values are drafted and staged for the Operator to enter — the skill-side system never files directly. Reg Lead approves the agency submission as a gate distinct from the Pedrero send approval (§8) — two separate audit-trail entries per filing. The Operator submits manually and captures the submission timestamp and any agency-assigned tracking number.

## 11. Agency Response, Statutory Clock, Closeout

`Window End` carries the statutory deadline, not Pedrero's expected return. Reminder schedule: MoCRA SAE (15 days) at 60% / 80% / 95%, daily after 80%; Recall Class I hourly after 80%; Class II on the same scale as MoCRA SAE; Class III at 50% / 75% / 90%, daily after 90%; State AE per the state-specific window on the 60/80/95% pattern. Escalation to Reg Lead fires automatically at 80% of clock and to the Operator at 95% if Pedrero hasn't returned the packet — a clock never slides silently.

On agency response: **acknowledgment** — timestamp and reference number logged, moving to Awaiting Agency Response or held in Submitted to Agency until the agency closes; **follow-up request** — captured, restaged to Pedrero if it needs regulatory review or answered directly if routine; **agency close** — a three-line summary (event type, classification, agency reference and close date), a close-the-loop note back to the originating complaint record, and the record moves to Closed.

## 12. Missed-Clock Handling

A breached statutory clock is never hidden: a late-filing packet is staged to Pedrero with explicit acknowledgment of the breach, the delay rationale, and recommended remediation. Pedrero confirms the strategy — late filing with voluntary disclosure of the delay, or an alternate path. The miss becomes part of the permanent record, referenced in the next CAPA, and routes to CAPA (SKN-OPS-001) with source `regulatory-observation` for systemic prevention.

## 13. Records and Retention

| Record | Retention |
|---|---|
| SAE filings sent to FDA | Indefinite — FDA standard for adverse event records |
| Recall reports sent to FDA | 7 years from agency close |
| Pedrero correspondence | 7 years from correspondence date |
| Agency correspondence | 7 years from agency close |
| State AE filings | Per state requirements; default 7 years from close |
| Working drafts that didn't ship | 1 year from abandonment |

Retention anchor: SKN-OPS-001 §5.6.

## 14. Procedure Review

Annual review on the SOP anniversary. Reg Lead reviews the procedure walk against actual filing outcomes from the prior 12 months, with Pedrero consult on substantive updates. Mid-cycle revisions are triggered by a material change to FDA or MoCRA implementation guidance, a new state AE requirement, a missed-clock incident surfacing a procedure gap, or an audit finding.

## 15. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-05-09 | Initial issue. Drafted with Pedrero Regulatory consult on substantive content. | Alvin Belt |
