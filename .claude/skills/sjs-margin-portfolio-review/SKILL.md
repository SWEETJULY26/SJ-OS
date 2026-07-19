---
name: sjs-margin-portfolio-review
description: >
  Run the quarterly Sweet July Skin margin portfolio review and produce
  the one-page margin architecture report. Use when Alvin asks for the
  quarterly review, the portfolio sweep, or the margin architecture
  report. Triggers on phrases like "run the quarterly review", "pull the
  margin architecture report", "how is the portfolio against the
  framework", "do the quarterly portfolio sweep", "acquisition-mix check",
  "perpetual launch mode audit", "where does the portfolio stand", "what's
  our wholesale-readiness", "are we drifting on margin", "Q[X] review
  for SJS". Sweeps every active SKU against every channel floor, runs the
  4 portfolio-level checks (wholesale floor hold, specialty prestige
  readiness, acquisition-mix cap, perpetual launch mode), and outputs a
  4-traffic-light report with exceptions named and walk-away paths
  recommended. Hands off to sjs-status-reporter for branded output.
---

# SJS Margin — Quarterly Portfolio Review

You run the full portfolio sweep against the ratified framework and
produce the margin architecture report — a one-page status with
exceptions named and paths recommended.

For framework rationale, consult `sjs-margin-architect` and its
`references/framework.md` Section 7.4.

---

## When to run

