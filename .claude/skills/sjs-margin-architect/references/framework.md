# Sweet July Skin — Margin Architecture Framework

**Status: DRAFT v1.0 — not yet ratified by leadership.**

This document captures the seven sections of the SJS margin architecture as
drafted in the 2026-04-20 scoping session. It serves as the source of truth
for the `sjs-margin-architect` plugin until the leadership-ratified version
replaces it.

The ratification loop: Alvin, Nicole, and Soraya review the companion Word
document (produced in Build 1) and mark up / sign off. The signed-off version
gets reformatted into this file and the DRAFT banner is removed.

---

## Load-bearing numbers flagged for review

These five figures carry the weight of the architecture and are the most
likely to shift in leadership review. Treat as **benchmark starting values**:

1. **55% GM floor at wholesale** (Section 4.2)
2. **$2.00 absolute per-unit contribution floor** (Section 4.5)
3. **12% creator/affiliate commission ceiling at marketplace** (Section 6.3)
4. **25% acquisition-mix cap** (Section 1.7)
5. **Composition bands** (Section 5.3)

---

# Section 1: Channel Universe & Channel Economics

## 1.1 The channels in scope

Sweet July Skin's channel architecture spans two states: **current** (what SJS
sells through today) and **future** (what SJS is building toward). Both must
be modeled, because SKUs priced correctly for the current mix will fail when
the future channels open, and SKUs priced for the future will starve in the
meantime.

**Current channels** are sweetjulyskin.com DTC (inclusive of Meta and other
ad-driven traffic that checks out on-site), TikTok Shop (in-app checkout),
Ulta Beauty Marketplace, Amazon 3P (FBA and FBM), and Goody. **Future
channels**, on a 12–36 month horizon, are specialty prestige wholesale
(Sephora, Ulta main floor, Credo, Goop, Bluemercury) and indie/boutique
wholesale at the Hosa tier.

A note on Meta: Instagram and Facebook Shops are connected to the Shopify
catalog, but checkout happens on sweetjulyskin.com. Economically, Meta is an
**acquisition layer**, not a distinct channel — the cost of Meta traffic
lives in CAC and marketing P&L, not in channel deductions.

Explicitly out of scope: international distribution, club and mass retail,
professional/treatment-room, and **Amazon 1P** (deliberate — retained as a
named exclusion to protect MAP and avoid friction with future Sephora/Ulta
relationships).

## 1.2 Why channels matter architecturally

A SKU that earns a healthy 70% gross margin today at DTC and Marketplace can
fall to 30% gross margin on the same landed COGS when it moves to Sephora.
The margin architecture exists to prevent that transition from being a
surprise.

## 1.3 Channel economics — the real numbers

The following are the channel-net benchmarks SJS designs against. Signed
deals and actual channel performance may deviate; the benchmarks become the
anchor, and live numbers replace them as available.

- **sweetjulyskin.com DTC** — Shopify fixed cost, 2.9% + $0.30 processing,
  3–5% returns, brand-subsidized shipping. **Net to SJS: 90–94% of MSRP.**
- **TikTok Shop (in-app)** — platform fees, creator commissions when
  creator-driven, higher return rates than DTC. **Net to SJS: 55–65% of
  MSRP** (wide — creator-heavy runs to the low end).
- **Ulta Beauty Marketplace** — 18% platform fee, SJS fulfills. **Net to
  SJS: 80–82% of MSRP.** Economically sits close to DTC; do not confuse
  with main-floor Ulta.
- **Amazon 3P (FBA)** — 15% referral + $3–6/unit FBA + 5–8% returns +
  10–15% ad spend. **Net to SJS: 55–65% of MSRP.** Assume low end until
  SJS's actual economics are modeled.
- **Amazon 3P (FBM)** — 15% referral + SJS fulfillment + ad spend, no FBA
  fee but no Prime badge. **Net to SJS: 60–70% of MSRP.**
- **Goody** — revenue-share at SJS's negotiated rate; SJS drop-ships.
  **Net to SJS: 85% of gift value** (15% to Goody). Processing fee paid
  by purchaser, not brand.
- **Specialty prestige wholesale** (Sephora, Ulta main, Credo, Goop,
  Bluemercury) — 50% off MSRP keystone, 5–10% trade, 2–5% returns &
  damages, 1–3% chargebacks/compliance, 3–8% sampling obligations. **Net
  to SJS: 32–40% of MSRP.** The floor-setting channel.
