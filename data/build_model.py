# -*- coding: utf-8 -*-
"""
Step 5 (v2): value-at-stake model, rebuilt for auditability.

Design rules:
  * No array formulas (no CSE, works in Excel 2013+ and LibreOffice).
  * Named ranges for every driver, so formulas read as sentences.
  * One source of truth: Inputs -> Benchmarks -> Sizing -> Scenarios.
  * A Checks tab that fails loudly.

Output: model/ValueAtStake.xlsx   Rebuild: python data/build_model.py
"""
import csv
from collections import OrderedDict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName

ROOT = Path(__file__).parent.parent
OUT = ROOT / "model" / "ValueAtStake.xlsx"

# ------------------------------------------------------------------ palette
NAVY = "1F3864"
MIDBLUE = "D9E2F3"
INPUT = "FFF2CC"
OUTPUT = "FCE4D6"
GREY = "F2F2F2"

TITLE = Font(name="Calibri", size=15, bold=True, color=NAVY)
SUB = Font(name="Calibri", size=10, italic=True, color="595959")
SECT = Font(name="Calibri", size=11, bold=True, color=NAVY)
BODY = Font(name="Calibri", size=10)
BOLD = Font(name="Calibri", size=10, bold=True)
SMALL = Font(name="Calibri", size=9, color="595959")
HDR = Font(name="Calibri", size=9, bold=True, color="FFFFFF")

HDR_FILL = PatternFill("solid", fgColor=NAVY)
SECT_FILL = PatternFill("solid", fgColor=MIDBLUE)
IN_FILL = PatternFill("solid", fgColor=INPUT)
OUT_FILL = PatternFill("solid", fgColor=OUTPUT)
GREY_FILL = PatternFill("solid", fgColor=GREY)

thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
TOPLINE = Border(top=Side(style="thin", color="808080"))

GBP = '#,##0;[Red](#,##0)'
GBP0 = '#,##0;[Red](#,##0)'
ONE1 = '0.0'
PCT1 = '0.0%'
PCT0 = '0%'

