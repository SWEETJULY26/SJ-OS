# Automations

**Use:** Canonical map of every recurring job for AC Brands / Sweet July Skin — cadence, source, output, owner skill, and failure mode.

**Source of truth:** the **Cowork scheduler**. Every active recurring job lives there. Its state file is `~/Library/Application Support/Claude/local-agent-mode-sessions/<owner>/<session>/scheduled-tasks.json` (call it File A); each job's prompt spec lives in `~/Documents/Claude/Scheduled/<job-id>/SKILL.md`. Jobs are created through the Claude desktop "schedule" action — there is no MCP/CLI tool that writes File A, so register and re-time jobs through the app UI (or edit File A with the app fully quit; see the consolidation script note below).

**The `scheduled-tasks` MCP is no longer an orchestrator.** As of 2026-05-26 all four of its jobs are disabled in place — none fire. They aren't hard-deleted: the MCP exposes no delete tool, only `enabled: false`, and IT restrictions (no Full Disk Access for Terminal) block the file-level cleanup of File B. So the registry sits inert rather than empty. Do not add or re-enable recurring jobs through the `mcp__scheduled-tasks__*` tools — that re-creates the parallel-scheduler split this consolidation removed. All four MCP entries can be hard-removed later if file access ever becomes available.

---

## Active Cowork jobs

All times are local (PT). Cron is 5-field `min hour dom month dow`. The scheduler adds a few minutes of dispatch jitter, so observed run times sit slightly after the cron minute (e.g. the 8:00 PD sweep logs around 08:13).

### Daily (Mon–Fri)

| Job id | Cron | Owner / routes through | Output |
|---|---|---|---|
| `sjs-pd-morning-sweep` | `0 8 * * 1-5` | sjs-pd-system, overnight window (5 PM prior day → now) | Recap comment on running log GID 1214208955674591; real-time URGENT comments |
| `sjs-regulatory-morning-sweep` | `10 8 * * 1-5` | sjs-regulatory-system / sjs-regulatory-sweep Job 1 | Silent unless one of the 7 urgency categories fires; posts to Regulatory Sweep Running Log |
| `sjs-quality-morning-sweep` | `20 8 * * 1-5` (was `12 8`) | quality-manager morning pass | Quality running log |
| `sjs-purchasing-morning-sweep` | `26 8 * * 1-5` | purchasing-manager | Purchasing running log |
| `sjs-pd-midday-sweep` | `0 12 * * 1-5` | sjs-pd-system, midday window | Running log GID 1214208955674591 |
| `sjs-pd-eod-reconciliation` | `0 16 * * 1-5` | sjs-pd-system, afternoon window (12 PM → now) + Skill 5 | 8-section payload, `pd_dashboard_runs` row, formatted comment on GID 1214208955674591 |

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
| `sjs-monthly-sop-sync` | `0 9 1 * *` | SharePoint → Supabase SOP/Form drift check | One-line drift summary. **Migrated from the MCP on 2026-05-26** (re-created in the Cowork UI; MCP copy `sop-sync-monthly` disabled). |

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

- **Ayesha Friday briefing** beyond the Canva slide — `ayesha-weekly-briefing`, Friday manual sweep.
- **Quarterly margin portfolio review** — `sjs-margin-portfolio-review`, end of quarter, manual.

---

## Throttling note (`global_limit` skips)

On 2026-05-22 and 2026-05-25 the Cowork runner recorded `global_limit` skips on several morning sweeps and weekly digests — a Cowork-level concurrency cap, not a tunable in `policy-limits.json`. The cause was exact-minute cron collisions. On 2026-05-26 the five worst offenders were de-clustered through the Cowork scheduler UI:

| Job | Was | Now |
|---|---|---|
| `sjs-quality-weekly-digest` | `30 7 * * 1` | `45 7 * * 1` |
| `sjs-marketing-research--weekly-run` | `0 8 * * 1` | `40 8 * * 1` |
| `sjs-quality-morning-sweep` | `12 8 * * 1-5` | `20 8 * * 1-5` |
| `sjs-regulatory-quarterly-cost-rollup` | `0 7 1-3 1,4,7,10 *` | `5 7 1-3 1,4,7,10 *` |
| `sjs-purchasing-quarterly-rollup-and-snapshot` | `10 7 1-3 1,4,7,10 *` | `20 7 1-3 1,4,7,10 *` |

The cap itself can't be raised from config; if skips recur, spread the cron minutes further rather than looking for a limit setting.

---

## Consolidation, 2026-05-26 (Priority 3, Bridge & System Audit)

Two schedulers had been running in parallel: Cowork (the real cadence) and the `scheduled-tasks` MCP (4 jobs). Cowork was confirmed as the single source of truth; the MCP was retired in place (disabled, not deleted — see the MCP note above).

- `sop-sync-monthly` (MCP) → **migrated** to Cowork as `sjs-monthly-sop-sync`, re-created through the scheduler UI (cron `0 9 1 * *`, spec at `~/Documents/Claude/Scheduled/sjs-monthly-sop-sync/SKILL.md`). MCP copy disabled.
- `regulatory-dashboard-monthly-snapshot` (MCP) → **disabled as redundant**. Cowork's `sjs-regulatory-monthly-rollup-and-snapshot` already fires regulatory-status-reporter Job 2.
- `sjs-regulatory-morning-sweep`, `sjs-regulatory-weekly-digest` (MCP copies) → **disabled as orphan duplicates** of the live Cowork jobs of the same name (they were already off).

Mechanism note: the original plan was a single app-closed shell script, but IT blocks Full Disk Access for Terminal, so the file-surgery route was abandoned. Instead the Cowork-side changes (the `sjs-monthly-sop-sync` migration and the five cron de-clusters) were made in the scheduler UI, and the MCP-side changes were made with the daemon-safe `mcp__scheduled-tasks__update_scheduled_task` tool. Backups of both state files are under `Skill Builder/scheduler-backup-*`.

Two dormant Cowork spec folders, superseded by live jobs, were deleted: `sjs-monday-pd-briefing` (replaced by `weekly-pd-update`) and `sjs-pd-eod-recap` (replaced by `sjs-pd-eod-reconciliation`). The hand-written `sop-sync-monthly` spec was also removed once the UI created its own under `sjs-monthly-sop-sync`.

---

## On failure

If a daily/weekly job doesn't run, trigger it manually by naming its work (e.g. "run today's PD recap", "run the regulatory morning sweep"). Each spec is self-contained and reproduces the same workflow on demand. If a job silently stops appearing in the running logs, check File A for its `lastRunAt` and confirm the app was open at the scheduled time — Cowork jobs only fire while the desktop app is running (a missed job runs on next launch).
