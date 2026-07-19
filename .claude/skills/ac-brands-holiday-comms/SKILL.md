---
name: ac-brands-holiday-comms
description: >
  Manage and auto-send the AC Brands annual holiday communications system. Use this skill
  whenever Alvin asks about holiday reminder emails, wants to send or schedule a holiday
  notice to the team, references the holiday calendar, asks "has the holiday email gone out",
  "send the Thanksgiving reminder", "draft the R&R email", "set up holiday comms for the year",
  or any request related to notifying the AC Brands team of upcoming office closures.
  Covers all 11 sends across 3 email templates — standalone weekly reminders (T1), the
  November Holiday Season Overview (T2), and the December R&R Heads-Up (T3). Auto-sends
  on scheduled dates via Cowork automation. Always sends from alvin@ac-brands.com with
  all team members on BCC.
---

# AC Brands Holiday Communications System

Automated annual holiday notification system for AC Brands. Sends warm, casual emails
to the full team before each office closure, pulled from the 2026 AC Brands Holiday
Calendar in Asana (Operations team, project GID: `1214055559810920`).

---

## Sender & Recipients

| Field | Value |
|-------|-------|
| **From** | Alvin Belt — alvin@ac-brands.com |
| **To** | alvin@ac-brands.com |
| **BCC** | alvin@ac-brands.com, kate@ac-brands.com, soraya@ac-brands.com, ciarra@ac-brands.com, ivy@ac-brands.com, nicole@ac-brands.com, danielle@ac-brands.com |

---

## Email Templates

### T1 — Standard Weekly Reminder
_Sent 1 week before each standalone holiday or holiday cluster._

**Subject:** `Friendly Reminder: Office Closed [DAY, MONTH DATE] for [HOLIDAY]`

**Body:**
```
Hey team! 👋

Just a quick heads-up — the AC Brands office will be closed [DAY, MONTH DATE]
in observance of [HOLIDAY]. We'll be back and ready to go on [RETURN DATE].

Make sure to wrap up anything time-sensitive before then, and don't forget
to set your out-of-office if needed!

Enjoy the time off — you've earned it. 🙌

Alvin
```

---

### T2 — November Holiday Season Overview
_Sent ~November 2. Full picture of every closure from Veterans Day through end of year._

**Subject:** `AC Brands Holiday Schedule: What's Coming Up Through End of Year 🎉`

**Body:**
```
Hey team! 👋

Can you believe we're already in November? As we head into the holiday stretch,
I wanted to give everyone a full picture of our upcoming office closures through
the end of the year so you can plan ahead. Here's what's coming:

🇺🇸 Veterans Day — Wednesday, November 11
    Office closed. Back Thursday, November 12.

🦃 Thanksgiving — Thursday, November 26 & Friday, November 27
    Office closed both days. Back Monday, November 30.

🎄 Christmas Eve & Christmas Day — Thursday, December 24 & Friday, December 25
    Office closed both days.

🌟 R&R Period — Monday, December 21 through Sunday, January 3, 2027
    The office will be closed for our annual rest & recharge period.
    We'll be back and ready to go on Monday, January 4, 2027.

🥂 New Year's Eve & New Year's Day — Thursday, December 31 & Friday, January 1
    Included in the R&R Period above.

It's going to be a great end to the year — make sure to plan your projects
and deadlines accordingly. As always, set your out-of-office before any
extended time away.

Wishing everyone a wonderful holiday season ahead! 🙏

Alvin
```

---

### T3 — December R&R Heads-Up
_Sent ~December 1. Focused reminder that the R&R wind-down is just weeks away._

**Subject:** `R&R Period Reminder: Office Closes December 21 🌟`

**Body:**
```
Hey team! 👋

Just a friendly reminder that our annual R&R Period is just around the corner!

🌟 R&R Period: Monday, December 21, 2026 – Sunday, January 3, 2027
    We'll be back in the office on Monday, January 4, 2027.

That's less than a month away — so now is a great time to:
  • Wrap up any outstanding projects or deliverables
  • Communicate timelines to any external partners
  • Set up your out-of-office before December 21

Also a reminder that Christmas Eve (Dec 24), Christmas Day (Dec 25),
New Year's Eve (Dec 31), and New Year's Day (Jan 1) all fall within
the R&R window.

Enjoy the wind-down — you've all worked hard this year and deserve
every moment of rest. See you on the other side! 🎉

Alvin
```

---

## Full Send Calendar — 11 Sends

| # | Holiday(s) | Send Date | Template | Subject Tokens |
|---|-----------|-----------|----------|----------------|
| 1 | Memorial Day | Mon, May 18, 2026 | T1 | Monday, May 25 / Memorial Day / Tuesday, May 26 |
| 2 | Juneteenth | Mon, Jun 12, 2026 | T1 | Friday, June 19 / Juneteenth / Monday, June 22 |
| 3 | Independence Day (Observed) | Mon, Jun 26, 2026 | T1 | Friday, July 3 / Independence Day (Observed) / Monday, July 6 |
| 4 | Labor Day | Mon, Aug 31, 2026 | T1 | Monday, September 7 / Labor Day / Tuesday, September 8 |
| 5 | **Holiday Season Overview** | Mon, Nov 2, 2026 | **T2** | _(no tokens — full template)_ |
| 6 | Veterans Day | Mon, Nov 4, 2026 | T1 | Wednesday, November 11 / Veterans Day / Thursday, November 12 |
| 7 | Thanksgiving + Day After | Mon, Nov 19, 2026 | T1 (combined) | Thursday & Friday, November 26–27 / Thanksgiving Holiday / Monday, November 30 |
| 8 | **December R&R Heads-Up** | Mon, Dec 1, 2026 | **T3** | _(no tokens — full template)_ |
| 9 | R&R Period | Mon, Dec 14, 2026 | T1 (combined) | Monday, December 21 / R&R Period / Monday, January 4, 2027 |
| 10 | Christmas Eve + Christmas Day | Mon, Dec 17, 2026 | T1 (combined) | Thursday & Friday, December 24–25 / Christmas Holiday / See you after R&R! |
| 11 | New Year's Eve + New Year's Day | Mon, Dec 28, 2026 | T1 (combined) | Thursday & Friday, December 31 – January 1 / New Year's Holiday / Monday, January 4, 2027 |

