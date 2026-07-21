# CAPA Coordinator — Draft Plan for Approval
**Source handoff:** `[CAPA Pending — capa-coordinator] Pava Toner Lot 26-02 — 4 Skin Reactions complaints in 21 days` (from complaint-and-event-handler)
**Prepared:** 2026-07-21 | **Status:** Draft — nothing written to Asana. Approve/edit each gated decision below.

No prior CAPA/NCR history found for Element Packaging or Pava Toner (checked wiki pages `supplier/element` and `sku/pava-toner` — neither exists yet; checked SJS CAPA Log for existing NCR/CAPA numbers this year — none found, so this opens as `NCR-2026-001`, confirm against live Asana count before commit). PLM confirms Element Packaging is an active vendor and Pava Toner (SKU `988357`) is an active product; the FOA-ROSE component record wasn't found by name/lot in PLM's `components` table — flagging as a data gap, not a blocker, since the complaint brief already names the suspected lot.

---

## 1. NCR Record (SKN-OPS-005 §3.2)

| Field | Value |
|---|---|
| NCR number | **NCR-2026-001** *(pending confirmation against live count — first NCR this skill has drafted for either party)* |
| Date opened | 2026-07-21 |
| Reporter | complaint-and-event-handler (system handoff) |
| Source | `complaint-trend` |
| Category | Product |
| SKU(s) affected | Pava Toner (SKU 988357) |
| Batch / lot code(s) | Lot 26-02 |
| Vendor | Element Packaging — suspected component: FOA-ROSE, vendor lot R26-008 |
| Description | 4 DTC-channel complaints in 21 days against Pava Toner Lot 26-02. Consistent pattern: itching and redness, all onset within 48 hours of first use. No SAE-level events reported (no medical intervention, no hospitalization). complaint-and-event-handler's working theory points to the FOA-ROSE component (Element, vendor lot R26-008) as the suspected contributing material — this is a hypothesis to test in RCA, not yet an established root cause. |
| Evidence | 4 linked complaint task IDs (from complaint-and-event-handler's log — pull gids at intake approval), consumer-reported onset timing, channel = DTC for all 4 |
| Suspected severity | **Major** (see §2 below) |
| Containment action taken | *Not yet confirmed as of this handoff.* Recommend: quarantine remaining Lot 26-02 inventory (DTC + any retail allocation) pending investigation, and flag Lot 26-02 in Shopify/Logiwa to stop further fulfillment from that lot. **This needs an explicit containment answer from Operator before intake closes** — the brief doesn't say whether Lot 26-02 stock has been held. |

**Open question for Operator before I commit intake:** has Lot 26-02 been held/quarantined yet? If not, that's the first action, ahead of anything else in this plan.

---

## 2. Severity Call

**Recommendation: Major**, not Critical, not Minor.

Reasoning against SKN-OPS-005 §3.3 bands:
- **Not Minor** — this is a batch-linked complaint cluster (4 complaints, same lot, 21 days), not an isolated single-unit event. §3.3 names "single-batch complaint cluster" as a Major trigger explicitly.
- **Not Critical** — no medical-intervention SAE, no FDA observation, no retailer chargeback, and this isn't a repeat NCR on the same batch (first NCR on this lot). The brief is explicit that there are no SAE-level events.
- **Major fits**: quality impact that can't be absorbed without action, but doesn't cross into direct safety/recall territory as currently scoped.

Consistent with the "err high" guidance in §3.3 — if the complaint count climbs past 4, or an SAE-level report comes in on this lot, this gets re-read as Critical and the CAPA timeline compresses. Flagging that trigger now so it's not missed.

**SLA that follows from Major:** NCR review within 10 business days; NCR→CAPA conversion within 10 business days of NCR open (i.e., by **2026-08-04**).

---

## 3. NCR Review (SKN-OPS-005 §4.1) and NCR→CAPA Conversion Decision

Walking the §4.1 checklist:

1. **Description specific enough?** Yes — pattern (itching/redness), timing (48h onset), channel (DTC), count (4/21 days), suspected material all captured.
2. **Severity consistent with §3.3?** Yes, per §2 above.
3. **Existing open CAPA on this root cause?** None found — no prior CAPA/NCR history on Element or Pava Toner in the CAPA Log or the wiki. This is a fresh thread, not a recurrence.
4. **Pattern across recent closed NCRs?** No comparison data available (first NCR touching either party). Recommend the wiki gets written back once this closes so the next Element- or Pava Toner-linked event has history to check against.
5. **Containment confirmed?** **Not yet — see the open question in §1.** Recommend holding conversion approval until containment is confirmed, per §4.1 item 5 ("if not, drive containment first; the NCR can wait"). I'm drafting the conversion decision below on the assumption containment gets confirmed promptly, since the complaint pattern and Major severity clearly warrant it — but flagging that this is technically out of sequence per the SOP if containment isn't nailed down first.

**Decision: Convert to CAPA.** Required at Major severity per §4.2(A). Assign **CAPA-2026-001** *(same numbering caveat as NCR — confirm against live count)*.

**Gate:** NCR→CAPA conversion requires QA Lead sign-off (Perrine). This decision is staged `Gate = Pending QA Lead` — routing to Perrine for approval before the CAPA file opens.

---

## 4. CAPA Opening

```
CAPA Number: CAPA-2026-001
Linked NCR: NCR-2026-001
Date opened: 2026-07-21
Severity: Major
Source: complaint-trend
Category: Product

Linked records:
- Batch: Pava Toner Lot 26-02 (PLM product id c762529c-b587-49b4-b9e3-5c0a1e2af714, SKU 988357)
- Vendor: Element Packaging (suspected — FOA-ROSE component, vendor lot R26-008)
- SKU: 988357 — Pava Toner
- Source task: [CAPA Pending — capa-coordinator] Pava Toner Lot 26-02 — 4 Skin Reactions complaints in 21 days (complaint-and-event-handler handoff)

Investigation team (proposed — Operator confirms):
- Operator — Alvin Belt (Lead)
- Voice of Customer — Nicole Iturbe (advisor — complaint-driven CAPA)
- Department Manager (Vendor-driven) — Purchasing lead, to review Element's FOA-ROSE R26-008 lot record and COA
- QA Lead — Perrine (root cause sign-off gate)

Statement of non-conformance: Four DTC-channel consumers reported itching and redness within 48 hours of first use of Pava Toner Lot 26-02, all within a 21-day window (2026-07-21 review). No SAE-level events. Suspected contributing material: FOA-ROSE component from Element Packaging, vendor lot R26-008.
```

---

## 5. Root Cause Analysis Approach

**Tool selection: Fishbone first, then 5 Whys on the strongest branch.**

Why Fishbone over 5 Whys as the starting tool: this isn't a single-chain event (like a mislabeled batch) — it's a cluster of independent consumer reactions with a suspected but unconfirmed material link. That's exactly the "systemic pattern, multiple contributing factors" case the RCA reference calls out for Fishbone over 5 Whys. Once Fishbone identifies the strongest branch (likely Material or Method, given the vendor-lot hypothesis), follow up with 5 Whys on that branch to get to an attributable root cause.

**Fishbone prompts to walk with the investigation team:**

| Category | Prompt |
|---|---|
| Manpower | Did anyone change in formulation, filling, or QC sign-off around Lot 26-02's production run? Any handoff gaps? |
| Method | Does the current incoming-inspection or formulation-release process test for irritant potential on new component lots, or only visual/COA review? Was Lot 26-02 released on COA review alone? |
| Machine | Any equipment or mixing-process changes for this batch run vs. prior Pava Toner lots? |
| Material | Is FOA-ROSE vendor lot R26-008 confirmed as an input to Lot 26-02 via BOM/batch record (not yet verified in PLM as of this draft)? Any change in Element's sourcing, formulation, or supplier-of-supplier for this lot vs. prior lots that didn't generate complaints? |
| Measurement | Did the COA for R26-008 report anything unusual (pH, concentration, contaminant) that incoming inspection didn't flag as material? |
| Environment | Any seasonal, climate, or shipping-condition factor specific to this lot's component delivery or finished-good storage? |

**Data gap to close before/during RCA:** confirm in PLM (via plm-assistant) that FOA-ROSE vendor lot R26-008 is actually the BOM-linked component for Pava Toner Lot 26-02 — this wasn't independently verified against PLM records in this draft (the component wasn't found by name/lot search in the `components` table; it may be filed under a different SKU/lot naming convention). This is foundational to the vendor-driven hypothesis and should be the team's first checkpoint, not an assumption carried into the Fishbone.

