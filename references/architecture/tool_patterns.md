# Tool Patterns

**Use:** Patterns for using MCPs and build tools that have been validated in practice. When a skill says "search Outlook" or "pull Fireflies transcripts," this file holds the working pattern.

---

## Fireflies — pull by date, not by keyword

**Wrong pattern:** Filter Fireflies meetings by keyword like "KDC" or "lip" or "SJS PD." This misses critical content.

**Why it misses:** PD topics show up in meetings titled "Revenue Plan," "Weekly TB," "1:1s," "Quarterly Review," and other non-obvious titles. Keyword filtering on title silently drops the SJ Skin Weekly PD meeting and any internal sync where products were discussed in passing.

**Right pattern:**
1. `fireflies_get_transcripts` with date range (`from:` parameter), no keyword filter
2. Pull all meetings in the window
3. `fireflies_get_transcript` with each `transcriptId` to fetch full content
4. Filter on content, not title

For daily recap automation, always pull the full day's meetings. Never narrow by keyword.

---

## Outlook — broad query + date range, not narrow keyword

**Wrong pattern:** `outlook_email_search` with narrow keyword like `"Sorrel approval"` and no date filter.

**Why it misses:** PD-relevant emails arrive with non-obvious subjects (re-replies on threads, FW: forwards, supplier subject conventions that don't match the product name). A narrow keyword search drops 30-50% of what should be in scope.

**Right pattern:**
1. `outlook_email_search` with `afterDateTime` (and `beforeDateTime` if bounding) + a broad query (sender domain, supplier name, or no query at all)
2. Pull all returned messages
3. `read_resource` for full content on the candidates that look relevant

For sweep workflows ("scan my emails this week"), use no query and a date range only. Filter in post-processing.

---

## Asana — common patterns

**List all projects:** `asana_get_projects` with `opt_fields=name,gid` and `limit:50`.

**Resolve a project name to GID:** `asana_typeahead_search` with `resource_type=project` and the search query.

**Pull portfolio contents with status:** `asana_get_items_for_portfolio` with `opt_fields=name,gid,resource_type,current_status_update.title,current_status_update.color,current_status_update.created_at,due_date,owner.name` and `limit:100`.

**Update a task with custom fields:** Verify the field is attached to the project first. If `update_tasks` returns `"Custom field with ID X is not on given object"`, the field needs to be added to the project via UI.

**Portfolio custom fields:** Read-only via MCP. See `_shared/gids.md` for the Chrome extension fallback.

---

## Supabase / PLM — read direct, write via plm-assistant

**Reads (SELECT):** Direct via Supabase MCP `execute_sql` is fine. No confirmation needed.

**Writes (INSERT / UPDATE / DELETE):** Stage in the calling skill (build proposed SQL, get HITL approval, format preview), then hand to `plm-assistant` for commit. Never call `execute_sql` for writes from a non-PLM-assistant skill — that's a build-pattern violation.

**Inspect schema:**
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = '[table]'
ORDER BY ordinal_position;
```

**Common gotchas:**
- `incoterm` (singular), not `incoterms`
- PO sequencing: `MAX(po_number::int) + 1`
- Tooling line items don't need `component_id`

---

## Lip program vendor logic

The lip program has three configurations and the terminology is precise:

**Turnkey tinted** = HCT tube + HCT carton + KDC-One fill. HCT delivers the finished assembled secondary; KDC ships finished primary. One vendor relationship handles both component sides.

**Non-turnkey** = HCT tube + CDW carton, sourced and managed independently. Tubes flow HCT → KDC for fill. Cartons flow CDW → fulfillment separately.

**All lip tubes are HCT.** Always. The split is on the carton side.

Vendor names live in `public.vendors`; supplier scope detail (which products each vendor runs, current contract state) lives in `public.wiki_pages WHERE page_type='supplier'`. Read both at run time — no vendor enumeration belongs in a skill file.

---

## Chrome MCP — treat as unreliable

Chrome MCP has been persistently unreliable in recent sessions. Default assumption: it is not available.

**Fallback for browser-mediated tasks:**
- Local preview: build HTML in `/home/claude/`, serve locally if needed
- Netlify deploy: use the Netlify MCP for sharable previews
- Programmatic validation: regex-parse the generated HTML for structural correctness rather than visual inspection

If Chrome MCP works on a given attempt, fine. If it disconnects (it usually does), pivot immediately to the fallback. Don't burn time retrying.

---

## Build pattern for large HTML outputs

For dashboards, infographics, and any HTML > ~500 lines:

1. Generate programmatically via Python script in `/home/claude/`
2. Write the HTML to `/home/claude/`
3. Validate inline — regex-parse for panels, nodes, card counts, coordinate bounds, approximate SVG text-width estimation
4. `cp` the validated file to `/mnt/user-data/outputs/`
5. `present_files` to share

Direct file writes work for shorter outputs. The programmatic pattern is more reliable for anything large or repetitive.

**Excel parsing:** `.xlsx` files require `openpyxl` (`load_workbook` with `data_only=False`, iterate with `values_only=True`).

---

## Brand fonts (for Sweet July Skin output)

Brand fonts live at `/mnt/skills/user/sweet-july-skin-brand/assets/fonts/`. For HTML or PDF output, base64-encode them and embed as `@font-face` data URIs so the file renders correctly offline and on Netlify.

**Character width factors for layout estimation:**
- GT America Expanded: ~0.66
- Adrianna: ~0.55 (renders narrower in practice than the metric suggests)

Always defer to the brand skill for canonical font and color spec.
