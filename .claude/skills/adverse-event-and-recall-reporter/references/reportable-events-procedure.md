# Reportable Events Procedure — SKN-OPS-009 Rev.1

**SOP Number:** SKN-OPS-009
**Title:** Reportable Events Procedure
**Effective Date:** May 9, 2026
**Revision Number:** 1.0
**Prepared by:** Alvin Belt (adverse-event-and-recall-reporter skill-side); Reg Lead (procedural-side); Pedrero Regulatory consult on substantive content.
**Approved by:** Alvin Belt
**Status:** Ratified 2026-05-09. Original draft authored same day, ratified in-place. SharePoint master copy to be filed at `Sweet July/PD/Quality Control & Assurance/SOP/Reportable Events Procedure SKN-OPS-009 Rev.1.docx`.

**Owner:** adverse-event-and-recall-reporter (skill-side); Reg Lead (procedural-side, currently Alvin Belt at v6.2)
**Anchors:** SKN-OPS-001 Rev.1 §5.6 (retention), SKN-OPS-002 Rev.1 (SAE intake — complaint-and-event-handler), SKN-OPS-003 Rev.1 (recall — complaint-and-event-handler), system-c-regulatory-scope.md (system architecture)

## Revision history

| Revision | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-05-09 | Alvin Belt | Initial issue. Authored during v6.2 build of adverse-event-and-recall-reporter; ratified in-place same session. Same pattern as SKN-OPS-006 / 007 / 008. |

---

## Why this exists

MoCRA serious adverse events and FDA product recalls have hard statutory clocks (15 days for SAE awareness; 1-3 days Class I; ~10 days Class II; ~30 days Class III). Without a documented procedure:

- Agency packets get drafted ad hoc — different formats, different evidence depth.
- Pedrero gets pinged from multiple inboxes — no single thread per filing.
- Clock-tracking lives in someone's head — a missed deadline is a regulatory observation or worse.
- Classification becomes inconsistent — what one Operator calls Class II, another might call Class III.

This procedure closes those gaps so every reportable event walks the same intake-to-close workflow with proposed classification, Pedrero binding sign-off, agency submission, and statutory clock tracking.

---

## 1. Scope

Applies to any Sweet July Beauty, LLC reportable event:

- MoCRA serious adverse events (consumer events meeting MoCRA SAE definition criteria)
- FDA product recalls (Class I, II, III per 21 CFR 7)
- State adverse event reports (CA, NY, WA, OR consumer protection statutes)
- MoCRA-specific recall reporting (post-MoCRA implementation rules)

Does not apply to:
- Customer complaint intake or triage (SKN-OPS-002, SKN-OPS-004 — complaint-and-event-handler)
- Recall ops execution: customer notifications, retailer pulls, return logistics (SKN-OPS-003 — complaint-and-event-handler)
- The CAPA opened from an SAE or recall (SKN-OPS-001 — capa-coordinator)
- Pre-launch IL review, claim sub, label artwork, retailer attestations (SKN-OPS-008 — claims-il-and-label-keeper)
- MoCRA registrations or state cosmetic registries (regulatory-manager v6.3)
- International adverse-event reporting

---

## 2. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Quality (complaint-and-event-handler) on the cross-flag, or Operator on direct intake. |
| **Operator** | Confirms scope at intake, drafts proposed classification, drafts packet contents, drafts Pedrero send, drafts agency submission. Submits agency filing manually after Reg Lead approval. Currently Alvin Belt. |
| **Reg Lead** | Internal sign-off authority. Approves every Pedrero send AND every agency submission as two distinct gates per filing — separate audit-trail entries. Currently Alvin Belt at v6.2 (same person as Operator; gate fires as a separate confirmation step). |
| **External Reg Partner** | All substantive regulatory review including binding classification calls. Pedrero Regulatory: Amy Pedrero principal, Heather Folkes and Teona Bebia secondary. No internal authority. |
| **QA Lead** | Consult-only on overlapping issues (e.g., a recall surfacing a stability finding that loops back to batch-lifecycle-tracker). Currently Perrine. |
| **Voice of Customer** | Consult-only on SAE classification when customer narrative interpretation matters. Currently Nicole Iturbe. |