- **Indie/boutique wholesale (Hosa tier)** — 40–50% off MSRP, minimal
  trade, no chargebacks, 2–3% returns. **Net to SJS: 47–57% of MSRP.**

## 1.4 What "margin floor" means in this framework

Margin floors are set against **net revenue** — what SJS actually keeps from
a sale after channel deductions — not against MSRP. The distinction is
critical: a SKU running 75% gross margin on MSRP at DTC can run 45% gross
margin on net revenue at specialty prestige wholesale off the same landed
COGS.

## 1.5 Goody as acquisition channel

Goody is treated as an **acquisition channel** rather than a margin channel.
Its strategic purpose is to place SJS product in front of corporate-gifting
recipients — a distinct, high-value customer segment — and generate
second-order DTC repeat from those recipients. Acquisition channels don't
need to clear the standard per-unit margin floor in isolation; they clear
a blended floor alongside the downstream customer value they generate.

## 1.6 Channel classification summary

For architectural purposes, the channels cluster into four categories:

- **Direct** (~90–94% net): sweetjulyskin.com DTC. Meta, Google, organic,
  email all land here.
- **Marketplace** (~55–82% net): Ulta Beauty Marketplace, TikTok Shop,
  Amazon 3P FBA, Amazon 3P FBM. Shared features: SJS retains seller-of-
  record, controls MSRP, pays platform percentage.
- **Wholesale** (~32–57% net): specialty prestige and indie/boutique
  (future). Shared features: SJS loses pricing control, absorbs
  trade/returns/chargebacks.
- **Acquisition** (blended margin): Goody today; potentially corporate
  gifting partnerships, sampling platforms, influencer seeding programs
  at scale in the future.

## 1.7 The portfolio floor approach

The architecture is governed by a **blended portfolio floor** rather than
per-SKU enforcement, on three structural guardrails:

1. **Acquisition-mix cap.** No more than **25% of revenue** may come from
   SKUs or channels running below the standard per-SKU floor. Above that
   threshold, the portfolio is structurally under-margin'd and the
   architecture escalates to leadership for rebalance.

2. **Absolute contribution floor.** Even acquisition SKUs and acquisition
   channels cannot run below an absolute contribution margin floor per
   unit (set in Section 4.5). Below that line, SJS is paying customers
   to take the product.

3. **Annual re-examination.** Acquisition designation is not permanent.
   Every SKU and every channel tagged as acquisition gets re-examined
   annually.

Further, two principles govern the whole architecture:

- **The framework must hold at the channel SJS is building toward, not
  just the channel SJS is shipping to today.** When Sephora or Ulta main
  floor makes an offer, SJS knows within an hour which SKUs can ship at
  those terms and which cannot.
- **The founder-funded runway buys strategic time, not margin tolerance.**
  Design the model as if the founder weren't backing it, even while the
  founder is backing it.

---

# Section 2: Archetype Classification

## 2.1 Why the portfolio needs archetypes

Accessible-prestige brands that serve a portfolio cannot be governed by a
single set of margin and COGS rules, because the cost profile of products
inside the portfolio is fundamentally different. A formula-hero serum has
different COGS composition than a ritual-hero lip treatment, and treating
them identically produces wrong architecture.

## 2.2 Two orthogonal dimensions: Archetype and Commercial Designation

Every SKU carries two classifications that govern different things:

- **Archetype** = COGS composition and product narrative. Governs cost-
  lever permissions and what the product is telling the customer it *is*.
  Values: **Formula-Hero, Ritual-Hero, Accessory, Bundle.**

- **Commercial Designation** = margin treatment and strategic role.
  Governs which margin floor the SKU must clear. Values: **Standard,
  Acquisition.**

Under this model, a lip treatment is *Ritual-Hero / Acquisition*. The Pava
Toner Spray is *Formula-Hero / Standard*. A hypothetical future clinical-
actives SKU priced below floor to drive category entry would be *Formula-
Hero / Acquisition* — the framework handles it without a bolt-on exception.

## 2.3 Archetype definitions

- **Formula-Hero.** The one-sentence description leads with an active,
  a percentage, a clinical claim, or a functional mechanism. Cost
  signature is actives-forward.
