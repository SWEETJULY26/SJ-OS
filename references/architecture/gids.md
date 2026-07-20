# GIDs & System Identifiers

**Use:** Quick lookup for Asana, PLM, and other system IDs. Read at runtime to avoid guessing GIDs.

**Discipline:** When a new GID lands in your context, add it here. Do not let GIDs accumulate in skill bodies or chat history without making it back to this file.

---

## Asana

### Workspace
- **Workspace name:** AC Brands
- **Workspace GID:** `1200120716421441` (used in every `app.asana.com/1/<workspace>/project/...` URL)
- **MCP endpoint:** `https://mcp.asana.com/sse`

### Teams
| Team | GID |
|------|-----|
| Operations | `1200120716421443` |
| SJ Ops | `1202786171817904` |
| Product (PD team — owns all SJ SKIN projects) | `1200207382836669` |

### Portfolios
| Name | GID |
|------|-----|
| 2026-2028 Product Development Roadmap | `1208854258418250` |
| Operations Dashboard | `1208174221370391` |
| Website Development & Maintenance (nested under Operations Dashboard) | `1203794275435836` |

### Key tasks
| Name | GID | Project |
|------|-----|---------|
| Daily PD recap running log | `1214208955674591` | AC Brands PD + Ops Dashboard |

### Project GIDs

Use `asana_typeahead_search` with `resource_type=project` or `asana_get_projects` with `opt_fields=name,gid` and `limit:50` to resolve project GIDs. Cache within a session.

Verified GIDs (names confirmed live via `asana_get_project` on 2026-05-31). Field, option, and section GIDs for the Quality / CAPA / Regulatory / Reportable Events projects are **not** repeated here — they live in `asana-field-gids.md` (API-pulled, the source of truth for field-level IDs). This table is the project-level lookup only.

**PD — trackers & infrastructure**
| Project | GID |
|---------|-----|
| SJ SKIN – Formula Development Tracker | `1213280384100264` |
| Skin NPD & Reverse Engineering Tracker | `1211644346712828` |
| Product Development Risk Register | `1212875424020186` |
| Sweet July Skin NPD Meeting | `1206991824031789` |
| Product End of Life (EOL) — also listed under Ops | `1202076429028079` |
| AC Brands PD Dashboard — see Dashboards | `1210908660076461` |

**PD — SKU projects (2026-2028 PD Roadmap, 23)**

Full roadmap roster as of 2026-05-31. Jamaican Cherry doubles as the reference template for new SKU projects.

| # | Project | GID |
|---|---------|-----|
| 1 | SJ SKIN – Jamaican Sunset Tinted Lip Treatment (KDC/One Port Jervis) | `1214502055661454` |
| 2 | SJ SKIN – Tamarind Tinted Lip Treatment (KDC/One Port Jervis) | `1214502055661475` |
| 3 | SJ SKIN – Ting Tinted Lip Treatment (KDC/One Port Jervis) | `1214501855377088` |
| 4 | SJ SKIN – Hibiscus Tinted Lip Treatment (KDC/One Port Jervis) | `1214501855377109` |
| 5 | SJ SKIN – Coffee Fix Lip Treatment (KDC/One Port Jervis 18JW83353) | `1213913920143639` |
| 6 | SJ SKIN – Rum Cake Lip Treatment (KDC/One Port Jervis) | `1214286636217352` |
| 7 | SJ SKIN – Guava Lip Treatment (KDC/One Port Jervis) | `1214286596710432` |
| 8 | SJ SKIN – Resurrection Balm (Capsum NBG3172) | `1214233710015203` |
| 9 | SJ SKIN – Essential Lip Treatment (KDC/One Port Jervis 18GS822085) | `1214206736192789` |
| 10 | SJ SKIN – New Coffee Fix Eye Cream (AMR Labs) | `1214046109102022` |
| 11 | SJ SKIN – Lychee Lip Treatment (KDC/One Port Jervis 18GS838057) | `1214054993856184` |
| 12 | SJ SKIN – Jamaican Cherry Tinted Lip Treatment (KDC/One Port Jervis 18GS830129) — reference template | `1213900755157243` |
| 13 | SJ SKIN – Sorrel Tinted Lip Treatment (KDC/One Port Jervis 18GS830107) | `1213900755157220` |
| 14 | SJ SKIN – Fig Tinted Lip Treatment (KDC/One Port Jervis 18GS830111) | `1213870527792236` |
| 15 | SJ SKIN – New Irie Power Oil (AMR Labs 7577D) | `1211664753330621` |
| 16 | SJ SKIN – New Castaway Cream (AMR Labs 7576C) | `1211664749517668` |
| 17 | SJ SKIN – New Pava Cleanser (Vegelabs VL13-41-4) | `1211656300474404` |
| 18 | SJ SKIN – New Soursop Vit C (AMR Labs 7587C) | `1211654563188028` |
| 19 | SJ SKIN – New Good Youth Retinol (AMR Labs 7575B) | `1211651306132807` |
| 20 | SJ SKIN – New Pava Toner Spray (AMR Labs 7497E) | `1211496482060309` |
| 21 | SJ SKIN – Pineapple Punch Face Mask 5/pk (IKS) | `1213306966885475` |
| 22 | SJ SKIN – Pineapple Punch Lip Treatment (KDC/One Port Jervis 18GS838017) | `1211047706252252` |
| 23 | SJ SKIN – Castaway Cleansing Oil (Vegelabs VL13-53-3R1) | `1208080045186859` |