Names live in the runtime role map, not in this procedure.

---

## 3. MoCRA SAE Classification

### 3.1 Definition criteria (current as of MoCRA implementation guidance)

A consumer event is a serious adverse event under MoCRA if it results in any of:

- Death
- A life-threatening experience
- In-patient hospitalization
- A persistent or significant disability or incapacity
- A congenital anomaly or birth defect
- An infection that requires medical or surgical intervention to prevent any of the above
- Any serious or important medical event that, based on reasonable medical judgment, jeopardizes the health of the consumer or requires medical or surgical intervention to prevent any of the above

### 3.2 One event, one filing

Each consumer event with a potentially serious outcome gets its own SAE filing. Aggregation across consumers requires Pedrero confirmation that aggregation criteria are met (e.g., a single batch with multiple identical events tracing to one root cause).

### 3.3 Classification draft

The skill walks §3.1 criteria and proposes:
- Whether the event meets SAE definition (yes / no / Pedrero call required)
- Cited criteria points met
- Evidence references (complaint task, batch records, lab results)

Pedrero confirms or revises. Pedrero's call is binding.

---

## 4. FDA Recall Classification (21 CFR 7)

### 4.1 Class definitions (21 CFR 7.3(m))

| Class | Definition |
|---|---|
| **Class I** | A situation in which there is a reasonable probability that the use of, or exposure to, a violative product will cause serious adverse health consequences or death. |
| **Class II** | A situation in which use of, or exposure to, a violative product may cause temporary or medically reversible adverse health consequences or where the probability of serious adverse health consequences is remote. |
| **Class III** | A situation in which use of, or exposure to, a violative product is not likely to cause adverse health consequences. |

### 4.2 Reporting timeline expectations

| Class | Target window |
|---|---|
| Class I | 1-3 days from awareness |
| Class II | ~10 days from awareness |
| Class III | ~30 days from awareness |

These are operational targets; actual statutory triggers depend on the specific defect and FDA correspondence. Pedrero confirms the binding window per case.

### 4.3 Classification draft

The skill walks §4.1 criteria and proposes:
- Class with rationale
- Cited 21 CFR 7 criteria points met
- Evidence references (complaint pattern, batch records, lab data, distribution scope)

Pedrero confirms or revises. Pedrero's call is binding.

---

## 5. SAE Packet Contents

Every SAE packet sent to Pedrero must include:

| Element | Notes |
|---|---|
| Date of awareness | When AC Brands first became aware of the event |
| Date of consumer event (if known) | From complaint record |
| Consumer information | Consistent with HIPAA-equivalent privacy rules |
| Event description | Verbatim from complaint, plus Operator-summarized facts |
| Severity assessment | Per §3.1 criteria walk |
| Batch context | PLM batch_code, manufacturing date, distribution data |
| Complaint linkage | Originating complaint task (SJ Skin Complaint Log) + Quality `[Reg Flag Pending]` reference |
| Proposed classification | Per §3.3 with rationale |
| Supporting documents | Lab reports if any, complaint history pattern if relevant |
| Specific reg ask | Plain-language ask: "please confirm SAE classification per MoCRA definition" |

---

## 6. Recall Report Contents

Every recall report sent to Pedrero must include:

| Element | Notes |
|---|---|
| Event description | What was discovered, when, by whom |
| Batch scope | Single batch or multi-batch with explicit list. Multi-batch list captured in Linked Batch field comma-separated |
| Distribution data | DTC + retailer breakdown via oc3pl-order-manager queries; specific retailer SKUs and quantities |
| Hazard assessment | Health consequences expected from continued use |
| Proposed Class | Per §4.3 with 21 CFR 7 rationale |
| 21 CFR 7 supporting docs | Recall strategy draft, customer notification draft (from complaint-and-event-handler), retailer notification list |
| Specific reg ask | Plain-language ask: "please confirm recall Class per 21 CFR 7" |