- **Ritual-Hero.** The description leads with a sensory, experiential,
  or format claim. Cost signature is experience-forward.
- **Accessory.** Not a formulated cosmetic — soft goods, hard goods,
  tools. Operates on landed-cost logic rather than beauty logic.
- **Bundle.** A curated multi-SKU set priced off the sum of constituent
  MSRPs. Inherits composition from constituents plus a bundle-specific
  packaging component.

## 2.4 Hybrid treatment

Some SKUs carry a **primary archetype and a secondary modifier**. A serum
with a premium dropper and an ornate bottle has formula-hero economics
with ritual-hero packaging spend. The primary archetype governs MSRP band
and margin floor; the secondary modifier allows a specific composition
band exception (see 5.4) without expanding total COGS envelope.

Hybrids are named exceptions, not default settings. If more than ~20% of
the portfolio needs hybrid treatment, the archetypes are wrong.

## 2.5 Classification rules for new SKUs

Every new SKU entering development gets an archetype assignment during
concept approval, **before the BOM is locked**. The archetype assignment
is a decision about what story the SKU is telling and what cost levers
it's permitted to pull — it cannot be assigned retroactively to justify
a COGS overrun.

Classification is made by **Nicole (PD lead) and Soraya (brand lead)
jointly** at concept approval, recorded in PLM as two first-class fields
(`archetype` and `commercial_designation`), and cannot be retroactively
changed to justify a COGS overrun.

## 2.6 Draft classification for current portfolio

*For Nicole and Soraya to ratify or revise — not a framework decision.*

- *Formula-Hero / Standard (draft):* Pava Toner Spray, Good Youth Retinol
  Sleep Serum, Soursop Vitamin C Serum, Pava Exfoliating Cleanser,
  Castaway Cleansing Oil, Castaway Cream Daily Moisturizer, Coffee Fix
  Peptide Eye Cream, Irie Power Face Oil
- *Ritual-Hero / Standard (draft):* Pineapple Punch Face Mask (both SKUs)
- *Ritual-Hero / Acquisition (draft):* all 12 lip treatments, Sweet July
  Chapstick, Resurrection Balm (when priced)
- *Accessory (draft):* Face Towel Set, Reusable Face Rounds, Terry Spa
  Headband, Vanity Bag
- *Bundle (draft):* all 8 active bundles

---

# Section 3: MSRP Bands by Archetype

## 3.1 The positioning anchor

SJS is priced to live in the zone between accessible prestige (the $18–38
band occupied by Glow Recipe, Youth to the People, Bubble) and core
prestige (the $38–78 band occupied by Tatcha, Drunk Elephant, Summer
Fridays). Not accessible-prestige — the ticket can't read as entry-level
when the brand is pursuing Sephora and Ulta main floor. But not
core-prestige either, since the customer SJS wants is a recruitment-age
beauty customer who wants prestige *feeling* at a price that doesn't
require a committed decision.

Working price architecture for formulated skincare: **$28 to $58**, with
deliberate tiering. Accessories, bundles, and lip sit outside that band
on their own logic.

## 3.2 The bands

- **Hero (Formula-Hero / Standard):** $46–58. Clinically-led treatments
  where efficacy justifies the ticket. Current SJS SKUs in band: Good
  Youth Retinol Sleep Serum ($55), Soursop Vitamin C Serum ($49), Irie
  Power Face Oil ($48).
- **Core (Formula-Hero / Standard):** $34–42. Daily moisturizers, toners,
  cleansing oils, treatment-cleansers. Current SJS SKUs: Castaway Cream
  ($30), Pava Toner Spray ($30), Castaway Cleansing Oil ($32), Coffee Fix
  Peptide Eye Cream ($34). **Three of four currently below band** —
  material to Section 4.
- **Basics (Formula-Hero / Standard):** $26–32. Entry-tier functional
  SKUs — simple cleansers, basics where the price signal is accessibility.
  Current: Pava Exfoliating Cleanser ($29). In band.
- **Ritual-Hero / Standard:** $34–48. Masks, specialty treatments,
  ritual-forward formats. Current: Pineapple Punch Face Mask ($22 /
  unpriced) — both below band; pricing conversation before launch.
- **Ritual-Hero / Acquisition:** $18–28 typical, but set by commercial
  purpose not band. Current: lip treatments at $20 — defensible under
  blended portfolio logic, makes the blend work harder.
