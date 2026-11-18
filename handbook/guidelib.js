// Layout helpers for the Rapid Assets Studio guide book.
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, HeadingLevel,
  AlignmentType, LevelFormat, BorderStyle, PageBreak, Footer, PageNumber, TabStopType, ImageRun } = require("docx");

const FONT = "Arial";
const INK = "1F2328", GREY = "595959", LIGHT = "F3F4F6", ORANGE = "E8650A", ORANGE_BG = "FDEBDD", LINE = "D0D4D9";
const W = 9640; // text width in DXA (Letter, 1300 margins)

const border = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const borders = { top: border, bottom: border, left: border, right: border };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };

// Inline markup: **bold**, `ui label` (bold, dark), ›/→ kept as typed.
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  const s = String(text);
  while ((m = re.exec(s))) {
    if (m.index > last) out.push(new TextRun({ text: s.slice(last, m.index), font: FONT, size: 21, ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, font: FONT, size: 21, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), bold: true, color: INK, font: FONT, size: 21, ...base }));
    last = m.index + t.length;
  }
  if (last < s.length) out.push(new TextRun({ text: s.slice(last), font: FONT, size: 21, ...base }));
  return out;
}

const p = (text, o = {}) => new Paragraph({ spacing: { after: 120 }, children: runs(text, o) });
const small = (text) => new Paragraph({ spacing: { after: 100 }, children: runs(text, { size: 18, color: GREY }) });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun({ text: t, font: FONT })] });
const h1keep = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, font: FONT })] });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, children: [new TextRun({ text: t, font: FONT })] });
const h3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, children: [new TextRun({ text: t, font: FONT })] });
const bullet = (t) => new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 70 }, children: runs(t) });
const sub = (t) => new Paragraph({ numbering: { reference: "b", level: 1 }, spacing: { after: 60 }, children: runs(t) });
const gap = () => new Paragraph({ spacing: { after: 60 }, children: [] });

let instance = 0;
function steps(list) {
  instance += 1;
  const inst = instance;
  return list.map((t) => Array.isArray(t)
    ? t.map((s) => new Paragraph({ numbering: { reference: "b", level: 1 }, spacing: { after: 60 }, children: runs(s) }))
    : new Paragraph({ numbering: { reference: "steps", level: 0, instance: inst }, spacing: { after: 80 }, children: runs(t) })).flat();
}

function cell(content, width, o = {}) {
  const kids = (Array.isArray(content) ? content : [content]).map((c) =>
    c instanceof Paragraph ? c : new Paragraph({ keepNext: !!o.keep, spacing: { after: 40 }, children: runs(c, { size: 19, ...(o.head ? { bold: true, color: "FFFFFF" } : {}), ...(o.bold ? { bold: true } : {}) }) }));
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: o.head ? { fill: INK, type: ShadingType.CLEAR } : o.fill ? { fill: o.fill, type: ShadingType.CLEAR } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 }, children: kids,
  });
}

function table(widths, head, rows, o = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [
      ...(head ? [new TableRow({ tableHeader: true, cantSplit: true, children: head.map((h, i) => cell(h, widths[i], { head: true })) })] : []),
      ...rows.map((r) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], { keep: o.keep, fill: i === 0 && o.firstCol ? LIGHT : undefined, bold: i === 0 && o.firstColBold })) })),
    ],
  });
}

// Key/value box at the top of every flow.
function facts(rows) {
  return table([2000, W - 2000], null, rows, { firstCol: true, firstColBold: true, keep: true });
}

// Shaded call-out paragraph.
function callout(text, fill = ORANGE_BG) {
  return new Paragraph({
    spacing: { before: 80, after: 140 }, shading: { fill, type: ShadingType.CLEAR },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: ORANGE, space: 6 } },
    indent: { left: 120, right: 120 }, children: runs(text, { size: 20 }),
  });
}

