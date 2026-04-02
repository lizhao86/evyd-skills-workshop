#!/usr/bin/env node
/**
 * gen_free.js — Free-design PPTX renderer (PptxGenJS, no template)
 *
 * Usage:
 *   node gen_free.js <content.json> [--style dark_navy] [--output path/to/out.pptx]
 *
 * Unlike gen_pptx.py (which fills an EVYD Aptos template), this renderer
 * draws every shape, color, and text box from scratch using PptxGenJS.
 * This allows fully custom visual styles independent of any template.
 *
 * Styles live in ./styles/<name>.js — copy dark_navy.js to add a new one.
 *
 * After generation, run QA:
 *   /Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
 *     --convert-to pdf out.pptx --outdir /tmp/
 *   pdftoppm -jpeg -r 150 /tmp/out.pdf /tmp/slide
 *   open /tmp/slide-*.jpg
 */

const pptxgen  = require("pptxgenjs");
const path     = require("path");
const fs       = require("fs");

// ── CLI args
const args    = process.argv.slice(2);
const jsonArg = args.find(a => !a.startsWith("--"));
if (!jsonArg) { console.error("Usage: node gen_free.js <content.json> [--style NAME] [--output PATH]"); process.exit(1); }

const styleArg  = args[args.indexOf("--style")  + 1] || null;
const outputArg = args[args.indexOf("--output") + 1] || null;

// ── Load content
const content = JSON.parse(fs.readFileSync(jsonArg, "utf8"));
const meta    = content.meta || {};

// ── Load style
const styleName = styleArg || meta.free_style || "dark_navy";
const stylePath = path.join(__dirname, "styles", styleName + ".js");
if (!fs.existsSync(stylePath)) {
  console.error(`Style not found: ${stylePath}\nAvailable: ${fs.readdirSync(path.join(__dirname, "styles")).join(", ")}`);
  process.exit(1);
}
const ST = require(stylePath);
const C  = ST.colors;
const F  = ST.fonts;

// ── Output path
const outputPath = outputArg || meta.output || path.join(process.cwd(), "output_free.pptx");

// ── Slide dimensions
const W = 10, H = 5.625;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title  = meta.title || "Presentation";

// ════════════════════════════════════════════
// HELPERS
// ════════════════════════════════════════════

function addHeader(s, sectionTag, title) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.65, fill: { color: C.header_bg }, line: { type: "none" } });
  s.addText(sectionTag, { x: 0.5, y: 0, w: 2.8, h: 0.65, fontSize: 9, fontFace: F.body, bold: true, color: C.accent_orange, valign: "middle", charSpacing: 1.5, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 3.35, y: 0.22, w: 0.02, h: 0.22, fill: { color: C.header_sep }, line: { type: "none" } });
  s.addText(title, { x: 3.45, y: 0, w: 6.2, h: 0.65, fontSize: 15, fontFace: F.body, bold: true, color: C.text_white, valign: "middle", margin: 0 });
}

function slideNum(s, n, total, light) {
  s.addText(`${String(n).padStart(2,"0")} / ${String(total).padStart(2,"0")}`, {
    x: 8.8, y: 5.3, w: 1, h: 0.2, fontSize: 8, color: light ? C.slide_num_lt : C.slide_num, align: "right", margin: 0,
  });
}

// ════════════════════════════════════════════
// SLIDE RENDERERS
// ════════════════════════════════════════════

