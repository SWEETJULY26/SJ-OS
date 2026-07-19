# Scheduled task: sjs-quality-quarterly-rollup

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
Run the SJS Quality Quarterly Rollup.

Step 0 — Business day check:
Today must be the first business day of Jan/Apr/Jul/Oct. If not, abort and exit silently.

Step 1 — Compose the quarterly rollup:
Call quality-manager Job 8 (quarterly operational rollup). Operational only — no cost rollup, no vendor_invoices query. Return payload matches references/cadence-composition-spec.md §3. Payload includes:
- Quarter-over-quarter metric deltas
- Quarterly-only block: SOP review cycle progress, audits, retailer questionnaires, regulatory inspections
- Four narratives: quarter recap, trends emerging, focus for next quarter, founder signal for Ayesha briefing
- Two staged handoff comments (draft state): one for sjs-status-reporter running log, one for ayesha-weekly-briefing source pool

Step 2 — Refresh the Quarterly tab:
Call quality-status-reporter Job 5 (quarterly tab refresh). The job:
- Reads the payload from Step 1
- Renders the Quarterly tab content for quality-dashboard.html
- Renders data/quality-quarterly-snapshot.json (static fallback + canonical source)
- Publishes both files via the landing-hub-publish Netlify Function with commit message "quality dashboard: quarterly tab refresh <Quarter YYYY>". Resolve HUB_FUNCTION_SECRET per the `HUB_FUNCTION_SECRET` environment variable.

HITL gate 1: Operator approves the publish payload before POST. Surface the rendered files, commit message, and the four narratives; wait for approval. On approval, fire the POST; the function commits via GitHub API and Netlify auto-deploys.

Step 3 — Post breadcrumb:
After landing-hub-publish returns ok and Netlify deploys (~60s), post a breadcrumb comment to the Quality Sweep Running Log task (GID 1214843467424902). Format per references/tab-refresh-spec.md §Quarterly tab refresh breadcrumb. Include RAG, headline, quarter recap first 2 sentences, trends emerging first sentence, founder signal flag, and the Quarterly tab link with #quarterly anchor.

Step 4 — Stage handoff comments for separate approval:
Surface the two staged handoff comments from Step 1's payload (sjs-status-reporter comment, ayesha-weekly-briefing comment). Each goes to a separate HITL gate.

HITL gate 2: Operator approves the sjs-status-reporter comment. On approval, post to the sjs-status-reporter running log.

HITL gate 3: Operator approves the ayesha-weekly-briefing comment. On approval, append to the ayesha-weekly-briefing source pool for the following Friday's briefing.

Important: No Asana attachment. No frozen archive page. The dashboard is the artifact. The handoff comments are the secondary outputs.

If any step fails, stop and surface the error. Do not retry automatically.