**Gate:** Root cause statement requires QA Lead (Perrine) sign-off before Action Plan (Job 4) can proceed. RCA verbatim walk gets captured as a comment thread on the CAPA task per the standard artifact format; only the final statement goes in the `Root Cause Statement` field.

---

## 6. Action Plan (drafted pending root cause — structure ready, content is placeholder until RCA lands)

Per SKN-OPS-001 §5.3, both plans are normally drafted *after* root cause is approved. Since this task asked to walk through to the action-plan stage, here is the plan **scaffold** with the most likely actions given the current hypothesis (vendor material, single-lot scope) — treat the specific actions as a starting draft the investigation team will firm up once RCA confirms the actual root cause, not a final commitment.

### Corrective Actions (addresses the immediate non-conformance)

| # | Action | Owner | Due | Evidence required | Status |
|---|---|---|---|---|---|
| C1 | Confirm containment: hold/quarantine remaining Lot 26-02 inventory across DTC and any retail allocation; stop further fulfillment from this lot in Logiwa/Shopify | Operator — Alvin Belt | 2026-07-23 | Inventory hold confirmation + Logiwa/Shopify SKU-lot block screenshot | Open |
| C2 | Pull and review Element's COA for FOA-ROSE vendor lot R26-008 against spec | Purchasing lead | 2026-07-28 | COA on file + written comparison against spec | Open |
| C3 | Confirm via PLM/BOM that R26-008 is the actual component lot in Lot 26-02's batch record (close the data gap flagged in §5) | Purchasing lead + plm-assistant | 2026-07-25 | PLM batch-to-component trace, screenshotted or linked | Open |
| C4 | Direct outreach to the 4 complainants confirming investigation is open (coordinate with complaint-and-event-handler — this is their §4.E corrective-action lane, not a CAPA write) | complaint-and-event-handler (cross-reference only) | — | — | Cross-referenced, not owned here |

