# Trigger phrases — grouped by intent

The skill description holds the canonical trigger list for routing. This file is the working library — operators and other skills can browse it to understand what fires this skill versus a peer.

## Generate the live dashboard (Job 1)

Phrases that regenerate the live page and commit to GitHub.

- "regenerate regulatory dashboard"
- "rebuild the regulatory dashboard"
- "push the regulatory dashboard"
- "publish the regulatory dashboard"
- "redeploy the regulatory page"
- "the regulatory dashboard needs a refresh"
- "rebuild reg dashboard"

Also fires automatically on first-run setup.

## Monthly snapshot (Job 2)

Phrases that capture a month-end archive.

- "snapshot the regulatory dashboard"
- "create monthly regulatory archive"
- "archive this month's regulatory state"
- "regulatory month-end snapshot"

Also fires automatically:
- First business day of each month at 9am PT via the `schedule` skill (cron `0 9 1 * * America/Los_Angeles`)

## Read-only summary on demand (Job 3)

Phrases that return a chat-formatted regulatory summary.

- "regulatory update for the team"
- "regulatory summary"
- "give me the regulatory rollup"
- "regulatory status now"
- "where are we on regulatory"
- "how does regulatory look this week"

Some of these phrases also fire `regulatory-manager` Job 2 directly. The two skills are sister readers; either can serve a summary query, but `regulatory-status-reporter` adds the optional Asana comment + branded format.

## Asana attachment (Job 4)

Read-only on triggers — attachment fires automatically as part of Job 1 or Job 2.

- "attach the regulatory dashboard to [task]"
- "log this regulatory dashboard generation"

## Status (cross-cutting)

Read-only. No HITL gate.

- "is the regulatory dashboard up to date"
- "when did the regulatory dashboard last regenerate"
- "is the Netlify Function for regulatory rollup healthy"
- "any [Monthly Regulatory Dashboard Snapshot] tasks open"

## Boundary phrases — these route to peer skills

| Phrase pattern | Routes to | Why |
|---|---|---|
| "what's open in regulatory" / "regulatory dashboard" (read-only intent) | regulatory-manager Job 2 | Cross-skill rollup composition lives there. This skill renders the rollup, doesn't compose it. |
| "any open SAEs" / "stage the recall report" | adverse-event-and-recall-reporter | SAE/recall workflow lives there. |
| "stage the IL on [SKU]" / "stage the [retailer] attestation" | claims-il-and-label-keeper | IL/claim/label/attestation lifecycle lives there. |
| "log this complaint" / "trigger an SAE protocol" | complaint-and-event-handler | Customer signal intake lives there. |
| "branded quality dashboard" / "regenerate quality dashboard" | quality-status-reporter | System B sister skill. |
| "branded PD update" / "Sweet July Skin status update" | sjs-status-reporter | PD-side rollup rendering. |
| "update PLM on [SKU]" | plm-assistant | PLM is the only writer. |

When a peer skill isn't live yet, this skill renders the relevant section as a "section unavailable" placeholder rather than fabricating data.

## Edge cases the skill should handle

| Pattern | Behavior |
|---|---|
| "skip the operator approval — just push it" | Decline. Per memory: never commit without confirmation. |
| "deploy directly to Netlify" | Decline. Per memory: deployment goes through GitHub commit-and-push to main; Netlify auto-deploys. |
| "the Netlify Function is returning 500" | Don't render fake counts. Surface the function error as a banner on the live page; archive the most recent successful state if available. |
| "the rollup is stale by 3 days" | Surface the staleness with `last_updated` timestamp on the page; let the operator decide whether to manually trigger a refresh. |
| "render this in PDF" | Decline at v6.4. PDF/PPTX/DOCX outputs are out of scope. Stage as a future-revision request to the operator. |
| "add a new KPI tile" | Pause. Tile changes require a scope memo update (regulatory-status-reporter-scope.md §F). Operator + Reg Lead approve before commit. |
| "the regulatory section on links.json got removed" | Restore from git history; surface to operator. Don't silently re-add — confirm intent. |
