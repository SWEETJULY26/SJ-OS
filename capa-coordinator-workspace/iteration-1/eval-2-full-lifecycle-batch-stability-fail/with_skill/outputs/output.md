# CAPA Full Lifecycle Walkthrough (DRAFT — no Asana writes made)

**Source signal:** `[CAPA Request — batch-lifecycle-tracker]` Soursop Vit C Lot 25-09 — 3-month accelerated stability fail on Vitamin C assay (89% of label claim, spec ≥95%)
**Why this is urgent:** batch is active in market at Ulta and DTC. Everything below is staged for your review per SKN-OPS-001, walked phase by phase. Nothing commits until you say go.

**Immediate flag, outside CAPA's lane:** the in-market exposure means two decisions need to happen today, in parallel with CAPA intake, and neither belongs to this skill:
- **Hold/release on Lot 25-09** — batch-lifecycle-tracker's call (SKN-OPS-007), not CAPA's. CAPA receives the fail signal; it doesn't decide whether the batch gets pulled or held.
- **Recall scoping** — if this is assessed as a labeling/potency violation on product already sold, complaint-and-event-handler owns recall trigger and SAE/reportability screening (SKN-OPS-002/003). CAPA's containment field captures whatever's been done, but the recall call itself sits with that skill.

Both should be running now, independent of the CAPA clock below. I'll draft the cross-flags in Phase 6 for when this closes, but flagging here so it's not read as CAPA "handling" the batch or the recall.

---

## Phase 1 — NCR Open (SKN-OPS-001 §5.1, SKN-OPS-005 §3)

**Produces:** a drafted NCR record, staged for Operator approval. On approval, the skill assigns `NCR-2026-0NN` (exact number set at the highest existing 2026 NCR + 1, checked at write time), creates the task in **NCR Open**, and writes these fields:

| Field | Draft value |
|---|---|
| NCR number | NCR-2026-0NN *(assigned on approval)* |
| Date opened | 2026-07-21 |
| Reporter | batch-lifecycle-tracker (system handoff) |
| Source | lab-OOS |
| Category | Product |
| SKU(s) affected | Soursop Vit C [serum/SKU code — confirm exact SKU via plm-assistant] |
| Batch / lot code | 25-09 (linked PLM batch record) |
| Vendor | TBD — pulled from batch BOM via plm-assistant once formulation/packaging suppliers are confirmed as in-scope for RCA |
| Description | 3-month accelerated stability pull on Lot 25-09 returned a Vitamin C assay result of 89% of label claim against a ≥95% spec. Batch is active in market (Ulta, DTC). |
| Evidence | Accelerated stability test report (3-month timepoint) — link pending from batch-lifecycle-tracker/lab |
| Suspected severity | **Critical** — see rationale below |
| Containment action taken | Pending confirmation from batch-lifecycle-tracker: has the batch been held? This field cannot close as "none yet" given in-market exposure — flagging for immediate operator follow-up alongside NCR approval |

**Severity rationale (SKN-OPS-005 §3.3):** Critical band triggers include direct safety/label-claim exposure and recall risk. An 89%-of-claim potency result on a product already at retail and DTC is exactly this — a label claim failure with recall exposure, not a contained lab miss. Reads should err high per §3.3; this reads Critical.

**HITL — Operator approves intake.** Approval assigns the NCR number, creates the task, and moves it to NCR Open. *(Not yet approved — awaiting your go-ahead.)*

---

## Phase 2 — NCR Review and Escalation Decision (SKN-OPS-001 §5.2, SKN-OPS-005 §4)

**Produces:** a drafted review + decision record.

**§4.1 checklist walk:**
1. *Description specific enough?* Yes — assay result, spec, timepoint, and market exposure are all stated.
2. *Severity consistent with §3.3?* Yes, Critical confirmed above.
3. *Existing open CAPA on this root cause?* Unconfirmed — recommend a check against open CAPAs tagged Source = lab-OOS or Category = Product for Soursop Vit C or related Vitamin C SKUs before opening a new file, to catch a duplicate or a pattern.
4. *Pattern across recent NCRs?* Recommend pulling the Soursop Vit C SKU wiki page and any prior stability NCRs on this SKU or formulation family before RCA — if this is a second stability miss, it changes the RCA tool choice (see Phase 3).
5. *Containment confirmed?* No — outstanding per Phase 1. This should not sit waiting on CAPA process; flagging again for immediate parallel action.

