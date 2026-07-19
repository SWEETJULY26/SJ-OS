---
name: sweet-july-skin-brand
description: Apply Sweet July Skin brand guidelines whenever creating, designing, or formatting any document, deck, PDF, HTML, or Canva output for Sweet July Skin. Use this skill any time the user asks to create a Word doc, PowerPoint, PDF, webpage, Canva deck, email, report, proposal, one-pager, or any other formatted output that should reflect the Sweet July Skin brand identity. Trigger even when the user just says "make a deck," "write a document," or "create a report" in the context of Sweet July Skin work — assume brand guidelines should always apply unless explicitly told otherwise. Also use when the user asks to "rebrand," "update the styling," or "make it on-brand."
---

# Sweet July Skin Brand Skill

This skill ensures all created documents, decks, PDFs, HTML pages, and Canva designs consistently reflect the Sweet July Skin brand identity.

## Step 1: Load Brand Guidelines

Before creating any output, read the full brand reference:

```
/mnt/skills/user/sweet-july-skin-brand/references/brand-guidelines.md
```

This file contains the authoritative source for colors, typography, logo rules, voice, and layout principles.

## Step 2: Load Brand Fonts

The real brand fonts are bundled in this skill. **Always use these — never substitute Google Fonts or system fonts for document/PDF/HTML outputs.**

Font files are located at:
```
/mnt/skills/user/sweet-july-skin-brand/assets/fonts/
```

### Available Font Files

| File | Use |
|------|-----|
| `GT-America-Expanded-Medium.ttf` | Extra headlines, large type moments, logo-equivalent titles |
| `GT-America-Standard-Medium.ttf` | GT America standard weight medium — UI labels, callouts |
| `GT-America-Standard-Regular.ttf` | GT America standard regular — website body (web only) |
| `GT-America-Standard-Light.ttf` | GT America light — supporting text, captions |
| `GT-America-Extended-Regular.ttf` | Extended regular — alternate display use |
| `Adrianna-Demibold.ttf` | **Primary headlines** — most common heading font |
| `Adrianna-Regular.ttf` | **All body text and paragraphs** |
| `Adrianna-Bold.ttf` | Emphasis within body copy |
| `Adrianna-BoldItalic.ttf` | Bold italic emphasis |
| `Adrianna-Italic.ttf` | Italic body text |
| `Adrianna-Extrabold.ttf` | Strong emphasis / callout headlines |

### Font Embedding by Output Type

**Word Documents (.docx):**
- Specify font names in python-docx as `"GT America Expanded"` for headings and `"Adrianna"` for body
- Copy `Adrianna-Regular.ttf`, `Adrianna-Demibold.ttf`, and `GT-America-Expanded-Medium.ttf` from the skill assets into the working directory before running the generation script

**PowerPoint (.pptx):**
- Set `run.font.name` to `"GT America Expanded"` for title placeholders and `"Adrianna"` for body/content placeholders
- Copy the same three core TTFs into working directory

**PDF (WeasyPrint):**
- Use `@font-face` in CSS pointing to the font file paths from the skill assets folder
- Register all weights before building

**PDF (ReportLab):**
- Register fonts: `pdfmetrics.registerFont(TTFont('Adrianna', '/mnt/skills/user/sweet-july-skin-brand/assets/fonts/Adrianna-Regular.ttf'))`
- Register each weight separately before use

**HTML / Claude.ai Artifacts:**
- For Claude.ai artifacts, the browser cannot access the skill's file path directly
- Read each font file, base64-encode it, and embed inline as a `data:font/truetype;base64,...` URI in `@font-face`
- See the HTML font stack template below

---

## Step 3: Load Brand Logos

The real brand logo files are bundled in this skill. **Always use these — never approximate the logo with typed text, emoji, or a placeholder.**

Logo files are located at:
```
/mnt/skills/user/sweet-july-skin-brand/assets/logos/
```

Before picking a specific file, read the logo folder's own quick-reference:
```
/mnt/skills/user/sweet-july-skin-brand/assets/logos/README.md
```

### The five marks

