# 💼 Zellis Rightsizing Diagnostic

### Can a private-equity-owned company be over-staffed or under-productive — and what is that worth?

**A self-built consulting case study: an organisational-effectiveness diagnostic of a PE-backed UK company, benchmarked against its PE-owned peers — built entirely from public data.**

![Status](https://img.shields.io/badge/status-complete-brightgreen) ![Type](https://img.shields.io/badge/type-consulting_case_study-blue) ![Data](https://img.shields.io/badge/source-Companies_House-9cf) ![Model](https://img.shields.io/badge/model-live_formulas-yellow) ![Deck](https://img.shields.io/badge/deck-10_slides-orange)

---

## 📖 The one-paragraph version (for non-consultants)

**Zellis** runs payroll and HR software for UK businesses — think "the company that makes sure your salary arrives on payday". In 2024 it was bought by a **private equity (PE) fund** for ~£1.25bn. PE funds buy companies, improve them, and sell them for more — so they constantly ask one question: *is every pound we spend creating value?*

I asked that question about Zellis's **biggest cost after technology: its 2,655 employees**. I compared it against three similar PE-owned software companies using nothing but **public filings** (UK companies must publish annual accounts at Companies House — I downloaded and OCR'd ~2,000 pages of them). The result:

> **Zellis generates £98k of revenue per employee, while its PE-owned peers generate £135k — a 27% gap.**
> Closing it would be worth **£32–37m of profit a year**. But Zellis pays its people *less* than peers do, so the answer isn't "pay is too high" — it's that each employee's work converts into less revenue. And Zellis is already improving fast. So the recommendation is a **productivity review, not a headcount cut**.

---

## 🎯 The question (framed before any data was touched)

> *"Is Zellis over-staffed or under-productive versus its PE peers — and what is the EBITDA value at stake?"*

A good consulting question is **falsifiable**: I wrote down what data would *disprove* each hypothesis before looking. Three hypotheses, three kill tests — see [`analysis/step-1-framing.md`](analysis/step-1-framing.md).

---

## 📊 The result

| Metric | Zellis (target) | PE-peer median | Gap |
|---|---|---|---|
| Revenue per employee (FTE) | **£98.3k** | £135.3k | **−27.3%** 🔴 |
| Staff cost as % of revenue | **52.3%** | 40.0% | **+12.3 pts** 🔴 |
| Staff cost per employee | **£51.4k** | £54.0k | **−4.8%** 🟢 |

| Growth (revenue CAGR) | |
|---|---|
| Zellis | **+14.2%/yr** 🟢 |
| Access | +20%/yr (heavily acquisition-driven) |
| IRIS | +17.1%/yr |
| OneAdvanced | −0.8%/yr |

**Value at stake (two independent methods, agreeing within 16%):**
- Method A — staff-ratio gap × revenue: **£32.2m** annual EBITDA
- Method B — headcount implied by peer productivity × pay: **£37.3m**
- Scenarios (anchored to the peer distribution): **£16m / £32m / £37m+** · Year-1 phased: ~£13m net

---

## 🧭 Why we decided what we decided (the decision log)

This section is the actual thinking — the part tools can't do for you.

### Why Zellis as the target?
Three reasons, in order: **(1) Data** — it files full (non-abridged) accounts at Companies House every year, so revenue, staff costs and headcount are all public. **(2) Fresh PE ownership** — Apax & Vitruvian bought it in April 2024, so a "value creation plan" narrative is real, not invented. **(3) Story** — a payroll company being judged on its own staffing productivity makes the case memorable and honest.

### Why these three peers?
They had to be **PE-owned**, **in the same business** (payroll/HR/business software), **UK-filed**, and **file full accounts**. Many candidates failed the last test — small companies file "abridged" accounts that hide revenue. That's why **Sage** (listed, 10× larger) is shown as context but *excluded from the peer medians*: different scale, different disclosure.

### Why group accounts for Zellis & OneAdvanced, but entity accounts for Access?
Comparability. "Zellis UK Ltd" is only *half* of the Zellis group (£130m vs £261m) — benchmarking an entity against groups would be apples-to-oranges. So we used the **top-level consolidated accounts** for Zellis and OneAdvanced. Access's structure required its main trading entity, and IRIS's group accounts were found filed under an obscure Companies Act exemption (`PARENT_ACC`) — its 2025 accounts cover an unusual 13.5-month first period, so we used its clean 12-month FY2024 instead. **Every one of these choices is written down** — that's what makes a benchmark defensible.

### Why median, not average?
One unusual company would drag an *average* around. The **median is the "typical middle peer"** and is robust to outliers. We also report the interquartile range (the peer "normal band") — Zellis sits below even the 25th percentile, so the gap is not a marginal miss.

### Why revenue-per-employee AND staff-cost-ratio — two metrics, not one?
Public filings show what companies **spend** on people, not what each person *does*. Using both metrics together separates **pay** ("do we pay too much?") from **output** ("does each person produce enough?"). The punchline of this case comes from that separation: Zellis pays *less* per head than peers, so the 12-point staff-cost gap **cannot** be a pay problem — it's organisational output.

