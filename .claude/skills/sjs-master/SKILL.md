---
name: sjs-master
description: >
  Brand-level master router for Sweet July Skin's full skills system. Use when a
  request could touch more than one sub-system (PD, Ops, Margin, Quality,
  Regulatory, Comp/Retail intel, Founder briefing, Brand), when the right
  sub-system is ambiguous, or when a cross-system handoff is in play (concept
  approval that should fire margin checks, complaint that may route back to PD,
  signed approval that triggers production PO, etc.). This router holds no
  domain data — all canonical references live alongside the router and in PLM.
  When a sub-system router clearly owns the request, defer to it; this router
  only fires for genuinely cross-system or ambiguous cases. Org-level requests
  (board reporting, multi-brand consolidation, holiday comms) belong to the
  future `ac-brands-master` org router, not this one.
---

# Sweet July Skin — Master Router

This is the brand-level routing layer for the Sweet July Skin skills system. It does one job: look at a request and either route it to the right sub-system router, or coordinate a cross-system handoff. It never holds canonical data — names, GIDs, products, vendors, brand spec, style rules — those live in the support files alongside this router and in PLM, where every skill reads them at runtime.

The router runs **silently**. Don't announce which sub-system you're consulting; just deliver the answer.

---

## Read these at runtime

Every session that activates this router should pull current state from the support files alongside this SKILL.md:

- `system_map.md` — every skill, which system, dependencies
- `bridge_queue_contract.md` — canonical map of bridge → Asana queue → router/skill that picks up
- `gids.md` — Asana / PLM identifiers
- `style_rules.md` — banned words, formatting, status update titles, vendor terminology
- `tool_patterns.md` — Fireflies/Outlook/Asana/PLM working patterns, lip program vendor logic
- `automations.md` — daily PD recap, weekly briefing, etc.

Vendors, products, suppliers, contacts, and partners are read live from Supabase, not from files:

```sql
SELECT id, name FROM public.vendors;                                     -- material / component vendors
SELECT id, sku, name FROM public.products;                                -- portfolio
SELECT slug, title, content FROM public.wiki_pages WHERE page_type='supplier';  -- supplier scope detail
SELECT slug, title, content FROM public.wiki_pages WHERE page_type='partner';   -- contractors, labs, 3PLs, tooling
SELECT slug, title, content FROM public.wiki_pages WHERE page_type='contact';   -- people, internal + external
```

The four bridges load these at run time. (Retired `senders.md`, `products.md`, and `suppliers.md` on 2026-05-26 — see `Bridge-and-System-Audit-2026-05-26.md` Priority 1. Lip turnkey/non-turnkey logic and banned "vessel" terminology moved to `tool_patterns.md` and `style_rules.md`.)

If a piece of the request needs canonical brand spec, defer to `sweet-july-skin-brand`.

---

## When to fire this router

Fire when any of these are true:

- The request crosses two or more sub-systems ("a complaint just came in that may be a formulation issue")
- The right sub-system is ambiguous from the prompt
- The request is about the system itself (audit, sync, lint, "what skills do I have")
- A cross-system handoff is in play (concept approval, signed approval, formulation root cause, UBM listing readiness)

When the request clearly belongs to one sub-system, defer to that sub-system's router and stay silent here.

---

## Sub-system routing

### PD work — Asana, Fireflies, Outlook, PLM bridges, branded outputs

Route to: `sjs-pd-system`

Triggers: anything about Sweet July Skin product development tasks, projects, portfolio, formulas, supplier emails or calls, PD status updates, branded reports, dashboards, the daily PD sweeps (morning 8 AM, midday 12 PM, EOD reconciliation 4 PM) and the Monday weekly update.

### Ops work — purchasing, inventory, S&OP, freight, DTC fulfillment

Route to: `sjs-ops-system`

Triggers: vendors, POs, RFQs, on-hand position, three-way recon, S&OP forecasts, buy plans, inbound/outbound freight, customs, retailer ASN, daily Logiwa parse, DTC order ops.

### Margin work — pressure-tests, archetype advisory, walk-away, portfolio review

Route to: `sjs-margin-architect`

Triggers: SKU margin questions, channel floor validation, archetype/designation classification, walk-away advisory, quarterly portfolio review, interactive margin model.

### Quality work — System B

Route to: `sjs-quality-system`.

Triggers: customer complaints, allergic reactions, adverse event triage, recall triggers, NCRs, CAPA opening or closeout, root cause analysis, OOS/OOT lab results, vendor flags, vendor scorecard signals, batch holds and releases, in-market stability scheduling, near-expiry quality decisions, SOP catalog queries, SOP ratifications, SOP annual reviews, audit prep, retailer questionnaires, regulatory inspection prep, quality system reviews, QoS rollup, branded quality dashboard. The System B router disambiguates within Quality and forwards to the right sub-skill.

### Regulatory work — System C

Route to: `sjs-regulatory-system`.

