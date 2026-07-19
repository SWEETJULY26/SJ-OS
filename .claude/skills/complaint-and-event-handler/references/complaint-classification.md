# Complaint classification — field map and recommendation logic

Mirrors the live custom-field schema on the **SJ Skin Complaint Log** Asana project (gid `1204763097184846`). Pulled 2026-04-28. If options drift, refresh this file before writing.

## Field map

| Field | Type | Purpose | Notes |
|---|---|---|---|
| Complaint Date | date | When the customer experienced the issue | Distinct from task creation date |
| Priority level? | enum | Triage urgency | High / Medium / Low |
| Complaint Type | multi_enum | Classification | Four options below |
| First Response Corrective Action | multi_enum | What we're doing about it | Four options below |
| Customer name | text | Free text | |
| Product Sales Channel | multi_enum | Where they bought it | Amazon / SJ Oakland / Web Store |
| Invoice/Order Number | number | Cross-reference to fulfillment record | |
| Product Name | enum | SKU involved | Full active SKU list (cleansers, toners, oils, serums, creams, eye cream, four lip treatments) |
| Product Batch Code | text | Batch lookup key | Pivots into PLM batch context via plm-assistant |

## Sections (workflow stages)

`New feedback` → `Backlog` → `Actioning` → `Not actioning` → `Completed`

The intake form drops everything into `New feedback`. The skill never modifies sections; it moves tasks between them based on operator decisions.

## Complaint Type — current options

1. **Product Performance Issues** — ineffective results, drying, greasy texture, peeling, residue or white cast, breakouts
2. **Skin Reactions & Irritations** — allergic reactions, burning sensation, excessive dryness, unusual skin discoloration, increased sensitivity
3. **Packaging & Application Issues** — broken or defective packaging, leakage or spillage, hard to dispense, inaccurate product labeling, difficulty applying (too thick, runny)
4. **Fragrance & Sensory Complaints** — strong or unpleasant scent

## First Response Corrective Action — current options

1. **Return** — customer returns the product, refund issued
2. **Exchange** — customer returns the product, replacement sent
3. **Replace and no return** — replacement sent, no return requested (low-value or contamination concerns)
4. **No action needed** — informational, customer satisfied with response, no remediation

## Type-to-action recommendation map

These are recommendations — the operator decides. Multi-enum allows stacking (e.g., Replace and no return + Return).

| Complaint Type | Default first-response recommendation | Reasoning |
|---|---|---|
| Product Performance Issues | Exchange (or Return if customer prefers refund) | Performance is subjective; offer remedy without disposing of product |
| Skin Reactions & Irritations | Replace and no return | Do not require customer to return product they reacted to. Flag for SAE review if reaction is severe (see SKN-OPS-002) |
| Packaging & Application Issues | Replace and no return | Low-cost remedy; flag for batch quality pattern check |
| Fragrance & Sensory Complaints | No action needed (with apology) or Replace and no return | Often subjective; pattern across multiple complaints on same batch flags formula or storage issue |

## Skin Reactions — escalation path

Any complaint classified as **Skin Reactions & Irritations** must be checked against SAE keywords before closing first-response. The skill scans the description for: hospitalization, ER, emergency room, anaphylaxis, swelling, blistering, scarring, infection, or any phrase suggesting medical intervention. If matched, escalate to Job 4 (SKN-OPS-002 walk). The operator decides severity at Initial Assessment; the skill does not auto-classify SAE level.

## Trend analysis thresholds (defaults)

These are starting defaults. The operator can override per ask.

- **Single batch:** 3+ complaints in 30 days → CAPA brief drafted
- **Single SKU, single complaint type:** 5+ complaints in 30 days → CAPA brief drafted
- **Single channel, single type:** 10+ complaints in 30 days → flag to operator for fulfillment QoS check (Amazon-only spike often signals a logistics issue, not a product issue)
- **Skin Reactions, single SKU:** 2+ in 30 days → flag to operator for batch + formula check, regardless of severity

Below threshold, the skill surfaces the trend in routine reports but does not draft a CAPA.

## Refresh procedure

When custom-field options shift (new SKU added, new complaint type, new corrective action option), refresh this file before the next intake run. Pull current schema via Asana API (`asana_get_project` with `opt_fields=custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_options.gid`). Update tables above. Increment the "pulled" date in the header.
