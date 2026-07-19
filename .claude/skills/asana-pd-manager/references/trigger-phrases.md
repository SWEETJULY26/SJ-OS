---
name: asana-pd-manager trigger phrases
description: Canonical phrases that route into asana-pd-manager. Grouped by intent so operators and sibling skills can browse to understand what fires this skill vs. a peer.
last_updated: 2026-05-17
---

# Trigger phrases — grouped by intent

The SKILL.md description holds the short canonical list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## Catch-up / status visibility (Job 1)

- "what's overdue"
- "catch me up on SJ SKIN"
- "what's stale"
- "what's at risk"
- "flag blockers"
- "where are we on [product]"
- "give me a PD status"

Also fires automatically when:
- `sjs-status-reporter` pulls PD portfolio state for a branded output
- Weekly portfolio status update

## Stage-gate moves (Job 2)

- "move [product] to In Review"
- "move the Fig lip treatment to Signed Approvals"
- "send [product] back for revisions"
- "reject [product]"
- "stage-gate move on [product]"

Also fires automatically when `fireflies-asana-bridge` or `outlook-asana-bridge` proposes a stage move based on meeting or email signal.

## IL Review Gate (Job 3)

Auto-fires inside Job 2 on every Signed Approvals move. Operator-facing phrases:

- "did the IL gate fire on [SKU]"
- "what's the IL status on [SKU]"
- "is [SKU] held on IL review"

## Task and subtask creation (Job 4)

- "create a task for Nicole"
- "add a subtask to [task] for [person]"
- "open a [follow-up / reformulation / spec review] task on [SKU]"
- "task: [name] — [assignee] — [project]"

## Updates and assignments (Job 5)

- "assign this to Danielle"
- "update the due date on [task]"
- "change the assignee on [task] to [person]"
- "rename [task] to [new name]"

## Status updates (Job 6)

- "draft a status update for [project]"
- "update the project status"
- "update the portfolio status"
- "post amber on [product] — we're waiting on [supplier]"
- "draft a weekly portfolio update"

## Comment and activity logging (Job 7)

- "add a comment to the lip treatment task"
- "log this on [SKU]"
- "leave a note on [task]"
- (Fires inbound from fireflies-asana-bridge and outlook-asana-bridge for meeting / email logging.)

## Stale / overdue surfacing (Job 8)

Same phrases as Job 1 catch-up; surfaces 7+-day stale items and overdue items in the catch-up output without an explicit ask.

## Implicit triggers (no Asana mention)

asana-pd-manager also fires when Alvin mentions a **formula, supplier, or product name + action word** without ever saying "Asana":

- "create a follow-up for KDC-One on Sorrel" → task creation
- "Mayra needs to weigh in on the Pava Cleanser sample" → task or comment
- "the Castaway Cream is at risk — we should reflect that" → status update

## Boundary phrases — these route to peer skills

| Phrase pattern | Routes to | Why |
|---|---|---|
| "log this from my call with [supplier]" | `fireflies-asana-bridge` | Meeting intake lives there; bridge proposes the write, asana-pd-manager confirms and executes |
| "log this email to [project]" | `outlook-asana-bridge` | Email intake lives there |
| "sync this approval to PLM" | `asana-plm-bridge` | Asana-to-PLM sync lives there; PLM writes commit via plm-assistant |
| "file the batch COA" / "log the PO ack" | `outlook-plm-bridge` | Email-to-PLM direct lives there |
| "generate a status report" / "build a deck" | `sjs-status-reporter` | Branded output generation lives there |
| "open a CAPA" / "log this complaint" | `complaint-and-event-handler` / `capa-coordinator` | Quality intake lives in System B |
| "stage the IL on [SKU]" / "log the new IL version" | `claims-il-and-label-keeper` | Regulatory IL execution lives there; asana-pd-manager only flips the gate field on Signed Approvals |
| "review this new claim" / "stage the [retailer] attestation" | `claims-il-and-label-keeper` | New-claim and retailer attestation lifecycle |
| "monthly quality summary" / "quality dashboard" | `quality-manager` | System B umbrella |
| "monthly regulatory summary" / "regulatory dashboard" | `regulatory-manager` | System C umbrella |
| "run a pressure-test on [SKU]" / "what archetype" | `sjs-margin-pressure-test` / `sjs-margin-archetype-advisory` | Margin work |
| "update PLM on [SKU]" | `plm-assistant` | PLM is the only writer |
| "rename [X] to [Y] across [project]" | `asana-find-replace` | Bulk find-and-replace utility |
| "what should I send to Sweet July this week" | `sjs-status-reporter` | Founder / brand-team output |

## Edge cases

| Pattern | Behavior |
|---|---|
| "skip confirmation on this one — it's obvious" | Decline. Every PD write goes through Rule 1 confirmation per `references/confirmation-protocol.md`. The audit trail is the point. |
| "just create the task — figure out the project later" | Decline. Rule 3: no standalone tasks. Ask which project and section. |
| "move [SKU] to Signed Approvals — but skip the IL gate this once" | Decline. Rule 7: IL Review Gate fires on every Signed Approvals move. No exceptions. |
| "assign to Erin — she has Asana, right?" | Verify via `asana_get_workspace_users` before assigning. Internal handle without an Asana-bound email per `references/role-map.md` is a flag. |
| "move [SKU] backward from Signed Approvals to In Review" | Rule 6: confirm intent explicitly. Unusual moves get a stronger preview. |
