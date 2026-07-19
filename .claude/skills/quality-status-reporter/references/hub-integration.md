# Hub Integration — `acb-thelanding`

How quality-status-reporter integrates with the AC Brands landing hub. Repo at `/Users/alvinbelt/Downloads/acb-thelanding/`, deploys to `acb-thelanding.netlify.app` via GitHub `SWEETJULY26/acb-thelanding`.

---

## 1. Nav placement — `data/links.json`

The hub is data-driven via `data/links.json`. Each function area has `sections` with `tools`. Add a new section to `product-development`:

```json
{
  "id": "product-development",
  // ... existing fields ...
  "sections": [
    { "label": "Portfolio & Status", ... },
    { "label": "PLM", ... },
    { "label": "Margin & Economics", ... },
    {
      "label": "Quality Management",
      "tools": [
        {
          "title": "Quality Dashboard",
          "description": "Live System B rollup — CAPAs, lab findings, batch state, complaints, SOPs, QoS metrics.",
          "url": "quality-dashboard.html",
          "status": "live"
        }
      ]
    }
  ]
}
```

Status values seen in the codebase: `live`, `wip`, `planned`. Use `live` once the page deploys and works.

If additional quality tools are added later (e.g., a separate SOP browser page), they go as additional `tools` entries in this same Quality Management section. No need to split into multiple sections.

---

## 2. Page chrome integration

Per the project memory:

- Pages must reuse `Hub.renderHeader` / `renderNav` / `renderFooter` so chrome matches the rest of the hub.
- After injecting `renderShell` content, call `Hub.bindNav()` and `Hub.bindEditMode()` — without that, the Functions ▾ dropdown won't open.

The `assets/js/hub.js` initializer reads the `data-page` attribute on `#page-root` and applies chrome routing. The page module (`assets/js/quality-dashboard.js`) is responsible for injecting the shared header partial and binding the nav.

### Header partial pattern

Existing pages load `assets/includes/site-header.html` via fetch, inject into a header container, then call `Hub.bindNav()`:

```javascript
async injectSharedHeader() {
  const res = await fetch('assets/includes/site-header.html', { cache: 'no-store' });
  const html = await res.text();
  document.body.insertAdjacentHTML('afterbegin', html);
  if (window.Hub && window.Hub.bindNav) window.Hub.bindNav();
  if (window.Hub && window.Hub.bindEditMode) window.Hub.bindEditMode();
},
```

Mirror this pattern in `quality-dashboard.js`. Header injection happens once at `init` before content render.

---

## 3. Files to write

| File | Purpose | Created on |
|---|---|---|
| `quality-dashboard.html` | Page entry shell | Job 1 first run; rewritten on subsequent Job 1 |
| `assets/js/quality-dashboard.js` | Page module | Job 1 first run; rewritten on subsequent Job 1 |
| `assets/css/quality-dashboard.css` | Page styles | Job 1 first run; rewritten on subsequent Job 1 |
| `netlify/functions/sjs-quality-rollup.js` | Live data Function | Job 1 first run; rewritten when GIDs change |
| `data/links.json` | Hub registration | Job 1 first run only (one section addition); subsequent Job 1 runs leave alone |
| `data/quality-monthly-snapshot.json` | Monthly tab payload (static fallback) | Job 2 — rewritten on each monthly refresh |
| `data/quality-quarterly-snapshot.json` | Quarterly tab payload (static fallback) | Job 5 — rewritten on each quarterly refresh |

---

## 4. Deploy pattern

Per memory:

- **Never deploy directly to Netlify.** Always commit and push the GitHub repo; Netlify auto-deploys.
- **Commit and push to main** — no PRs, no feature branches unless asked.
- Confirm with operator before pushing.

Standard git flow from the skill:

```bash
cd /Users/alvinbelt/Downloads/acb-thelanding/
git status                     # confirm clean state before edits
# ... skill writes files ...
git add quality-dashboard.html assets/js/quality-dashboard.js assets/css/quality-dashboard.css netlify/functions/sjs-quality-rollup.js data/links.json
git status                     # show diff to operator
# OPERATOR APPROVES
git commit -m "Add quality-dashboard.html and supporting assets (v5.6 build)"
git push origin main
```

After push, Netlify's connected repo deploys automatically. Verify the deploy succeeded in the Netlify UI; if it fails, check the build log and adjust.

---

## 5. Memory rules to honor

| Rule | Source | How v5.7 honors |
|---|---|---|
| Pages must use shared header | `feedback_acb_hub_pages_chrome.md` | `quality-dashboard.js` injects `assets/includes/site-header.html` |
| Re-bind nav after shell | `feedback_acb_hub_bindnav_after_shell.md` | Call `Hub.bindNav()` and `Hub.bindEditMode()` after header injection |
| Asana references → live counts | `feedback_acb_hub_live_counts.md` | Live page calls Netlify Function on every load; never hardcoded counts |
| Asana live-sync function pattern | `feedback_acb_hub_asana_live_pattern.md` | sjs-quality-rollup follows project pagination + completed_since + PT timezone |
| Deploy via GitHub only | `feedback_acb_hub_deploy.md` | Commit and push; never use Netlify CLI direct deploy |
| Push to main | `feedback_github_workflow.md` | Direct to main, no PR |
| Production repo path | `reference_acb_hub_repo_path.md` | `/Users/alvinbelt/Downloads/acb-thelanding/` |

---

## 6. Edit mode

`assets/js/editor.js` self-initializes on every hub page. It owns Cmd/Ctrl+Shift+E and the `?edit=1` query param. The skill doesn't need to do anything special — including the third script tag in `quality-dashboard.html` is enough.

---

## 7. CSS tokens and main.css

`assets/css/main.css` defines the hub's design tokens (colors, type, spacing). `quality-dashboard.css` should:

- Import `main.css` first (already in HTML head).
- Reuse main.css tokens where possible (CSS variables).
- Define quality-specific tokens only where main.css doesn't cover (e.g., RAG badge colors if main.css doesn't define green/amber/red as semantic tokens).
- Match the visual rhythm of `inventory-dashboard.css` — same card style, same table treatment, same loading skeleton — so the hub feels consistent.

Read `main.css` and `inventory-dashboard.css` at first build to see what tokens exist before defining new ones.
