# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## On-demand dashboard generation (Job 1)

Phrases that fire a full regeneration of `quality-dashboard.html` and a commit-push.

- "regenerate quality dashboard"
- "rebuild the quality dashboard"
- "push the quality dashboard"
- "publish the quality dashboard"
- "update the quality dashboard"
- "deploy the quality dashboard"
- "the quality dashboard layout needs an update"
- "fix the quality dashboard"

Always require operator confirmation before commit. No auto-push at v5.7.

## Monthly tab refresh (Job 2)

Auto-fires monthly. Manual triggers also valid.

- "refresh monthly quality tab"
- "push the monthly quality update"
- "refresh the monthly quality dashboard"
- "monthly quality tab refresh"

Auto-fire schedule: `sjs-quality-monthly-snapshot` scheduled task — first business day of month, 7:00 AM PT America/Los_Angeles. Registered via the `schedule` skill at first-run.

## Read-only summary (Job 3)

Phrases that return a chat-formatted summary, no file writes.

- "what's open in quality" (this also fires quality-manager Job 2 — return both views)
- "quality update for the team"
- "quality summary"
- "give me the quality rollup"
- "quality status now"
- "what's the quality state"
- "quality health"

## Asana attachment (Job 4)

Auto-fires as part of Job 1 only at v5.7. Direct triggers:

- "attach the quality dashboard to [task]"
- "attach the quality dashboard to the on-demand task"

Monthly (Job 2), Quarterly (Job 5), and Weekly digest (Job 6) cadences do NOT attach files — they post a breadcrumb to the Quality Sweep Running Log task instead.

## Quarterly tab refresh (Job 5)

Auto-fires quarterly. Manual triggers also valid.

- "refresh quarterly quality tab"
- "push the quarterly quality update"
- "quarterly quality tab refresh"
- "quarterly quality rollup push"

Auto-fire schedule: `sjs-quality-quarterly-rollup` scheduled task — first business day of Jan/Apr/Jul/Oct, 7:00 AM PT America/Los_Angeles. Registered via the `schedule` skill at first-run.

## Weekly digest push (Job 6)

Named scheduled trigger for the Weekly tab. Auto-fires weekly. Manual triggers also valid.

- "push weekly quality digest"
- "push the weekly quality update"
- "weekly quality digest push"
- "fire the weekly quality cadence"

Auto-fire schedule: `sjs-quality-weekly-digest` scheduled task — Monday 7:30 AM PT America/Los_Angeles. Registered via the `schedule` skill at first-run.

## Status (cross-cutting)

Read-only. No HITL gate.

- "when did the quality dashboard last run"
- "any pending quality dashboard generations"
- "what's the latest quality dashboard archive"
- "is the quality dashboard live"

## Boundary phrases — these route to peer skills

Listed for clarity so the skill knows when to defer.

| Phrase pattern | Routes to | Why |
|---|---|---|
| "what's open in quality" (when wanting raw rollup, not a dashboard refresh) | quality-manager Job 2 | Rollup composition lives there. v5.7 renders it. |
| "quality dashboard for Ayesha" / "quality update to send to [retailer]" | sweet-july-skin-brand + this skill | If branded for a specific external audience, brand styling applies. v5.7 still owns the underlying rendering. |
| "PD dashboard" / "branded PD update" | sjs-status-reporter | PD-side rollup; sister skill, not this scope. |
| "operations dashboard" / "branded ops update" | future ops-status-reporter | Operations-side rollup; sister skill, not this scope. |
| "leadership dashboard" / "executive dashboard" | ac-brands-leadership-dashboard | Cross-system dashboard. |
| "open a CAPA on [issue]" | capa-coordinator | CAPA + NCR lifecycle. |
| "log this complaint" | complaint-and-event-handler | Customer signal intake. |
| "log this OOS" / "OOT on [batch]" | quality-lab-coordinator | Lab classification. |
| "release / hold on [batch]" | batch-lifecycle-tracker | Batch state. |
| "ratify [procedure]" / "SOP catalog" | quality-manager | Catalog + ratification queue. |

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "regenerate without confirming the commit" | Decline. Every commit requires operator confirmation per memory `feedback_acb_hub_deploy.md`. |
| "skip the Netlify Function update" | Pause. If section / project GIDs changed, the Function must regenerate too. Confirm with operator before keeping the Function as-is. |
| "publish to a different repo" | Decline. The hub repo at `/Users/alvinbelt/Downloads/acb-thelanding/` is the only target at v5.7. |
| "snapshot the dashboard for next month" | Decline. Snapshots are point-in-time of current state. Use the live page to see future months as they unfold. |
| "make a PDF of the dashboard" | Decline at v5.7. PDF / PPTX / DOCX are out of scope. If the user needs print output, suggest browser print-to-PDF as a workaround. |
| "build the page without quality-manager rollup" | Decline. quality-manager rollup is the single source. Building without it diverges from the canonical state. If quality-manager is unavailable, surface that to the operator and stop. |
| "deploy directly via Netlify CLI" | Decline. Per memory `feedback_acb_hub_deploy.md`, deploy goes through GitHub commit-push only. |
| "push without seeing the diff" | Pause. Show `git status` and `git diff` to the operator before commit. |
| "merge the quality dashboard with the inventory dashboard" | Decline. Single-page, single-purpose. Cross-page navigation goes via the hub nav. |
