# SKN-OPS-002 — Serious Adverse Event (SAE) Reporting and Management

**Source:** SharePoint → `Sweet July/Product Development/Quality Control & Assurance/SOP/Serious Adverse Event (SAE) SOP SKN-OPS-002 Rev. 1.docx`
**Effective:** 2024-06-30
**Revision:** 1.0
**Prepared by:** Alvin Belt / Shirlene Loi
**Approved by:** Alvin Belt

This file mirrors the SOP for in-skill reference. The SharePoint version is canonical — always link operators back to source on any SAE walk.

## 1. Purpose

Establish a standardized process for the identification, documentation, investigation, and management of Serious Adverse Events (SAEs) associated with the use of skincare products.

## 2. Scope

All employees and contractors involved in the development, production, and monitoring of skincare products at Sweet July Beauty, LLC.

## 3. Definitions

- **Serious Adverse Event (SAE):** an adverse event resulting in death, life-threatening conditions, hospitalization, disability, or any significant health event requiring medical intervention.
- **Adverse Event (AE):** any undesirable experience associated with the use of a product that may or may not be serious.

## 4. Responsibilities

- **Quality Assurance (QA) or designee:** oversee the SAE reporting system, ensure compliance with this SOP, maintain SAE records.
- **Product Development Manager:** lead the investigation of SAEs, ensure appropriate actions are taken.
- **All Employees:** report any SAEs immediately to their supervisor or QA.

## 5. Procedure

### 5.1 Identification and Reporting

- Any employee identifying an SAE reports it immediately to their supervisor or QA.
- Complete an SAE Report Form, including details of the event, date, and responsible person.

**Skill action:** when an SAE is flagged from a complaint or direct intake, draft the SAE Report Form (Appendix A) using fields from the source task plus operator inputs. Stage the form, do not submit. HITL.

### 5.2 Documentation

- Ensure all relevant information is accurately documented on the SAE Report Form.
- Include product involved, description of the SAE, patient demographics (if applicable), medical treatment required.

**Skill action:** populate Asana task `[SAE Open]` in the SJ Skin Complaint Log with the form draft as a comment. Cross-link the source complaint task.

### 5.3 Initial Assessment

- QA reviews the SAE Report Form to determine severity and potential impact.
- If necessary, initiate immediate corrective actions to mitigate further risk.

**Skill action:** surface the SOP fields the operator must decide. The SOP does not define a formal severity matrix — severity is the operator's judgment call. The skill presents the event details and asks for the call. HITL on every triage decision.

### 5.4 Investigation

- Form an investigation team including the Product Safety Officer and relevant personnel.
- Conduct a thorough investigation to identify the root cause.
- Use appropriate tools (Fishbone Diagram, 5 Whys per Appendix C). Document findings.

**Skill action:** stage the investigation team ask. Draft a CAPA brief for handoff to capa-coordinator (v5.2) once root cause is identified. Pre-v5.2, post the brief as a comment and add `[CAPA Pending — capa-coordinator]` task.

### 5.5 Corrective and Preventive Action Plan

- Develop corrective action to address root cause.
- Develop preventive action to prevent recurrence.
- Implement per defined plan. Monitor and document completion.

**Skill action:** drafts the CAPA plan structure for the operator and hands off. Tracking lives in capa-coordinator post-v5.2.

### 5.6 Communication and Reporting

- Internal: communicate findings and actions to relevant stakeholders.
- External: report to regulatory authorities in accordance with local regulations if required. Provide detailed reports as mandated.

**Skill action:** drafts internal stakeholder summary. For external reporting, cross-flag to regulatory-manager (System C, live) — drafts the reg flag and adds `[Reg Flag Pending — regulatory-manager]` task in SJS Quality Management. regulatory-manager Job 1 picks up, Operator confirms type, fans out to adverse-event-and-recall-reporter for MoCRA SAE filing per SKN-OPS-009.

### 5.7 Verification and Effectiveness

- QA verifies all actions completed as planned.
- Confirm corrective actions effectively addressed the root cause.
- Conduct effectiveness review. Document findings.

**Skill action:** schedules a follow-up task on the SAE close date for the operator to run the effectiveness review.

### 5.8 Documentation and Records

- Maintain a file for each SAE: SAE Report Forms, investigation reports, action plans, verification records, effectiveness reviews.
- Retain SAE files for a minimum of [duration TBD per regulatory standards].

**Skill action:** every SAE artifact attaches to the source Asana task and the linked PLM batch record (via plm-assistant). The Asana task is the index; PLM holds the linked records.

## 6. Training

All employees in the SAE process receive appropriate training on this SOP. Training records documented.

## 7. Review and Approval

SOP reviewed annually and updated as necessary. All revisions approved by the QA Manager.

## Appendices

- **A:** SAE Report Form
- **B:** SAE Investigation Template
- **C:** Root Cause Analysis Tools (Fishbone Diagram, 5 Whys)

Operators run the form templates directly from SharePoint. The skill does not maintain its own copies — it points operators to the canonical files.

## Content gap noted

The SOP does not define a formal severity triage tree at §5.3. The skill walks the SOP as written and surfaces the severity call as an operator decision. If the operator wants a triage tree added to the SOP, that's a CAPA-worthy SOP improvement and routes to the SOP owner — the skill does not paper over the gap with invented logic.
