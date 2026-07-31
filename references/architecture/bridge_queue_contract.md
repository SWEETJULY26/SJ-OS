# Bridge queue contract

**Use:** Authoritative rule for how the four bridges hand off to the rest of the system. Single source of truth — bridges, sub-system routers, and destination skills all reference this file.

**Companion:** `asana_task_contract.md`. This file decides **which queue** a task goes to. That one decides **what the write looks like** once the queue is known — resolve before create, required fields, due dates, collaborators, section moves and multi-homing. Every bridge and destination skill walks both.

**Last updated:** 2026-07-29 — Added the companion pointer to `asana_task_contract.md` and the multi-home note under "Cross-system signal" below. Prior 2026-05-26 — Authored as Priority 2 of `Bridge-and-System-Audit-2026-05-26.md`. Resolves the router/bridge ownership asymmetry by codifying the queue model the system already uses in practice.

---

## The rule

The four bridges never call destination skills directly. They post to specific Asana projects (and to PLM via `plm-assistant`). Each sub-system's umbrella router and member skills pick up work from those projects on their own cadence.

This means:

- Bridges describe **what queue they write to**, not what skill consumes it.
- Sub-system routers describe **which Asana projects they pick up from**, not which bridges call them.
- Destination skills (member skills under a router) consume tasks from their queue — they don't need to know which bridge produced the task.
- Cross-system signal is the same model: a bridge that detects cross-system signal posts to the **target system's** queue, and that system's router fans out.

**Cross-system signal doesn't always mean a second task.** When the signal is the same work item that a second system needs to see, it's one task multi-homed into both queues — one owner, one due date, each system closing its own side. A second task is right only when each system owes a distinct deliverable with its own close. `asana_task_contract.md` Phase 4 has the test and the API call.

### Inbound PO with a freight leg — Purchasing **and** Logistics

The `ops` row above reads as one-of, and for most signals it is. An inbound purchase order that is physically shipping is the exception: it is one work item that two systems act on, so it is one task multi-homed into both, per Phase 4's could-one-person-close-it-once test.

- **AC Brands Purchasing** — primary. Owns the PO lifecycle and the close. Carries the `Status` field.
- **Sweet July Skin Logistics** — secondary, section by cargo type: `Inbound — Components` or `Inbound — FG`. Owns the move. Carries `Shipment Status` and `Carrier/Vendor`.

Both homes get their own fields populated in the same pass, per `asana_task_contract.md` Phase 4. The two `Status`-shaped fields are different fields measuring different things and both are set: Purchasing's tracks the PO lifecycle and advances to `In Transit` on the first shipping signal, while Logistics' `Shipment Status` tracks physical position and stays `Pre-Ship` until the cargo actually departs. Neither is wrong when they disagree.

This matches the ownership split already stated in `sjs-ops-system` ("Logistics owns the move; Inventory…") — it just says which task each side reads it from, which was previously unspecified. Before 2026-07-31 no rule put a PO in Logistics at all, and the one place Logistics appeared as a multi-home destination named a project that does not exist.

**Not yet proven at volume.** PLM's `shipments` table is empty and the Logistics project was mostly section seeds until this rule landed. The freight flow is built, not exercised. Expect to revise section choice and the owner split once real shipments run through it.

Margin, Intel, and Founder skills do not run an Asana queue. They are direct-output skills that read Asana / PLM live, generate output, and stop. Bridges therefore do not "fan out" to them. The bridges' role for those skills is to land the underlying data in PLM and Asana, where the direct-output skills then read it.

---

## Asana queue map

The Asana projects each bridge can post to, and the router / member skill that picks up.

### PD queue

| Asana destination | Picked up by |
|---|---|
| Individual SKU projects (13 active) | `asana-pd-manager` (PD router: `sjs-pd-system`) |
| SJ SKIN – Formula Development Tracker | `asana-pd-manager` |
| AC Brands PD + Ops Dashboard | `asana-pd-manager` |
| 2026-2028 Product Development Roadmap (portfolio) | `asana-pd-manager` |

### Ops queue

Per `sjs-ops-system`. Each Ops skill operates a dedicated Asana project; the bridge posts to the project named by the signal type.

| Asana destination | Picked up by |
|---|---|
| AC Brands Purchasing | `purchasing-manager` |
| AC Brands Inventory | `inventory-manager` |
| Sweet July Skin S&OP | `supply-demand-planner` |
| Logistics project | `logistics-manager` |
| OC3PL Order Management | `oc3pl-order-manager` |
| SJ Shipping Dashboard | `oc3pl-order-manager` |

### Quality queue

Per `sjs-quality-system`.

