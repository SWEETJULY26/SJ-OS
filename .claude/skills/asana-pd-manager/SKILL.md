---
name: asana-pd-manager
description: Manage Asana for AC Brands' Sweet July Skin product development work. Use whenever Alvin asks about PD tasks, projects, or portfolios — even casually. Triggers include "what's overdue", "catch me up on SJ SKIN", "add a comment to the lip treatment task", "move this to In Review", "update the project status", "create a task for Nicole", "what's stale", "flag blockers", "assign this to Danielle", "draft a status update", or any request involving SJ SKIN PD projects in Asana. Also fires when Alvin mentions a formula, supplier, or product name alongside an action word — even if "Asana" is never mentioned. Core engine of the 7-skill PD system routed via sjs-pd-system. Reads and writes every PD task, project, and portfolio; fires the IL Review Gate on every Signed Approvals stage move (SKN-OPS-008). Sibling PD skills (fireflies-asana-bridge, outlook-asana-bridge, asana-plm-bridge, outlook-plm-bridge, sjs-status-reporter) all feed into or read from this skill.
last_updated: 2026-05-17
---

# Asana PD Manager

The core engine of Sweet July Skin's PD system. Reads and writes every PD task, project, and portfolio in Asana. Owns the Formula Development Tracker stage-gate workflow and the IL Review Gate handoff to `claims-il-and-label-keeper`. Sibling PD skills (`fireflies-asana-bridge`, `outlook-asana-bridge`, `asana-plm-bridge`, `outlook-plm-bridge`, `sjs-status-reporter`) feed into or read from this skill via the contracts in `references/confirmation-protocol.md` and `references/cross-skill-handoffs.md`.

## Why this exists

The PD system needs one place where Asana state is read, written, and confirmed against a consistent set of rules. Meeting intake, email intake, PLM sync, and branded outputs all sit alongside this skill in the 7-skill PD system per `references/architecture/system_map.md`, but every Asana-side write lands here. Centralizing the write contract — confirmation, role-based assignment, stage-gate logic, IL Review Gate — keeps PD signal coherent across the four bridges and one reporter.

## Design principles

**Read AND write by design.** Unlike `quality-manager` and `regulatory-manager` (which are read-most umbrellas), this skill writes constantly. Every write goes through Rule 1 confirmation per `references/confirmation-protocol.md`.

**Confirmation before every write.** Rule 1 is the contract sibling skills consume. No exceptions, no batched silent commits.

**Project + section required on every task.** Rule 3. Standalone tasks are not acceptable.

**Asana = workflow truth. PLM = source of truth for product / batch / vendor data.** Sync to PLM happens via `asana-plm-bridge` or `outlook-plm-bridge`; this skill never writes PLM directly.

**Role-based assignment.** Look up user GIDs via `asana_get_workspace_users` against the role-holders in `references/role-map.md`. Never guess.

**Brand scope: Sweet July Skin only.** Other AC Brands projects out of scope at this build.

**Walks SKN-OPS-008 on the regulatory side.** The IL Review Gate procedure mirrors the ratified SOP. See `references/stage-gate-procedure.md`.

## The eight core jobs

### Job 1 — Catch-up rollup

Read across all SJ SKIN PD projects, filter to At Risk / stale (7+ days no update) / overdue. Return highlights-only format.

```
🔴 AT RISK / BLOCKED
• [Product name] — [Supplier] | Due: [date] | [Issue / blocker]

🟡 STALE (7+ days no update)
• [Product name] — [Supplier] | Last update: [X days ago] | Formula rev: [#]

⚠️ OVERDUE
• [Task name] — Assigned: [name] | Was due: [date]
```

If nothing is at risk, stale, or overdue, say so in one line. Don't pad.

- *Trigger:* phrases in `references/trigger-phrases.md` §catch-up
- *HITL:* none — read-only

### Job 2 — Stage-gate moves on Formula Tracker

Move tasks between the 5 stages (Intake / Concept → In Review → Signed Approvals → Revisions Required → Rejected) per `references/stage-gate-procedure.md`. Backward moves require explicit intent check (Rule 6).

- *Trigger:* phrases in `references/trigger-phrases.md` §stage-gate-moves; inbound from `fireflies-asana-bridge` or `outlook-asana-bridge`
- *HITL:* Operator confirms every move (Rule 1). Reversal moves get the stronger intent-check preview (Rule 6).

### Job 3 — IL Review Gate (auto-fires on Signed Approvals)

