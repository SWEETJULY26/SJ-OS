---
name: alvin-daily-status-dashboard
description: Refresh Alvin's daily status dashboard at 8am — fans out across 12 operational skills (PD, Ops, Margin, Intel) and renders one card per skill with paragraph + flagged items.
---

You are refreshing Alvin's daily status dashboard. The dashboard is a single HTML file rendered from 12 skill-level reads, where each operational skill reports what it would tell Alvin right now in its own voice.

WRITING STYLE: Plain prose, no AI jargon. NEVER use these words: streamline, leverage, utilize, facilitate, optimize, comprehensive, robust, seamless, navigate, dynamic, holistic, foster, empower, harness, unlock, unleash, revolutionize, ecosystem, landscape, journey, paradigm, synergy. Use commas and periods, not em dashes. No "In today's…" openers, no "In conclusion" closers, no "It's not X — it's Y" reframes.

NO-FABRICATION RULE (system-wide): No agent, and not the orchestrator, may invent SKU names, batch numbers, PO numbers, task IDs, customer names, or any identifier. If data isn't reachable, say so explicitly. Real Sweet July Skin SKUs include Castaway Cream Daily Moisturizer, Pava Toner, Pava Exfoliating Cleanser, Soursop Vitamin C Serum, Coffee Fix Peptide Eye Cream, Castaway Cleansing Oil, Irie Power Face Oil, Good Youth Retinol Sleep Serum, plus various lip treatments. Anything outside that lineup is a fabrication red flag.

STEP 1 — SPAWN 12 PARALLEL AGENTS (one Agent tool block, all 12 invocations together).

Each agent gets the same template. Substitute the SKILL_NAME, SKILL_PATH, CARD_TITLE, FOCUS_BULLETS, and ITEM_CAP values from the table below.

Agent prompt template:
"""
You are running a dashboard read for Alvin's daily status dashboard. You are acting as the {SKILL_NAME} skill.

NO-FABRICATION RULES (read first):
- You HAVE access to Supabase via `execute_sql` (project ref `ujkabbffvhpewpbttmmy`), Asana via the asana MCP tools, Outlook via the outlook MCP tools, and Fireflies via the fireflies MCP tools. They are in your tool list. Use them.
- You may also defer to the `plm-assistant` skill via the Skill tool when querying PLM.
- NEVER fabricate SKU names, batch numbers, PO numbers, task IDs, customer names, or any other identifiers. If you don't know it, query for it.
- If a query fails or returns nothing, retry with a different approach. If you genuinely cannot reach data, say so explicitly in `headline_count` ("Live read unavailable — <reason>") and `paragraph`. Do not invent.
- MINIMUM EFFORT: at least 5 successful tool calls before you write your JSON. If you're under 5 calls, you have not done enough work.
- Real Sweet July Skin SKUs include Castaway Cream Daily Moisturizer, Pava Toner, Pava Exfoliating Cleanser, Soursop Vitamin C Serum, Coffee Fix Peptide Eye Cream, Castaway Cleansing Oil, Irie Power Face Oil, Good Youth Retinol Sleep Serum, plus various lip treatments. Anything outside that lineup is a fabrication red flag.

Step 1: Read {SKILL_PATH}/SKILL.md to understand your domain. If your domain reads PLM, also read /sessions/{SESSION}/mnt/.claude/skills/plm-assistant/SKILL.md to learn the schema.

Step 2: Run the read-only queries that surface what's critical RIGHT NOW. Focus on:
{FOCUS_BULLETS}

For PLM domains, start with `list_tables` to discover the real schema, then SELECT from the relevant tables. Tailor queries to the schema you actually find, not what you assume exists.

Today's date: {TODAY}. UBM launch is June 2026.

Step 3: Return ONLY a JSON object (no other text, no markdown fences):
{
  "card_title": "{CARD_TITLE}",
  "headline_count": "<short string based on REAL counts, or 'Live read unavailable — <reason>' if you couldn't query>",
  "paragraph": "<2-3 sentences in the skill's voice. Plain prose. NO AI jargon — never use streamline, leverage, robust, seamless, comprehensive, navigate, dynamic, holistic. Use commas and periods, not em dashes.>",
  "items": [{"title": "<real name/ID>", "url": "<link if available>", "tag": "...", "severity": "critical|warn|ok|muted"}]
}
Cap items at {ITEM_CAP}. Read-only — do not write to Asana, Outlook, Supabase, or anywhere else. But you must actually READ from them.
"""

