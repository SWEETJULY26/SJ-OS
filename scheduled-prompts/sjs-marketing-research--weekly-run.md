# Scheduled task: sjs-marketing-research--weekly-run

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- (none — this task needs no project skills)
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse). Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
Go to the SJ SKIN — Marketing Research Intelligence project in Asana. Find all tasks that are due this week. For each due task, read the task description carefully — it contains the full research prompt. Run the research using web search. Then post the completed research output as a comment on that Asana task and mark the task complete.

Start with any task labeled "Weekly Viral Social Recap" first, then the competitor snapshot for the current week.
