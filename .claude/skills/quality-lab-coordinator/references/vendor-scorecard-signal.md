# Vendor Scorecard Signal — Handshake Contract with purchasing-manager

The contract between quality-lab-coordinator (signal source) and purchasing-manager (scorecard owner). Defines what the signal looks like, where it gets posted, and what each side does next.

**The single rule:** purchasing-manager owns the vendor scorecard records. quality-lab-coordinator never writes the scorecard. The handshake is a comment-back on a purchasing-manager record, not a cross-project write to a scorecard.

---

## Why comment-back instead of direct write

Two reasons:

1. **Single ownership of the scorecard.** Vendor performance is a multi-input record — lead time and fill rate from purchasing data, defect rate from lab + receiving data, documentation reliability from compliance docs, landed cost from logistics-manager. If multiple skills wrote directly, the scorecard would split-brain on conflicts. purchasing-manager already owns the integration of all those inputs into the scorecard view per its Job 5 (vendor performance).

2. **Audit trail.** A comment is timestamped, attributable, and lives next to the vendor's existing record. Anyone reading the purchasing-manager task sees "lab signaled X on date Y, scorecard updated on date Z." A direct write would lose that lineage.

---

## When this fires

Job 5 in SKILL.md. Trigger conditions:
1. Job 4 (vendor flag review) decision = Flag for vendor scorecard signal.
2. QA Lead has approved the flag.
3. The flagged LF (or LF cluster) is fully classified, contained, and documented.

If any of those is missing, the signal does not post. Operator can stage; QA Lead approval is the commit gate.

---

## Target record resolution

The signal lives as a comment on a specific purchasing-manager Asana task. Resolution order:

1. **Open vendor record.** If the vendor has an open task in AC Brands Purchasing (project gid `1214373717266702`) with `Vendor` field matching, post on that task.
2. **Most recent closed PO.** If no open vendor task, find the most recent PO task for that vendor (Status in Closed, sorted by completion date). Post on that task.
3. **Vendor onboarding task.** If neither exists (rare — should only happen for newly onboarded vendors with no PO history), post on the onboarding task.
4. **No record found.** Abort the post and surface to the Operator: "No purchasing-manager record found for [vendor]. Confirm vendor is onboarded before flagging."

The skill resolves by reading the AC Brands Purchasing project via Asana directly (this skill has read access to that project per SKILL.md "Reads via" section). The skill does not write tasks in that project — only comments.

---

## Comment format

The comment is structured so purchasing-manager's scanner picks it up cleanly. Format:

```
[Vendor Scorecard Signal] from quality-lab-coordinator

**LF reference(s):** LF-YYYY-NNN, LF-YYYY-NNN, ...
**Pattern type:** [Vendor cluster | SKU cluster | Spec cluster | Severity-weighted]
**Window:** [60 / 90 days, or 12 months]

**Findings summary:**
- LF-YYYY-NNN | YYYY-MM-DD | [SKU] | [batch] | [classification + severity] | [one-line statement]
- LF-YYYY-NNN | ...
- LF-YYYY-NNN | ...

**Proposed scorecard impact:**
- Category: [Lead time | Fill rate | Defect rate | Documentation reliability | Multiple]
- Severity of impact: [Note | Caution | Performance review trigger]
- Reasoning: [one or two sentences tying the LFs to the proposed category]

**Suggested next step for purchasing-manager:** [e.g., "Update [vendor] defect rate in Q[X] scorecard." | "Trigger performance review per scorecard threshold." | "No PO action; flag for next QBR."]

**Containment status:** [each LF's containment confirmed / closed]
**No CAPA opened OR CAPA-YYYY-NNN opened/closed:** [whichever applies]

**QA Lead approval:** [role + name] | YYYY-MM-DD HH:MM
**Lab finding tasks:** [Asana links to each LF in SJS Quality Management]
```

The format mirrors the structured intake format purchasing-manager already reads in its Job 5 (vendor performance) — so this signal slots into the same scorecard composition flow.

---

## What purchasing-manager does on receipt

Defined for clarity, but executed by purchasing-manager — not this skill.

1. Acknowledge the signal in a reply comment within 2 business days.
2. Decide whether to write the scorecard impact now or aggregate with other Q-period signals.
3. If a performance review is triggered, route per their Job 5.
4. Reply-comment back to the signal with the scorecard write timestamp + scorecard view link. Closes the loop visibly on the purchasing-manager record.

quality-lab-coordinator's job 5 closes when the purchasing-manager reply-comment posts. That close moves the LF Status from `Scorecard Signaled` to `Closed` per Job 6.

---

## Severity-of-impact bands

Three bands, used by purchasing-manager to gauge urgency. quality-lab-coordinator proposes; purchasing-manager calibrates against their own scorecard rules.

**Note** — Single LF or marginal pattern. Logged for the next quarterly scorecard refresh, no immediate action needed.
- Default for: 1 Minor LF, 2 Minor LFs in a SKU cluster, 1 Major LF on a Tier-3 vendor.

**Caution** — Pattern is real and needs visibility. Surfaces in next monthly scorecard view.
- Default for: 3+ Minor LFs in a vendor cluster, 1 Major LF on a Tier-1 or Tier-2 vendor, any spec cluster.

**Performance review trigger** — Pattern crosses a scorecard performance threshold and warrants a vendor conversation per purchasing-manager's renewal/dispute logic.
- Default for: any 1 Critical LF, 2+ Major LFs in 12 months on the same vendor, severity-weighted threshold per Lab Quality Procedure §4.2.

The skill drafts the band per these defaults; QA Lead approves the band as part of Job 4 sign-off.

---

## Failure modes and fallbacks

| Failure | Behavior |
|---|---|
| Vendor record not found in AC Brands Purchasing | Abort post, surface to Operator. Do not create a vendor record from this skill — that's purchasing-manager Job 2. |
| Comment post fails (Asana API error, permissions) | Retry once. If still failing, mark LF status as `Scorecard Signal — Post Failed`, surface to Operator. Do not silently drop. |
| purchasing-manager doesn't reply within 5 business days | Surface to Operator as overdue. Do not re-post the signal — duplicate signals pollute the scorecard composition. |
| QA Lead approves the flag but the LF cluster has been closed in the meantime (e.g., new evidence resolved the pattern) | Pause the post. Operator confirms whether the flag is still valid given the new state. |
| Vendor disputes the signal after post | The dispute lands in purchasing-manager's `Compliance, Renewals & Disputes` flow. quality-lab-coordinator stays out of the dispute resolution but provides the LF evidence on request. |

---

## What this contract is not

- Not a cross-project Asana task creation. quality-lab-coordinator never creates tasks in AC Brands Purchasing.
- Not a PLM write. PLM updates to the vendor record go through plm-assistant, called by purchasing-manager when they decide to write the scorecard.
- Not a notification. The comment is the artifact; no separate Slack / email ping fires from this skill.
- Not a one-way fire-and-forget. The reply-comment from purchasing-manager is what closes the LF — without it, the LF stays in `Scorecard Signaled` status indefinitely.

---

## Versioning

Contract version: v0.1, 2026-05-08. Any change to comment format, severity bands, or target resolution order requires update on both sides (quality-lab-coordinator + purchasing-manager). Both skills cache the contract version they were built against; mismatch surfaces on first run.