**Decision: Convert to CAPA.** Required for Critical per §4.2(A) — assign `CAPA-2026-0NN`, linked to `NCR-2026-0NN`.

**SLA:** Critical NCR→CAPA conversion required within 5 business days of NCR open (2026-07-21) — target conversion by **2026-07-28**.

**HITL — two gates here:**
- Operator approves the review decision (convert vs. close vs. hold) — drafted above as convert.
- **QA Lead (Perrine) approves the NCR→CAPA conversion** — `Gate = Pending QA Lead` on the task until she signs off. This is the audit-trail gate SKN-OPS-005 exists to protect.

---

## Phase 3 — CAPA Opening, Team Formation, Root Cause Analysis (SKN-OPS-001 §5.2)

**Produces:** the CAPA cover block, a proposed investigation team, and the RCA artifact (tool walk + root cause statement).

### CAPA cover block (draft)

```
CAPA Number: CAPA-2026-0NN
Linked NCR: NCR-2026-0NN
Date opened: 2026-07-21 (pending conversion approval)
Severity: Critical
Source: lab-OOS
Category: Product

Linked records:
- Batch: Lot 25-09, Soursop Vit C [PLM batch ID — pull via plm-assistant]
- Vendor: TBD pending BOM pull
- SKU: Soursop Vit C [SKU code — pull via plm-assistant]
- Source task: [CAPA Request — batch-lifecycle-tracker] Asana gid — pending

Investigation team: [see below]

Statement of non-conformance: Lot 25-09 of Soursop Vit C failed its 3-month
accelerated stability pull on Vitamin C assay, returning 89% of label claim
against a ≥95% spec. Batch is active in market at Ulta and DTC.
```

### Proposed investigation team

Vitamin C potency loss under accelerated stability is a formulation/packaging/process question first, vendor question second (unless a raw material or component defect surfaces). Draft team:

- **QA Lead (Perrine)** — Lead
- **PD/Formulation** — owns the antioxidant system and stability protocol design for this SKU
- **Purchasing** — pulled in if the RCA implicates the ascorbic-acid raw material lot or the packaging vendor's oxygen barrier spec
- **Operator (you)** — oversight, cross-functional unblock

*HITL — Operator confirms team composition before RCA work starts.*

### Root cause analysis — recommended tool: **Fishbone, followed by 5 Whys on the strongest branch**

Per `references/rca-tools.md`'s default selection rule: single-event/single-chain issues get 5 Whys; systemic or multi-factor issues get Fishbone first. A Vitamin C potency failure at 3 months can trace to several independent or interacting causes — antioxidant system robustness, packaging oxygen ingress, fill-process air exposure, storage/handling deviation, or an analytical method issue at the lab. That's multi-factor by nature, so Fishbone for breadth, then 5 Whys on whichever branch reads strongest, matches the tool's own guidance for exactly this shape of failure.

**Fishbone scaffold (prompts only — team fills in):**

| Category | Prompt |
|---|---|
| Manpower | Who ran the fill, and who logged the stability pull? Any training gaps on handling ascorbic-acid-based formulas? |
| Method | Was the accelerated stability protocol (temp/humidity/duration) correct for this formulation? Was fill-line SOP followed without deviation? |
| Machine | Any equipment issue at fill — dosing accuracy, headspace/air exposure, capping torque affecting seal integrity? |
| Material | Was the ascorbic acid / antioxidant raw material within spec and from the expected lot/vendor? Any change in raw material sourcing before this batch? |
| Measurement | Was the assay method validated and consistent with prior batches? Any change in analytical method or lab? |
| Environment | Any deviation in batch's storage conditions pre-stability-pull? Any packaging change (jar/bottle, liner) that altered the oxygen barrier? |