---

## 7. Pedrero Send Mechanics

### 7.1 Subject line conventions

| Filing type | Subject prefix |
|---|---|
| MoCRA SAE | `[SAE Filing — SKU-CODE]` |
| FDA Recall | `[FDA Recall — Class X — SKU-CODE]` (X = I / II / III / TBD) |
| State AE | `[State AE — STATE — SKU-CODE]` |
| MoCRA-specific recall | `[MoCRA Recall — SKU-CODE]` |

Always include `URGENT — by [date]` when statutory clock is tighter than 5 business days.

### 7.2 Contacts

| Field | Recipient |
|---|---|
| To | Amy Pedrero (amy@pedreroregulatory.com) |
| Cc | Heather Folkes (heather@pedreroregulatory.com), Teona Bebia (teona@pedreroregulatory.com) |
| Cc (internal) | Operator (Alvin Belt) for record |

### 7.3 Return windows

| Filing | Default window |
|---|---|
| SAE — MoCRA | 3 business days |
| Recall — Class I | 1 business day |
| Recall — Class II | 5 business days |
| Recall — Class III | 5 business days |
| State AE | 5 business days |

Pedrero on-call expectation for SAE and Class I recall: same-day acknowledgment, full review within window. If she doesn't respond within window, see §11 escalation path.

### 7.4 Send commit

The skill never sends Outlook autonomously. The send draft is composed and staged; Operator hits send manually after Reg Lead approval. The Asana task moves to **In Pedrero Review** on Operator-confirmed send, with the outbound timestamp captured.

---

## 8. Pedrero Return Processing

### 8.1 Return classifications

| Classification | Action |
|---|---|
| **Approved (classification confirmed)** | Move to §9 agency submission staging. If classification revised, update `Event Type` field and packet accordingly before submission. |
| **Returned for revision** | Move to **Returned — Action Required**. Capture rationale. Operator decides next step (revise packet, escalate severity, downgrade classification, request additional internal evidence). |
| **Question / clarifying request** | Stage a clarifying reply. Reg Lead approves the reply send. Asana task stays in **In Pedrero Review**. |

### 8.2 No verbal-only opinions

If Pedrero says anything binding on a call, stage written confirmation send: `[CONFIRMING — SAE Classification — SKU-CODE — Pedrero verbal opinion]`. Do not act on verbal opinion alone. Particularly critical for Pedrero opinions that an event does NOT meet SAE definition or that a recall doesn't require reporting — those decisions must be in writing.

### 8.3 HITL on return

- Operator approves the classification.
- Reg Lead approves any clarifying reply send.

---

## 9. Agency Submission

### 9.1 Channels by filing type

| Filing | Channel | Notes |
|---|---|---|
| MoCRA SAE | FDA MedWatch portal (Form FDA 3500A or MoCRA-specific equivalent) | Confirm current channel at submission time — MoCRA implementation may have introduced a dedicated portal |
| FDA recall | FDA recall reporting portal per 21 CFR 7 | Includes Recall Strategy submission |
| State AE — CA | CA-CDPH Cosmetics Program reporting channel | Specifics confirmed at SKN-OPS-009 ratification |
| State AE — NY | NY-DOH consumer cosmetic adverse event channel | Specifics confirmed at ratification |
| State AE — WA | WA-DOH consumer cosmetic channel | Specifics confirmed at ratification |
| State AE — OR | OR-OHA consumer cosmetic channel | Specifics confirmed at ratification |

### 9.2 Submission mechanics

The skill drafts the submission per agency portal requirements. Stages attachments and form-field values for Operator to enter. The skill never files directly.

### 9.3 HITL

Reg Lead approves the agency submission as a separate gate from the Pedrero send approval at §7. Two distinct audit-trail entries per filing: Pedrero send approval + agency submission approval.