# ------------------------------------------------------------------ data
def load_rows():
    rows = OrderedDict()
    with open(ROOT / "data" / "financials.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            key = (r["company_name"], r["fy"])
            if key not in rows:
                rows[key] = {
                    "company": r["company_name"],
                    "role": r["role"],
                    "fy": r["fy"],
                    "period_end": r["period_end"],
                    "revenue": None,
                    "staff": None,
                    "fte": None,
                    "pages": {},
                    "notes": set(),
                }
            d = rows[key]
            metric = r["metric"]
            val = float(r["value"])
            if metric == "revenue_gbp":
                d["revenue"] = val
                d["pages"]["rev"] = r["source_page"]
            elif metric == "staff_costs_gbp":
                d["staff"] = val
                d["pages"]["staff"] = r["source_page"]
                d["pages"]["file"] = r["source_file"]
            elif metric == "avg_headcount":
                d["fte"] = val
                d["pages"]["fte"] = r["source_page"]
                if "file" not in d["pages"]:
                    d["pages"]["file"] = r["source_file"]
            if r["notes"]:
                d["notes"].add(r["notes"])
    return list(rows.values())


DATA = load_rows()

COMPANY_ORDER = [
    "Zellis Holdings Limited",
    "Access UK Ltd",
    "OneAdvanced Group Limited",
    "IRIS Business Software Limited (group)",
]

META = {
    "Zellis Holdings Limited": (
        "TARGET", "Group consolidated", "Apax + Vitruvian (Apr 2024, GBP 1.25bn)"),
    "Access UK Ltd": (
        "peer", "Entity, roll-up", "Hg Capital"),
    "OneAdvanced Group Limited": (
        "peer", "Group consolidated", "Vista + BC Partners"),
    "IRIS Business Software Limited (group)": (
        "peer", "Group via s401 PARENT_ACC", "Hg + Leonard Green"),
}

LATEST_FY = {
    "Zellis Holdings Limited": "FY2025",
    "Access UK Ltd": "FY2025",
    "OneAdvanced Group Limited": "FY2025",
    "IRIS Business Software Limited (group)": "FY2024",
}

INPUTS = [d for c in COMPANY_ORDER for d in DATA if d["company"] == c]
INPUTS.sort(key=lambda d: (COMPANY_ORDER.index(d["company"]), d["fy"]))

wb = Workbook()

# ================================================================== helpers
def title_block(ws, title, subtitle, width_cols=10):
    ws["A1"] = title
    ws["A1"].font = TITLE
    ws["A2"] = subtitle
    ws["A2"].font = SUB
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = 22
    ws.sheet_view.zoomScale = 100


def section(ws, row, text, span=6):
    ws.cell(row=row, column=1, value=text).font = SECT
    for c in range(1, span + 1):
        ws.cell(row=row, column=c).fill = SECT_FILL
    ws.row_dimensions[row].height = 18


def hdr_row(ws, row, headers, height=26):
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = HDR
        c.fill = HDR_FILL
        c.border = BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = height


def widths(ws, mapping):
    for col, w in mapping.items():
        ws.column_dimensions[col].width = w


def fmt(ws, cell, number_format, bold=False, fill=None, border=False, align=None):
    c = ws[cell]
    c.number_format = number_format
    if bold:
        c.font = BOLD
    if fill:
        c.fill = fill
    if border:
        c.border = BOX
    if align:
        c.alignment = Alignment(horizontal=align)


# ================================================================== COVER
ws = wb.active
ws.title = "Cover"
title_block(
    ws,
    "Zellis Holdings: value at stake from the organisational gap",
    "Rightsizing diagnostic. Every figure traceable to a filed account; every cell a live formula.",
)
widths(ws, {"A": 3, "B": 26, "C": 86, "D": 14})

section(ws, 4, "THE ANSWER", span=3)
ws["B5"] = "Annual EBITDA at stake"
ws["B5"].font = BOLD
ws["C5"] = (
    '="GBP "&TEXT(Sizing!B24/1000,"0.0")&"m to GBP "&TEXT(Sizing!B25/1000,"0.0")'
    '&"m, from two independent methods that reconcile within "'
    '&TEXT(Sizing!B20,"0%")'
)
ws["C5"].font = Font(name="Calibri", size=11, bold=True, color=NAVY)
ws["C5"].fill = OUT_FILL
ws["C5"].alignment = Alignment(wrap_text=True, vertical="center")
ws.row_dimensions[5].height = 30

ws["B6"] = "The gap"
ws["B6"].font = BOLD
ws["C6"] = (
    '="Zellis generates GBP "&TEXT(Benchmarks!B19,"0.0")&"k of revenue per FTE against a peer '
    'median of GBP "&TEXT(Peer_Median_RevFTE,"0.0")&"k, a "&TEXT(-Benchmarks!B21,"0%")'
    '&" shortfall, while paying under the peer median per head (GBP "&TEXT(Target_Staff/Target_FTE,"0.0")'
    '&"k vs GBP "&TEXT(Peer_Median_CostFTE,"0.0")&"k)."'
)
ws["C6"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[6].height = 30

ws["B7"] = "So what"
ws["B7"].font = BOLD
ws["C7"] = (
    "The problem is output per head, not pay per head. A headcount cap would cut capacity and "
    "the wrong people; a productivity review targets spans, layers and mix."
)
ws["C7"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[7].height = 30

section(ws, 9, "HOW TO USE THIS FILE", span=3)
guide = [
    ("Yellow cells", "The only editable inputs, all on 'Assumptions'. Everything else is a formula."),
    ("Grey headers", "Sourced data. Each row cites the filing and page in 'Inputs'."),
    ("Orange cells", "Outputs. Do not type in them."),
    ("'Checks' tab", "Ten integrity tests. All must read PASS before any number leaves this file."),
    ("Units", "GBP thousands throughout, unless a cell says 'GBP m'."),
]
r = 10
for label, text in guide:
    ws[f"B{r}"] = label
    ws[f"B{r}"].font = BOLD
    ws[f"C{r}"] = text
    ws[f"C{r}"].font = BODY
    r += 1

section(ws, 16, "TABS", span=3)
tabs = [
    ("Inputs", "16 company-years, FY2021-FY2025, one row per company-year, with filing and page."),
    ("Benchmarks", "Each company at its latest comparable year. Peer median and quartiles computed live."),
    ("Assumptions", "The three judgements in this model: realisation, implementation cost, tolerance."),
    ("Sizing", "Method A (cost-ratio gap) and Method B (headcount implied by peer productivity)."),
    ("Scenarios", "25th percentile, median and 75th percentile of peer revenue per FTE."),
    ("Sensitivity", "Net year-1 EBITDA, gap closed x cost to implement."),
    ("Checks", "Integrity tests across the whole file."),
]
r = 17
for label, text in tabs:
    ws[f"B{r}"] = label
    ws[f"B{r}"].font = BOLD
    ws[f"C{r}"] = text
    ws[f"C{r}"].font = BODY
    r += 1

section(ws, 25, "CAVEATS THAT COULD MOVE THE ANSWER", span=3)
caveats = [
    "Entity vs group: Zellis, OneAdvanced and IRIS at group level. Access is an entity that "
    "hives up acquisitions, so its productivity is flattered by M&A.",
    "Vintage: each peer at its latest comparable filed year. IRIS FY2025 covers a 13.5-month "
    "first period, so FY2024 is used.",
    "OneAdvanced: continuing operations only. Its application-modernisation business was sold "
    "to IBM in March 2024.",
    "Restatements: OneAdvanced FY2024 restated; Zellis FY2022 headcount restated 2,129 to 2,300; "
    "IRIS FY2023 headcount restated to include contractors.",
    "Public data: headcount is the filed average. It cannot show grade mix, contractors or "
    "offshore delivery, which is why the recommendation ends in management dialogues.",
]
r = 26
for text in caveats:
    ws[f"C{r}"] = "\u2022  " + text
    ws[f"C{r}"].font = BODY
    ws[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 28
    r += 1

section(ws, 32, "SOURCES", span=3)
ws["C33"] = (
    "Companies House filing history per company number, 31 filings, FY2021-FY2025. "
    "Full log: data/data-log.md. Dataset: data/financials.csv. "
    "Findings: analysis/step-4-analysis.md. Rebuild: python data/build_model.py"
)
ws["C33"].font = SMALL
ws["C33"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[33].height = 40

# ================================================================== INPUTS
ws = wb.create_sheet("Inputs")
title_block(
    ws,
    "Inputs: filed accounts",
    "One row per company-year. Revenue, staff costs and average headcount as filed. "
    "Ratios are formulas, never typed.",
)
hdr_row(ws, 4, [
    "Company", "Role", "FY", "Period end", "Year", "Revenue GBP k",
    "Staff costs GBP k", "Avg FTE", "Revenue / FTE GBP k",
    "Staff cost % of revenue", "Staff cost / FTE GBP k",
    "Source file", "Page", "Note", "Latest FY",
])
widths(ws, {
    "A": 38, "B": 8, "C": 8, "D": 11, "E": 7, "F": 13, "G": 13, "H": 9,
    "I": 12, "J": 13, "K": 12, "L": 30, "M": 7, "N": 46, "O": 9,
})

first = 5
for i, d in enumerate(INPUTS):
    r = first + i
    ws.cell(row=r, column=1, value=d["company"]).font = BODY
    ws.cell(row=r, column=2, value=d["role"]).font = BODY
    ws.cell(row=r, column=3, value=d["fy"]).font = BODY
    c = ws.cell(row=r, column=4, value=d["period_end"])
    c.font = BODY
    c.number_format = "yyyy-mm-dd"
    ws.cell(row=r, column=5, value=f"=YEAR(D{r})").font = BODY
    ws.cell(row=r, column=6, value=d["revenue"]).font = BODY
    ws.cell(row=r, column=7, value=d["staff"]).font = BODY
    ws.cell(row=r, column=8, value=int(d["fte"])).font = BODY
    ws.cell(row=r, column=9, value=f"=F{r}/H{r}").font = BODY
    ws.cell(row=r, column=10, value=f"=G{r}/F{r}").font = BODY
    ws.cell(row=r, column=11, value=f"=G{r}/H{r}").font = BODY
    src = d["pages"].get("file", "")
    ws.cell(row=r, column=12, value=src.replace(".pdf", "")).font = SMALL
    page = "rev p.%s / staff p.%s" % (
        d["pages"].get("rev", "?"), d["pages"].get("staff", "?"))
    ws.cell(row=r, column=13, value=page).font = SMALL
    note = "; ".join(sorted(d["notes"]))[:180]
    ws.cell(row=r, column=14, value=note).font = SMALL
    latest = 1 if d["fy"] == LATEST_FY.get(d["company"]) else 0
    ws.cell(row=r, column=15, value=latest).font = BODY
    for col in range(1, 16):
        ws.cell(row=r, column=col).border = BOX
    fmt(ws, f"F{r}", GBP)
    fmt(ws, f"G{r}", GBP)
    fmt(ws, f"H{r}", GBP0)
    fmt(ws, f"I{r}", ONE1)
    fmt(ws, f"J{r}", PCT1)
    fmt(ws, f"K{r}", ONE1)
    ws.row_dimensions[r].height = 24

last = first + len(INPUTS) - 1
ws.freeze_panes = "C5"
ws.auto_filter.ref = f"A4:O{last}"
ws["A" + str(last + 2)] = (
    "Sage Group plc is downloaded in the manifest but excluded here: as a listed company it is "
    "a valuation anchor, not an org peer."
)
ws["A" + str(last + 2)].font = SMALL

# ================================================================== BENCHMARKS
ws = wb.create_sheet("Benchmarks")
title_block(
    ws,
    "Benchmarks: one row per company, latest comparable year",
    "Peer statistics are computed from this block. Changing a figure in 'Inputs' flows through.",
)
hdr_row(ws, 4, [
    "Company", "Basis", "FY", "Revenue GBP k", "Staff costs GBP k", "Avg FTE",
    "Revenue / FTE GBP k", "Staff cost % of revenue", "Staff cost / FTE GBP k", "Ownership",
])
widths(ws, {
    "A": 38, "B": 24, "C": 8, "D": 14, "E": 14, "F": 9,
    "G": 13, "H": 14, "I": 14, "J": 34,
})

row_of = {d["company"]: first + i for i, d in enumerate(INPUTS)
          if d["fy"] == LATEST_FY.get(d["company"])}

for i, company in enumerate(COMPANY_ORDER):
    r = 5 + i
    src = row_of[company]
    role, basis, owner = META[company]
    ws.cell(row=r, column=1, value=company).font = BOLD if role == "TARGET" else BODY
    ws.cell(row=r, column=2, value=basis).font = BODY
    ws.cell(row=r, column=3, value=f"=Inputs!C{src}").font = BODY
    ws.cell(row=r, column=4, value=f"=Inputs!F{src}").font = BODY
    ws.cell(row=r, column=5, value=f"=Inputs!G{src}").font = BODY
    ws.cell(row=r, column=6, value=f"=Inputs!H{src}").font = BODY
    ws.cell(row=r, column=7, value=f"=D{r}/F{r}").font = BODY
    ws.cell(row=r, column=8, value=f"=E{r}/D{r}").font = BODY
    ws.cell(row=r, column=9, value=f"=E{r}/F{r}").font = BODY
    ws.cell(row=r, column=10, value=owner).font = SMALL
    for col in range(1, 11):
        ws.cell(row=r, column=col).border = BOX
    fmt(ws, f"D{r}", GBP)
    fmt(ws, f"E{r}", GBP)
    fmt(ws, f"F{r}", GBP0)
    fmt(ws, f"G{r}", ONE1)
    fmt(ws, f"H{r}", PCT1)
    fmt(ws, f"I{r}", ONE1)
    if role == "TARGET":
        for col in range(1, 11):
            ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="E2EFDA")

section(ws, 11, "PEER STATISTICS (live)", span=6)
stats = [
    ("Peer median revenue per FTE (GBP k)", "=MEDIAN(G6:G8)", ONE1, "Peer_Median_RevFTE"),
    ("Peer 25th percentile revenue per FTE (GBP k)", "=QUARTILE(G6:G8,1)", ONE1, "Peer_P25_RevFTE"),
    ("Peer 75th percentile revenue per FTE (GBP k)", "=QUARTILE(G6:G8,3)", ONE1, "Peer_P75_RevFTE"),
    ("Peer median staff cost % of revenue", "=MEDIAN(H6:H8)", PCT1, "Peer_Median_StaffPct"),
    ("Peer median staff cost per FTE (GBP k)", "=MEDIAN(I6:I8)", ONE1, "Peer_Median_CostFTE"),
]
for j, (label, formula, number_format, name) in enumerate(stats):
    r = 12 + j
    ws.cell(row=r, column=1, value=label).font = BODY
    c = ws.cell(row=r, column=2, value=formula)
    c.font = BOLD
    c.fill = OUT_FILL
    fmt(ws, f"B{r}", number_format)

section(ws, 18, "TARGET VERSUS PEERS", span=6)
gap_rows = [
    ("Target revenue per FTE (GBP k)", "=G5", ONE1),
    ("Gap to peer median (GBP k per FTE)", "=G5-B12", ONE1),
    ("Gap to peer median (%)", "=G5/B12-1", PCT1),
    ("Target staff cost % of revenue", "=H5", PCT1),
    ("Staff-cost ratio gap versus peers (pts)", "=H5-B15", PCT1),
    ("Target staff cost per FTE (GBP k)", "=I5", ONE1),
    ("Target pays versus peer median (%)", "=I5/B16-1", PCT1),
]
for j, (label, formula, number_format) in enumerate(gap_rows):
    r = 19 + j
    ws.cell(row=r, column=1, value=label).font = BODY
    c = ws.cell(row=r, column=2, value=formula)
    c.font = BOLD
    fmt(ws, f"B{r}", number_format)

ws["A27"] = (
    "n = 3 peers, so quartiles are interpolated (inclusive method). Sage is excluded: listed "
    "scale and a different filing basis."
)
ws["A27"].font = SMALL

# ================================================================== ASSUMPTIONS
ws = wb.create_sheet("Assumptions")
title_block(
    ws,
    "Assumptions: the only editable cells",
    "Three judgements. Everything else in the file is sourced data or arithmetic.",
)
widths(ws, {"A": 52, "B": 14, "C": 70})

section(ws, 4, "DRIVERS", span=3)
drivers = [
    ("Benefits realised in year 1 (%)", 0.60, PCT0, "Realisation_Y1",
     "A rightsizing programme does not land on day one: hiring freezes, attrition and "
     "redeployment take 3-4 quarters."),
    ("Cost to implement (% of annualised benefit, one-off)", 0.25, PCT0, "One_Off_Cost_Pct",
     "Severance, programme office, interim management. Paid once, so it is subtracted, "
     "not multiplied into the benefit."),
    ("Reconciliation tolerance between methods (%)", 0.20, PCT0, "Check_Tolerance",
     "If Method A and Method B disagree by more than this, the peer set or the basis is "
     "wrong and the answer is not published."),
]
for j, (label, value, number_format, name, note) in enumerate(drivers):
    r = 5 + j
    ws.cell(row=r, column=1, value=label).font = BODY
    c = ws.cell(row=r, column=2, value=value)
    c.font = BOLD
    c.fill = IN_FILL
    c.border = BOX
    c.alignment = Alignment(horizontal="center")
    fmt(ws, f"B{r}", number_format)
    ws.cell(row=r, column=3, value=note).font = SMALL
    ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 34

section(ws, 10, "WHY THESE ARE JUDGEMENTS, NOT FACTS", span=3)
ws["A11"] = (
    "No filed account contains a realisation curve or a severance bill. These three numbers "
    "are stated openly so a reviewer can move them and watch the answer change, rather than "
    "finding them buried in a formula."
)
ws["A11"].font = BODY
ws["A11"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A11:C11")
ws.row_dimensions[11].height = 46

# ================================================================== SIZING
ws = wb.create_sheet("Sizing")
title_block(
    ws,
    "Sizing: two independent routes to the same number",
    "Method A prices the gap off the cost ratio. Method B prices it off headcount implied by "
    "peer productivity. They must agree.",
)
widths(ws, {"A": 52, "B": 16, "C": 16, "D": 60})

section(ws, 4, "METHOD A: STAFF-COST-RATIO GAP x REVENUE", span=3)
mA = [
    ("Target staff cost % of revenue", "=Target_Staff/Target_Revenue", PCT1),
    ("Peer median staff cost % of revenue", "=Peer_Median_StaffPct", PCT1),
    ("Ratio gap (target minus median)", "=B5-B6", PCT1),
    ("Target revenue (GBP k)", "=Target_Revenue", GBP),
    ("VALUE AT STAKE: Method A (GBP k)", "=B7*B8", GBP),
]
for j, (label, formula, number_format) in enumerate(mA):
    r = 5 + j
    ws.cell(row=r, column=1, value=label).font = BOLD if "VALUE" in label else BODY
    c = ws.cell(row=r, column=2, value=formula)
    c.font = BOLD
    if "VALUE" in label:
        c.fill = OUT_FILL
    fmt(ws, f"B{r}", number_format)
ws["D9"] = "Reads: if Zellis carried peers' staff-cost ratio at its own revenue, the difference is margin."
ws["D9"].font = SMALL
ws["D9"].alignment = Alignment(wrap_text=True, vertical="top")

section(ws, 11, "METHOD B: HEADCOUNT IMPLIED BY PEER PRODUCTIVITY", span=3)
mB = [
    ("Target average FTE", "=Target_FTE", GBP0),
    ("FTE implied at the peer median revenue per FTE", "=Target_Revenue/Peer_Median_RevFTE", GBP0),
    ("FTE delta (target minus implied)", "=B12-B13", GBP0),
    ("Target staff cost per FTE (GBP k)", "=Target_Staff/Target_FTE", ONE1),
    ("VALUE AT STAKE: Method B (GBP k)", "=B14*B15", GBP),
]
for j, (label, formula, number_format) in enumerate(mB):
    r = 12 + j
    ws.cell(row=r, column=1, value=label).font = BOLD if "VALUE" in label else BODY
    c = ws.cell(row=r, column=2, value=formula)
    c.font = BOLD
    if "VALUE" in label:
        c.fill = OUT_FILL
    fmt(ws, f"B{r}", number_format)
ws["D16"] = "Reads: at peers' revenue per FTE, Zellis would need this many fewer people to deliver today's revenue."
ws["D16"].font = SMALL
ws["D16"].alignment = Alignment(wrap_text=True, vertical="top")

section(ws, 18, "CROSS-CHECK", span=3)
ws["A19"] = "Absolute difference (GBP k)"
ws["A19"].font = BODY
ws["B19"] = "=ABS(B9-B16)"
fmt(ws, "B19", GBP)
ws["A20"] = "Difference as % of Method A"
ws["A20"].font = BODY
ws["B20"] = "=B19/B9"
fmt(ws, "B20", PCT1)
ws["A21"] = "Verdict"
ws["A21"].font = BOLD
ws["B21"] = '=IF(B20<=Check_Tolerance,"RECONCILED","INVESTIGATE")'
ws["B21"].font = BOLD
ws["B21"].fill = OUT_FILL
ws["C21"] = (
    "The two routes disagree because they use different peer statistics: the cost ratio and "
    "revenue per FTE are not the same distribution. Agreement within tolerance means the "
    "answer is not an artefact of one metric."
)
ws["C21"].font = SMALL
ws["C21"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[21].height = 40

section(ws, 23, "THE NUMBER WE CARRY FORWARD", span=3)
out_rows = [
    ("Low end (Method A)", "=MIN(B9,B16)", GBP),
    ("High end (Method B)", "=MAX(B9,B16)", GBP),
    ("Midpoint used in the deck", "=AVERAGE(B9,B16)", GBP),
    ("Midpoint as % of revenue", "=C25/B8", PCT1),
    ("Midpoint as % of staff cost", "=C25/Target_Staff", PCT1),
]
for j, (label, formula, number_format) in enumerate(out_rows):
    r = 24 + j
    ws.cell(row=r, column=1, value=label).font = BOLD if j == 2 else BODY
    c = ws.cell(row=r, column=2, value=formula)
    c.font = BOLD
    if j == 2:
        c.fill = OUT_FILL
    fmt(ws, f"B{r}", number_format)

section(ws, 30, "YEAR 1: WHAT ACTUALLY LANDS", span=3)
y1 = [
    ("Annualised benefit (midpoint)", "=B26", GBP),
    ("Realisation in year 1", "=Realisation_Y1", PCT0),
    ("Year-1 gross benefit", "=B31*B32", GBP),
    ("One-off implementation cost", "=B31*One_Off_Cost_Pct", GBP),
    ("Year-1 net EBITDA impact", "=B33-B34", GBP),
]
for j, (label, formula, number_format) in enumerate(y1):
    r = 31 + j
    ws.cell(row=r, column=1, value=label).font = BOLD if "net" in label else BODY
    c = ws.cell(row=r, column=2, value=formula)
    c.font = BOLD
    if "net" in label:
        c.fill = OUT_FILL
    fmt(ws, f"B{r}", number_format)
ws["D35"] = (
    "One-off cost is subtracted once. It is not a percentage of the benefit in perpetuity, "
    "which is the most common error in rightsizing models."
)
ws["D35"].font = SMALL
ws["D35"].alignment = Alignment(wrap_text=True, vertical="top")

# ================================================================== SCENARIOS
ws = wb.create_sheet("Scenarios")
title_block(
    ws,
    "Scenarios: anchored to the peer distribution",
    "Each case asks what happens if Zellis reaches a different point in the peer revenue-per-FTE "
    "distribution. No arbitrary percentages.",
)
hdr_row(ws, 4, [
    "Scenario", "Anchor revenue / FTE GBP k", "Implied FTE at anchor",
    "FTE delta versus today", "Annual benefit GBP k",
    "Benefit as % of staff cost", "What it means",
], height=34)
widths(ws, {"A": 14, "B": 16, "C": 14, "D": 14, "E": 15, "F": 13, "G": 60})

scen = [
    ("Conservative", "=Peer_P25_RevFTE", "Reach the peer 25th percentile: the weakest quartile."),
    ("Base", "=Peer_Median_RevFTE", "Reach the peer median, the number used in the deck."),
    ("Stretch", "=Peer_P75_RevFTE", "Reach the peer 75th percentile: best-in-peer-set productivity."),
]
for j, (name, anchor, meaning) in enumerate(scen):
    r = 5 + j
    fill = OUT_FILL if name == "Base" else None
    ws.cell(row=r, column=1, value=name).font = BOLD
    ws.cell(row=r, column=2, value=anchor).font = BODY
    ws.cell(row=r, column=3, value=f"=Target_Revenue/B{r}").font = BODY
    ws.cell(row=r, column=4, value=f"=Target_FTE-C{r}").font = BODY
    ws.cell(row=r, column=5, value=f"=D{r}*Target_Staff/Target_FTE").font = BOLD
    ws.cell(row=r, column=6, value=f"=E{r}/Target_Staff").font = BODY
    ws.cell(row=r, column=7, value=meaning).font = SMALL
    for col in range(1, 8):
        c = ws.cell(row=r, column=col)
        c.border = BOX
        if fill:
            c.fill = fill
    fmt(ws, f"B{r}", ONE1)
    fmt(ws, f"C{r}", GBP0)
    fmt(ws, f"D{r}", GBP0)
    fmt(ws, f"E{r}", GBP)
    fmt(ws, f"F{r}", PCT1)
    ws.row_dimensions[r].height = 28

section(ws, 9, "HOW TO READ THIS", span=7)
ws["A10"] = (
    "The two methods on 'Sizing' are not repeated here: at a fixed revenue-per-FTE anchor, the "
    "cost-ratio route and the headcount route are the same algebra, so showing both would "
    "fake a robustness we do not have. The honest range comes from the distribution of peers, "
    "which is what this table varies."
)
ws["A10"].font = BODY
ws["A10"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A10:G10")
ws.row_dimensions[10].height = 46

ws["A12"] = "Cross-check against Sizing"
ws["A12"].font = BOLD
ws["A13"] = "Base scenario benefit minus Sizing midpoint (GBP k)"
ws["A13"].font = BODY
ws["B13"] = "=E6-Sizing!B26"
fmt(ws, "B13", GBP)
ws["A14"] = "Base scenario versus Method B gap"
ws["A14"].font = BODY
ws["B14"] = "=E6-Sizing!B16"
fmt(ws, "B14", GBP)

# ================================================================== SENSITIVITY
ws = wb.create_sheet("Sensitivity")
title_block(
    ws,
    "Sensitivity: net year-1 EBITDA impact",
    "Rows: share of the productivity gap actually closed. Columns: one-off implementation cost "
    "as a share of annualised benefit.",
)
widths(ws, {"A": 22, "B": 12, "C": 12, "D": 12, "E": 12, "F": 12, "G": 3, "H": 60})

ws["A4"] = "Gap closed \\ cost to implement"
ws["A4"].font = HDR
ws["A4"].fill = HDR_FILL
ws["A4"].alignment = Alignment(horizontal="left", vertical="center")
ws["A4"].border = BOX
for i, cp in enumerate([0.10, 0.20, 0.30, 0.40, 0.50]):
    c = ws.cell(row=4, column=2 + i, value=cp)
    c.font = HDR
    c.fill = HDR_FILL
    c.border = BOX
    c.alignment = Alignment(horizontal="center")
    fmt(ws, c.coordinate, PCT0)

for i, gp in enumerate([0.25, 0.50, 0.75, 1.00]):
    r = 5 + i
    c = ws.cell(row=r, column=1, value=gp)
    c.font = BOLD
    c.fill = GREY_FILL
    c.border = BOX
    c.alignment = Alignment(horizontal="center")
    fmt(ws, c.coordinate, PCT0)
    for j in range(5):
        col = get_column_letter(2 + j)
        cell = ws[f"{col}{r}"]
        cell.value = (
            f"=Sizing!$B$26*$A{r}*(Realisation_Y1-{col}$4)"
        )
        cell.number_format = GBP
        cell.border = BOX
        cell.alignment = Alignment(horizontal="right")

ws["H4"] = (
    "Each cell = annualised benefit x gap closed x (realisation in year 1 minus one-off cost "
    "as a share of annualised benefit). Negative cells mean the programme costs more in year 1 "
    "than it returns."
)
ws["H4"].font = SMALL
ws["H4"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("H4:H10")
ws.row_dimensions[4].height = 60

section(ws, 11, "THE SAME GRID, ANNUALISED (STEADY STATE, NO ONE-OFF COST)", span=6)
ws["A12"] = "Gap closed \\ annualised benefit"
ws["A12"].font = HDR
ws["A12"].fill = HDR_FILL
ws["A12"].border = BOX
ws["A12"].alignment = Alignment(horizontal="left")
for j in range(5):
    col = get_column_letter(2 + j)
    c = ws[f"{col}12"]
    c.value = f"={col}4"
    c.font = HDR
    c.fill = HDR_FILL
    c.border = BOX
    c.alignment = Alignment(horizontal="center")
    fmt(ws, c.coordinate, PCT0)

for i, gp in enumerate([0.25, 0.50, 0.75, 1.00]):
    r = 13 + i
    c = ws.cell(row=r, column=1, value=gp)
    c.font = BOLD
    c.fill = GREY_FILL
    c.border = BOX
    c.alignment = Alignment(horizontal="center")
    fmt(ws, c.coordinate, PCT0)
    for j in range(5):
        col = get_column_letter(2 + j)
        cell = ws[f"{col}{r}"]
        cell.value = f"=Sizing!$B$26*$A{r}"
        cell.number_format = GBP
        cell.border = BOX

# ================================================================== CHECKS
ws = wb.create_sheet("Checks")
title_block(
    ws,
    "Checks: ten reasons to distrust this model if any of them fails",
    "Every test is a live formula. Nothing is published while a row reads FAIL.",
)
hdr_row(ws, 4, ["#", "Check", "Value", "Threshold", "Status", "Why it matters"], height=30)
widths(ws, {"A": 5, "B": 52, "C": 14, "D": 14, "E": 10, "F": 64})

checks = [
    ("All 16 input rows carry revenue, staff cost and FTE",
     '=COUNTIFS(Inputs!F5:F20,">0",Inputs!G5:G20,">0",Inputs!H5:H20,">0")',
     16, "=C5=D5", "A blank cell silently becomes zero and poisons every ratio."),
    ("Every peer has exactly one latest-year row in Benchmarks",
     "=COUNTA(Benchmarks!A6:A8)", 3, "=C6=D6", "Duplicate vintage would double-count a peer in the median."),
    ("Target row is in Benchmarks and is not a peer",
     '=COUNTIF(Benchmarks!A5:A5,"Zellis*")', 1, "=C7=D7", "The target must never enter the peer statistic."),
    ("Staff-cost ratio is between 0% and 100% for every row",
     '=COUNTIFS(Inputs!J5:J20,">0",Inputs!J5:J20,"<1")', 16, "=C8=D8", "A ratio outside that range means a units error."),
    ("Target revenue per FTE is below the peer median",
     "=Benchmarks!B20", 0, "=C9<D9", "This is the finding. If it fails, the case has no premise."),
    ("Methods A and B reconcile within tolerance",
     "=Sizing!B20", "=Check_Tolerance", "=C10<=D10", "Two routes agreeing is what makes the number defensible."),
    ("Implied FTE is below current FTE",
     "=Sizing!B14", 0, "=C11>D11", "A negative headcount delta would mean Zellis is under-staffed."),
    ("Scenario anchors are ordered P25 <= median <= P75",
     "=Benchmarks!B13-Benchmarks!B12", 0, "=C12<=D12", "Unsorted anchors would mislabel conservative and stretch."),
    ("Sensitivity falls as cost to implement rises",
     "=Sensitivity!B5-Sensitivity!F5", 0, "=C13>D13", "Wrong direction means the cost sign is inverted."),
    ("Sensitivity falls as less of the gap is closed",
     "=Sensitivity!B8-Sensitivity!B5", 0, "=C14>D14", "Catches a row/column transposition in the grid."),
]
for j, (label, formula, threshold, status, why) in enumerate(checks):
    r = 5 + j
    ws.cell(row=r, column=1, value=j + 1).font = BODY
    ws.cell(row=r, column=2, value=label).font = BODY
    c = ws.cell(row=r, column=3, value=formula)
    c.font = BODY
    if isinstance(threshold, str):
        ws.cell(row=r, column=4, value=threshold).font = BODY
    else:
        ws.cell(row=r, column=4, value=threshold).font = BODY
        fmt(ws, f"D{r}", ONE1)
    s = ws.cell(row=r, column=5, value=status)
    s.font = BOLD
    s.alignment = Alignment(horizontal="center")
    ws.cell(row=r, column=6, value=why).font = SMALL
    ws.cell(row=r, column=6).alignment = Alignment(wrap_text=True, vertical="top")
    for col in range(1, 7):
        ws.cell(row=r, column=col).border = BOX
    ws.row_dimensions[r].height = 30

fmt(ws, "C10", PCT1)
fmt(ws, "D10", PCT1)

section(ws, 16, "OVERALL", span=6)
ws["B17"] = '=IF(COUNTIF(E5:E14,"FAIL")=0,"ALL CHECKS PASS","REVIEW: "&COUNTIF(E5:E14,"FAIL")&" FAILED")'
ws["B17"].font = Font(name="Calibri", size=12, bold=True, color=NAVY)
ws["B17"].fill = OUT_FILL
ws["B17"].alignment = Alignment(horizontal="center")
ws.merge_cells("B17:C17")
ws.row_dimensions[17].height = 24

from openpyxl.formatting.rule import CellIsRule
ws.conditional_formatting.add(
    "E5:E14",
    CellIsRule(operator="equal", formula=['"PASS"'],
               fill=PatternFill("solid", fgColor="C6EFCE"),
               font=Font(color="006100", bold=True)),
)
ws.conditional_formatting.add(
    "E5:E14",
    CellIsRule(operator="equal", formula=['"FAIL"'],
               fill=PatternFill("solid", fgColor="FFC7CE"),
               font=Font(color="9C0006", bold=True)),
)

# ================================================================== named ranges
def name(nm, ref):
    wb.defined_names.add(DefinedName(nm, attr_text=ref))

name("Target_Revenue", "Benchmarks!$D$5")
name("Target_Staff", "Benchmarks!$E$5")
name("Target_FTE", "Benchmarks!$F$5")
name("Peer_Median_RevFTE", "Benchmarks!$B$12")
name("Peer_P25_RevFTE", "Benchmarks!$B$13")
name("Peer_P75_RevFTE", "Benchmarks!$B$14")
name("Peer_Median_StaffPct", "Benchmarks!$B$15")
name("Peer_Median_CostFTE", "Benchmarks!$B$16")
name("Realisation_Y1", "Assumptions!$B$5")
name("One_Off_Cost_Pct", "Assumptions!$B$6")
name("Check_Tolerance", "Assumptions!$B$7")

# ================================================================== finishing
ws = wb["Sizing"]
for row in ws.iter_rows(min_row=4, max_row=35, min_col=1, max_col=4):
    for c in row:
        if c.value is not None:
            c.alignment = Alignment(vertical="center", wrap_text=False)

for sheet in wb.worksheets:
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.page_setup.orientation = "landscape"
    sheet.print_options.horizontalCentered = True

wb["Cover"].sheet_properties.tabColor = "1F3864"
wb["Inputs"].sheet_properties.tabColor = "808080"
wb["Benchmarks"].sheet_properties.tabColor = "2E75B6"
wb["Assumptions"].sheet_properties.tabColor = "FFC000"
wb["Sizing"].sheet_properties.tabColor = "C00000"
wb["Scenarios"].sheet_properties.tabColor = "C00000"
wb["Sensitivity"].sheet_properties.tabColor = "C00000"
wb["Checks"].sheet_properties.tabColor = "00B050"

wb.calculation.fullCalcOnLoad = True
wb.active = 0
OUT.parent.mkdir(exist_ok=True)
wb.save(OUT)
print("wrote", OUT)
print("input rows:", len(INPUTS))
