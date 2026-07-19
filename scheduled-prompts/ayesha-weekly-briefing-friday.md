# Scheduled task: ayesha-weekly-briefing-friday

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/ayesha-weekly-briefing/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-status-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/regulatory-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/sweet-july-skin-brand/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Canva, Fireflies, Microsoft 365, Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
Run Alvin's weekly Operations briefing for Ayesha Curry by invoking the `ayesha-weekly-briefing` skill. This is the Friday 8am autonomous run — land the deck well before noon local. Do not ask clarifying questions; proceed end-to-end.

Per the current skill (v6.3), Alvin owns BOTH Slide 5 and Slide 6 of the persistent Canva deck (design ID DAHGewVQYFo, title pattern "AC Weekly Briefing [date]"):

- **Slide 5 — Business Operations (true ops):** HR, logistics, purchasing, finance, S&OP, regulatory, fulfillment. Write 5–7 founder-filtered bullets here. Do NOT include PD/launch updates — those go on Slide 6 if at all.

- **Slide 6 — Product Development (shared with Nicole):** Append 1–3 PD-Ops bullets BELOW Nicole's PD content. Alvin's Slide 6 content is the PD-Ops angle: AC Brands landing hub (acb-thelanding.netlify.app) and dashboards, AI/IT-side PD work, packaging readiness, supply chain risk affecting product. Write Slide 6 every week regardless of whether Nicole has refreshed her content. Never overwrite Nicole's content — append below it. If her content is stale (last week), append anyway and flag in the completion report.

Sweep the past 7 days across Asana (OC3PL Order Management, SJ Shipping Dashboard, PD Portfolio — note Ops Dashboard GID may be stale; fall back to other sources if it fails), Outlook, Fireflies, PLM Supabase, and the regulatory-manager rollup. Apply the founder filter (decision/milestone, risk/material change, cross-functional impact, founder relevance, or regulatory signal) before any bullet earns a slot.

Voice rules: AC Brands writing style (no banned words, no hyphens, sparing em dashes since this is external/founder-facing). Translate acronyms on first mention (OC3PL → our 3PL, UBMP → Ulta Beauty Marketplace, KDC → KDC-One).

Write directly to the Canva deck using start-editing-transaction → perform-editing-operations → commit-editing-transaction. Report on completion: deck name and title, Slide 5 bullet count, Slide 6 bullet count, any flags (stale deck title from Danielle, stale Nicole content, data source failures). If any data source returns nothing meaningful, note that in the completion report rather than padding bullets.
