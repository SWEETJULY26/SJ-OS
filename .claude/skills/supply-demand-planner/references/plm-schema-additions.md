# PLM schema additions

Three structural changes plus a settings seed went into the Sweet July PLM
(Supabase project `ujkabbffvhpewpbttmmy`) for v3 of supply-demand-planner.
All applied via plm-assistant migrations on 2026-04-27.

## 1. `forecast_lines.channel` column

Added a nullable `channel text` column to `forecast_lines`. NULL means
all-channel (legacy / consolidated forecast). Specific values: `dtc`, `ubm`,
`amazon`.

```sql
ALTER TABLE forecast_lines ADD COLUMN channel text NULL;

-- Partial unique index allows one row per (plan, product, channel)
-- including the legacy NULL-channel row for backward compatibility
CREATE UNIQUE INDEX forecast_lines_plan_product_channel_uniq
  ON forecast_lines (plan_id, product_id, COALESCE(channel, ''));

CREATE INDEX forecast_lines_channel_idx
  ON forecast_lines (channel) WHERE channel IS NOT NULL;
```

Notes:
- Legacy rows pre-migration have `channel = NULL`. The skill treats NULL as
  "all-channel" but writes new rows with explicit channel.
- The unique index uses `COALESCE` to allow exactly one NULL-channel row per
  (plan, product) plus one row per explicit channel.

## 2. `inventory_targets` table

New table. Per SKU × channel safety-stock and reorder targets.

```sql
CREATE TABLE inventory_targets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  channel text NULL,
  safety_stock_days integer,
  reorder_point numeric,
  reorder_qty numeric,
  lead_time_days_override integer,
  target_dsi numeric,
  source text NOT NULL DEFAULT 'plan' CHECK (source IN ('plan', 'manual')),
  plan_id uuid REFERENCES forecast_plans(id),
  notes text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE INDEX inventory_targets_product_channel_idx
  ON inventory_targets (product_id, channel);
```

Plus an `updated_at` trigger to maintain modification timestamp:

```sql
CREATE TRIGGER inventory_targets_set_updated_at
  BEFORE UPDATE ON inventory_targets
  FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
```

RLS active for authenticated users (read + write):

```sql
ALTER TABLE inventory_targets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can read inventory_targets"
  ON inventory_targets FOR SELECT TO authenticated USING (true);

CREATE POLICY "Authenticated users can write inventory_targets"
  ON inventory_targets FOR ALL TO authenticated USING (true) WITH CHECK (true);
```

`source` distinguishes plan-driven targets (written by this skill) from manual
overrides. Manual overrides take precedence — the skill checks for an active
`source='manual'` row before writing a `source='plan'` row.

`plan_id` links the target to the forecast plan it was computed from. For
`source='manual'`, `plan_id` is NULL.

## 3. `component_forecast_entries` RLS

The table existed pre-migration, scaffolded but unused. Activated RLS so the
skill can write to it through plm-assistant.

```sql
ALTER TABLE component_forecast_entries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can read component_forecast_entries"
  ON component_forecast_entries FOR SELECT TO authenticated USING (true);

CREATE POLICY "Authenticated users can write component_forecast_entries"
  ON component_forecast_entries FOR ALL TO authenticated USING (true) WITH CHECK (true);
```

Used by the BOM explosion flow. See `component-explosion-flow.md` for the
paired-plan model that drives writes here.

## 4. Settings seed (sdp_* keys)

25 keys seeded. Tunable in PLM, not in the skill.

| Key | Default | Purpose |
|---|---|---|
| `sdp_brand_scope` | `sweet-july-skin` | Brand the skill operates on |
| `sdp_active_channels` | `["dtc","ubm","amazon"]` | Channels in scope |
| `sdp_run_cadence` | `monthly` | S&OP run frequency |
| `sdp_ubm_launch_date` | `2026-06-01` | UBM go-live |
| `sdp_auto_adjust_direct_comp_factor` | `-0.10` | Direct comp launch hit |
| `sdp_auto_adjust_direct_comp_days` | `90` | Direct comp window |
| `sdp_auto_adjust_indirect_comp_factor` | `-0.05` | Indirect comp launch hit |
| `sdp_auto_adjust_indirect_comp_days` | `60` | Indirect comp window |
| `sdp_auto_adjust_retail_above_factor` | `0.05` | Above-expectation benchmark |
| `sdp_auto_adjust_retail_above_days` | `90` | Retail above window |
| `sdp_auto_adjust_retail_below_factor` | `-0.10` | Below-expectation benchmark |
| `sdp_auto_adjust_retail_below_days` | `90` | Retail below window |
| `sdp_auto_adjust_vendor_transition_hold` | `true` | Hold flat during transition |
| `sdp_exception_variance_pct` | `0.20` | Variance threshold for exception |
| `sdp_exception_new_launch_days` | `90` | New-launch exception window |
| `sdp_exception_low_cover_days` | `60` | Days-of-cover exception threshold |
| `sdp_exception_vendor_transition_window_days` | `60` | Transition lookahead |
| `sdp_default_safety_stock_days_dtc` | `45` | DTC default safety stock |
| `sdp_default_safety_stock_days_ubm` | `60` | UBM default safety stock |
| `sdp_default_safety_stock_days_amazon` | `30` | Amazon default safety stock |
| `sdp_default_target_dsi_ubm` | `90` | UBM default target days-of-supply |
| `sdp_default_target_dsi_amazon` | `60` | Amazon default target days-of-supply |
| `sdp_filler_kdc_one_lead_time_days` | `70` | KDC-One default lead time |
| `sdp_filler_vegelabs_lead_time_days` | `60` | Vegelabs default lead time |
| `sdp_packaging_default_lead_time_days` | `105` | Default packaging lead time |

DTC doesn't have a default target DSI because DSI for DTC is governed by
fulfillment-day inventory, not retailer DSI.

## How the skill writes

Every write goes through plm-assistant with HITL. The skill drafts and stages;
Operations approves; plm-assistant executes the SQL.

Forecast updates → `forecast_lines` upsert keyed on (plan_id, product_id, channel).

Component explosions → `component_forecast_entries` via paired-plan pattern in
`component-explosion-flow.md`.

Target resets → `inventory_targets` upsert keyed on (product_id, channel,
plan_id, source). Manual overrides win.

Settings tuning → `settings` upsert. Surfaced in run summary header so changes
are auditable.

## What the skill does NOT touch

- `products` (read-only)
- `bills_of_materials` (read-only)
- `components` (read-only)
- `vendors` (read-only)
- `purchase_orders` (read-only — purchasing-manager owns writes)
- `batches` (read-only — outlook-plm-bridge / plm-assistant own writes)
- `channel_inventory` / `inventory_movements` (read-only — inventory-manager
  owns writes)