function levelBanner(tag, title, text) {
  return [
    new Paragraph({ spacing: { before: 280, after: 40 }, keepNext: true, children: [
      new TextRun({ text: tag.toUpperCase(), bold: true, color: ORANGE, size: 18, font: FONT, characterSpacing: 40 })] }),
    new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 0, after: 80 }, children: [new TextRun({ text: title, font: FONT })] }),
    ...(text ? [new Paragraph({ spacing: { after: 160 }, keepNext: true, children: runs(text, { color: GREY }) })] : []),
  ];
}

// Screenshots: JPEGs made by shots/prep.py, listed in shots/jpg/index.json as {name: [w, h]}.
const fs = require("fs");
const path = require("path");
const SHOT_DIR = process.env.GUIDE_SHOTS || "";
const SHOTS = SHOT_DIR && fs.existsSync(path.join(SHOT_DIR, "index.json")) ? JSON.parse(fs.readFileSync(path.join(SHOT_DIR, "index.json"), "utf8")) : {};
const missing = [];
function shot(name, caption, widthIn = 6.2) {
  if (!SHOTS[name]) { missing.push(name); return []; }
  const [w, h] = SHOTS[name];
  const px = Math.round(widthIn * 96);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 80, after: 40 },
      children: [new ImageRun({ type: "jpg", data: fs.readFileSync(path.join(SHOT_DIR, name + ".jpg")),
        transformation: { width: px, height: Math.round(px * h / w) },
        altText: { title: caption || name, description: caption || name, name } })] }),
    ...(caption ? [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: runs(caption, { size: 17, color: GREY, italics: true }) })] : []),
  ];
}

// One flow = id + title, a facts box (use when / where / cost / result), screenshots, numbered steps, optional tips.
function flow(f) {
  const out = [h3(`${f.id}  ·  ${f.title}`)];
  const rows = [];
  if (f.when) rows.push(["Use it when", f.when]);
  if (f.where) rows.push(["Where", f.where]);
  if (f.cost) rows.push(["Cost", f.cost]);
  if (f.result) rows.push(["You get", f.result]);
  if (rows.length) out.push(facts(rows), new Paragraph({ keepNext: true, spacing: { after: 60 }, children: [] }));
  for (const [n, c] of (f.img || [])) out.push(...shot(n, c));
  if (f.intro) out.push(p(f.intro));
  if (f.steps) out.push(...steps(f.steps));
  if (f.table) out.push(gap(), table(f.table.widths, f.table.head, f.table.rows, f.table.o || {}), gap());
  if (f.tips && f.tips.length) {
    out.push(new Paragraph({ spacing: { before: 100, after: 60 }, keepNext: true, children: [new TextRun({ text: "Tips", bold: true, font: FONT, size: 20, color: GREY })] }));
    out.push(...f.tips.map(bullet));
  }
  if (f.callout) out.push(callout(f.callout));
  out.push(gap());
  return out;
}

function build(children, footerText) {
  return new Document({
    creator: "Rapid Assets", title: "Rapid Assets Studio Guide Book",
    styles: {
      default: { document: { run: { font: FONT, size: 21, color: INK } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 34, bold: true, font: FONT, color: INK }, paragraph: { spacing: { before: 0, after: 200 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 26, bold: true, font: FONT, color: INK }, paragraph: { spacing: { before: 260, after: 100 }, outlineLevel: 1 } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 23, bold: true, font: FONT, color: ORANGE }, paragraph: { spacing: { before: 240, after: 100 }, outlineLevel: 2 } },
      ],
    },
    numbering: { config: [
      { reference: "b", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 260 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 900, hanging: 260 } } } }] },
      { reference: "steps", levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 320 } }, run: { bold: true, color: ORANGE } } }] },
    ] },
    sections: [{
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1300, right: 1300, bottom: 1200, left: 1300 } } },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
        new TextRun({ text: `${footerText}  ·  `, size: 16, color: "808080", font: FONT }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "808080", font: FONT })] })] }) },
      children,
    }],
  });
}

module.exports = { Packer, Paragraph, TextRun, PageBreak, p, small, h1, h1keep, h2, h3, bullet, sub, gap, steps, table, facts, callout,
  levelBanner, flow, build, shot, missing, W, INK, GREY, ORANGE, LIGHT, FONT, runs };
