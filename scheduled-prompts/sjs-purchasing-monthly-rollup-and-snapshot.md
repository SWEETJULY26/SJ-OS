# Scheduled task: sjs-purchasing-monthly-rollup-and-snapshot

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
You are running the AC Brands Purchasing monthly rollup. This fires on the 1st, 2nd, and 3rd of each month at 7:10 AM PT to catch the first business day regardless of weekends.

## First-business-day guard

Before doing anything, check: is today the first US business day of the current calendar month? If not, exit silently — the actual run happened (or will happen) on the correct day. A "business day" excludes weekends and US federal holidays, anchored to America/Los_Angeles.

If today IS the first business day of the month, continue.

## Objective

Compose the monthly purchasing cost rollup (the canonical engine is `regulatory-manager` Job 8 over `vendor_invoices`, scoped to purchasing here — `purchasing-manager` has no monthly cost-rollup job), stage the project status update body for HITL approval, commit the project status update on AC Brands Purchasing once Alvin signs off, and generate the hub archive page.

## Steps

1. **Compose the monthly purchasing cost rollup inline.** The canonical monthly cost-rollup engine is `regulatory-manager` Job 8 over `vendor_invoices`; scope it to purchasing here. (`purchasing-manager` has no monthly cost-rollup job — its Job 10 is the receipt-discrepancy flow.) Compose the rollup from:
   - Direct Supabase SELECT on `vendor_invoices` for spend by `cost_category` (regulatory, quality, pd, ops, marketing, general), spend by vendor, MoM and T3M comparison
   - AC Brands Purchasing project (GID `1214373717266702`) for PO activity, vendor activity, compliance & renewals roll-forward, sourcing throughput
   - Vendor scorecard movement from `logistics-manager` and `oc3pl-order-manager` cross-skill signals
   - Compliance gap velocity (gaps opened/closed for the month)

2. **Compute status color.** Apply this logic:
   - **Green:** total spend within ±10% of T3M avg, compliance net delta ≤0, no scorecard downgrades, all renewals on track
   - **Yellow:** any one of — spend ±10–25% T3M, compliance net delta +1, 1–2 scorecard downgrades, renewal slipped <15 days
   - **Red:** any one of — spend >±25% T3M, compliance net delta ≥+2 for 2 months running, scorecard downgrade on a top-10-spend vendor, any renewal lapsed

3. **Stage the status update body.** Build using this template:

```
# Purchasing — {Month Year} Rollup

**Total spend:** ${total} ({MoM%} vs prior, T3M avg ${t3m})
**PO commit issued:** ${po_issued} across {po_count} POs
**Compliance gap net delta:** {opened} opened / {closed} closed → {net} net
**Vendor scorecard movement:** {up} up / {down} down

## Spend by cost_category
| Category | This month | Prior | MoM | T3M avg | Top vendor |
|---|---|---|---|---|---|
| regulatory | ... | ... | ... | ... | ... |
| quality | ...
| pd | ...
| ops | ...
| marketing | ...
| general | ...

## Top 3 callouts
- {callout 1 — biggest material change}
- {callout 2 — risk or watch item}
- {callout 3 — what changed in vendor or compliance posture}

## What's open going into next month
- HITL queue: {count} items, oldest {days}d
- Renewals due ≤30d: {count}
- Open variance: {count} POs / ${amount}

[View archive →]({hub_archive_url})
```

4. **HITL gate.** Present the staged status update body, the computed status color, and the data sources used. Wait for Alvin's explicit approval before posting. Do not auto-commit.

5. **On approval, commit the project status update.** Post to AC Brands Purchasing project (GID `1214373717266702`) using the Asana connector's `asana_create_project_status` tool with the approved body, the computed color, and a one-line headline like "Purchasing {Month Year} Rollup".

6. **Generate hub archive.** If `purchasing-status-reporter` skill exists, invoke it to render a frozen snapshot of the Monthly tab targeted at path `archive/purchasing-YYYY-MM.html`. Publish via landing-hub-publish: POST to `https://acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish` with header `x-hub-secret` (read from the `HUB_FUNCTION_SECRET` environment variable), body `{ "files": [ { "path": "archive/purchasing-YYYY-MM.html", "content": "<frozen HTML>" } ], "commit_message": "purchasing dashboard: monthly snapshot YYYY-MM" }`. The function commits to main; Netlify auto-deploys. If the skill does not yet exist, log "archive generation skipped — purchasing-status-reporter not yet available" and continue. The status update body's `{hub_archive_url}` should point to `https://acb-thelanding.netlify.app/archive/purchasing-YYYY-MM.html` for the relevant month.

## Constraints

- HITL is REQUIRED for the status update commit. Do not post without explicit operator approval.
- Read-only on `vendor_invoices` (Supabase SELECT, never write).
- Do not write to PLM. This monthly rollup is a composer, not a writer.
- Brand scope: AC Brands corporate, Sweet July Skin first.
- Operator: Alvin.
- Reference pattern: `sjs-regulatory-monthly-rollup-and-snapshot` uses the same shape.
