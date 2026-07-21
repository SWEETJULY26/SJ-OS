# CAPA Walkthrough — Soursop Vit C Lot 25-09, Accelerated Stability Fail (Draft, Not Yet Written to Asana)

Trigger: batch-lifecycle-tracker handoff in SJS CAPA Log — "[CAPA Request — batch-lifecycle-tracker] Soursop Vit C Lot 25-09 — 3-month accelerated stability fail on Vitamin C assay (89% of label claim, spec is ≥95%)."

Classification going in: Critical NCR. The batch is live at Ulta and DTC, so this isn't a paperwork exercise — every phase below assumes market exposure and moves on a compressed clock.

## Phase 1 — NCR Intake and Open

**What it produces:** A new NCR record in the SJS CAPA Log with:
- Source: batch-lifecycle-tracker (automated handoff from stability monitoring)
- Product/Lot: Soursop Vitamin C Serum, Lot 25-09
- Non-conformance: 3-month accelerated stability assay result 89% of label claim vs. ≥95% spec
- Initial severity flag: Critical (active market batch, potency failure, retail + DTC channels)
- Containment question raised immediately: is Lot 25-09 still shipping from OC3PL, and is any downstream stock at Ulta DCs or on the DTC site sellable pending investigation?

**Approval gate:** Operator (Alvin or delegate) reviews intake within 24 hours for a Critical-flagged NCR. This gate confirms the NCR is real, correctly scoped to one lot (not conflated with other SKUs/lots), and decides whether to request an immediate hold on Lot 25-09 as a parallel containment action — that hold request routes to batch-lifecycle-tracker, not through this CAPA record itself.

**Handoff fired at this step:** A hold recommendation to batch-lifecycle-tracker for Lot 25-09 (and any sibling lots on the same fill run, if applicable) pending root cause. This is a containment action, logged as a cross-reference on the NCR, not a CAPA action yet — CAPA actions don't start until conversion.

## Phase 2 — Conversion: NCR → CAPA

**What it produces:** A decision record on whether this NCR escalates to a full CAPA. For a Critical NCR with market exposure, conversion is close to automatic, but the record still needs to state why: recurring risk (stability failures can indicate formulation, packaging, or process drift that will recur in future lots), regulatory exposure (potency below claim on a marketed cosmetic has labeling and possibly MoCRA implications), and channel exposure (Sephora/Ulta/Whole Foods relationships at stake).

Once converted, the record gets:
- A CAPA number
- Scope statement: this CAPA covers Lot 25-09's Vitamin C assay failure at 3-month accelerated stability; it does not automatically cover other SKUs unless root cause implicates a shared ingredient, process, or supplier
- Status field set to the CAPA phase (Root Cause in Progress)

**Approval gate:** Operator approves the conversion and scope statement. This is where the Operator also decides urgency posture — given the Critical flag, this should trigger parallel-tracking with complaint-and-event-handler (any customer complaints tied to this lot?) and potentially regulatory-manager if a market withdrawal or retailer notification becomes likely.

**Handoffs fired at this step:**
- Cross-flag to complaint-and-event-handler: check whether any open or closed complaints on Soursop Vit C map to Lot 25-09, since a potency failure could explain efficacy complaints already on file.
- Cross-flag to regulatory-manager (staged, not sent): flag that a Critical stability failure on an in-market batch may require a retailer attestation update or MoCRA adverse-event review, pending root cause outcome. This is informational at this stage — no filing action yet.

## Phase 3 — Root Cause Analysis

**Recommended tool: Fishbone (Ishikawa), not 5 Whys.**

Reasoning: 5 Whys works best on a single linear causal chain with one clear failure point. A Vitamin C potency drop over accelerated stability is a classic multi-variable degradation problem — Vitamin C (ascorbic acid and its derivatives) is notoriously sensitive to oxidation, pH, temperature, light exposure, and packaging barrier properties, and any of those alone or in combination could explain an 89%-of-claim result. Fishbone forces the investigation to check all plausible categories before converging, which matters here because jumping straight to one "why" chain risks missing a contributing factor (e.g., blaming the antioxidant package when the real driver is a packaging barrier change).

