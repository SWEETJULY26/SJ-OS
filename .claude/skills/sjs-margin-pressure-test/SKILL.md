---
name: sjs-margin-pressure-test
description: >
  Pressure-test a Sweet July Skin SKU (real or hypothetical) against every
  channel floor and the specialty prestige stress test. Use when Alvin asks
  to run the numbers on a SKU, validates a proposed price, or evaluates
  channel readiness. Triggers on phrases like "run the numbers on the eye
  cream", "can we launch this at $42", "what's the margin on the Soursop
  Serum at Sephora", "is this Sephora-ready", "is this specialty-prestige
  ready", "pressure-test the new toner", "what's the COGS ceiling for a
  $45 hero", "would this clear at Ulta Marketplace", "do the math on this
  SKU", "show me the margin waterfall". Also fires when asana-pd-manager
  flags a SKU at concept approval and needs preliminary margin validation.
  Reads landed COGS from PLM Supabase via SELECT. Output is a channel-by-
  channel pass/fail table with walk-away recommendations for any failures.
---

# SJS Margin — Pressure Test

You run a single SKU against every channel floor and the specialty prestige
stress test. Output is a structured pass/fail table with walk-away paths
for any failures.

For framework rationale or edge cases, consult the `architect` skill in
this plugin (`sjs-margin-architect`) and its `references/
framework.md`.

---

## When to run

- Alvin asks to evaluate a specific SKU's margin position.
- A new SKU is at concept approval and needs preliminary validation.
- A pricing proposal needs a math check before going to Soraya (Marketing Manager) and Danielle (President).
- A wholesale offer comes in and needs a "can this SKU ship there" answer.

---

## Inputs you need

- **Product identifier** — name or SKU (find in PLM `products` table).
- **MSRP** — committed (`current_price`) or proposed (`target_msrp`, or
  user-provided for hypotheticals).
- **Archetype + commercial designation** — read from PLM if assigned;
  otherwise recommend per the `sjs-margin-architect` skill's `references/archetype-rules.md` and flag as
  unratified.
- **Landed COGS** — best source in order: (1) `target_landed_cogs`,
  (2) latest `batches.unit_cost_actual`, (3) BOM subtotal from
  `bill_of_materials` JOIN `components`, (4) derived from MSRP with
  caveats. **Always flag the source.**

---

## SQL patterns (PLM Supabase, project `ujkabbffvhpewpbttmmy`)

```sql
-- Product identity, pricing, archetype
SELECT id, name, sku, current_price, target_msrp,
       archetype, commercial_designation, target_landed_cogs,
       product_status, current_phase
FROM products
WHERE name ILIKE '%<search>%' OR sku = '<sku>';

-- BOM subtotal (formula + components, excludes fill/freight/duty)
SELECT p.name, p.sku,
       SUM(bom.quantity * COALESCE(bom.unit_cost_override, c.unit_cost)) AS bom_cogs_subtotal
FROM products p
JOIN bill_of_materials bom ON bom.product_id = p.id
JOIN components c ON c.id = bom.component_id
WHERE p.id = '<product-uuid>'
GROUP BY p.id, p.name, p.sku;

-- Component breakdown for composition analysis
SELECT c.component_type, c.name, bom.quantity, c.unit,
       COALESCE(bom.unit_cost_override, c.unit_cost) AS unit_cost,
       (bom.quantity * COALESCE(bom.unit_cost_override, c.unit_cost)) AS line_cost
FROM bill_of_materials bom
JOIN components c ON c.id = bom.component_id
WHERE bom.product_id = '<product-uuid>'
ORDER BY c.component_type, c.name;
```

You **read only**. Any writes to PLM go through `plm-assistant`.

---

## The run

### Step 1 — Confirm setup

Pull MSRP, archetype, designation, and landed COGS. If archetype or
designation is unset, recommend per the `sjs-margin-architect` skill's `references/archetype-rules.md` (one-
sentence test) and flag as Perrine + Soraya's call to ratify (Alvin admin, Nicole consults, Danielle approves). If landed
COGS is missing, flag the data gap and use the best derivable estimate.

### Step 2 — Channel floor checks

For **Standard** designation, run against all 4 channel categories.
For **Acquisition** designation, skip per-channel floors; check unit
contribution against the $2.00 absolute floor at each channel.

Channel-net midpoints:
- DTC: 92% | Ulta Marketplace: 81% | TikTok Shop: 60%
- Amazon FBA: 60% | Amazon FBM: 65% | Goody: 85%
- Specialty prestige: 36% | Indie/boutique: 52%

GM floors (Standard):
- Direct: 72% | Marketplace: 60% | Wholesale: 55% | Acquisition: blended

For Acquisition designation, compute unit contribution = `channel_net −
landed_cogs`, pass = `≥ $2.00`.

### Step 3 — Specialty prestige stress test (always run)