### Preventive Actions (addresses underlying cause — firm up once root cause lands)

| # | Action | Owner | Due | Evidence required | SOP impact | Status |
|---|---|---|---|---|---|---|
| P1 | If Material/Method branch confirms — add an irritant-risk or expanded QC check for new/changed component lots on skin-contact SKUs, not just COA review | QA Lead — Perrine | TBD post-RCA | Updated incoming-inspection checklist | Likely SOP-NNN revision (incoming inspection procedure) | Open |
| P2 | If vendor-sourcing change is implicated — build a trigger so vendor sourcing/formulation changes at Element propagate to Quality for review before release (mirrors the RCA reference's own worked example for exactly this failure pattern) | Purchasing lead + QA Lead | TBD post-RCA | Documented review-trigger process | Likely New SOP or SOP-NNN revision | Open |

Any preventive action that lands on "SOP-NNN revision" or "New SOP" auto-stages a `[SOP Revision Pending — quality-manager]` task once approved — flagging that now so it's expected, not a surprise at Job 4 commit.

---

## 7. Handoffs staged (not committed — for visibility)

- **6a, close-the-loop:** once this CAPA closes, comment back on the originating complaint-and-event-handler task with the closeout summary + CAPA number.
- **6c, vendor scorecard signal:** this is vendor-driven (Source = complaint-trend, suspected category = vendor). If RCA confirms Element/R26-008 as root cause, stage a `[Vendor Scorecard Signal]` comment on Element's purchasing-manager record with the CAPA number and root cause, once root cause is confirmed — not before.
- **6d, regulatory feed:** no SAE, no recall trigger per the brief — no regulatory flag staged. Re-evaluate if complaint count or severity changes.

---

## What I need from you to proceed

1. **Confirm containment status on Lot 26-02** — held or not, and where. This is the one item that's out of sequence in this draft (§1, §3).
2. **Approve NCR-2026-001 intake** (Operator gate) — confirm the number against the live CAPA Log count before I write anything.
3. **Approve severity = Major** (§2).
4. **Approve NCR→CAPA conversion decision** — routes to Perrine (QA Lead) for sign-off (§3).
5. **Confirm investigation team** (§4) — Purchasing lead name for the Department Manager slot.
6. **Approve RCA approach** (Fishbone → 5 Whys) and the PLM verification checkpoint (§5) before the team convenes.
7. Once root cause lands and Perrine signs off, I'll firm up the Action Plan (§6) actions and owners for your approval — the current table is a draft scaffold, not a commitment.

Nothing above has been written to Asana. This is the full draft for your review.
