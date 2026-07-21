# Complaint intake plan — Pava Toner, lot 25-03 (draft, not yet written to Asana)

## What came in

Customer reports her face turned red and itchy after using the Pava Toner, lot 25-03. She's asking for a refund.

**Missing: Invoice/Order Number.** The intake didn't include one, and I need it to pivot into fulfillment context (oc3pl-order-manager) and to fold this complaint into any future recall scoping tied to lot 25-03. Recommend sending this back-to-customer ask before or alongside first-response:

> "Thanks for flagging this — sorry to hear about the reaction. Can you send your order number so we can pull up your purchase and process the refund?"

## SAE keyword check

Scanned the description against the SKN-OPS-002 keyword list: hospitalization, ER, emergency room, anaphylaxis, swelling, blistering, scarring, infection, or any phrase suggesting medical intervention.

"Red and itchy" does not match any of those. No SAE trigger. This stays a standard complaint, not an SAE escalation. Worth asking the customer directly whether she sought any medical treatment — if the answer comes back yes, this gets re-triaged into the SKN-OPS-002 walk (Job 4) at that point, operator's call on severity.

## Recommended classification

| Field | Recommendation |
|---|---|
| Complaint Type | **Skin Reactions & Irritations** |
| Priority level | **Medium** — real reaction, not consistent with SAE keywords, but a reaction complaint on an active lot warrants attention |
| First Response Corrective Action | **Return** (refund, as she's requesting) — stacked with **Replace and no return** is the type default per the classification map, but she's explicitly asking for a refund, not a replacement, so recommend leading with **Return** |
| Product Name | Pava Toner |
| Product Batch Code | 25-03 |
| Product Sales Channel | *(not provided — confirm with customer or pull from order once Invoice/Order Number is in hand)* |

**Reasoning:** Skin Reactions & Irritations is the closest match for "face turned red and itchy" — it sits under allergic reaction / increased sensitivity in the field's option definition. The type default recommends "Replace and no return" so the customer isn't asked to return a product they reacted to, but she's asked for a refund outright — recommend honoring that and setting First Response Corrective Action to **Return**, not overriding her preference with the default.

## Batch / trend check — worth running before you approve

Per the trend thresholds in the classification reference: **Skin Reactions, single SKU: 2+ in 30 days → flag for batch + formula check, regardless of severity.** Before closing this out, I'd run a quick pull on lot 25-03 and on Pava Toner generally for any other Skin Reactions complaints in the last 30 days. If this is a second one, it crosses that threshold and I'd draft a CAPA brief for capa-coordinator rather than treat this as an isolated case. Flagging this as a follow-up, not doing it here since you asked me not to write/query yet — say the word and I'll pull it.

## Staged Asana writes (on your approval — nothing committed yet)

1. Set custom fields on the task: Complaint Type = Skin Reactions & Irritations; Priority level = Medium; First Response Corrective Action = Return; Product Name = Pava Toner; Product Batch Code = 25-03.
2. Set `Status = Actioning`.
3. Move task from New feedback → Actioning section.
4. Post a comment logging this action plan (classification + reasoning + first-response) to the task.
5. Send the back-to-customer ask for the missing Invoice/Order Number (separate from the Asana write — this is the actual customer-facing reply).

## What I need from you to proceed

- Approve or edit the classification and first-response action above.
- Confirm you want the refund-only response (Return) rather than stacking a replacement offer.
- Say if you want the lot 25-03 / Pava Toner trend check run now before this gets actioned.

Nothing above has been written to Asana. This is the plan for your sign-off.
