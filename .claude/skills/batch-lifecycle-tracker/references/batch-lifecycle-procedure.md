# Batch Lifecycle Procedure — SKN-OPS-007 Rev.1

**SOP Number:** SKN-OPS-007
**Title:** Batch Lifecycle Procedure
**Effective Date:** May 8, 2026
**Revision Number:** 1.0
**Prepared by:** Alvin Belt (batch-lifecycle-tracker skill-side); QA Lead (procedural-side)
**Approved by:** Alvin Belt
**Status:** Ratified 2026-05-08. Drafted and ratified in-place during batch-lifecycle-tracker v5.4 build, same pattern as SKN-OPS-006. SharePoint master copy to be filed at `Sweet July/PD/Quality Control & Assurance/SOP/Batch Lifecycle Procedure SKN-OPS-007 Rev.1.docx`.

**Owner:** batch-lifecycle-tracker (skill-side); QA Lead (procedural-side, currently Perrine — technical QA/QC lead)
**Anchors:** SKN-OPS-001 Rev.1 (CAPA escalation, retention floor), SKN-OPS-006 Rev.1 (Lab Quality severity bands), capa-coordinator NCR Procedure §3.3 (severity bands kept aligned), ISO 11930 (PET applies only to water-containing emulsions)

---

## Why this exists

Batch state lives across PLM, Asana, and tribal memory. SKN-OPS-001 governs corrective action *after* a batch fails; SKN-OPS-006 governs lab classification *of* a result. Neither defines:

- The state machine a batch walks from production through expiration
- When and how to schedule in-market stability tests
- What evidence is required to release a held batch
- How near-expiry signals split between operational write-offs (inventory) and quality-side decisions (lifecycle)
- The handshake from pre-launch stability (asana-pd-manager) to in-market stability tracked here

Without this, hold reasons drift, releases happen on operator memory, stability tests slip silently, and the audit trail can't show who decided what when. This procedure closes those gaps.

---

## 1. Scope

Applies to every Sweet July Beauty, LLC finished-good batch from first commercial production through terminal state. Covers:

- Batch state ownership (Active → Hold → Released | Pulled | Expired)
- In-market stability scheduling and result tracking
- Hold and release decisions
- Near-expiry quality-side decisions
- Pre-launch → in-market transition handoff

Does not apply to:
- Pre-launch stability (asana-pd-manager Formula Development Tracker keeps)
- Batch creation at receipt (inventory-manager Job 2 keeps)
- On-hand quantity per batch (inventory-manager keeps)
- Expired write-offs (inventory-manager Job 7 keeps)
- Lab result classification (quality-lab-coordinator owns OOS/OOT severity bands and retest path)
- CAPA lifecycle (capa-coordinator)
- Customer complaint intake or trends (complaint-and-event-handler)
- Component-batch tracking (raw materials and packaging stay with purchasing-manager and inventory-manager)

---

## 2. Roles

| Role | Responsibility |
|---|---|
| **Operator** | Reviews transition handoffs, drafts hold/release records, surfaces near-expiry decisions, owns close. Currently Alvin Belt, VP of Operations, AC Brands. |
| **QA Lead** | Approves every hold, every release, and every CAPA-route decision. Currently Perrine (technical QA/QC lead). Same holder as capa-coordinator and quality-lab-coordinator QA Lead — the three System B skills share the gate. |
| **Voice of Customer** | Manages quality intake from the customer perspective. Advisor on complaint-trend holds and customer-driven CAPAs (in complaint-and-event-handler). Currently Nicole Iturbe (Senior Director, Consumer Strategy & Operations). |
| **Department Manager** | Owns containment within their domain when a hold opens. Resolved at hold opening based on Hold Reason. |

Names live in the runtime role map, not in this procedure. As the org evolves, role-holders change without re-issuing the SOP.

---

## 3. Batch state machine

Every batch sits in one of these states. Transitions are the audit-trail moments; this skill writes the Status field on every transition with the source signal that drove it.

```
                                         ┌──> Released ──> [retained for 3yr post-expiration]
                                         │
        Active <──> Hold/Release Review ──┼──> On Hold ──> Hold/Release Review ──> Released | Pulled
          │                                │
          v                                └──> CAPA route ──> [reopens at Hold Review on close]
        Watch
          │
          v
        Active OR Hold/Release Review (per re-review outcome)
          │
          v
        Expired (terminal — auto on PLM sj_expiration_date)
```

