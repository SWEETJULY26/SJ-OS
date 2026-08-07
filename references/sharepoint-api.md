# SharePoint — connection reference

**Mechanism:** MCP (`mcp__Microsoft_365__sharepoint_search`, `sharepoint_folder_search`, `read_resource` for folder listings and file content) — same connector as Outlook/Teams, see `references/microsoft-365-api.md` for the shared connector basics.
**Covers:** Knowledge/files domain in `connections.md` (SharePoint half — Supabase/PLM is the other half, see `references/supabase-plm-api.md`).
**Read-only.** No skill in this suite can write to SharePoint via MCP. Every "publish to SharePoint" step across Quality and Regulatory skills is a manual UI drag-and-drop — the skill drafts the file and hands it to Alvin to file.

## The real vs. unfinished structure — confirmed 2026-07-27

There are two parallel SharePoint structures. **Confirmed with Alvin: the old `Shared Documents` library is the real, live one. A migration to a dedicated `sites/SWEETJULY` site was started and never finished.**

- **Real / live:** the `Shared Documents` library at `acbrands.sharepoint.com` — paths look like `Shared Documents/Sweet July/...`. 421.6 GB. Actively edited (files found modified through 2026-07-24).
- **Unfinished migration target:** `sites/SWEETJULY/...` — 8 document libraries (PRODUCT DEVELOPMENT, OPERATIONS, LEADERSHIP, FINANCE, MARKETING, RETAIL & EVENTS, SYSTEMS, Documents). Roughly 5.8 GB, well under 2% of the real library by size. Partial mirror — PD covers 7 of the real PD's 19 folders.

**⚠️ DO NOT DELETE THE `sites/SWEETJULY` SITE. It is not a disposable snapshot.** An earlier pass concluded it was frozen at 2026-02-28 and safe to discard — that was wrong, based on reading folder timestamps only. **File** timestamps run months past the folder dates: the 2026 SJ Skin Supply + Demand Plan (2026-05-15), Castaway BOM (2026-04-02), Lychee COAs (2026-03-10), vendor list CSV (2026-03-03), and two ACTIVE-marked Ops governance SOPs (2026-03-01). Someone worked in that site for ~2.5 months after it was created.

**Critically, the entire OPERATIONS library exists ONLY on that site and is more complete than the live library's Ops material.** Unique content with no `Shared Documents` counterpart: `Ops SOPs and User Guides/Documentation & Governance/` (an AC Brands SOP template and an Operations file-naming standard, both marked ACTIVE), the 2026 Supply + Demand Plan, the vendor list CSV, product weights/dims, Channel Operations/Amazon, and an Operations Control Center site page. By comparison `Shared Documents/Sweet July/Operations/` is 171 KB and `Sweet July Skin/Operations/` is 79 KB.

So the two structures are not original-and-copy. They're **split brain**: PD/Quality/product content is authoritative in the old library, Operations content is authoritative on the new site. Any consolidation has to merge, not pick a winner.

No edits found on the new site after 2026-05-15, so it is dormant — but dormant is not disposable.

**Don't build new skill logic against `sites/SWEETJULY/...` paths** for PD/Quality/product work — prefer the `Shared Documents` equivalent. For Operations material, the new site may be the only source; check both.

## Common query patterns

```
sharepoint_search(query)        — full-text search across accessible sites/libraries
sharepoint_folder_search(query) — find a folder by name/path
read_resource(uri)              — list a folder's contents, or read a file, given the URI from a search hit
```
Search returns metadata/URIs, not file content or folder listings — always follow up with `read_resource` on the returned URI to see what's actually inside a folder.

## Folder map (confirmed against the live tenant, 2026-07-27)

**SOP master folder — real, but incomplete.** `Shared Documents/Sweet July/Product Development/Quality Control & Assurance/SOP/` exists and holds exactly four files:

- Corrective Action Preventive Action (CAPA) SOP SKN-OPS-001 Rev.1.docx
- Serious Adverse Event (SAE) SOP SKN-OPS-002 Rev. 1.docx
- Product Recall Standard Operating Procedure (SOP) SKN-OPS-003 Rev. 1.docx
- Customer Complaint SKN-OPS-004 Rev 1.docx