```
ceiling = MSRP × 0.162
pass = landed_cogs ≤ ceiling
```

If SKU isn't launching to specialty prestige, a fail here is not a blocker
— but it IS a named constraint on future channel strategy. Surface it.

### Step 4 — Composition band check (only if BOM available)

Pull component breakdown, compute each component's % of landed COGS,
compare to archetype's bands in the `sjs-margin-architect` skill's `references/archetype-rules.md`. Out-of-
band components flag as "conversation required" per Section 5.5 — they
do not block, but they do trigger a named "why?".

### Step 5 — Output

Format:

```
PRESSURE TEST — <Product Name> (<SKU>)

Setup:
  MSRP: $X (band: <archetype band>)
  Landed COGS: $Y (source: <real / BOM subtotal / derived>)
  Archetype: <formula_hero | ritual_hero | accessory | bundle> (<confirmed | recommended>)
  Designation: <standard | acquisition> (<confirmed | recommended>)

MSRP band check: <PASS / BELOW BAND / ABOVE BAND>

Channel floors:
┌─────────────────────────┬────────┬──────────┬───────┬──────────┐
│ Channel                 │ Net %  │ GM floor │ GM %  │ Result   │
├─────────────────────────┼────────┼──────────┼───────┼──────────┤
│ DTC                     │ 92%    │ 72%      │ XX%   │ PASS/FAIL│
│ Ulta Marketplace        │ 81%    │ 60%      │ XX%   │ PASS/FAIL│
│ TikTok Shop             │ 60%    │ 60%      │ XX%   │ PASS/FAIL│
│ Amazon FBA              │ 60%    │ 60%      │ XX%   │ PASS/FAIL│
│ Specialty prestige      │ 36%    │ 55%      │ XX%   │ PASS/FAIL│
│ Indie/boutique          │ 52%    │ 55%      │ XX%   │ PASS/FAIL│
└─────────────────────────┴────────┴──────────┴───────┴──────────┘

Specialty prestige stress test: <PASS / FAIL — ceiling $X, actual $Y>

Composition (if BOM available):
  Formula:       X% (in band / above ceiling / below floor)
  Primary pack:  X% (...)
  ...

Recommended paths (failures only):
  <Path 1: ...>
  <Path 2: ...>

Owner routing (per Section 7.2):
  <decision>: <owner>
```

Keep it tight. No preamble. If a SKU clears every check, say so in one
line. If it fails, the table tells the story; the path recommendations
make it actionable.

---

## Edge cases

- **Hybrid SKU** — apply hybrid composition bands per Section 5.4 ONLY
  if `archetype_modifier` is explicitly set in PLM. Don't infer.
- **Acquisition SKU** — show the per-channel GM% for context, but evaluate
  pass/fail against $2.00 unit contribution, not GM floors.
- **Bundle** — evaluate against weighted average of constituent SKUs'
  channel-net GMs, adjusted for bundle discount. Fetch all constituent
  SKUs first.
- **Data missing** — never fabricate. State what's missing and what you
  can/can't compute as a result.

---

## Hand-offs

- **Floor break → walk-away advisory needed:** invoke
  `sjs-margin-walk-away` with the failing SKU and channel.
- **Output needs branded format:** hand off to `sjs-status-reporter`.
- **PLM write needed** (e.g., commit a target_landed_cogs after
  pressure-test confirms): hand off to `plm-assistant`.
- **Asana update needed** (e.g., post pressure-test result as comment
  on a PD task): hand off to `asana-pd-manager`.

---

## Wiki context (runs before live queries)

Before running live Supabase or PLM queries, read the relevant pages from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as bridge skills process supplier cost emails, margin reviews, and meeting traffic. Reading them first gives this skill institutional memory about cost history, channel performance, archetype, and past margin decisions without re-scanning raw sources.

### Which pages to read

- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`
- Named supplier (when cost shifts are in play) → `'supplier/' || public.wiki_slugify(vendor_name)`

SKU pages carry cost history, channel performance, archetype, and past margin decisions. Supplier pages carry cost-increase history, MOQ changes, and tariff signals.

### Read query

```sql
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'sku/' || public.wiki_slugify('{sku_code_or_product_name}'));

SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before running the margin check. Treat it as the SKU's margin history briefing.

### Write-back (stale pages only)

If a page is stale or `source_count = 0` and live queries produced genuine new margin signal not already in the wiki, update the page:

```sql
UPDATE wiki_pages
SET content = '{updated synthesized content}',
    source_count = source_count + 1,
    last_source = 'manual',
    last_source_ref = 'retrieval-skill-writeback',
    updated_at = now()
WHERE slug = '{slug}';
```

Only on genuine new signal. Never on every read.

### What this skill does NOT do

- Does not create new wiki pages (bridge skills own all wiki writes)
- Does not write to wiki on every invocation — only on genuine stale updates
- Does not replace live Supabase or PLM queries for current cost and channel state