- **Accessory:** $12–48, category-driven, not archetype-driven.
- **Bundle:** 10–15% off sum of constituent MSRPs.

## 3.3 Current-portfolio findings (for Section 4 pressure-test)

- Core tier is underpriced against target architecture (three of four
  SKUs below band).
- Ritual-hero mask tier is underpriced.
- Lip acquisition pricing is defensible at $20 but fragile at wholesale.

## 3.4 Enforcement

Every new SKU entering development has an MSRP assigned at concept
approval inside its archetype band — or, if outside, the exception is
named and justified at the same time the archetype is assigned. Enforced
at PLM level via the `target_msrp` field with archetype-band validation.

---

# Section 4: Target Gross Margin Floors per Channel

## 4.1 What a floor is, and what it is not

A margin floor is the **minimum gross margin percentage a SKU must clear
at a specific channel's net revenue**, before sampling, GWP, and
discretionary discounting are applied. Always expressed in net-revenue
terms, not MSRP.

Floors are not ceilings. A SKU at floor is a SKU on watch. Floors apply
to **Standard** designation SKUs. **Acquisition** SKUs run under blended
portfolio logic (Section 1.7), bounded by the absolute contribution
floor in 4.5.

## 4.2 The channel-level floors

- **Direct channel floor: 72% GM on channel-net.** At 90–94% net-to-MSRP,
  implies landed COGS roughly 24–28% of MSRP for a SKU to be healthy.
  Any SKU failing this floor has a structural problem.
- **Marketplace channel floor: 60% GM on channel-net.** Ulta Marketplace,
  TikTok Shop, Amazon FBA, Amazon FBM. Set against the weighted mid-range
  of a realistic marketplace mix.
- **Wholesale channel floor: 55% GM on channel-net.** Specialty prestige
  and indie/boutique. At 32–40% net-to-MSRP for specialty prestige, the
  55% GM floor means **landed COGS cannot exceed roughly 14–18% of
  MSRP**. For a $45 hero SKU, landed COGS ceiling ~$6.30–$8.10.
- **Acquisition channel floor: blended, not absolute.** Goody and future
  acquisition channels. Evaluated against portfolio blend, bounded by
  acquisition-mix cap (1.7) and absolute contribution floor (4.5).

## 4.3 Archetype-specific adjustments

- **Accessory floor: 50% GM on channel-net at wholesale** (vs. 55%
  standard). Soft-goods retail logic runs lower margins than beauty.
- **Bundle floor: evaluated against component blend**, not standalone.
  Bundle's channel-net GM must equal or exceed weighted average of
  constituent SKUs' channel-net GMs, adjusted for bundle discount.

## 4.4 Acquisition-mix cap

No more than **25% of revenue** from sub-floor SKUs/channels. Above that,
the portfolio is structurally under-margined and escalates. Measured on
trailing 12-month basis at quarterly portfolio review.

## 4.5 Absolute contribution floor

**$2.00 per unit** minimum contribution margin. Even acquisition SKUs on
acquisition channels cannot run below this. Below $2.00 per unit, SJS is
effectively paying customers to take the product.

*This is a benchmark starting value, not a fixed-forever number. To be
re-examined annually against portfolio volume.*

## 4.6 The specialty prestige stress test

Every new SKU entering development is evaluated against specialty prestige
economics *regardless of whether specialty prestige is in its launch
channel plan*. The stress test:

- Assume **36% channel-net** (midpoint of specialty prestige's 32–40%
  range).
- Apply **55% wholesale GM floor**.
- Derive the **landed COGS ceiling**: MSRP × 0.36 × 0.45 = MSRP × 0.162.
- Compare against SKU's actual or projected landed COGS.

SKUs that fail the stress test at concept get redesigned, repriced, or
deliberately tagged as DTC/marketplace-only with a documented walk-away
from specialty prestige.

A SKU deliberately tagged as marketplace-only is a **permitted** outcome —
but must be a named decision at concept, not retroactive rationalization.

## 4.7 Walk-away logic for channel vs. SKU conflicts

Four legitimate paths when a channel's floor and a SKU's economics
cannot be reconciled:

1. **Reformulate** — reduce landed COGS. Owned by Nicole with sourcing.
2. **Reprice upward** — lift MSRP to expand channel-net envelope. Owned
   by Alvin with Soraya.
