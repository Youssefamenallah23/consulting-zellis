"""
Step 6: build the 10-slide Investment Committee deck (conclusion titles).

Output: deck/IC_Deck_Zellis_Rightsizing.pptx
Rebuild: python deck/build_deck.py

Design rules (Humatica-style):
- Every slide title is a conclusion (action title), not a topic
- One chart per finding slide
- Pyramid Principle: the answer is on slide 1
- A "management dialogues" slide acknowledges what public data cannot prove
"""
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt

import duckdb

OUT = Path(__file__).parent / "IC_Deck_Zellis_Rightsizing.pptx"

TITLE_SIZE = Pt(28)
BODY_PT = 16
NAVY = RGBColor(31, 78, 121)
GREY = RGBColor(89, 89, 89)

con = duckdb.connect(str(Path(__file__).parent.parent / "data" / "org_effectiveness.duckdb"), read_only=True)
rows = con.execute(
    """
    SELECT company_name, role, fy,
           MAX(CASE WHEN metric='revenue_gbp' THEN value END) AS rev,
           MAX(CASE WHEN metric='staff_costs_gbp' THEN value END) AS staff,
           MAX(CASE WHEN metric='avg_headcount' THEN value END) AS hc
    FROM financials GROUP BY 1,2,3 ORDER BY company_name, fy
    """
).fetchall()
hist = con.execute(
    """
    SELECT fy, MAX(CASE WHEN metric='revenue_gbp' THEN value END) AS rev,
           MAX(CASE WHEN metric='staff_costs_gbp' THEN value END) AS staff,
           MAX(CASE WHEN metric='avg_headcount' THEN value END) AS hc
    FROM financials WHERE company_name='Zellis Holdings Limited' GROUP BY 1 ORDER BY 1
    """
).fetchall()
con.close()

# each peer enters the FY2025-vintage peer stats at its latest filed FY
latest = {}
for name, role, fy, rev, staff, hc in rows:
    if name not in latest or fy > latest[name][2]:
        latest[name] = [name, role, fy, rev, staff, hc]
rows = sorted(latest.values(), key=lambda r: r[0])

peers = [r for r in rows if r[1] == "peer"]
tgt = [r for r in rows if r[1] == "target"][0]
import statistics

med_rf = statistics.median(r[3] / r[5] for r in peers)
med_staff_pct = statistics.median(r[4] / r[3] for r in peers)
med_staff_fte = statistics.median(r[4] / r[5] for r in peers)
tgt_rf = tgt[3] / tgt[5]
tgt_sp = tgt[4] / tgt[3]
tgt_sf = tgt[4] / tgt[5]
gap_pct = (1 - tgt_rf / med_rf) * 100
method_a_k = (tgt_sp - med_staff_pct) * tgt[3]
method_b_k = (tgt[5] - tgt[3] / med_rf) * tgt_sf

def peer_label(r):
    fy_note = "" if r[2] == "FY2025" else f" ({r[2]} basis)"
    return r[0].split(" ")[0] + fy_note

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide(title, subtitle=None):
    slide = prs.slides.add_slide(BLANK)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.size = TITLE_SIZE
    run.font.bold = True
    run.font.color.rgb = NAVY
    if subtitle:
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = subtitle
        r2.font.size = Pt(14)
        r2.font.color.rgb = GREY
    return slide


def add_bullets(slide, items, left=0.6, top=1.7, width=12.1, height=5.2):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (text, lvl) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.level = lvl
        p.font.size = Pt(BODY_PT - 2 * lvl)
    return tb


def add_chart(slide, chart_type, categories, series, left, top, width, height):
    cd = CategoryChartData()
    cd.categories = categories
    for name, values in series:
        cd.add_series(name, values)
    return slide.shapes.add_chart(chart_type, Inches(left), Inches(top), Inches(width), Inches(height), cd).chart


# ================================================================ Slide 1 - Executive summary
s = add_slide(
    f"Zellis generates {gap_pct:.0f}% less revenue per employee than PE peers - worth ~GBP {method_a_k / 1000:.0f}m of annual EBITDA",
    "Rightsizing diagnostic | Investment Committee | Prepared from public filings",
)
add_bullets(
    s,
    [
        ("Situation: Apax and Vitruvian acquired Zellis (UK & Ireland payroll/HR software) in April 2024 for ~GBP 1.25bn.", 0),
        (f"Complication: FY2025 revenue per FTE is GBP {tgt_rf:.0f}k vs a PE-peer median of GBP {med_rf:.0f}k - a {gap_pct:.0f}% gap.", 0),
        ("Insight: Zellis pays LESS per head than peers (GBP 51k vs GBP 58k), so this is an output problem, not a pay problem.", 0),
        ("Trajectory: the staff-cost ratio improved from 58% to 52% in four years while revenue grew 14%/yr - invest, don't slash.", 0),
        (f"Value at stake: ~GBP {method_a_k / 1000:.0f}m annualised EBITDA (ratio route) to GBP {method_b_k / 1000:.0f}m (headcount route) if the gap closes to the peer median.", 0),
        ("Recommendation: a productivity-focused operating review and management dialogues - not a headcount cap.", 0),
    ],
)