**SKN-OPS-005 through 009 are not there.** Five skills — `capa-coordinator` (SKN-OPS-005 NCR), `quality-lab-coordinator` (SKN-OPS-006 Lab Quality), `batch-lifecycle-tracker` (SKN-OPS-007 Batch Lifecycle), `claims-il-and-label-keeper` (SKN-OPS-008 IL/Claims/Label), `adverse-event-and-recall-reporter` (SKN-OPS-009 Reportable Events) — each note "ratified in-place, SharePoint master to follow" in their own `references/` file. None of those masters were ever actually filed. The skills have been treating these five as ratified SOPs for months off their own working drafts; the real SOP library disagrees. This is a manual-filing gap, not a skill bug — someone needs to actually generate and upload those five `.docx` files (build scripts for 006/007 already exist per `quality-manager/references/sop-catalog.md` §3.3).

**Correct root path.** It's `Sweet July/Product Development/Quality Control & Assurance/` (unabbreviated "Product Development," directly under `Sweet July`, not under `Sweet July Skin`). `quality-manager/references/sop-catalog.md` had this abbreviated to `Sweet July/PD/...` — wrong, now corrected there too.

**`Sweet July/Regulatory/` genuinely does not exist.** Confirmed by direct folder search — zero hits. `regulatory-manager/references/sharepoint-pointer.md`'s entire subfolder table (IL Versions, Claim Substantiation, Label Artwork Archive, Retailer Attestations, Reportable Events, Registrations, Pedrero Correspondence) describes a structure that was never built. What actually exists instead, both directly under `Product Development`:

- `Compliance/` — contents not fully inventoried; known to include ingredient-list / MOCRA-adjacent files
- `MOCRA_Ariana/` — a loose folder (not nested under Compliance), holding two files: `SWEET JULY SKIN BLACK LIST.docx` and MOCRA INCI spreadsheets (`...Inci Mocra_2.0...xlsx`)

Neither maps cleanly onto the seven-subfolder structure the skills assume. Standing up the real `Regulatory/` folder (or deciding `Compliance/` + `MOCRA_Ariana/` already serve that purpose and should just get referenced as-is) is an open decision for Alvin, not something to build skill logic around yet.

**Logistics:** routing-guide PDFs, customs invoices, and retailer compliance spec source docs live "under the logistics folder" per `logistics-manager` — not yet located in this sweep. Get the actual path from Alvin before wiring a live logistics SharePoint read.

**File naming convention** (regulatory artifacts, per SKN-OPS-008 §5): `[SKU-CODE]_[ARTIFACT-TYPE]_[VERSION]_[YYYY-MM-DD].ext` — aspirational until the folder it applies to exists.

## Open cleanup items (Alvin's call, most need manual SharePoint access — MCP here is read-only)

0. **Plaintext credentials.** `Shared Documents/Sweet July/Marketing/Social Media/Log In Information and Passwords.docx` holds social account logins in the clear, modified 2026-06-29. Surfaced incidentally during the structure sweep. Move to a password manager and revoke/rotate.

1. Decide the fate of the unfinished `sites/SWEETJULY/...` migration — finish it, or merge its unique Operations content back and *then* retire it. **Do not delete it outright**: the OPERATIONS library exists only there and is more complete than the live library's Ops material (see above).
2. File the five missing SOP masters (SKN-OPS-005–009) as real `.docx` uploads to the SOP folder — closes the gap between what the skills claim is ratified and what SharePoint actually holds.
3. Decide what the Regulatory folder situation actually is: build the `Sweet July/Regulatory/` structure the skills assume, or repoint `regulatory-manager`/`claims-il-and-label-keeper`/`adverse-event-and-recall-reporter` at `Compliance/` + `MOCRA_Ariana/` as they exist today.
4. Get the real logistics SharePoint path from Alvin so that reference stops being a guess.

## Where the deeper structure lives

- `.claude/skills/regulatory-manager/references/sharepoint-pointer.md` — the regulatory folder pointer this file's findings correct
- `.claude/skills/quality-manager/references/sop-catalog.md` — the SOP catalog, path corrected 2026-07-27
- `.claude/skills/complaint-and-event-handler/references/skn-ops-002-sae.md`, `skn-ops-003-recall.md` — SOP mirrors, path already matched the real one
- `.claude/skills/logistics-manager/references/asn-templates.md`, `forms/retailer-spec.md` — logistics' SharePoint-sourced compliance docs
- `decisions/log.md` (2026-07-27 entry) — the full cleanup finding and why it matters
