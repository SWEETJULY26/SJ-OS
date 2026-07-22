# Task: Move the Fig lip treatment to Signed Approvals

Mode: raw Asana MCP tool access only (no skill invoked). No writes executed — proposal only, per instructions.

## What I found

"Fig lip treatment" resolves to the Sweet July Skin SKU **Fig Tinted Lip Treatment** (KDC/One Port Jervis, formula code 18GS830111). It shows up across several Asana objects:

- **Project**: `SJ SKIN - Fig Tinted Lip Treatment (KDC/One Port Jervis 18GS830111)` — gid `1213870527792236`. Sections: Risks, Phase 1 - Ideation, Phase 2 - Formula & Vessel Sampling (Allure & HCT), Phase 2 - Stability + Compatibility Testing, Phase 3 - Design + Storytelling, Phase 3 - Marketing/Creative, Phase 4 - Ramp Up, Phase 5 - Final Production, Phase 6 - Commercialization, Add-Ons.
- **Regulatory task**: `Regulatory (Amy) IL Review of Fig Tinted Lip Treatment` — gid `1213843552247307`, sitting in project `SJS Regulatory Management` (gid `1214660807386611`), section **Inbound Staging**, with custom fields Artifact Type = IL Review, Decision Status = Pending Review, Gate = (unset), Task Status = Not Started.
- A companion task, `Request and Receive IL from Port Jervis for Fig Tinted Lip Treatment` (gid `1213843552247300`), also in Inbound Staging on the same project.

## Problem: no "Signed Approvals" destination exists

I checked every place a stage/section by that name could live and found nothing called "Signed Approvals":

- `SJS Regulatory Management` sections: Inbound Staging, In Pedrero Review, Returned — Action Required, Active / In-Effect, Renewal Window, Closed, Registrations — Active, Registrations — Renewal Window, Pedrero Liaison, Cross-Skill Dashboard.
- `SJ SKIN - Fig Tinted Lip Treatment` (product project) sections: listed above — all phase-based, no approvals stage.
- `Lip Treatment (July 2025)` (umbrella lip PD project, gid `1206259636748363`) sections: Ideation, Formula Sampling, Stability Testing, Marketing Samples, Item Creation/PO, Artwork Sourcing/Sampling, Lip Final Production, Creative/Marketing, Commercialization, Risks.
- `AC Brands PD Dashboard` (gid `1210908660076461`) sections: Rollover/Risks, PD + Ops Agenda, Sourcing, Formulation and Testing, Packaging & Design, Regulatory, Logistics, Quality, Document Control, Completed.
- Two other lip/skincare project templates checked (Rum Cake Lip Treatment, Skin Parfait) — same phase-based section naming, no "Signed Approvals" anywhere.
- Custom field enum options on the regulatory task (Artifact Type, Decision Status, Gate, Registration Type, Task Status, etc.) — none named "Signed Approvals" either.
- Portfolio/task typeahead search for the literal string "Signed Approvals" returned no project and no task with that name.

So "Signed Approvals" isn't a section, board column, or field value that raw Asana access can confirm anywhere in this workspace. It reads like a named workflow stage from a documented procedure (the org's SKN-OPS-008 gate references a "Signed Approvals" stage move as a trigger point), but nothing in Asana itself is labeled that way — I can't verify which project/section it's supposed to correspond to from Asana data alone.

## Proposed change (not executed)

Best-guess candidates, in order of likelihood, if forced to pick a destination:

1. Move `Regulatory (Amy) IL Review of Fig Tinted Lip Treatment` (gid `1213843552247307`) from **Inbound Staging** → **In Pedrero Review** in `SJS Regulatory Management` — closest semantic match to an "approvals in progress" stage, but its name doesn't say "signed."
2. Move it to **Active / In-Effect** instead, if "Signed Approvals" means the approval has already been executed/signed and filed.
3. Alternatively, the ask may refer to a task/section that doesn't exist yet and needs to be created.

I did not execute any of these moves. Recommend confirming with Alvin (or whoever owns the SKN-OPS-008 procedure) which exact project and section "Signed Approvals" refers to before making any update — a blind section move risks filing the IL review in the wrong regulatory queue.

## Tool calls made

14 read-only Asana MCP calls (search/typeahead/get_task/get_project_sections/get_projects). Zero write calls. Zero errors.
