# Scheduled task: sjs-purchasing-weekly-digest

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/purchasing-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-ops-system/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse). Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
You are running the AC Brands Purchasing weekly digest. This fires every Monday at 7:30 AM PT.

## Objective

Regenerate the live purchasing dashboard, post the updated HTML to the running Weekly Purchasing Dashboard task on Asana, and post a short text summary comment to the Purchasing Sweep Running Log.

## Setup

Invoke the `purchasing-status-reporter` skill. If that skill does not yet exist (it is being built in a separate Claude Code session), exit and log: "purchasing-status-reporter not yet available — weekly digest skipped YYYY-MM-DD". Do not attempt to regenerate the dashboard without the skill.

## Steps

1. **Generate the weekly dashboard HTML.** Invoke `purchasing-status-reporter`. The skill composes the Weekly tab content from:
   - Asana state on AC Brands Purchasing project (GID `1214373717266702`)
   - Direct Supabase SELECT on `vendor_invoices` for the spend strip
   - `purchasing-manager` rollup composition (Jobs 3, 4, 5, 7, 8, 9)
   - Cross-skill reads from `supply-demand-planner` (forward cover) and `inventory-manager` (on-hand position)
   - Vendor scorecard inputs from `logistics-manager` and `oc3pl-order-manager`

2. **Publish the hub file via landing-hub-publish.** POST to `https://acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish` with header `x-hub-secret`. Resolve the secret from the `HUB_FUNCTION_SECRET` environment variable. Body:
   ```json
   {
     "files": [
       { "path": "purchasing-dashboard.html", "content": "<regenerated HTML>" }
     ],
     "commit_message": "purchasing dashboard: weekly digest — [YYYY-WW]"
   }
   ```
   The function commits to main via the GitHub API; Netlify auto-deploys. No local clone, no local git.

3. **Post to Asana — Weekly Purchasing Dashboard running task.** Locate the `[Weekly Purchasing Dashboard]` task in the Cross-Skill Dashboard section of AC Brands Purchasing (GID `1214373717266702`). This is a single persistent running task — do NOT create a new task per week. Post a comment dated YYYY-WW with the rendered HTML as an attachment on that comment. Comment body should be a short one-liner: "Week YYYY-WW dashboard — see attachment. Live page: https://acb-thelanding.netlify.app/purchasing-dashboard.html"

4. **Post text summary to Purchasing Sweep Running Log.** Locate the Purchasing Sweep Running Log task in the same section. Post a separate comment with the headline figures:
   ```
   Weekly digest YYYY-WW

   - HITL queue: {count} items, oldest {days}d
   - POs in flight: {count} ({sent}/{ack}/{transit}), variance {vcount} (${vamount})
   - Compliance & renewals window: {count} expiring ≤30d, closest {date}
   - PO commit on the water: ${amount}, forward cover {days}d
   - Total monthly spend MTD: ${amount} ({MoM%} vs prior month)

   Dashboard: https://acb-thelanding.netlify.app/purchasing-dashboard.html
   ```

## Constraints

- HITL is NOT required for the weekly digest — the dashboard regen and comment posts are read-only against PLM. No record creation, no spend actions.
- Do not modify task fields. Do not open new tasks.
- The HTML attachment lives on the comment, not on the task body. Each weekly run adds a new comment with a fresh attachment.
- Brand scope: AC Brands corporate, Sweet July Skin first.
- Operator: Alvin.
- Reference pattern: `sjs-regulatory-weekly-digest` and `sjs-quality-weekly-digest` use parallel patterns.