Operator submits manually. Captures submission timestamp, agency-assigned tracking number (when issued) in `Filing Reference` field, `Agency` field set to specific agency.

---

## 10. Agency Response, Statutory Clock, Closeout

### 10.1 Statutory clock tracking

`Window End` field carries the statutory deadline (NOT Pedrero's expected return — agency clock is what matters).

| Clock | Reminder schedule |
|---|---|
| MoCRA SAE (15 days from awareness) | 60% (~9 days), 80% (~12 days), 95% (~14 days) — daily after 80% |
| Recall Class I (1-3 days) | Hourly after 80% — these are urgent |
| Recall Class II (~10 days) | Same scale as MoCRA SAE |
| Recall Class III (~30 days) | 50% / 75% / 90% / daily after 90% |
| State AE | Per state-specific window; 60% / 80% / 95% reminder pattern |

Skill auto-escalates to Reg Lead at 80% of clock and Operator at 95% if Pedrero hasn't returned the packet. Never lets a clock slide silently.

### 10.2 Agency response handling

| Response | Action |
|---|---|
| **Acknowledgment** | Log timestamp + reference number (if not already captured). Move to **Awaiting Agency Response** if agency requires follow-up; otherwise hold in **Submitted to Agency** until agency closes. |
| **Follow-up request** | Capture the request. If response requires Pedrero review, restage via §7. If routine, Operator drafts and Reg Lead approves the agency reply send. |
| **Agency close** | Three-line summary (event type, classification, agency reference + close date). Close-the-loop comment back to Quality's complaint task and the originating SJ Skin Complaint Log entry. Move to **Closed**. |

### 10.3 HITL

Operator approves close. Reg Lead approves any post-submission Pedrero re-stage or agency reply send.

---

## 11. Missed-Clock Handling

If a statutory clock is breached:

1. Don't hide the miss. Stage a late-filing packet to Pedrero with explicit acknowledgment of clock breach, rationale for delay, recommended remediation.
2. Pedrero confirms strategy: late filing + voluntary disclosure of delay vs alternate path.
3. The miss becomes part of the record — captured in Closeout Summary, referenced in next CAPA, and surfaced in next regulatory review.
4. Root cause routes to capa-coordinator as `Source = regulatory-observation` for systemic prevention.

---

## 12. Records and Retention

| Record | Retention |
|---|---|
| SAE filings sent to FDA | Indefinite — FDA standard for adverse event records |
| Recall reports sent to FDA | 7 years from agency close per FDA standard |
| Pedrero correspondence | 7 years from correspondence date |
| Agency correspondence | 7 years from agency close |
| State AE filings | Per state requirements; default 7 years from close |
| Working drafts that didn't ship | 1 year from abandonment |

Storage:
- v6.2 interim: Asana task attachments. The skill's Asana task is the version-of-record; attachments live on the task.
- v6.3 forward: SharePoint regulatory folder. v6.3 build migrates v6.2 attachments to SharePoint and updates retention pointers.

Retention anchor: SKN-OPS-001 §5.6.

---

## 13. Procedure Review

Annual review on SOP anniversary. First review due 2027-05-09 if ratified 2026-05-09.

Review path mirrors SKN-OPS-001 §7. Reg Lead reviews the procedure walk against actual filing outcomes from prior 12 months. Pedrero consult on substantive content updates. quality-manager catalog updates with new revision. Skill SKILL.md updated with new revision reference.

Mid-cycle revisions allowed when:
- FDA or MoCRA implementation guidance changes materially (e.g., new MoCRA-specific portal launches)
- A state agency publishes new AE reporting requirements
- A missed-clock incident surfaces a procedure gap
- An audit finding identifies a procedural weakness

---

## Appendix A — SAE packet template

(To be locked at first SAE filing. Walk the template at second filing to compare what worked.)

## Appendix B — Recall report template

(To be locked at first recall report. Includes 21 CFR 7 supporting doc list per Class.)

## Appendix C — State AE channels

(To be populated at first per-state filing or at ratification, whichever comes first.)
