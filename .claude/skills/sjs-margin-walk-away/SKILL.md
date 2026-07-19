---
name: sjs-margin-walk-away
description: >
  Run the four-path walk-away advisory for a Sweet July Skin SKU that's
  breaking a margin floor, composition band, or allowance ceiling. Use when
  a SKU fails its economics and Alvin needs the legitimate options laid
  out with owners and effort. Triggers on phrases like "what do we do
  about X", "this SKU is breaking floor", "how do we fix the Castaway
  margin", "walk-away on this SKU", "what are our options on the lip
  treatment", "reformulate or reprice", "the eye cream isn't penciling at
  Sephora — now what", or any ask about how to remediate a failing SKU.
  Walks the four paths from framework Section 4.7 / 7.3 (reformulate,
  reprice, restrict, retire) in order of preference, naming owner and
  effort for each, and recommending one based on portfolio role and SKU
  designation. Acquisition SKUs reorder paths (restrict before reformulate).
---

# SJS Margin — Walk-Away Advisory

You walk a failing SKU through the four legitimate paths to remediation
with owner and effort for each, then recommend one. This is not a vibe
check — Section 7.3 of the framework explicitly forbids "note it and
continue" as an outcome.

For framework rationale, consult `sjs-margin-architect` and its
`references/framework.md` Section 4.7 / 7.3.

---

## When to run

- A pressure test (from `sjs-margin-pressure-test`) returned
  a floor failure.
- Quarterly portfolio review surfaced a SKU breaking a floor.
- Alvin asks directly: "what do we do about [SKU]".
- A new wholesale offer requires a SKU at terms its current economics
  can't support.

---

## Inputs you need

1. **The failing SKU** — name and SKU.
2. **The failure** — what floor / band / ceiling broke, at what channel,
   by how much. If only the SKU is named, run `pressure-test` first to
   confirm the failure before recommending paths.
3. **Current state from PLM**:
   - MSRP and archetype band placement
   - Landed COGS and source
   - Archetype + commercial designation
   - Current channel set
   - Latest batch unit cost (for reformulation feasibility)

```sql
SELECT id, name, sku, current_price, target_msrp,
       archetype, commercial_designation, target_landed_cogs,
       product_status
FROM products
WHERE name ILIKE '%<search>%' OR sku = '<sku>';
```

---

## The four paths

### Path 1 — Reformulate

Reduce landed COGS to fit the channel's floor.

- **Math:** target landed COGS = MSRP × channel-net% × (1 − GM floor%).
  E.g., $30 SKU at specialty prestige: $30 × 0.36 × 0.45 = $4.86.
- **Delta:** how much cost-out is needed (current COGS − target).
- **Lever:** identify the most likely lever from the BOM:
  - Formula cost-down (active concentration, supplier swap)
  - Component swap (down-spec primary pack, simplify carton)
  - Volume aggregation (pool tooling across SKUs)
  - Vendor re-sourcing (move from one CM to a lower-cost CM)
- **Owner:** **Perrine (PD owner) with Alvin (PD admin) and sourcing; Nicole consults.**
- **Effort:** typically 2–4 months for meaningful reformulation; longer
  if the active is the issue (need stability testing).
- **Risk:** can compromise the brand narrative if formula is the hero.

### Path 2 — Reprice upward

Lift MSRP to expand the channel-net envelope.

- **Math:** required MSRP = current_landed_cogs / (channel-net% × (1 − GM
  floor%)). E.g., $4.86 COGS at specialty prestige needs MSRP ≥ $30.
- **Band check:** is the new MSRP inside the archetype's band per Section
  3.2?
  - In band → straightforward.
  - Above band → named exception required at Alvin/Soraya level; Danielle (President) approves.
- **Owner:** **Alvin with Soraya (Marketing Manager); Danielle (President) approves.**
- **Effort:** DTC reprice can ship in days; Amazon takes weeks (price
  history); wholesale takes a full buy cycle (months).

### Path 3 — Restrict channel set

Remove the SKU from the failing channel.

- **Outcome:** name the restriction explicitly: "DTC + Ulta Marketplace
  only", "DTC only", etc.
- **Trade-off:** which channels do we lose? Does this constrain future
  channel strategy (e.g., locks SKU out of specialty prestige forever)?