### Why two sizing methods (and a cross-check)?
One formula can be silently wrong. We sized the opportunity two independent ways — **(A)** close the staff-cost-ratio gap × revenue, and **(B)** the headcount reduction implied by peer productivity × pay — and checked they agree. They agree within 16%, *and the reason they differ is itself informative* (peers pay similar-or-more per head, so closing output at Zellis's pay levels converts to less cash). Method B is the conservative case.

### Why scenarios anchored to peer percentiles?
"Low = −20%, High = +10%" is arbitrary. Our Low/Base/High are **the peer 25th percentile, median, and 75th percentile** — every scenario has a data provenance an interviewer can audit.

### Why the recommendation is NOT a headcount cut?
The data: Zellis's staff ratio already improved **58% → 52% in four years** while revenue compounded at **14%/yr** and headcount grew only 19% against 64% revenue growth. Cutting heads would attack the growth engine the sponsors just bought. The gap closes through **output, mix and process** — hence a productivity operating review, validated in five named management dialogues (slide 9 of the deck).

### Why OCR ~2,000 pages?
Because Companies House filings are **image scans with no text layer** (we verified before building anything — half the "data analysis" on the internet dies exactly here). So we built a polite, page-cached OCR pipeline. Bonus finds along the way: a dormant shell company masquerading as a peer, three restatements, and a business quietly sold to IBM mid-period.

---

## 📁 Repository structure

```
├── README.md                        <- you are here
├── PLAN.md                          <- the 20-day engagement plan
├── glossary.md                      <- every acronym explained (PE, EBITDA, MECE, FTE…)
├── keyword-map.md                   <- job-description keywords -> proof artifacts
├── analysis/                        <- framing, peer selection, findings, metrics
├── data/
│   ├── data-log.md                  <- AUDIT TRAIL: sourced findings, each with a link
│   ├── financials.csv               <- 49 verified data rows (company, FY, metric, value, filing+page)
│   ├── manifest.csv                 <- every downloaded filing with its source URL
│   ├── org_effectiveness.duckdb     <- the analysis database
│   ├── pull_filings.py              # downloads accounts from Companies House (polite, cached)
│   ├── ocr_financials.py            # OCR pipeline (self-throttled, page-cached, crash-safe)
│   ├── analysis.py                  # productivity metrics
│   ├── build_model.py               # regenerates the Excel model with live formulas
│   ├── verify_model.py              # independent recomputation of every model number
│   ├── load_duckdb.py               # builds the database from financials.csv
│   └── ai_retrieval.py              # research accelerator: search filings, answers with citations
├── model/
│   ├── ValueAtStake.xlsx            <- LIVE-formula model (assumptions, dual-method, scenarios, sensitivity)
│   └── README.md                    <- model documentation
└── deck/
    ├── IC_Deck_Zellis_Rightsizing.pptx  <- 10-slide Investment Committee deck, conclusion titles
    ├── walkthrough_script.md            <- 5-minute narration script
    └── build_deck.py                    # regenerates the deck from the database
```

## 🔁 Rebuild everything in 8 commands

```bash
pip install openpyxl formulas duckdb pymupdf   # only needed once
python data/pull_filings.py        # download filings from Companies House (public, polite)
python data/ocr_financials.py      # OCR the scanned filings (self-throttled, cached)
python data/load_duckdb.py         # build the database from data/financials.csv
python data/analysis.py            # productivity metrics -> analysis/metrics.csv
python data/build_model.py         # rebuild the Excel model (live formulas)
python data/verify_model.py        # independent recomputation check
python deck/build_deck.py          # rebuild the deck from the database
python data/ai_retrieval.py "average number of employees"   # search filings with citations
```

`data/financials.csv` is the verified dataset: **48 rows across 16 company-years, each traceable to a filing and a page.**

## 🧪 What makes this trustworthy

- **Every number has a filing and a page number** (`data/financials.csv`, `data/data-log.md`)
- **The model is audited**: `verify_model.py` recalculates the workbook with an independent engine and asserts 24 cells against hand-computed values; the workbook's own 10 integrity checks must all read PASS
- **The deck was generated from the database** — no copy-paste drift between analysis, model and slides
- **Own weaknesses are documented**: entity-vs-group basis, restatements, a roll-up peer, public-data limits

## 📚 What I learned building this

- Companies House PDFs are image scans — verifying data *before* building tooling saves days
- A dormant holdings structure can hide the real trading entity (we nearly benchmarked a shell)
- Median over mean; percentiles over arbitrary scenarios; two methods over one
- ONNX Runtime uses **one thread per core by default** — always check library threading defaults before long jobs
- The best consulting insight isn't the gap — it's *what the gap is not* (pay, scale, decline)

---

*Built as a demonstration of structured analysis for a consulting application. All data is from public sources; all figures traceable to filings and page numbers. Zellis, OneAdvanced, Access and IRIS are used as public-data subjects only.*