# Scheduled task: sjs-quality-weekly-digest

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/SJ-OS` — **case-sensitive**. If that path does not resolve, locate the repo before doing anything else (`ls -d /home/user/*` and look for the checkout containing `.claude/skills/`) and use what you find; do not proceed on the assumption the skills are unreadable. Until 2026-07-31 every spec in this directory said `/home/user/sj-os`, which does not exist on a case-sensitive filesystem, so fired runs could not read their own instructions.
The landing hub repo (`SWEETJULY26/acb-thelanding`) is also cloned at `/home/user/acb-thelanding`, **read-only** — use it to check current file structure, CSS tokens, and existing page patterns before generating output. Any skill instructions referencing `/Users/alvinbelt/Downloads/acb-thelanding/` mean this clone. Do not commit or push to it — publishing still goes through the `landing-hub-publish` Netlify Function per the skill's Publishing section.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/SJ-OS/.claude/skills/sjs-quality-system/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/quality-manager/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/capa-coordinator/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/complaint-and-event-handler/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/quality-lab-coordinator/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/batch-lifecycle-tracker/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/quality-status-reporter/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/oc3pl-order-manager/SKILL.md`
- `/home/user/SJ-OS/.claude/skills/sjs-master/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse). Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral. The acb-thelanding clone is read-only; never commit or push to it.

## Task
Run the SJS Quality Weekly Digest.

Step 1 — Compose the digest:
Call quality-manager Job 6 (weekly digest composition). The job pulls from capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker, and oc3pl-order-manager QoS metrics. Return payload matches references/cadence-composition-spec.md §1.

Step 2 — Render the Weekly tab:
Call quality-status-reporter Job 6 (weekly digest push). The job:
- Reads the payload from Step 1
- Renders the Weekly tab content for quality-dashboard.html (the default tab)
- Renders data/quality-weekly-snapshot.json (static fallback)
- Publishes both files via the landing-hub-publish Netlify Function with commit message "quality dashboard: weekly digest push <YYYY-MM-DD>". Resolve HUB_FUNCTION_SECRET per the `HUB_FUNCTION_SECRET` environment variable.

HITL: Operator approves the publish payload before POST. Surface the rendered files and commit message; wait for approval. On approval, fire the POST; the function commits via GitHub API and Netlify auto-deploys.

Step 3 — Post breadcrumb:
After landing-hub-publish returns ok and Netlify deploys (~60s), post a breadcrumb comment to the Quality Sweep Running Log task (GID 1214843467424902). Format per references/tab-refresh-spec.md §Weekly digest breadcrumb. Include RAG, headline, top 3-5 priorities, and the dashboard link.

If any step fails, stop and surface the error to Operator. Do not retry automatically.