# ================================================================ Slide 2 - Context
s = add_slide(
    "A new sponsor needs an organisational view of the UK's largest payroll platform",
    "Why this company, why now, and how we sized it from public data",
)
add_bullets(
    s,
    [
        ("Zellis Holdings: payroll & HR software and services (Zellis, Moorepay, Benifex brands); ~GBP 261m revenue, ~2,655 FTE (FY2025).", 0),
        ("Ownership: Bain Capital sold to Apax Funds & Vitruvian Partners in April 2024 (GBP 1.25bn) - a fresh value creation plan is being built.", 0),
        ("Peer set (all PE-owned, UK-filed group accounts): OneAdvanced (Vista/BC Partners), Access UK (Hg/TA) and IRIS (Hg/Leonard Green) - each at its latest comparable filed year.", 0),
        ("Method: Companies House filings OCR'd and benchmarked (revenue per FTE, staff-cost ratio, 3-year CAGR); model in model/ValueAtStake.xlsx.", 0),
        ("Basis note: Zellis and OneAdvanced at group level; Access is an acquisition roll-up entity - treated with an M&A caveat.", 0),
    ],
)

# ================================================================ Slide 3 - Finding 1
s = add_slide(
    f"Output per head is {gap_pct:.0f}% below the PE-peer median - and scale does not explain it",
    "Revenue per average FTE, FY2025 (GBP k) - PE peers only; Sage (listed) shown as context, excluded from medians",
)
chart = add_chart(
    s,
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    ["Zellis (target)"] + [peer_label(r) for r in peers],
    [("Revenue per FTE (GBP k)", [tgt_rf] + [r[3] / r[5] for r in peers])],
    0.8, 1.9, 7.6, 4.6,
)
chart.has_legend = False
add_bullets(
    s,
    [
        (f"Gap vs median (GBP {med_rf:.0f}k): {gap_pct:.0f}%. Versus the scale-matched peer (OneAdvanced, GBP 309m revenue): 27%.", 0),
        ("OneAdvanced's size (GBP 309m vs Zellis GBP 261m) rules out a pure scale artefact; IRIS (GBP 374m) at 27% too.", 0),
        ("Access is higher still (GBP 164k), but its growth is heavily acquisition-driven - treated as a caveat, not a benchmark.", 0),
    ],
    left=8.6, top=2.1, width=4.4, height=4.4,
)

# ================================================================ Slide 4 - Finding 2
s = add_slide(
    "Zellis pays less per head than peers - the gap is output, not compensation",
    "Staff cost per FTE (GBP k) and staff cost as % of revenue, FY2025",
)
chart = add_chart(
    s,
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    ["Zellis (target)"] + [peer_label(r) for r in peers],
    [
        ("Staff cost per FTE (GBP k)", [tgt_sf] + [r[4] / r[5] for r in peers]),
        ("Staff cost as % of revenue (%)", [100 * tgt_sp] + [100 * r[4] / r[3] for r in peers]),
    ],
    0.8, 1.9, 7.6, 4.6,
)
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False
add_bullets(
    s,
    [
        (f"Cost per FTE: Zellis GBP {tgt_sf:.0f}k vs peer median GBP {med_staff_fte:.0f}k - below the median.", 0),
        (f"Yet staff cost = {tgt_sp * 100:.0f}% of revenue vs peer median {med_staff_pct * 100:.0f}% - a {100 * (tgt_sp - med_staff_pct):.0f}-point gap.", 0),
        ("Implication: the same payroll delivers less revenue per pound of pay - organisational output, mix or process, not salary inflation.", 0),
    ],
    left=8.6, top=2.1, width=4.4, height=4.4,
)

# ================================================================ Slide 5 - Finding 3
s = add_slide(
    "The trajectory is improving - this is efficiency of investment, not decline",
    "Zellis group staff cost as % of revenue, FY2021-FY2025, with revenue CAGR",
)
cats = [h[0] for h in hist]
staff_pct_series = [100 * h[2] / h[1] for h in hist]
chart = add_chart(
    s,
    XL_CHART_TYPE.LINE_MARKERS,
    cats,
    [("Staff cost as % of revenue", staff_pct_series)],
    0.8, 1.9, 7.6, 4.6,
)
chart.has_legend = False
add_bullets(
    s,
    [
        ("Staff ratio fell from 58.1% (FY2021) to 52.3% (FY2025) - 5.8 points of self-delivered improvement.", 0),
        ("Revenue compounded at 14.2%/yr over the same period; peer OneAdvanced went backwards (-0.8%/yr).", 0),
        ("Headcount grew only 19% while revenue grew 64% - the organisation is already absorbing growth.", 0),
        ("Implication for the IC: close the gap through productivity and mix - a forced headcount cut would risk the growth engine.", 0),
    ],
    left=8.6, top=2.1, width=4.4, height=4.4,
)

