Subject: Sweet July Skin AIOS — system overview + a maintenance/validation ask

Ash,

Attached is a visual map of what I've built so far — the skill system running PD, Ops, Quality, and Regulatory for Sweet July Skin, plus the tech stack underneath it and who owns what on our side.

Quick orientation on the diagram: Claude Code runs the whole thing, with connectors into Asana, Outlook, Fireflies, our PLM database, and Shopify. On top of that sit four systems — PD, Ops, Quality, Regulatory — each with a router skill and a handful of working skills underneath it. Cross-system bridges move data between them (meeting notes into task queues, PLM syncs, that kind of thing).

Here's where I need Exogix's help. I built this myself over the past few months, and I'm not fully confident everything is wired correctly or holding up under real use. Two things:

1. Validation — I'd like a second set of eyes to go through the system and confirm it's actually working the way it's supposed to: routing logic, data flowing to the right place, no silent failures.
2. Ongoing maintenance — I don't have the bandwidth to keep this running solo as it grows. I'm looking for regular support to catch issues, keep connectors healthy, and help me extend it as we add more skills.

Happy to walk you through it live or send more detail on any piece. Let me know what you'd need from me to scope this.

Alvin
