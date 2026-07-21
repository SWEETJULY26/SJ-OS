# NCR Draft — HCT Cap Receipt, Single-Unit Crack (DRAFT ONLY — not written to Asana)

Per your instruction, nothing below has been committed to Asana. This is the drafted record and the escalation walk-through for your (Operator) review. Numbering shown as placeholder pending an Asana check for the current NCR sequence — confirm before commit.

## 1. NCR record (draft)

| Field | Value |
|---|---|
| NCR number | `NCR-2026-0XX` *(placeholder — assign on approval after checking highest existing NCR-2026 number in SJS CAPA Log)* |
| Date opened | 2026-07-21 |
| Reporter | Receiving inspector (name TBD — fill in who caught it) |
| Source | vendor-receipt |
| Category | Vendor |
| SKU(s) affected | Pava Toner |
| Component | HCT-CAP-007 (cap component) |
| Batch / lot code(s) | Not yet linked — pull the receiving lot/PO from PLM if you want this tied to a batch record |
| Vendor | HCT |
| Description | HCT shipped 50 units of HCT-CAP-007 (Pava Toner cap) against [PO #]. At incoming inspection, 1 of 50 units showed a visible hairline crack. The remaining 49 units passed inspection. |
| Evidence | Receiving inspection notes / photo of cracked unit (attach when available) |
| Suspected severity | **Minor** (see §3.3 read below) |
| Containment action taken | Cracked unit quarantined at receiving. Remaining 49 units released to stock as passed. No further containment needed — the failure was caught before it reached production or a customer-facing batch. |

## 2. Severity read (SKN-OPS-005 §3.3)

Minor: "Isolated, contained, no recurrence pattern, no compliance exposure." Triggers listed include "single-unit cosmetic defect... already corrected."

This fits Minor cleanly:
- **Isolated** — 1 of 50 units, not a full-batch or systemic defect.
- **Contained** — caught at receiving inspection, before it entered production or shipped. Quarantine already executed.
- **No recurrence pattern** — you noted HCT has no NCR history in the last 12 months. That's the pattern check called for in NCR Procedure §4.1.4.
- **No compliance/safety exposure** — a cracked cap caught at receiving carries no safety, labeling, or regulatory angle. It never reached a batch or a customer.

None of the Critical or Major triggers apply (no safety/recall/regulatory angle, no full-batch OOS, no vendor-systemic pattern, no repeat-NCR-same-root-cause).

## 3. Escalation decision: Convert to CAPA vs. Close — No CAPA

Walking NCR Procedure §4.2's three branches:

**A. Convert to CAPA** — required for Critical/Major, *permitted* for Minor. Not required here. You could still choose to open one if you wanted to push HCT on packaging QC upstream, but nothing in this record obligates it.

**B. Close — No CAPA** — this is the branch that fits. Permitted for Minor, and this NCR checks every box: contained at receiving, no recurrence, no compliance exposure. Recommended path.

**C. Hold for more information** — not needed. You have everything: quantity, defect type, containment, vendor history. No open question to hold on.

**Recommendation: Close — No CAPA.**

### Draft justification (NCR Procedure §5 — required fields for Closed-No-CAPA)

- **Why no CAPA:** Single-unit hairline crack in a 50-unit component shipment, caught and quarantined at receiving before any production or customer exposure. Meets Minor criteria per SKN-OPS-005 §3.3 (isolated, contained, no recurrence, no compliance exposure). No systemic vendor or process failure indicated by one unit in one shipment.
- **What containment resolved:** Cracked unit quarantined at receiving; remaining 49 units inspected and passed, released to stock. Loop closed at intake — no further action needed to protect product or customer.
- **Trend exposure:** HCT has no recurrence pattern in the trailing 12 months (per your input). No open or recent NCRs against HCT reviewed that would indicate a developing pattern. *(If you want, I can pull HCT's supplier wiki page / NCR history live to confirm this before you sign off — I did not run that query since you asked for the plan only.)*
- **Reviewer:** Operator (Alvin Belt) — pending QA Lead (Perrine) awareness per the monthly Closed-No-CAPA review cadence (§5: reviewed monthly by Operator, quarterly by QA Lead — not a blocking sign-off on close itself, since Minor Close-No-CAPA doesn't gate through QA Lead the way NCR→CAPA conversion does).

## 4. What happens on approval (if you approve this plan)

1. Assign real `NCR-2026-NNN` number (check current sequence in SJS CAPA Log first).
2. Create the task in **NCR Open**, then move to **NCR Closed (No CAPA)** section with the justification fields above written to the record.
3. Set `Status = Closed-No-CAPA`, `Source = vendor-receipt`, `Severity = Minor`.
4. **Vendor scorecard signal (§6c):** Since this is vendor-driven (HCT), stage a `[Vendor Scorecard Signal]` comment on the relevant purchasing-manager HCT record noting the single-unit defect — informational, not a CAPA trigger, but keeps HCT's receiving-inspection record complete for scorecard purposes. Purchasing-manager owns the actual scorecard write.
5. No SOP revision, no regulatory flag, no batch-lifecycle handoff — none of those apply to a contained single-unit component defect.
6. Retained per §6 (3 years post-batch-expiration).

## 5. Open items before I commit anything

- Need the PO number and receiving lot to fully populate the record.
- Need the receiving inspector's name for the Reporter field.
- Confirm you want the HCT vendor-scorecard signal staged, or skip it since this is a single unit with no pattern.

Say "approved" (with any corrections) and I'll write this to Asana — number, fields, section placement, and the vendor scorecard comment-back.
