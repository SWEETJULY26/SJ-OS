---
name: sjs-margin-archetype-advisory
description: >
  Recommend an archetype (formula_hero / ritual_hero / accessory / bundle)
  and commercial designation (standard / acquisition) for a Sweet July
  Skin SKU. Use when Alvin is classifying a new SKU at concept approval
  or asking how an existing SKU should be tagged. Triggers on phrases
  like "is this ritual-hero or formula-hero", "what archetype should the
  new toner get", "should this be Standard or Acquisition", "classify
  this SKU", "is the eye cream a hybrid", "tag the new lip treatment",
  "what's this SKU's commercial designation", "recommend an archetype
  for the cleansing balm", or any question about how to assign archetype
  or commercial designation to a SKU. Always presented as a recommendation
  for Nicole (PD lead) and Soraya (brand lead) to ratify per Section 7.2
  — never as a final assignment. Cannot be changed retroactively per
  Section 2.5; classification must happen before the BOM is locked.
---

# SJS Margin — Archetype & Commercial Designation Advisory

You recommend an archetype and commercial designation for a SKU based
on the classification rules in Section 2 of the framework. Your output
is always a **recommendation for Nicole and Soraya to ratify** — never
a final assignment.

For framework rationale and the full classification logic, consult
`sjs-margin-architect` and its `references/archetype-rules.md`
and `references/framework.md` Section 2.

---

## When to run

- A new SKU is at concept approval and needs an archetype assigned
  before BOM lock.
- An existing SKU has missing classification fields in PLM.
- Alvin asks how a specific SKU should be classified.
- A pressure test or portfolio review surfaces a SKU without a
  classification and needs one to proceed.

---

## Inputs you need

- **Product description** — what is the SKU? Format, ingredients/actives,
  packaging, intended sensory or efficacy story.
- **Strategic role** — is this a hero, a daily essential, a basic, an
  acquisition driver, a portfolio extension?
- **Pricing intent** — at-band MSRP or deliberately sub-band for funnel
  function?
- **PLM state** (if existing SKU):

```sql
SELECT id, name, sku, current_price,
       archetype, commercial_designation,
       product_status, current_phase
FROM products
WHERE name ILIKE '%<search>%' OR sku = '<sku>';
```

---

## Step 1 — Apply the archetype one-sentence test

Ask: in one sentence, what is this SKU?

| If the description leads with... | Archetype |
|---|---|
| An active, a percentage, a clinical claim, or a functional mechanism | **formula_hero** |
| A sensory, experiential, or format claim | **ritual_hero** |
| A non-formulated good (soft goods, hard goods, tools) | **accessory** |
| A curated multi-SKU set priced off constituent sum | **bundle** |

Examples:
- "Vitamin C serum with 15% L-ascorbic acid" → formula_hero (leads with
  active + percentage)
- "Cooling under-eye treatment with metal applicator" → ritual_hero
  (leads with format + experience)
- "Reusable face rounds in organic cotton" → accessory
- "The Hydration Set: cleanser + toner + moisturizer" → bundle

---

## Step 2 — Evaluate for hybrid

If the SKU has BOTH a strong formula story AND significant packaging /
applicator investment, flag hybrid potential:

- **formula_hero with ritual packaging modifier** — actives lead the
  story but the component is doing meaningful work (premium dropper,
  ornate bottle, custom applicator). E.g., a serum in a weighted-glass
  apothecary bottle.
- **ritual_hero with clinical formula modifier** — sensory format leads
  but the actives are credible and substantive. E.g., a luxe lip mask
  with peptides.

Hybrids are **named exceptions**, not defaults. If you're tempted to call
something a hybrid, double-check whether the secondary component is
really meaningful, or just nice. Most SKUs are not hybrids.

If >20% of the portfolio is being classified as hybrid, the archetypes
are wrong (per Section 2.4). Surface this to Alvin if you notice the
pattern.

---

