# Task: Move the Fig lip treatment to Signed Approvals

## What I found (live Asana reads)

**Task:** "Lip Treatment - Fig - Formula Development" — `gid 1215142031949462`
**Project:** SJ SKIN – Formula Development Tracker (`1213280384100264`)
**Current section:** **Approved** (`1213275856358443`)
**Permalink:** https://app.asana.com/1/1200120716421441/project/1213280384100264/task/1215142031949462

Key custom field values on the task today:
- Formula # — `18GS842159`
- Revision # — `3`
- Review Status — `Approved`
- Submission Status — `Approval Form Signed`
- Chain of Custody — `With Ayesha`
- Formula CM — `Port Jervis (KDC/One)`
- Flavor/Fragrance — `.73% Natural Fig Type Flavor N81008 (Carrubba) with .42% Sweetener`
- **IL Status — null (not set)**

Three other "Fig" formula-development tasks exist, all in **Archived/Rejected** (earlier revisions #1 and #2, plus a duplicate — `1214314392109294`, `1213275856358455`, `1213275856358556`). Not relevant to this move; the live #3 revision is the one above.

## Discrepancy found — flagging before proposing anything

`references/stage-gate-procedure.md` documents the Formula Tracker as a 5-stage workflow: **Intake / Concept → In Review → Signed Approvals → Revisions Required → Rejected**.

The live project's actual sections (via `asana_get_project_sections`) are: **Intake / Concept, In Review, Sampling, Revisions in Progress, Final Review, Approved, Archived/Rejected, References.**

There is no section literally named "Signed Approvals." The closest match is **Approved** — and the Fig task is already sitting there, with `Review Status = Approved` and `Submission Status = Approval Form Signed`. So either:
1. The task is already at the stage Alvin means by "Signed Approvals" (no move needed), or
2. "Approved" and "Signed Approvals" are the same stage under different labels and the reference doc is stale against the live project's section names.

Either way, executing a move right now would be a no-op (source section = destination section), and I'm not willing to fire the IL Review Gate (Rule 7) on a no-op move without Alvin confirming that's actually what he wants.

## Rule 1 confirmation preview (per `references/confirmation-protocol.md`) — STOPPING HERE, NOT EXECUTED

```
📋 Confirm before I proceed:
• Action: Move Formula Tracker task to "Approved" (closest live-Asana match to "Signed Approvals")
• Target: "Lip Treatment - Fig - Formula Development" (gid 1215142031949462)
• Details:
   - Current section: Approved — task is already here. This would be a no-op move unless you want me to treat it as a fresh Signed-Approvals confirmation.
   - IL Status custom field would flip: null → "Pending IL Review"
   - Per Rule 7 / stage-gate-procedure.md, this fires the IL Review Gate atomically:
       1. Create inbound task in SJS Regulatory Management (1214660807386611), title prefixed
          "[IL Review Pending — claims-il-and-label-keeper]"
       2. Place it in Inbound Staging section (1214661463988658)
       3. Set Artifact Type = IL Review
       4. Set Linked SKU = Fig Tinted Lip Treatment (Formula # 18GS842159)
       5. Link back to this Formula Tracker task in the new task's description
   - Note: section-name mismatch flagged above (Approved vs. Signed Approvals) — want me to update the
     reference doc to match live Asana, or is "Approved" not actually equivalent to "Signed Approvals"?

Proceed?
```

No writes executed. No stage move, no IL Status flip, no IL Review Gate task created. Awaiting Alvin's confirmation and a call on the naming discrepancy above.
