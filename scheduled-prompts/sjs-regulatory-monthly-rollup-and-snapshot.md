# Scheduled task: sjs-regulatory-monthly-rollup-and-snapshot

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.
The landing hub repo (`SWEETJULY26/acb-thelanding`) is also cloned at `/home/user/acb-thelanding`, **read-only** — use it to check current file structure, CSS tokens, and existing page patterns before generating output. Any skill instructions referencing `/Users/alvinbelt/Downloads/acb-thelanding/` mean this clone. Do not commit or push to it — publishing still goes through the `landing-hub-publish` Netlify Function per the skill's Publishing section.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/sjs-regulatory-system/SKILL.md`
- `/home/user/sj-os/.claude/skills/regulatory-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/claims-il-and-label-keeper/SKILL.md`
- `/home/user/sj-os/.claude/skills/adverse-event-and-recall-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/regulatory-status-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-master/SKILL.md`
- `/home/user/sj-os/.claude/skills/plm-assistant/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral. The acb-thelanding clone is read-only; never commit or push to it.

## Task
SJS Regulatory Monthly Cost Rollup + Dashboard Snapshot. Today is one of the first three days of the month and the scheduler woke you up. First check: confirm today is the FIRST BUSINESS DAY of the month (skip weekends and US federal holidays — observed New Year's Day, MLK Day, Presidents' Day, Memorial Day, Juneteenth, Independence Day, Labor Day, Columbus Day, Veterans Day, Thanksgiving, Christmas). If today is not the first business day of the month, exit silently — do not run anything, do not post to Asana, do not touch the repo.

If today IS the first business day of the month, proceed.

The target month for the rollup and snapshot is the PRIOR calendar month (e.g. running on first business day of June 2026 produces the May 2026 rollup and May 2026 archive).

STEP 1 — Fire regulatory-manager Job 8 (Monthly regulatory cost rollup).
Run a Supabase SELECT against the vendor_invoices table in PLM project ujkabbffvhpewpbttmmy. Filter: (cost_category='regulatory' OR regulatory_driver=true) AND invoice_date in the prior calendar month AND state IN ('approved','paid'). Compose five aggregations:
- total spend
- by-cost-category split (regulatory / quality / pd / ops / marketing / general counts and dollars)
- by-vendor top-10
- by-SKU breakdown via linked_sku_id (where set)
- MoM variance vs prior month

Post the rollup as a project status comment on SJS Regulatory Management Asana project (gid 1214660807386611). Cache the rollup output in memory for Step 2.

STEP 2 — Fire regulatory-status-reporter Job 2 (Monthly snapshot).
Read the freshly composed Job 8 rollup. Render two files in memory: a static archive page targeted at `archive/regulatory-YYYY-MM.html` (where YYYY-MM is the prior month) using the same Hub shell, header, and CSS as the live regulatory-dashboard.html with the v6.7 spend strip baked in (monthly headline + per-cost-category mini-bars, data embedded inline); and an updated `regulatory-dashboard.html` with a new "Recent snapshots" footer entry linking to the archive page.

Stage a [Monthly Regulatory Dashboard Snapshot] YYYY-MM task in SJS Regulatory Management → Cross-Skill Dashboard section (gid 1214660230826189). Set Artifact Type custom field (gid 1214661463988667) to "Monthly Regulatory Dashboard Snapshot" — fall back to "Other" if the option doesn't exist. The archive HTML attaches to the task after Step 3 returns the commit SHA.

STEP 3 — HITL gate + publish.
Pause. Show Alvin (alvin@ac-brands.com) the staged file list (the new archive path + the updated regulatory-dashboard.html), the spend headline, and the commit message draft. Wait for approval. On approval, POST both files in a single landing-hub-publish call with commit message "regulatory dashboard: monthly snapshot <Month YYYY>". Resolve HUB_FUNCTION_SECRET per the `HUB_FUNCTION_SECRET` environment variable. The function commits to main via GitHub API; Netlify auto-deploys. Confirm deploy success and capture the commit SHA before closing the run.

Net surfaces this run produces: Asana project status comment with Job 8 rollup; Asana attached snapshot task in Cross-Skill Dashboard; Netlify-deployed archive page at acb-thelanding.netlify.app/archive/regulatory-YYYY-MM.html; updated link in live dashboard footer.

Constraints:
- All PLM writes go via plm-assistant (single-writer rule). This run is read-only on PLM.
- All Asana writes use the documented project and section gids above.
- No commits to GitHub without operator approval.
- USD assumed at v1 — no multi-currency conversion.
- If the cached rollup from Step 1 fails or is empty for the target month (no invoices found), still produce the snapshot but render the spend strip with a "no spend recorded for [month]" placeholder. Do not block the snapshot on empty data.

Reference: the installed `regulatory-manager` skill (Jobs 8 + 9) and the installed `regulatory-status-reporter` skill (Job 2 + v6.7 spend strip + Cross-Skill Dashboard section gid). Invoke them by name; do not rely on any session-mount file path.
