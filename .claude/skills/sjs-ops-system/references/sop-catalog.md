---
name: SJS Ops SOP catalog
description: Catalog of Ops's own ratified SOPs (SKN-OPS-010, 012-023) across Purchasing, Inventory, Supply & Demand Planning, Logistics, and DTC/OC3PL. sjs-ops-system holds this catalog on behalf of the five Ops skills, none of which has an umbrella of its own the way Quality (quality-manager) or Regulatory (regulatory-manager) does. The shared ratification/annual-review/numbering process it follows lives in quality-manager/references/sop-program.md.
last_updated: 2026-08-06 (new)
---

# Sweet July Skin Ops SOP Catalog

The runtime source of truth for which revision of an Ops SOP is current, across Purchasing, Inventory, Supply & Demand Planning, Logistics, and DTC fulfillment.

**This catalog covers Ops's own SOPs only.** Quality, Regulatory, and PD each keep their own — see `quality-manager/references/sop-program.md` for the full catalogs-by-function map, and for the ratification protocol, annual review protocol, and numbering policy shared across all four. This file holds Ops's SOP rows and nothing else.

**Why this lives in `sjs-ops-system` rather than an Ops umbrella skill.** Quality and Regulatory each have an umbrella skill that already holds canonical cross-skill state — `quality-manager` and `regulatory-manager` — and PD's core engine `asana-pd-manager` fills the same role for PD. Ops has no equivalent: `purchasing-manager`, `inventory-manager`, `supply-demand-planner`, `logistics-manager`, and `oc3pl-order-manager` are five peer skills with no umbrella, and `sjs-ops-system` (this router, alongside its apparent near-duplicate `ac-brands-ops-system`) was built as a thin, read-only router with no canonical data of its own. Putting the catalog here is the closest fit available today, not a perfect one. If an `ops-manager` umbrella skill is ever built to mirror `quality-manager`/`regulatory-manager` in shape, this catalog should move there.

This catalog is new as of 2026-08-06, created alongside the first PD/Ops/DTC SOP batch. Before this, none of the five Ops skills had a ratified SOP or a catalog.

---

## 1. Catalog

| SOP Number | Title | Revision | Effective | Status | Canonical text | Skill-side Mirror | Next Review Due |
|---|---|---|---|---|---|---|---|
| SKN-OPS-010 | Supplier Onboarding Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-010-supplier-onboarding.md` | `purchasing-manager` Job 2A–2D (inline) | 2027-08-06 |
| SKN-OPS-012 | PD Readiness → PO Request Handoff Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-012-pd-po-request-handoff.md` | `asana-pd-manager` + `purchasing-manager` Job 3a (inline) | 2027-08-06 |
| SKN-OPS-013 | Purchase Order Lifecycle Procedure (Draft to Close) | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-013-po-lifecycle.md` | `purchasing-manager` Job 3 (inline) | 2027-08-06 |
| SKN-OPS-014 | Receipt Discrepancy Investigation Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-014-receipt-discrepancy-investigation.md` | `purchasing-manager` Job 10 (inline) | 2027-08-06 |
| SKN-OPS-015 | Vendor Invoice Cost Classification & Routing Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-015-vendor-invoice-cost-routing.md` | `purchasing-manager` Job 9 (inline) | 2027-08-06 |
| SKN-OPS-016 | Receiving & Batch Creation Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-016-receiving-batch-creation.md` | `inventory-manager` Job 2 (inline) | 2027-08-06 |
| SKN-OPS-017 | Inventory Adjustment, Write-Off, and Return Disposition Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-017-adjustment-writeoff-return-disposition.md` | `inventory-manager` Job 7 (inline) | 2027-08-06 |
| SKN-OPS-018 | Monthly S&OP Run Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-018-monthly-sop-run.md` | `supply-demand-planner` (inline) | 2027-08-06 |
| SKN-OPS-019 | Inbound Shipment Receipt & Fault-Attribution Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-019-inbound-shipment-fault-attribution.md` | `logistics-manager` Flows A/B (inline) | 2027-08-06 |
| SKN-OPS-020 | Retailer Outbound ASN & Routing Compliance Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-020-retailer-outbound-asn-routing.md` | `logistics-manager` Flows C/G (inline) | 2027-08-06 |
| SKN-OPS-021 | International Outbound DTC Compliance Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-021-international-outbound-dtc-compliance.md` | `logistics-manager` Flow H (inline) | 2027-08-06 |
| SKN-OPS-022 | DTC Order Exception Routing Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-022-dtc-order-exception-routing.md` | `oc3pl-order-manager` (inline) | 2027-08-06 |
| SKN-OPS-023 | Pre-Ship OOS Hold Sync Procedure | 1 | 2026-08-06 | Ratified | `sops/SKN-OPS-023-pre-ship-oos-hold-sync.md` | `oc3pl-order-manager` (inline) | 2027-08-06 |

**SKN-OPS-012 is joint with PD** — it also appears in `asana-pd-manager/references/sop-catalog.md`, since PD holds the readiness-gate side of the same procedure. This is the one deliberate cross-catalog listing; every other SOP number lives in exactly one catalog. If this SOP revises, update both catalog rows in the same pass.

**All thirteen rows carry the standing full-set annual review deferral** per `sop-program.md` §2 — none review individually on their Next Review Due date; they join the same one-time pass as SKN-OPS-001–004.

**Canonical text lives in `sops/`,** per the 2026-08-04 decision. None of the five Ops skills has a dedicated skill-side mirror file — the working procedure text for every row above lived inline in that skill's `SKILL.md` body, which is what's cited in the Skill-side Mirror column.

---

## 2. Asana representation

No pinned-task rendering exists for this catalog yet — there's no single Ops-wide Asana project to pin it in, since the five Ops skills each operate their own project. Worth revisiting if a cross-cutting Ops surface (something like Quality's SJS Quality Management) ever gets built.

---

## 3. Open items (Ops-specific)

- **No Ops umbrella skill.** This catalog's home in `sjs-ops-system` is a compromise — see the explanation above. Building an `ops-manager` skill that mirrors `quality-manager`/`regulatory-manager` in shape (cross-skill rollup, this catalog, a ratification queue) is the real fix, not done here.
- **No dedicated skill-side mirror files.** All thirteen SOPs' working text lives inline in five different `SKILL.md` bodies. Externalizing each into its own `references/skn-ops-*.md`, matching the Quality pattern, is a follow-on decision.
- **No Asana pinned-task rendering** (see §2).

For process-level open items (numbering, catalog-split structure), see `quality-manager/references/sop-program.md`.
