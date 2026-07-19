# Scheduled task: sjs-pd-midday-sweep

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/ac-brands-pd-system/SKILL.md`
- `/home/user/sj-os/.claude/skills/asana-pd-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/fireflies-asana-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/outlook-asana-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/asana-plm-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/outlook-plm-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-status-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-master/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Fireflies, Microsoft 365, Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
Run the AC Brands PD System reconciliation for the morning window (8 AM PT → now).

Read /mnt/skills/user/ac-brands-pd-system/SKILL.md to confirm router state, then route through it. Fire skills as warranted by the signals in the window:

- Skill 2 (fireflies-asana-bridge): pull transcripts in the window
- Skill 3 (outlook-asana-bridge): scan inbox and Sent Items
- Skill 6 (outlook-plm-bridge): file PLM-bound docs (PO acks, COAs, vendor records, batch data)
- Skill 1 (asana-pd-manager): create tasks, comments, stage moves
- Skill 4 (asana-plm-bridge): sync approvals or batch data into PLM and back

DEDUP: Before creating any task or comment, check Asana task GID 1214208955674591 (the running log) for prior runs today. If a signal was already actioned in an earlier run, skip it. The running log comments are the source of truth for what's been handled.

Execute fully. Do not ask permission. Do not produce a written brief.

URGENT — if any of the following surface, post a "🚨 URGENT — [HH:MM PT] — [item + Asana link]" comment on Asana task GID 1214208955674591 the moment it's detected:

- Priority = High and overdue or blocked
- Complaint or adverse-event signal
- Open PO with no vendor ack > 48 hours
- Stability or COA fail
- Launch at risk inside 30 days

End silently otherwise.
