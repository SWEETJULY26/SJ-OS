# NCR Draft Plan — HCT-CAP-007 Hairline Crack at Receiving

**Note:** This is a draft plan only. Nothing has been written to Asana.

## 1. NCR Intake (proposed record)

| Field | Value |
|---|---|
| Title | Hairline crack — HCT-CAP-007 (Pava Toner cap), 1 of 50 units |
| Source | Receiving inspection |
| Vendor | HCT |
| Component | HCT-CAP-007 (Pava Toner cap) |
| Quantity received | 50 |
| Quantity affected | 1 |
| Quantity passed | 49 |
| Defect type | Hairline crack, visible on visual inspection |
| Disposition | Quarantined (affected unit) |
| Detection point | Receiving |
| Date | 2026-07-21 (today, pending actual receiving date) |

## 2. Should this open as an NCR?

Yes. Any nonconforming material caught at receiving should get an NCR record even if the disposition is simple — it's the mechanism that creates the paper trail, closes the loop on the quarantined unit, and feeds the vendor quality history HCT builds up over time. Opening it costs almost nothing and means the data exists later if a pattern shows up.

## 3. Does this need a CAPA, or can it close without one?

**Recommendation: Close the NCR without a CAPA.** Here's the reasoning, walked through:

**Severity — low.** A single cracked cap is a component-level cosmetic/mechanical defect, not a safety, efficacy, or regulatory issue. It doesn't touch the finished product's formula, claims, or labeling.

**Containment — already worked.** Receiving inspection is the system doing its job. The defect was caught before the cap reached production or a customer. There's no shipped-product exposure, no downstream containment action needed (no WIP or finished goods to sweep, no field action).

**Scope — contained to one unit.** 1 out of 50 (2%) is within normal supplier variability for a mechanical component like an injection-molded cap. It's not a lot-wide or batch-wide failure — 49 of 50 passed inspection clean.

**Recurrence — none.** HCT has no defect pattern on this component (or with this vendor generally) over the trailing 12 months. That's the deciding factor. A CAPA is warranted when there's a *pattern* — repeat occurrences, a systemic vendor process problem, or a defect rate trending up. One isolated, caught-at-the-gate unit with a clean 12-month history doesn't meet that bar.

**What CAPA would require instead:** If this were the second or third hairline-crack incident from HCT on this cap in the trailing 12 months, or if the defect rate on this lot were higher (say, several units in the 50, suggesting a mold or tooling issue), or if it had slipped past receiving into WIP/finished goods, that would flip the answer — root cause investigation (5 Whys or fishbone on HCT's molding/QC process) and a corrective action (tooling fix, incoming inspection AQL tightening, vendor corrective action request) would be warranted.

## 4. Proposed NCR close-out path

1. Log the NCR with the details above, disposition = quarantine/scrap the single unit (reject and return-to-vendor or scrap per standard component reject handling — confirm which HCT uses).
2. Note in the vendor history: 1 hairline-crack unit, 50-unit shipment, no CAPA triggered, no recurrence in trailing 12 months.
3. Close the NCR at "no CAPA required" — reasoning: isolated incident, caught at receiving, no recurrence pattern, low severity, no safety/regulatory dimension.
4. No notification to HCT is required beyond standard reject reporting on this PO line — this isn't a rate or pattern issue that needs a formal vendor corrective action request.
5. Recommend keeping a running count of HCT-CAP-007 defect incidents (rolling 12-month view) so that if a second or third instance shows up, the pattern is visible immediately and triggers the CAPA conversation at that point rather than starting from zero.

## Bottom line

Open the NCR (record it), disposition the single unit as quarantined/rejected, and close the NCR without a CAPA. The facts — one unit out of fifty, caught at the gate, no safety issue, no vendor recurrence in 12 months — don't meet the bar for root cause investigation and corrective action. Keep an eye on HCT-CAP-007 going forward; a second occurrence changes the calculus.
