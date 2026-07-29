# Asana task write contract

**Use:** The rules every skill walks before it writes a task to Asana. Resolve against what already exists, fill every required field, always set a due date, always set collaborators, and move or multi-home an existing task instead of opening a second one.

**Scope:** All four bridges (`outlook-asana-bridge`, `fireflies-asana-bridge`, `asana-plm-bridge`, `outlook-plm-bridge`) and every destination skill that creates or updates Asana tasks. Single source of truth — consuming skills point here rather than restating the rules.

**Companion contracts:** `bridge_queue_contract.md` decides *which queue* a task belongs to. This file decides *what the write looks like once the queue is known*. HITL confirmation itself lives in `asana-pd-manager/references/confirmation-protocol.md` (Rule 1); this contract adds the field discipline that confirmation preview displays.

**Last updated:** 2026-07-29 — Authored to close four gaps Alvin flagged: bridges created tasks without checking for an existing one, left fields blank when the source didn't mention them, shipped tasks with no due date, and split same-work items into separate cross-referenced tasks in each queue instead of multi-homing one.

---

## Tool baseline

Use the `mcp__Asana__*` server for every call in this contract. The alternate `mcp__Asana-c313a468__*` server's `asana_update_task` has no `add_projects` parameter, so it cannot move sections or multi-home — a write routed there silently loses Phase 4.

Verified working against the AC Brands workspace on 2026-07-29:

| Need | Call | Notes |
|---|---|---|
| Phase 0 search | `search_tasks` with `projects_any`, `text`, `completed` | Premium search is enabled on this workspace. |
| Current section + existing homes | `search_tasks` / `get_task` with `opt_fields=memberships.project.name,memberships.section.name` | See the empty-memberships gotcha below. |
| Field + option GIDs | `get_project` with `opt_fields=custom_field_settings.custom_field.name,custom_field_settings.custom_field.gid,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_options.gid` | Returns every field and every enum option GID in one call. |
| Section GIDs | `get_project` with `include_sections: true` | Cheaper than a separate sections call when you need fields anyway. |
| User GIDs | `get_users` with `opt_fields=gid,name,email` | Returns name + email; match role-map holders on email, not display name. |
| Create | `create_tasks` | Takes `project_id`, `section_id`, `assignee`, `due_on`, `followers`, `custom_fields` in one call. One project only at create time. |
| Update, move, multi-home | `update_tasks` | `add_projects: [{project_id, section_id}]`, `add_followers`, `due_on`, `custom_fields`. |

**Empty-memberships gotcha.** `search_tasks` sometimes returns `memberships: []` for a task that genuinely sits in the searched project. Never read that as "not in a project" or "no section" — re-read the task with `get_task` before deciding placement. Acting on the empty array is how a resolve step wrongly concludes a task needs creating or re-homing.

---

## Phase 0 — Resolve before create

No skill creates a task before searching for one that already covers the work. This is the gap that produced duplicate tasks whenever a supplier emailed three times about one thing, or a meeting re-raised what an email had already opened.

### Dedupe key

Every task type declares a **dedupe key**: the smallest set of identifiers that make two mentions the same work item. Keys already in use across the system, which this contract generalizes rather than replaces:

| Work type | Dedupe key | Owning skill |
|---|---|---|
| DTC order hold | `Order #` | `oc3pl-order-manager` |
| Stock position | `SKU + location` | `inventory-manager` |
| Near-expiry | `batch code + threshold` | `inventory-manager` → `batch-lifecycle-tracker` |
| PO receipt | `PO number + vendor` | `purchasing-manager` |
| Vendor renewal | `vendor + renewal window` | `purchasing-manager` |
| Vendor invoice | `vendor + invoice number` | `purchasing-manager` (matches the PLM unique constraint) |
| Lab finding | `batch code + test type` | `quality-lab-coordinator` |
| CAPA / NCR | `NCR number`, or `source event + SKU` before one is assigned | `capa-coordinator` |
| Complaint | `complaint ID`, or `customer + SKU + date` before one is assigned | `complaint-and-event-handler` |
| IL / claims artifact | `SKU + artifact type` | `claims-il-and-label-keeper` |
| Reportable event | `SAE ID` or `recall ID` | `adverse-event-and-recall-reporter` |
| PD work item | `SKU + work item` | `asana-pd-manager` |
| Waiting-on | `counterparty + ask` | `outlook-asana-bridge` |

A new task type declares its key here before it ships.