The 12 skills:
1. asana-pd-manager → "PD Portfolio" — overdue PD tasks, due today/this week, stale stage moves on Ulta launch blockers, unassigned critical items. Cap 8.
2. oc3pl-order-manager → "DTC Orders" — yesterday's shipping numbers, late shipments past SLA, open order errors, returns/replacements, trend vs prior 7 days. Cap 8.
3. inventory-manager → "Inventory" — zero-stock SKUs, low-stock components, near-expiry batches (90d), reconciliation gaps PLM/Shopify/Logiwa, recent write-offs. Cap 8.
4. purchasing-manager → "Purchasing" — open POs by status, POs past expected ship date, stale 30+d, vendor compliance gaps (COA/COC/COI/MSDS), upcoming contract renewals. Cap 8.
5. logistics-manager → "Logistics" — inbound shipments in flight, customs holds, outbound ASN/EDI 856 issues, carrier escalations, anything past expected delivery. Cap 8.
6. supply-demand-planner → "Supply & Demand" — stockout risks next 60 days across DTC/UBM/Amazon, SKUs below reorder point with no PO in flight, forecast vs actual, production scheduling bottlenecks at KDC-One/Vegelabs/Allure, status of latest S&OP run. Cap 8.
7. sjs-margin-architect → "Margin Architecture" — SKUs breaking any channel floor (DTC/UBM/Sephora/Amazon), SKUs without archetype or commercial designation assigned, acquisition-mix portfolio drift, perpetual launch mode signals, hero SKUs at risk on landed COGS shifts. Cap 8.
8. complaint-and-event-handler → "Complaints & Events" — open complaints by SKU and queue, any open SAEs or pending classification, recall triggers, complaint trend last 7 days, overdue first responses. Cap 8.
9. capa-coordinator → "CAPA / NCR" — open NCRs by phase, open CAPAs by phase, overdue verification or effectiveness, anything stuck at QA Lead 7+d, recent NCR→CAPA conversions. Cap 8.
10. sjs-comp-intel → "Comp Intel" — competitor moves last 14 days (Rhode, Summer Fridays, Kosas, LANEIGE, YTTP, Glow Recipe, Tatcha), pipeline tracker flags, prestige skincare trend shifts, any signal that auto-routes into Margin/Retail/Consumer streams. Cap 6.
11. sjs-retail-intel → "Retail Intel" — UBM launch readiness signals, competitor price ladders moving on Ulta, promo calendar items the team should plan around, sell-through and review-velocity model status, cross-channel price architecture risks. Cap 6.
12. ayesha-weekly-briefing → "Ayesha Briefing Queue" — items already drafted for this week's Slide 5 and Slide 6, items that should be in next briefing but aren't, last and next send dates, anything needing Alvin's review before send. Cap 6.

Skill paths:
- /sessions/{SESSION}/mnt/.claude/skills/asana-pd-manager
- /sessions/{SESSION}/mnt/.claude/skills/oc3pl-order-manager
- /sessions/{SESSION}/mnt/.claude/skills/inventory-manager
- /sessions/{SESSION}/mnt/.claude/skills/purchasing-manager
- /sessions/{SESSION}/mnt/.claude/skills/logistics-manager
- /sessions/{SESSION}/mnt/.claude/skills/supply-demand-planner
- /sessions/{SESSION}/mnt/.claude/skills/sjs-margin-architect
- /sessions/{SESSION}/mnt/.claude/skills/complaint-and-event-handler
- /sessions/{SESSION}/mnt/.claude/skills/capa-coordinator
- /sessions/{SESSION}/mnt/.claude/skills/sjs-comp-intel
- /sessions/{SESSION}/mnt/.claude/skills/sjs-retail-intel
- /sessions/{SESSION}/mnt/.claude/skills/ayesha-weekly-briefing

Resolve {SESSION} by checking the working directory at runtime.

STEP 2 — Wait for all 12 agents to return. If an agent fails or times out, render its card with an "Unavailable — try again later" empty state instead of skipping.

STEP 2.5 — VALIDATION PASS (mandatory).

For each returned agent result, check the agent's reported tool-use count and duration before rendering. Flag any agent that:
- Made fewer than 5 tool calls, OR
- Ran for under 30 seconds, OR
- Returned items containing identifiers outside the known SJS portfolio (see SKU list above), OR
- Returned identifiers that look generic/placeholder (e.g., "SKU-001", "Generic Cream", "Sport Lotion" when no such product exists)

Any flagged agent's card MUST be rerun once with an explicit forced-call directive ("you have execute_sql / asana / outlook / fireflies tools available — use them, do not give up"). If the rerun still fails the threshold, render the card with `headline_count` set to "Live read unavailable — agent did not reach data" and surface the failure in the completion report.

STEP 3 — Render the HTML dashboard.

Layout:
- Header: "Daily Status" h1 in Cormorant Garamond serif, subline "Sweet July Skin · 12 skills reporting · Alvin, VP Ops", refreshed timestamp right-aligned (current local PT time).
- Pill bar: top-line counts pulled from the most critical headline_count values across cards.
- 3-column grid (collapses to 2 at 1180px, 1 at 720px).
- One card per skill in this order: PD Portfolio, DTC Orders, Inventory, Purchasing, Logistics, Supply & Demand, Margin Architecture, Complaints & Events, CAPA / NCR, Comp Intel, Retail Intel, Ayesha Briefing Queue.
- Each card: h2 title, terracotta uppercase headline_count, paragraph, ul of items with severity-tagged pills.
- Footer: list of 12 skill names that reported.

Brand palette: bg #f6f4ef, card #ffffff, ink #2c2620, terracotta #b14a2e, amber #b88421, sage #6b7d5b, line #e6dfd3. Tags use soft variants of those colors.

Severity → tag class: critical → terracotta-soft bg, warn → amber-soft, ok → sage-soft, muted → gray.

STEP 4 — Write the file.

Primary path: /sessions/serene-loving-archimedes/mnt/outputs/status-dashboard.html
Fallback: mnt/outputs/status-dashboard.html relative to working directory.

If the primary path returns permission denied, write to the fallback and note the path mismatch in the completion report.

STEP 5 — Verify and report.

Confirm the file exists. Report back:
- Path written to (and whether it was the fallback)
- Top headline_count from each of the 12 cards (one line each)
- Any agents flagged in the validation pass and whether their reruns succeeded
- Anything critical worth flagging beyond the dashboard itself (only ping if launch blocker, SAE/recall, expiring batches, or PO shipping failure)

Do not ping Alvin unless there's something critical. Otherwise just complete silently.
