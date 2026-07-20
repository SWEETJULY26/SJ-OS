---
name: PD-side supplier routing
description: Sweet July Skin supplier-to-SKU mapping with PD-side routing notes. Used by asana-pd-manager and siblings to resolve a supplier mention to the right SKU project.
last_updated: 2026-05-17
---

# PD-side supplier routing

Canonical supplier master lives in Supabase — `public.vendors` (PLM-tracked vendors) and `public.wiki_pages WHERE page_type='supplier'` (supplier scope detail). This file holds only the PD-routing slice — which supplier owns formula vs. component work for which SKU, and which suppliers fire the email/meeting bridges.

## Source of truth

Supplier-to-SKU relationships live in PLM (`public.product_vendors` joined with `public.products` and `public.vendors`) and are enriched by `public.wiki_pages WHERE page_type='supplier'` for scope detail. Read live; no enumeration in this file.

Two structural notes that don't fit cleanly in PLM and stay here:

- **Allure Labs on Castaway Cream** is a fill-site relationship — formula is owned by AMR Labs. When a Castaway Cream signal hits, route formula questions to AMR and fill / operations questions to Allure.
- **Lip-program component split** follows the turnkey vs non-turnkey logic in `references/architecture/tool_patterns.md` (HCT tube every time; carton flows HCT for turnkey, CDW for non-turnkey).

## How this skill routes

When Alvin mentions a supplier by name without naming the SKU, look up the suppliers's SKUs and ask which one if more than one matches.

When a `pd` signal lands from `fireflies-asana-bridge` or `outlook-asana-bridge` with a supplier mention, route the resulting task to the matched SKU project per `references/pd-projects.md`.

## Cross-references

- Full supplier contact directory → `public.wiki_pages WHERE page_type='contact'`
- Canonical supplier master → `public.vendors` + `public.wiki_pages WHERE page_type='supplier'`
- SKU projects → `references/pd-projects.md`
