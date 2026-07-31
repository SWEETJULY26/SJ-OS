# Routine registration — what needs doing in the UI

**Use:** The working list for getting the recurring jobs correctly registered as Claude Code Routines. Companion to `references/architecture/automations.md`, which is the canonical map; this file is the punch list.

**Why it exists:** On 2026-07-31 a live check found six of seven daily jobs not running, and every spec in this directory pointing at a repo path that does not resolve. Both are fixable but not from inside a Claude Code session — the API refuses on both counts, documented below.

---

## What an agent cannot do, and why

Three hard limits, each hit and verified on 2026-07-31. They are the reason this file is a punch list rather than a completed change.

**An agent cannot re-enable a Routine it did not create.** `update_trigger` returns: *"this routine was created via `http_api`, not by an agent. Agents can only update routines they created. A routine's own session may still disable itself (`enabled=false` only)."* Every existing Routine was created in the claude.ai Routines UI, so all of them are read-only from here. An agent can turn itself off and nothing else.

**An agent cannot attach connectors.** A Routine created with `create_trigger` from a session gets no MCP connectors, because a session can only pass through grants it holds and a remote session holds none. The resulting Routine fires into a session with no Outlook, no PLM and no Asana — useless for any sweep. Every working Routine carries 7–9 connectors: `Microsoft_365`, `Supabase`, `Asana`, `Asana-c313a468`, `Netlify`, `Fireflies`, `Vercel`, `Canva`, `Excalidraw`.

**An agent cannot set completion notifications on an existing Routine.** `update_trigger` has no `notifications` parameter at all. `create_trigger` does — `{push: true, email: true}` — but only for Routines with `create_new_session_on_fire: true`, and creating one from a session reintroduces the connector problem. So notifications are UI-only for anything that already exists.

**Net:** create and edit recurring ops Routines in the Routines UI. Use `list_triggers` from a session to audit; do not use `create_trigger` to build them.

---

## Punch list

### 1. Re-enable three paused morning sweeps

Approved by Alvin 2026-07-31. All three keep their connectors, so this is a toggle — nothing needs recreating.

| Routine | Trigger ID | Cron (UTC) | Last fired |
|---|---|---|---|
| `sjs-purchasing-morning-sweep` | `trig_01Y9ewzNuvZn24EzjzyjKyqC` | `26 15 * * 1-5` | 2026-07-17 |
| `sjs-quality-morning-sweep` | `trig_01AVRFDRc7aHu8L7gv3etEza` | `20 15 * * 1-5` | 2026-07-17 |
| `sjs-regulatory-morning-sweep` | `trig_01DY3iScZ6Ai3yV2FbbRbEMW` | `10 15 * * 1-5` | 2026-07-20 |

**Expect a backlog on the first run.** These have been dark for two weeks, and each sweep's window is "since the last run." The first firing may surface a fortnight of signal at once rather than a normal day's worth. Fire the first run manually from the Routines UI so the catch-up lands while you are watching rather than at 8:10 on a Monday.

**Correction, 2026-07-31:** an earlier note here claimed `fire_trigger` works on any Routine regardless of creator. It does not — it carries the same restriction as `update_trigger` and refuses anything created via `http_api`. Manual firing is UI-only too. Assume **nothing** about an existing Routine can be driven from a session except reading it via `list_triggers`.

### 2. Register three PD dailies that were never created

Documented in `automations.md` since before the Routines migration, present as specs in this directory, absent from Routines entirely. The PD recap running log (Asana task `1214208955674591`) has therefore had no automated writer.

| Routine to create | Cron (UTC) | Cron (PT) | Prompt spec |
|---|---|---|---|
| `sjs-pd-morning-sweep` | `0 15 * * 1-5` | 8:00 AM | `scheduled-prompts/sjs-pd-morning-sweep.md` |
| `sjs-pd-midday-sweep` | `0 19 * * 1-5` | 12:00 PM | `scheduled-prompts/sjs-pd-midday-sweep.md` |
| `sjs-pd-eod-reconciliation` | `0 23 * * 1-5` | 4:00 PM | `scheduled-prompts/sjs-pd-eod-reconciliation.md` |

Paste each spec file as the Routine's prompt. Settings to match the working jobs: fresh session per fire, all connectors attached, and completion notifications on per Alvin's 2026-07-31 ask.

### 3. Register the Logiwa receipt sweep

| Routine to create | Cron (UTC) | Cron (PT) | Prompt |
|---|---|---|---|
| `sjs-receipt-report-sweep` | `32 15 * * 1-5` | 8:32 AM | On placeholder `trig_01DnJ5tmwNVTvod7LXetHa1i` |

A disabled placeholder exists carrying the full prompt — copy it out, create the real Routine in the UI, then delete the placeholder. It is disabled on purpose: created from a session, so no connectors, so it would fail every weekday run.

Spec it implements: `.claude/skills/inventory-manager/references/logiwa-receipt-report.md`.

### 4. Notifications on every recurring job

Alvin asked on 2026-07-31 for completion notifications when these finish. Set `push` and `email` per Routine in the UI. Only works on fresh-session-per-fire Routines; a Routine bound to a persistent session cannot carry them.

### 5. Leave `ac-brands-holiday-comms-2026` alone for now

`trig_01W9T3k8qRo7ru3JZMQwtgBN`, paused, last fired 2026-07-13. **It auto-sends email to the whole team on BCC.** Check the send calendar in `ac-brands-holiday-comms` against today's date before re-enabling — a two-week-dark reminder system may fire a notice whose date has already passed, or skip one it owed.

---

## Fixed in the repo on 2026-07-31

**The repo path in all 23 specs.** Every one said the skills repo was cloned at `/home/user/sj-os`. The actual path is `/home/user/SJ-OS`, and on a case-sensitive filesystem the lowercase form does not resolve — so a fired Routine could not read any of the skill files it was instructed to follow. Corrected in all 23, with a fallback instruction added to each so a future path change degrades into "find the repo" rather than silently proceeding without instructions.

This is worth weighing when judging whether the eleven currently-running Routines have been doing their jobs. They fired, but they could not read their own instructions.
