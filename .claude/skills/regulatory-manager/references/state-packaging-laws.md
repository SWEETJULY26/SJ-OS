---
name: State packaging laws reference
description: State-level packaging compliance scope for Sweet July Skin — CA SB 343 Truth in Recycling Labeling, 19-state packaging toxics (heavy-metals certificate of compliance), and Extended Producer Responsibility (EPR) per state with thresholds and deadlines. Used by regulatory-manager registrations tracker and by claims-il-and-label-keeper IL packet assembly. Added 2026-05-12 post-Pedrero touchbase.
last_updated: 2026-05-12
---

# State packaging laws reference

Three regulatory regimes govern packaging beyond ingredient-side state laws (CA Prop 65, CA AB-2762, WA SB-5703). All three surfaced in the 2026-05-12 Pedrero touchbase as additions to the registrations tracker.

## 1. CA SB 343 — Truth in Recycling Labeling

### What it requires

Any product or packaging that displays the recycling chasing-arrows symbol must use a Pantone color that falls within California's approved gradient. Dark Pantones (most SJS packaging) fall outside the approved gradient.

### Compliance options per SKU

For each component or carton:

1. **Compliant** — Pantone is within approved gradient. Recycling symbol may stay.
2. **Lighten** — adjust Pantone to fall within gradient. Recycling symbol may stay.
3. **Remove symbol** — Pantone stays dark. Recycling symbol comes off the artwork.

### Who supplies what

- Heather Folkes (Pedrero) supplies the approved Pantone gradient reference and the per-Pantone pass/fail rule.
- Alvin (Operator) supplies the artwork files with their Pantone specs (primary, secondary, sample units / Z Pack).
- claims-il-and-label-keeper §6 label cross-check executes the per-component check; flags fail per SKU.

### Scope

All primary and secondary components plus sample units (Z Pack and equivalent). Out of scope: shipping cartons (not retail-facing).

### Status at 2026-05-12

Portfolio sweep seeded as `CA SB 343 — Pantone Audit — 2026` in Registrations — Active section. Subtasks per component pending first run.

## 2. 19-state packaging toxics — 100 ppm heavy metals certificate of compliance

### What it requires

A certificate of compliance from each packaging supplier certifying total heavy metals across all components ≤100 ppm. Covers 19 states (Toxics in Packaging Clearinghouse model legislation; varies state to state but all converge on the 100 ppm collective threshold).

### Enforcement

- **Heavy enforcement:** Target, Walmart, and other large retailers conduct supplier-side audits and request these on a recurring basis.
- **Light enforcement:** DTC and small retailers rarely audit; risk surface is the retailer audit, not state-side direct enforcement.

### Who supplies what

- Heather Folkes (Pedrero) supplies the specific verbiage SJS uses to request the certificate from suppliers — saves negotiation cycles.
- Component suppliers (Elements ACT, HCT, Impress, CDW, and any other active vendor) issue the certificate on request. Reputable suppliers know what this is and turn it around quickly.
- Operator (purchasing-manager skill cross-references) holds the supplier roster.

### IL packet integration (v6.6)

For any SKU distributed through Target / Walmart / other large retailers, the certificate of compliance attaches to the IL packet at §3 IL Review Gate per claims-il-and-label-keeper Rev.2 §3 update. Pedrero confirms presence; missing cert pauses the IL approval until cert lands.

### Status at 2026-05-12

Portfolio sweep seeded as `Packaging Toxics — 19 State — Cert of Compliance — 2026`. Subtasks per active component supplier.

## 3. Extended Producer Responsibility (EPR)

### What it requires

Cosmetics companies that exceed sales thresholds register with the Circular Action Alliance (CAA) for each EPR state, report annual packaging weights / materials / units sold, and pay sliding-scale fees calibrated to recyclability and volume.

### Active states (2026-05-12)

| State | Status | First fee deadline | Notes |
|---|---|---|---|
| Oregon | Live since 2025 | 2025 reporting cycle | Fees: $300 – $3,000 typical |
| California | Live; CA-specific threshold | 2026-05-31 for 2023 data; first CA invoices Aug 2026 | Fees: ~3x Oregon. ~$25K+ for high-non-recyclable packaging |
| Colorado | Live | Per CO cycle | — |

Three additional states joining in 2026 (specific states TBD; CAA publishes the roster).

### Thresholds (exemptions)

| Threshold | Notes |
|---|---|
| **General: $5M global sales** | Under this, exempt across most EPR states. |
| **CA: $1M in-state sales** | California uses a separate, lower threshold; under this, exempt from CA EPR specifically. |

### SJS status at 2026-05-12

**Exempt.** SJS is under $5M global and $1M in-state CA. EPR is a monitoring item, not a filing.

### Trigger condition (when EPR becomes a real workflow)

The EPR threshold monitor task (`EPR — Threshold Monitor — Annual`) auto-flags when:

- Trailing-12-month sales reach 80% of $5M global, **OR**
- Trailing-12-month CA in-state sales reach 80% of $1M, **OR**
- The 3-year financial plan projects exceeding either threshold in the coming year.

At 80% flag, founder signal fires via ayesha-weekly-briefing seam. Pedrero engages CAA registration walk-through. Sub-skill workflow (per-state registration, packaging-weight reporting, fee payment) does not exist at v6.6 — built when threshold approaches.

### Risk surface

CAA reportedly maintains brand-side data and coordinates with states on fee projections. Lawsuits pending; none yet favorable to brands. Status quo: pay the fee when threshold trips.

## Update protocol

1. New state EPR program → add to "Active states" table; revisit threshold monitor logic.
2. New state packaging toxics legislation → add to scope; surface to Pedrero for verbiage update.
3. CA SB 343 Pantone gradient revision → Heather (Pedrero) supplies updated gradient; repeat portfolio sweep.
4. SJS sales projection crosses 80% of EPR threshold → escalate to Operator + founder signal; build EPR registration workflow.
5. Update `last_updated`.
