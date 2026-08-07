---
name: SJS Quality SOP catalog
description: Catalog of Quality's own ratified SOPs (SKN-OPS-001-007). Sub-skills query at runtime to confirm current revision before significant writes. quality-manager owns this catalog; the shared ratification/annual-review/numbering process it follows lives in references/sop-program.md, which also owns which SOPs Regulatory, PD, and Ops each catalog separately.
last_updated: 2026-08-06 (split out of the combined catalog into a Quality-only one; process moved to sop-program.md)
---

# Sweet July Skin Quality SOP Catalog

The runtime source of truth for which revision of a Quality SOP is current. Sub-skills query this catalog before significant writes (e.g., capa-coordinator confirms SKN-OPS-001 Rev before opening a CAPA; batch-lifecycle-tracker confirms SKN-OPS-007 Rev before drafting a hold record).

**This catalog covers Quality's own SOPs only.** Regulatory, PD, and Ops each keep their own catalog now — see `references/sop-program.md` for the full catalogs-by-function map, and for the ratification protocol, annual review protocol, and numbering policy shared across all four. This file holds Quality's SOP rows and nothing else; it doesn't restate the shared process.

---

## 1. Catalog

| SOP Number | Title | Revision | Effective | Status | Canonical text | Skill-side Mirror | Next Review Due |
|---|---|---|---|---|---|---|---|
| SKN-OPS-001 | CAPA Procedure | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-001-capa-procedure.md` | `capa-coordinator/references/skn-ops-001.md` | 2026-06-30 |
| SKN-OPS-002 | Serious Adverse Event (SAE) | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-002-sae-reporting.md` | `complaint-and-event-handler/references/skn-ops-002-sae.md` | 2026-06-30 |
| SKN-OPS-003 | Product Recall | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-003-product-recall.md` | `complaint-and-event-handler/references/skn-ops-003-recall.md` | 2026-06-30 |
| SKN-OPS-004 | Customer Complaint Handling | 1.0 | 2024-06-30 | Ratified | `sops/SKN-OPS-004-customer-complaint-handling.md` | (none — owned by complaint-and-event-handler workflow) | 2026-06-30 |
| SKN-OPS-005 | Non-Conformance Report (NCR) Procedure | 1.0 | 2026-05-09 | Ratified | `sops/SKN-OPS-005-ncr-procedure.md` | `capa-coordinator/references/ncr-procedure.md` | 2027-05-09 |
| SKN-OPS-006 | Lab Quality Procedure | 1.0 | 2026-05-08 | Ratified | `sops/SKN-OPS-006-lab-quality-procedure.md` | `quality-lab-coordinator/references/lab-procedure.md` | 2027-05-08 |
| SKN-OPS-007 | Batch Lifecycle Procedure | 1.0 | 2026-05-08 | Ratified | `sops/SKN-OPS-007-batch-lifecycle.md` | `batch-lifecycle-tracker/references/batch-lifecycle-procedure.md` | 2027-05-08 |

**Annual review deferred per `sop-program.md` §2.** SKN-OPS-001–004 are overdue (due 2026-06-30) but wait for the full-set review pass across all four catalogs rather than firing individually.

**Canonical text moved to `sops/` on 2026-08-04.** The **Skill-side Mirror** column is each skill's operational walk layered on top of the canonical text (job mappings, HITL gates, field maps); it is not a second source of truth and should not drift into restating procedure text the canonical file already owns. SKN-OPS-004's canonical text was reconstructed from skill behavior rather than transcribed from a SharePoint original, and stands as the real version going forward — no reconciliation pass is planned.

**Forms (SKN-F-OPS-NNN).** Five forms sit alongside the procedures in PLM `sop_documents`, all Rev 1.0, effective 2024-06-30, on the same 2026-06-30 review cycle as SKN-OPS-001–004: F-001 CAPA Investigation Template, F-002 SAE Report Form, F-003 SAE Investigation Template, F-004 Root Cause Analysis Tools, F-005 Non-Conformance Report (NCR) Form. They were absent from this catalog until the 2026-07-29 wiki audit.

**SharePoint master path (historical, pre-2026-08-04):** `Sweet July/Product Development/Quality Control & Assurance/SOP/` — note the real path is unabbreviated `Product Development`, directly under `Sweet July` (no folder named `PD` has ever existed in the tenant; the 2026-07-27 audit confirmed this and the string here was corrected 2026-08-07). That folder still holds only the four 2024 Rev.1 docx (SKN-OPS-001–004), now non-canonical copies of the `sops/` markdown — unmarked as superseded on the SharePoint side.
**SOP & Form Log (historical):** `Sweet July/Product Development/Quality Control & Assurance/Logs/SOP & Form Log.xlsx` — last modified 2024-07-22; predates everything ratified since.

---

## 2. Asana representation

This catalog renders in Asana as a pinned task in the SOP Catalog section of SJS Quality Management. The pinned task description carries the §1 catalog table. Updates to the table happen at every ratification, every annual review, every status change.

The pinned task GID is cached in SKILL.md after first-run setup.

---

## 3. Open items (Quality-specific)

- SKN-OPS-001 §5 in-text gaps (effectiveness review window not specified, retention period `[X]` placeholder, RCA tool selection criteria absent): SKN-OPS-005 closes the effectiveness window gap; the retention placeholder and RCA tool selection criteria stay open. Bundle into a future Rev.2 of SKN-OPS-001 when authored.
- SKN-OPS-001 through SKN-OPS-004 annual review: due 2026-06-30, overdue. Deferred per `sop-program.md` §2 until the full SOP set across all four catalogs is populated, then run as one pass rather than per-SOP.

For process-level open items (numbering, catalog-split structure, mirror-file gaps), see `sop-program.md` and the other three catalogs' own Open Items.
