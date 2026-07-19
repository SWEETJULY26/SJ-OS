# Scheduled task: sjs-purchasing-morning-sweep

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/purchasing-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/outlook-plm-bridge/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-ops-system/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-master/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Microsoft 365, Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
You are running the AC Brands Purchasing morning sweep. This fires Mon–Fri at 8:26 AM PT. Output is silent on clean days.

## Objective

Scan the AC Brands Purchasing Asana project (GID `1214373717266702`) against 9 urgency categories. If any fire, post a single bundled comment to the **Purchasing Sweep Running Log** task in the **Cross-Skill Dashboard** section, with offenders grouped by category. If nothing fires, exit silently.

## Setup

Invoke the `purchasing-manager` skill first to load context, then the `sjs-ops-system` router for cross-skill seams. Read the AC Brands Purchasing project's Cross-Skill Dashboard section to locate the Purchasing Sweep Running Log task by name.

All "business days" use US business calendar, anchored to America/Los_Angeles. If today is a US federal holiday, exit silently and post nothing.

## The 9 urgency categories and thresholds

1. **PO variance** — header-level drift ≥5% OR absolute $ drift ≥$500 (whichever fires first). Quantity drift fires at >1 unit OR ≥2% of order qty. Line-level discrepancies stay in PLM unless they roll up into a header breach.
2. **PO ack overdue** — Sent ≥5 business days, no ack logged via `outlook-plm-bridge` and no manual ack mark from operator.
3. **PO ETA slippage** — slip ≥14 calendar days past original ETA, OR slip pushes ETA past the demand-plan cover window for the linked SKU/component (cross-ref `supply-demand-planner`; trips when cover drops below safety stock + lead time buffer). Whichever fires first.
4. **Compliance doc expiring** — ≤30 days for COAs, COCs, MSDSes with no replacement in flight. ≤60 days for COIs.
5. **Vendor invoice stuck in HITL classification** — State = Pending in Vendor Invoices section for >3 business days without any operator action (field touch, comment, or state change).
6. **Vendor dispute open** — Dispute task in Compliance, Renewals & Disputes section open ≥10 business days without movement (comment, state change, or assignee touch).
7. **Contract renewal stalled** — Renewal date inside 30-day window with no active `Renewal — Vendor Name (30d / 15d)` task in motion. 60d marker is informational only.
8. **Onboarding stalled** — Task in HITL — Needs Operations Review section, title-prefix `Onboarding —`, sitting in HITL >5 business days.
9. **Receipt → on-hand reconciliation lag** — PO task Status = Received for ≥3 business days without `inventory-manager` logging on-hand for the batch in PLM.

## Output format

If nothing fires: log "Purchasing sweep YYYY-MM-DD: clean" and exit. Do not post to Asana.

If anything fires: post a single comment to the Purchasing Sweep Running Log task. Group offenders by category. For each offender include:
- Task name + Asana permalink
- The specific threshold breach (e.g. "Sent 7 business days, no ack")
- Vendor name and PO number where applicable

Format:
```
Purchasing sweep YYYY-MM-DD

Category N — {category name}
- {task name} ({permalink}) — {breach detail}
- {task name} ({permalink}) — {breach detail}

Category M — {category name}
- ...
```

No preamble, no summary. Just the list.

## Constraints

- HITL is NOT required for posting the running log comment — the comment is the audit trail, not a record-creation or spend action.
- Do not open new tasks. Do not modify task fields. Read-only on the project except for the single comment write.
- Brand scope: AC Brands corporate, Sweet July Skin first.
- Operator: Alvin.
- Reference patterns: `sjs-regulatory-morning-sweep` (existing scheduled task) uses the same pattern.
