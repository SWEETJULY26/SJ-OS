# Fireflies — connection reference

**Mechanism:** MCP (`mcp__Fireflies__*`)
**Covers:** Meeting intelligence domain in `connections.md`.

## Common query patterns

**Find and read a transcript:**
```
fireflies_search or fireflies_get_transcripts  — with appropriate date filters (date/scope first, not narrow keyword)
fireflies_fetch  — pulls the full transcript once you have the ID
```

**Other available tools:** `fireflies_get_summary`, `fireflies_get_analytics`, `fireflies_get_active_meetings`, `fireflies_get_user`, `fireflies_get_user_contacts`, `fireflies_list_channels`, `fireflies_share_meeting`, `fireflies_create_soundbite`.

## Two operating modes (per `fireflies-asana-bridge`, the primary consumer)

1. **Manual catch-up** — Alvin asks about a specific meeting or time period. Search with date filters → fetch full transcript → extract action items → confirm before pushing to Asana.
2. **Urgent auto-flag** — scanning recent transcripts proactively for missed deadlines, supplier issues, formula rejections, testing failures, or explicit "we need to..." statements. Surfaced separately, flagged urgent, before the regular action item list.

## Where the deeper structure lives

- `.claude/skills/fireflies-asana-bridge/SKILL.md` — full extraction logic and the PD/Ops/Quality/Regulatory classification signal table
- `references/architecture/bridge_queue_contract.md` — where extracted signals route
