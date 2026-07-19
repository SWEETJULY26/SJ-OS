# Archetype & Commercial Designation — Fast Lookup

Source: framework Sections 2, 3, 5. Use for routine classification,
MSRP-band, and composition-band checks. Read `framework.md` for full
rationale and edge cases.

---

## Two orthogonal dimensions

Every SKU carries TWO classifications:

- **Archetype** = COGS composition + product narrative
  - Values: `formula_hero`, `ritual_hero`, `accessory`, `bundle`
- **Commercial Designation** = margin treatment + strategic role
  - Values: `standard`, `acquisition`

Example: Pava Toner Spray = `formula_hero / standard`.
Lip treatment = `ritual_hero / acquisition`.
Hypothetical below-floor clinical-actives entry SKU = `formula_hero / acquisition`.

---

## Archetype classification rules

Apply the one-sentence test to any new SKU:

| If the description leads with... | Archetype |
|---|---|
| An active, a percentage, a clinical claim, or a functional mechanism | **Formula-Hero** |
| A sensory, experiential, or format claim | **Ritual-Hero** |
| A non-formulated good (soft goods, hard goods, tools) | **Accessory** |
| A curated multi-SKU set priced off constituent sum | **Bundle** |

### Hybrid treatment

Some SKUs carry **primary archetype + secondary modifier**. Hybrids are
named exceptions, not defaults. If >20% of portfolio needs hybrid
treatment, archetypes are wrong.

Approved hybrid modifiers:
- **Formula-hero with ritual packaging modifier** — primary pack up to
  28% (vs. 24% standard), offset from formula or tertiary.
- **Ritual-hero with clinical formula modifier** — formula up to 28%
  (vs. 24% standard), offset from primary or secondary pack.

Total COGS envelope does not expand with hybrids; only redistributes.

### Who decides

**Nicole (PD) + Soraya (brand)** jointly, at concept approval, before
BOM is locked. Recorded in PLM as `archetype` and `commercial_designation`
fields. **Cannot be changed retroactively** to justify a COGS overrun.

---

## Commercial designation rules

| Designation | When to assign | Margin treatment |
|---|---|---|
| **Standard** | SKU clears channel floors on its own economics | Per-channel floors enforced (Section 4.2) |
| **Acquisition** | Strategic purpose is funnel entry, volume, virality, or cross-sell — commercial function outweighs margin contribution | Blended portfolio logic, bounded only by $2.00 absolute floor |

### Acquisition guardrails

1. ≤ 25% of revenue from acquisition SKUs/channels (annual).
2. Absolute $2.00/unit contribution floor (still applies).
3. Annual re-examination — not a permanent designation.

---

## MSRP bands by archetype

| Archetype / tier | Band | Logic |
|---|---|---|
| **Hero** (Formula-Hero / Standard) | **$46–58** | Clinically-led treatments where efficacy justifies ticket. Retinol, vit C, peptide, acids. |
| **Core** (Formula-Hero / Standard) | **$34–42** | Daily moisturizers, toners, cleansing oils, treatment-cleansers. |
| **Basics** (Formula-Hero / Standard) | **$26–32** | Entry-tier functional SKUs. Simple cleansers, basics. |
| **Ritual-Hero / Standard** | **$34–48** | Masks, specialty treatments, ritual-forward formats. |
| **Ritual-Hero / Acquisition** | **$18–28** | Set by commercial purpose, not by band. |
| **Accessory** | $12–48 | Category-driven, not archetype-driven. |
| **Bundle** | 10–15% off sum | Off sum of constituent MSRPs. |

### Current portfolio placement (draft per Section 2.6)

**Formula-Hero / Standard (Hero):**
- Good Youth Retinol Sleep Serum — $55 ✓ in band
- Soursop Vitamin C Serum — $49 ✓ in band
- Irie Power Face Oil — $48 ✓ in band

**Formula-Hero / Standard (Core):**
- Castaway Cream Daily Moisturizer — $30 ⚠️ below band
- Pava Toner Spray — $30 ⚠️ below band
- Castaway Cleansing Oil — $32 ⚠️ below band
- Coffee Fix Peptide Eye Cream — $34 ✓ bottom of band

**Formula-Hero / Standard (Basics):**
- Pava Exfoliating Cleanser — $29 ✓ in band

**Ritual-Hero / Standard:**
- Pineapple Punch Face Mask (5-pack) — $22 ⚠️ below band
- Pineapple Punch Face Mask (single) — unpriced

**Ritual-Hero / Acquisition:**
- 12 lip treatments — $20 (defensible but fragile)
- Sweet July Chapstick
- Resurrection Balm (when priced)

**Accessory:**
- Face Towel Set, Reusable Face Rounds, Terry Spa Headband, Vanity Bag

**Bundle:**
- All 8 active bundles

---

## COGS composition bands (% of total landed COGS)

⚠️ These bands are load-bearing numbers. Industry-typical starting points
for accessible-core prestige; likely to need tuning against SJS's actual
supplier base.

### Formula-Hero (actives-forward)

| Component | Band |
|---|---|
| Formula | 30–42% |
| Primary pack | 16–24% |
| Secondary pack | 6–10% |
| Tertiary | 3–6% |
| Fill / labor / QA | 10–16% |
| Freight-in | 4–8% |
| Duty | 0–6% |

### Ritual-Hero (experience-forward)

| Component | Band |
|---|---|
| Formula | 16–24% |
| Primary pack | **28–38%** ← budget lives here |
| Secondary pack | 10–16% |
| Tertiary | 4–8% |
| Fill / labor / QA | 10–16% |
| Freight-in | 5–9% |
| Duty | 0–8% |

### Accessory (landed-cost-driven)

| Component | Band |
|---|---|
| Product (sourced good) | 55–70% |
| Packaging (primary + secondary) | 10–18% |
| Tertiary | 2–5% |
| Fill / labor / QA | 0–4% |
| Freight-in | 8–15% |
| Duty | 3–12% |

### Bundle

- Bundle-specific packaging = **2–6% of bundle MSRP** (not of COGS).
- Above 6%: over-packaged, margin being eaten.
- Below 2%: doesn't read as a bundle.
- Otherwise, bundle inherits composition from constituents.

---

## How to apply composition bands

Composition bands are **conversation-forcing, not blocking** (Section 5.5).

- Section 4 floors = blocking. Fail = named path.
- Section 5 bands = named-conversation-required. Out of band = "why?" with
  recorded justification. Proceeds with documented exception.

Use the band check to diagnose failures: if a SKU fails a Section 4 floor,
run the composition analysis to see which component is out of band.
That's usually where the reformulation lever is.

---

## Volume sensitivity note (Section 5.6)

Composition bands assume reasonable SKU-level volume. Low-volume SKUs
will blow through bands because fixed allocations (tooling amortization,
minimum-run fill charges) dominate per-unit COGS.

A SKU projected below minimum viable volume needs one of:
1. Composition exception at concept (named, bounded).
2. Consolidation with another SKU's component tooling.
3. Different archetype assignment.

Volume threshold varies by format — established per-launch, not in the
framework.
