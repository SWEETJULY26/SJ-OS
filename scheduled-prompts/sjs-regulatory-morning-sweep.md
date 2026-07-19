# Scheduled task: sjs-regulatory-morning-sweep

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
Use only the attached connectors: Asana, Asana(sse), Microsoft 365, Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral. The acb-thelanding clone is read-only; never commit or push to it.

## Task
Run the SJS Regulatory Sweep — daily morning pass.

Read /mnt/skills/user/sjs-regulatory-sweep/SKILL.md (or the cowork-resolved path) and execute Job 1. Urgency rules are in references/urgency-thresholds.md (last_updated 2026-05-12).

Window: since the prior weekday's 8:10 AM PT through now. On a Monday, window covers Friday 8:10 PT through now plus the weekend.

Route through sjs-regulatory-system. Scan:
- Asana — SJS Regulatory Management (gid 1214660807386611), SJS Reportable Events (gid 1214660834583706)
- outlook-asana-bridge — regulatory-tagged Inbox + Sent (Amy Pedrero, Heather Folkes, Teona Bebia, Ecomundo, agency channels, retailer compliance, customs)
- fireflies-asana-bridge — regulatory-tagged action items in window
- outlook-plm-bridge — compliance docs arriving (CoCs, registration confirmations, formula clearances)
- Quality cross-flag queue — `[Reg Flag Pending — regulatory-manager]` aged >3 days
- logistics-manager — customs holds, import refusals
- SB 312 RTK marker — canonical task 1211320433655582 surfaces every morning until closed

Surface anything meeting the seven urgency categories from references/urgency-thresholds.md:
4a — hard statutory clocks (SAE <5 business days, recall in play, MoCRA/state/CA/UK/EU renewal ≤30d, EPR deadline ≤30d)
4b — Pedrero artifact returned, Pedrero queue >5 items aging >7d, retailer attestation ≤14d, new retailer questionnaire, Ulta Marketplace request
4c — new customs hold, repeat hold same market <30d, import refusal/detention
4d — PD cross-flags (reformulation with existing claims, artwork without compliance check, formula approved without clearance matrix update)
4e — Quality cross-flags (`[Reg Flag Pending — regulatory-manager]` aged >3d, OOS/hold with SAE implications)
4f — strategic horizon (EPR trigger trailing-12 ≥80% of $5M global / $1M CA, new state EPR program, regulation enforcement <30d including Canada extended allergens 2026-07-31)
4g — California SB 312 (canonical task open, SB 312 listing event due, CDPH inquiry)

If nothing meets the thresholds, end silently. No posts, no narration.

If anything meets the thresholds, post to the regulatory running log task (Cross-Skill Dashboard section gid 1214660230826189, task titled "Regulatory Sweep Running Log") in this format, one line per urgent, newest first:

URGENT — [HH:MM PT] — [signal] — [Asana link or evidence link]

Dedup: scan today's prior comments on the running log before posting. Skip any signal already surfaced and not yet handled.

Execute fully. Do not ask permission. Do not produce a written brief. The sweep is read-only — any required action is owned by the underlying skill (regulatory-manager, claims-il-and-label-keeper, adverse-event-and-recall-reporter) under its own HITL.
