# Scheduled task: sjs-regulatory-quarterly-cost-rollup

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
SJS Regulatory Quarterly Cost Rollup + Dashboard Snapshot.

**Pre-flight: business-day check.**
Cron fires days 1–3 of Jan / Apr / Jul / Oct at 7am PT to cover weekends and US holidays. Before doing anything, check today's date against the first business day rule:
- If today is the first US business day of Jan / Apr / Jul / Oct (the first non-weekend, non-US-federal-holiday day on or after the 1st), proceed.
- If today is day 2 or 3 and the first business day already passed (and the run already completed), exit silently — do not double-fire.
- If today is day 2 or 3 because day 1 was a weekend/holiday and this is the actual first business day, proceed.

Use `date` to check the current date and reason through this. If you cannot confirm first-business-day status with certainty, post a one-line note to the running log asking the operator to confirm and exit.

**Target quarter.** The quarter to be snapshotted is the prior full calendar quarter:
- Jan run → Q4 of prior year
- Apr run → Q1 of current year
- Jul run → Q2 of current year
- Oct run → Q3 of current year

Format the label as `YYYY-QN` (e.g., `2026-Q1`).

**Step 1 — Run regulatory-manager Job 9 (quarterly cost rollup).**
Invoke the regulatory-manager skill. Ask it to run Job 9 for the target quarter (per the rule above). The job should produce:
- Total regulatory-driven spend for the quarter
- Breakdown by cost_category
- Top-10 vendor spend list
- Per-SKU regulatory cost (where linked_sku_id is set)
- Country split (US / CA / EU / UK / Other)
- QoQ variance (vs prior quarter) and YoY variance (vs same quarter last year)

Confirm Job 9 wrote its results where downstream consumers expect (Asana status comment on SJS Regulatory Management quarterly thread; data ready for sjs-status-reporter and ayesha-weekly-briefing pickup).

**Step 2 — Run regulatory-status-reporter Job 5 (quarterly snapshot).**
Invoke the regulatory-status-reporter skill. Ask it to run Job 5 for the same target quarter. The job should:
- Read the current rollup via the Netlify Function (same source the live page uses)
- Render two files in memory: a frozen archive page targeted at `archive/regulatory-YYYY-QN.html` with the quarterly spend strip variant (QoQ + YoY chevrons, per-SKU sub-strip, country-split mini-bars) baked in from Job 9; and an updated `regulatory-dashboard.html` with the new quarterly entry added to "Recent snapshots" (sorted with monthly entries by date; quarterly entries labeled `YYYY-QN`)
- Stage a `[Quarterly Regulatory Dashboard Snapshot] YYYY-QN` task in SJS Regulatory Management → Cross-Skill Dashboard section (gid 1214660230826189) with Artifact Type = `Quarterly Regulatory Dashboard Snapshot` (fall back to `Other` if the option doesn't exist yet). Attach the archive HTML to the task after Step 3 returns the commit SHA.

**Step 3 — HITL gate + publish.**
Surface a summary of what's about to ship:
- Archive page path and quarter label
- Live page diff (the new footer link entry)
- Asana snapshot task it will be attached to
- Commit message draft

Wait for operator approval. On approval, POST both files in a single landing-hub-publish call with commit message `regulatory dashboard: quarterly snapshot YYYY-QN`. Resolve HUB_FUNCTION_SECRET per the `HUB_FUNCTION_SECRET` environment variable. The function commits to main via GitHub API; Netlify auto-deploys. On rejection, hold the payload and post a one-line note to the running log; nothing publishes.

**Step 4 — Handoffs.**
After push (or after the operator declines the push), confirm:
- Job 9 results are available for sjs-status-reporter (quarterly leadership view)
- Job 9 results are available for ayesha-weekly-briefing (next Friday digest)

If either handoff target needs an explicit nudge, comment on the relevant Asana thread.

**On failure or ambiguity:** stop, post a one-line note to the Regulatory Sweep Running Log, and surface to the operator. Do not commit or push unilaterally.
