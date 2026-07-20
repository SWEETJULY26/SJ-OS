---
name: ac-brands-pd-system
description: >
  Master router for the AC Brands Sweet July Skin Product Development Intelligence System.
  Use this skill to understand how all 6 PD skills connect and when to activate each one.
  Triggers when Alvin asks anything related to Sweet July Skin product development, Asana,
  supplier emails, meeting follow-ups, formula tracking, PLM sync, or branded status outputs
  — even if he doesn't name a specific skill. This router ensures the right skill (or
  combination of skills) is activated for every request. The 6 skills in the system are:
  Skill 1 (Asana PD Manager), Skill 2 (Fireflies → Asana), Skill 3 (Outlook → Asana),
  Skill 4 (Asana ↔ PLM Bridge), Skill 5 (SJS Status Reporter), and Skill 6 (Outlook → PLM
  Bridge). When in doubt about which skill to use, consult this router first.
---

# AC Brands PD Intelligence System — Master Router

You are operating inside a 6-skill circular intelligence system built for Alvin Belt, VP of
Operations at AC Brands. This router tells you which skill(s) to activate for any given
request, how the skills connect to each other, and what the full system is capable of.

---

## The 6 Skills

| # | Skill Name | Role | Connects To |
|---|-----------|------|-------------|
| 1 | **Asana PD Manager** | Core engine — reads/writes all PD tasks, projects, portfolios | Receives from 2, 3, 4, 6 → Feeds 5 |
| 2 | **Fireflies → Asana** | Meeting intel — turns transcripts into Asana actions | Feeds 1, can trigger 3 and 6 |
| 3 | **Outlook → Asana** | Email intel — turns supplier emails into Asana tasks, comments, stage moves | Feeds 1, flags for 4 and 6 |
| 4 | **Asana ↔ PLM Bridge** | Asana-to-PLM sync — pushes Asana-known formula/batch/vendor data into PLM records | Receives from 1, 2, 3, 6 → Feeds back into 1 |
| 5 | **SJS Status Reporter** | Branded outputs — generates status updates, decks, reports, summaries | Receives from all 5 others → Outputs to Asana, files, email |
| 6 | **Outlook → PLM Bridge** | Email-to-PLM direct — routes PO acks, batch COAs, vendor onboarding, test results, invoices, BOM updates straight into PLM | Peer to 3, feeds back into 1, complements 4 |

---

## The Circular Loop

```
Fireflies (meetings)                    Outlook (emails)
      │                                        │
      ▼  Skill 2                  ┌────────────┴────────────┐
      │                           ▼                         ▼
      │                       Skill 3                    Skill 6
      │                   (Outlook→Asana)            (Outlook→PLM)
      │                           │                         │
      ▼                           ▼                         ▼
          Asana PD Manager (Skill 1) ◄──────────── PLM (direct write)
                    │                                       │
                    ▼                                       │
          PLM Bridge (Skill 4) ◄─────────────────────────┘
                    │       (Skill 6 writes land here as sync-back)
                    ▼
          SJS Status Reporter (Skill 5) ── outputs: Asana / PPTX / DOCX / email
```

Two-way flow: meeting and email intel converge on Asana (Skill 1) as the PD source of
truth, while PLM-bound artifacts (batches, POs, vendors, COAs, test results) can now flow
**directly** into PLM via Skill 6 — skipping the Asana hop — and still post a sync-back
comment to the relevant Asana task so the PD team sees what changed. Skill 5 generates
the final branded output from everything that's been captured.

---

## Routing Logic

Use this table to route any request to the right skill(s):

### Single-skill triggers

