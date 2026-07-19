# System B sub-skill summary

One-paragraph profile of each of the six System B sub-skills, used by the router to disambiguate intent. The canonical record of what each skill owns and where its data lives stays in the sub-skill's own SKILL.md; this file is a compact reference for routing.

---

## quality-manager (v5.5)

The umbrella. Cross-skill rollup, SOP catalog (active registry of every SJS SOP plus pending ratification queue), ratification protocol, annual review protocol, cross-cutting tasks (SOP annual reviews, audit prep, retailer questionnaires, regulatory inspection prep, quality system reviews, QoS threshold tasks), QoS aggregation pulled from oc3pl-order-manager. Asana home: SJS Quality Management project (gid `1214660401644163`). Read-most with two HITL gates: cross-skill task creation (QA Lead approves) and SOP ratification approval (QA Lead approves). The canonical role-map for System B lives here.

**Routes here when:** request is ambiguous, cross-skill, generic about quality state, about SOPs (catalog, ratification, annual review), about cross-cutting work (audits, regulatory inspections, retailer questionnaires, quarterly system reviews), or about QoS aggregation.

---

## capa-coordinator (v5.2)

CAPA + NCR lifecycle per SKN-OPS-001. Two intake paths (quality finding or regulatory finding) through the SJS CAPA Log Asana project. Walks SKN-OPS-001 §5.1 → §5.6 verbatim. Authored SKN-OPS-005 (NCR Procedure, ratified 2026-05-09). HITL split: Operator (intake, conversion, action plan, implementation) and QA Lead (root cause sign-off, verification, effectiveness, close). Hands off to complaint-and-event-handler, purchasing-manager (vendor scorecard), regulatory-manager (System C, live), quality-manager (SOP revisions).

**Routes here when:** request is about a CAPA, NCR, root cause investigation, 5 Whys / Fishbone, action plan, verification, effectiveness, or CAPA closeout.

---

## complaint-and-event-handler (v5.1)

Single intake door for end-customer-driven quality signals — complaints, adverse events, recall workflow. Reads SJ Skin Complaint Log Asana project (gid `1204763097184846`). Walks SKN-OPS-002 (SAE) and SKN-OPS-003 (Recall). Trend detection feeds CAPA handoffs to capa-coordinator. Voice of Customer (Nicole) holds gates on complaint classification and complaint-driven escalations.

**Routes here when:** request is about a customer complaint, SAE, allergic reaction, adverse event, recall trigger, complaint trend, or customer-quality intake.

---

## quality-lab-coordinator (v5.3)

Lab-side and supplier-side quality signal per SKN-OPS-006. OOS/OOT classification, incoming material defect handling, lab pattern analysis, vendor flag thresholds. Comment-back signal to purchasing-manager for vendor scorecard updates (single ownership of the scorecard stays with Purchasing — this skill never writes the scorecard). Operates Lab Findings sections within SJS Quality Management. Hands off CAPA-worthy patterns to capa-coordinator.

**Routes here when:** request is about an OOS/OOT lab result, incoming material defect, COA mismatch, retest decision, lab pattern by vendor, vendor quality flag, or vendor scorecard signal.

---

## batch-lifecycle-tracker (v5.4)

Ongoing in-market batch state per SKN-OPS-007 — Active, Hold, Released, Pulled, Expired. Receives the handoff from inventory-manager at first commercial batch and from asana-pd-manager when Formula Tracker hits Signed Approvals. Schedules and tracks in-market stability (PET, accelerated, real-time) per ISO 11930 cadence — water-based gets full PET schedule, anhydrous gets real-time annual only. HITL on every hold, release, and transition. Operates Batch sections within SJS Quality Management.

**Routes here when:** request is about a batch state change, hold/release on a batch, in-market stability scheduling or results, near-expiry quality decision, or pre-launch → in-market transition.

---

## quality-status-reporter (v5.6)

The rendering layer. Generates the branded HTML quality dashboard at `acb-thelanding.netlify.app/quality-dashboard.html` from quality-manager's rollup. On-demand + monthly auto-snapshot. Writes to two destinations every generation: Asana attachment in SJS Quality Management and the GitHub repo at `/Users/alvinbelt/Downloads/acb-thelanding/`. Sister to sjs-status-reporter (PD) and the future ops-status-reporter (Ops).

**Routes here when:** request is about generating, regenerating, publishing, or snapshotting the quality dashboard, or about a branded quality output.

---

## Quick-glance routing matrix

| Request domain | Skill |
|---|---|
| CAPA / NCR / root cause | capa-coordinator |
| Complaint / SAE / recall | complaint-and-event-handler |
| Lab result / vendor flag / scorecard | quality-lab-coordinator |
| Batch state / stability / hold/release | batch-lifecycle-tracker |
| SOP catalog / ratification / annual review / audit prep / cross-cutting | quality-manager |
| Quality dashboard generation / publication | quality-status-reporter |
| Cross-skill / ambiguous / generic | quality-manager (rollup) |