**PD — active skin SKUs outside the roadmap portfolio**

Skin projects on the Product team that aren't in the 2026-2028 Roadmap portfolio.

| Project | GID |
|---------|-----|
| Skin Parfait (Q3 2026) KDC | `1210632749647197` |
| Coffee Fix Eye Patches 5/pk (IKS) | `1213306732889235` |

**Scope note.** The Product team (`1200207382836669`) carries ~55 active + ~36 archived projects total. Most are legacy Sweet July lifestyle lines (linens, ceramics, candles, coffee, apparel) outside Sweet July Skin scope — deliberately **not** registered here. This file tracks the SJS PD set: the 23 roadmap SKUs, the trackers above, and the two non-roadmap skin SKUs. For the full team roster, query the Product team GID directly.

**Ops** (live)
| Project | GID |
|---------|-----|
| AC Brands Inventory | `1214374368959019` |
| AC Brands Purchasing | `1214373717266702` |
| Sweet July Skin Logistics | `1214370420013442` |
| Sweet July Skin S&OP | `1214347479282044` |
| OC3PL Order Management | `1214235522292179` |
| SJ Shipping Dashboard | `1206266539116267` |
| Work Requests | `1202063921848694` |
| SJ Oakland Conversion | `1208186347159221` |
| Product End of Life (EOL) | `1202076429028079` |
| Sweet July Skin 3PL Transition – FWS to OC3PL | `1213371671094748` |
| AC Brands Holiday Calendar | `1214055559810920` |

`inventory-manager`'s queue ("AC Brands Inventory" in `bridge_queue_contract.md`) resolves to `1214374368959019`. The 3PL Transition project is an active FWS→OC3PL migration.

**Ops — archived in Asana** (reference only, do not route to)
| Project | GID |
|---------|-----|
| SJ Inventory Dashboard (superseded by AC Brands Inventory) | `1207103091400936` |
| AC Brands Ops Dashboard | `1202106077428461` |

**Dashboards & cross-functional** (Operations Dashboard portfolio roster)
| Project | GID |
|---------|-----|
| AC Brands PD Dashboard | `1210908660076461` |
| AC Brands Leadership Dashboard | `1210917729477334` |
| ACB Landing Hub — Updates & Releases | `1214790724230121` |

**Quality** (field + section GIDs in `asana-field-gids.md`)
| Project | GID |
|---------|-----|
| SJS Quality Management | `1214660401644163` |
| SJS CAPA Log | `1214660784338465` |
| SJ Skin Complaint Log | `1204763097184846` |

**Regulatory** (field + section GIDs in `asana-field-gids.md`)
| Project | GID |
|---------|-----|
| SJS Regulatory Management | `1214660807386611` |
| SJS Reportable Events | `1214660834583706` |

### Purchasing project section GIDs

Sections inside the AC Brands Purchasing project. Used by `outlook-plm-bridge` Flow C-gate and `purchasing-manager` Job 2.

| Section | GID |
|---------|-----|
| Vendor Onboarding | `1215139855143672` |
| Compliance, Renewals & Disputes | `1214373372406262` |

### Project-level custom field GIDs

These are attached at the project level and **work** via Asana MCP `update_tasks`.

| Field | GID | Type |
|-------|-----|------|
| Task Status | `1202066776433270` | enum |
| Priority | `1200877060153810` | enum |
| Functional Area | `1205205983000962` | enum |
| Decision Type | `1213817530901693` | enum |
| Decision Status | `1213817442678365` | enum |

If a custom field returns `"Custom field with ID X is not on given object"` on `update_tasks`, the field needs to be attached to the project via UI first, then re-run.

### Portfolio-level custom field GIDs — 2026-2028 PD Roadmap

These are attached at the portfolio level. They appear on each project as a portfolio item. **Read works via MCP. Writes do not.** All 20 fields require the Chrome extension portfolio spreadsheet view for updates.

