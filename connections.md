# Connections

Registry of every system your AIOS can reach. Filled by `/onboard` from Q4-Q7 answers; expanded over time as you wire new tools. `/audit` checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | Shopify (sweetjuly.com) | mcp | connected | 2026-07-19 |
| 2 | Customer interactions | Outlook | mcp | connected | 2026-07-19 |
| 3 | Calendar | Outlook Calendar | mcp | connected | 2026-07-19 |
| 4 | Communication | Outlook, Microsoft Teams, iMessage | mcp (Outlook/Teams); not yet connected (iMessage) | connected (Outlook/Teams); — | 2026-07-19 |
| 5 | Project / task tracking | Asana | mcp | connected | 2026-07-19 |
| 6 | Meeting intelligence | Fireflies | mcp | connected | 2026-07-19 |
| 7 | Knowledge / files | SharePoint, Supabase (PLM) | mcp | connected | 2026-07-19 |
| 8 | Business surface / function map | AC Brands landing hub (`SWEETJULY26/acb-thelanding`) | repo | connected | 2026-07-31 |
| 9 | Digital marketing | WITHIN (paid media, Klaviyo email) | partner — see `references/external-partners.md` | — | 2026-07-31 |
| 10 | Web development | Teknologics (sweetjuly.com, Shopify storefront) | partner — see `references/external-partners.md` | — | 2026-07-31 |
| 11 | Finance | Ironclad Finance (Dan Bender) | partner — see `references/external-partners.md` | — | 2026-07-31 |
| 12 | HR / payroll | Calm HR (PEO, co-employer); Paylocity platform | partner — see `references/external-partners.md` | — | 2026-07-31 |
| 13 | Managed IT / infrastructure | Coastal Interactive (back-end IT, equipment, identity) | partner — see `references/external-partners.md` | — | 2026-07-31 |

The landing hub's `data/links.json` defines the eleven business functions with a named lead each. It is the canonical answer to "what does this business actually do" and is a source for the org-wide RACI in `deliverables/`.

**Mechanism options:** `mcp` (MCP server), `repo` (git repository), `partner` (external organisation), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever.