### Wiki pre-check

The bridges' Job 0 narrative writes already record task GIDs inline on `supplier/<slug>` and `sku/<slug>` wiki pages — `(Asana: 100342 — KDC-One Port Jervis, gid 1215063252723231.)` and similar. Skills that read the wiki page before drafting (`purchasing-manager`'s wiki-read-first rule, and every bridge's Job 0 entity loop) are therefore already holding a list of tasks previously opened against that supplier or SKU, at no extra cost.

Check it first:

```sql
SELECT slug, content FROM public.wiki_lookup(p_slug => 'supplier/kdc-one');
-- then scan content for `gid <digits>` alongside the work being logged
```

A hit is a **candidate**, not a verdict — the prose is written by a narrative layer, not a structured index, so confirm with `get_task` before treating it as a match. A miss proves nothing and the Asana search below still runs. Treat this as a cheap accelerator on work the system has touched before, not as the dedupe mechanism.

### The search

Two passes, both scoped to the candidate queue GIDs from `bridge_queue_contract.md`:

```
search_tasks(projects_any: <queue GIDs>, text: <key terms>, completed: false,
             opt_fields: "name,due_on,assignee,followers,completed,modified_at,
                          memberships.project.name,memberships.section.name")

search_tasks(projects_any: <queue GIDs>, text: <key terms>, completed: true,
             completed_on_after: <today - 30d>, opt_fields: <same>)
```

`text` searches names, descriptions, and comments, so the dedupe key written into the description (Phase 1) is itself searchable — that is why the key goes in the body, not just the title. Search on the key's identifiers, not the full task name; a re-worded title must still match.

When a task type spans queues, search every candidate queue. A failing lab result on a SKU with open PD work has to be searched in Quality *and* the SKU project, or Phase 4 can't tell "multi-home the existing task" from "create a new one."

### Three verdicts

Every write states which one fired, in the confirmation preview:

```
🔁 Resolve: NEW — no open task matches `PO-4471 · KDC-One`
🔁 Resolve: UPDATE task 1214048212856468 "Receipt — PO 4471 — KDC-One" (last touched 6d ago)
🔁 Resolve: REOPEN? task 1214048212856468 closed 2026-07-19 — reopen, or open a fresh occurrence?
```

**NEW** — create, walking Phases 1–3.

**UPDATE** — not "skip." Post the new signal as a comment with source attribution, refresh any field whose value changed, re-run the Phase 2 ladder in case the deadline moved, move the section if state advanced (Phase 4), and multi-home if a second system now owns part of the work. An UPDATE verdict that produces only a comment when the source carried a new date or a new state is an incomplete write.

**REOPEN?** — always asks. A recurrence of something closed last week is sometimes the same work resurfacing and sometimes a genuinely new occurrence, and the two want different histories. Never decide this silently.

### Ambiguity

More than one open task matching the key means the queue already holds duplicates. Surface all matches and ask which to update rather than picking the newest — and say plainly that the duplicates exist, since that's a cleanup signal.

---

## Phase 1 — Required fields, no silent blanks

This replaces the old "prompt for missing details only when needed" behavior. A field is never simply absent.

### Universal required set

Every task, every queue:

- **Name** — the queue's prefix convention, then the dedupe key's identifiers in a stable order.
- **Project** and **Section** — never a standalone task, never an unplaced one.
- **Assignee** — one owner. Multi-homed tasks still have exactly one.
- **`due_on`** — always. Derived per Phase 2.
- **Followers** — derived per Phase 3.
- **Description** — the queue's own template, plus the three required blocks below.

Three blocks every description carries:

```
SOURCE
- Email from Mayra Reyes (Vegelabs), 2026-07-27 — "Pava Toner — VL13-41-4 stability"
  (or: Meeting "SJ Ops Standup", 2026-07-20 | Asana task 1214… | Ramp invoice INV-8891)

KEY
- Dedupe key: PO-4471 · KDC-One

LINKS
- Cross-system homes: SJS Quality Management → Lab Findings Open
- Related: task 1214… (parent PD work), PLM batch 18GS830107
```

The KEY block is what makes the next run's Phase 0 search find this task. Omitting it breaks dedupe for every future mention.

### Queue custom fields

Resolve field and option GIDs live per session via `get_project` — do not hard-code them.

