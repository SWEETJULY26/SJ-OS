# SKN-OPS-001 — CAPA Procedure walk

Mirrored from `Sweet July/Product Development/Quality Control & Assurance/SOP/Corrective Action Preventive Action (CAPA) SOP SKN-OPS-001 Rev.1.docx` (Effective June 30, 2024). The skill walks the phase structure verbatim and applies judgment within each phase per the Design Principles in SKILL.md.

---

## Source SOP

**Title:** Corrective and Preventive Action (CAPA) Procedure
**SOP Number:** SKN-OPS-001
**Effective Date:** June 30, 2024
**Revision:** 1.0
**Prepared by:** Alvin Belt / Shirlene Loi
**Approved by:** Alvin Belt

## §1. Purpose

Establish a systematic approach for identifying, documenting, analyzing, and implementing corrective and preventive actions to address non-conformances and potential non-conformances within Sweet July Beauty, LLC.

## §2. Scope

Applies to all departments and personnel involved in the identification, documentation, investigation, and resolution of non-conformances and potential non-conformances at Sweet July Beauty, LLC.

## §3. Definitions

- **Corrective Action:** Action taken to eliminate the cause of a detected non-conformance or other undesirable situation.
- **Preventive Action:** Action taken to eliminate the cause of a potential non-conformance or other undesirable potential situation.
- **Non-Conformance:** A deviation from a standard or specification that may affect product quality, safety, or regulatory compliance.

## §4. Responsibilities

| Role | Responsibility |
|---|---|
| Quality Assurance (QA) | Overall responsibility for the CAPA system; compliance with this SOP; maintaining CAPA records |
| Department Managers | Ensure non-conformances within their department are reported, investigated, and resolved |
| All Employees | Report non-conformances and potential non-conformances to their supervisors or QA |

**Skill mapping:** QA Lead role-holder = Perrine (technical QA/QC lead). Voice of Customer role-holder = Nicole Iturbe (Senior Director, Consumer Strategy & Operations) — advisor on complaint-driven CAPAs. Department Manager varies by source category. See `references/role-map.md`.

## §5. Procedure

### §5.1 Identification and Documentation

**SOP text:**
- Any employee identifying a non-conformance or potential non-conformance should report it immediately to their supervisor or QA designee.
- Complete a Non-Conformance Report (NCR) form, including details of the non-conformance, date, and responsible person.

**Skill behavior:**
- Walk `references/ncr-procedure.md` (SKN-OPS-005 Rev.1, ratified 2026-05-09) §3 for intake fields. SKN-OPS-001 §5.1 left NCR fields underspecified ("details, date, responsible person"); SKN-OPS-005 fills the gap with structured intake.
- Job 1 in SKILL.md handles this phase.
- HITL: Operator approves intake.

### §5.2 Investigation

**SOP text:**
- *Initial Assessment:* QA reviews the NCR form to determine the need for a CAPA. If a CAPA is required, assign a CAPA number and open a CAPA file.
- *Root Cause Analysis:* Form a CAPA investigation team including relevant personnel. Conduct a root cause analysis using appropriate tools (e.g., Fishbone Diagram, 5 Whys).

**Skill behavior:**
- Walk SKN-OPS-005 §4 for the review checklist and three decision branches (convert / close-no-CAPA / hold).
- For the convert path, assign `CAPA-YYYY-NNN`, draft team, walk RCA tool from `references/rca-tools.md`.
- The SOP doesn't specify which RCA tool when. Skill defaults: 5 Whys for single-event causes; Fishbone for systemic / multi-factor causes. Operator can override.
- Job 2 (NCR review) and Job 3 (CAPA opening + RCA) in SKILL.md handle this phase.
- HITL: Operator approves NCR→CAPA conversion and team. **QA Lead approves the root cause statement.**

**Closed SOP gap:** §5.2 originally left "need for a CAPA" entirely judgment-based. SKN-OPS-005 §3.3 documents severity bands and §4.2 documents decision branches. Gap closed at SKN-OPS-005 ratification (2026-05-09).

### §5.3 Action Plan

**SOP text:**
- *Corrective Action Plan:* Develop a corrective action plan to address the root cause of the non-conformance. Define actions, responsibilities, and timelines.
- *Preventive Action Plan:* Identify potential non-conformances and develop a preventive action plan. Define actions, responsibilities, and timelines.

