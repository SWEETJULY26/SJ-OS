# AIS-OS Intake

This is the source-of-truth file for your AIOS. Fill it in by typing, voice-pasting (Wispr Flow / OS dictation), or running `/onboard` for a guided conversation. Whichever mode, this file is what `/onboard` reads to scaffold your Day-1 setup.

**Hard cap: 7 questions.** Each answerable in under 60 seconds. Don't overthink — you can edit and re-run `/onboard` any time.

---

## Q1 — Who are you, what do you sell, who do you sell it to?

Identity, offer, ICP. One paragraph each is fine.

```
I'm Alvin, running Operations for AC Brands, the company behind Sweet July — Ayesha Curry's lifestyle brand — and its skincare line, Sweet July Skin. Sweet July Skin sells Caribbean/Jamaican-rooted skincare ("modern formulas, ancient wisdom") direct-to-consumer via sweetjuly.com and through retail partners like Sephora, Ulta, and Whole Foods. This AIOS is meant to become the operating system for the brand — starting as my tool for running day-to-day ops, but built so the knowledge and process are documented well enough to hand off (succession planning), not just personal productivity.
```

---

## Q2 — Paste 1-2 things you've written recently. Don't edit them.

An email, a LinkedIn post, a DM, a doc — anything that sounds like you when you're not trying. **Paste verbatim.** Do not type these mid-conversation with Claude — chat-shaped samples are worse than no samples (voice contamination).

```
Hi Brian,

Sounds good! Understood.

I will inform the team and lab.

Best,
Alvin
```

```
Purpose: Align demand, supply, inventory, and cash

Agenda:
  1.  Demand outlook (sales, promos)
  2.  Supply & capacity review
  3.  Inventory position & risks
  4.  Financial implications
  5.  Decisions & approvals
```

---

## Q3 — What are your 2-3 biggest priorities for the next 90 days?

Quarterly priorities. Not yearly aspirations. Things that, if not done by July, would make you say "I wasted Q2."

```
1. Hire a new Ops specialist and a Product Development specialist.
2. Build out the AI-assisted skill and agent system to support the execution layer of the brand's operating tasks — Asana/task management, order management, inventory management, and the rest of the ops stack.
```

---

## Q4 — Where does revenue actually land, and where is it tracked?

Multiple answers OK. Stripe? Skool? GoHighLevel? QuickBooks? A spreadsheet?

```
[Your answer here]
```

---

## Q5 — Where do you talk to customers, your team, and the outside world day-to-day?

Email (which one — Gmail / Outlook)? Slack? Teams? DMs (Skool / Discord / iMessage)? Phone?

```
[Your answer here]
```

---

## Q6 — Where do meeting recordings, notes, and important docs live?

Granola? Otter? Fireflies? Google Drive? Notion? Dropbox? A folder on your desktop you keep meaning to organize?

```
[Your answer here]
```

---

## Q7 — What's the one task that eats your week, and where do you currently track work?

The single biggest time-suck or recurring drudgery. Plus where tasks/projects live (ClickUp / Asana / Linear / Notion / a notebook).

```
[Your answer here]
```

---

When this file is filled, run `/onboard` (or re-run it) and the wizard will scaffold your Day-1 file set: `context/`, `references/voice.md`, populated `connections.md`, and a filled `CLAUDE.md`.
