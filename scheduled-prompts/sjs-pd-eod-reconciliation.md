# Scheduled task: sjs-pd-eod-reconciliation

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/sjs-pd-system/SKILL.md`
- `/home/user/sj-os/.claude/skills/asana-pd-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/fireflies-asana-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/outlook-asana-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/asana-plm-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/outlook-plm-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-status-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-master/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
Run the AC Brands PD System reconciliation for the afternoon window (12 PM PT → now).

Read /home/user/sj-os/.claude/skills/sjs-pd-system/SKILL.md and route through it. Fire skills as warranted. Create, comment, and write to PLM the same way the 8 AM and 12 PM runs do.

DEDUP: Before creating any task or comment, check Asana task GID 1214208955674591 (the running log) for prior runs today. Skip anything already actioned.

URGENT handling — same five rules as the morning runs. Post real-time "🚨 URGENT — [HH:MM PT] — [item + Asana link]" comments to GID 1214208955674591 as they surface during this run:
- Priority = High and overdue or blocked
- Complaint or adverse-event signal
- Open PO with no vendor ack > 48 hours
- Stability or COA fail
- Launch at risk inside 30 days

After reconciliation completes, build the day's dashboard in this order. Compile from the day's combined activity across all three runs (5 PM PT yesterday → now), not just the afternoon window.

STEP A — Compile the 8-section payload. Each section pulls from specific source skills:

1. Meeting Intel — Skill 2 (fireflies-asana-bridge), PD topics only. Meeting summaries, decisions surfaced, action items captured.
2. Vendor & Partner Movement — Skills 3 (outlook-asana-bridge) + 6 (outlook-plm-bridge). Supplier emails, PO acks, sample shipments, batch updates, vendor compliance.
3. Asana Activity — Skill 1 (asana-pd-manager). Tasks created, status moves, comments, stage transitions.
4. PLM Activity — Skills 6 (outlook-plm-bridge) + 4 (asana-plm-bridge) folded silently. New batches, vendor records, formula approvals, BOM updates, stability data.
5. Decisions Logged — Skills 1 + 3 + 6. Explicit decisions captured today across Asana comments, vendor emails, and PO updates. A decision in a vendor email is just as real as one in Asana.
6. Decisions Pending — Skills 1 + 3 + 6. Outstanding decisions waiting for input, aged 3+ days.
7. Blockers Added or Cleared — Skills 1 + 3 + 6. Blockers appearing today + blockers resolved today. A blocker that surfaces because Element said "can't ship until June" comes through Skill 6's PO update, not Asana — capture all three streams.
8. Tomorrow's Top Three — Skills 1 + 3 + 6, signal-ranked across all three streams. Ranking priority: overdue → blocker age → decision pressure → 48h milestones.

Format the payload as JSON with these exact keys:

{
  "meeting_intel": [...],
  "vendor_partner_movement": [...],
  "asana_activity": [...],
  "plm_activity": [...],
  "decisions_logged": [...],
  "decisions_pending": [...],
  "blockers": [...],
  "tomorrows_top_three": [...],
  "summary": { "rag_driver": "...", "what_shifted": "...", "watch_tomorrow": "..." }
}

Each item in each section should include at minimum: description (string), source (which skill surfaced it), and asana_url (string, where applicable). Add other fields as needed per section (e.g. days_open for vendors, age_days for decisions, launch_date for milestones).

The summary block is required on every run, quiet days included. Three fields, plain prose, no bullets:
- rag_driver: the one or two facts that set today's RAG color. On Red, name the launch/complaint/PO at fault. On Yellow, name the aging item. On Green, say "no material risk surfaced."
- what_shifted: what's new vs. yesterday's EOD row in pd_dashboard_runs. If today is Red and yesterday was also Red on the same driver, say so (e.g. "Pineapple Punch 5/19 carry-over from 5/13 EOD — no new movement"). If a Red cleared to Green/Yellow, name it. If a Yellow escalated to Red, name the trigger. Read the most recent prior row from Supabase to compare.
- watch_tomorrow: the single item the morning sweep should lead with. Usually mirrors the top of tomorrows_top_three but can diverge when a delayed signal (e.g. vendor reply expected overnight) outranks the queue.

THRESHOLDS:
- Vendor silence: a vendor with no movement for 2 business days appears in Section 2 as a flagged item
- Decision aging: a decision pending 3+ days is included in Section 6
- Blocker age: weighted in Section 8 ranking

QUIET DAY CHECK: If no material activity surfaced — no urgents, total items across all eight sections under 3, no decisions pending, no blockers — set quiet_day = true. The Asana post collapses to a single line + a one-line summary; Supabase still gets a row with the summary block populated.

STEP B — Determine RAG color:
- Red: any urgents OR any launches at risk inside 14 days OR any complaint/adverse-event/recall signal
- Yellow: any launches at risk inside 30 days OR any vendor silent past 2 business days OR any overdue High priority OR any decision pending 3+ days
- Green: otherwise

STEP C — Write one row to Supabase project ujkabbffvhpewpbttmmy, table public.pd_dashboard_runs. Use the Supabase MCP execute_sql tool. Single insert with columns:
- run_date: today YYYY-MM-DD
- run_timestamp: now() with timezone
- rag_color: from Step B
- quiet_day: boolean from quiet day check
- payload: full 9-key JSONB from Step A (the 8 sections + summary block)

STEP D — Render the final Asana comment using Skill 5 (sjs-status-reporter). Pass Skill 5 the payload, RAG color, and quiet_day flag. Skill 5 owns the final formatting and brand voice and posts to Asana task GID 1214208955674591 (append, do not replace).

Skill 5 directives for this output:
- Match SJS Ops Dashboard family styling
- Render the 8 sections in numerical order, but PRUNE quiet sections (zero items get omitted, not rendered as "None")
- Render the Summary block last, under a "📌 Summary" header, three labeled lines: "RAG driver:", "What shifted:", "Watch tomorrow:". Always render — never prune, even on Green or quiet days.
- Quiet day: collapse the sections to one line — "🟢 [Date] EOD — quiet day, no material activity." — then still render the Summary block underneath (three lines, terse).
- Open with the RAG header: "🟢🟡🔴 RAG Color — [Today's Date] EOD" using the matching color emoji for the RAG state
- Skill 4 (asana-plm-bridge) signals fold into Section 4 (PLM Activity) silently — never call out Skill 4 by name in the post
- No closing line beyond the Summary block, no signoff

If the Supabase write in Step C fails, run Step D anyway and append a "⚠️ Supabase write failed: [error]" line at the bottom of the Asana comment so the gap is visible. The Summary block still renders — its What shifted line will read "comparison unavailable — Supabase write failed."