**Skill behavior:**
- Both plans drafted using `references/capa-investigation.md` template (mirrors SOP Appendix B).
- Each action item: action, owner (role + person), timeline (date-bounded), evidence-on-completion description.
- Preventive actions tagged for SOP-revision implications (Job 4 in SKILL.md). Any preventive action that changes a SOP routes a `[SOP Revision Pending — quality-manager]` task.
- HITL: Operator approves both plans.

### §5.4 Implementation

**SOP text:**
- *Execute Action Plans:* Implement corrective and preventive actions according to the defined plan. Monitor progress and document completion in the CAPA file.

**Skill behavior:**
- Read-only tracking surface. Action owners post completion as comments with attached evidence.
- Skill surfaces overdue actions on status queries.
- Job 5 in SKILL.md.
- HITL: none — read-only.

### §5.5 Verification and Effectiveness

**SOP text:**
- *Verification:* QA verifies that all actions have been completed as planned. Ensure that corrective actions have effectively eliminated the root cause.
- *Effectiveness Review:* Conduct a review to confirm the effectiveness of corrective and preventive actions. Document the review findings in the CAPA file.

**Skill behavior:**
- Verification = "did the actions happen as planned." Effectiveness = "did the change hold." Distinct steps.
- Effectiveness window by severity (SKN-OPS-005 §3.3): Critical 90 days, Major 60 days, Minor 30 days. SKN-OPS-001 doesn't specify windows; SKN-OPS-005 covers the bands.
- If effectiveness fails, the CAPA reopens at investigation (Job 3) with the failed-effectiveness signal as a new evidence item.
- Job 5 in SKILL.md.
- HITL: **QA Lead approves verification and effectiveness.**

### §5.6 Documentation and Records

**SOP text:**
- *CAPA File Maintenance:* Maintain a CAPA file for each CAPA, including all related documents (NCR forms, investigation reports, action plans, verification records, effectiveness reviews).
- *Record Retention:* Retain CAPA files for a minimum of [X] years, or as required by regulatory standards.

**Skill behavior:**
- The Asana task is the CAPA file. All required artifacts attach as comments / attachments.
- Retention floor: 3 years post-batch-expiration (ISO 22716 cosmetic GMP). The SOP `[X]` placeholder is flagged for §7 revision on first run.
- Job 6 in SKILL.md.

## §6. Training

All employees involved in the CAPA process receive appropriate training on this SOP. Training records documented.

**Skill behavior:** out of scope. Training records belong to a future people-management surface, not capa-coordinator.

## §7. Review and Approval

This SOP should be reviewed annually and updated as necessary. All revisions must be approved by the QA Manager.

**Skill behavior:** the §7 revision queue is what `[SOP Revision Pending — quality-manager]` tasks feed into. Pre-v5.5, the tasks live in SJS CAPA Log; post-v5.5, quality-manager owns the SOP library and the queue.

## §8. Appendices

- **Appendix A:** Non-Conformance Report (NCR) Form — see `references/ncr-procedure.md` §3.2 for the intake field set.
- **Appendix B:** CAPA Investigation Template — see `references/capa-investigation.md`.
- **Appendix C:** Root Cause Analysis Tools (Fishbone Diagram, 5 Whys) — see `references/rca-tools.md`.

---

## Known SOP gaps (flagged on first run for §7 revision)

| Gap | Location | Skill workaround |
|---|---|---|
| ~~NCR procedure undefined as standalone~~ | §5.1, §5.2 | **CLOSED** 2026-05-09 — SKN-OPS-005 Rev.1 ratified (`references/ncr-procedure.md`) |
| NCR→CAPA escalation criteria absent | §5.2 | Severity bands in NCR Procedure §3.3 + decision branches in §4.2 |
| Effectiveness review window not specified | §5.5 | Severity-based defaults (Critical 90 / Major 60 / Minor 30) |
| Retention period placeholder `[X]` | §5.6 | ISO 22716 floor: 3 years post-batch-expiration |
| RCA tool selection criteria absent | §5.2 | Default rule: 5 Whys for single-event, Fishbone for systemic; operator can override |

These five gaps generate two `[SOP Revision Pending — quality-manager]` tasks on first-run setup (one for the NCR Procedure ratification, one bundling the four §5/§5.5/§5.6 in-text gaps).
