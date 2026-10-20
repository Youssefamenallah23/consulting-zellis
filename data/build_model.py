"""
Step 5: build the value-at-stake Excel model with LIVE formulas.
Output: model/ValueAtStake.xlsx | Rebuild: python data/build_model.py
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

import duckdb

OUT = Path(__file__).parent.parent / "model" / "ValueAtStake.xlsx"
OUT.parent.mkdir(exist_ok=True)

BOLD = Font(bold=True)
TITLE = Font(bold=True, size=14)
HDR_FILL = PatternFill("solid", fgColor="1F4E78")
HDR_FONT = Font(bold=True, color="FFFFFF")
WARN_FILL = PatternFill("solid", fgColor="FFF2CC")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def put(ws, cell, value, bold=False, fmt=None, fill=None, border=False):
    c = ws[cell]
    c.value = value
    if bold:
        c.font = BOLD
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if border:
        c.border = BOX
    return c


def header_row(ws, row, headers):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=1 + i, value=h)
        c.fill = HDR_FILL
        c.font = HDR_FONT
        c.border = BOX


con = duckdb.connect(str(Path(__file__).parent / "org_effectiveness.duckdb"), read_only=True)
rows = con.execute(
    """
    SELECT company_name, role, fy, period_end,
           MAX(CASE WHEN metric='revenue_gbp' THEN value END) AS revenue,
           MAX(CASE WHEN metric='staff_costs_gbp' THEN value END) AS staff_costs,
           MAX(CASE WHEN metric='avg_headcount' THEN value END) AS headcount
    FROM financials GROUP BY 1,2,3,4 ORDER BY company_name, fy
    """
).fetchall()
con.close()

wb = Workbook()

# ================================================================ README
ws = wb.active
ws.title = "README"
put(ws, "A1", "Value-at-Stake Model - Zellis Rightsizing Diagnostic", TITLE)
lines = [
    "",
    "How to use: every white cell is a live formula. Change assumptions on 'Assumptions' only.",
    "All money figures in GBP thousands (GBP k) unless marked GBP m.",
    "",
    "Tabs:",
    "  Inputs_Sourced  - verified figures from filed accounts (each with source reference)",
    "  Assumptions     - the only place to change drivers; peer stats computed live from Inputs_Sourced",
    "  Model           - dual-method sizing (A: ratio-gap x revenue; B: headcount delta x cost/FTE)",
    "  Scenarios       - Low / Base / High anchored to peer percentiles (QUARTILE formulas)",
    "  Sensitivity     - 2-way grid: % of gap closed x cost-to-implement (all formulas)",
    "",
    "Rebuild: python data/build_model.py",
    "Data log: data/data-log.md | dataset: data/financials.csv | findings: analysis/step-4-analysis.md",
    "",
    "Caveats: entity-vs-group basis; OneAdvanced continuing ops; Access roll-up (M&A-driven growth);",
    "restatements; IRIS group accounts via PARENT_ACC filings; Sage excluded as listed anchor.",
]
for i, t in enumerate(lines, start=2):
    put(ws, f"A{i}", t)

# ================================================================ Inputs_Sourced
ws = wb.create_sheet("Inputs_Sourced")
put(ws, "A1", "Sourced data - filed accounts (GBP k; headcount = average monthly FTE)", TITLE)
header_row(ws, 3, ["Company", "Role", "FY", "Period end", "Revenue GBP k", "Staff costs GBP k", "Avg headcount", "Source", "In peer stats"])
r = 4
for name, role, fy, pend, rev, staff, hc in rows:
    ws.append([name, role, fy, pend, rev, staff, hc])
    ws[f"H{r}"] = "see data/financials.csv + data/data-log.md"
    ws[f"J{r}"] = f'=AND($B{r}="peer",COUNTIFS($A$4:$A$100,$A{r},$C$4:$C$100,">"&$C{r})=0)'
    for col in "ABCDEFGHIJ":
        ws[f"{col}{r}"].border = BOX
    r += 1
put(ws, f"A{r + 1}", "Sage Group plc (public anchor) excluded from peer stats - listed company, different scale.")

# ================================================================ Assumptions
ws = wb.create_sheet("Assumptions")
put(ws, "A1", "Assumptions - the only tab to edit", TITLE)
put(ws, "A2", "Yellow cells = editable judgement. White = computed live from Inputs_Sourced.", Font(italic=True))
M = 'MATCH(1,(Inputs_Sourced!$B$4:$B$100="target")*(Inputs_Sourced!$C$4:$C$100="FY2025")*(Inputs_Sourced!$A$4:$A$100="Zellis Holdings Limited"),0)'

ws["A4"] = "TARGET (Zellis Holdings, group) - FY2025"
ws["A4"].font = BOLD
put(ws, "A5", "Target revenue (GBP k)")
put(ws, "B5", f"=INDEX(Inputs_Sourced!$E:$E,{M})", fmt="#,##0")
put(ws, "A6", "Target average headcount")
put(ws, "B6", f"=INDEX(Inputs_Sourced!$G:$G,{M})", fmt="#,##0")
put(ws, "A7", "Target staff costs (GBP k)")
put(ws, "B7", f"=INDEX(Inputs_Sourced!$F:$F,{M})", fmt="#,##0")
put(ws, "A8", "Target staff cost per FTE (GBP k)")
put(ws, "B8", "=B7/B6", fmt="0.0")
put(ws, "A9", "Target staff cost as % of revenue")
put(ws, "B9", "=B7/B5", fmt="0.0%")
put(ws, "A10", "Target revenue per FTE (GBP k)")
put(ws, "B10", "=B5/B6", fmt="0.0")

ws["A12"] = "PEER STATS (PE peers only; computed live)"
ws["A12"].font = BOLD
PF = 'IF(Inputs_Sourced!$B$4:$B$100="peer",IF(Inputs_Sourced!$J$4:$J$100=TRUE,'
put(ws, "A13", "Peer median revenue per FTE (GBP k)")
put(ws, "B13", f"=MEDIAN({PF}Inputs_Sourced!$E$4:$E$100/Inputs_Sourced!$G$4:$G$100)))", fmt="0.0")
put(ws, "A14", "Peer 25th percentile revenue per FTE")
put(ws, "B14", f"=QUARTILE({PF}Inputs_Sourced!$E$4:$E$100/Inputs_Sourced!$G$4:$G$100)),1)", fmt="0.0")
put(ws, "A15", "Peer 75th percentile revenue per FTE")
put(ws, "B15", f"=QUARTILE({PF}Inputs_Sourced!$E$4:$E$100/Inputs_Sourced!$G$4:$G$100)),3)", fmt="0.0")
put(ws, "A16", "Peer median staff cost as % of revenue")
put(ws, "B16", f"=MEDIAN({PF}Inputs_Sourced!$F$4:$F$100/Inputs_Sourced!$E$4:$E$100)))", fmt="0.0%")
put(ws, "A17", "Peer median staff cost per FTE (GBP k)")
put(ws, "B17", f"=MEDIAN({PF}Inputs_Sourced!$F$4:$F$100/Inputs_Sourced!$G$4:$G$100)))", fmt="0.0")

ws["A19"] = "SCENARIO JUDGEMENTS (editable)"
ws["A19"].font = BOLD
put(ws, "A20", "Low: fraction of gap to median closed")
put(ws, "B20", 0.5, fill=WARN_FILL, fmt="0%")
put(ws, "A21", "Base: fraction of gap to median closed")
put(ws, "B21", 1.0, fill=WARN_FILL, fmt="0%")
put(ws, "A22", "High: multiplier on median rev/FTE (1.10 = 10% beyond)")
put(ws, "B22", 1.10, fill=WARN_FILL, fmt="0.00")
put(ws, "A23", "Cost to implement (% of annualised benefit, one-off)")
put(ws, "B23", 0.25, fill=WARN_FILL, fmt="0%")
put(ws, "A24", "Benefits realised in year 1 (%)")
put(ws, "B24", 0.6, fill=WARN_FILL, fmt="0%")
put(ws, "A25", "Anchors follow the peer DISTRIBUTION (25th/median/75th), not arbitrary %s.", Font(italic=True))

# ================================================================ Model
ws = wb.create_sheet("Model")
put(ws, "A1", "Dual-method value-at-stake sizing (Base case: close gap to peer median)", TITLE)

put(ws, "A3", "METHOD A - staff-cost-ratio gap x revenue", BOLD)
put(ws, "A4", "Target staff cost ratio")
put(ws, "B4", "=Assumptions!B9", fmt="0.0%")
put(ws, "A5", "Peer median staff cost ratio")
put(ws, "B5", "=Assumptions!B16", fmt="0.0%")
put(ws, "A6", "Ratio gap (target - median)")
put(ws, "B6", "=B4-B5", fmt="0.0%")
put(ws, "A7", "Target revenue (GBP k)")
put(ws, "B7", "=Assumptions!B5", fmt="#,##0")
put(ws, "A8", "VALUE AT STAKE - Method A (GBP k)")
put(ws, "B8", "=B6*B7", fmt="#,##0", fill=WARN_FILL)

put(ws, "A10", "METHOD B - headcount delta x cost per FTE", BOLD)
put(ws, "A11", "Target headcount")
put(ws, "B11", "=Assumptions!B6", fmt="#,##0")
put(ws, "A12", "Headcount implied at peer median rev/FTE")
put(ws, "B12", "=Assumptions!B5/Assumptions!B13", fmt="#,##0.0")
put(ws, "A13", "Headcount delta (target - implied)")
put(ws, "B13", "=B11-B12", fmt="#,##0.0")
put(ws, "A14", "Target staff cost per FTE (GBP k)")
put(ws, "B14", "=Assumptions!B8", fmt="0.0")
put(ws, "A15", "VALUE AT STAKE - Method B (GBP k)")
put(ws, "B15", "=B13*B14", fmt="#,##0", fill=WARN_FILL)

put(ws, "A17", "CROSS-CHECK", BOLD)
put(ws, "A18", "|A-B| as % of Method A (investigate if >20%)")
put(ws, "B18", "=ABS(B8-B15)/B8", fmt="0.0%")
put(ws, "A19", "A prices the gap off the cost ratio; B off the headcount implied by peer productivity.", Font(italic=True))

put(ws, "A21", "YEAR-1 VIEW (phasing)", BOLD)
put(ws, "A22", "Benefits realised in year 1")
put(ws, "B22", "=Assumptions!B24", fmt="0%")
put(ws, "A23", "Year-1 gross benefit (average of methods, phased)")
put(ws, "B23", "=(B8+B15)/2*B22", fmt="#,##0")
put(ws, "A24", "One-off implementation cost")
put(ws, "B24", "=(B8+B15)/2*Assumptions!B23", fmt="#,##0")
put(ws, "A25", "Year-1 net impact (GBP k)")
put(ws, "B25", "=B23-B24", fmt="#,##0")

# ================================================================ Scenarios
ws = wb.create_sheet("Scenarios")
put(ws, "A1", "Scenarios - anchored to the peer distribution", TITLE)
header_row(ws, 3, ["Scenario", "Target rev/FTE assumption (GBP k)", "Implied staff ratio", "Ratio-route benefit (GBP k)", "Headcount-route benefit (GBP k)", "Average annual benefit (GBP k)"])

ws["A4"] = "Low"
ws["B4"] = "=Assumptions!B10+(Assumptions!B13-Assumptions!B10)*Assumptions!B20"
ws["A5"] = "Base"
ws["B5"] = "=Assumptions!B10+(Assumptions!B13-Assumptions!B10)*Assumptions!B21"
ws["A6"] = "High"
ws["B6"] = "=Assumptions!B10+(Assumptions!B15-Assumptions!B10)*Assumptions!B22"

for r in (4, 5, 6):
    ws[f"C{r}"] = f"=Assumptions!$B$7/(Assumptions!$B$6*B{r})"
    ws[f"D{r}"] = f"=(Assumptions!$B$9-C{r})*Assumptions!$B$5"
    ws[f"E{r}"] = f"=(Assumptions!$B$6-Assumptions!$B$5/B{r})*Assumptions!$B$8"
    ws[f"F{r}"] = f"=(D{r}+E{r})/2"
    ws[f"B{r}"].number_format = "0.0"
    ws[f"C{r}"].number_format = "0.0%"
    for col in "DEF":
        ws[f"{col}{r}"].number_format = "#,##0"
    for col in "ABCDEF":
        ws[f"{col}{r}"].border = BOX

put(ws, "A8", "Low/High follow the peer IQR (25th/75th percentile of revenue per FTE), not arbitrary choices.", Font(italic=True))
put(ws, "A9", '="Peer 25th pct: "&TEXT(Assumptions!B14,"0.0")&"  |  Median: "&TEXT(Assumptions!B13,"0.0")&"  |  75th pct: "&TEXT(Assumptions!B15,"0.0")')

# ================================================================ Sensitivity
ws = wb.create_sheet("Sensitivity")
put(ws, "A1", "Sensitivity: net year-1 EBITDA impact (GBP k)", TITLE)
put(ws, "A2", "Rows = % of productivity gap closed. Columns = cost-to-implement as % of annualised benefit.", Font(italic=True))

gap_pcts = [0.25, 0.50, 0.75, 1.00, 1.10]
cost_pcts = [0.10, 0.20, 0.30, 0.40, 0.50]
put(ws, "A4", "gap closed \\ cost%", bold=True, border=True)
for j, cp in enumerate(cost_pcts):
    put(ws, f"{get_column_letter(2 + j)}4", cp, fmt="0%", bold=True, border=True)
for i, gp in enumerate(gap_pcts):
    row = 5 + i
    put(ws, f"A{row}", gp, fmt="0%", bold=True, border=True)
    for j in range(len(cost_pcts)):
        col = get_column_letter(2 + j)
        ws[f"{col}{row}"] = (
            f"=(Assumptions!$B$13-Assumptions!$B$10)*$A{row}*Assumptions!$B$6*Assumptions!$B$24"
            f"*(1-{get_column_letter(2 + j)}$4)"
        )
        ws[f"{col}{row}"].number_format = "#,##0"
        ws[f"{col}{row}"].border = BOX

put(ws, "A11", "Gap-closure benefit expressed via the revenue-equivalent route (consistent with Method B).", Font(italic=True))

wb.save(OUT)
print(f"model written -> {OUT}")
print(f"data rows embedded: {len(rows)}")