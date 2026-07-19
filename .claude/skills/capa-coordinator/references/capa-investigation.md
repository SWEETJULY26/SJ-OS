# CAPA Investigation + Action Plan Template

Mirrors SKN-OPS-001 Appendix B. Use this structure when drafting the CAPA file content for §5.3 (Action Plan), §5.4 (Implementation tracking), and §5.5 (Verification + Effectiveness).

The skill drafts; the team fills in. Every CAPA's content lives on the Asana task — this template is what gets posted as the structured comment / description.

---

## CAPA cover block

```
**CAPA Number:** CAPA-YYYY-NNN
**Linked NCR:** NCR-YYYY-NNN
**Date opened:** YYYY-MM-DD
**Severity:** Critical | Major | Minor
**Source:** [from NCR Procedure §3.2 source list]
**Category:** Product | Process | Vendor | Regulatory | Lab | Fulfillment

**Linked records:**
- Batch: [PLM batch ID + link]
- Vendor: [name + purchasing-manager record link]
- SKU: [SKU code + name]
- Source task: [Asana gid + title]

**Investigation team:**
- [Role] — [Person] (Lead)
- [Role] — [Person]
- [Role] — [Person]

**Statement of non-conformance:** [one or two sentences — what happened, when, to what]
```

---

## Root Cause Analysis section

Output of the RCA work captured per `references/rca-tools.md`. Posted as its own comment thread on the CAPA task. The root cause statement gets pulled into the cover block + the `Root Cause Statement` custom field.

```
**Root cause statement:** [one sentence, attributable to a process/system/design choice]
**Root cause category** (if Fishbone used): [Manpower | Method | Machine | Material | Measurement | Environment]
**Tool(s) used:** [5 Whys | Fishbone | Other — describe]
**RCA artifact:** [link to the comment thread holding the verbatim walk]
```

---

## Corrective Action Plan (§5.3)

Addresses the immediate non-conformance. Each action stands alone — owner, timeline, evidence requirement, completion check.

```
**Corrective Actions**

| # | Action | Owner | Due | Evidence required on completion | Status |
|---|---|---|---|---|---|
| C1 | [specific action] | [role + name] | YYYY-MM-DD | [what evidence — signed doc, photo, retest result, etc.] | Open / In progress / Complete |
| C2 | ... | ... | ... | ... | ... |
```

Actions should be:
- **Specific** — "update incoming inspection SOP to require moisture verification for botanicals" not "improve incoming inspection"
- **Owned** — a single person at a single role, not "Quality team"
- **Date-bounded** — actual date, not "ASAP" or "next sprint"
- **Verifiable** — the evidence requirement makes verification possible later

---

## Preventive Action Plan (§5.3)

Addresses the underlying cause to prevent recurrence. Same structure. Crucially: each preventive action gets tagged for whether it changes a SOP, a process, or a habit.

```
**Preventive Actions**

| # | Action | Owner | Due | Evidence required | SOP impact | Status |
|---|---|---|---|---|---|---|
| P1 | [specific action] | [role + name] | YYYY-MM-DD | [evidence] | None / SOP-NNN revision / New SOP | Open / In progress / Complete |
| P2 | ... | ... | ... | ... | ... | ... |
```

For any P-action with `SOP-NNN revision` or `New SOP` in the SOP impact column, the skill auto-stages a `[SOP Revision Pending — quality-manager]` task with the proposed change carried forward. That's the bridge from CAPA into the SOP library.

---

## Implementation Tracking (§5.4)

Read-only surface. As action owners post completion, the skill updates status fields and surfaces overdue items. No template per se — this is just the act of keeping the table current.

Skill behavior on overdue:
- Action 1 day overdue: comment ping the owner.
- Action 5 days overdue: comment ping the owner + Operator.
- Action 10 days overdue: surface to QA Lead via `[Pending QA Lead — Overdue Action]` prefix on the CAPA task.

---

## Verification Record (§5.5)

Once all actions report complete, draft the verification record. QA Lead approves.

```
**Verification — CAPA-YYYY-NNN — [Date]**

For each action:
- C1: [completion date] — [verifier role + name] — [evidence link] — Verified ✓ / Not verified [reason]
- C2: ...
- P1: ...
- P2: ...

**All actions completed as planned:** Yes / No
**If No, reopen at:** [phase to return to per SKN-OPS-001 §5.5]

**Verifier:** [QA Lead role + name]
**Date:** YYYY-MM-DD
```

Verification answers "did the actions happen." Effectiveness is separate.

---

## Effectiveness Review (§5.5)

Answers "did the change hold." Tied back to the original root cause statement.

Effectiveness window by severity:
- **Critical** — 90 days from last action completion
- **Major** — 60 days
- **Minor** — 30 days

The skill schedules the review at action completion + window. Pulls leading indicators via plm-assistant or related skills.

```
**Effectiveness Review — CAPA-YYYY-NNN — [Date]**

**Original root cause statement:** [pulled from cover block]

**Effectiveness window:** [Critical 90 / Major 60 / Minor 30] days
**Review date:** YYYY-MM-DD (window end)

**Leading indicators reviewed:**
- [Indicator 1 — e.g., "next 3 batches of [SKU] passed incoming inspection on [spec]"] — [evidence]
- [Indicator 2 — e.g., "no recurrence of [non-conformance type] in [time period]"] — [evidence]
- [Indicator 3 — e.g., "audit follow-up shows [specific change] is in place"] — [evidence]

**Recurrence check:** Has the same non-conformance (or near-miss) occurred since the corrective action completed? Yes / No
- If Yes: [describe and link]

**Effectiveness verdict:** Effective / Partially effective / Not effective
**If Partially or Not effective:** Reopen investigation at [phase] with the failed-effectiveness signal as new evidence.

**Reviewer:** [QA Lead role + name]
**Date:** YYYY-MM-DD
```

---

## Closeout Summary (§5.6)

Four-line summary on close. Posted as the final comment + captured in `Closeout Summary` custom field. Used by handoffs (Jobs 6a–d).

```
**CAPA-YYYY-NNN closeout (YYYY-MM-DD):**
- **Source event:** [non-conformance statement, abbreviated]
- **Root cause:** [root cause statement]
- **Actions taken:** [brief list — corrective and preventive]
- **Effectiveness verdict:** Effective — [evidence summary] / Partially or Not effective — [next action / reopen]
```

---

## What goes where

| Artifact | Where |
|---|---|
| Cover block | Task description |
| RCA verbatim walk | Comment thread on task |
| Action plans | Pinned comment, kept current as status changes |
| Verification record | Comment, posted at QA Lead approval |
| Effectiveness review | Comment, posted at QA Lead approval |
| Closeout summary | Final comment + `Closeout Summary` field |
| Evidence (photos, COAs, test results, signed docs) | Task attachments |
| Root cause statement | `Root Cause Statement` custom field |
| Root cause category (if Fishbone) | `Root Cause Category` custom field |
| Severity, Source, Category, Linked* | Custom fields per Asana surface in SKILL.md |
