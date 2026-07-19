# Sweet July Skin — Logo Assets

Five logo marks, each available in the original vector source plus scalable SVG and high-resolution transparent PNG, in four color variants (five for the flower submark).

---

## Which logo do I use?

| Situation | Use |
|-----------|-----|
| Cover page of a deck or doc for Sweet July Skin | **Sweet July Skin — stacked** |
| Running header, footer, website header, email signature for SJS | **Sweet July Skin — inline** |
| Document about the parent brand (Ayesha Curry / Sweet July lifestyle brand, not the skincare line) | **Sweet July — stacked** or **wordmark** |
| Decorative background element on a Sweet July Skin layout | **Lignum Vitae flower** (only when a logo is also present on the page) |

---

## Which color variant do I pick?

| Background | Variant file |
|-----------|--------------|
| Bone (`#f4f0e8`) or white | `-black`, `-pava`, or `-goodyouth` |
| Pava Brown (`#8a665a`) | `-white` |
| Good Youth (`#795d50`) | `-white` |
| Any dark primary brand color | `-white` |
| Flower submark on Bone | `-soursop` (preferred) or `-goodyouth` |

Per brand guidelines: the logo can render in any brand color as appropriate. The four provided variants cover the most common needs. To make a custom-color variant, copy the SVG and swap the fill (see bottom of this file).

---

## Which file format do I pick?

| Output | Format |
|--------|--------|
| Word doc (.docx) | PNG |
| PowerPoint (.pptx) | PNG |
| PDF (WeasyPrint, ReportLab) | PNG or SVG |
| HTML / Claude.ai artifact | SVG (inline the file contents) |
| Canva upload | PNG (or .ai for the designer) |
| Any scenario where a designer will open in Illustrator | `.ai` (original source) |

The PNGs are 300 DPI with transparent backgrounds — they drop cleanly onto any color.

---

## Folder map

```
logos/
├── sweet-july-skin/
│   ├── stacked/        ← "SWEET / JULY / SKIN" three-line logo. Default/primary mark.
│   │   ├── sjs-stacked.ai                    (original vector source)
│   │   ├── sjs-stacked-black.{svg,png}
│   │   ├── sjs-stacked-white.{svg,png}
│   │   ├── sjs-stacked-pava.{svg,png}
│   │   └── sjs-stacked-goodyouth.{svg,png}
│   └── inline/         ← "SWEET JULY SKIN" one-line logo. For web headers, footers, narrow spaces.
│       ├── sjs-inline.ai
│       └── sjs-inline-{black,white,pava,goodyouth}.{svg,png}
│
├── sweet-july/         ← Parent brand (Ayesha Curry's lifestyle brand). Use only for parent-brand contexts.
│   ├── stacked/
│   │   ├── sj-stacked.ai
│   │   └── sj-stacked-{black,white,pava,goodyouth}.{svg,png}
│   └── wordmark/       ← "SWEET JULY" single-line wordmark.
│       ├── sj-wordmark.ai
│       └── sj-wordmark-{black,white,pava,goodyouth}.{svg,png}
│
└── submark-flower/     ← Lignum Vitae flower. Never use alone — always alongside a logo.
    ├── lignum-vitae-flower.pdf               (original vector source)
    └── lignum-vitae-flower-{black,white,pava,goodyouth,soursop}.{svg,png}
```

---

## Brand rules at a glance

- **Default mark for Sweet July Skin:** the stacked logo.
- **The Lignum Vitae flower is a submark.** Never use it without a logo on the same page — the brand guidelines are firm on this.
- **Flower colors:** soursop or a neutral gray, always on a Bone background. The `-soursop` variant is only generated for the flower.
- **Cover pages** (Pava Brown or Good Youth background): always use the `-white` variant.

---

## Recoloring an SVG to a custom brand color

The source SVGs use a single fill color for all ink. To swap it to any hex color:

```python
from pathlib import Path
import re

def recolor_svg(src_path, out_path, hex_color):
    hx = hex_color.lstrip('#')
    r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    svg = Path(src_path).read_text()
    # Replace any rgb(...) fill with the new color
    svg = re.sub(r'rgb\([\d.]+%?,\s*[\d.]+%?,\s*[\d.]+%?\)', f'rgb({r}, {g}, {b})', svg)
    Path(out_path).write_text(svg)

# Example: make an Irie Power variant of the inline logo
recolor_svg(
    'sweet-july-skin/inline/sjs-inline-black.svg',
    '/tmp/sjs-inline-iriepower.svg',
    '#b08a6c'
)
```

For HTML artifacts, you can also recolor on the fly by inlining the SVG and overriding `fill` with CSS: `svg path { fill: #b08a6c; }`.