- **Owner:** **Alvin with commercial leads; Danielle (President) approves.**
- **Effort:** low — a PLM flag (`channel_restrictions` field, if exists)
  + documented rationale.

### Path 4 — Retire / decline

Discontinue the SKU or decline to ship it.

- **Pull-through cost:** remaining inventory liquidation, open POs,
  brand messaging, customer comms.
- **Use only when:** Paths 1–3 are exhausted or clearly inapplicable AND
  the SKU's portfolio contribution doesn't justify the architecture
  exception.
- **Owner:** **Alvin with Perrine (PD owner) and Soraya (Marketing Manager); Nicole consults; Danielle (President) approves.**
- **Effort:** medium — inventory wind-down + customer comms + brand
  messaging revision.

---

## Path ordering by designation

**Standard SKUs:** order of preference is as listed: 1 → 2 → 3 → 4.
Reformulate first, reprice second, restrict third, retire as last resort.

**Acquisition SKUs:** order shifts to **Restrict → Reformulate → Reprice
→ Retire**. Reason per framework: acquisition narratives are usually
engineered to a specific commercial function and can't be value-engineered
without compromising what makes them acquisition SKUs in the first place.
Restricting channels preserves the function.

---

## The recommendation

After walking all four paths, **name one** based on:

- SKU's current MSRP position in its archetype band (room to reprice?)
- COGS structure (room to cost-out without breaking the archetype?)
- Channel role (is this SKU's commercial purpose threatened by
  restriction?)
- Portfolio role (is this a hero, a basic, an acquisition driver?)
- Stage (in-market vs. concept — concept SKUs have more reformulation
  runway)

Be explicit. "I recommend Path 2 (reprice to $36) because [reason]" — not
"any of these could work."

---

## Output format

```
WALK-AWAY ADVISORY — <Product Name> (<SKU>)

Failure:
  <Floor / band / ceiling broken> at <channel>
  <Current value> vs. <required value>
  Gap: <amount or %>

Designation: <standard | acquisition>
Path order: <1→2→3→4 | restrict-first for acquisition>

Path 1 — Reformulate:
  Target COGS: $X (delta from current: $Y)
  Likely lever: <formula / pack / volume / vendor>
  Owner: Perrine + Alvin (admin) + sourcing (Nicole consults) | Effort: ~3 months
  Viability: <high / medium / low — and why>

Path 2 — Reprice:
  Target MSRP: $X (delta: +$Y)
  Band check: <in band / above band — exception needed>
  Owner: Alvin + Soraya (Marketing) (Danielle approves) | Effort: <days/weeks/months by channel>
  Viability: <high / medium / low — and why>

Path 3 — Restrict:
  Restrict to: <channel set>
  Channels dropped: <list>
  Future constraint: <e.g., locks SKU out of specialty prestige>
  Owner: Alvin + commercial (Danielle approves) | Effort: low
  Viability: <high / medium / low — and why>

Path 4 — Retire:
  Wind-down: <inventory + POs + comms>
  Owner: Alvin + Perrine + Soraya (Nicole consults, Danielle approves) | Effort: medium
  Viability: <only if 1-3 fail>

Recommendation: Path <N> — <one-sentence rationale>

Decision logging required (no silent drift):
  → PLM update via plm-assistant: <what to log>
  → Asana comment via asana-pd-manager: <task to update>
```

---

## Hand-offs

- **Decision made → log it:** route to `plm-assistant` for the PLM write
  (target_landed_cogs change, channel restriction flag, status change)
  AND to `asana-pd-manager` for the Asana comment on the relevant PD task.
  Both are required — no silent drift.
- **Reformulation chosen → start the work order:** ask `asana-pd-manager`
  to create a reformulation subtask in the relevant SJ SKIN PD project.
- **Decision needs leadership write-up:** hand off to
  `sjs-status-reporter` for branded format.

---

## What this skill won't do

- Make the decision for you. The framework structures the conversation;
  named owners (Section 7.2) make the call.
- Recommend "monitor and revisit" — that path doesn't exist.
- Soften the failure language. If the SKU breaks a floor, it breaks a
  floor. Hedging doesn't change the math.

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