**Fishbone categories to work through for this failure:**
- **Materials:** Was the Vitamin C raw material (or stabilized derivative) from the qualified lot/vendor, within spec on COA, and within its own shelf life at time of use? Any recent supplier change or raw material lot substitution?
- **Formula/Process:** Any deviation in mixing time, temperature, or order of addition during manufacture of Lot 25-09? Was pH verified in-process and does it match the validated range for ascorbic acid stability?
- **Packaging:** Is this lot using the qualified primary packaging (bottle/pump barrier, opacity, oxygen ingress)? Any packaging component change, vendor change, or lot-to-lot variance in barrier performance?
- **Environment/Storage:** Was the batch stored and transported within spec temperature/light conditions between manufacture and the 3-month pull? Any cold-chain or warehouse exception logged?
- **Testing/Measurement:** Is the assay method validated and was it run correctly — instrument calibration, standard curve, sample handling? A measurement artifact should be ruled out before treating this as a true formulation failure.
- **People/Method:** Any deviation from the stability protocol itself — pull timing, sample prep, chain of custody from OC3PL or the stability chamber to the lab?

**What this phase produces:** A completed Fishbone diagram (or structured equivalent) attached to the CAPA record, a stated root cause (or ranked short list if inconclusive), and supporting evidence — COAs, batch record excerpts, in-process pH/temp logs, packaging spec docs, assay method validation reference.

**Approval gate:** QA Lead approves the root cause conclusion. For a Critical CAPA, QA Lead sign-off should include an explicit statement on whether root cause is confirmed or still probable, since that determines how aggressive the corrective action needs to be (e.g., "probable root cause: packaging barrier lot variance" might justify action on packaging alone, but if unconfirmed, corrective action needs to cover the top 2–3 candidates).

## Phase 4 — Corrective and Preventive Actions

**What it produces:** Two linked action sets:

**Corrective (fixes this failure/this lot and immediate exposure):**
- Disposition decision on remaining Lot 25-09 inventory across OC3PL, DTC, and retail (Ulta) — hold confirmed, and a decision on pull-from-shelf vs. sell-through-with-monitoring depending on severity of the potency gap and whether efficacy claims are at risk
- Retest or extended investigation on retained samples from Lot 25-09 to confirm the assay result isn't an outlier
- If root cause points to a specific input (raw material lot, packaging lot), quarantine any unused inventory of that same input

**Preventive (stops recurrence in future lots):**
- If raw material: tighten incoming COA review or add an internal verification assay for Vitamin C potency/stability markers before release to production
- If packaging: requalify the barrier packaging spec, or add an accelerated-stability check tied specifically to packaging lot changes
- If process: update the batch record/work instruction with the corrected parameter (e.g., pH range, mix time) and retrain production staff
- If measurement: revalidate the assay method or retrain lab technicians on sample handling

Each action gets an owner, a due date, and links back to the specific root cause finding it addresses.

**Approval gate:** Operator approves the action plan for feasibility, cost, and timeline (can we actually execute this against active production schedules and supplier relationships). QA Lead approves the plan for technical adequacy (does it actually address the confirmed root cause, and does the corrective side adequately cover market risk).

**Handoffs fired at this step:**
- purchasing-manager, if root cause implicates a raw material or packaging vendor — this triggers a supplier corrective action request (SCAR) or at minimum a vendor performance flag and COA review tightening.
- inventory-manager, for the hold/disposition execution on remaining Lot 25-09 stock and any quarantined input material.
- complaint-and-event-handler stays looped in if any complaints were confirmed tied to this lot in Phase 2 — corrective action here should reference whether customer-facing remediation (refunds, replacement) is warranted.

