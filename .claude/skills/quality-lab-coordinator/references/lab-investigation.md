# Lab Finding Investigation Template

Structure for the LF Asana task content. The skill drafts; the Operator (and QA Lead at the gates) approves. Mirrors the capa-investigation.md pattern in capa-coordinator so that when an LF hands off to capa-coordinator, the existing context flows forward without rework.

---

## LF cover block

```
**LF Number:** LF-YYYY-NNN
**Date opened:** YYYY-MM-DD
**Reporter:** [Name + role | Contract lab name]
**Procedure version:** Lab Quality Procedure v0.1 (2026-05-08)

**Classification:** OOS | OOT | Incoming Defect | Pattern | In-Spec Flag
**Severity:** Critical | Major | Minor
**Source:** lab-OOS | lab-OOT | vendor-receipt | vendor-systemic | batch-pattern | COA-mismatch | internal-flag | direct-open

**Linked records:**
- Batch: [PLM batch ID + link]
- Vendor: [name + purchasing-manager record link]
- SKU: [SKU code + name]
- PLM lab record: [link]
- Source task (if from a bridge): [Asana gid + title]

**Spec(s) affected:** [list]
**Result vs spec:** [measured value(s) vs spec value(s)]

**Statement of finding:** [one or two sentences — what was observed, when, on what]
```

---

## Containment block (drafted at intake, confirmed before any retest or handoff)

```
**Containment recommendation:** Hold | Quarantine | Retest only | No action
**Containment rationale:** [why this level — tied to severity and classification]
**Containment owner:** [role + name]
**Containment status:** Recommended / Confirmed / Closed (no longer needed)
```

For Critical severity: hold is the default; deviation requires explicit Operator + QA Lead sign-off.
For Major: hold or quarantine.
For Minor: retest-only or no-action are valid.

---

## Decision block (drafted after intake, approved per HITL)

```
**Decision path:** Retest | Watch list | Vendor flag | CAPA handoff | Close (Minor + retest passed)
**Decision rationale:** [tied to Lab Quality Procedure §3.3 + §4.2 thresholds]
**Approver:** [Operator | QA Lead — depending on path]
**Approval timestamp:** YYYY-MM-DD HH:MM
```

Rules per path:
- **Retest:** Operator approves. Capture retest reason, lab destination, expected return date.
- **Watch list:** Operator approves. Capture watch window (default 2 monthly cycles) and re-review trigger.
- **Vendor flag:** **QA Lead approves.** Walks Job 4 §4.3 review checklist before sign-off.
- **CAPA handoff:** Operator approves the stage. capa-coordinator runs its own intake HITL on receipt.
- **Close (Minor + retest passed):** Operator approves. Closeout summary required.

---

## Retest record (when chosen)

```
**Retest #:** [1, 2, etc.]
**Reason:** Sample integrity question | Suspected lab error | Expected drift | Vendor request | Other
**Lab dispatched to:** [name + request ID]
**Sample pulled:** YYYY-MM-DD | by [role + name]
**Expected return:** YYYY-MM-DD
**Result returned:** YYYY-MM-DD
**Retest result:** [value(s)]
**Retest verdict:** Pass | Fail | Inconclusive
```

If retest passes: classification shifts to In-Spec Flag, Operator decides watch or close.
If retest fails: original classification stands; severity may shift up; CAPA handoff path engages.

---

## Pattern read (when applicable — Job 3 output)

For LFs created from a pattern surfacing (Source = batch-pattern or vendor-systemic), or as a section in any LF that contributes to a pattern:

```
**Pattern type:** Vendor cluster | SKU cluster on single vendor | Spec cluster | Severity-weighted
**Window:** [time window — 60 / 90 days, or 12 months for severity-weighted]
**LFs in pattern:**
- LF-YYYY-NNN | [date] | [SKU] | [batch] | [vendor] | [classification]
- LF-YYYY-NNN | ...
- LF-YYYY-NNN | ...

**Threshold crossed:** Yes / No
**Rationale:** [why the cluster is or isn't real per §4.3 review checklist]
**Recommended action:** Vendor flag → scorecard | Vendor flag → CAPA | Watch list — additional cycles | No action
```

---

## Vendor flag block (when Decision path = Vendor flag)

```
**Vendor:** [name + purchasing-manager record link]
**Flag type:** Scorecard signal | CAPA route
**Pattern reference:** [LFs cited above, plus §4.2 threshold matched]
**Proposed scorecard impact:** Lead time | Fill rate | Defect rate | Documentation reliability | Multiple
**Severity of impact:** Note | Caution | Performance review trigger
**QA Lead approver:** [role + name]
**Approval timestamp:** YYYY-MM-DD HH:MM
```

If Flag type = Scorecard signal: Job 5 fires the comment-back per `vendor-scorecard-signal.md`.
If Flag type = CAPA route: Job 5b fires the capa-coordinator handoff with NCR intake context populated.

---

## CAPA handoff block (when Decision path = CAPA handoff)

Mirrors the NCR Procedure §3.2 intake fields so capa-coordinator picks up cleanly.

```
**Handoff to:** capa-coordinator → SJS CAPA Log Inbound Staging
**NCR intake context:**
- Source: lab-OOS | lab-OOT | vendor-receipt | vendor-systemic
- Category: Lab | Vendor | Process
- SKU(s): [list]
- Batch / lot code(s): [list]
- Vendor: [name]
- Description: [pulled from Statement of finding above]
- Evidence: [links to LF, PLM lab record, COA, retest result]
- Suspected severity: [matches LF severity]
- Containment action taken: [from Containment block]

**Handoff Asana task created:** [SJS CAPA Log gid + link]
**Handoff status:** Staged / Picked up by capa-coordinator / NCR opened (NCR-YYYY-NNN) / CAPA opened (CAPA-YYYY-NNN)
```

The skill comments back on the LF with the NCR / CAPA number once capa-coordinator opens.

---

## Closeout summary

```
**LF-YYYY-NNN closeout (YYYY-MM-DD):**
- **Source event:** [statement of finding, abbreviated]
- **Classification + severity:** [e.g., OOS, Major]
- **Resolution:** [retest passed | watch closed clean | scorecard signal posted to [vendor] on [date] | CAPA-YYYY-NNN closed Effective on [date] | batch hold released by batch-lifecycle-tracker on [date]]
```

Posted as the final comment + captured in the `Closeout Summary` custom field. Used by Job 6 close-the-loop comments on source records.

---

## What goes where

| Artifact | Where |
|---|---|
| Cover block | Task description |
| Containment block | Pinned comment, kept current |
| Decision block | Comment, posted at approval |
| Retest record | Comment per retest, attached evidence |
| Pattern read | Comment when LF contributes to a pattern |
| Vendor flag block | Comment when flag is staged + when QA Lead approves |
| CAPA handoff block | Comment when handoff stages |
| Closeout summary | Final comment + `Closeout Summary` custom field |
| Evidence (test reports, COAs, photos) | Task attachments |
| Classification, Severity, Source, LF Number, Linked Batch, Linked Vendor, Linked CAPA | Custom fields per Asana surface in SKILL.md |
