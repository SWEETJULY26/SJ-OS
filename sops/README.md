# SOPs

Sweet July Skin's standard operating procedures, as markdown. This directory is the source of truth — not SharePoint, not a database row.

Each file is one SOP: `<sop-id>-<slug>.md`, with YAML frontmatter (`sop_id`, `title`, `revision`, `status`, `owner`, `effective_date`, `next_review_date`) followed by the procedure body in plain markdown.

Skills reference these files directly by `sop_id` when they need to walk a procedure, so an edit here takes effect everywhere that SOP is used without touching the skill itself. Formatted output (Word, PDF, a landing page) gets generated from the file on request — the markdown doesn't change to match the output, the output is rendered from the markdown.

| SOP ID | Title | Status |
|---|---|---|
| SKN-OPS-010 | Supplier Onboarding Procedure | draft |