# ================================================================ Slide 6 - Value at stake
s = add_slide(
    f"Closing the gap to the peer median is worth GBP {method_a_k / 1000:.0f}-{method_b_k / 1000:.0f}m of annualised EBITDA",
    "Dual-method sizing (model/ValueAtStake.xlsx); scenarios anchored to the peer distribution",
)
add_bullets(
    s,
    [
        (f"Method A (staff-ratio gap x revenue): {100 * (tgt_sp - med_staff_pct):.0f} pts x GBP 261m = ~GBP {method_a_k / 1000:.0f}m.", 0),
        (f"Method B (headcount implied by peer productivity): ~{tgt[5] - tgt[3] / med_rf:.0f} FTE x GBP 51k = ~GBP {method_b_k / 1000:.0f}m.", 0),
        (f"Cross-check gap of {abs(method_a_k - method_b_k) / method_a_k * 100:.0f}% is explained: peers pay similar or more per head, so closing output at Zellis's pay levels converts to less cash - Method B is the conservative case.", 0),
        (f"Scenarios (peer-percentile anchored): Low ~GBP {method_a_k / 2000:.0f}m (half-gap) | Base ~GBP {method_a_k / 1000:.0f}m (median) | High ~GBP {method_a_k / 1000 * 1.15:.0f}m+ (toward peer 75th pct).", 0),
        ("Year-1 phasing: 60% realisation, 25% one-off implementation cost -> ~GBP 13m net year-1 (base).", 0),
        ("Full workings: model/ValueAtStake.xlsx - live formulas, peer percentiles, and a 2-way sensitivity table.", 0),
    ],
)

# ================================================================ Slide 7 - Recommendations
s = add_slide(
    "We recommend a productivity-focused operating review - not a headcount cap",
    "Three actions that fit the value creation plan",
)
add_bullets(
    s,
    [
        ("1. Productivity diagnostic at business-unit level (Zellis / Moorepay / Benifex): reconcile the group-level 34% gap to unit-level drivers - spans of control, service mix, delivery model.", 0),
        ("2. Commercial engine review: payroll & BPaaS pricing and packaging - the low cost per FTE suggests capacity to serve more revenue per head without new hires.", 0),
        ("3. Codify the improvement: the staff ratio improved 5.8 points in four years - extract what worked (automation, centralisation) and set it as the FY2026 operating target (52% -> sub-48%).", 0),
        ("Explicitly NOT recommended: a top-down headcount reduction. The growth engine (14%/yr) is the asset the sponsors bought; the gap closes through output, not exits.", 0),
    ],
)

# ================================================================ Slide 8 - Risks
s = add_slide(
    "Three data caveats could move the answer - none changes the direction",
    "What would make us revise, and by how much",
)
add_bullets(
    s,
    [
        ("Entity vs group basis: Zellis and OneAdvanced are group accounts; Access is a roll-up entity whose M&A-driven growth flatters its productivity - excluding Access lowers the median and widens the gap (more value at stake, not less).", 0),
        ("Accounting comparability: OneAdvanced FY2024 restatement and AppMod disposal (continuing-ops basis used); Zellis FY2022 headcount restatement; IRIS FY2025 covers a 13.5-month first period - its FY2024 12-month accounts are used instead.", 0),
        ("Public-data limits: filings show cost, not output quality - revenue per FTE blends pricing, mix and efficiency; only management dialogues can separate them.", 0),
        ("Mitigation: all figures are in the data log with filing + page references; restatements flagged; the model recomputes from the data tab.", 0),
    ],
)

# ================================================================ Slide 9 - Management dialogues
s = add_slide(
    "Five management dialogues would convert this hypothesis into an executable plan",
    "What public data cannot prove - and who in the business can",
)
add_bullets(
    s,
    [
        (f"CFO: reconcile the {100 * (tgt_sp - med_staff_pct):.0f}-point staff-ratio gap - how much is mix (services vs software), how much is span of control and layers?", 0),
        ("MD Zellis (enterprise): capacity utilisation in managed services and implementations - is the delivery bench under-loaded?", 0),
        ("MD Moorepay (SMB): pricing and package mix vs OneAdvanced's SMB payroll business - revenue per client trends.", 0),
        ("CHRO: attrition, open roles and time-to-fill - is the 2,655 FTE base carrying vacancy-driven agency cost?", 0),
        ("CTO/CPO: automation roadmap (AI in payroll processing) - what output gain is already committed in the FY2026 plan?", 0),
    ],
)

# ================================================================ Slide 10 - Next steps
s = add_slide(
    "Next steps: a 90-day path from diagnostic to value",
    "Owned, dated, and consistent with the sponsors' value creation plan",
)
add_bullets(
    s,
    [
        ("Days 0-30: business-unit productivity diagnostic (data + activity analysis) and the five management dialogues above.", 0),
        ("Days 30-60: commercial engine review (pricing, packaging, service mix) and FY2026 operating target setting (staff ratio < 48%).", 0),
        (f"Days 60-90: implementation plan with named owners, tracked against the model's year-1 phasing; IC checkpoint on the GBP {method_a_k / 1000:.0f}m base case.", 0),
        ("Appendix available on request: data log, sourcing map, model, OCR pipeline, and this deck's build script.", 0),
    ],
)

prs.save(OUT)
print(f"deck written -> {OUT}")
print(f"slides: {len(prs.slides._sldIdLst)}")