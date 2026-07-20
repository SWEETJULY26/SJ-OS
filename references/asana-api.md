# Asana — connection reference

**Mechanism:** MCP (`mcp__Asana__*` and `mcp__Asana-c313a468__*` — two connector instances present in this environment; tools are largely mirrored across both, prefer whichever is already loaded in a given session rather than assuming one is canonical).
**Workspace:** AC Brands (`ac-brands.com`)
**Auth:** Connected via MCP, no manual token management needed from this side.

## Core objects and how this AIOS uses them

- **Projects** — the primary unit of work tracking. 146+ active (non-archived) projects across Operations, Product, SJ Ops, Product Marketing, Events and Activations, Executive teams. No single project holds "everything" — PD work lives in per-SKU projects plus a Formula Development Tracker and a 2026-2028 Product Development Roadmap portfolio.
- **Portfolios** — group projects for portfolio-level rollups. Key one: `2026-2028 Product Development Roadmap` (portfolio GID `1208854258418250`).
- **Custom fields** — carry structured state (RAG status, SOP phase, HITL gate state, IL Status). Full field GID cache lives in `references/architecture/gids.md`.
- **Tasks/subtasks** — standard work items. Status update title convention: `[RAG emoji] [Color], [Month Day], [Year] Update` (e.g. `🟢 Green, May 28, 2026 Update`) — this is how portfolio-wide sweeps parse color state without opening every project.

## Common query patterns

**List projects with task counts:**
```
mcp__Asana__get_projects(limit: 100, opt_fields: "name,archived,owner.name,current_status.title,team.name")
```
Paginate via the returned `next_page.offset`.

**Find a project by name (don't guess GIDs):**
```
mcp__Asana__search_objects or asana_typeahead_search
```
Always look up on first use and cache the GID in the conversation — never hardcode a GID you haven't verified this session.

**Pull tasks for a project:**
```
mcp__Asana__get_tasks(project: <gid>)
```

**Search across the workspace:**
```
mcp__Asana__search_tasks / asana_search_tasks
```

## Known limitations

- **Timing/Cutover Risk Notes** custom field (GID `1211644347258861`) is **not readable/writable through the MCP connector** — requires the Asana Chrome extension directly. Say so rather than silently skipping or guessing at its value.
- Two MCP connector instances exist in this environment (`Asana` and `Asana-c313a468`) — scheduled Routines' `allowed_tools` lists sometimes reference both explicitly; don't assume only one is wired.

## Write operations

Asana is one of the two domains in this AIOS that can WRITE (the other is Outlook/email). Every skill that writes to Asana confirms with the operator first (HITL) — see `.claude/skills/asana-pd-manager/references/confirmation-protocol.md` for the canonical write-confirmation contract other skills reuse.

## Where the deeper structure lives

- `references/architecture/system_map.md` — every skill, which Asana projects/queues it owns
- `references/architecture/bridge_queue_contract.md` — which Asana project each cross-system signal lands in
- `references/architecture/gids.md` — full custom-field and project GID cache
- `.claude/skills/asana-pd-manager/references/pd-projects.md` — PD-specific project shape
