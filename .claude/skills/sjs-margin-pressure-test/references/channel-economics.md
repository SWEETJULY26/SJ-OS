# Channel Economics — Fast Lookup

Source: framework Sections 1 and 4. Use for routine floor checks without
re-reading the full framework. When an answer requires rationale or
edge-case reasoning, read `framework.md` instead.

All floors are **on channel-net revenue**, NOT on MSRP.

---

## Channel-net ranges (what SJS keeps from MSRP)

| Channel | Net to SJS | Category |
|---|---|---|
| sweetjulyskin.com DTC | 90–94% | Direct |
| Ulta Beauty Marketplace | 80–82% | Marketplace |
| TikTok Shop (in-app) | 55–65% | Marketplace |
| Amazon 3P FBA | 55–65% | Marketplace |
| Amazon 3P FBM | 60–70% | Marketplace |
| Goody | 85% (of gift value) | Acquisition |
| Specialty prestige wholesale | 32–40% | Wholesale |
| Indie/boutique wholesale (Hosa tier) | 47–57% | Wholesale |

**Amazon 1P:** deliberately out of scope. Do not model.

**Meta/Facebook/Instagram:** acquisition layer only; checkout is DTC.
Spend lives in CAC, not channel deductions.

---

## GM floors by channel category (for Standard-designation SKUs)

| Category | GM floor on channel-net |
|---|---|
| Direct | **72%** |
| Marketplace | **60%** |
| Wholesale | **55%** ⚠️ load-bearing number |
| Acquisition | blended (see 1.7 / 4.4) |

### Archetype adjustments

- **Accessory at wholesale:** 50% (vs. 55% standard) — soft-goods retail
  logic runs lower margins than beauty.
- **Bundle floor:** evaluated as weighted average of constituents'
  channel-net GMs, adjusted for bundle discount.

---

## Absolute contribution floor

**$2.00 per unit minimum**, applies to ALL SKUs including Acquisition-
designated SKUs running on blended logic. Below $2.00/unit, SJS is
effectively paying customers to take the product.

⚠️ Load-bearing number. Benchmark starting value, re-examined annually.

---

## Acquisition-mix cap

**≤ 25% of revenue** from sub-floor SKUs/channels (trailing 12 months).
Above 25%, portfolio is structurally under-margined and escalates.

⚠️ Load-bearing number.

---

## The specialty prestige stress test (Section 4.6)

Runs against every new SKU at concept, regardless of whether specialty
prestige is in launch plan.

**Formula:**

```
landed_cogs_ceiling = MSRP × 0.36 × 0.45
                    = MSRP × 0.162
```

Where:
- 0.36 = midpoint of specialty prestige channel-net range (32–40%)
- 0.45 = 1 − 55% (wholesale GM floor inverted)

**Worked examples:**

- $30 MSRP → **$4.86** landed COGS ceiling
- $45 MSRP → **$7.29** landed COGS ceiling
- $55 MSRP → **$8.91** landed COGS ceiling

If SKU's landed COGS exceeds ceiling at concept, options are:
reformulate, reprice upward, or tag as DTC/marketplace-only with
documented specialty-prestige walk-away.

---

## Quick landed-COGS-ceiling calculations by channel

For a given MSRP, what landed COGS does the SKU need to stay under to
clear each channel's floor?

| Channel | Formula | $30 MSRP | $45 MSRP | $55 MSRP |
|---|---|---|---|---|
| DTC (72% floor, 92% net) | MSRP × 0.258 | $7.74 | $11.61 | $14.19 |
| Ulta Marketplace (60% floor, 81% net) | MSRP × 0.324 | $9.72 | $14.58 | $17.82 |
| TikTok Shop (60% floor, 60% net) | MSRP × 0.240 | $7.20 | $10.80 | $13.20 |
| Amazon FBA (60% floor, 60% net) | MSRP × 0.240 | $7.20 | $10.80 | $13.20 |
| Specialty prestige (55% floor, 36% net) | MSRP × 0.162 | $4.86 | $7.29 | $8.91 |
| Indie/boutique (55% floor, 52% net) | MSRP × 0.234 | $7.02 | $10.53 | $12.87 |

**The binding floor is specialty prestige at 16.2% of MSRP.** A SKU that
clears specialty prestige clears every other channel.

---

## Walk-away paths when a floor breaks (Section 4.7 / 7.3)

1. **Reformulate** — reduce landed COGS. Perrine (PD owner) with Alvin (PD admin) and sourcing; Nicole consults.
2. **Reprice** — lift MSRP into band. Alvin with Soraya (Marketing Manager); Danielle (President) approves.
3. **Restrict** — tag SKU as DTC/marketplace-only. Alvin with commercial; Danielle (President) approves.
4. **Retire** — discontinue. Alvin with Perrine (PD owner) and Soraya (Marketing Manager); Nicole consults; Danielle (President) approves.

Order of preference: as listed for Standard SKUs. For Acquisition SKUs,
restrict comes before reformulate.

"Note it and continue" is **not a permitted response.**
