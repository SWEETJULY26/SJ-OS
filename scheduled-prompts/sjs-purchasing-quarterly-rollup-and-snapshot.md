# Scheduled task: sjs-purchasing-quarterly-rollup-and-snapshot

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/purchasing-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/regulatory-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-ops-system/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
You are running the AC Brands Purchasing quarterly rollup. This fires on the 1st, 2nd, and 3rd of January, April, July, and October at 7:10 AM PT to catch the first business day of each quarter regardless of weekends.

## First-business-day-of-quarter guard

Before doing anything, check: is today the first US business day of the current calendar quarter (Q1 starts Jan 1, Q2 Apr 1, Q3 Jul 1, Q4 Oct 1)? If not, exit silently. A "business day" excludes weekends and US federal holidays, anchored to America/Los_Angeles.

If today IS the first business day of the quarter, continue.

## Objective

Compose the quarterly purchasing cost rollup (the canonical engine is `regulatory-manager` Job 9 over `vendor_invoices`, scoped to purchasing here — `purchasing-manager` has no quarterly cost-rollup job), stage the project status update body for HITL approval, commit the project status update on AC Brands Purchasing once Alvin signs off, and generate the hub archive page.

## Steps

1. **Compose the quarterly purchasing cost rollup inline.** The canonical quarterly cost-rollup engine is `regulatory-manager` Job 9 over `vendor_invoices`; scope it to purchasing here. (`purchasing-manager` has no quarterly cost-rollup job.) Compose the rollup from:
   - Direct Supabase SELECT on `vendor_invoices` for quarterly $ by cost_category over trailing 4 quarters, top-10-by-spend vendor list at quarter-end, single-vendor and top-5 concentration
   - AC Brands Purchasing project (GID `1214373717266702`) for contract & renewal posture, open POs at quarter-end, sourcing throughput (RFQs by status, win rate by category, median cycle time)
   - Vendor scorecard movement quarter-over-quarter from `logistics-manager` (landed-cost) and `oc3pl-order-manager` (carrier cost variance) cross-skill signals
   - Compliance posture — % of active vendors with all docs current at quarter-end

2. **Compute status color.** Apply this logic:
   - **Green:** QoQ spend within ±20%, compliance posture ≥90%, no top-10 scorecard downgrades, sourcing closure rate ≥60%, no concentration breach
   - **Yellow:** any one of — QoQ ±20–35%, posture 80–90%, 1 top-10 downgrade, closure rate 45–60%, single-vendor concentration 25–30%
   - **Red:** any one of — QoQ >±35%, posture <80%, ≥2 top-10 downgrades, closure rate <45%, single-vendor concentration >30%

3. **Stage the status update body.** Build using this template:

```
# Purchasing — {Quarter Year} Rollup

**Total spend:** ${total} ({QoQ%} vs prior, {YoY%} YoY)
**Top-5 vendor concentration:** {pct}% (worst-case single vendor: {pct}%)
**Compliance posture:** {pct}% of active vendors fully compliant
**Sourcing closure rate:** {pct}% ({opened} opened / {awarded} awarded, median {days}d)

## Top-10 vendor scorecard movement
- Upgrades: {list}
- Downgrades: {list}
- New entrants in top-10: {list}

## Top 3 strategic callouts
- {callout 1 — biggest concentration or scorecard shift}
- {callout 2 — sourcing pipeline read}
- {callout 3 — compliance or contract posture}

## Going into next quarter
- Contracts up for renewal: {count} (${exposure})
- RFQs in flight: {count}
- Open PO commit: ${amount} across {count} POs, oldest {days}d

[View archive →]({hub_archive_url})
```

4. **HITL gate.** Present the staged status update body, the computed status color, and the data sources used. Wait for Alvin's explicit approval before posting. Do not auto-commit.

5. **On approval, commit the project status update.** Post to AC Brands Purchasing project (GID `1214373717266702`) using the Asana connector's `asana_create_project_status` tool with the approved body, the computed color, and a one-line headline like "Purchasing {Quarter Year} Rollup".

6. **Generate hub archive.** If `purchasing-status-reporter` skill exists, invoke it to render a frozen snapshot of the Quarterly tab targeted at path `archive/purchasing-YYYY-Q[1-4].html`. Publish via landing-hub-publish: POST to `https://acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish` with header `x-hub-secret` (read from the `HUB_FUNCTION_SECRET` environment variable), body `{ "files": [ { "path": "archive/purchasing-YYYY-Q[1-4].html", "content": "<frozen HTML>" } ], "commit_message": "purchasing dashboard: quarterly snapshot YYYY-QN" }`. The function commits to main; Netlify auto-deploys. If the skill does not yet exist, log "archive generation skipped — purchasing-status-reporter not yet available" and continue. The status update body's `{hub_archive_url}` should point to `https://acb-thelanding.netlify.app/archive/purchasing-YYYY-Q[1-4].html` for the relevant quarter.

## Constraints

- HITL is REQUIRED for the status update commit. Do not post without explicit operator approval.
- Read-only on `vendor_invoices` (Supabase SELECT, never write).
- Do not write to PLM. This quarterly rollup is a composer, not a writer.
- Brand scope: AC Brands corporate, Sweet July Skin first.
- Operator: Alvin.
- Reference pattern: `sjs-regulatory-quarterly-cost-rollup` uses the same shape.
