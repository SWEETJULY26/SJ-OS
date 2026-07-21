# CAPA Intake Plan — Pava Toner Lot 26-02 (Draft for Approval)

**Source handoff:** complaint-and-event-handler → capa-coordinator
**Task title:** [CAPA Pending — capa-coordinator] Pava Toner Lot 26-02 — 4 Skin Reactions complaints in 21 days
**Prepared:** 2026-07-21
**Status:** DRAFT — nothing written to Asana. Awaiting Alvin's approval before any record is created or moved.

---

## 1. Intake Summary (as received)

- Product: Pava Toner
- Lot: 26-02
- Signal: 4 skin-reaction complaints in 21 days
- Pattern: itching + redness, onset within 48h of first use
- Channel: all 4 from DTC
- Severity flag from handler: no SAE-level events reported
- Suspected contributing component: FOA-ROSE, vendor Element, component lot R26-008
- Handler's recommended scope: single-lot CAPA

I'm treating the handler's classification (non-SAE) and scope recommendation as inputs to validate, not as settled facts — the coordinator role re-checks severity and scope independently before committing resources.

## 2. NCR Record (Draft)

| Field | Value |
|---|---|
| NCR ID | NCR-2026-XXXX (assigned on creation) |
| Title | Pava Toner Lot 26-02 — Skin reaction complaint cluster |
| Product / SKU | Pava Toner |
| Affected lot(s) | 26-02 (finished good) |
| Suspected component | FOA-ROSE, vendor Element, component lot R26-008 |
| Date opened | 2026-07-21 |
| Source | complaint-and-event-handler handoff (SJ Skin Complaint Log) |
| Non-conformance description | 4 consumer complaints of itching and redness, each with onset within 48 hours of first use, all reported through the DTC channel, within a 21-day window, all tied to Lot 26-02. No SAE-level events reported to date. |
| Quantity/scope affected | Single finished-good lot (26-02) pending root cause confirmation on whether the issue is lot-specific or component/vendor-wide |
| Immediate containment considered | See Section 5 (Corrective — Containment) |
| Linked records | SJ Skin Complaint Log entries (4), pending SJS Reportable Events check (Section 3) |
| Status (SOP phase) | Intake / Pending Severity & Conversion Decision |
| Gate (HITL state) | Awaiting Operator approval to proceed to Conversion Decision |

## 3. Severity Call

**Working severity: Moderate.**

