# Microsoft 365 (Outlook, Teams, SharePoint) — connection reference

**Mechanism:** MCP (`mcp__Microsoft_365__*`)
**Covers:** Outlook email + calendar, Microsoft Teams, SharePoint — one connector, three domains in `connections.md` (Customer interactions, Calendar, Communication, Knowledge/files partially).
**Operator email:** alvin@ac-brands.com

## Common query patterns

**Search email (Inbox, Sent Items, or any named folder):**
```
outlook_email_search(query, sender, recipient, folderName, afterDateTime, beforeDateTime, order, limit)
```
- Prefer **date/scope-first, then filter** over narrow keyword search — keyword filters miss content that's worded differently than expected. `afterDateTime` accepts natural language ("yesterday", "last week") or ISO dates.
- `folderName` recognizes `Inbox`, `Sent Items`, `Drafts`, `Deleted Items`, `Archive`, `Junk Email`, `Outbox` directly; anything else is looked up by enumerating folders.
- Returns metadata only — use `read_resource` on the returned URI for full body content.
- Max 25 results per call; paginate via `nextOffset` or `nextCursor` depending on query type.

**Calendar:**
```
outlook_calendar_search, outlook_find_available_time, find_meeting_availability
```

**Teams:**
```
teams_list_chats, chat_message_search
```

**SharePoint:**
```
sharepoint_search, sharepoint_folder_search
```

## Known patterns from this AIOS's skills

- The two Outlook-intake bridges (`outlook-asana-bridge`, `outlook-plm-bridge`) both scan Inbox + Sent Items and classify every email into `pd`/`ops`/`quality`/`regulatory`/`margin`/`intel` before deciding what to do with it — see `references/architecture/bridge_queue_contract.md` for where each classification routes.
- Sender/vendor/contact recognition is loaded live from Supabase (`public.wiki_pages` + `public.vendors`), not hardcoded — new contacts are recognized the moment they land in PLM, no file to update.

## Where the deeper structure lives

- `.claude/skills/outlook-asana-bridge/SKILL.md` and `outlook-plm-bridge/SKILL.md` — the two consumers of this connector, including the full classification signal table
- `references/voice.md` — Alvin's actual voice, pulled from real Sent Items samples, for drafting anything that goes out under his name
