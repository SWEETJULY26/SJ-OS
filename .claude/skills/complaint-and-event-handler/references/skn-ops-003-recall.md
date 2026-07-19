# SKN-OPS-003 — Product Recall Procedure

**Source:** SharePoint → `Sweet July/Product Development/Quality Control & Assurance/SOP/Product Recall Standard Operating Procedure (SOP) SKN-OPS-003 Rev. 1.docx`
**Effective:** 2024-06-30
**Revision:** 1.0
**Prepared by:** Alvin Belt
**Approved by:** Alvin Belt

This file mirrors the SOP for in-skill reference. The SharePoint version is canonical — always link operators back to source on any recall walk.

## 1. Purpose

Establish a process for recalling skincare products in case of a quality issue or safety concern.

## 2. Scope

All employees responsible for the recall of skincare products manufactured by Sweet July Beauty, LLC, including the Quality Control Team, Production Team, and Customer Service Team.

## 3. Responsibilities

- **A. Quality Control Team:** identify the issue requiring a recall, determine scope, identify affected batches.
- **B. Production Team:** identify root cause, take corrective and preventive actions to prevent recurrence.
- **C. Customer Service Team:** notify customers, coordinate the return of affected products.
- **D. Management Team:** oversee the recall process, review corrective and preventive actions, ensure appropriate actions taken.

## 4. Recall Process

### 4.A — Identify the Issue

Quality Control Team identifies the issue requiring recall (quality issues, safety concerns).

**Skill action:** the recall is never auto-initiated. The skill triggers only on the explicit kickoff phrase ("trigger a recall on …"). When invoked, it pulls the affected SKU and batch from the kickoff phrase, surfaces all complaints linked to that SKU/batch from the SJ Skin Complaint Log, and pulls batch context from PLM via plm-assistant. HITL: operator confirms the issue summary before proceeding to §4.B.

### 4.B — Scope of Recall

Quality Control Team determines scope: affected batches, distribution channels, customer information.

**Skill action:** drafts the scope from PLM batch records (units produced, distribution split by channel, customer order list via plm-assistant + oc3pl-order-manager). Surfaces to operator. HITL: operator confirms scope or expands/narrows it before proceeding.

### 4.C — Notification

Customer Service Team notifies customers via email, phone, or letter, depending on severity. Notification includes return instructions and refund/replacement options.

**Skill action:** drafts customer notification in three forms (email, phone script, letter) using sweet-july-skin-brand for tone. Drafts an internal cross-functional ask list — Customer Service Team owns send, Operations owns retail partner notifications, Regulatory owns external authority notifications. HITL: operator approves each draft before sending. The skill never sends customer comms — drafts only.

### 4.D — Return and Disposal of Affected Products

Customer Service Team coordinates return and disposal per applicable laws and regulations.

**Skill action:** drafts return instructions, return shipping label process (handoff to oc3pl-order-manager), and disposal documentation requirements. HITL on every step.

### 4.E — Corrective and Preventive Actions

Production Team identifies root cause, takes corrective and preventive actions to prevent recurrence. Actions documented, timelines established.

**Skill action:** opens a CAPA brief and hands off to capa-coordinator (v5.2). Pre-v5.2, drafts the brief and adds `[CAPA Pending — capa-coordinator]` task to the SJ Skin Complaint Log so the operator can hand off manually.

### 4.F — Follow-up

Customer Service Team follows up with customers to confirm products returned and issues resolved.

**Skill action:** schedules follow-up tasks for Customer Service in the SJ Skin Complaint Log. Tracks resolution rate. Surfaces unresolved items in trend analysis.

## 5. Documentation

All recall-related documents (customer notification, return and disposal records, corrective and preventive actions) documented and maintained in a recall log.

**Skill action:** every recall artifact attaches to the source Asana task `[Recall Open]` and to the affected batch record in PLM via plm-assistant. The Asana task is the index.

## 6. Training

All employees in the recall process receive training on this SOP and understand their roles.

## 7. Review

SOP reviewed and updated annually or as needed.

## 8. Communication

SOP communicated to all employees in the recall process. Updates communicated promptly.

## 9. Record Retention

All recall records retained for a minimum of 5 years or per company policy.

## Skill operating notes

- **Kickoff phrase is non-negotiable.** Any pattern in trend analysis or SAE escalation that *suggests* a recall surfaces the question to the operator. The recall does not start until the operator says "trigger a recall on …" with a specific SKU or batch.
- **Step-by-step approval is non-negotiable.** Each of §4.A through §4.F is a separate HITL gate. The skill drafts and stages; the operator approves.
- **Customer comms are never auto-sent.** sweet-july-skin-brand-styled drafts only.
- **Cross-functional ask list is mandatory output.** Every recall produces a list with named owners (CS, Ops, Regulatory, Production). The skill won't pretend it can drive cross-functional execution — it surfaces the asks and lets the operator drive.
