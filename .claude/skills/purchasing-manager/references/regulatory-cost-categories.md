# Regulatory Cost Categories — Classification Reference

Reference for outlook-plm-bridge Flow I and purchasing-manager Job 9 when classifying vendor invoices. Cost category is **primary spend domain**. The `regulatory_driver` boolean is an **override** that fires regardless of category when the spend is driven by a regulatory requirement.

## The six cost_category buckets

### regulatory
Spend whose primary domain is regulatory. Falls here even when no other domain is involved.

Examples:
- Pedrero Regulatory monthly retainer + filing fees
- Ecomundo Canada compliance work
- UK Responsible Person retainer
- South Africa RP work
- Eurofins compliance testing where the test is run because regulation requires it (CPSR, Canadian notification)
- US state filings (MoCRA-equivalents, packaging EPR registration fees)
- Health Canada notification fees
- Leaping Bunny certification fees
- 19-state packaging toxics certification fees
- CA SB 343 Pantone audit fees
- Quebec French-language compliance review fees

Multi-home: SJS Regulatory Management is primary; no second home unless `linked_sku_id` is set, in which case the SKU's PD project is added.

### quality
Spend whose primary domain is product quality testing and assurance, with no direct regulatory driver.

Examples:
- AMR Labs micro testing on a finished batch
- IKS stability testing (real-time and accelerated) — NON-regulatory driven, e.g., shelf-life confirmation
- Vendor quality audits run for our own assurance
- Vegelabs lab fees for batch QC
- PET testing run for shelf-life (NOT for regulatory CPSR) — defaults to quality unless flagged regulatory_driver

Multi-home: SJS Quality Management is primary; PD project added if `linked_sku_id` set.

**Watch:** PET, RIPT, stability testing, and microbiological challenge work very often have a regulatory driver (CPSR for EU, Canadian notification, etc.). When that's the case, log as `cost_category=quality` but flip `regulatory_driver=true` so Regulatory rollup captures the spend. See "regulatory_driver override" below.

### pd
Spend whose primary domain is product development — formulation, prototyping, sample work, pre-launch development that hasn't yet reached batch production.

Examples:
- KDC-One bench batch development fees
- HCT formula development bench work
- Vegelabs formula bench batches (pre-commercial)
- Sample-only invoice runs from formulators
- AMR Labs PD-stage testing (NOT batch-release testing)
- IKS pre-launch sensory work
- Prototype packaging fees from Element, Impress, CDW for sample runs

Multi-home: PD project for the linked SKU is primary AND the invoice case task gets positioned as a subtask under the master Asana task for that SKU (per purchasing-manager Job 9 multi-home routing matrix). Without `linked_sku_id`, defaults to the SJS Master PD project at root level.

### ops
Spend whose primary domain is operational tooling, infrastructure, or recurring operations costs.

Examples:
- Asana workspace subscription
- Supabase PLM hosting
- Netlify hosting for the landing hub
- Cowork subscription
- Logiwa, ShipStation, OC3PL platform fees
- Fireflies subscription
- Microsoft / Outlook licenses
- AWS / GCP infrastructure costs
- HRIS / payroll platform fees

Multi-home: Ops projects (no single canonical home — purchasing-manager Job 9 routes to the most relevant Ops project for the spend type, or to Master Ops as fallback).

### marketing
Spend whose primary domain is marketing, PR, or commercial activation.

Examples:
- Influencer fees
- PR retainer fees
- Paid media spend (Meta, TikTok, Google)
- Photo / video production for marketing assets
- Sample fulfillment for press / influencer seeding
- Sephora / Ulta co-op marketing line items (when invoiced separately, NOT MAP allowances)
- Brand strategy consultancy fees

Multi-home: SJS Brand / Marketing project. PD project added if a SKU-specific campaign and `linked_sku_id` is set.

### general
Catch-all for spend that doesn't fit a domain bucket. Use sparingly — if a more specific category fits, prefer it.

