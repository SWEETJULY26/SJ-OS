# Scheduled task: sjs-quality-morning-sweep

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
Use only the attached connectors: Asana, Asana(sse), Microsoft 365. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral. The acb-thelanding clone is read-only; never commit or push to it.

## Task
Run the SJS Quality Morning Sweep for the window of 5 PM PT yesterday through now (Pacific time).

Route through the sjs-quality-system router. Pull state from the following sources:

1. capa-coordinator — SJS CAPA Log
2. complaint-and-event-handler — SJ Skin Complaint Log (gid 1204763097184846)
3. quality-lab-coordinator — SJS Quality Management Lab Findings sections
4. batch-lifecycle-tracker — SJS Quality Management Batch sections
5. oc3pl-order-manager — QoS metrics for the overnight window

Scan for these eight urgency categories. Silent if none surface. If any surface, fan out:

a. New OOS or OOT result — open or unclassified
b. Batch placed on hold
c. Complaint trend break — rate spike on a SKU or batch crossing the threshold in references/qos-thresholds.md
d. SAE cross-flag from complaint-and-event-handler (any [SAE Triage] task entering open state)
e. Near-expiry batch crossing the 90-day threshold for the first time
f. Retailer audit or questionnaire surfaced from outlook-asana-bridge in the window
g. Overdue CAPA or NCR closure (past target close date)
h. Recall trigger phrase from any channel

For each urgent that surfaces, post a real-time comment to the Quality Sweep Running Log task in SJS Quality Management. Running Log task GID: 1214843467424902.

Comment format for each urgent:
[Urgent — <category>] <one-line headline>
Source: <sub-skill name>
Task: <Asana link to the originating task>
First action: <recommended next step>

If zero urgents in the window, do not post. Skill exits silently.

HITL: none on the scan. None on the comment posts — these are real-time urgency surfaces, not record creates.