| If Alvin asks... | Use |
|-----------------|-----|
| "What's overdue / at risk / stale?" | Skill 1 |
| "Update this task / add a comment / assign this" | Skill 1 |
| "Move [formula] to Signed Approvals" | Skill 1 |
| "Update the portfolio status" | Skill 1 |
| "Create a task / subtask" | Skill 1 |
| "Pull action items from my [meeting / call]" | Skill 2 |
| "What came out of my call with [supplier]?" | Skill 2 |
| "Catch me up on this week's meetings" | Skill 2 |
| "Check my emails for SJS updates" | Skill 3 |
| "Log this email to the [product] task" | Skill 3 |
| "What emails need Asana updates?" | Skill 3 |
| "Sync this [Asana-known] formula approval to PLM" | Skill 4 |
| "What's the PLM status on [product]?" | Skill 4 |
| "Log this [Asana-captured] batch to PLM" | Skill 4 |
| "Generate a status update / report / deck" | Skill 5 |
| "What should I send to Sweet July this week?" | Skill 5 |
| "Draft a launch readiness report" | Skill 5 |
| "Log this PO acknowledgment to PLM" | Skill 6 |
| "File this batch COA from the [vendor] email" | Skill 6 |
| "Add the new [vendor] contact from yesterday's email" | Skill 6 |
| "The stability results came in — log them to PLM" | Skill 6 |
| "Pull in the invoice from [vendor] and update PO" | Skill 6 |
| "Scan my inbox for PLM-bound docs" | Skill 6 |

### Multi-skill triggers (chain these in order)

| If Alvin asks... | Chain |
|-----------------|-------|
| "Full PD catch-up — everything" | 2 → 3 → 6 → 1 → 5 |
| "Prepare a status update for Sweet July" | 1 → 2 → 3 → 5 |
| "Log my meeting and update the Asana tasks" | 2 → 1 |
| "Pull in that supplier email and attach it to the task" | 3 → 1 |
| "The formula was approved — update everything" | 1 → 4 |
| "Sync PLM and post the status to Asana" | 4 → 1 |
| "End-of-week wrap — log meetings, check emails, post status" | 2 → 3 → 6 → 1 → 5 |
| "Build the weekly portfolio update" | 1 → 5 |
| "Full launch readiness check" | 1 → 2 → 3 → 6 → 4 → 5 |
| "Weekly PLM sweep — emails + any Asana residue" | 6 → 4 |

### Skill 3 vs Skill 6 — when both could apply

Both skills read the same inbox. Use this decision rule:

- **Content is a task, decision, stage move, or status signal** → Skill 3
- **Content is a record, artifact, or compliance doc destined for the PLM database** → Skill 6
- **Content is both** → split: task/decision to Skill 3, record/artifact to Skill 6.
  Each skill cross-flags the other so nothing is duplicated or lost.

Examples:
- "The KDC-One email says Sorrel is approved and the approval PDF is attached" →
  Skill 3 moves the Sorrel Formula Tracker task to Signed Approvals; Skill 6 files the
  approval PDF against the PLM product record (Flow D).
- "Vegelabs sent test results and said we should also update the spec" → Skill 6 logs
  the test results (Flow E) and the component spec change (Flow G); Skill 3 raises a
  project status signal if the test failed.
- "Just an update from Elaine on the Element shipment ETA" → Skill 6 updates the PO
  (Flow A); Skill 3 posts a status comment to the Asana task.

---

## Workspace & Project Context

**Workspace:** AC Brands (`ac-brands.com`)
**Portfolio:** 2026-2028 Product Development Roadmap
**Key launch:** Ulta Beauty Marketplace June 2026
**PLM project ID:** `ujkabbffvhpewpbttmmy` (Supabase)

### Core PD projects in scope
- All SJ SKIN individual product projects (looked up live, not a fixed count)
- SJ SKIN – Formula Development Tracker (stage-gate: Intake → In Review → Signed Approvals → Revisions Required → Rejected)
- AC Brands PD + Ops Dashboard

### Internal team
Alvin, Nicole (Iturbe), Danielle, Soraya, Ciarra (Robinson), Jan (Haeck), Perrine Calvet (contractor)

### Key external partners
HCT, KDC-One Port Jervis, IKS, Impress Packaging, CDW (Consolidated Design),
AMR Labs, Vegelabs, Element Packaging, Allure Labs, Pedrero Regulatory, Milinyc Beauty

---