3. **Restrict channel set** — tag SKU as DTC/marketplace-only. Owned by
   Alvin with commercial leads.
4. **Retire or decline** — when no other path clears. Owned by Alvin
   with Nicole and Soraya.

Order of preference for Standard SKUs: as listed. For Acquisition SKUs:
channel restriction comes before reformulation, because acquisition
narratives usually can't be value-engineered without compromising
commercial function.

## 4.8 Enforcement

- Every new SKU has a **target landed COGS** derived from 4.2 floors, set
  at concept approval as a PLM commitment (field: `target_landed_cogs`).
- Every in-market SKU evaluated quarterly against all four channel floors.
- Every launch-channel decision evaluated against the specialty prestige
  stress test, even for SKUs not launching there.

---

# Section 5: COGS Composition Rules by Archetype

## 5.1 Why composition rules exist

Margin floors tell you *whether* a SKU clears. Composition rules tell you
*how it got there*. Two SKUs can land at the same COGS via radically
different compositions — if the composition doesn't match the archetype,
the product is telling a story its cost structure doesn't back up.

## 5.2 The seven COGS components

Every SKU resolves to seven cost components, tracked on every BOM:

1. **Formula** — bulk product (actives, base, preservative, fragrance).
   For purchased FG, replaced by CM unit cost.
2. **Primary packaging** — contacts/dispenses the formula (tube, bottle,
   jar, pump, dropper, stick mechanism).
3. **Secondary packaging** — over-wrap that houses primary (folded carton,
   sleeve, seal).
4. **Tertiary/shipper** — mailer, corrugate, void fill, inserts.
5. **Fill, labor, QA** — CM charge to fill, cap, label, assemble,
   QA-release.
6. **Freight-in** — inbound from CM or component vendor.
7. **Duty and customs** — import duty, brokerage, harbor fees, tariffs.

## 5.3 The composition bands

Each archetype carries a band for each component. Bands are **% of total
landed COGS**.

### Formula-Hero composition (actives-forward)

- Formula: **30–42%**
- Primary pack: **16–24%**
- Secondary pack: **6–10%**
- Tertiary: **3–6%**
- Fill / labor / QA: **10–16%**
- Freight-in: **4–8%**
- Duty: **0–6%**

### Ritual-Hero composition (experience-forward)

- Formula: **16–24%**
- Primary pack: **28–38%** ← budget lives here
- Secondary pack: **10–16%**
- Tertiary: **4–8%**
- Fill / labor / QA: **10–16%**
- Freight-in: **5–9%**
- Duty: **0–8%**

### Accessory composition (landed-cost-driven)

- Product (sourced good): **55–70%**
- Packaging (primary + secondary): **10–18%**
- Tertiary: **2–5%**
- Fill / labor / QA: **0–4%**
- Freight-in: **8–15%**
- Duty: **3–12%**

### Bundle composition

Bundles inherit composition from constituent SKUs plus:

- Bundle packaging as **% of bundle MSRP** (not of bundle COGS): **2–6%**.
  Above 6% = over-packaged, margin being eaten. Below 2% = doesn't read
  as a bundle.

## 5.4 Hybrid composition modifiers

- **Formula-hero with ritual packaging modifier:** primary pack permitted
  up to **28%** (vs. 24% standard), with additional spend drawn from
  formula (ceiling 38% vs. 42%) or tertiary (ceiling 4% vs. 6%).
- **Ritual-hero with clinical formula modifier:** formula permitted up
  to **28%** (vs. 24% standard), with additional spend drawn from primary
  pack (ceiling 34% vs. 38%) or secondary (ceiling 14% vs. 16%).

**Total COGS envelope does not expand with hybrids — only redistributes.**

## 5.5 What composition rules do and don't do

Composition bands are **review criteria at concept approval and portfolio
review**, not blocking validations. A SKU outside its bands is flagged for
a named conversation — "why is Irie Power Face Oil's primary pack at 27%
when formula-hero ceiling is 24%?" — and proceeds only with an explicit,
recorded justification.

Section 4 floors are **blocking**. Section 5 bands are **conversation-
forcing**.

## 5.6 Volume sensitivity

Every band in 5.3 assumes reasonable volume at the SKU level. Low-volume
SKUs will struggle to fit composition bands because fixed allocations
(tooling amortization, minimum-run fill charges) dominate per-unit COGS.