Reasoning:
- Frequency: 4 complaints in 21 days on a single lot is a real cluster, not an isolated one-off. That alone raises this above "log and monitor."
- Clinical picture: itching and redness with 48-hour onset is consistent with an irritant or allergic contact reaction — not benign, but also not the profile of a serious adverse event (no reports of blistering, swelling beyond application site, medical treatment sought, or systemic symptoms per the brief).
- Channel concentration: all 4 from DTC is useful signal — it could mean DTC is where volume/exposure is concentrated for this lot, or it could mean retail hasn't surfaced complaints yet (lag) or retail received a different sub-lot. This needs a check before ruling anything out.
- No SAE-level events: I'm accepting the handler's SAE determination as a reasonable first pass, but this CAPA should independently confirm no SAE criteria are met (per adverse-event-and-recall-reporter's classification logic) rather than just inherit the label. That confirmation is a required step before this severity call is finalized — see Section 3a.

**Severity does NOT currently support:**
- Full recall trigger (no SAE, no batch-wide signal established yet, no retailer/regulatory pressure noted)
- "Low" / no-action classification (frequency and pattern are too consistent to file as noise)

**Recommended severity: Moderate — single-lot CAPA justified, with an explicit trigger for escalation to Major/multi-lot if any of the conditions in Section 3a are hit.**

### 3a. Escalation triggers (if any occur, severity escalates before this plan proceeds further)
- A 5th complaint on Lot 26-02, or any complaint on a different Pava Toner lot with the same symptom pattern
- Any complaint that meets SAE criteria (medical attention sought, symptoms beyond application site, hospitalization, etc.) — route immediately to adverse-event-and-recall-reporter for SAE classification, do not hold inside this CAPA
- Confirmation that component lot R26-008 shipped into other finished-good lots or other SKUs beyond Pava Toner 26-02
- Retail channel (Sephora/Ulta/Whole Foods) surfaces a matching complaint — would break the "DTC-only" containment assumption

## 4. NCR → CAPA Conversion Decision

**Decision: Convert to CAPA.**

Rationale against typical conversion criteria:
- Recurrence: 4 events in 21 days on one lot clears a "pattern, not isolated" bar
- Consumer safety relevance: skin reactions on a leave-on/apply-to-skin product are a legitimate safety and brand-trust issue even without SAE status
- Traceable suspected cause: a specific incoming component (FOA-ROSE, Element, lot R26-008) is implicated, which is investigable and gives root cause analysis a concrete starting hypothesis rather than a vague "customer sensitivity" catch-all
- Vendor exposure: if root cause confirms the component, this has purchasing and vendor-quality implications beyond this one lot

**Scope decision: Single-lot CAPA, with a scoping checkpoint before corrective action is finalized.**

I'm agreeing with the handler's single-lot recommendation as the starting scope, but flagging that scope should be revisited once two facts are confirmed during root cause work:
1. Whether component lot R26-008 was used exclusively in Pava Toner Lot 26-02, or also in other finished-good lots/SKUs (purchasing-manager / PLM component-to-batch traceability)
2. Whether Element has other open quality signals on FOA-ROSE (vendor performance history)

If either comes back positive, scope should widen to multi-lot or vendor-level CAPA before corrective actions are finalized — flagged explicitly in Section 6 as a decision gate, not something to quietly expand later.

## 5. Root Cause Analysis Approach

**Method: 5 Whys, structured around the ingredient/formulation hypothesis, with a Fishbone as backup if 5 Whys dead-ends or reveals multiple contributing factors.**

5 Whys chosen over Fishbone as the primary tool because there's already a concrete leading hypothesis (a specific incoming component from a specific vendor lot) rather than an open field of possible causes — 5 Whys is the right tool when you have a thread to pull, Fishbone is better when you're mapping an unknown cause space. If the 5 Whys line breaks down (e.g., the component tests clean), I'd pivot to a Fishbone covering Material / Method / Machine / Man / Environment to avoid tunnel vision on the vendor.

**Draft 5 Whys thread (to be filled in with actual investigation, not assumed):**

1. Why are consumers reporting itching/redness after using Pava Toner Lot 26-02? → Reaction pattern and 48h onset is consistent with an irritant/sensitizer effect from a topical ingredient.
2. Why would this lot specifically trigger reactions when prior lots reportedly did not? → Suspected variance tied to FOA-ROSE component, lot R26-008, sourced from Element.
3. Why would component lot R26-008 differ from prior accepted lots? → To be determined: check incoming COA/COI for R26-008 against spec and against prior accepted lots' COAs; check for any formulation or process deviation logged on Lot 26-02's batch record.
4. Why would a spec deviation (if found) have passed incoming QC/release? → To be determined: review incoming inspection records for R26-008 — were all required tests run, and were results in-spec at the time of release?
5. Why would the system allow an out-of-spec or borderline component to reach production without catching it? → To be determined: this is the systemic question that preventive action needs to answer regardless of what the earlier Whys reveal.

**Data/records to pull before root cause can be finalized (not yet done — this is the investigation plan):**
- Batch/production record for Pava Toner Lot 26-02
- Incoming inspection + COA/COI for component lot R26-008 (Element)
- PLM component-to-batch trace: confirm which finished-good lot(s) used R26-008
- Element vendor history: any other complaints, deviations, or CAPAs tied to FOA-ROSE or this vendor in the trailing 12 months (purchasing-manager)
- The 4 underlying complaint records themselves (symptom detail, photos if provided, product usage reported, any batch/lot confirmation from the consumer side)
- Retail channel complaint check for Pava Toner in the same window, to confirm the DTC-only pattern isn't a reporting artifact

**Owner of root cause execution:** QA Lead (per CAPA gate split — Operator owns intake/conversion/plan approval, QA Lead owns root cause, verification, effectiveness, and close).

## 6. Corrective Action Plan (Draft)

Corrective action addresses this specific occurrence — Lot 26-02 and the immediate exposure.

1. **Containment (immediate, pending approval):** Place remaining on-hand units of Lot 26-02 on hold across DTC inventory pending root cause outcome. Route hold/release decision to batch-lifecycle-tracker per its hold protocol — this CAPA does not execute the hold itself, it triggers the request.
2. **Component quarantine:** Flag remaining on-hand inventory of Element component lot R26-008 for hold pending investigation, and check whether any other finished-good lot consumed the same component lot (PLM trace, via inventory-manager/purchasing-manager).
3. **Consumer-facing response:** Confirm with complaint-and-event-handler that each of the 4 complainants has received first-response guidance per SKN-OPS-002/003 (this sits with the handler, not duplicated here, but conversion should not proceed without confirming it happened).
4. **Vendor notification:** If root cause implicates the component, issue a formal non-conformance notice to Element referencing lot R26-008, request their internal deviation investigation and COA re-verification — routed through purchasing-manager as the vendor-facing owner.
5. **Disposition of held stock:** Once root cause is confirmed, determine disposition (release, rework if applicable — unlikely for a finished toner, or scrap) for both the finished-good hold and the component hold.

Corrective actions 1 and 2 are containment moves that should not wait for the full root cause to close — recommend executing these on approval of this plan, in parallel with the investigation, rather than sequencing them after Section 5 completes.

## 7. Preventive Action Plan (Draft)

Preventive action addresses recurrence — this component, this vendor, and the broader intake system.

1. **Incoming QC tightening (if root cause confirms component variance):** Add or tighten an incoming test parameter for FOA-ROSE from Element that would have caught the deviation in lot R26-008, rather than relying solely on COA acceptance.
2. **Vendor requalification trigger:** If Element's investigation reveals a process gap on their end, open a vendor corrective action request and consider a requalification or increased incoming-inspection frequency for FOA-ROSE for a defined trial period (e.g., next 3 lots receive 100% inspection instead of standard sampling).
3. **Complaint-to-CAPA latency check:** As a systemic side note — confirm the time from 1st complaint to CAPA handoff was within target per SKN-OPS-002; if the 3rd or 4th complaint is what triggered the pattern recognition, consider whether the complaint log's trend-detection threshold should trigger earlier (e.g., at 2-3 complaints on a single lot within a rolling window) rather than waiting for 4.
4. **Cross-SKU check:** If FOA-ROSE is used in other Sweet July Skin SKUs beyond Pava Toner, confirm whether those SKUs draw from the same component lot pool and need a parallel watch, even without complaints yet.

Preventive action 1 and 2 are contingent on what root cause actually finds — they're staged here as the likely paths, not pre-committed actions. If root cause instead points to something outside the component (e.g., a formulation stability issue independent of this vendor, or a labeling/usage-instruction gap), this section needs to be rewritten around the actual finding rather than forced into the vendor-fault narrative the initial hypothesis suggests.

## 8. Status Field / Gate Recommendation (for Asana, once approved)

- **Status (SOP phase):** Move from "Pending" to "NCR Opened — Root Cause In Progress" upon approval
- **Gate (HITL state):** Operator gate clears on approval of this plan (intake + conversion + corrective/preventive plan approved); next gate is QA Lead sign-off on root cause findings before this can move toward verification and close
- **Immediate next actions once approved:** (a) create the NCR/CAPA record and populate fields per Section 2, (b) trigger containment holds per Section 6.1–6.2, (c) hand root cause execution to QA Lead per Section 5

## 9. Open Questions for Alvin

1. Approve single-lot scope as starting point, with the widen-if-triggered condition in Section 4 — or start broader (multi-lot / vendor-level) given Element is named directly?
2. Approve containment holds (finished-good Lot 26-02 + component lot R26-008) to run in parallel with root cause, rather than waiting?
3. Any reason to fast-track a direct Element notification now versus waiting for root cause to confirm the component before contacting the vendor?

---
*This document is a draft plan only. No Asana record has been created, no task has been moved, and no hold has been executed. All actions above require explicit approval before execution.*
