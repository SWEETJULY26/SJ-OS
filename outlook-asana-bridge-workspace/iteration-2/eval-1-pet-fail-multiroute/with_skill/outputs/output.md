# Outlook → Asana Bridge — "Allure Labs flagged a PET fail on Castaway Cream — log it"

## Email search result

I searched Outlook (Inbox + Sent Items, no folder restriction) for this. Two passes:

- `query: "Castaway Cream PET"` — no email matching a PET fail. Results were unrelated (portfolio digests, Element Packaging color samples, a Milinyc "PET Reports" email confirming *passing* preservative system results — not Castaway, not a fail — and older Castaway Cream regulatory/shipping threads).
- `sender: allurelabs.com` — 25 results, none mentioning PET testing or a failing lab result. Allure Labs' actual traffic with us is unit cartons, inventory reports, POs, and tube/shipping requests — they're a 3PL/fulfillment partner, not a testing lab.

**I could not find a real email matching this request.** One more thing worth flagging: PET (preservative efficacy) testing on Castaway Cream in our system runs through **AMR Labs** (Jaclene@AMRLabs.com / Jasmine@AMRLabs.com), not Allure Labs (priyanka@allurelabs.com) — confirmed against both the vendor table and the Formula Tracker task history ("New Castaway Cream (AMR Labs) PET Testing Begins at AMR Labs," "Perform PET Testing for Toner, Cleanser, Irie Power Oil, Castaway Cream..."). Allure Labs is a fulfillment/3PL vendor. Before I log anything, check whether the sender name got crossed — if the fail actually came from AMR Labs, say so and I'll re-run this against the real thread.

Proceeding below with the classification and confirmation preview built from the scenario as described, so this is ready to push the moment the real email (or a correction) surfaces.

---

## Classification

**Labels:** `[quality, pd, plm]`

| Label | Why |
|---|---|
| `quality` | "PET fail" is a failing lab result signal — explicit trigger in the quality signal table |
| `pd` | Castaway Cream is an active PD product with an open Formula Tracker / stability history |
| `plm` | Failing test result — PLM product test fields need the record; cross-flag to `outlook-plm-bridge` per the PLM-bound attachment/signal rule |

**Priority order:** `quality` > `regulatory` > `ops` > `pd` > `margin` > `intel` > `founder` → **quality wins the parent slot.**

## Proposed actions (fan-out, cross-referenced)

**1. Parent — Quality (quality-lab-coordinator)**
Open an OOS/OOT investigation in SJS Quality Management for the Castaway Cream PET fail.
- Title: `PET Fail — Castaway Cream (source: [lab] — confirm sender)`
- Description: `Source: Email from [sender — pending confirmation], [date] — "[Subject]". PET (preservative efficacy) failure reported on Castaway Cream. Cross-refs: PLM Bridge flag (below), PD task comment (below).`
- Note in the task: existing related context already in Asana — `[Batch Lifecycle] Castaway Cream — 875502` (batch-lifecycle-tracker) and the open `Perform PET Testing for Toner, Cleanser, Irie Power Oil, Castaway Cream, Soursop Vit C, and Good Youth Serum to Support Shelf-Life Extension` task — worth linking if this fail relates to either.

**2. Secondary — PD**
Comment on the Castaway Cream PD task with the fail notice and a pointer to the Quality parent action.
- `📧 From: [sender — pending confirmation] ([date]) — PET fail reported. Quality investigation opened: [parent task link]. Formula Tracker stage impact TBD pending root cause.`

**3. Secondary — PLM cross-flag**
`⚙️ PLM Bridge: PET fail result on Castaway Cream — route via outlook-plm-bridge to update product test fields (failing result, date, lab). Cross-ref: Quality parent [link], PD comment [link].`

All three reference each other per the multi-route cross-referencing rule.

## Confirmation preview (per `asana-pd-manager/references/confirmation-protocol.md`) — STOPPING HERE, no writes made

```
Proposed Asana actions for: "Allure Labs flagged a PET fail on Castaway Cream"

1. CREATE TASK — SJS Quality Management (parent)
   Title: PET Fail — Castaway Cream (source pending confirmation)
   Description: Source: Email — sender/date to be confirmed once located.
                PET failure reported on Castaway Cream.
                Cross-refs: PD task comment, PLM Bridge flag (below).
   Related context to link if confirmed: [Batch Lifecycle] Castaway Cream — 875502

2. COMMENT — PD task "Castaway Cream"
   📧 From: [pending] ([date]) — PET fail reported.
   Quality investigation opened: [parent task link].

3. PLM CROSS-FLAG (for outlook-plm-bridge, not written here)
   ⚙️ PLM Bridge: PET fail result on Castaway Cream — update product test
   fields. Cross-ref: Quality parent, PD comment.

⚠️ Before pushing: confirm the actual source email — Allure Labs is a
fulfillment/3PL vendor in our records, not the PET testing lab (that's
AMR Labs). No matching email was found in Outlook under either sender.

Which should I push? (say "all", list numbers, or "skip")
```

No Asana, PLM, or Supabase writes were made. This stops at the confirmation-preview step per instructions.