## Step 3 — Assess commercial designation

Ask: what is this SKU's primary commercial purpose in the portfolio?

| Designation | When to assign |
|---|---|
| **standard** | SKU is meant to drive per-unit margin. Carries its own channel economics. Hero, core, basics, ritual-hero standard, most accessories. |
| **acquisition** | SKU's primary purpose is funnel entry, volume, virality, cross-sell, or category-entry — commercial function outweighs margin contribution. |

Acquisition SKUs:
- Run on blended portfolio logic, bounded by the $2.00 absolute floor.
- Subject to the 25% acquisition-mix cap.
- Re-examined annually — not a permanent designation.

Tells that point to acquisition:
- MSRP deliberately set below archetype band.
- Very high projected volume relative to portfolio average.
- Strategic intent to drive trial / repeat / cross-sell explicitly stated.
- Category-entry SKU at sub-band pricing to compete on price visibility.

Tells that point to standard:
- MSRP in archetype band.
- Margin contribution expected to clear floors on its own.
- No explicit funnel-function in the brief.

---

## Step 4 — Sanity check against the portfolio

Pull the current archetype distribution to make sure the recommendation
doesn't skew the portfolio:

```sql
SELECT archetype, commercial_designation, COUNT(*) AS sku_count
FROM products
WHERE product_status = 'active'
GROUP BY archetype, commercial_designation
ORDER BY archetype, commercial_designation;
```

If the recommendation would push acquisition SKUs above 25% of revenue
or push hybrid SKUs above 20% of count, flag it as a portfolio-level
concern that may need leadership attention before classification proceeds.

---

## Step 5 — Output

Format:

```
ARCHETYPE RECOMMENDATION — <Product Name> (<SKU if existing>)

Recommended:
  Archetype: <formula_hero | ritual_hero | accessory | bundle>
  Designation: <standard | acquisition>
  Hybrid modifier: <none | formula_hero_with_ritual_packaging |
                    ritual_hero_with_clinical_formula>

Rationale:
  Archetype: <one-sentence story + cost-lever implication>
  Designation: <one-sentence commercial purpose>
  Hybrid (if any): <why the secondary component is meaningful>

Implications (so the recommendation is informed):
  MSRP band: $<low>–$<high> per archetype-rules.md
  COGS composition: <archetype's spend signature>
  Margin floors: <which floors apply per designation>
  Acquisition treatment (if applicable): blended logic, $2.00 absolute,
    25% portfolio cap

Portfolio context:
  Current acquisition-mix: X% of TTM revenue (cap: 25%)
  Current hybrid count: X of Y active SKUs (ceiling: ~20%)

This is a recommendation for Nicole and Soraya to ratify per Section 7.2.
Final assignment at concept approval, recorded in PLM. Cannot be
retroactively changed to justify COGS overruns per Section 2.5.

Next step: Nicole + Soraya confirm; assignment logged to PLM via
plm-assistant (fields: archetype, commercial_designation,
archetype_modifier).
```

---

## Hand-offs

- **Once Nicole + Soraya ratify:** route to `plm-assistant` to write
  the `archetype` and `commercial_designation` fields to the product
  record. Use UPDATE with the audit trail.
- **If concept approval is in Asana:** route to `asana-pd-manager` to
  comment the ratified classification on the relevant PD task.
- **If recommendation triggers a pressure test:** route to
  `sjs-margin-pressure-test` for the channel-floor sweep.

---

## What this skill won't do

- Make the assignment final. It's always Nicole + Soraya's call.
- Recommend a hybrid to make a borderline call easier — hybrids are
  named exceptions, not a third bucket.
- Re-classify an already-ratified SKU to fix a downstream problem.
  Section 2.5 explicitly forbids retroactive archetype changes to
  justify COGS overruns. If a ratified archetype no longer fits, the
  conversation is "do we have the wrong product" or "do we have the
  wrong cost target", not "let's re-tag it."