When a Formula Tracker task moves to Signed Approvals, atomically: flip `IL Status = Pending IL Review`, create inbound task in SJS Regulatory Management with prefix `[IL Review Pending — claims-il-and-label-keeper]`, set `Artifact Type = IL Review` and `Linked SKU`. PD launch flow holds until `IL Status = IL Approved` (written back by claims-il-and-label-keeper). See `references/stage-gate-procedure.md`.

- *Trigger:* every Signed Approvals move from Job 2 (Rule 7 — no exceptions)
- *HITL:* the Signed Approvals confirmation in Job 2 covers it; gate firing is part of the move's effect

### Job 4 — Task and subtask creation

Create tasks per the structure below. Always specify project + section (Rule 3). Ask for missing assignee / due date / section only when needed (Rule 2).

```
Task name: [Clear, descriptive name]
Project: [Project name] → [Section]
Assignee: [Name]
Due date: [Date]
Description: [Context]
Subtasks: [List if applicable]
```

- *Trigger:* phrases in `references/trigger-phrases.md` §task-creation; inbound from PD bridges
- *HITL:* Operator confirms via Rule 1 preview before creation. Subtasks confirm parent task before children.

### Job 5 — Updates and assignments

Update task name, notes, due date, assignee, completion status. Move tasks between sections (non-stage-gate moves). Assign by looking up user GID per `references/role-map.md`. Confirm all changes (Rule 1, Rule 5).

- *Trigger:* phrases in `references/trigger-phrases.md` §updates-assignments
- *HITL:* Operator confirms every change

### Job 6 — Project and portfolio status updates

Draft RAG color + written summary + next steps / blockers. Show draft, confirm, post.

Title convention for the Asana project status update itself: `[RAG emoji] [Color], [Month Day], [Year] Update` (e.g. `🟢 Green, May 28, 2026 Update`). Match this exactly — it's how the portfolio-wide status sweep parses color state without opening every project.

```
📊 Draft status update for: [Project name]
Color: 🟡 Amber
Summary: [Plain-language status]
Next steps: [Action + owner]
Blockers: [If any]

Post this?
```

- *Trigger:* phrases in `references/trigger-phrases.md` §status-updates
- *HITL:* Operator approves the draft before post

### Job 7 — Comment and activity logging

Add comments to tasks from `fireflies-asana-bridge` (meeting source), `outlook-asana-bridge` (email source with sender + subject + date attribution), `asana-plm-bridge` (PLM sync-back), `outlook-plm-bridge` (PLM sync-back).

- *Trigger:* phrases in `references/trigger-phrases.md` §commenting; inbound from PD bridges
- *HITL:* Operator confirms every comment

### Job 8 — Stale and overdue flagging (proactive)

Any time task or project data gets pulled (Job 1, Job 6, or sibling read), surface items with no Asana update in 7+ days. Read-only surfacing — actions taken on stale items follow their own job's HITL.

- *Trigger:* fires inside every read
- *HITL:* none — read-only surfacing

## How you connect

### Inbound writes from PD peers

| Sibling | What lands |
|---|---|
| `fireflies-asana-bridge` | Meeting action items as proposed tasks, comments, stage moves. Bridge follows `references/confirmation-protocol.md`. |
| `outlook-asana-bridge` | Email-sourced tasks, comments, stage moves with sender + subject attribution. Same protocol. |
| `asana-plm-bridge` | `📦 PLM Sync` comments on PD tasks after PLM writes land. |
| `outlook-plm-bridge` | `📦 PLM Sync` comments on PD tasks after PLM writes land. |

### Outbound handoffs

See `references/cross-skill-handoffs.md` for the full table. Headline wires:

- **Signed Approvals stage move** → `claims-il-and-label-keeper` (IL Review Gate), `purchasing-manager` (production PO), `asana-plm-bridge` (PLM phase update)
- **Signed product near launch window** → `supply-demand-planner` (forecast + buy plan)
- **Concept approval** → `sjs-margin-archetype-advisory` then `sjs-margin-pressure-test`
- **Pressure-test fail** → `sjs-margin-walk-away`
- **SKU heads to UBM listing** → `sjs-retail-intel`
- **Annual PD roadmap** → `regulatory-manager` (Pedrero capacity)

### Inbound reverse-handoffs (non-PD systems → PD)

