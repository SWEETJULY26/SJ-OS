# Automations

**Use:** Canonical map of every recurring job for AC Brands / Sweet July Skin — cadence, source, output, owner skill, and failure mode.

**Source of truth:** **Claude Code Routines.** Every recurring job is a Routine, managed through the claude.ai Routines UI or the `mcp__Claude_Code_Remote__*` tools (`list_triggers`, `create_trigger`, `update_trigger`, `delete_trigger`, `fire_trigger`). Verify live state with `list_triggers` rather than trusting this file — the tables below are a snapshot.

**Cowork is retired.** Until 2026-07-31 this file named the Cowork scheduler as the source of truth, with a state file under `~/Library/Application Support/Claude/…/scheduled-tasks.json`. That is no longer used and no longer fires anything. Nothing in this repo should reference it, and the failure-mode advice that depended on the desktop app being open is gone with it — Routines are server-side and fire whether any app is running or not.

### Three things to get right

**Cron is stored in UTC, and this file's tables are local PT.** A job written here as `26 8 * * 1-5` (8:26 AM PT) is stored on the Routine as `26 15 * * 1-5`. Convert on the way in and out; if the conversion crosses midnight, the day-of-week field shifts too. Getting this wrong is how a morning sweep ends up running overnight.

**An existing Routine is read-only from a session.** `list_triggers` reads it; `update_trigger`, `fire_trigger` and `delete_trigger` all refuse anything created via `http_api`, which is every Routine here. A Routine may only disable *itself*. Re-enabling, re-timing, manual firing and deletion are all UI work.

**A Routine needs connectors attached, or its session has no tools.** Every working job below carries 7–9 connectors (`Microsoft_365`, `Supabase`, `Asana`, `Asana-c313a468`, `Netlify`, `Fireflies`, `Vercel`, `Canva`, `Excalidraw`) and was created via the Routines UI (`created_via: http_api`). A Routine created from inside a Claude Code session gets **no** connectors — the session can only pass through grants it holds itself, and a remote session holds none. Such a job fires into a session with no Outlook, no PLM and no Asana, which for a sweep means it fails every run. **Create recurring ops jobs in the Routines UI, not from a session.**

**Fresh session per fire.** Use `create_new_session_on_fire` for recurring ops jobs so each run starts clean. A Routine bound to a persistent session inherits that conversation's state and model, which drifts.

---

## Live state — and how to check it without getting it wrong

**Read this before trusting any audit of what is running, including the one below.**

`list_triggers` **paginates, and one-shot `send_later` triggers count against the same limit.** A pull with `limit: 25` returned 15 cron Routines and 10 one-shots; raising it to 30 surfaced 20 crons — five jobs that had been invisible, including `pd-monthly-rollup`, `ayesha-weekly-briefing-friday`, `sjs-marketing-research--weekly-run` and `pd-quarterly-rollup`. Nothing in the response signals truncation. Always raise the limit until the count stops growing, and remember that this account's list is not necessarily every Routine that exists.

**A Routine absent from `list_triggers` is not proof the job is not running.** On 2026-07-31 an audit concluded the three PD dailies "were never registered." They are in fact running and have been throughout — `sweeps/sjs-pd-morning-sweep-2026-07-30.txt` and `sjs-pd-eod-2026-07-30.html` are committed to `acb-thelanding` by the jobs themselves, with commit `4e81690` reading `sjs-pd-morning-sweep 2026-07-30 07:58 PT`. They are registered somewhere this account's Routine list does not reach. **Check the output artifact before concluding a job is dead** — for the PD jobs that means `acb-thelanding/sweeps/` and `sjs-pd-eod/`, and for the digests the relevant Asana running log.

### What is actually off, verified twice

Three morning sweeps are paused — `enabled: false`, no `ended_reason` or `suspension_reason`, so user-paused rather than system-stopped, each with `next_run_at` in the past:

| Routine | Trigger ID | Cron (UTC) | Last fired |
|---|---|---|---|
| `sjs-purchasing-morning-sweep` | `trig_01Y9ewzNuvZn24EzjzyjKyqC` | `26 15 * * 1-5` | 2026-07-17 |
| `sjs-quality-morning-sweep` | `trig_01AVRFDRc7aHu8L7gv3etEza` | `20 15 * * 1-5` | 2026-07-17 |
| `sjs-regulatory-morning-sweep` | `trig_01DY3iScZ6Ai3yV2FbbRbEMW` | `10 15 * * 1-5` | 2026-07-20 |

Also paused: `ac-brands-holiday-comms-2026` (`trig_01W9T3k8qRo7ru3JZMQwtgBN`, last fired 2026-07-13). **It auto-sends email to the team on BCC** — check the send calendar against today before re-enabling.

**Pending connectors:** `sjs-receipt-report-sweep` (`trig_01DnJ5tmwNVTvod7LXetHa1i`) is disabled on purpose. Created from a session, so it carries no connectors and cannot read Outlook or PLM. Recreate it in the Routines UI, then delete the placeholder; the prompt is on the trigger.

**Punch list:** `scheduled-prompts/REGISTRATION.md`, which also records that an existing Routine is read-only from a session — `update_trigger`, `fire_trigger` and `delete_trigger` all refuse anything created via `http_api`.

**Repo path bug, fixed 2026-07-31.** All 23 specs in `scheduled-prompts/` said the repo was cloned at `/home/user/sj-os`; it is `/home/user/SJ-OS`, and the lowercase form does not resolve on a case-sensitive filesystem. Corrected in all 23 with a locate-the-repo fallback. Worth weighing against the fact that the PD jobs were producing sane output anyway — either their environment resolves the path differently, or they coped. Do not assume the bug was harmless; do not assume it was fatal either.

## Active jobs


All times are local (PT). Cron is 5-field `min hour dom month dow`. The scheduler adds a few minutes of dispatch jitter, so observed run times sit slightly after the cron minute (e.g. the 8:00 PD sweep logs around 08:13).

### Daily (Mon–Fri)

Cron shown as **local PT**; the Routine stores UTC (PT + 7). Status as of 2026-07-31 — re-check with `list_triggers`.