| # | Field name | Field GID | Type | Enum options |
|---|-----------|-----------|------|---------------|
| 1 | Priority | `1206108577437801` | enum | High · Medium · Low |
| 2 | Category | `1211644347258834` | enum | Innovation · Reverse Engineering |
| 3 | Formula Supplier (Current → New) | `1211653169077368` | enum | Allure → KDC/One (Port Jervis) · VeggieLabs · GoodKind → VeggieLabs · GoodKind → AMR Labs · AMR Labs · KDC/One (Chemaid) · KDC/One (Port Jervis) · Allure Labs · IKS · Allure → AMR Labs · Capsum |
| 4 | Vessel Supplier (Current → New) | `1211653183800178` | enum | HCT · Element · PKG. · Allure → HCT · Element → HCT · Element → PKG. · N/A · IKS · Capsum |
| 5 | Carton Supplier (Current → New) | `1211653184352624` | enum | CDW · Element · Element → CDW · N/A · IKS · HCT · Capsum |
| 6 | Current BOM Cost | `1211653353033276` | number | — |
| 7 | New BOM Cost | `1211644347258859` | number | — |
| 8 | Timing/Cutover Risk Notes | `1211644347258861` | text | free-form |
| 9 | Forecasted Inventory Runout/Expiration | `1211644347258863` | date | — |
| 10 | Change Impact | `1211644347258865` | text | free-form |
| 11 | Current Price | `1211724237730637` | number | — |
| 12 | Target Price | `1211724239511155` | number | — |
| 13 | Launch Risk Status | `1213727989303579` | enum | Off Track · At Risk · On Track |
| 14 | Current Phase | `1213812213696307` | enum | Ideation · R&D · Packaging · Sampling · Testing · Production · Launch Ready |
| 15 | Financial Status | `1213814907458121` | enum | On Target · At Risk · Off Target |
| 16 | Financial Risk Flag | `1213814907372417` | enum | Yes · No |
| 17 | Decision Required | `1213815051835915` | enum | Yes · No |
| 18 | Primary Blocker | `1213814921823765` | enum | None · Formula · Packaging · Vendor Capacity · Testing · Regulatory · Internal Approval |
| 19 | Dependency Status | `1213815113149769` | enum | None · Waiting on Vendor · Waiting on Internal · Blocked |
| 20 | SKU | `1213879801597825` | text | free-form |

**Note on terminology:** Portfolio fields named "Vessel Supplier" use the legacy "Vessel" term. Per `style_rules.md`, never use "vessel" in any output, comment, or communication — this field name is internal-Asana-only. Externally, refer to specific components (tube, bottle, jar, pump, cap, carton).

---

## Asana MCP — known limitations

### Portfolio-level custom fields
**Read works via MCP. Writes do not.** All 20 portfolio-level fields above require the Chrome extension portfolio spreadsheet view for any update operation.

**Working pattern when updating portfolio fields at scale:**
1. Stage the value changes in chat as a paste-ready table (project name → field → new value)
2. Open the portfolio spreadsheet view in Chrome
3. Paste row-by-row into the spreadsheet

### Other limitations
- **Custom fields not attached to a project** return `"Custom field with ID X is not on given object"` on `update_tasks` calls. Resolution: attach the field to the project via UI first, then re-run the batch.
- **Task name copy errors from project duplication** can be fixed via `asana_update_task` with the corrected name.

---

## PLM (Supabase)

| Item | Value |
|------|-------|
| Project ID | `ujkabbffvhpewpbttmmy` |
| MCP endpoint | `https://mcp.supabase.com/mcp` |

### Vendor IDs (frequent references)
| Vendor | ID |
|--------|-----|
| KDC-One | `ea2f6d63-375b-499f-8c0e-c7ee877f1733` |

### Schema notes
- `incoterm` (singular) — not `incoterms`. Common error.
- `vendor_invoices` (created 2026-05-31) — Flow I cost ledger. Unique `(vendor_id, invoice_number)`; `cost_category` check (regulatory/quality/pd/ops/marketing/general); `status` check (staged/approved/paid/disputed/void). Written via `plm-assistant`.
- `product_test_results` (created 2026-05-31) — Flow E target. One row per test event; `test_type` (stability/compatibility/RIPT/PET/micro/challenge/other), `result` (pass/fail/pending/conditional); `batch_id` null for pre-launch formula-level tests. Replaces the old (nonexistent) "product test fields" on `products`.
- PO numbering: `MAX(po_number::int) + 1` for the next sequence.
- One-time tooling items are valid in `purchase_order_items` without `component_id`.
- Company billing defaults live in `settings`.
- Use a CTE pattern when inserting a PO + line items in a single transaction.

---

## Microsoft 365

| Item | Value |
|------|-------|
| MCP endpoint | `https://microsoft365.mcp.claude.com/mcp` |
| Alvin's email | alvin@ac-brands.com |

---

## Fireflies

| Item | Value |
|------|-------|
| MCP endpoint | `https://api.fireflies.ai/mcp` |
