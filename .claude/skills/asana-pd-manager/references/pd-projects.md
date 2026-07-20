---
name: SJS PD projects
description: Canonical list of in-scope Sweet July Skin PD projects in Asana — active SKU projects (looked up live, not enumerated here), the Formula Development Tracker, and the portfolio. Used by asana-pd-manager and by sibling skills that need to resolve a SKU mention to an Asana project.
last_updated: 2026-05-17
---

# SJS PD projects

Cross-reference: SKU master lives in Supabase — `public.products` for the live portfolio and `public.wiki_pages WHERE page_type='sku'` for synthesized briefings (phase history, formula context, prior PLM writes). This file holds only Asana-project shape — project name, supplier, GID cache slot, stage-gate involvement.

## Portfolio

| Portfolio | Asana name | GID |
|---|---|---|
| Roadmap | 2026-2028 Product Development Roadmap | Look up on first use; cache in conversation |

## Stage-gate tracker

| Project | Asana name | GID |
|---|---|---|
| Formula tracker | SJ SKIN – Formula Development Tracker | `1213280384100264` |

The Formula Development Tracker is the only project that carries the 5-stage workflow + `IL Status` custom field. See `references/stage-gate-procedure.md` for the procedure.

## Individual SKU projects

Each SKU has its own Asana project. Look up by name on first use via `asana_typeahead_search` and cache the GID in the conversation. Primary supplier (the lab or fill site for the formula) comes from PLM:

```sql
SELECT p.name, v.name AS primary_supplier
FROM public.products p
LEFT JOIN public.product_vendors pv ON pv.product_id = p.id AND pv.role = 'primary'
LEFT JOIN public.vendors v ON v.id = pv.vendor_id
ORDER BY p.name;
```

Castaway Cream is the only split case the routing cares about: AMR Labs owns the formula; Allure Labs is the fill site. See `references/suppliers.md`.

## Project lookup discipline

For any project Alvin mentions that is not on this list, use `asana_typeahead_search` or `asana_get_projects`. Never guess a project GID.

Never create a task without specifying a project and section (Rule 3 in `references/confirmation-protocol.md`).

## Cross-references

- SKU master → `public.products` + `public.wiki_pages WHERE page_type='sku'`
- Supplier-to-SKU routing notes → `references/suppliers.md`
- Stage-gate procedure → `references/stage-gate-procedure.md`
- Asana field GIDs → `references/gids-pointer.md`
