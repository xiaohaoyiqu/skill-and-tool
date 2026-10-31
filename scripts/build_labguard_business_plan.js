const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  Header,
  HeadingLevel,
  LevelFormat,
  Packer,
  PageBreak,
  PageNumber,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableOfContents,
  TableLayoutType,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = require("../.docx-build/node_modules/docx");

const ROOT = path.resolve(__dirname, "..");
const SOURCE = path.join(ROOT, "商业计划书完整版_LabGuard.md");
const OUTPUT = path.join(ROOT, "LabGuard实验室安全与资源协同管理平台_完整版.docx");

const NAVY = "12324A";
const BLUE = "1E5B8C";
const TEAL = "0D8C8C";
const LIGHT_BLUE = "EAF3F8";
const LIGHT_TEAL = "E6F4F3";
const LIGHT_GREY = "F3F6F8";
const MID_GREY = "61717C";
const TEXT = "24333D";
const PAGE_WIDTH = 9360;

function textRun(text, options = {}) {
  return new TextRun({
    text: text.replaceAll("**", ""),
    font: "Microsoft YaHei",
    size: options.size || 21,
    color: options.color || TEXT,
    bold: options.bold || false,
    italics: options.italics || false,
  });
}

function plainParagraph(text, options = {}) {
  return new Paragraph({
    alignment: options.alignment || AlignmentType.JUSTIFIED,
    spacing: { after: options.after ?? 130, line: options.line ?? 360 },
    indent: options.indent,
    children: [textRun(text, options)],
  });
}

function heading(text, level) {
  const isTop = level === 1;
  return new Paragraph({
    heading: isTop ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
    spacing: { before: isTop ? 280 : 180, after: isTop ? 160 : 110 },
    border: isTop
      ? { bottom: { color: TEAL, space: 7, style: BorderStyle.SINGLE, size: 12 } }
      : undefined,
    children: [
      textRun(text, {
        size: isTop ? 32 : 25,
        bold: true,
        color: isTop ? NAVY : BLUE,
      }),
    ],
  });
}

function widthsFor(columns) {
  if (columns === 2) return [2700, 6660];
  if (columns === 3) return [2250, 3900, 3210];
  if (columns === 4) return [1450, 3500, 1600, 2810];
  const base = Math.floor(PAGE_WIDTH / columns);
  return Array.from({ length: columns }, (_, index) =>
    index === columns - 1 ? PAGE_WIDTH - base * (columns - 1) : base,
  );
}

function makeCell(text, width, header) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    shading: {
      type: ShadingType.CLEAR,
      color: "auto",
      fill: header ? BLUE : "FFFFFF",
    },
    margins: { top: 90, bottom: 90, left: 110, right: 110 },
    children: [
      new Paragraph({
        spacing: { after: 0, line: 280 },
        children: [
          textRun(text, {
            size: 18,
            color: header ? "FFFFFF" : TEXT,
            bold: header,
          }),
        ],
      }),
    ],
  });
}

function makeTable(rows) {
  const columns = Math.max(...rows.map((row) => row.length));
  const widths = widthsFor(columns);
  return new Table({
    width: { size: PAGE_WIDTH, type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "C8D5DE" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "C8D5DE" },
      left: { style: BorderStyle.SINGLE, size: 4, color: "C8D5DE" },
      right: { style: BorderStyle.SINGLE, size: 4, color: "C8D5DE" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 3, color: "DCE5EB" },
      insideVertical: { style: BorderStyle.SINGLE, size: 3, color: "DCE5EB" },
    },
    rows: rows.map(
      (row, rowIndex) =>
        new TableRow({
          children: Array.from({ length: columns }, (_, index) =>
            makeCell(row[index] || "", widths[index], rowIndex === 0),
          ),
        }),
    ),
  });
}

