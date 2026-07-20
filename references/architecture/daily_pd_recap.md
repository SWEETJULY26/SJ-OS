# Daily PD Recap — Orchestration Spec

**Use:** Reproduces the 2 PM PT daily PD recap. Reverse-engineered from comment history on running log task `1214208955674591` between 2026-04-22 and 2026-04-29.

**Trigger:** 2 PM PT, daily (Cowork scheduled task). Manual fallback: "run today's PD recap."

**Output:** Comment posted to running log task `1214208955674591` in AC Brands PD + Ops Dashboard. HTML dashboard saved to outputs as `sjs-pd-recap-YYYY-MM-DD.html`.

---

## Architecture principle

This automation is a **composition of PD skills**, not a parallel tool implementation. Each PD skill already encapsulates its own tool patterns (Fireflies date-not-keyword, Outlook broad afterDateTime, Asana portfolio sweep, PLM SELECT). The recap calls those skills and lets them do the underlying work.

If a tool pattern needs to change (e.g., Fireflies API gets a new filter, Asana adds a new portfolio field), update the skill that owns it. The recap automatically benefits.

---

## Prompt structure

```
Run today's daily PD recap for Sweet July Skin product development.
Today's date is [auto-resolve]. Current ISO week is [auto-resolve].

ORCHESTRATION

Activate the PD skills in this order. Each skill returns its findings to feed
the synthesis step. Run silently — do not narrate which skill is firing.

1. fireflies-asana-bridge (Skill 2)
   Scope: today's meetings only.
   Output expected: action items, decisions, status signals, PLM flags.

2. outlook-asana-bridge (Skill 3)
   Scope: today's emails only, Inbox + Sent Items.
   Output expected: triage report — urgent items, action-needed (received and
   sent), no-reply-yet, PLM flags.

3. outlook-plm-bridge (Skill 6)
   Scope: today's emails only, Inbox + Sent Items.
   Output expected: PLM-bound items by flow (PO acks, batches, vendor updates,
   formula approvals, test results, invoices, BOM updates).

4. asana-pd-manager (Skill 1)
   Scope: current state of the 2026-2028 PD Roadmap portfolio + recent activity
   on each portfolio item over the past 24 hours.
   Output expected: RAG roll-up across all active projects, status changes
   since yesterday, new projects added.

5. sjs-status-reporter (Skill 5)
   Format: Daily recap.
   Inputs: outputs from Skills 1, 2, 3, 6.
   Output: the comment text below + the HTML dashboard.

OUTPUT — COMMENT TO RUNNING LOG

Post a comment to task 1214208955674591 with this exact structure:

🌅 DAILY EOD RECAP — [Weekday, Month Day, Year] · 2:00 PM PT — Week [N]

Top 5 most important things from today:
1. [item with context — owner and due date if applicable]
2. [item]
3. [item]
4. [item]
5. [item]

RAG summary across active SJ Skin PD projects:
On Track: [N] · At Risk: [N] · Off Track: [N] · No Status: [N] · Dropped: [N]

New projects added since last run:
[list, or "None" if none]

Other signal worth flagging:
• [bonus item from email/meeting/PLM intel]
• [bonus item]
• [bonus item]

Full HTML dashboard saved to outputs as sjs-pd-recap-[YYYY-MM-DD].html

OUTPUT — HTML DASHBOARD

Skill 5 generates the HTML dashboard following the SJS brand spec (loads
sweet-july-skin-brand for canonical fonts, colors, voice). Six tabs: Overall ·
Week Recap · Week Ahead · By Supplier · Signal Feed · Creative. Save to
/mnt/user-data/outputs/sjs-pd-recap-[YYYY-MM-DD].html.

CONFIRMATION

Recurring scheduled task with no HITL approval required. The component skills
each have their own confirmation rules for any writes — none of those should
trigger during a recap run because the recap is read + synthesize only. If a
skill flags a write candidate (e.g., Skill 3 wants to create an Asana task
from an inbox item), pass that flag through to Alvin for next-day handling
rather than executing it.

WHAT NOT TO DO

- Do not bypass the skills and pull from tools directly. The skills own those
  patterns.
- Do not narrate which skill is firing. Run silently and post the finished
  comment.
- Do not pad an empty day. If skills return nothing substantive, write a
  short recap noting the slow day.
- Do not include items that aren't sourced. Every line in the comment should
  come from a skill output.
```

---

## Skill prioritization for the Top 5

When Skill 5 synthesizes the Top 5, weight items in this order:

1. **Items affecting an immovable launch date** — Pineapple Punch July 19, Soursop UBM mid-June, etc.
2. **Status changes** — anything that flipped RAG color today
3. **Decisions captured** — explicit approvals, sign-offs, walk-aways from Skill 2 (meetings) or Skill 3 (sent emails)
4. **Blockers cleared or surfaced** — from any of Skills 1, 2, 3, 6
5. **Supplier deliverables in or out** — POs placed, samples shipped, COAs received, from Skill 6 mostly

Within those weights, prefer items with concrete artifacts (PO numbers, dollar amounts, ship dates, FedEx tracking) over narrative-only items.

---

## Format evolution

The format settled around 2026-04-28. Earlier recaps (Apr 22–25) used these variations that have since been replaced:

- Title prefix: "📊 SJS PD Recap" → "🌅 DAILY EOD RECAP"
- Section name for top items: "TOP 5 PRIORITY ACTIONS" / "Top 5 most important things today" / "TOP THINGS TODAY" → settled on "Top 5 most important things from today"
- RAG summary names: "RAG Summary" / "PORTFOLIO RAG" / "RAG SUMMARY (X active)" → settled on "RAG summary across active SJ Skin PD projects"
- Emoji indicators in counts: included in some, not in others → keeping plain (`On Track: 10 · At Risk: 8 · Off Track: 1 · Dropped: 1`) since the structured prefix isn't always rendering well in Asana

If a refresh on the format is needed, the latest comment on task `1214208955674591` is the source of truth.

---

## Adjacent automation — Monday Weekly Briefing

A separate scheduled task (`sjs-monday-pd-briefing`) runs Monday mornings and posts a different format to the same running log. Same orchestration model, longer time window. See `_shared/monday_weekly_briefing.md`.
