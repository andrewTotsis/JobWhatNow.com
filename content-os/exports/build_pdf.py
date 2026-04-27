"""Render current Content OS state as a single PDF (personas + keywords + prioritization)."""
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports" / "content-os-state.pdf"

personas = json.loads((ROOT / "personas.json").read_text())["personas"]
kw_doc = json.loads((ROOT / "keywords.json").read_text())
keywords = kw_doc["keywords"]

styles = getSampleStyleSheet()
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=18, spaceAfter=10)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=13, spaceAfter=6)
body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=9, leading=11)
cell = ParagraphStyle("cell", parent=styles["BodyText"], fontSize=7.5, leading=9)
cell_b = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=landscape(LETTER),
    leftMargin=0.4 * inch, rightMargin=0.4 * inch,
    topMargin=0.5 * inch, bottomMargin=0.5 * inch,
    title="JobWhatNow Content OS — Current State",
)

story = []

# Cover
story.append(Paragraph("JobWhatNow Content OS — Current State", h1))
story.append(Paragraph(
    "Snapshot of the data tables driving the editorial pipeline as of the latest commit on "
    "<b>claude/fix-vercel-auth-NYWOs</b>. Includes 50 personas, 100 keyword seeds, and the "
    "prioritization rubric. The master ranked content table (100 article rows) has not been "
    "generated yet — that is the next deliverable.",
    body,
))
story.append(Spacer(1, 12))

# ---- Personas table ----
story.append(Paragraph("Table 1 — Personas (50)", h2))
header = ["ID", "Name", "Role", "Voice", "Evidence type", "Signature move"]
data = [[Paragraph(c, cell_b) for c in header]]
for p in personas:
    data.append([
        Paragraph(p["id"], cell),
        Paragraph(p["name"], cell),
        Paragraph(p["role"], cell),
        Paragraph(p["voice"], cell),
        Paragraph(p["evidence_type"], cell),
        Paragraph(p["signature_move"], cell),
    ])
col_widths = [0.4, 1.6, 1.7, 2.4, 1.9, 2.0]
col_widths = [w * inch for w in col_widths]
t = Table(data, colWidths=col_widths, repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(PageBreak())

# ---- Keywords table ----
story.append(Paragraph("Table 2 — Keyword Seeds (100)", h2))
legend = kw_doc["scoring_legend"]
legend_text = (
    f"<b>Volume</b>: {legend['search_volume_score']} &nbsp;&nbsp; "
    f"<b>Competition</b>: {legend['competition_score']} &nbsp;&nbsp; "
    f"<b>Emotional</b>: {legend['emotional_intensity_score']} &nbsp;&nbsp; "
    f"<b>Monetization</b>: {legend['monetization_intent_score']}"
)
story.append(Paragraph(legend_text, body))
story.append(Spacer(1, 6))

kw_header = ["ID", "Query", "Intent", "Vol", "Comp", "Emo", "Monet"]
kw_data = [[Paragraph(c, cell_b) for c in kw_header]]
for k in keywords:
    kw_data.append([
        Paragraph(k["id"], cell),
        Paragraph(k["query"], cell),
        Paragraph(k["intent"], cell),
        Paragraph(str(k["search_volume"]), cell),
        Paragraph(str(k["competition"]), cell),
        Paragraph(str(k["emotional"]), cell),
        Paragraph(str(k["monetization"]), cell),
    ])
kw_widths = [0.5, 4.5, 1.0, 0.55, 0.7, 0.55, 0.85]
kw_widths = [w * inch for w in kw_widths]
kw_table = Table(kw_data, colWidths=kw_widths, repeatRows=1)
kw_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ALIGN", (3, 1), (-1, -1), "CENTER"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(kw_table)
story.append(PageBreak())

# ---- Prioritization summary ----
story.append(Paragraph("Table 3 — Prioritization Rubric", h2))
formula_lines = [
    "priority_score =",
    "    (search_volume_score      * 0.25) +",
    "    ((11 - competition_score) * 0.20) +",
    "    (emotional_intensity_score* 0.20) +",
    "    (virality_score           * 0.15) +",
    "    (monetization_intent_score* 0.10) +",
    "    (recency_score            * 0.10)",
]
mono = ParagraphStyle("mono", parent=body, fontName="Courier", fontSize=9, leading=11)
for line in formula_lines:
    story.append(Paragraph(line.replace(" ", "&nbsp;"), mono))
story.append(Spacer(1, 8))

tier_header = ["Score", "Tier", "Action"]
tier_rows = [
    ["8.5+", "Lead", "Hand-craft. Senior persona. Original quotes. ~1,000 words."],
    ["7.0–8.4", "Core", "Templated draft → human pass. Standard persona rotation. ~700 words."],
    ["5.5–6.9", "Long-tail", "Templated. Light review. ~600 words."],
    ["<5.5", "Defer", "Park in the queue. Re-score quarterly."],
]
tier_data = [[Paragraph(c, cell_b) for c in tier_header]] + [
    [Paragraph(c, cell) for c in r] for r in tier_rows
]
tier_table = Table(tier_data, colWidths=[1.0 * inch, 1.2 * inch, 6.5 * inch], repeatRows=1)
tier_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(tier_table)
story.append(Spacer(1, 12))

story.append(Paragraph("Refresh cadence", h2))
refresh_rows = [
    ["Trend pieces (AI, layoffs, hiring stats)", "Quarterly"],
    ["Job role pages (demand outlook)", "Every 6 months"],
    ["Insights essays (evergreen-ish)", "Annually"],
    ["Guides (tactical)", "Annually + after major platform shifts"],
]
refresh_data = [[Paragraph("Content type", cell_b), Paragraph("Refresh cadence", cell_b)]] + [
    [Paragraph(c, cell) for c in r] for r in refresh_rows
]
refresh_table = Table(refresh_data, colWidths=[5.0 * inch, 3.5 * inch], repeatRows=1)
refresh_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(refresh_table)

doc.build(story)
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
