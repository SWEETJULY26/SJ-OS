---
sop_id: SKN-OPS-011
title: Formula Development Stage-Gate & IL Review Gate Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Formula Development Stage-Gate & IL Review Gate Procedure

## 1. Purpose

Define the five stages every Sweet July Skin formula moves through from intake to launch readiness, and the hard regulatory gate — ingredient list (IL) review — that sits on top of the approval stage. Without a documented gate, a formula could reach sign-off and start finalizing artwork before Pedrero has confirmed the ingredient list, which is the exposure this procedure closes.

## 2. Scope

Applies to every formula tracked in the Formula Development Tracker, from first submission through Signed Approvals, Revisions Required, or Rejected. Covers the stage-gate workflow itself and the IL Review Gate handoff it triggers. Does not cover the regulatory review's substance — the IL packet contents, Pedrero correspondence, and label/claim work are owned by SKN-OPS-008 (IL / Claims / Label Procedure); this procedure owns the trigger, not the review.

## 3. Definitions

- **Stage** — one of five conceptual states a formula occupies: Intake/Concept, In Review, Signed Approvals, Revisions Required, Rejected. "Signed Approvals" is a conceptual name driven by a review/approval field being set to Approved, not a literal section — the underlying workspace section is named differently and can change without changing this procedure.
- **IL Status** — a formula-level field tracking where the ingredient list stands in regulatory review: Not Yet Triggered, Pending IL Review, In IL Review, IL Approved, IL Returned for Reformulation, IL Reformulated — Re-review Required.
- **IL Review Gate** — the hard hold at Signed Approvals: a formula does not proceed to artwork finalization until IL Status reaches IL Approved.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operator** | Confirms every stage move with stage name, task name, and reason before executing. Confirms the IL Review Gate handoff as a single atomic action. |
| **Technical Advisor** | Technical sign-off on formula stage moves — compatibility, stability, RIPT, PET judgment calls that inform whether a formula is ready to move. |
| **PD Consult + Quality Gate** | Strategy and consumer-side consult on PD decisions; final quality check on PD documentation once a formula clears a stage. |
| **Approver — President** | Approves direction-changing PD decisions (launch scope, supplier change, kill calls) that surface at a stage move. |
| **Approver — Founder** | Founder-level approval on brand-line moves surfaced through PD signal. |

## 5. Procedure

### 5.1 The five stages

| Stage | Meaning |
|---|---|
| Intake / Concept | Formula submitted, not yet in active review |
| In Review | Under evaluation — color match, texture, stability, sampling, final review; may span several working sections, all treated as pre-approval |
| Signed Approvals | Formula approved and signed off, driven by the review/approval field being set to Approved |
| Revisions Required | Sent back for reformulation or adjustment |
| Rejected | Not moving forward |

### 5.2 Stage move rules

Every stage move is confirmed before executing, naming the stage, the task, and the reason.

- Moving to **Revisions Required** — offer to log a comment explaining what revisions are needed.
- Moving to **Rejected** — offer to log the rejection reason as a comment.
- Moving **backward** (Signed Approvals → In Review, or similar) — flag as unusual and confirm intent explicitly before proceeding; a backward move is never routine.
- Moving to **Signed Approvals** — fire the IL Review Gate every time, no exceptions.

### 5.3 IL Review Gate trigger

When a formula reaches Signed Approvals, the following happens as one confirmed action:

1. **Dedup check first.** Before creating anything, check for an existing regulatory review task on the same SKU. If one already exists — most commonly on a re-approval after revision — surface it and confirm whether to link or update it instead of opening a duplicate.
2. Set IL Status to **Pending IL Review** on the formula record.
3. Open a regulatory intake task, only if step 1 found nothing existing.
4. Place the new task in regulatory intake staging.
5. Record the artifact type as IL Review and the linked SKU (code and name).
6. Link the new task back to the originating formula record.

### 5.4 Hold rule

The launch flow holds at Signed Approvals until IL Status reaches **IL Approved**. Component and carton artwork finalization is gated on that flip — it does not proceed on a formula sign-off alone.

### 5.5 Reformulation rule

If a SKU reformulates after a prior IL approval, IL Status resets to **IL Reformulated — Re-review Required**, and the gate re-fires when the reformulated version reaches Signed Approvals again.

### 5.6 Scope boundary

This procedure only fires the gate and stages the regulatory intake — it never drafts IL packet contents and never sends anything to the external regulatory partner directly. That substantive review is SKN-OPS-008's domain end to end.

## 6. Records

| Record | Where it lives |
|---|---|
| Stage state | Formula Development Tracker task, one per formula |
| IL Status | Formula-level field, drives the gate |
| Regulatory intake task | Regulatory management queue, linked back to the formula task |
| Gate resolution (approved / returned / reformulated) | Sync-back comment on the formula task from the regulatory side |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from the working stage-gate procedure already governing asana-pd-manager. | Alvin Belt |