A SKU projected below minimum viable volume either needs a composition
exception at concept, or needs to be consolidated with another SKU's
component tooling, or needs a different archetype assignment.

---

# Section 6: Promotional & Trade Allowances

## 6.1 What this section governs

Margin floors are set on channel-net *before* sampling, GWP, and
discretionary discounting. This section establishes how much of cleared
margin can be spent back on promotional and trade activity before the SKU
crosses from gross margin into contribution margin trouble.

Every promotional/trade dollar comes from a **named, bounded allowance
per SKU and per channel**, set at concept approval and reviewed annually.

## 6.2 The six P&T line items

1. **Sampling** — deluxe samples, sachets, tester units, gratis for press
   and influencer seeding, retailer sampling program inventory.
2. **Gift-with-purchase (GWP)** — free product with qualifying purchase.
3. **Trade spend** — retailer-facing: slotting, co-op, MDF, end-cap
   fees, in-store sampling obligations, visual merchandising, launch
   support. The cost of being on shelf.
4. **Discretionary discounting** — brand-initiated promotional pricing.
5. **Creator/affiliate commissions** — paid % to creators and affiliates.
   Distinct from paid advertising (CAC) because triggered by sale, not
   impression.
6. **Chargebacks/deductions** — retailer-initiated deductions from
   wholesale invoices.

## 6.3 The allowance ceilings

Expressed as max % of **channel-net revenue** for that SKU at that channel.

### Direct (sweetjulyskin.com)

- Sampling: up to **3%**
- GWP: up to **5%**
- Discretionary discounting: up to **8%** (annualized)
- Creator/affiliate commissions: up to **4%**
- **Combined ceiling: 15%**

### Marketplace (Ulta Marketplace, TikTok Shop, Amazon FBA/FBM)

- Sampling: up to **2%**
- GWP: up to **4%**
- Discretionary discounting: up to **6%**
- Creator/affiliate commissions: up to **12%** (TikTok Shop-heavy line)
- Chargebacks/deductions: up to **3%**
- **Combined ceiling: 22%**

### Wholesale (specialty prestige, indie/boutique)

- Sampling: up to **5%** (retailer programs contractual)
- GWP: up to **3%**
- Discretionary discounting: up to **2%**
- Chargebacks/deductions: up to **4%**
- Trade spend (slotting, co-op, MDF, VM): up to **8%**
- **Combined ceiling: 20%**

### Acquisition (Goody)

- **Combined ceiling: 0%** beyond the channel's own economics.
  Acquisition channels run on acquisition logic; additional stacking
  double-counts the trade.

## 6.4 Launch windows vs. steady-state

Ceilings in 6.3 are **steady-state**, measured on trailing 12 months at
SKU level. Launch windows — first 90 days in-market OR first 180 days
in a specific channel — permit up to **1.5× steady-state combined
ceiling** (e.g., marketplace launch can run 33% combined).

After launch window closes, SKU reverts. **Perpetual launch mode is a
named anti-pattern** (see 7.6) and triggers escalation.

## 6.5 The contribution margin bridge

Every SKU should be measurable through this bridge at every channel:

**MSRP → channel deductions → channel-net → landed COGS → gross margin →
P&T allowances → contribution margin**

A SKU that clears every floor in the bridge (including $2.00 absolute
contribution) is architecturally healthy. Any break flags.

## 6.6 Paid advertising is NOT a promotional allowance

Meta ads, Google ads, Amazon Sponsored Products, TikTok Shop Ads, and
influencer flat-fee partnerships live in **CAC**, not trade. Real cost of
the business, but not covered by this section's ceilings.

**Rule:** if spend is triggered by a sale, it counts against allowance
ceilings. If triggered by an impression, click, or flat fee, it counts
against CAC.

## 6.7 Enforcement

- Every SKU carries an **allowance budget at launch**, per-channel,
  recorded in PLM alongside archetype and COGS target.
- Quarterly review measures actual P&T spend against ceilings at
  SKU×channel level.
- Launch-window exceptions named at launch, close at 90-day (or 180-day
  channel entry) mark. No silent rollover.

---

# Section 7: Walk-Away Rules & Governance

## 7.1 What governance means

Sections 1–6 are rules. Section 7 is what happens when rules meet reality
— when a SKU breaks a floor, when a channel shifts, when a retailer
demands margin that doesn't pencil, when a commercial lead wants to
override a constraint.

