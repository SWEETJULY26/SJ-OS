# Scheduled task: sjs-regulatory-weekly-digest

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.
The landing hub repo (`SWEETJULY26/acb-thelanding`) is also cloned at `/home/user/acb-thelanding`, **read-only** — use it to check current file structure, CSS tokens, and existing page patterns before generating output. Any skill instructions referencing `/Users/alvinbelt/Downloads/acb-thelanding/` mean this clone. Do not commit or push to it — publishing still goes through the `landing-hub-publish` Netlify Function per the skill's Publishing section.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/sjs-regulatory-system/SKILL.md`
- `/home/user/sj-os/.claude/skills/regulatory-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/claims-il-and-label-keeper/SKILL.md`
- `/home/user/sj-os/.claude/skills/adverse-event-and-recall-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/regulatory-status-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-master/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral. The acb-thelanding clone is read-only; never commit or push to it.

## Task
Run the SJS Regulatory Sweep — Monday weekly digest.

Read /mnt/skills/user/sjs-regulatory-sweep/SKILL.md (or the cowork-resolved path) and execute Job 2. Render pattern is locked at regulatory-status-reporter v6.7 — do not regress to linear pages. (Render-pattern and chrome lock established v6.6.1–v6.6.2 still hold; the v6.7 spend strip applies to monthly/quarterly archives, not this weekly tab.)

Window: past 7 days through today, plus the next 90 days for the Clocks & Deadlines tab and the next 12 months for Strategic Horizon.

Sequence:
1. Route through sjs-regulatory-system.
2. Pull composed rollup from regulatory-manager (registrations, retailer attestation cadence, Pedrero liaison, international markets, state packaging laws).
3. Pull SAE / recall state from adverse-event-and-recall-reporter via SJS Reportable Events.
4. Pull IL / claim / label / attestation state from claims-il-and-label-keeper.
5. Pull customs / import activity past 7 days from logistics-manager.
6. Hand the composed rollup to regulatory-status-reporter for the tabbed render.

Render pattern (locked, v6.7; chrome lock v6.6.2 still in force — chrome-aligned with quality-dashboard, shipping-dashboard, inventory-dashboard):
- Start every regen from regulatory-status-reporter/references/dashboard-template.html — the canonical thin shell.
- Three-file output, mirroring quality-dashboard:
  * regulatory-dashboard.html — chrome shell only. DO NOT overwrite on weekly regen.
  * assets/js/regulatory-dashboard.js — overwrite only the inline tab content blocks inside mount(). Preserve Hub.renderHeader(true) / Hub.renderNav('Regulatory Dashboard') / Hub.renderFooter() / Hub.bindNav() / Hub.bindEditMode() chrome calls untouched.
  * assets/css/regulatory-dashboard.css — DO NOT overwrite unless a new component is added.
- No live Netlify Function call. Function (netlify/functions/sjs-regulatory-rollup.js) is deprecated at v6.6.1; dashboard is static-rendered weekly.

Page composition (top → bottom):
- Hub shell (AC · Brands eyebrow, "The Landing." headline, FUNCTIONS dropdown nav) via Hub.renderHeader/Nav/Footer
- Hero block (page title + blurb + week stamp)
- Lede strip (headline state of the week)
- KPI row — 4 tiles, color-tinted by urgency band (alert/warn/ok/neutral):
  1. Pedrero queue depth (capacity flag at ≥5 items / >7-day age per 2026-05-12 touchbase)
  2. Items we owe Pedrero (next packet ladder)
  3. Statutory clocks at 80%+ count (SAE, recall, agency follow-up)
  4. Renewal window 30d count (attestations + registrations)
- Tab nav + 5 tab panels:
  Tab 1 — Clocks & Deadlines (every dated regulatory item, 90-day window, countdown chips green/yellow/red/gray per SKN-OPS-009 §10.1)
  Tab 2 — Pedrero (queue depth, what they owe us vs what we owe them, Amy/Heather split, SB 343 thread separate, Ecomundo + UK/SA RP partner section)
  Tab 3 — Clearance Matrix (formula × market grid US/CA/UK/EU/SA on top; packaging compliance ladder per SKU on bottom — SB 343 chasing-arrows, Toxics-in-Packaging CoC per supplier, EPR registration status)
  Tab 4 — Operational Signal (customs/import past 7d, SAE clocks with bars, recall classification + windows, batch-affected counts, Quality fan-out queue, §7.4 reformulation claim-bridge per-SKU — Eye Cream / Toner / Power Oil)
  Tab 5 — Strategic Horizon (EPR threshold monitor trailing-12 vs $5M global / $1M CA, UBM June 2026 launch dependencies, Pedrero scope-change watch, UK/SA pipeline)

Visualization rules:
- Statutory clock bars — green <60%, yellow 60–95%, red ≥95%
- Canada extended-allergens countdown — green ≥60d to 2026-07-31, yellow 30–60d, red ≤30d
- EPR threshold — green <60% of $5M global / $1M CA, yellow 60–80%, red ≥80%
- Pedrero capacity — alert when queue ≥5 items or any single send sits >7 days

Push destinations:
- Asana attachment on a [Monday Regulatory Digest] YYYY-MM-DD task in SJS Regulatory Management (gid 1214660807386611) → Cross-Skill Dashboard section (gid 1214660230826189)
- acb-thelanding.netlify.app/regulatory-dashboard.html, published via the landing-hub-publish Netlify Function (POST regulatory-dashboard.html + the two updated assets + any data/regulatory-*-snapshot.json files in one call with header x-hub-secret). Resolve HUB_FUNCTION_SECRET per the `HUB_FUNCTION_SECRET` environment variable. The function commits to main via the GitHub API; Netlify auto-deploys. No local clone, no local git required.

After dashboard push, post a summary comment to the Regulatory Sweep Running Log (same task as the daily sweep, Cross-Skill Dashboard section). Format:

WEEKLY DIGEST — [YYYY-MM-DD]
[Linked dashboard URL]
[1-2 sentences on the biggest signal of the week]

Execute fully. Do not ask permission outside the regulatory-status-reporter publish HITL gate (Alvin approves the landing-hub-publish payload during the Monday window).