Triggers: pre-launch IL review gate, sustained claim substantiation, label artwork archive, retailer attestation responses (Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo), MoCRA serious adverse event filings, FDA recall reporting (Class I/II/III), state adverse event reports (CA/NY/WA/OR), MoCRA cosmetic product listings, MoCRA facility registrations, CA Prop 65, CA Fragrance and Flavor Right to Know Act, CA Toxic-Free Cosmetics Act, WA Toxic-Free Cosmetics Act, OR cosmetic registry, Leaping Bunny Certification, Pedrero liaison work, branded regulatory dashboard. The System C router disambiguates within Regulatory and forwards to the right sub-skill (regulatory-manager, claims-il-and-label-keeper, adverse-event-and-recall-reporter, regulatory-status-reporter).

### Comp / Retail intel — competitive teardowns, retail performance benchmarks

Route to: `sjs-comp-intel` or `sjs-retail-intel`.

Triggers: competitor pricing/positioning/launches, prestige skincare trend signals, UBM launch benchmarks, sell-through and review velocity modeling, promo calendar planning.

### Founder briefing — Ayesha weekly

Route to: `ayesha-weekly-briefing`.

Triggers: "weekly briefing," "Ayesha update," "Slide 5," "founder briefing," anything pointed at the Ayesha Canva deck.

### Brand work — fonts, colors, voice, output styling

Route to: `sweet-july-skin-brand`.

Triggers: any output deliverable for Sweet July Skin (deck, doc, PDF, HTML, email styled for the brand). The brand skill is also a dependency loaded by output-producing skills in other systems.

### Utility — ingredient lookup, find/replace, skill building

Route directly to `sjs-ingredient-lookup`, `asana-find-replace`, or `skill-creator`.

### Holiday comms — annual (org-level)

Route to: `ac-brands-holiday-comms`. This is the only org-level skill that fires from the brand router; it stays here until the org-tier `ac-brands-master` ships, at which point it migrates.

---

## Cross-system handoffs

When a single request triggers handoffs across systems, the master router coordinates the sequence. The handoff playbook lives in `system_map.md` under "Cross-system handoffs"; here are the most common paths.

### Concept approval (PD → Margin)

Trigger: an Asana task moves to concept approval, or Alvin signs off a new SKU at intake.

Sequence:
1. PD: Skill 1 logs the concept approval
2. Margin: `sjs-margin-archetype-advisory` recommends archetype + Standard/Acquisition
3. Margin: `sjs-margin-pressure-test` validates channel floors
4. If pressure-test fails: `sjs-margin-walk-away`
5. PD: Skill 5 surfaces the result in the next status update

### Signed Approval (PD → Ops)

Trigger: Formula Tracker moves to Signed Approvals.

Sequence:
1. PD: Skill 1 records the stage move
2. PD: Skill 4 syncs approval to PLM phase
3. Ops: `purchasing-manager` opens the production PO workflow
4. Ops: `supply-demand-planner` validates forecast and buy plan
5. PD: Skill 5 includes in next launch readiness report

### Complaint with formulation signal (Quality → PD)

Trigger: complaint trend on a SKU, or CAPA root cause = formulation.

Sequence:
1. Quality: complaint or CAPA logged via the relevant Quality skill
2. Master router flags formulation root cause
3. PD: Skill 1 opens a reformulation task
4. PD: Skill 4 logs the linked complaint/CAPA reference to PLM
5. Margin: re-run `sjs-margin-pressure-test` on any reformulated SKU

### UBM listing readiness (PD → Retail Intel)

Trigger: SKU enters the launch readiness window for Ulta Beauty Marketplace.

Sequence:
1. PD: Skill 1 confirms launch window
2. Retail Intel: `sjs-retail-intel` runs cohort positioning + price ladder
3. PD: Skill 5 incorporates retail benchmarks into Launch Readiness Report

### Weekly Founder Briefing (PD → Ayesha)

Trigger: Friday weekly briefing.

Sequence:
1. PD: Skill 1 sweeps PD Portfolio for founder-level signal
2. Ops: parallel sweep of OC3PL Order Management + Shipping Dashboard
3. `ayesha-weekly-briefing` synthesizes into the current week's Canva deck Slide 5
4. PD: Slide 6 is co-owned with Nicole — Ops contributes signal but Nicole has the pen

---

## Confirmation rules

This router does no writes itself. Sub-system routers and individual skills handle their own HITL approval per their own rules. Reads are always fine without confirmation.

The one exception: when the master router coordinates a multi-skill cross-system sequence, surface the full sequence to Alvin first and confirm before kicking off step 1.

```
🔀 Cross-system handoff:
[step 1] — owner: [skill]
[step 2] — owner: [skill]
[step 3] — owner: [skill]

Run the sequence?
```

---

## When to defer instead of route

If the request clearly belongs in one sub-system and the sub-system router is going to do the right thing, just defer. Do not narrate. Do not announce "I'm checking the PD router." Just answer.

The master router earns its keep on the genuinely cross-system requests. For the daily flow of "what's overdue," "log this email," "pull action items from yesterday's meeting," the sub-system routers do the work and the master is invisible.
