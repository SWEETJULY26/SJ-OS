---
name: excalidraw
description: Use when someone asks to draw a diagram, make an Excalidraw diagram, build an editable diagram, sketch a flowchart, or visualize a system or flow. Default for all diagram requests. Offers two modes — a lite mode for fast, low-token simple flows (3–10 nodes), and a full mode for detailed, nested, multi-zone architecture diagrams.
---

## What this skill does

Generates editable `.excalidraw` diagrams in one of two modes. Both produce valid Excalidraw JSON the user can open or paste at excalidraw.com.

- **Lite** — fast and low-token. Simple flowcharts, quick flows, basic relationships, roughly 3–10 nodes. No clarifying questions, minimal schema, up to 3 colors.
- **Full** — detailed and structured. Nested containers, multi-zone architecture, full color and typography systems, layout math, and a feedback loop for revisions.

## Step 1: Pick the mode (do this first, every time)

Before generating anything, ask the user which mode they want:

> Do you want this **lite** (fast, simple — best for a quick flow of 3–10 boxes) or **full** (detailed — best for architecture, nested containers, or multi-zone systems)?

Skip the question only when the user already said which one they want (e.g. "use the full version", "just a quick lite one"). Honor that without re-asking.

Once the mode is chosen:
- **Lite** → read and follow `references/lite.md`
- **Full** → read and follow `references/full.md`

The two reference files carry the mode-specific rules: layout grids, color tables, element schemas, and (for full) the clarifying-question / planning / feedback workflow.

## Shared rules (both modes)

These apply no matter which mode you're in.

### JSON wrapper

Every diagram uses this shell:
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ... ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

### Save location

Save to `diagrams/[concept-slug].excalidraw`. Always use the `diagrams/` subfolder to keep the project root clean.

### Deliver

1. Save the file to `diagrams/`.
2. Show the full JSON in a code block so the user can copy it directly.
3. Describe what the diagram shows (one sentence in lite mode; a short paragraph covering each color zone in full mode).
4. Tell the user how to open it:

> **How to view and edit your diagram:**
> - Go to excalidraw.com (free, no account needed)
> - Option A: Click the menu (top-left hamburger icon) > "Open" > select the `.excalidraw` file
> - Option B: Copy the JSON code block above, open excalidraw.com, and paste it with Ctrl+V / Cmd+V
> - Every element is fully editable — drag to move, grab handles to resize, double-click to edit text
