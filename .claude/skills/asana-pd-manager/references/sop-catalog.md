---
name: SJS PD SOP catalog
description: Catalog of PD's own ratified SOPs (SKN-OPS-011-012). asana-pd-manager owns this catalog; the shared ratification/annual-review/numbering process it follows lives in quality-manager/references/sop-program.md.
last_updated: 2026-08-06 (new)
---

# Sweet July Skin PD SOP Catalog

The runtime source of truth for which revision of a PD SOP is current.

**This catalog covers PD's own SOPs only.** Quality, Regulatory, and Ops each keep their own — see `quality-manager/references/sop-program.md` for the full catalogs-by-function map, and for the ratification protocol, annual review protocol, and numbering policy shared across all four. This file holds PD's SOP rows and nothing else.

This catalog is new as of 2026-08-06, created alongside the first PD/Ops/DTC SOP batch. Before this, PD had no ratified SOPs and no catalog.

---

## 1. Catalog

| SOP Number | Title | Revision | Effective | Status | Canonical text | Skill-side Mirror | Next Review Due |
|---|---|---|---|---|---|---|---|
| SKN-OPS-011 | Formula Development Stage-Gate & IL Review Gate Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-011-formula-stage-gate-il-review.md` | `asana-pd-manager/references/stage-gate-procedure.md` | 2027-08-06 |
| SKN-OPS-012 | PD Readiness → PO Request Handoff Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-012-pd-po-request-handoff.md` | `asana-pd-manager` + `purchasing-manager` Job 3a (inline, no dedicated reference file) | 2027-08-06 |

**SKN-OPS-012 is joint with Ops** — it also appears in `sjs-ops-system/references/sop-catalog.md`, since Purchasing holds the order side of the same procedure. This is the one deliberate cross-catalog listing; every other SOP number lives in exactly one catalog. If this SOP revises, update both catalog rows in the same pass.

---

## 2. Asana representation

PD doesn't yet render this catalog as a pinned Asana task the way Quality does. Worth adding once the PD SOP set grows, or once a dedicated PD project section exists for it.

---

## 3. Open items (PD-specific)

- No dedicated skill-side mirror file for SKN-OPS-012 — the PO-request-handoff procedure text lives inline across both `asana-pd-manager` and `purchasing-manager`'s `SKILL.md` bodies rather than in a shared reference file either side points to. Worth externalizing given it's a joint procedure with two skills each carrying part of the working text.
- No Asana pinned-task rendering yet (see §2).

For process-level open items (numbering, catalog-split structure, mirror-file gaps across functions), see `quality-manager/references/sop-program.md`.