- End of each fiscal quarter.
- Alvin explicitly asks ("pull the margin architecture report", "run the
  quarterly", "how's the portfolio").
- A material event triggers an off-cycle review (new channel opening,
  major repricing decision across the portfolio, founder-funding shift).

---

## Inputs

- All active SKUs from PLM
- Trailing 12-month revenue by SKU × channel (if available)
- Trailing 12-month allowance spend by SKU × channel (if available)

---

## Step 1 — Pull the active portfolio

```sql
SELECT id, name, sku, current_price,
       archetype, commercial_designation, target_landed_cogs,
       product_status, current_phase
FROM products
WHERE product_status = 'active'
ORDER BY archetype, current_price DESC;
```

If `archetype` or `commercial_designation` is missing on >10% of active
SKUs, flag the data gap explicitly in the report — the review can't
fully run without those classifications.

---

## Step 2 — Pull landed COGS for each SKU

Per-SKU precedence:
1. `products.target_landed_cogs` if set
2. Latest `batches.unit_cost_actual` for the product
3. BOM subtotal from `bill_of_materials` JOIN `components` (flag as
   "BOM subtotal — excludes fill, freight, duty")
4. Derived from MSRP using channel floors (flag as "derived")

If COGS is missing for >10% of active SKUs, flag the data gap.

---

## Step 3 — Per-SKU floor checks

For each SKU, run against all four channel categories using the floors
from the `sjs-margin-architect` skill's `references/channel-economics.md`:

- DTC: 72% GM on 92% net
- Marketplace: 60% GM on weighted-mid net
- Wholesale: 55% GM on 36% specialty prestige net (binding)
- Acquisition: $2.00 absolute contribution floor

Pass/fail per SKU × channel. Calculate clearance margin (GM% above floor).

---

## Step 4 — Four portfolio-level checks

### Check 1 — Wholesale floor hold

% of active Standard SKUs passing the 55% wholesale floor.

- 🟢 Green: ≥ 85%
- 🟡 Yellow: 70–85%
- 🔴 Red: < 70%

### Check 2 — Specialty prestige readiness

% of active Standard SKUs passing the specialty prestige stress test
(landed_cogs ≤ MSRP × 0.162).

- 🟢 Green: ≥ 85%
- 🟡 Yellow: 70–85%
- 🔴 Red: < 70%

### Check 3 — Acquisition-mix cap

% of trailing-12mo revenue from SKUs tagged Acquisition OR from channels
classified as Acquisition (currently Goody).

- 🟢 Green: ≤ 20%
- 🟡 Yellow: 20–25%
- 🔴 Red: > 25% (triggers Section 1.7 escalation — portfolio is
  structurally under-margined)

### Check 4 — Perpetual launch mode

Count of SKUs where trailing-12mo allowance spend exceeds 1.0×
steady-state ceiling for 4+ consecutive quarters (the launch-mode
allowance is 1.5× per Section 6.4; "perpetual" means staying above
steady-state long after launch is over).

- 🟢 Green: 0 SKUs
- 🟡 Yellow: 1–2 SKUs
- 🔴 Red: 3+ SKUs

---

## Step 5 — Composition band audit (if BOMs available)

For SKUs with full BOMs in PLM, run the composition check from
the `sjs-margin-architect` skill's `references/archetype-rules.md`. Count out-of-band components.

- 🟡 Yellow: > 15% of active SKUs have at least one out-of-band component
- 🟢 Green: ≤ 15%

This is a soft check — Section 5 bands are conversation-forcing, not
blocking. Surface the top 3 most material out-of-band components
specifically.

---

## Step 6 — Surface exceptions

For each SKU failing any check, prepare a recommended path. Don't run
the full walk-away advisory inline — invoke `sjs-margin-architect:walk-
away` for any SKU that needs a full path workup.

---

## Step 7 — Produce the report

Format (one page):

```
MARGIN ARCHITECTURE REPORT — Q<N> 20<YY>

Portfolio health (4 traffic lights):
  Wholesale floor hold:          [🟢 / 🟡 / 🔴]  X% of SKUs clearing
  Specialty prestige readiness:  [🟢 / 🟡 / 🔴]  X% stress-test ready
  Acquisition-mix cap:           [🟢 / 🟡 / 🔴]  X% of TTM revenue (cap: 25%)
  Perpetual launch mode:         [🟢 / 🟡 / 🔴]  X SKUs in pattern

Exceptions requiring decision:
  • <SKU name> — <issue> — recommended path: <reformulate / reprice /
    restrict / retire>, owner: <name per 7.2>
  • <SKU name> — <issue> — ...

Composition audit:
  X of Y active SKUs have components out of archetype bands.
  Top 3 most material:
    1. <SKU> — <component> at X% (band ceiling Y%)
    2. ...

Data gaps (if any):
  • Missing landed COGS: X SKUs (list)
  • Missing archetype/designation: X SKUs (list)
  • Missing allowance tracking: X SKUs (list)

Load-bearing numbers under pressure (per Section 7.5):
  <Any of the 5 flagged numbers trending toward revision>

Quarter-over-quarter delta:
  <Direction of each traffic light vs. last quarter — improving,
  steady, degrading>
```

---

## Step 8 — Hand off to brand format

Always invoke `sjs-status-reporter` to apply the Sweet July Skin brand
guidelines (Pava Brown cover, Bone interior, Soursop accents, Adrianna
typography) before delivering to leadership.

The report is for: Alvin (VP of Operations), Perrine (PD owner), Nicole
(PD consult), Soraya (Marketing Manager), Danielle (President), and any
leadership review attendees. It creates the recorded decision trail per
Section 7.4.

---

## Hand-offs

- **Per-SKU walk-away needed:** invoke `sjs-margin-walk-away`
  for each exception requiring full path analysis.
- **Branded format:** invoke `sjs-status-reporter`.
- **Asana logging:** via `asana-pd-manager` — one Asana task per
  exception with the recommended path, assigned to the named owner.
- **PLM updates** (if review reveals stale data, missing COGS, etc.):
  via `plm-assistant`.

---

## Edge cases

- **First quarterly review** — no Q-over-Q delta exists. State that and
  establish the baseline.
- **Data gaps too severe** — if >25% of active SKUs are missing critical
  data (COGS or archetype), pause the report and surface the data
  problem instead. A report on bad data is worse than no report.
- **Mid-quarter request** — clarify whether Alvin wants the formal
  quarterly or an interim snapshot. The interim snapshot has the same
  format but is labeled as such.

---

## Wiki context (runs before live queries)

Before running the portfolio sweep, read every active SKU page from `public.wiki_pages`. Wiki pages are synthesized margin briefings that compound as bridge skills process cost emails, channel reviews, and meeting traffic. Reading them first gives this skill a one-shot picture of cost history, archetype, and past margin decisions across the portfolio without re-scanning raw sources per SKU.

### Which pages to read

- All SKU pages — `p_page_type => 'sku'` with `p_limit => 50` (raise if portfolio grows)
- Suppliers tied to flagged SKUs (after the sweep, if a cost or MOQ thread needs context) — `'supplier/' || public.wiki_slugify(vendor_name)`

### Read query

```sql
-- Pull all SKU pages
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_page_type => 'sku', p_limit => 50);

-- Drill into a supplier referenced by a flagged SKU
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries for that SKU. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally for that SKU. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Use the SKU pages as the portfolio briefing layer. The framework checks (wholesale floor hold, specialty prestige readiness, acquisition-mix cap, perpetual launch mode) still run against live PLM data — the wiki pages contextualize *why* a SKU sits where it sits.

### Write-back (stale pages only)

If a SKU page is stale and the sweep surfaced genuine new margin signal not already in the wiki, update the page:

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
- Does not replace live PLM channel-floor checks — wiki is briefing, framework is the test
