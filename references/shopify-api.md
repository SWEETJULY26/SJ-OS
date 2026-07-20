# Shopify — connection reference

**Mechanism:** MCP (`mcp__Shopify__*`)
**Store:** Sweet July (`sweetjuly.com`) — Advanced plan, USD, PDT.
**Covers:** Revenue/Financials domain in `connections.md` — the primary DTC revenue source of truth.

## Common query patterns

**Store info:** `get-shop-info` — name, domain, plan, currency, timezone.
**Products:** `search_products`, `get-product`, `create-product`, `update-product`, `bulk-update-product-status`.
**Collections:** `search_collections`, `get-collection`, `create-collection`, `update-collection`, `add-to-collection`.
**Orders:** `list-orders`, `get-order`.
**Customers:** `list-customers`.
**Inventory:** `get-inventory-levels`, `set-inventory`.
**Analytics:** `run-analytics-query` (ShopifyQL).
**Discounts:** `create-discount`.

## GraphQL fallback

The built-in tools above cover common operations. For anything without a dedicated tool (gift cards, metafields, metaobjects, pages, blogs, markets, translations, publications, etc.), use `graphql_query` (read) or `graphql_mutation` (write) directly against the Admin API — don't report something as unavailable just because there's no shortcut tool for it. `graphql_schema` and `validate_graphql_codeblocks` help construct correct operations.

## Write discipline

Shopify writes (product updates, inventory changes, discounts) are real production changes to the live storefront — confirm with the operator before any create/update/bulk-update call, same discipline as Asana/PLM writes elsewhere in this AIOS.

## Where the deeper structure lives

Retail-side revenue (Sephora, Ulta, Whole Foods) is tracked separately, not through this Shopify connection — see `context/about-business.md` for the full channel list.