## Phase 5 — Verification

**What it produces:** Evidence that the corrective actions were actually implemented as planned — not that they worked yet, just that they happened. For this CAPA: confirmation that Lot 25-09 disposition was executed (hold/pull carried out at OC3PL and retail), confirmation that the raw material or packaging quarantine was executed, confirmation that any updated work instruction or spec was actually issued and acknowledged by the relevant team, confirmation that revised incoming inspection or assay steps are live.

**Approval gate:** QA Lead verifies each action against its stated completion criteria and signs off action-by-action. Any action not fully implemented gets kicked back with a revised due date rather than waved through.

## Phase 6 — Effectiveness Review

**What it produces:** A determination made after enough time/data has passed that the preventive action actually works — this is the step people skip and shouldn't. For this CAPA, effectiveness proof looks like: the next production lot(s) using the corrected process/spec/material pass 3-month accelerated stability on Vitamin C assay within spec, and ideally a real-time stability data point trending in the right direction as it becomes available. If the preventive action was a tightened incoming raw material check, effectiveness proof includes at least one to two supplier lots processed under the new check with no potency-related rejects.

Given the Critical severity here, effectiveness review should not close on a single passing data point alone — QA Lead should require at least one full accelerated stability cycle on a post-fix lot before calling it proven, given how sensitive Vitamin C stability data can be to sample-to-sample variance.

**Approval gate:** QA Lead approves the effectiveness determination. If the data doesn't support effectiveness, the CAPA reopens the action-plan phase rather than closing — this is a loop-back point, not a dead end.

## Phase 7 — Closeout

**What it produces:** A closeout record summarizing the full trail — root cause, actions taken, verification evidence, effectiveness evidence — signed and dated, with the CAPA status field moved to Closed and the Gate field cleared of HITL holds.

**Approval gate:** QA Lead signs the technical closeout. Operator gives final sign-off given the Critical/market-exposure nature of this one — Critical CAPAs with retail and DTC exposure should get Operator-level closeout visibility even though QA Lead owns most of the lifecycle from root cause forward.

**Handoffs fired at close:**
- regulatory-manager: final notification that the CAPA is closed, with a summary suitable for a retailer attestation response (Ulta may ask about corrective action on a stability-related issue) and for MoCRA recordkeeping if this rises to a reportable pattern.
- purchasing-manager: closes out any SCAR or vendor flag opened in Phase 4, or converts it into an ongoing vendor monitoring item if the root cause was supplier-side.
- inventory-manager: confirms final disposition of the held/quarantined material is closed out (destroyed, returned to vendor, or released, as applicable).
- batch-lifecycle-tracker: notified that the hold on Lot 25-09 is resolved per the CAPA outcome (either permanent removal from market or release, per the disposition decision made in Phase 4).
- complaint-and-event-handler: notified of closure so any linked complaint records can reference the resolved CAPA in their own closeout.

## Summary of Gate Ownership

| Phase | Approval Gate Owner |
|---|---|
| NCR Open | Operator |
| Conversion to CAPA | Operator |
| Root Cause Analysis | QA Lead |
| Corrective/Preventive Action Plan | Operator (feasibility) + QA Lead (technical adequacy) |
| Verification | QA Lead |
| Effectiveness Review | QA Lead |
| Closeout | QA Lead (technical) + Operator (final, given Critical/market exposure) |

## What This Draft Does Not Include

This is a walkthrough only — nothing above has been written to Asana. No hold has actually been requested from batch-lifecycle-tracker, no cross-flags have been sent to complaint-and-event-handler, regulatory-manager, purchasing-manager, or inventory-manager, and no root cause work has actually started. Before running this for real, confirm: (1) whether Lot 25-09 should be held immediately in parallel with intake rather than waiting on Phase 1 approval, given it's already at Ulta and DTC, and (2) whether any customer complaints already on file should be pulled before conversion so the CAPA scope statement reflects known complaint signal from the start.