There is no GID store to read them from. Checked 2026-07-29: the PLM database has no Asana GID column on any of its 57 tables, and the wiki layer holds no structured GIDs either — only task GIDs written incidentally into page prose by Job 0 (see the wiki pre-check above). Project-level GIDs live in `gids.md`. Field, option, and section GIDs live only in the canonical cache named by `asana-pd-manager/references/gids-pointer.md`, which sits outside this repo on Alvin's Mac. Live resolution is therefore the only reliable route for field-level IDs. Append newly resolved GIDs to `gids.md` per its own discipline note.

Enum fields take **option GIDs**, not display names. A name string is rejected.

If `update_tasks` returns `"Custom field with ID X is not on given object"`, the field isn't attached to that project. Say so and name the field — don't drop it silently and don't retry.

### The TBD rule

A required field that genuinely can't be determined from the source is written as:

```
TBD — <what's missing and who would know>
```

The task still gets created. Every TBD is then listed in the preview under an open-questions block:

```
❓ Open questions
- Assignee: TBD — no owner named in the email; Ops or PD?
- Linked SKU: TBD — email says "the toner", could be Pava Toner Spray or Pava Cleanser
```

A blank field is a silent failure that surfaces weeks later. A `TBD` with a stated reason is a visible one, and it survives in the task body so whoever opens the task next can see what was unknown at intake.

Text fields carry the `TBD — …` string. Enum fields have no such option, so leave them unset and raise the gap in the open-questions block. Never invent an option GID to avoid a blank.

---

## Phase 2 — Due date ladder

Walk in order, stop at the first hit. Every task ends up with a `due_on`.

**1. Explicit date in the source.** "Ship by August 12", "due 8/12".

**2. Deadline language,** resolved against the source's own date — not today's. "By Friday" in an email from July 20 means July 24, even when the bridge reads it on July 29. Getting this wrong silently backdates tasks on any catch-up run covering more than a day.

**3. Statutory or gate clock.** SAE filing windows, FDA recall report deadlines, contract renewal dates, batch expiry thresholds, retailer attestation due dates. These **override** the SLA default and never fall back to it — a regulatory clock is the real deadline, not a service target. The owning skill's SOP defines the window.

**4. SLA default,** by urgency and primary label:

| Case | Default |
|---|---|
| Flagged urgent by the source skill's urgency signals | 1 business day |
| `quality` | 3 business days |
| `regulatory` | 3 business days |
| `ops` | 5 business days |
| `pd` | 5 business days |
| Waiting-on / check-back | 5 business days |
| FYI, log-only, running-log entry | 10 business days |

Business-day math skips weekends and AC Brands office closures — the holiday calendar is Asana project `1214055559810920`, maintained by `ac-brands-holiday-comms`. A due date landing on a closure moves to the next open business day.

Always show the derivation, so a wrong default costs one word to fix:

```
Due: 2026-08-05 (SLA default — ops, 5bd)
Due: 2026-07-24 (stated: "by Friday", from 2026-07-20 email)
Due: 2026-08-11 (statutory — SAE 15-day window from 2026-07-27)
```

On an UPDATE verdict, re-run the ladder. A supplier who moves a date in a follow-up email should move the task's date; leaving the old one is the same failure as never setting it.

---

## Phase 3 — Collaborators

Followers are derived, not left to whatever the source happened to mention.

Every task gets:

- The **assignee**.
- **Alvin** (Operator) — always. `alvin@ac-brands.com`, GID `1200866724349684`.
- The **role-holder who owns the gate** for that queue, per `asana-pd-manager/references/role-map.md` for PD and the Quality / Regulatory role-maps for those queues.
- The **counterpart owner for every secondary home** on a multi-homed task, so each system sees its side.
- Any **internal person named in the source** as owning or awaiting part of the work.

Resolve every follower to a GID via `get_users`, matching on **email**, not display name — display names in this workspace are inconsistent ("Alvin", "Danielle Iturbe", "ash@teknologicsllc.com"). Never guess a GID (Rule 5).

**External contacts are never followers.** Pedrero, vendors, labs, and 3PL contacts are not workspace users; adding them fails or, worse, matches some unrelated guest account. They belong in the description's SOURCE block. This is the obvious way to misread "appropriate collaborators," so it's stated rather than assumed.

**A role-holder who doesn't resolve is surfaced, not dropped.** `role-map.md` currently lists an Operations Coordinator (Ciarra Robinson) with no matching workspace user as of 2026-07-29. When a mapped role-holder has no account, add the rest of the followers, name the unresolved one in the open-questions block, and let Alvin decide — silently shipping a task with a missing watcher is how gates get skipped.

