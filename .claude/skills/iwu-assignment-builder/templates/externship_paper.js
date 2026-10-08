// Externship-paper docx template (docx-js). Fill the CONFIG block, then: node externship_paper.js
// Style: Times New Roman 12pt, double-spaced body, centered title page, 2-col CLO table.
// Source pattern: UNV-501 Assignment 3.1 (Course 1, Term 3FA2026).
const { Document, Packer, Paragraph, TextRun, AlignmentType, PageBreak, Table, TableRow,
  TableCell, WidthType, VerticalAlign, ShadingType } = require("docx");
const fs = require("fs");

const CONFIG = {
  title: "Assignment 3.1: Externship Paper Course 1 Term 3FA2026",
  student: "Varsha Bhavandlapelli",
  school: "Indiana Wesleyan University",
  course: "UNV-501: Graduate CPT Seminar/Externship",
  instructor: "[Professor name not yet available]", // leave placeholder; never invent
  date: "October 25, 2026",
  courseLine: "MGMT-501: Foundations of Graduate Business",
  clos: [/* [courseOutcome, relationToJob] x N  -- outcomes from the pasted syllabus only */],
  applying: "",   // section C text (student's own words)
  proposal: "",   // section D text
  out: "UNV-501_Externship_Paper.docx",
};

const FONT = "Times New Roman", HEADER_FILL = "E8EEF7", W = 4680;
const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: 24, ...o });
const p = (c, o = {}) => new Paragraph({ children: c, spacing: { after: 200, line: 360 }, ...o });
const heading = (t) => new Paragraph({ spacing: { before: 240, after: 120 }, children: [run(t, { bold: true })] });
const cell = (t, hdr) => new TableCell({
  width: { size: W, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
  ...(hdr ? { shading: { type: ShadingType.CLEAR, fill: HEADER_FILL } } : {}),
  children: [new Paragraph({ children: [run(t, hdr ? { bold: true } : {})], spacing: { line: 300 } })] });
const center = (t, before = 0, bold = false) => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before, after: 240 }, children: [run(t, { bold })] });

const table = new Table({ width: { size: W * 2, type: WidthType.DXA }, columnWidths: [W, W], rows: [
  new TableRow({ tableHeader: true, children: [cell("Course Learning Outcomes (CLOs)", true), cell("Relationship/Application to Job", true)] }),
  ...CONFIG.clos.map(([a, b]) => new TableRow({ children: [cell(a), cell(b)] })) ] });

const doc = new Document({ sections: [{
  properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
  children: [
    center(CONFIG.title, 1600, true), center(CONFIG.student, 800), center(CONFIG.school),
    center(CONFIG.course), center(CONFIG.instructor), center(CONFIG.date),
    new Paragraph({ children: [new PageBreak()] }),
    heading("A. First Course This Term – Include the Course ID, Name and Instructor."), p([run(CONFIG.courseLine)]),
    heading("B. Outcomes Link to the Workplace"), table,
    heading("C. Applying Learning to Workplace Experience"), p([run(CONFIG.applying)]),
    heading("D. Work Proposal"), p([run(CONFIG.proposal)]),
  ] }] });

Packer.toBuffer(doc).then((b) => { fs.writeFileSync(CONFIG.out, b); console.log("wrote", CONFIG.out); });