| Asana destination | Picked up by |
|---|---|
| SJS Quality Management (gid `1214660401644163`) | `quality-manager` (umbrella) |
| SJS CAPA Log | `capa-coordinator` |
| SJ Skin Complaint Log | `complaint-and-event-handler` |
| Lab Findings sections of SJS Quality Management | `quality-lab-coordinator` |
| Batch lifecycle sections of SJS Quality Management | `batch-lifecycle-tracker` |

### Regulatory queue

Per `sjs-regulatory-system`.

| Asana destination | Picked up by |
|---|---|
| SJS Regulatory Management (gid `1214660807386611`) | `regulatory-manager` (umbrella) |
| SJS Reportable Events (gid `1214660834583706`) | `adverse-event-and-recall-reporter` |
| IL / Claims / Label sections of SJS Regulatory Management | `claims-il-and-label-keeper` |

### PLM (artifact destination, not Asana queue)

| Destination | Owner |
|---|---|
| `public.*` tables — products, batches, vendors, components, purchase_orders, vendor_invoices, etc. | `plm-assistant` (sole writer) |
| Sync-back comment on the originating Asana PD task | bridge that staged the PLM write |

Two of the four bridges (`asana-plm-bridge`, `outlook-plm-bridge`) write to PLM. They always stage through `plm-assistant`; they never call `execute_sql` for writes.

---

## Per-bridge queue routing

How each bridge classifies and posts. Each bridge owns its label set; the contract here only maps label → queue.

### `outlook-asana-bridge`

| Signal label | Queue destination |
|---|---|
| `pd` | PD queue (project named by SKU; Formula Tracker if stage-gate signal) |
| `ops` | Ops queue per signal subtype (vendor / PO → Purchasing; inventory → Inventory; forecast → S&OP; freight → Logistics; DTC order → OC3PL). **A PO and a freight leg on the same shipment is a both-case, not a choice** — see below. |
| `quality` | Quality queue (SJS Quality Management, plus CAPA or Complaint Log if signal subtype is clear) |
| `regulatory` | Regulatory queue (SJS Regulatory Management; SJS Reportable Events if SAE / recall) |
| `margin` | No queue. Stage the signal in PLM via cross-flag to `outlook-plm-bridge`; margin skills read PLM live. |
| `intel` | No queue. Surface to operator; intel skills read external sources, not bridge queues. |
| `founder` | No queue. Briefing skill reads upstream rollups live. |
| `plm` | Cross-flag to `outlook-plm-bridge`. |

### `fireflies-asana-bridge`

Same label set and queue routing as `outlook-asana-bridge`. Source is a transcript instead of an email; everything downstream is the same.

### `asana-plm-bridge`

Primary destination is PLM via `plm-assistant`. Sync-back comments post to the originating Asana PD task. Cross-system signal (Quality / Regulatory / Margin) that the bridge extracts while syncing follows the same queue map above — the bridge posts to the target Asana queue rather than trying to call the destination skill.

### `outlook-plm-bridge`

Same as `asana-plm-bridge` for the PLM writes (Flows A–H per its SKILL.md). Flow I (Ramp invoices) stages `vendor_invoices` rows and hands to `purchasing-manager` Job 9 via the AC Brands Purchasing queue. Cross-system signal follows the queue map.

---

## What this rule replaces

The four bridge SKILL.md files previously enumerated destination skills in "Connection points" / "Routes to" sections — every margin sub-skill, both intel skills, the founder briefing, every quality and regulatory destination by name. Most of those weren't reciprocated by the destination skills, and the bridge descriptions hit the 1024-char cap trying to claim them all.

The queue contract makes the asymmetry go away: bridges write to Asana / PLM; routers and skills pick up. New skills join the system by subscribing to an existing queue, not by getting added to every bridge's SKILL.md.

---

## How sub-system routers reference this

Each of `sjs-pd-system`, `sjs-ops-system`, `sjs-quality-system`, `sjs-regulatory-system` carries a short **Bridge intake** section that points here. The routers don't describe bridge logic — they describe which queues they pick up from. The bridges don't describe destinations — they describe what queues they write to. The contract is the only place both sides meet.

---

## Out of scope

- Skill-internal queue mechanics (custom field flags, sub-skill task templates) — those live in each skill's own SKILL.md and references. **Sections and state → section maps are not skill-internal** and live in `asana_task_contract.md` Phase 4 plus `queue_registry.md`; this line used to send readers to the skills, which is part of why no canonical map existed.
- Cross-system handoffs that don't pass through a bridge — e.g., Quality → PD via `[Reformulation Required]` flag — those live in the relevant router's "Cross-system handshakes" section.
- Non-Asana, non-PLM destinations (SharePoint artifact archive, branded HTML dashboards on `acb-thelanding`) — those are owned by reporter and archive skills.