Examples:
- Legal counsel retainer (non-regulatory, non-IP)
- Accounting / bookkeeping monthly fees
- Office supplies
- General consulting fees that don't fit a domain
- Banking / financial services fees
- Travel and entertainment (when not allocated to a domain project)

Multi-home: AC Brands General project (or single-homed if no AC Brands General Asana surface exists).

## The regulatory_driver override

The `regulatory_driver` boolean flips to `true` whenever the **reason** for the spend is a regulatory requirement, regardless of which `cost_category` bucket holds the primary domain.

When `regulatory_driver=true`, the invoice case task **always** adds Regulatory as a multi-home destination, even if `cost_category` is `quality`, `pd`, or anything else.

Canonical regulatory_driver cases:

| Case | Typical cost_category | Why regulatory_driver fires |
|---|---|---|
| PET (preservative efficacy testing) | quality | Required for EU CPSR; required for Health Canada notification on preservative-containing products |
| RIPT (repeated insult patch testing) | quality | Required for EU CPSR; substantiates safety claims for retailer attestations |
| EU CPSR (Cosmetic Product Safety Report) | regulatory | Direct EU regulatory requirement — usually already in `regulatory` category but flag the driver explicitly so the boolean stays consistent |
| Health Canada notification dossier work | regulatory | Direct Canadian regulatory requirement — usually already in `regulatory` category |
| FDA MoCRA registration fee | regulatory | Direct US regulatory requirement |
| State packaging toxics certification testing | quality OR regulatory | Test is run because state law requires it (CA SB 343, WA RCW 70A, etc.) |
| Microbiological challenge testing for retailer attestation | quality | Test required by Sephora Clean / Ulta Clean attestation language |
| Sample sent to Pedrero for review | regulatory | Direct Pedrero engagement spend |
| Reformulation stability testing post-formula change driven by regulation | quality | Reformulation driven by regulatory exclusion (e.g., CA Prop 65, EU Annex II/III change) |

When in doubt: **if the spend would not exist absent the regulatory requirement, regulatory_driver = true**.

## Classification HITL flow

outlook-plm-bridge Flow I and purchasing-manager Job 9 both stage classification proposals; the Operator approves at the HITL gate before plm-assistant commits. The proposal surfaces:

1. Proposed `cost_category` with one-line reasoning
2. Proposed `regulatory_driver` flag with one-line reasoning when `true`
3. Proposed `linked_sku_id` (if discoverable from the invoice line item or subject)
4. Proposed multi-home Asana routing per the matrix below

The Operator can override any field inline before commit.

## Multi-home routing matrix (canonical)

| cost_category | regulatory_driver | Primary home | Secondary home(s) | Subtask placement |
|---|---|---|---|---|
| regulatory | false | SJS Regulatory Management | linked SKU PD project (if set) | — |
| regulatory | true | SJS Regulatory Management | linked SKU PD project (if set) | — |
| quality | false | SJS Quality Management | linked SKU PD project (if set) | — |
| quality | true | SJS Quality Management | SJS Regulatory Management + linked SKU PD project (if set) | — |
| pd | false | SKU PD project (or Master PD root) | — | Under master Asana task for the SKU when `linked_sku_id` set |
| pd | true | SKU PD project (or Master PD root) | SJS Regulatory Management | Under master Asana task for the SKU when `linked_sku_id` set |
| ops | false | Ops project (routed) | — | — |
| ops | true | Ops project (routed) | SJS Regulatory Management | — |
| marketing | false | SJS Brand / Marketing | linked SKU PD project (if set) | — |
| marketing | true | SJS Brand / Marketing | SJS Regulatory Management | — |
| general | false | AC Brands General | — | — |
| general | true | AC Brands General | SJS Regulatory Management | — |

PD case rule: when `cost_category=pd` and `linked_sku_id` is set, the invoice case task is BOTH multi-homed to the SKU's PD project AND positioned as a subtask under the master Asana task for that SKU. This is the only category with a subtask placement rule.
