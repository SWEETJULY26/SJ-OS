---
name: sjs-margin-interactive-model
description: >
  Open the Sweet July Skin interactive margin model — a live, on-brand HTML
  tool for tuning MSRP, COGS, archetype, and channel mix and seeing pass/fail
  + contribution margin flow live. Use when Alvin wants to play with the
  numbers, model a what-if, demo the framework to leadership, or stress-test
  a hypothetical SKU visually rather than as a chat-based pressure test.
  Triggers on phrases like "open the margin tool", "show me the model",
  "let me play with the numbers", "interactive margin", "open the
  calculator", "pull up the model on the eye cream", "demo the framework",
  "what if we priced this at $48", "model the wholesale scenarios", "give me
  the visual one". Renders the HTML tool inline as an artifact. Can pre-load
  with real PLM data if a SKU is named (pulls landed COGS via Supabase
  SELECT, populates archetype + designation if assigned). For pure chat
  pressure-tests without UI, use sjs-margin-pressure-test instead.
---

# SJS Margin — Interactive Model

You open the on-brand interactive margin model — an HTML tool that lets the
user tune MSRP, COGS, archetype, designation, and hybrid modifier and
watch every channel's pass/fail status, contribution margin bridge, and
COGS composition update live.

This is the visual companion to `sjs-margin-pressure-test`. Same
math, same framework rules — but rendered as an interactive UI rather than
a chat table. Use this skill when Alvin wants to tune values, demo to
leadership, or model what-ifs. Use the chat pressure-test when he just
wants the numbers fast.

For framework rationale, consult `sjs-margin-architect` and its
`references/framework.md`.

---

## When to run

- Alvin asks to open the model, the calculator, the visual tool, or
  anything that signals he wants to *interact* rather than read output.
- Demo context — leadership review, brand team walkthrough, a
  conversation where moving sliders is more useful than a static table.
- What-if scenarios where multiple variables are in play and the
  conversation will iterate ("what if we lifted MSRP by $6 and dropped
  formula by 15%").
- A pricing decision that needs to be socialized — easier to share a
  link to the tool with a pre-loaded scenario than a chat transcript.

---

## How to render the tool

The tool lives at `references/margin-model.html` in this skill — a
single self-contained HTML file with embedded Sweet July Skin brand
fonts (Adrianna + GT America Expanded), live calculations, and an SVG
contribution margin waterfall.

**Render path:**

1. Read `references/margin-model.html`.
2. Output it as an HTML artifact in the conversation. The user can
   interact with sliders, dropdowns, and channel selection live.
3. If the user named a specific SKU, pre-populate the inputs by editing
   the default values in the HTML's initial state object before
   rendering. See "Pre-loading with PLM data" below.

The artifact renders inline — the user clicks, types, and drags sliders
to explore the model.

---

## Pre-loading with PLM data (when a SKU is named)

If Alvin says "open the model on the Castaway Cream" or similar, pull
the SKU's data from PLM before rendering and modify the initial state.

```sql
-- Pull SKU pricing + classification
SELECT id, name, sku, current_price, target_msrp,
       archetype, commercial_designation,
       target_landed_cogs
FROM products
WHERE name ILIKE '%<search>%' OR sku = '<sku>';

-- Pull landed COGS source (precedence)
-- 1. target_landed_cogs from products (if set)
-- 2. Latest batches.unit_cost_actual
-- 3. BOM subtotal:
SELECT SUM(bom.quantity * COALESCE(bom.unit_cost_override, c.unit_cost))
       AS bom_cogs_subtotal
FROM bill_of_materials bom
JOIN components c ON c.id = bom.component_id
WHERE bom.product_id = '<product-uuid>';
```

In the HTML, find the `INITIAL_STATE` JS object near the bottom of the
`<script>` block and update these fields:

- `productName` — SKU display name
- `msrp` — current_price or target_msrp
- `landedCogs` — best-source landed COGS
- `archetype` — formula_hero / ritual_hero / accessory / bundle (or null
  if unset — the tool will show "unset" and recommend)
- `designation` — standard / acquisition (default to 'standard' if unset)

Note in your message which fields came from PLM and which were
defaulted/derived, so the user knows what's authoritative vs. assumed.

---

## What the tool computes

For every channel selected, live:

- **Channel-net**: MSRP × channel-net %
- **Gross margin %**: (channel-net − landed COGS) / channel-net
- **Pass/fail vs. floor**: per channel category (Direct 72%, Marketplace
  60%, Wholesale 55%, Acquisition $2.00 absolute)
- **Clearance margin**: how many percentage points above the floor
- **On-watch flag**: passes but within 5pts of floor
- **Specialty prestige stress test**: MSRP × 0.162 vs. landed COGS
- **Contribution margin** at steady-state allowance ceiling per channel
  category (Section 6.3)
- **MSRP band check**: in-band, above, or below the archetype's band
- **COGS composition vs. archetype bands** (if components are entered)

All calculations match the framework exactly. No drift between this
tool's math and the chat pressure-test math.

---

## When NOT to use this skill

- Quick floor check ("is this SKU healthy at Sephora") — use
  `pressure-test` for the table.
- Walk-away advisory ("what do we do about X") — use `walk-away`.
- Quarterly portfolio review — use `portfolio-review`.
- Archetype classification — use `archetype-advisory`.

The interactive model is for **exploration and tuning**. The other
operational skills are for execution.

---

## Hand-offs

- **A scenario in the model becomes a real decision** — log via
  `plm-assistant` (target_landed_cogs commit, MSRP update, etc.).
- **Demo deliverable for leadership** — capture the scenario and hand
  to `sjs-status-reporter` for branded write-up.
- **Asana logging** for any decision made from a tool session — via
  `asana-pd-manager`.

---

## Limitations (be honest about them)

- The tool does not pull historical revenue or actual allowance spend —
  it works on framework ceilings, not actuals.
- Bundle SKUs are not modeled (need constituent SKU economics first).
- The 5 load-bearing numbers are framework starting values; the tool
  uses them but flags them visually so the user knows they're under
  review.
- Allowance ceilings used in the contribution bridge are the steady-
  state ceilings from Section 6.3, not the launch-window 1.5× ceilings.