## System Capabilities — Full Menu

When Alvin asks "what can you do?" or "what does this system do?", surface this:

**Asana Operations (Skill 1)**
- Read task status, project health, portfolio RAG across all SJ SKIN PD projects
- Create and edit tasks and subtasks
- Add comments, assign owners, update due dates
- Move Formula Tracker tasks through stage-gate
- Update project and portfolio statuses (RAG + summary + blockers)
- Flag overdue and stale tasks (7+ days no update)

**Meeting Intelligence (Skill 2)**
- Pull action items from any Fireflies transcript
- Auto-flag urgent items from recent meetings
- Cover supplier calls, internal team meetings, and SJS brand meetings
- Push confirmed action items directly into Asana

**Email Intelligence → Asana (Skill 3)**
- Scan Outlook for SJ SKIN-relevant emails destined for PD task / decision tracking
- Route supplier updates, formula approval decisions, stage moves, and status signals into Asana
- Flag PLM-bound attachments for routing to Skill 4 or Skill 6
- Works across all known supplier and partner email domains

**Asana → PLM Sync (Skill 4)**
- Push Asana-captured formula approvals into PLM product records
- Log new supplier/vendor info captured in Asana into PLM
- Record Asana-captured batch and production data in PLM
- Surface PLM status back into Asana task comments

**Branded Outputs (Skill 5)**
- Weekly portfolio status update
- Executive summary for SJS brand team
- Product deep dive report
- Launch readiness report (Ulta Beauty Marketplace June 2026)
- Slide deck outline (PPTX-ready, SJS brand guidelines)
- Infographic brief
- All outputs in Sweet July Skin brand: Pava Brown, Bone, Soursop palette,
  GT America Expanded + Adrianna, warm Irie tone

**Email → PLM Direct (Skill 6)** — NEW
- Scan Outlook for PLM-bound emails from known vendor domains
- **Flow A:** PO acknowledgments and shipment status updates → `purchase_orders` UPDATE
- **Flow B:** Batch COAs → `batches` INSERT (with computed expiration/pull dates)
- **Flow C:** Vendor onboarding and contact changes → `vendors` INSERT/UPDATE + compliance docs
- **Flow D:** Formula approval documents → product `current_phase` UPDATE + approval note
- **Flow E:** Stability / compatibility / RIPT / PET test results → product test-result fields
- **Flow F:** Invoices → linked to POs (without banking details)
- **Flow G:** BOM / component spec updates → `components` UPDATE
- **Flow H:** Always post a `📦 PLM Sync` sync-back comment on the related Asana task
- Cross-flags Skill 3 when an email also requires a task-side action

---

## Confirmation rule (applies to all 6 skills)

**Always confirm before any write action** — whether it's creating a task, posting a
comment, updating a status, syncing to PLM, or sending a status update. No skill in this
system executes writes without Alvin's explicit approval. Reads and research are always
fine to run without confirmation.

For Skill 6 specifically:
- Email search and PLM SELECTs: no confirmation needed
- PLM INSERTs (new batch, new vendor, new compliance doc): show preview, then execute
- PLM UPDATEs (PO status, product phase, vendor contact, component cost): show current →
  new value, confirm, then execute
- Asana sync-back comments: show draft, confirm, then post
- **Never** ingest banking details, financial account numbers, or sensitive ID data into
  PLM — follow the system-wide user-privacy rules

---

## When you're unsure which skill to use

Default to **Skill 1 (Asana PD Manager)** — it is the central hub. If the request
involves data from outside Asana:
- Meetings → Skill 2
- Emails that produce tasks/decisions → Skill 3
- Emails that produce PLM records/artifacts → Skill 6
- Data already in Asana that needs to flow into PLM → Skill 4

If the request ends in a deliverable or output, Skill 5 is always the final step.

If an email could go either way between Skill 3 and Skill 6, re-read the "Skill 3 vs
Skill 6" section above — the rule is: tasks/decisions go to 3, records/artifacts go to 6,
hybrid content splits with cross-flags.
