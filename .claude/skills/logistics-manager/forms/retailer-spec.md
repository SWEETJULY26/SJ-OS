# Retailer compliance spec — staged write

Use this form when staging a write to `retailer_compliance_specs` — either a
new retailer (Sephora, future channels) or a routing-guide rev for an existing
one (Ulta, Amazon).

Source PDFs live in SharePoint under the logistics folder. The structured rule
extract lives in PLM. Same separation pattern as the quality SOP library.

---

## Form fields

```yaml
retailer_name: <Ulta|Amazon|Sephora|other>
version: <semver-style or retailer's version label, e.g., "v3.2-2026-Q2">
prior_version: <prior row's version, null if new retailer>
last_updated: <YYYY-MM-DD>
effective_date: <YYYY-MM-DD — when this version becomes enforceable>
sharepoint_pdf_path: <full path to the source PDF in SharePoint>

# --- Operational fields ---
lead_time_days: <int>
asn_format: <EDI_856|portal|both>
asn_segments_required: <jsonb array of segment names — only for EDI>

pallet_spec:
  pallet_dimensions: <e.g., "48x40 GMA">
  max_height_in: <int>
  max_weight_lb: <int>
  mixed_sku_allowed: <true|false>
  mixed_sku_rule: <plain language, null if not allowed>
  stretch_wrap_min_wraps: <int>

label_spec:
  per_pallet: <plain language>
  per_case: <plain language>
  barcode_format: <e.g., GS1-128 SSCC>
label_placement_rule:
  pallet: <plain language placement detail>
  case: <plain language placement detail>

hazmat_rule: <plain language — what's accepted, what's flagged>
overage_tolerance_pct: <decimal — 0.0 = exact match required>
underage_tolerance_pct: <decimal>

# --- Diff summary ---
changed_fields: <array of field names changed from prior_version>
change_summary: <free text — one paragraph explaining what's different>

# --- Audit ---
source_email_id: <Outlook message ID if forwarded, null if pulled directly>
notes: <free text>
```

---

## Diff parsing rule

When a new routing guide PDF arrives:

1. Pull the prior `retailer_compliance_specs` row for the same retailer
2. Parse the new PDF section-by-section
3. Compare against prior fields; build the `changed_fields` array
4. Write `change_summary` in plain language — what changed and why it matters
5. Stage the YAML
6. Surface to Operations with the diff highlighted

If the new version drops a requirement, note it. If it tightens a tolerance
or adds a new label spec, that's the kind of change that feeds back into ASN
drafts immediately.

---

## Confirmation flow

1. Stage the YAML on the Asana parent task in `Compliance Specs` section
2. Upload the source PDF to SharePoint under the logistics folder, recording
   the path
3. Surface to Operations with the retailer, new version, and change summary
4. On approval, plm-assistant inserts a new row in `retailer_compliance_specs`
   (history is preserved by versioning, not overwriting)
5. Future ASN drafts and routing requests pull the latest version row
6. If `effective_date` is in the future, the prior version row stays the
   current default until the effective date passes

---

## Cross-reference

ASN drafts and routing requests both reference the latest active row of
`retailer_compliance_specs` for the matching retailer. The compliance check
in `forms/asn-draft.md` runs against `version` so any rev triggers an
automatic re-check on the next outbound shipment.