- **Quality → PD:** `complaint-and-event-handler` (complaint trend → formulation review task), `capa-coordinator` (CAPA root cause = formulation → reformulation task), `batch-lifecycle-tracker` (first commercial batch → close production task), `adverse-event-and-recall-reporter` (recall trigger → recovery task).
- **Regulatory → PD:** `claims-il-and-label-keeper` (IL Approved / Returned sync-back), `regulatory-manager` (Pedrero capacity flag on portfolio status).
- **Intel → PD:** `sjs-comp-intel` (monthly trend digest with category shift → surface to PD Lead + Operator + Marketing via `sjs-status-reporter`).

### Workspace

- **Workspace:** AC Brands (`ac-brands.com`)
- **Asana MCP:** `https://mcp.asana.com/sse`
- **Operator email:** alvin@ac-brands.com

## When NOT to use this skill

- **Multi-system orchestration** — that's `sjs-pd-system` (PD router) or `sjs-master` (brand router).
- **PLM writes** — those route through `asana-plm-bridge` / `outlook-plm-bridge`, with `plm-assistant` as the only PLM writer.
- **Quality / Regulatory / Margin workflows** — System B, System C, and the Margin family own their own intake. PD only acts on the reverse-handoffs documented above.
- **Bulk find-and-replace** — that's `asana-find-replace`.
- **Branded output** (decks, reports, dashboards) — that's `sjs-status-reporter`.
- **Direct Pedrero contact** — never. `claims-il-and-label-keeper` and `regulatory-manager` own Pedrero.

## Reference index

- `references/confirmation-protocol.md` — Rules 1–7. The contract sibling skills consume.
- `references/role-map.md` — canonical PD-system role-map. Sibling PD skills reference this.
- `references/pd-projects.md` — the 13 SKU projects + Formula Tracker + portfolio.
- `references/suppliers.md` — PD-side supplier routing (formula vs. component).
- External partner / contact recognition — read live from Supabase wiki, not from a file. `public.wiki_pages WHERE page_type='contact'` (people) and `WHERE page_type='partner'` (service contractors, labs, 3PLs, tooling) carry the recognition layer. The four bridges load them at run time. (Retired `references/external-contacts.md` on 2026-05-26 — see `Bridge-and-System-Audit-2026-05-26.md` Priority 1.)
- `references/stage-gate-procedure.md` — 5-stage Formula Tracker + IL Review Gate (SKN-OPS-008).
- `references/cross-skill-handoffs.md` — every PD ↔ non-PD wire.
- `references/trigger-phrases.md` — what fires this skill vs. a peer, with boundary phrases.
- `references/gids-pointer.md` — pointer to the canonical Asana field GID cache.

## Example interactions

**Catch-up:**
> "What's at risk in PD right now?"
→ Pull tasks across all SJ SKIN projects, filter for At Risk / stale / overdue, return Job 1 highlights format.

**Stage move + IL Review Gate:**
> "Move the Fig lip treatment to Signed Approvals"
→ Rule 1 preview includes the IL Review Gate side-effects. On confirm: stage move + IL Status flip + inbound regulatory task in one atomic action.

**Task creation:**
> "Create a task for Nicole to follow up with KDC-One on the Sorrel formula revision"
→ Ask which project / section (Rule 3). Preview full task (Rule 1) before creating.

**Status update:**
> "Update the Pineapple Punch project to amber — we're waiting on IKS"
→ Draft RAG + summary + next steps (Job 6). Post on confirmation.

**Assignment:**
> "Assign the Castaway Cleansing Oil compatibility testing task to Perrine"
→ Resolve Perrine's user GID via `asana_get_workspace_users`. Rule 1 preview. Execute on confirm.

**Reverse-handoff from Quality:**
> (capa-coordinator stages a CAPA with root cause = formulation on Sorrel)
→ asana-pd-manager opens a reformulation task on the Sorrel SKU project, cross-flagged to PD Lead (Perrine) per `references/cross-skill-handoffs.md`.

## History

- **2026-05-17** — Modernized to umbrella pattern. Extracted inline catalogs (team roster, product list, supplier map, external partners, stage-gate procedure, confirmation rules, trigger phrases) to `references/`. Updated system-position from "Skill 1 of 4-skill circular system" to "core engine of the 7-skill PD system" per `references/architecture/system_map.md`. Marked SKN-OPS-008 as ratified (was "pending ratification" — `quality-manager/references/sop-catalog.md` showed ratified 2026-05-09). Added Design principles, Core jobs (numbered), When NOT to use, Reference index. Documented cross-system handoffs to Quality, Regulatory, Margin, Ops, Retail Intel, and inbound reverse-handoffs.
- **2026-05-09** — Original monolithic v1 (14KB SKILL.md, no references/).
