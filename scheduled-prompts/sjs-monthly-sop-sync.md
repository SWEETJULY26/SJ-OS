# Scheduled task: sjs-monthly-sop-sync

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/plm-assistant/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Microsoft 365, Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
You are running the monthly SOP sync for AC Brands / Sweet July Skin. Initial backfill happened 2026-05-26; this is the recurring drift check. Work in the Skill Builder project space, alongside the other SJS jobs.

Goal: Reconcile SharePoint "SOP" and "Forms" folders against public.sop_documents and public.wiki_pages in Supabase project ujkabbffvhpewpbttmmy. Update where SharePoint is newer; flag drift in a one-line summary.

Authoritative inventory (current canonical mapping, last reconciled 2026-05-31):
SOPs (Active): SKN-OPS-001 CAPA Procedure; SKN-OPS-002 Serious Adverse Event (SAE); SKN-OPS-003 Product Recall; SKN-OPS-004 Customer Complaint Handling; SKN-OPS-006 Lab Quality Procedure (Rev.1); SKN-OPS-007 Batch Lifecycle Procedure (Rev.1); SKN-OPS-008 Claims, IL, and Label Procedure (Rev.2); SKN-OPS-009 Reportable Events Procedure (Rev.1).
Forms (Active): SKN-F-OPS-001 CAPA Investigation Template; SKN-F-OPS-002 SAE Report Form; SKN-F-OPS-003 SAE Investigation Template; SKN-F-OPS-004 Root Cause Analysis Tools; SKN-F-OPS-005 Non-Conformance Report (NCR) — filename uses F-OPS-005 but doc references SKN-OPS-005; filename is canonical.
SharePoint-master-pending: SKN-OPS-006/007/008/009 are ratified and Active in sop_documents, but their SharePoint masters are NOT yet filed — sharepoint_url is the sentinel 'pending-ratification://skn-ops-NNN'. For these four: skip the SharePoint diff, never call read_resource on the sentinel URL, never downgrade their status, and report them under "master filing pending."

SharePoint folders:
- /Shared Documents/Sweet July/Product Development/Quality Control & Assurance/SOP/ — the 4 SOPs
- /Shared Documents/Sweet July/Product Development/Quality Control & Assurance/Forms/ — the 5 forms
- /Shared Documents/Sweet July/Product Development/Quality Control & Assurance/Logs/SOP & Form Log.xlsx — index (known typos vs filenames; trust filenames)

Steps:
1. Inventory current state. SELECT sop_id, sharepoint_modified_at, sharepoint_item_id FROM public.sop_documents WHERE status='Active' ORDER BY sop_id.
2. Re-search SharePoint. Call sharepoint_search with query "SKN-OPS" and "SKN-F-OPS" (limit 50 each). Capture name, webUrl, id (item ID), lastModifiedDateTime.
3. Diff. For each Active row, compare SharePoint lastModifiedDateTime to sop_documents.sharepoint_modified_at.
   - If sharepoint_url starts with 'pending-ratification://' (the master-pending SOPs 006–009): skip — do not read_resource, do not write. Count under "master filing pending."
   - If newer or sharepoint_item_id changed: read_resource on the file URI, capture extracted text, UPDATE sop_documents (set extracted_text, sharepoint_modified_at, sharepoint_item_id, sharepoint_url, synced_at=now()), then UPDATE wiki_pages SET content=<new synthesized briefing: Purpose/Scope/Owner/Triggers/Key Steps/Statutory Clocks/Linked Forms/Cross-refs/Source>, source_count=source_count+1, last_source='seed', last_source_ref=<new sharepoint_item_id> WHERE slug='sop/'||public.wiki_slugify(sop_id). The invalidate_wiki_embedding trigger NULLs the embedding; wiki-embed-backfill cron re-embeds within 5 min.
   - If unchanged: no action.
4. Detect new SOPs/Forms in SharePoint not yet in sop_documents. If found, log as drift but do NOT auto-insert — surface the list at the end.
5. Detect SharePoint master filing for the four master-pending SOPs (006–009). For each, check if SharePoint now has a matching SKN-OPS-NNN master file. If yes, surface as drift requiring HITL: the real master should replace the sentinel sharepoint_url and seed extracted_text + the wiki briefing (do not auto-write). If no match, report "master filing pending."
6. Final summary. One line: Synced X, unchanged Y, drift Z (new) + W (ratification ready). Embeddings: V SOP pages null pending next backfill tick.

Constraints:
- Slug rule: always 'sop/' || public.wiki_slugify(sop_id). Validator trigger rejects anything else.
- Never delete rows. Status changes only via HITL.
- Placeholder sentinel URL is pending-ratification://skn-ops-NNN — not a real SharePoint URL.
- The audit_wiki_pages trigger auto-logs every change; do NOT insert audit rows manually.
- If extracted text is shorter than 200 chars on a doc that previously had real content, treat as a parse failure and skip the write — surface it in the drift summary.

Output: post a single text summary at the end. No files written. If nothing changed, say so in one line.