| Job id | Cron (PT) | UTC | Status | Owner / routes through | Output |
|---|---|---|---|---|---|
| `sjs-pd-morning-sweep` | `0 8 * * 1-5` | `0 15 …` | **running** (not visible via this account's `list_triggers`; output in `acb-thelanding/sweeps/`) | sjs-pd-system, overnight window (5 PM prior day → now) | Recap comment on running log GID 1214208955674591; real-time URGENT comments |
| `sjs-regulatory-morning-sweep` | `10 8 * * 1-5` | `10 15 …` | **paused** | sjs-regulatory-system / sjs-regulatory-sweep Job 1 | Silent unless one of the 7 urgency categories fires; posts to Regulatory Sweep Running Log |
| `sjs-quality-morning-sweep` | `20 8 * * 1-5` (was `12 8`) | `20 15 …` | **paused** | quality-manager morning pass | Quality running log |
| `sjs-purchasing-morning-sweep` | `26 8 * * 1-5` | `26 15 …` | **paused** | purchasing-manager | Purchasing running log |
| `sjs-receipt-report-sweep` | `32 8 * * 1-5` | `32 15 …` | **created, disabled — no connectors** | inventory-manager Job 2 / `references/logiwa-receipt-report.md` | Looks back 24h (72h on Mondays) for Logiwa `Receipt Order Report` emails from `noreply@wmsnotification.com` and `noreply@wmssystem.logiwa.com`. Silent when none arrived. Stages `po_receipts` / `po_receipt_items` for HITL; never writes unattended. Reports RO class and the PLM reconciliation verdict. Placeholder `trig_01DnJ5tmwNVTvod7LXetHa1i` — recreate in the Routines UI so connectors attach, then delete it. |
| `sjs-pd-midday-sweep` | `0 12 * * 1-5` | `0 19 …` | **running** (see note above) | sjs-pd-system, midday window | Running log GID 1214208955674591 |
| `sjs-pd-eod-reconciliation` | `0 16 * * 1-5` | `0 23 …` | **running** (output `acb-thelanding/sjs-pd-eod/`) | sjs-pd-system, afternoon window (12 PM → now) + Skill 5 | 8-section payload, `pd_dashboard_runs` row, formatted comment on GID 1214208955674591 |

### Weekly

| Job id | Cron | Owner | Output |
|---|---|---|---|
| `weekly-pd-update` | `0 7 * * 1` | PD composition (audience: Nicole, Danielle, Soraya, Perrine) | HTML to acb-thelanding, Asana attach, 5-section comment on GID 1214208955674591 |
| `sjs-regulatory-weekly-digest` | `15 7 * * 1` | regulatory-manager | Regulatory weekly digest |
| `sjs-purchasing-weekly-digest` | `30 7 * * 1` | purchasing-manager | Purchasing weekly digest |
| `sjs-quality-weekly-digest` | `45 7 * * 1` (was `30 7`) | quality-manager | Quality weekly digest |
| `sjs-marketing-research--weekly-run` | `40 8 * * 1` (was `0 8`) | marketing research | Asana + Canva candidate design |
| `ayesha-weekly-briefing-friday` | `0 8 * * 5` | ayesha-weekly-briefing | Slide 5 of the AC Weekly Briefing Canva deck |
| `ac-brands-holiday-comms-2026` | `0 9 * * 1` | ac-brands-holiday-comms | Holiday email (fires only when the calendar matches; otherwise exits) |

### Monthly (first business day, days 1–3 guard inside the spec)

| Job id | Cron | Owner | Output |
|---|---|---|---|
| `sjs-regulatory-monthly-rollup-and-snapshot` | `0 7 1-3 * *` | regulatory-manager Job 8 → regulatory-status-reporter Job 2 | Cost rollup comment + frozen archive page + snapshot task. **Supersedes the old MCP `regulatory-dashboard-monthly-snapshot`.** |
| `sjs-purchasing-monthly-rollup-and-snapshot` | `10 7 1-3 * *` | purchasing-manager | Monthly rollup + snapshot |
| `quality monthly` (`sjs-quality-monthly-snapshot`) | `15 7 1-3 * *` | quality-status-reporter | Monthly quality snapshot |
| `pd-monthly-rollup` | `20 7 1-3 * *` | PD composition | Monthly PD rollup |
| `sjs-monthly-sop-sync` | `0 9 1 * *` | SharePoint → Supabase SOP/Form drift check | One-line drift summary. **Migrated from the MCP on 2026-05-26** (re-created in the scheduler UI of the day; MCP copy `sop-sync-monthly` disabled). |

### Quarterly (days 1–3 of Jan/Apr/Jul/Oct)

| Job id | Cron | Owner | Output |
|---|---|---|---|
| `sjs-regulatory-quarterly-cost-rollup` | `5 7 1-3 1,4,7,10 *` (was `0 7`) | regulatory-manager | Quarterly cost rollup |
| `sjs-purchasing-quarterly-rollup-and-snapshot` | `20 7 1-3 1,4,7,10 *` (was `10 7`) | purchasing-manager | Quarterly rollup + snapshot |
| `sjs-quality-quarterly-rollup` | `30 7 1-3 1,4,7,10 *` | quality-status-reporter | Quarterly quality rollup |
| `pd-quarterly-rollup` | `45 7 1-3 1,4,7,10 *` | PD composition | Quarterly PD rollup |

### Other cadence

| Job id | Cron | Owner | Notes |
|---|---|---|---|
| `sjs-monthly-sop-run` | `0 7 8-14 * 4` | supply-demand-planner | Monthly S&OP on the 2nd Thursday. Asks Alvin which forecast plan first (STEP 0). Unrelated to `sop-sync-monthly`. |
| `ac-brands-holiday-comms-memorial-day-2026` | one-time `fireAt` | ac-brands-holiday-comms | Disabled (past). |

### Manual / not scheduled

- **Ayesha Friday briefing** beyond the Canva slide — `ayesha-weekly-briefing`. The Canva slide itself IS scheduled as `ayesha-weekly-briefing-friday` (`0 15 * * 5` UTC, verified enabled and last fired 2026-07-31); only the wider Friday sweep is manual.
- **Quarterly margin portfolio review** — `sjs-margin-portfolio-review`, end of quarter, manual.

---

## Throttling note (`global_limit` skips)

**Historical, Cowork-era.** On 2026-05-22 and 2026-05-25 the Cowork runner recorded `global_limit` skips on several morning sweeps and weekly digests — a Cowork-level concurrency cap, not a tunable in `policy-limits.json`. The cause was exact-minute cron collisions. On 2026-05-26 the five worst offenders were de-clustered through the Cowork scheduler UI:

| Job | Was | Now |
|---|---|---|
| `sjs-quality-weekly-digest` | `30 7 * * 1` | `45 7 * * 1` |
| `sjs-marketing-research--weekly-run` | `0 8 * * 1` | `40 8 * * 1` |
| `sjs-quality-morning-sweep` | `12 8 * * 1-5` | `20 8 * * 1-5` |
| `sjs-regulatory-quarterly-cost-rollup` | `0 7 1-3 1,4,7,10 *` | `5 7 1-3 1,4,7,10 *` |
| `sjs-purchasing-quarterly-rollup-and-snapshot` | `10 7 1-3 1,4,7,10 *` | `20 7 1-3 1,4,7,10 *` |

The cap itself couldn't be raised from config, so the fix was spreading cron minutes. Whether Routines has an equivalent concurrency cap is untested — the de-clustered minutes were carried over, so the collisions have not recurred either way. Keep spreading minutes as a default.

---

## Consolidation, 2026-05-26 (Priority 3, Bridge & System Audit) — historical

Kept for the reasoning, not as current guidance. Both schedulers named below are retired: the `scheduled-tasks` MCP in 2026-05, Cowork on 2026-07-31. Routines is the third and current mechanism.

Two schedulers had been running in parallel: Cowork (the real cadence) and the `scheduled-tasks` MCP (4 jobs). Cowork was confirmed as the single source of truth; the MCP was retired in place (disabled, not deleted — see the MCP note above).

- `sop-sync-monthly` (MCP) → **migrated** to Cowork as `sjs-monthly-sop-sync`, re-created through the scheduler UI (cron `0 9 1 * *`, spec at `~/Documents/Claude/Scheduled/sjs-monthly-sop-sync/SKILL.md`). MCP copy disabled.
- `regulatory-dashboard-monthly-snapshot` (MCP) → **disabled as redundant**. Cowork's `sjs-regulatory-monthly-rollup-and-snapshot` already fires regulatory-status-reporter Job 2.
- `sjs-regulatory-morning-sweep`, `sjs-regulatory-weekly-digest` (MCP copies) → **disabled as orphan duplicates** of the live Cowork jobs of the same name (they were already off).

Mechanism note: the original plan was a single app-closed shell script, but IT blocks Full Disk Access for Terminal, so the file-surgery route was abandoned. Instead the Cowork-side changes (the `sjs-monthly-sop-sync` migration and the five cron de-clusters) were made in the scheduler UI, and the MCP-side changes were made with the daemon-safe `mcp__scheduled-tasks__update_scheduled_task` tool. Backups of both state files are under `Skill Builder/scheduler-backup-*`.

Two dormant Cowork spec folders, superseded by live jobs, were deleted: `sjs-monday-pd-briefing` (replaced by `weekly-pd-update`) and `sjs-pd-eod-recap` (replaced by `sjs-pd-eod-reconciliation`). The hand-written `sop-sync-monthly` spec was also removed once the UI created its own under `sjs-monthly-sop-sync`.

---

## On failure

If a daily/weekly job doesn't run, trigger it manually by naming its work (e.g. "run today's PD recap", "run the regulatory morning sweep"). Each spec is self-contained and reproduces the same workflow on demand. If a job silently stops appearing in the running logs, run `list_triggers` and check its `enabled`, `last_fired_at` and `next_run_at`. A `next_run_at` in the past with `enabled: false` means it was paused, not that it failed. Routines fire server-side, so nothing needs to be open — a job that stopped was paused, deleted, or never registered.