function makeCallout(text) {
  return new Table({
    width: { size: PAGE_WIDTH, type: WidthType.DXA },
    columnWidths: [PAGE_WIDTH],
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: TEAL },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL },
      left: { style: BorderStyle.SINGLE, size: 6, color: TEAL },
      right: { style: BorderStyle.SINGLE, size: 6, color: TEAL },
    },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: PAGE_WIDTH, type: WidthType.DXA },
            shading: { type: ShadingType.CLEAR, color: "auto", fill: LIGHT_TEAL },
            margins: { top: 140, bottom: 140, left: 180, right: 180 },
            children: [
              new Paragraph({
                spacing: { after: 0, line: 320 },
                children: [textRun(text, { size: 19, color: NAVY, italics: true })],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function parseTable(lines, start) {
  const rows = [];
  let index = start;
  while (index < lines.length && lines[index].startsWith("|")) {
    const cells = lines[index]
      .trim()
      .replace(/^\||\|$/g, "")
      .split("|")
      .map((cell) => cell.trim());
    if (!cells.every((cell) => /^:?-{3,}:?$/.test(cell))) rows.push(cells);
    index += 1;
  }
  return { rows, index };
}

function build() {
  const lines = fs.readFileSync(SOURCE, "utf8").replace(/\r/g, "").split("\n");
  const children = [];
  let coverMode = true;
  let index = 0;

  while (index < lines.length) {
    const line = lines[index].trimEnd();
    if (!line.trim()) {
      index += 1;
      continue;
    }
    if (line === "<!-- pagebreak -->") {
      children.push(new Paragraph({ children: [new PageBreak()] }));
      coverMode = false;
      index += 1;
      continue;
    }
    if (line === "<!-- toc -->") {
      index += 1;
      continue;
    }
    if (line.startsWith("|")) {
      const parsed = parseTable(lines, index);
      children.push(makeTable(parsed.rows));
      children.push(new Paragraph({ spacing: { after: 120 } }));
      index = parsed.index;
      continue;
    }
    if (line.startsWith("# ")) {
      children.push(new Paragraph({ spacing: { before: 2700, after: 240 }, children: [textRun(line.slice(2), { size: 48, color: NAVY, bold: true })] }));
      children.push(new Paragraph({ spacing: { after: 300 }, border: { bottom: { color: TEAL, space: 8, style: BorderStyle.SINGLE, size: 16 } }, children: [textRun("高校实验室日常管理方案", { size: 24, color: TEAL })] }));
      index += 1;
      continue;
    }
    if (line.startsWith("## ")) {
      const title = line.slice(3);
      if (title === "目录") {
        children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 180, after: 240 }, children: [textRun("目录", { size: 32, color: NAVY, bold: true })] }));
        children.push(new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-2", useAppliedParagraphOutlineLevel: true }));
      } else {
        children.push(heading(title, 1));
      }
      index += 1;
      continue;
    }
    if (line.startsWith("### ")) {
      children.push(heading(line.slice(4), 2));
      index += 1;
      continue;
    }
    if (line.startsWith("> ")) {
      children.push(makeCallout(line.slice(2)));
      children.push(new Paragraph({ spacing: { after: 100 } }));
      index += 1;
      continue;
    }
    if (/^\d+\.\s/.test(line)) {
      children.push(plainParagraph(line, { indent: { left: 420, hanging: 260 }, after: 85, line: 330 }));
      index += 1;
      continue;
    }
    if (line.startsWith("- ")) {
      children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 85, line: 330 }, children: [textRun(line.slice(2))] }));
      index += 1;
      continue;
    }

    const isMetadata = coverMode && (line.includes("院校") || line.includes("团队") || line.includes("成员") || line.includes("赛道") || line.includes("版本"));
    children.push(
      plainParagraph(line.replace(/\s{2,}$/g, ""), {
        alignment: isMetadata ? AlignmentType.LEFT : AlignmentType.JUSTIFIED,
        color: isMetadata ? MID_GREY : TEXT,
        size: isMetadata ? 22 : 21,
        after: isMetadata ? 100 : 130,
      }),
    );
    index += 1;
  }

  const document = new Document({
    creator: "LabGuard 团队",
    title: "LabGuard 实验室安全与资源协同管理平台商业计划书",
    description: "广东白云学院高教主赛道创意组商业计划书",
    features: { updateFields: true },
    styles: {
      default: { document: { run: { font: "Microsoft YaHei", size: 21, color: TEXT } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, paragraph: { outlineLevel: 0 }, run: { font: "Microsoft YaHei", size: 32, bold: true, color: NAVY } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, paragraph: { outlineLevel: 1 }, run: { font: "Microsoft YaHei", size: 25, bold: true, color: BLUE } },
      ],
    },
    numbering: {
      config: [
        { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 420, hanging: 260 } } } }] },
        { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 420, hanging: 260 } } } }] },
      ],
    },
    sections: [
      {
        properties: { page: { margin: { top: 1224, right: 1080, bottom: 1080, left: 1080 } } },
        headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [textRun("LabGuard ｜ 商业计划书", { size: 16, color: MID_GREY })] })] }) },
        footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 }, children: [textRun("广东白云学院  ｜  ", { size: 16, color: MID_GREY }), new TextRun({ children: [PageNumber.CURRENT], font: "Microsoft YaHei", size: 16, color: MID_GREY })] })] }) },
        children,
      },
    ],
  });

  return Packer.toBuffer(document).then((buffer) => {
    fs.writeFileSync(OUTPUT, buffer);
    console.log(OUTPUT);
  });
}

build().catch((error) => {
  console.error(error);
  process.exit(1);
});
