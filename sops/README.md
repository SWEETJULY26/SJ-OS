# SOPs

Sweet July Skin's standard operating procedures, as markdown. This directory is the source of truth — not SharePoint, not a database row.

Each file is one SOP: `<sop-id>-<slug>.md`, with YAML frontmatter (`sop_id`, `title`, `revision`, `status`, `owner`, `effective_date`, `next_review_date`) followed by the procedure body in plain markdown.

Skills reference these files directly by `sop_id` when they need to walk a procedure, so an edit here takes effect everywhere that SOP is used without touching the skill itself. Formatted output (Word, PDF, a landing page) gets generated from the file on request — the markdown doesn't change to match the output, the output is rendered from the markdown.

| SOP ID | Title | Status |
|---|---|---|
| SKN-OPS-001 | Corrective and Preventive Action (CAPA) Procedure | ratified — overdue for annual review |
| SKN-OPS-002 | Serious Adverse Event (SAE) Reporting and Management | ratified — overdue for annual review |
| SKN-OPS-003 | Product Recall Procedure | ratified — overdue for annual review |
| SKN-OPS-004 | Customer Complaint Handling | ratified |
| SKN-OPS-005 | Non-Conformance Report (NCR) Procedure | ratified |
| SKN-OPS-006 | Lab Quality Procedure | ratified |
| SKN-OPS-007 | Batch Lifecycle Procedure | ratified |
| SKN-OPS-008 | IL / Claims / Label Procedure | ratified (Rev.2) |
| SKN-OPS-009 | Reportable Events Procedure | ratified |
| SKN-OPS-010 | Supplier Onboarding Procedure | draft |