---

## Tone Guidelines

- **Warm and casual** — this is an internal team email, not a formal HR notice
- Always open with `Hey team! 👋`
- Always close with `Alvin` (no title, no formal sign-off)
- Use emojis sparingly but intentionally — one per holiday callout is fine
- Mention the return date in every email — this is the most useful info
- Remind team to set out-of-office for multi-day closures
- For combined holidays (e.g. Thanksgiving + Day After), address both in one natural sentence

---

## Cowork Automation Instructions

The Cowork automation handles two responsibilities: (1) syncing each holiday task to the
AC Brands Org Calendar in Outlook, and (2) auto-sending holiday reminder emails on schedule.

---

### Step 1 — Outlook Calendar Sync (Run Once at Setup)

For each of the 12 holiday tasks, Cowork navigates directly into the Asana task and uses
the built-in **Outlook Calendar app integration** to create the event — exactly as shown
in the Asana UI (Apps → Outlook Calendar → "Create new event").

**For each holiday task, Cowork:**
1. Opens the task via its Asana permalink
2. In the Apps panel, triggers **Outlook Calendar → Create new event**
3. In the dialog:
   - Sets **Calendar** to **AC Brands Org Calendar** (not the personal Calendar)
   - Confirms event title matches the task name (auto-populated)
   - Confirms start/end dates match the task dates (auto-populated)
   - Ensures **All day event** is checked
   - Unchecks **Create a Teams meeting link for this event**
   - Clicks **Submit**
4. Confirms the event was created, moves to next task

**Holiday tasks to sync (in order):**
| Holiday | Task GID | Permalink | Start | End |
|---------|----------|-----------|-------|-----|
| Memorial Day | 1214041881992469 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214041881992469) | 2026-05-25 | 2026-05-25 |
| Juneteenth | 1214048194080090 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214048194080090) | 2026-06-19 | 2026-06-19 |
| Independence Day (Observed) | 1214041881995784 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214041881995784) | 2026-07-03 | 2026-07-03 |
| Labor Day | 1214041882001789 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214041882001789) | 2026-09-07 | 2026-09-07 |
| Veterans Day | 1214048194083397 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214048194083397) | 2026-11-11 | 2026-11-11 |
| Thanksgiving Day | 1214048194088081 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214048194088081) | 2026-11-26 | 2026-11-26 |
| Day After Thanksgiving | 1214055559827083 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214055559827083) | 2026-11-27 | 2026-11-27 |
| Christmas Eve | 1214040452721724 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214040452721724) | 2026-12-24 | 2026-12-24 |
| Christmas Day | 1214040452725665 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214040452725665) | 2026-12-25 | 2026-12-25 |
| New Year's Eve | 1214041882017722 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214041882017722) | 2026-12-31 | 2026-12-31 |
| R&R Period | 1214040452731449 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214040452731449) | 2026-12-21 | 2027-01-03 |
| New Year's Day 2027 | 1214041882018652 | [open](https://app.asana.com/1/1200120716421441/project/1214055559810920/task/1214041882018652) | 2027-01-01 | 2027-01-01 |

---

### Step 2 — Auto-Send Holiday Reminder Emails (Recurring, Date-Triggered)

Monitors the send calendar and fires each email automatically on the scheduled date.
No approval needed — all drafts are pre-approved.

**Trigger logic:**
1. On each send date in the table above, identify the correct template (T1, T2, or T3)
2. For T1: populate `[DAY, MONTH DATE]`, `[HOLIDAY]`, and `[RETURN DATE]` from the Send Calendar tokens column
3. For T2 and T3: send the full template as-is (no token substitution needed)
4. Send via Microsoft 365 Outlook with the recipient configuration above
5. Log send confirmation to the AC Brands Holiday Calendar Asana project as a comment on the relevant holiday task

**Error handling:**
- If a send fails, retry once after 30 minutes
- If retry fails, flag to alvin@ac-brands.com with subject: `⚠️ Holiday Email Send Failed: [HOLIDAY]`

---

## Year-to-Year Maintenance

At the start of each new year:
1. Update the Asana holiday project with the new year's dates
2. Update the Send Calendar table in this skill with new dates
3. Update all T2 and T3 body copy date references
4. Update BCC list if team membership has changed
5. Archive the previous year's Asana holiday project

---

## Asana Project Reference

- **Project:** 2026 AC Brands Holiday Calendar
- **GID:** `1214055559810920`
- **Team:** Operations
- **Workspace:** ac-brands.com (`1200120716421441`)
- **View:** Calendar

Holiday task GIDs for reference:
| Holiday | Task GID |
|---------|----------|
| Memorial Day | 1214041881992469 |
| Juneteenth | 1214048194080090 |
| Independence Day (Observed) | 1214041881995784 |
| Labor Day | 1214041882001789 |
| Veterans Day | 1214048194083397 |
| Thanksgiving Day | 1214048194088081 |
| Day After Thanksgiving | 1214055559827083 |
| Christmas Eve | 1214040452721724 |
| Christmas Day | 1214040452725665 |
| New Year's Eve | 1214041882017722 |
| R&R Period | 1214040452731449 |
| New Year's Day 2027 | 1214041882018652 |