| Mark | When to use | Folder |
|------|-------------|--------|
| **Sweet July Skin — stacked** | Default and primary logo. Cover pages, product pages, deck title slides. | `sweet-july-skin/stacked/` |
| **Sweet July Skin — inline** | Single-line version. Website headers, document running headers, email signatures, narrow spaces. | `sweet-july-skin/inline/` |
| **Sweet July — stacked** | Parent brand (Ayesha Curry's lifestyle brand). Use only in parent-brand contexts. | `sweet-july/stacked/` |
| **Sweet July — wordmark** | Parent brand, one-line version. | `sweet-july/wordmark/` |
| **Lignum Vitae flower** (submark) | Decorative background accent. **Never use alone** — a logo must also be on the page. | `submark-flower/` |

### Color variants

Each logo ships in four color variants (five for the flower):

| Variant | Use on |
|---------|--------|
| `-black` | Bone or white backgrounds (default) |
| `-pava` (Pava Brown `#8a665a`) | Bone or white backgrounds, for warm brand feel |
| `-goodyouth` (Good Youth `#795d50`) | Bone or white backgrounds, slightly darker option |
| `-white` | Pava Brown, Good Youth, or any dark brand-color background |
| `-soursop` (flower only, `#bcab83`) | Flower submark on Bone — the brand-preferred color |

### File format by output type

| Output | Format | Why |
|--------|--------|-----|
| Word (.docx) | **PNG** | `add_picture()` in python-docx takes raster |
| PowerPoint (.pptx) | **PNG** | `add_picture()` in python-pptx takes raster |
| PDF (WeasyPrint) | **SVG** or **PNG** | SVG scales cleanly in modern WeasyPrint |
| PDF (ReportLab) | **PNG** | ReportLab's SVG support is limited |
| HTML / Claude.ai artifact | **SVG** (inline contents) | Scales to any size, recolorable via CSS |
| Canva upload | **PNG** | Canva accepts PNG uploads with transparency |
| Designer handoff | **.ai** original | For editing in Illustrator |

PNGs are 300 DPI with transparent backgrounds, so they drop cleanly onto any color.

### Logo embedding by output type

**Word Documents (.docx):**
```python
from docx.shared import Inches
doc.add_picture(
    '/mnt/skills/user/sweet-july-skin-brand/assets/logos/sweet-july-skin/stacked/sjs-stacked-pava.png',
    width=Inches(2.0)
)
```

**PowerPoint (.pptx):**
```python
from pptx.util import Inches
# Cover slide on Pava Brown — use white variant
slide.shapes.add_picture(
    '/mnt/skills/user/sweet-july-skin-brand/assets/logos/sweet-july-skin/stacked/sjs-stacked-white.png',
    left=Inches(4), top=Inches(2.5), width=Inches(2.5)
)
```

**PDF (ReportLab):**
```python
from reportlab.platypus import Image
logo = Image('/mnt/skills/user/sweet-july-skin-brand/assets/logos/sweet-july-skin/inline/sjs-inline-pava.png', width=180, height=40)
```

**HTML / Claude.ai Artifacts — inline the SVG contents:**
```python
from pathlib import Path
logo_svg = Path('/mnt/skills/user/sweet-july-skin-brand/assets/logos/sweet-july-skin/inline/sjs-inline-white.svg').read_text()
# Inject directly into your HTML template:
html = f'<header class="brand-bar">{logo_svg}</header>'
```
Inlining the SVG (not `<img src="...">`) lets you style it with CSS, e.g. `header svg path { fill: #ffffff; }` for on-the-fly recoloring.

---

## Step 4: Identify Output Type

Determine which format is being created and apply the appropriate output-type guidance below.

---

## Output-Type Guidelines

### Word Documents (.docx)
- Also read `/mnt/skills/public/docx/SKILL.md` before proceeding
- **Background:** White or Bone (`#f4f0e8`)
- **Heading 1:** Adrianna Demibold, Pava Brown (`#8a665a`), ALL CAPS
- **Heading 2:** Adrianna Demibold, Good Youth (`#795d50`), sentence case
- **Body text:** Adrianna Regular, dark brown or black, 11–12pt
- **Accent lines/dividers:** Soursop (`#bcab83`) or Pava (`#cab29d`) horizontal rules
- **Cover page:** Pava Brown background, white logo — `logos/sweet-july-skin/stacked/sjs-stacked-white.png`
- **Running header:** Inline logo in Pava — `logos/sweet-july-skin/inline/sjs-inline-pava.png` at ~1.5" wide
- **Tone:** Warm, confident, irie — not clinical or corporate

### PowerPoint Decks (.pptx)
- Also read `/mnt/skills/public/pptx/SKILL.md` before proceeding
- **Cover slide:** Full Pava Brown (`#8a665a`) or Good Youth (`#795d50`) background. Use the white stacked logo: `logos/sweet-july-skin/stacked/sjs-stacked-white.png` (centered, ~2.5" wide)
- **Content slides:** Bone (`#f4f0e8`) background, Pava Brown headings in Adrianna Demibold, dark body text in Adrianna Regular. Small inline logo in a corner if desired: `logos/sweet-july-skin/inline/sjs-inline-pava.png`
- **Section divider slides:** Bold primary color backgrounds — alternate Pava Brown and Good Youth. Use the white stacked logo.
- **Decorative element:** Lignum Vitae flower as subtle background watermark — `logos/submark-flower/lignum-vitae-flower-soursop.png` at ~23.92° rotation, low opacity. **Only use when the full logo is also on the slide.**
- **Font hierarchy:** Large title = GT America Expanded Medium; Subhead = Adrianna Demibold; Body = Adrianna Regular
- **Accent colors:** Use Soursop, Pava, or Essential for data callouts or highlight boxes

### PDFs
- Also read `/mnt/skills/public/pdf/SKILL.md` before proceeding
- Same color and typography rules as Word Documents
- Bone background for content areas, Pava Brown for headers/cover
- Generous margins and white space — never cluttered
- **Cover page logo:** Use `logos/sweet-july-skin/stacked/sjs-stacked-white.png` on a Pava Brown or Good Youth cover
- **Header/footer logo:** Use `logos/sweet-july-skin/inline/sjs-inline-pava.png` at a small size
- **WeasyPrint:** prefer SVG — `<img src="file:///mnt/skills/user/sweet-july-skin-brand/assets/logos/sweet-july-skin/inline/sjs-inline-pava.svg">` scales crisply
- **ReportLab:** use PNG paths with `Image(path, width=..., height=...)` — SVG support in ReportLab is limited

### Web / HTML Artifacts

- **Background:** Bone (`#f4f0e8`)
- **Headings:** Good Youth (`#795d50`), Adrianna Demibold
- **Buttons/CTAs:** Pava Brown (`#8a665a`) background, white text
- **Accent borders:** Soursop (`#bcab83`) or Pava (`#cab29d`)
- **Header logo:** Read the inline SVG and embed its contents directly in the HTML (not as `<img src="...">`) so it scales and can be recolored with CSS:

```python
from pathlib import Path
logo_svg = Path('/mnt/skills/user/sweet-july-skin-brand/assets/logos/sweet-july-skin/inline/sjs-inline-pava.svg').read_text()
html = f'<header class="brand-bar">{logo_svg}</header>'
```

- **Dark hero sections:** use `sjs-inline-white.svg` or `sjs-stacked-white.svg`
- **Flower as decorative background:** inline `logos/submark-flower/lignum-vitae-flower-soursop.svg`, rotate ~23.92°, set low opacity (e.g. 0.15). Only use when the logo is also on the page.
- **Recolor SVGs on the fly with CSS:** if the inlined SVG uses `<path>` with a fill attribute, override it with `header svg path { fill: #b08a6c; }`

**Font embedding for HTML artifacts (base64 method):**

```python
import base64

def font_to_base64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

fonts = {
    'gt_expanded': font_to_base64('/mnt/skills/user/sweet-july-skin-brand/assets/fonts/GT-America-Expanded-Medium.ttf'),
    'adrianna_regular': font_to_base64('/mnt/skills/user/sweet-july-skin-brand/assets/fonts/Adrianna-Regular.ttf'),
    'adrianna_demibold': font_to_base64('/mnt/skills/user/sweet-july-skin-brand/assets/fonts/Adrianna-Demibold.ttf'),
    'adrianna_bold': font_to_base64('/mnt/skills/user/sweet-july-skin-brand/assets/fonts/Adrianna-Bold.ttf'),
    'adrianna_italic': font_to_base64('/mnt/skills/user/sweet-july-skin-brand/assets/fonts/Adrianna-Italic.ttf'),
}
```

Then inject into the HTML `<style>` block:

```css
@font-face {
  font-family: 'GT America';
  src: url('data:font/truetype;base64,{gt_expanded}') format('truetype');
  font-weight: 500;
}
@font-face {
  font-family: 'Adrianna';
  src: url('data:font/truetype;base64,{adrianna_regular}') format('truetype');
  font-weight: 400;
}
@font-face {
  font-family: 'Adrianna';
  src: url('data:font/truetype;base64,{adrianna_demibold}') format('truetype');
  font-weight: 600;
}
@font-face {
  font-family: 'Adrianna';
  src: url('data:font/truetype;base64,{adrianna_bold}') format('truetype');
  font-weight: 700;
}
@font-face {
  font-family: 'Adrianna';
  src: url('data:font/truetype;base64,{adrianna_italic}') format('truetype');
  font-weight: 400;
  font-style: italic;
}

h1, .display { font-family: 'GT America', sans-serif; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }
h2, h3      { font-family: 'Adrianna', sans-serif; font-weight: 600; }
body, p     { font-family: 'Adrianna', sans-serif; font-weight: 400; }
```

### Canva Decks
- **Color palette:** Bone backgrounds; primary brand colors for emphasis
- **Cover:** Pava Brown background, white title in GT America Expanded (wide-tracked caps). Upload `logos/sweet-july-skin/stacked/sjs-stacked-white.png` for the cover.
- **Content slides:** Bone background, Adrianna for all text. Upload `logos/sweet-july-skin/inline/sjs-inline-pava.png` for headers or corner marks.
- **Accent slides:** Rotate through Good Youth (`#795d50`), Irie Power (`#b08a6c`) — use the white logo on these
- **Flower submark:** Upload `logos/submark-flower/lignum-vitae-flower-soursop.png` as a decorative background element (only alongside a logo)
- **Font note:** Instruct the user to upload GT America and Adrianna to their Canva Brand Kit. Describe intended font choices clearly in the design spec.
- **Designer handoff:** If the user is passing the file to a designer, the original `.ai` files in each logo folder are editable in Illustrator

---

## Brand Voice Reminders

- **Warm and celebratory** — not clinical or corporate
- **Rooted in Caribbean/Jamaican culture** — evocative references to rituals, ingredients, nature
- **Inclusive and skin-tone celebrating**
- **Irie energy** — peaceful, positive, confident
- **Avoid:** overly formal language, clinical skincare jargon, cold or distant tone

### Signature phrases:
- "Everything Irie" · "Barefaced and sun-kissed" · "Time-tested Caribbean ingredients"
- "Modern formulas, ancient wisdom" · "Your daily ritual" · "A private self-care retreat"

---

## Key Brand Don'ts

- ❌ Never use the Lignum Vitae flower without the logo also present on the same page
- ❌ Never approximate the logo with typed text, system fonts, or emoji — always use a file from `assets/logos/`
- ❌ Never stretch, skew, rotate (except the 23.92° flower variant), or recolor the logo into a non-brand color
- ❌ Never use the black or colored logo variants on a dark Pava Brown or Good Youth background — use `-white` instead
- ❌ Never use the parent **Sweet July** logo in place of **Sweet July Skin** — the skincare line has its own mark
- ❌ Never use Saol Display as a primary or body font — accent only
- ❌ Never use neon, fluorescent, or stark colors outside the brand palette
- ❌ Never use busy patterned backgrounds
- ❌ Never write in a clinical, pharmaceutical, or overly corporate tone
- ❌ Never use GT America Regular for body text (website-only exception)
- ❌ Never substitute Google Fonts or system fonts — use the real brand fonts from this skill's assets

---

## Quick Color Reference

| Purpose | Color Name | Hex |
|---------|-----------|-----|
| Primary dark | Pava Brown | `#8a665a` |
| Primary dark alt | Good Youth | `#795d50` |
| Primary mid | Irie Power | `#b08a6c` |
| Background | Bone | `#f4f0e8` |
| Accent warm | Soursop | `#bcab83` |
| Accent blush | Pava | `#cab29d` |
| Accent neutral | Castaway | `#978369` |
| Accent blue | Coffee Fix | `#a2b2c8` |
| Accent green | Guava | `#a9c47f` |
| Accent light | Lychee | `#d7d2cb` |
| Accent pink | Essential | `#e1b7a7` |
| Accent rust | Rum Cake | `#9b5f3a` |
| Accent yellow | Pineapple Punch | `#f3d54e` |