State definitions:

- **Active** — Healthy batch in distribution. Default state from transition (Job 1) until a signal moves it.
- **Stability Pending** — Stability test scheduled but result not yet returned. Active for distribution purposes; flagged for the calendar.
- **Hold/Release Review** — HITL gate. Awaiting QA Lead sign-off on either a hold being opened or a release being granted. Transient.
- **On Hold** — QA-Lead-approved hold in effect. Distribution stopped; investigation in progress.
- **Watch** — Flagged for monitoring, not held. Used for a single LF that didn't escalate, late-life pattern, or marginal evidence cases. Re-reviewed monthly.
- **Released** — Returned to distribution after a hold cleared, or held through to natural EOL. Terminal for the lifecycle work surface; record retained.
- **Pulled** — Removed from distribution before natural EOL. Triggers inventory-manager write-off conversation (separate path).
- **Expired** — PLM `sj_expiration_date` reached. Terminal. Auto-state from PLM read; inventory-manager writes the position adjustment.

---

## 4. Pre-launch → in-market transition (Job 1)

### 4.1 Trigger

The transition fires the first time both conditions hold for a SKU:
1. asana-pd-manager Formula Development Tracker has the SKU at `Signed Approvals`.
2. inventory-manager has created the first commercial batch in PLM (`batch_quantity` exceeds the SKU's sample threshold — default 100 units; QA Lead can tune per SKU).

### 4.2 What gets staged

The skill stages `[Transition to In-Market Stability — confirm] [SKU]` in Inbound Staging. Description holds:

- Source PD project name + URL
- First batch's PLM `batch_code` + `batch_quantity` + `supplier_production_date` + `sj_expiration_date`
- Formula type read from PLM (water-based / anhydrous / hybrid) — drives §F stability schedule
- Proposed in-market stability schedule generated from §F
- List of asana-pd-manager pre-launch tasks slated to close at transition

### 4.3 Operator approval

One-time approval per SKU per launch. On approval:
- The first batch's lifecycle task opens with Status = Active in `Batch — Active in Market`.
- Stability schedule subtasks generate per §F and land in `Batch — Stability Schedule`.
- PD-side pre-launch stability tasks close with sync-back comment naming this skill.
- Transition record posts as a pinned comment on the SKU's first batch task.

The transition is a one-time event per SKU. Subsequent batches for the same SKU enter directly at Active without going through Job 1 — inventory-manager creates them, this skill picks them up automatically.

### 4.4 Edge cases

- **PD never reached Signed Approvals.** No transition fires. Batch sits without a lifecycle task; surface to Operator as an exception.
- **Sample-threshold ambiguity.** If `batch_quantity` is between 100 and 500 units, surface to QA Lead for the Operator confirm step. Default 100 is the floor.
- **SKU launches multiple variants from one PD project.** Each variant transitions independently per its own first batch.

---

## 5. Stability scheduling (Job 3)

### 5.1 Cadence by formula type — anchored in ISO 11930

| Formula type | Examples | Cadence |
|---|---|---|
| Water-based emulsion | Toner, serum, cream, lotion | PET at launch, PET-EOL, accelerated stability at 3 months, real-time stability annually |
| Anhydrous | Balm, oil, lip oil, lip balm, body oil | Real-time stability annually only — no PET (no preservative system to test) |
| Hybrid (W/O, O/W with low water, lip treatments with water content) | Some lip treatments, certain salves | Anhydrous schedule + microbial spot-check at launch |

### 5.2 Per-batch vs every-other-batch

First commercial batch and re-runs on each new batch by default. Once a SKU has 3 consecutive batches that all passed clean (PET launch, PET-EOL where applicable, accelerated, real-time annual), the schedule shifts to **every other batch** at QA Lead discretion. Any fail re-tightens to per-batch.

### 5.3 Subtask generation

At batch creation (Job 1 for first batch; auto-fire for subsequent), the skill generates stability subtasks per the SKU's cadence. Each subtask carries:

- Test type (PET-launch, PET-EOL, Accelerated-3mo, Real-time-annual, Microbial-spot-check)
- Due date (computed from `supplier_production_date` + cadence offset)
- Dispatch destination (contract lab — captured per SKU at QA Lead config)
- Result-receipt evidence requirement (test report, COA-style summary, raw data)

### 5.4 Result handling

- **Pass:** Operator (or skill, on contract-lab return) marks subtask complete + logs result in batch task comment thread. No HITL gate on a pass.
- **Fail:** Routes through quality-lab-coordinator (single door for lab signal). quality-lab-coordinator classifies, runs retest path if warranted, and posts `[Batch Hold Request — batch-lifecycle-tracker]` if the result warrants a hold. No batch-lifecycle direct lab-record reads.

---

## 6. Hold and release decisions (Job 4)

### 6.1 Hold review checklist

Before drafting a hold record, the Operator confirms:

1. Is the source signal documented? (Lab finding, complaint trend, vendor signal, regulatory observation, internal flag — must trace to a documented source.)
2. Is the severity classification consistent with the source? Lab severity → SKN-OPS-006 §3.4 bands. Complaint trend severity → complaint-and-event-handler thresholds.
3. What's the containment scope? (Whole batch, single distribution lane, specific retailer, specific channel.)
4. Has the affected position been identified? (Pull from inventory-manager via plm-assistant — on-hand by location, in-transit, allocated to retailer POs.)
5. Is there an existing hold or open CAPA covering this issue? Don't double-hold.

### 6.2 Hold draft fields

| Field | Notes |
|---|---|
| Hold Reason | Lab fail / Complaint trend / Vendor signal / Regulatory observation / Internal flag / Other |
| Source | Originating skill or task — quality-lab-coordinator LF, complaint-and-event-handler complaint task, etc. |
| Severity | Critical / Major / Minor — aligned with NCR Procedure §3.3 |
| Containment scope | Whole batch / specific lane / retailer / channel |
| Affected position | On-hand by location, in-transit, allocated — read from PLM at hold time |
| Date of hold | ISO date |
| Approving QA Lead | Captured at sign-off — role + name + timestamp |

### 6.3 Release review checklist

Before drafting a release, the Operator confirms:

1. Is the underlying issue resolved? (CAPA closed Effective, retest passed clean, complaint pattern broken, regulatory observation resolved.)
2. Is there evidence the issue won't recur on this batch specifically? (Effectiveness window passed, leading indicators clean.)
3. Is the original Hold Reason still valid as the only release barrier, or have new signals added since the hold?
4. Are downstream notifications staged? (Retailer comms if any retail position was affected; inventory-manager updates if position handling changes.)

### 6.4 Release draft fields

| Field | Notes |
|---|---|
| Release rationale | 2–3 sentences tying release to evidence |
| Resolution path | CAPA closed Effective / Clean retest / Pattern broken / Other |
| Evidence | CAPA closeout link, retest result, complaint-trend resolution comment, etc. |
| Downstream notifications | Retailer comms, inventory updates, internal stakeholder list |
| Approving QA Lead | Captured at sign-off — role + name + timestamp |

### 6.5 HITL gates

**QA Lead approves every hold and every release.** No exceptions at v5.4. Operator can stage; QA Lead approval is the commit step. If the QA Lead role-holder needs to change for a specific decision, update `references/role-map.md` first.

---

## 7. Near-expiry quality-side decisions (Job 5)

### 7.1 Cross-post handshake with inventory-manager

inventory-manager Job 6 surfaces near-expiry at 90/60/30-day thresholds in its operational queue. For each threshold task, inventory cross-posts (multi-homes the task to SJS Quality Management) so the quality-side conversation happens here. Inventory keeps the operational write-off action because it's a position-changing PLM write that belongs in their ledger.

### 7.2 Decision tree by threshold

**90-day threshold** — typically a routine note, no action required.
- Skill comments back on the inventory task: "Quality call: continue to release. PET-EOL scheduled for [date]."
- No HITL.

**60-day threshold** — confirm late-life PET-EOL is scheduled or completed (water-based) or that real-time annual is current (anhydrous).
- If scheduled and on-track: comment back "Quality call: continue to release."
- If not scheduled: Operator stages the missing test in `Batch — Stability Schedule`.
- HITL: Operator approves any added test.

**30-day threshold** — confirm pull plan or expedite EOL.
- Default: pull plan. The skill drafts a pull recommendation citing remaining on-hand position.
- Alternative: expedite EOL with a final stability test if shelf-life math allows.
- HITL: Operator approves the quality-side decision. Decision posts back to inventory-manager so they have the quality call before any write-off.

### 7.3 Past-expiration

When PLM `sj_expiration_date` <= today, the batch's Status auto-flips to Expired and the lifecycle task moves to `Batch — Closed`. inventory-manager handles the position write-off in their ledger. This skill closes its lifecycle task with a closeout summary; no quality-side decision needed at this point because the call was made at the 30-day threshold (or earlier).

---

## 8. CAPA handoff (Job 6)

For batch fails that need root cause work:

- Repeat OOS or OOT on the same SKU + spec within 12 months
- Multi-batch pattern (2+ batches with the same fail signature)
- Regulatory observation against a batch
- Critical-severity lab fail by default

The skill composes NCR intake context per capa-coordinator's NCR Procedure §3.2 and creates an inbound task in SJS CAPA Log. Operator approves the handoff stage. capa-coordinator runs its own intake HITL on receipt.

The originating batch task moves to `Batch — On Hold` (Status = On Hold) until the CAPA closes. CAPA close re-routes the batch to Hold/Release Review for the release decision per §6.3.

---

## 9. Closeout and retention

Every batch task closes when terminal state is reached.

### 9.1 Documentation

The batch task holds (via comments and attachments):
- Transition record (Job 1, pinned comment)
- Stability schedule + each result + each subtask
- Every hold rationale + approving QA Lead + timestamp
- Every release rationale + approving QA Lead + timestamp
- Near-expiry decisions per threshold
- CAPA links if any
- Closeout summary (terminal-state comment)

### 9.2 Retention

3 years post-batch-expiration per SKN-OPS-001 §5.6 and ISO 22716 cosmetic GMP. Asana task stays in `Batch — Closed`; PLM batch record is the source-of-truth registry.

### 9.3 Closeout summary format

```
Batch [batch_code] — [SKU] closeout (YYYY-MM-DD):
- Lifecycle highlights: [holds, stability passes/fails, watch-list periods]
- Terminal state: Released | Pulled | Expired
- Reason: [for Pulled — pull rationale; for Released — natural EOL; for Expired — PLM auto]
- Retention end: [sj_expiration_date + 3 years]
```

---

## 10. SLAs

| Action | SLA |
|---|---|
| Transition handoff stage (Job 1) | 2 business days from trigger |
| Stability subtask dispatch reminder | 5 business days before due |
| Hold review (Job 4) | 1 business day for Critical, 3 for Major, 5 for Minor |
| Release review (Job 4) | 3 business days from evidence-complete |
| Near-expiry 30-day decision (Job 5) | 5 business days from cross-post |
| CAPA handoff stage (Job 6) | Critical within 5 business days, Major within 10, Minor within 15 |
| Closeout (Job 7) | 5 business days from terminal state |

---

## 11. Revision history

| Revision | Date | Notes |
|---|---|---|
| 1.0 | 2026-05-08 | Initial ratification. Drafted and ratified in-place during batch-lifecycle-tracker v5.4 build. SOP & Form Log entry to be added at SharePoint filing. |

Annual review per SKN-OPS-001 §7 pattern. All revisions approved by the QA Manager.

---

## 12. Known content gaps (flagged for §7 revision queue)

| Gap | Section | Skill workaround |
|---|---|---|
| Sample threshold for "first commercial batch" | §4.1 | Default 100 units; QA Lead can tune per SKU at ratification |
| Contract lab destinations per SKU | §5.3 | Captured per SKU at QA Lead config; default to current Sweet July contract lab |
| Every-other-batch shift criteria | §5.2 | Default 3 consecutive clean batches; QA Lead can tighten or loosen |
| 30-day pull-vs-EOL default | §7.2 | Default to pull plan; QA Lead can flip to EOL-default per SKU |
| Voice of Customer gate scope | §2 | Customer-quality intake gates owned in complaint-and-event-handler; Nicole advises on complaint-trend holds. Specific gate scope refined at next revision. |

These gaps do not block intake. They get bundled into the SOP revision task on first run.
