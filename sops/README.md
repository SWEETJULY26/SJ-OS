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
| SKN-OPS-010 | Supplier Onboarding Procedure | ratified |
| SKN-OPS-011 | Formula Development Stage-Gate & IL Review Gate Procedure | ratified |
| SKN-OPS-012 | PD Readiness → PO Request Handoff Procedure | ratified |
| SKN-OPS-013 | Purchase Order Lifecycle Procedure (Draft to Close) | ratified |
| SKN-OPS-014 | Receipt Discrepancy Investigation Procedure | ratified |
| SKN-OPS-015 | Vendor Invoice Cost Classification & Routing Procedure | ratified |
| SKN-OPS-016 | Receiving & Batch Creation Procedure | ratified |
| SKN-OPS-017 | Inventory Adjustment, Write-Off, and Return Disposition Procedure | ratified |
| SKN-OPS-018 | Monthly S&OP Run Procedure | ratified |
| SKN-OPS-019 | Inbound Shipment Receipt & Fault-Attribution Procedure | ratified |
| SKN-OPS-020 | Retailer Outbound ASN & Routing Compliance Procedure | ratified |
| SKN-OPS-021 | International Outbound DTC Compliance Procedure | ratified |
| SKN-OPS-022 | DTC Order Exception Routing Procedure | ratified |
| SKN-OPS-023 | Pre-Ship OOS Hold Sync Procedure | ratified |
