---
name: SJS Regulatory SOP catalog
description: Catalog of Regulatory's own ratified SOPs (SKN-OPS-008-009). Sub-skills query at runtime to confirm current revision before significant writes. regulatory-manager owns this catalog; the shared ratification/annual-review/numbering process it follows lives in quality-manager/references/sop-program.md.
last_updated: 2026-08-06 (new — split out of quality-manager's combined catalog)
---

# Sweet July Skin Regulatory SOP Catalog

The runtime source of truth for which revision of a Regulatory (System C) SOP is current. Sub-skills query this catalog before significant writes (e.g., claims-il-and-label-keeper confirms SKN-OPS-008 Rev before staging an IL packet; adverse-event-and-recall-reporter confirms SKN-OPS-009 Rev before a filing).

**This catalog covers Regulatory's own SOPs only.** Quality, PD, and Ops each keep their own catalog — see `quality-manager/references/sop-program.md` for the full catalogs-by-function map, and for the ratification protocol, annual review protocol, and numbering policy shared across all four. This file holds Regulatory's SOP rows and nothing else.

This catalog is new as of 2026-08-06. Before that, SKN-OPS-008 and 009 sat in quality-manager's combined catalog alongside Quality's own SOPs, because that catalog was the only one that existed.

---

## 1. Catalog

| SOP Number | Title | Revision | Effective | Status | Canonical text | Skill-side Mirror | Next Review Due |
|---|---|---|---|---|---|---|---|
| SKN-OPS-008 | IL / Claims / Label Procedure | 2.0 | 2026-05-12 | Ratified | `sops/SKN-OPS-008-il-claims-label-procedure.md` | `claims-il-and-label-keeper/references/il-claims-label-procedure.md` | 2027-05-12 |
| SKN-OPS-009 | Reportable Events Procedure | 1.0 | 2026-05-09 | Ratified | `sops/SKN-OPS-009-reportable-events-procedure.md` | `adverse-event-and-recall-reporter/references/reportable-events-procedure.md` | 2027-05-09 |

Neither row is currently overdue for review — both post-date the SKN-OPS-001–004 review cycle. They are not part of the standing full-set deferral in `sop-program.md` §2 unless their own Next Review Due date arrives before that pass runs; if it does, defer them into the same pass rather than reviewing in isolation.

**Canonical text lives in `sops/`,** per the 2026-08-04 decision. The **Skill-side Mirror** column is each skill's operational walk layered on top of the canonical text; it is not a second source of truth.

---

## 2. Asana representation

Regulatory doesn't yet render this catalog as a pinned Asana task the way Quality does — SJS Regulatory Management doesn't currently carry a SOP Catalog section. Until one exists, this file is read directly rather than surfaced in Asana. Worth adding if Regulatory's SOP set grows past two.

---

## 3. Open items (Regulatory-specific)

- No Asana pinned-task rendering yet (see §2).
- No skill-side gaps currently flagged against either SOP.

For process-level open items (numbering, catalog-split structure, mirror-file gaps across functions), see `quality-manager/references/sop-program.md`.