Without explicit governance, frameworks become advisory. With explicit
governance, they become load-bearing.

Governance has four components: **decision rights**, **escalation paths**,
**review cadence**, **amendment process**.

## 7.2 Decision rights

- **Archetype and commercial designation** (Section 2): **Nicole
  (PD) + Soraya (brand)** jointly, at concept approval, recorded in PLM.
  Cannot be changed retroactively without named review.
- **MSRP and band placement** (Section 3): **Alvin** with input from
  Soraya and commercial leads. Out-of-band exceptions require named
  justification at concept approval.
- **Landed COGS target** (Section 4, Section 5): **Nicole** with
  sourcing. Derived from MSRP and channel floors. Set at concept approval
  as PLM commitment.
- **Channel set at launch** (Section 4.6, 4.7): **Alvin** with commercial
  leads. Restrictions from specialty prestige are named with documented
  rationale.
- **Allowance budget** (Section 6): **Alvin + commercial/brand leads**
  jointly. Named at launch, measured quarterly.
- **Exception approval for any framework rule**: **Alvin**, with Nicole
  and Soraya for archetype/COGS exceptions, commercial leads for
  channel/margin exceptions. Exceptions are named, bounded, time-limited,
  logged.
- **Framework amendment**: **Alvin**. Annual review. Process in 7.5.

## 7.3 The four-path escalation model

When a SKU breaks a floor, a composition band (outside a permitted
modifier), or an allowance ceiling (outside a named launch window), one
of four paths is taken. **No fifth path — "note it and continue" is
not permitted.**

1. **Reformulate.** Reduce landed COGS. Nicole with sourcing. Documented
   as reformulation work order in PLM with target completion date.
2. **Reprice.** Lift MSRP. Alvin with Soraya. Documented as repricing
   decision with effective date and channel rollout plan.
3. **Restrict.** Remove SKU from failing channel. Alvin with commercial
   leads. Documented as channel restriction in PLM with named rationale.
4. **Retire.** Discontinue or decline to ship. Alvin with Nicole and
   Soraya.

## 7.4 Review cadence

**Quarterly portfolio review** runs the full sweep: every SKU against
every floor, acquisition-mix cap check, perpetual-launch-mode check,
composition band audit.

Any SKU failing any test is flagged with a 7.3 recommendation. Portfolio
review also surfaces channel-level patterns (wholesale floor holding in
aggregate? acquisition-mix trending toward 25%? CAC creeping into trade?).

Produces a short **margin architecture report** each quarter — a one-page
status with exceptions named and paths recommended. Archived via
`sjs-status-reporter`. Leadership closes or extends exceptions at review,
creating a recorded decision trail.

## 7.5 Amendment process

Three types of change distinguished:

- **Numeric recalibration** (floor %, composition bands, allowance
  ceilings, $2.00 floor): annual, Q4 review. Owned by Alvin. Logged as
  version update to plugin's reference files.
- **Structural change** (adding/retiring archetype, adding channel
  category, changing decision-rights, changing escalation paths): owned
  by Alvin with Nicole and Soraya. Requires named rationale and
  before/after doc. Triggered by new channel category opening, new
  archetype emerging, or commercial model shift.
- **Scope expansion** (adding out-of-scope channels — international,
  club, mass, pro): triggered only by strategic decision, not
  opportunistic offer. Single one-off opportunity is named exception,
  not amendment trigger.

## 7.6 Anti-patterns the architecture resists

- **Perpetual launch mode.** A SKU that never exits its launch-window
  allowance ceiling. Symptom: 12-month trailing allowance stays at 1.5×
  steady-state quarter after quarter, each justified by "we're still
  building the SKU."
- **Retroactive archetype change to justify COGS overrun.** Blocked by
  7.2 — archetype is assigned at concept, cannot be changed to rationalize
  a BOM that drifted.
- **Allowance creep into CAC (or vice versa).** Blocked by 6.6's
  sale-vs-impression rule.
- **Quiet floor drift.** Blocked by 7.3 — "note it and continue" is not
  a permitted response.
- **Founder-backstop rationalization.** The architecture's hardest
  discipline is designing the model as if the founder weren't backing it,
  even while the founder is backing it.

---

*End of framework v1.0 DRAFT.*