Once populated, identify the strongest branch and cross-category links, then run 5 Whys on that branch per the standard prompt structure (Why 1 → Why 5, stop at a process/system-level answer, not "human error" or a name).

**Root cause statement:** *not drafted — this is where the team's actual investigation goes. The skill will not invent a root cause.* Placeholder field, populated once the team completes the walk.

**HITL — two gates:**
- Operator approves the team.
- **QA Lead approves the final root cause statement** — `Gate = Pending QA Lead`. This can't be signed off until the Fishbone/5-Whys work is actually done; nothing here is pre-filled.

---

## Phase 4 — Corrective and Preventive Action Plans (SKN-OPS-001 §5.3)

**Produces:** two action-plan tables, both tied to whatever root cause statement clears Phase 3. Drafted here as placeholder structure — real actions can't be written until root cause is approved.

### Corrective Action Plan (draft structure)

| # | Action | Owner | Due | Evidence required | Status |
|---|---|---|---|---|---|
| C1 | [e.g., re-test remaining Lot 25-09 retain samples for confirmation; assess whether other in-market lots of this SKU are at risk] | QA Lead | TBD | Retest results | Open |
| C2 | [e.g., correct the identified process/formulation gap for future batches of this SKU] | PD/Formulation | TBD | Updated batch record / revised spec | Open |

### Preventive Action Plan (draft structure)

| # | Action | Owner | Due | Evidence required | SOP impact | Status |
|---|---|---|---|---|---|---|
| P1 | [e.g., if root cause is protocol-related — revise accelerated stability protocol for antioxidant-system SKUs] | QA Lead | TBD | Revised protocol doc | Likely SOP-NNN revision | Open |
| P2 | [e.g., if root cause is packaging-related — tighten incoming oxygen-barrier verification for this component] | Purchasing | TBD | Updated incoming inspection checklist | Possible SOP revision | Open |

