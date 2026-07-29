---
name: PD confirmation protocol
description: The canonical confirmation rules for every write asana-pd-manager makes. Sibling PD skills (fireflies-asana-bridge, outlook-asana-bridge, asana-plm-bridge, outlook-plm-bridge) reference this file by path instead of restating the rules.
last_updated: 2026-07-29
---

# Confirmation protocol

Every Asana write that lands through the PD system follows these rules. asana-pd-manager owns the rules; sibling PD skills route their writes through them.

## Rule 1 — Always confirm before writing

Before executing ANY create, update, move, assign, comment, or edit action, show Alvin a confirmation preview. Use this format:

```
📋 Confirm before I proceed:
• Action: [what you're about to do]
• Target: [task / project name]
• Details: [key fields being set or changed]

Proceed?
```

Only execute after Alvin confirms (e.g., "yes", "do it", "go ahead").

Confirmation can be batched if Alvin says "do them all" — but each item in the batch still gets a one-line preview in the confirmation block.

## Rule 2 — Every required field carries a value

Superseded 2026-07-29 by the field discipline in `references/architecture/asana_task_contract.md` Phase 1. The old rule ("ask for assignee, due date, or section only when missing") let tasks land with blank fields whenever the source didn't happen to mention them, and let tasks land with no due date at all.

Now: derive every required field. Assignee, section, and collaborators come from the role-map and the queue's routing rules; the due date comes from the Phase 2 ladder and is never omitted. A field that genuinely can't be determined is written `TBD — <what's missing and who would know>` and raised in the preview's open-questions block — not left blank, and not a reason to stall the write.

Never create a task without a project AND section. See Rule 3.

## Rule 3 — Always add tasks to a specific project and section

Standalone tasks (no project) are not acceptable. If Alvin does not specify, ask:

> "Which project and section should this go in?"

If a sibling skill (`fireflies-asana-bridge`, `outlook-asana-bridge`) proposes a task without a project, the bridge surfaces the question — it does not get answered by guessing.

## Rule 4 — Flag stale items proactively

Any time you pull task or project data, flag items with no Asana update in 7+ days. Surface these in the catch-up output. This is read-side hygiene, not a write — no confirmation needed to surface, but every action taken on a stale item still goes through Rule 1.

## Rule 5 — Role-based assignment

When assigning a task, look up the assignee via `asana_get_workspace_users` and confirm the role they hold per `references/role-map.md`. Never guess a user GID. When Alvin refers to a person by first name only, the assignment confirmation preview shows the resolved full name.

## Rule 6 — Stage-gate moves require intent check on reversals

Moving a Formula Tracker task **backward** through the 5-stage workflow (e.g., Signed Approvals → In Review) is flagged as unusual. The confirmation preview asks Alvin to confirm intent explicitly before the move. Forward moves use the standard Rule 1 preview. See `references/stage-gate-procedure.md` for the full procedure.

## Rule 7 — IL Review Gate fires on Signed Approvals every time

When a Formula Tracker task moves to Signed Approvals, the IL Review Gate fires automatically (flip `IL Status` to `Pending IL Review`, create the inbound task in SJS Regulatory Management). The move itself follows Rule 1; the gate is part of the move's effect, not a separate confirmation. See `references/stage-gate-procedure.md`.

## Rule 8 — Walk the task write contract before every Asana write

`references/architecture/asana_task_contract.md` governs the shape of every Asana write in the system — the four bridges and every destination skill, not only PD. Walk its five phases before the Rule 1 preview goes up:

1. **Resolve** against existing tasks by dedupe key. Never create what already exists — update it.
2. **Fields** — every required field valued or explicitly `TBD` (Rule 2 above).
3. **Due date** — always set, derived by the ladder, derivation shown.
4. **Collaborators** — derived from the role-map, not from whatever the source mentioned.
5. **Move / multi-home** — one task in two projects when it's the same work item; a second task only when each system owes a distinct deliverable.

The Rule 1 preview carries the results: a `🔁 Resolve` verdict, the `Due` derivation, `Collaborators`, `Homes`, and any open questions. A preview with no Resolve verdict means Phase 0 didn't run — treat it as an incomplete write and go back.

## How siblings consume this

| Sibling skill | Where it applies |
|---|---|
| `fireflies-asana-bridge` | Every `pd`-labeled write proposed from a meeting transcript |
| `outlook-asana-bridge` | Every `pd`-labeled write proposed from an email |
| `asana-plm-bridge` | Asana-side comments posted as PLM sync-back (Rule 1 applies). PLM writes themselves go through `plm-assistant` and follow its confirmation rules, not these. |
| `outlook-plm-bridge` | Same as `asana-plm-bridge` for Asana sync-back comments. |

## Update protocol

When a rule changes here, every sibling skill that references this file should be re-read in the same conversation to confirm no inline restating of the old rule has drifted. The whole point of externalizing this is that the rules live in one place.