---

## Phase 4 — Update, move, multi-home

### Section move

State advancing means the task moves. Same call as multi-homing, pointed at the project the task already sits in:

```
update_tasks(tasks: [{task: <gid>,
                      add_projects: [{project_id: <the project it is already in>,
                                      section_id: <the new section>}]}])
```

Each queue keeps a state → section map, resolved live from `get_project(include_sections: true)`. Section names drift; GIDs are cached per session, never hard-coded into a skill body.

### Multi-home

Same work item owned by two systems means **one task in two projects**, not two tasks pointing at each other:

```
update_tasks(tasks: [{task: <gid>,
                      add_projects: [{project_id: <secondary queue>,
                                      section_id: <its intake section>}],
                      add_followers: [<counterpart owner GID>]}])
```

One task, one assignee, one due date. Each system closes its own side of the work; the last one to finish completes the task. This generalizes the rule `inventory-manager` already runs (SKILL.md — near-expiry tasks multi-homed into SJS Quality Management, Purchasing multi-homes for reorder review) and the routing matrix in `purchasing-manager` Job 9.

Multi-homing is live and working in this workspace today — task `1214048212856468` sits in both the Lychee Lip Treatment SKU project (Phase 5 section) and AC Brands Purchasing (Receiving). Any skill note claiming the MCP can't multi-home is stale.

### Multi-home or separate tasks

Multi-home when it is **the same work item** — one deliverable, one owner, visible to two systems. A receipt that Purchasing and PD both track. A near-expiry batch that Inventory and Quality both act on.

Create **separate cross-referenced tasks** when each system owes a **distinct deliverable** with its own owner and its own close. A failing lab result where Quality owes an investigation and PD owes a reformulation decision is two tasks — different work, different owners, different completion criteria — and they cross-reference through the LINKS block.

The test: could one person close it once? Same work, multi-home. Two closes needed, two tasks.

### Never

Don't create a second task to represent a state change. Don't create a second task because the section is wrong. Don't create a second task because a secondary system needs visibility. Each of those is an `update_tasks` call on the task that already exists.

---

## Confirmation preview

Extends the Rule 1 preview in `confirmation-protocol.md` rather than replacing it. Full shape for a single write:

```
📋 Confirm before I proceed:
🔁 Resolve: NEW — no open task matches `VL13-41-4 · stability`
• Action: Create task
• Target: SJS Quality Management → Lab Findings Open
• Name: [Lab Finding] Pava Toner Spray — VL13-41-4 — stability OOT
• Assignee: Perrine Calvet (PD Lead / QA Lead)
• Due: 2026-08-03 (SLA default — quality, 3bd)
• Collaborators: Alvin (Operator), Perrine Calvet (QA Lead gate)
• Fields: Status=Triage · Classification=OOT · Severity=Major · Linked Batch=VL13-41-4 · Linked SKU=Pava Toner Spray
• Homes: SJS Quality Management → Lab Findings Open (primary)
         SJ SKIN – New Pava Toner Spray → Testing (secondary, same work item)

❓ Open questions
- Severity: set Major from "significant drift" — confirm or downgrade?

Proceed?
```

On a batch confirmation ("do them all"), each item keeps its one-line preview and its own Resolve verdict. A batch that reports no verdicts hasn't run Phase 0.

For skills whose report format is deliberately terse — `fireflies-asana-bridge` after its 2026-07-21 cost rescope — the Resolve verdict rides on the existing item line rather than adding one:

```
• Pava Toner stability OOT — Perrine — due 8/3 — 🔁 UPDATE 1214… (SJ Ops Standup, 7/20)
```

---

## What this contract does not cover

- **Which queue a task belongs to** — `bridge_queue_contract.md`.
- **Whether to write at all** — the HITL confirmation rules in `confirmation-protocol.md`, and each Quality / Regulatory skill's own gate rules.
- **PLM writes** — `plm-assistant` is the sole PLM writer and follows its own confirmation rules. The PLM bridges apply this contract to their Asana-side writes only.
- **Task description templates per queue** — those live with their owning skill (`inventory-manager/references/task-description-templates.md`, `purchasing-manager/references/task-description-templates.md`). This contract sets the three blocks every template must carry, not the rest of the body.
- **Attachments** — the Asana API can't take file uploads from Claude. Flag them for manual attachment as each bridge already documents.