Any preventive action landing on "SOP-NNN revision" or "New SOP" auto-stages a `[SOP Revision Pending — quality-manager]` task carrying the proposed change — this fires automatically once P-actions are finalized, no separate approval needed for the staging itself (the SOP change still goes through quality-manager's ratification cycle).

**HITL — Operator approves both plans** once root cause is in hand and actions are filled in for real.

---

## Phase 5 — Implementation Tracking, Verification, Effectiveness Review (SKN-OPS-001 §5.4–§5.5)

**Implementation tracking (read-only):** as C1/C2/P1/P2 owners post completion with evidence attached, the skill keeps the status table current and pings on overdue — 1 day overdue: owner ping; 5 days: owner + Operator; 10 days: escalates to QA Lead via `[Pending QA Lead — Overdue Action]`. No HITL gate here — informational only.

**Verification record (drafted once all actions report complete):**

```
Verification — CAPA-2026-0NN — [date]
C1: [completion date] — [verifier] — [evidence link] — Verified ✓ / Not verified
C2: [completion date] — [verifier] — [evidence link] — Verified ✓ / Not verified
P1: [completion date] — [verifier] — [evidence link] — Verified ✓ / Not verified
P2: [completion date] — [verifier] — [evidence link] — Verified ✓ / Not verified

All actions completed as planned: [Yes/No]
Verifier: QA Lead (Perrine)
```

**HITL — QA Lead approves verification** (`Gate = Pending QA Lead`). Verification answers "did the actions happen," not "did it work."

**Effectiveness review — window and what it checks:**

Severity is Critical, so the effectiveness window is **90 days from last action completion** — the longest window on the books, appropriate given this is an in-market potency failure. Drafted structure:

```
Effectiveness Review — CAPA-2026-0NN — [date, 90 days post last action completion]

Original root cause statement: [pulled from Phase 3]
Effectiveness window: 90 days (Critical)

Leading indicators reviewed:
- Next production batch(es) of Soursop Vit C — 3-month accelerated stability
  assay result, pulled via plm-assistant
- Any near-expiry or routine stability checks on remaining in-market Lot 25-09
  units, if not fully pulled
- Confirmation the SOP/process change (if any) is actually in use on the
  production floor — not just documented

Recurrence check: has the same non-conformance (Vitamin C assay below spec at
accelerated stability) recurred on any batch since the corrective action
completed? Yes/No

Effectiveness verdict: Effective / Partially effective / Not effective
Reviewer: QA Lead (Perrine)
```

If the verdict comes back Partially or Not effective, the CAPA does **not** close — it reopens at Investigation (Phase 3) with the failed-effectiveness result logged as new evidence, and the cycle runs again.

**HITL — QA Lead approves the effectiveness verdict** (`Gate = Pending QA Lead`).

---

## Phase 6 — Closeout, Documentation, Handoffs (SKN-OPS-001 §5.6)

**Only reachable once verification AND effectiveness both clear.** Produces:

**Closeout summary (4-line, drafted at close):**

```
CAPA-2026-0NN closeout ([date]):
- Source event: Lot 25-09 Soursop Vit C — 3-month accelerated stability fail,
  Vitamin C assay 89% vs. ≥95% spec
- Root cause: [from Phase 3]
- Actions taken: [from Phase 4, corrective + preventive]
- Effectiveness verdict: Effective — [evidence summary]
```

**Documentation check:** confirms every required artifact is attached before staging close — NCR record, RCA thread, action plans, verification record, effectiveness review. Retention: 3 years post-batch-expiration.

**Handoffs that fire on close — all four checked for applicability:**

- **6a. Close-the-loop on the originating record.** Comment on the source `[CAPA Request — batch-lifecycle-tracker]` task with the closeout summary and CAPA number, so batch-lifecycle-tracker sees the loop closed on Lot 25-09. *Applies — always fires here since the source is a batch-lifecycle-tracker handoff.*
- **6b. SOP revision feed.** If any P-action came out of Phase 4 tagged SOP-NNN revision or New SOP, a `[SOP Revision Pending — quality-manager]` task carries the proposed change into the ratification queue. *Likely applies* — a stability protocol or incoming-spec change is a plausible outcome of this RCA.
- **6c. Vendor scorecard signal.** Only fires if Source resolves to vendor-receipt or vendor-systemic. Current Source is lab-OOS; this fires only if the RCA implicates a specific raw-material or packaging vendor as root cause. *Conditional — depends on Phase 3 findings.*
- **6d. Regulatory feed.** A potency/label-claim failure on in-market product is a plausible reportability trigger — cosmetic GMP deviation, and depending on recall outcome, a filing obligation. Pre-v6, this stages as `[Reg Flag Pending — regulatory-manager]` inside SJS CAPA Log rather than a live handoff. *Recommend flagging as applicable* given the market exposure, for the Operator/QA Lead to confirm at close.

Also worth restating: **this closeout does not stand in for the recall/SAE decision.** If complaint-and-event-handler's recall or SAE process is still open when this CAPA is ready to close, the closeout comment lets them know CAPA is done, but the recall/reportability call runs on its own track and its own approvals.

**HITL — QA Lead approves the close.** On approval: all four handoffs (as applicable) commit, Status → Closed, Gate → Open, task moves to the Closed section.

---

## Summary — gate map

| Phase | Operator gate | QA Lead gate |
|---|---|---|
| 1. NCR intake | Approve intake | — |
| 2. NCR review/escalation | Approve decision | Approve NCR→CAPA conversion |
| 3. CAPA open/RCA | Approve team | Approve root cause statement |
| 4. Action plan | Approve corrective + preventive plans | — |
| 5. Implementation | (read-only, no gate) | Approve verification; approve effectiveness verdict |
| 6. Closeout | — | Approve close |

Role-holders: Operator = Alvin Belt. QA Lead = Perrine.

## What's staged vs. what's real right now

Nothing above has been written to Asana. No NCR or CAPA number has actually been assigned — those get pulled from the live highest-existing-number check at first real write. No fields, comments, or handoff tasks have been created. This is the complete walkthrough for review; say go and Phase 1 intake goes live first, with the containment/hold question surfaced to batch-lifecycle-tracker in parallel, not gated behind CAPA's clock.
