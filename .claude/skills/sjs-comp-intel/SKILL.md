---
name: sjs-comp-intel
description: >
  Run competitive intelligence for Sweet July Skin. Use whenever Alvin asks about quarterly
  competitor teardowns, monthly category trend digests, launch cadence or innovation pipeline
  tracking, what Rhode/Summer Fridays/Kosas/LANEIGE/YTTP are doing, prestige skincare trend
  shifts, or whether a competitor move should flag into the Margin, Retail Performance, or
  Consumer & Category streams. Triggers on phrases like "what's the comp set doing", "pull
  the trend digest", "time for the Q[N] teardown", "is [brand] promoting", "what did Rhode
  just launch", "run the quarterly on Summer Fridays", "update the pipeline tracker", or any
  request to monitor, analyze, or flag competitor activity in prestige skincare.
---

# Sweet July Skin — Competitive Intelligence

This skill runs the Competitive Intelligence workstream inside the SJS Margin & Market Research project. It is the fourth of five research streams and deliberately runs on a monthly rhythm, not on depth bursts.

## What this skill does

Three sub-streams, one sustainable cadence.

**Monthly trend digest** — two to three page forwardable brief covering one ingredient, one format, one claim pattern, one sustainability move, and the "what it means for SJS" analytical layer. Ships by the 5th of each month. Source: `references/templates/monthly-trend-digest-template.md`.

**Quarterly teardown** — eight to twelve page deep read on each of the five comp brands covering launches, pricing, packaging, retail footprint, social, and earned media. Ships end of month one in each quarter. Source: `references/templates/quarterly-teardown-template.md`. Cohort anchors in `references/comp-brands/`.

**Pipeline tracker** — emergent rollup of launch data from the quarterly teardowns, refreshed quarterly starting in month five. Not a separate research effort. See `references/sequencing-plan.md`.

## The comp cohort

Five brands total. Three direct, two aspirational. Do not expand past five without approval — the cadence breaks above that.

**Direct comps**
- **Rhode** — closest structural analog (founder led celebrity skincare, lip led acquisition strategy, DTC to Sephora pivot). Primary watch.
- **Summer Fridays** — benchmark for hero SKU led portfolio economics and lip as acquisition.
- **Kosas** — only founder led Ulta native brand in the tier. Best signal for Ulta merchant behavior toward brands that look like SJS.

**Aspirational**
- **LANEIGE** — category defining lip balm at Ulta. Not a peer but unignorable for lip strategy.
- **Youth to the People** — the disciplined 18 month pipeline model. What legible innovation pacing looks like at prestige scale.

Profiles live in `references/comp-brands/`. Rhode is fully populated as the working template; the other four are skeletons populated during first quarterly teardowns.

**Explicitly not in the cohort**: Fenty Skin (scale mismatch), Drunk Elephant (established, L'Oréal pace), Glow Recipe (over analyzed, Summer Fridays covers archetype better), The Ordinary (mass prestige, distracts price ladder work), Topicals (different category focus).

## Ownership

- **Stream DRI**: Nicole Iturbe (Sr. Director Consumer Strategy & Ops)
- **Sub-stream 1 (quarterly teardowns) owner**: Soraya Salgadoe (Marketing Manager)
- **Support**: Kate Le (Social Media Coordinator) on the social and content pillars across both teardowns and digest
- **Sign-off**: Alvin on quarterly teardowns before they circulate to Danielle and the SJS brand team

Details in `references/team-ownership.md`.

## Tooling POV

Skip Mintel and Spate for year one. Free plus lightweight paid stack does 80% of the work. Total year one budget: $8K to $15K.

- **Free layer**: Glossy, BoF Beauty, Beauty Independent, BeautyMatter, Retail Dive, WWD Beauty, CosmeticsDesign, Sephora/Ulta/Amazon new arrival pages, Wayback Machine, Reddit r/SkincareAddiction and r/beautyguruchatter, founder podcasts.
- **Lightweight paid**: Glossy Pro, BeautyMatter Pro, Dash Hudson starter or equivalent social listening, Helium 10 for Amazon.
- **Heavyweight (skip year one)**: Mintel, Spate, WGSN, LaunchMetrics full, BeautyStreams, Tribe Dynamics.

Full source catalog in `references/source-stack.md`.

## Cross-stream handoff rules

CI is the connective tissue between the other four streams. Standing rules:

- **To Margin Architecture**: any competitor pricing move that would invalidate a margin floor gets flagged within two weeks. Any competitor packaging or formula change that shifts category cost benchmarks goes to margin within a month.
- **To Retail Performance Intelligence**: price ladder data lives in retail intel, not CI — consume and extend, don't rebuild. Monthly pricing surveillance feeds into retail intel's promo calendar. The retail intel 10 brand cohort is the canonical universe; CI's five is the deep watch tier inside it.
- **To Consumer & Category Research**: trend digest feeds whitespace analysis. When C&C identifies a consumer gap, CI validates whether competitors are already addressing it. Claims direction flows from CI to C&C (what is every comp claiming) not the other way.

Rules and exchange formats in `references/cross-references.md`.

## Cadence and sequencing

Standing calendar:
- **By the 5th of every month**: monthly trend digest delivered to Danielle and the SJS brand team
- **End of month one in each quarter** (Jan, Apr, Jul, Oct): quarterly teardown delivered for all five brands
- **End of Q1 each year**: pipeline tracker refreshed (starting Q1 2027, after back catalog build in late 2026)

Build sequencing in `references/sequencing-plan.md`. Short version: digest and teardown templates built in parallel months 1 and 2, first digest ships month 2, first full teardown ships month 4, pipeline emerges as rollup month 7 onward.

## Dashboard

The CI Dashboard (HTML, maintained alongside this skill) is the at-a-glance surface for Alvin. It shows the five comp brands, the cadence tracker, the current trend digest, active cross-stream flags, and the pipeline tracker preview. The dashboard reads from the same source data the skill references produce; keep them in sync.

## When invoked, follow this logic

1. **Routine monthly digest request** — open `references/templates/monthly-trend-digest-template.md`, ask which sources have been scanned this month, produce the digest. Flag anything that should route to another stream.
2. **Quarterly teardown request** — open `references/templates/quarterly-teardown-template.md`, ask which of the five brands to start with, produce teardown section by section. Cross reference against the brand's profile in `references/comp-brands/` for "what changed since last quarter."
3. **Ad hoc competitor question** — check the relevant profile in `references/comp-brands/`, supplement with web search for freshness, answer the question, update the profile if new information warrants.
4. **"What should we flag" request** — scan recent activity against `references/cross-references.md` rules, surface any unrouted signals.
5. **Dashboard refresh** — pull current state from references, regenerate the HTML dashboard. Keep the design system consistent with the existing dashboard file.

## Output formatting rules

Applies to every CI deliverable Alvin receives:
- No hyphens. Em dashes or rewrite.
- Lead with the bottom line. Insight, action, risk.
- Flag confidence levels. Directional vs confirmed.
- End with a clear next step or decision required.
- Benchmark against prestige skincare specifically.
- Apply Sweet July Skin brand guidelines on formal deliverables going to Danielle or the brand team. Internal working material (Alvin only) stays unbranded.

## What this skill is not

Not a PD management tool. Not a sales data system. Not a retail performance tracker. Those live in `asana-pd-manager`, elsewhere in AC Brands infrastructure, and the Retail Performance Intelligence chat respectively. This skill covers external market surveillance only.
