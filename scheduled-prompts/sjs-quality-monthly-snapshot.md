# Scheduled task: sjs-quality-monthly-snapshot

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.
The landing hub repo (`SWEETJULY26/acb-thelanding`) is also cloned at `/home/user/acb-thelanding`, **read-only** — use it to check current file structure, CSS tokens, and existing page patterns before generating output. Any skill instructions referencing `/Users/alvinbelt/Downloads/acb-thelanding/` mean this clone. Do not commit or push to it — publishing still goes through the `landing-hub-publish` Netlify Function per the skill's Publishing section.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/sjs-quality-system/SKILL.md`
- `/home/user/sj-os/.claude/skills/quality-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/capa-coordinator/SKILL.md`
- `/home/user/sj-os/.claude/skills/complaint-and-event-handler/SKILL.md`
- `/home/user/sj-os/.claude/skills/quality-lab-coordinator/SKILL.md`
- `/home/user/sj-os/.claude/skills/batch-lifecycle-tracker/SKILL.md`
- `/home/user/sj-os/.claude/skills/quality-status-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/oc3pl-order-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-master/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse). Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral. The acb-thelanding clone is read-only; never commit or push to it.

## Task
Run the SJS Quality Monthly Snapshot.

Step 0 — Business day check:
Today must be the first business day of the calendar month. If today is a weekend or holiday and the first business day is later this week, abort and exit silently. If today IS the first business day, proceed.

Step 1 — Compose the monthly rollup:
Call quality-manager Job 7 (monthly operational rollup). The job computes prior-month metrics, current-month metrics, deltas, and trend direction. Return payload matches references/cadence-composition-spec.md §2. Operational only — no cost rollup.

Step 2 — Refresh the Monthly tab:
Call quality-status-reporter Job 2 (monthly tab refresh). The job:
- Reads the payload from Step 1
- Renders the Monthly tab content for quality-dashboard.html
- Renders data/quality-monthly-snapshot.json (static fallback + canonical source)
- Publishes both files via the landing-hub-publish Netlify Function with commit message "quality dashboard: monthly tab refresh <Month YYYY>". Resolve HUB_FUNCTION_SECRET per the `HUB_FUNCTION_SECRET` environment variable.

HITL: Operator approves the publish payload before POST. Surface the rendered files and commit message; wait for approval. On approval, fire the POST; the function commits via GitHub API and Netlify auto-deploys.

Step 3 — Post breadcrumb:
After landing-hub-publish returns ok and Netlify deploys (~60s), post a breadcrumb comment to the Quality Sweep Running Log task (GID 1214843467424902). Format per references/tab-refresh-spec.md §Monthly tab refresh breadcrumb. Include RAG, headline, top 5 deltas vs. prior month, and the Monthly tab link with #monthly anchor.

Important: No Asana attachment. No frozen archive page. The dashboard is the artifact.

If any step fails, stop and surface the error. Do not retry automatically.