const RENDERERS = {

  // ── Cover
  cover(s, d, n, total) {
    s.background = { color: C.bg_primary };
    const [barTop, barBot] = ST.motifs.left_bar_colors;
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0,    w: 0.07, h: H/2, fill: { color: barTop }, line: { type: "none" } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: H/2,  w: 0.07, h: H/2, fill: { color: barBot }, line: { type: "none" } });
    s.addShape(pres.shapes.OVAL, { x: 5.8, y: -1.5, w: 6, h: 6, fill: { color: C.accent_teal, transparency: 94 }, line: { type: "none" } });

    // Tag
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 0.85, w: 2.8, h: 0.32, fill: { color: C.accent_dark2 }, line: { color: C.accent_orange, width: 1 } });
    s.addText((d.tag || "课题  ·  PRESENTATION").toUpperCase(), {
      x: 0.55, y: 0.85, w: 2.8, h: 0.32, fontSize: 8, fontFace: F.body, bold: true,
      color: C.accent_orange, align: "center", valign: "middle", charSpacing: 1.5, margin: 0,
    });

    // Title
    s.addText(d.title || "", {
      x: 0.55, y: 1.3, w: 7.2, h: 1.9,
      fontSize: 40, fontFace: F.heading, color: C.text_white, valign: "top", margin: 0,
    });

    // Subtitle
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 3.35, w: 0.05, h: 0.68, fill: { color: C.accent_teal }, line: { type: "none" } });
    s.addText(d.subtitle || "", {
      x: 0.7, y: 3.35, w: 5.8, h: 0.68,
      fontSize: 14, fontFace: F.body, color: C.text_muted, valign: "middle", margin: 0,
    });

    // Logo
    s.addText(d.logo || "EVYD  ·  2025", {
      x: 7.5, y: 5.1, w: 2.2, h: 0.3,
      fontSize: 9, fontFace: F.body, color: C.header_sep, align: "right", charSpacing: 3, margin: 0,
    });
    slideNum(s, n, total);
  },

  // ── Bullets with side quote panel
  bullets_with_panel(s, d, n, total) {
    s.background = { color: C.bg_content };
    addHeader(s, d.section || "", d.title || "");

    const bx = 0.45, by = 0.82, bw = 6.2, rowH = 1.0;
    (d.bullets || []).forEach((txt, i) => {
      const y = by + i * rowH;
      s.addShape(pres.shapes.OVAL, { x: bx, y: y + 0.42, w: 0.1, h: 0.1, fill: { color: ST.motifs.bullet_dot_color }, line: { type: "none" } });
      s.addText(txt, { x: bx + 0.2, y, w: bw, h: rowH, fontSize: 12.5, fontFace: F.body, color: C.text_primary, valign: "middle", margin: 0 });
    });

    // Quote panel
    s.addShape(pres.shapes.RECTANGLE, { x: 6.8, y: 0.65, w: 3.05, h: 4.8, fill: { color: C.bg_primary }, line: { type: "none" } });
    s.addShape(pres.shapes.RECTANGLE, { x: 6.8, y: 0.65, w: 0.05, h: 4.8, fill: { color: C.accent_teal }, line: { type: "none" } });

    const panel = d.side_panel || {};
    s.addText("\u201C", { x: 6.95, y: 0.8, w: 1, h: 0.9, fontSize: 54, fontFace: F.heading, color: ST.motifs.quote_mark_color, margin: 0 });
    s.addText(panel.text || "", {
      x: 6.95, y: 1.75, w: 2.7, h: 2.8,
      fontSize: 13, fontFace: F.body, italic: true, color: C.text_primary, valign: "top", margin: 0,
    });
    slideNum(s, n, total);
  },

  // ── Criteria rows (white background)
  criteria_rows(s, d, n, total) {
    s.background = { color: d.background === "white" ? C.bg_white : C.bg_content };
    const isWhite = d.background !== "blue";
    addHeader(s, d.section || "", d.title || "");

    if (d.subtitle) {
      s.addText(d.subtitle, { x: 0.5, y: 0.7, w: 9, h: 0.28, fontSize: 11, fontFace: F.body, color: C.text_muted, margin: 0 });
    }

    const rx = 0.45, rw = 9.1, rh = 0.86;
    (d.criteria || []).forEach((row, i) => {
      const ry = 1.1 + i * (rh + 0.1);
      s.addShape(pres.shapes.RECTANGLE, { x: rx, y: ry, w: rw, h: rh, fill: { color: isWhite ? C.bg_row : "FFFFFF", transparency: isWhite ? 0 : 94 }, line: { type: "none" } });
      s.addShape(pres.shapes.RECTANGLE, { x: rx, y: ry, w: 0.06, h: rh, fill: { color: C.accent_teal }, line: { type: "none" } });
      s.addText(row.num, { x: rx + 0.15, y: ry, w: 0.7, h: rh, fontSize: 24, fontFace: F.heading, bold: true, color: C.accent_teal, valign: "middle", margin: 0 });
      s.addShape(pres.shapes.RECTANGLE, { x: rx + 0.95, y: ry + 0.25, w: 0.02, h: 0.36, fill: { color: isWhite ? "CCCCCC" : "4A7A9B" }, line: { type: "none" } });
      s.addText(row.label, { x: rx + 1.1, y: ry, w: 1.8, h: rh, fontSize: 10, fontFace: F.body, bold: true, color: isWhite ? C.bg_primary : C.text_white, valign: "middle", charSpacing: 0.5, margin: 0 });
      s.addText(row.text,  { x: rx + 3.1, y: ry, w: 6.0, h: rh, fontSize: 12, fontFace: F.body, color: isWhite ? C.text_mid : C.text_primary, valign: "middle", margin: 0 });
    });
    slideNum(s, n, total, isWhite);
  },

  // ── Scope tiers (4 colored bands)
  scope_tiers(s, d, n, total) {
    s.background = { color: C.bg_content };
    addHeader(s, d.section || "", d.title || "");
    if (d.subtitle) {
      s.addText(d.subtitle, { x: 0.5, y: 0.7, w: 9, h: 0.28, fontSize: 11, fontFace: F.body, color: C.text_blue_lt, margin: 0 });
    }

    const tx = 0.45, tw = 9.1, th = 0.84;
    (d.tiers || []).forEach((t, i) => {
      const ty = 1.1 + i * (th + 0.1);
      const col = Array.isArray(t.color) ? t.color.map(v => v.toString(16).padStart(2,"0")).join("") : t.color;
      s.addShape(pres.shapes.RECTANGLE, { x: tx, y: ty, w: tw, h: th, fill: { color: "FFFFFF", transparency: 94 }, line: { type: "none" } });
      s.addShape(pres.shapes.RECTANGLE, { x: tx, y: ty, w: 0.07, h: th, fill: { color: col }, line: { type: "none" } });
      s.addText("●", { x: tx + 0.15, y: ty, w: 0.35, h: th, fontSize: ST.motifs.tier_dot_size, fontFace: F.body, color: col, valign: "middle", margin: 0 });
      s.addText(t.label, { x: tx + 0.55, y: ty, w: 2.3,  h: th, fontSize: 12, fontFace: F.body, bold: true, color: C.text_white, valign: "middle", margin: 0 });
      s.addText(t.desc,  { x: tx + 2.95, y: ty, w: 4.5,  h: th, fontSize: 11, fontFace: F.body, color: C.text_primary, valign: "middle", margin: 0 });
      if (t.example) {
        s.addText(t.example, { x: tx + 7.5, y: ty, w: 1.55, h: th, fontSize: 7.5, fontFace: F.body, italic: true, color: C.text_example, valign: "middle", align: "right", margin: 0 });
      }
    });
    slideNum(s, n, total);
  },

  // ── Two column steps
  two_column_steps(s, d, n, total) {
    s.background = { color: C.bg_content };
    addHeader(s, d.section || "", d.title || "");

    s.addShape(pres.shapes.RECTANGLE, { x: 4.95, y: 0.65, w: 0.02, h: 4.55, fill: { color: "FFFFFF", transparency: 82 }, line: { type: "none" } });

    const cols = d.columns || [];
    const colX = [0.4, 5.15];
    const dotColors = [C.accent_teal, C.accent_orange];
    const stepH = 1.15;

    cols.forEach((col, ci) => {
      const cx = colX[ci];
      s.addText(col.title || "", { x: cx, y: 0.72, w: 4.4, h: 0.35, fontSize: 10, fontFace: F.body, bold: true, color: C.accent_orange, charSpacing: 1, margin: 0 });
      s.addShape(pres.shapes.RECTANGLE, { x: cx, y: 1.1, w: 4.4, h: 0.02, fill: { color: C.accent_orange, transparency: 60 }, line: { type: "none" } });

      (col.steps || []).forEach((step, si) => {
        const sy = 1.18 + si * stepH;
        const label = ci === 0 ? String(si + 1) : String.fromCharCode(65 + si);
        s.addShape(pres.shapes.RECTANGLE, { x: cx, y: sy, w: 4.4, h: stepH - 0.08, fill: { color: "FFFFFF", transparency: 93 }, line: { type: "none" } });
        s.addShape(pres.shapes.RECTANGLE, { x: cx, y: sy, w: 0.05, h: stepH - 0.08, fill: { color: C.text_white, transparency: 70 }, line: { type: "none" } });
        s.addShape(pres.shapes.OVAL, { x: cx + 0.12, y: sy + 0.16, w: 0.38, h: 0.38, fill: { color: dotColors[ci] }, line: { type: "none" } });
        s.addText(label, { x: cx + 0.12, y: sy + 0.16, w: 0.38, h: 0.38, fontSize: 10, fontFace: F.body, bold: true, color: C.text_white, align: "center", valign: "middle", margin: 0 });
        s.addText(step.bold   || "", { x: cx + 0.65, y: sy + 0.1,  w: 3.6, h: 0.3,  fontSize: 12,   fontFace: F.body, bold: true, color: C.text_white, margin: 0 });
        s.addText(step.normal || "", { x: cx + 0.65, y: sy + 0.42, w: 3.6, h: 0.65, fontSize: 10.5, fontFace: F.body, color: C.text_dim, margin: 0 });
      });
    });

    if (d.warning) {
      s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.05, w: W, h: 0.45, fill: { color: C.warning_bg }, line: { type: "none" } });
      s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.05, w: W, h: 0.04, fill: { color: C.accent_orange }, line: { type: "none" } });
      s.addText(d.warning, { x: 0.4, y: 5.09, w: 9.2, h: 0.38, fontSize: 10, fontFace: F.body, color: C.text_dim, valign: "middle", margin: 0 });
    }
    slideNum(s, n, total);
  },

  // ── Ending slide
  ending(s, d, n, total) {
    s.background = { color: C.bg_primary };
    s.addShape(pres.shapes.OVAL, { x: 2.5, y: 0.3, w: 5, h: 2.8, fill: { color: C.accent_teal, transparency: 93 }, line: { type: "none" } });
    s.addText(d.title || "", { x: 0.5, y: 0.7, w: 9, h: 1.1, fontSize: 36, fontFace: F.heading, color: C.text_white, align: "center", valign: "middle", margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 4.45, y: 1.9, w: 1.1, h: 0.05, fill: { color: C.accent_teal }, line: { type: "none" } });
    if (d.subtitle) {
      s.addText(d.subtitle, { x: 1, y: 2.05, w: 8, h: 0.45, fontSize: 14, fontFace: F.body, color: C.text_muted, align: "center", margin: 0 });
    }
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 3.55, w: W, h: 0.015, fill: { color: "FFFFFF", transparency: 88 }, line: { type: "none" } });

    const acts = d.actions || [];
    const aw = W / Math.max(acts.length, 1);
    acts.forEach((a, i) => {
      const ax = i * aw;
      if (i > 0) s.addShape(pres.shapes.RECTANGLE, { x: ax, y: 3.57, w: 0.015, h: 2.0, fill: { color: "FFFFFF", transparency: 88 }, line: { type: "none" } });
      s.addText(a.icon || "", { x: ax + 0.35, y: 3.68, w: 0.55, h: 0.5, fontSize: 22, align: "center", margin: 0 });
      s.addText(a.title || "", { x: ax + 1.0, y: 3.7,  w: aw - 1.1, h: 0.35, fontSize: 12,   fontFace: F.body, bold: true, color: C.accent_teal, margin: 0 });
      s.addText(a.desc  || "", { x: ax + 1.0, y: 4.07, w: aw - 1.1, h: 0.65, fontSize: 10.5, fontFace: F.body, color: "607D8E", margin: 0 });
    });
    slideNum(s, n, total);
  },
};

// ════════════════════════════════════════════
// RENDER
// ════════════════════════════════════════════

const slides = content.slides || [];
const total  = slides.length;

slides.forEach((d, i) => {
  const renderer = RENDERERS[d.type];
  if (!renderer) { console.warn(`Unknown slide type: ${d.type} (skipped)`); return; }
  const slide = pres.addSlide();
  renderer(slide, d, i + 1, total);
});

pres.writeFile({ fileName: outputPath })
  .then(() => console.log(`✓ Saved → ${outputPath}`))
  .catch(e => { console.error(e); process.exit(1); });
