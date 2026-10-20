# Org-Effectiveness Rightsizing Diagnostic

A self-built consulting case: a Humatica-style **Rightsizing / pre-deal organizational due diligence** of a PE-backed UK company, benchmarked against sector peers using public Companies House data.

**Target audience:** Humatica Business Analyst Intern application (London/Munich, 2027 start).
**The buyer of this analysis:** the Investment Committee of a (fictional) PE fund.

> Every number has a source and an assumption note. A stranger can rebuild this model from this README. The recommendation fits in 3 sentences.

## Project structure

```
consulting-case/
├── README.md          <- you are here
├── PLAN.md            <- the 20-day plan
├── glossary.md        <- every acronym & term, explained (read this first)
├── keyword-map.md     <- job description keywords -> proof artifacts
├── data/
│   └── data-log.md    <- log of every figure pulled (source + date)
├── analysis/
│   └── step-1-framing.md  <- question, issue tree, hypotheses
├── model/             <- Excel value-at-stake model (steps 5)
└── deck/              <- 10-slide IC deck (step 6)
```

## Status

| Step | Description | Days | Status |
|---|---|---|---|
| 1 | Frame the question | 1–2 | ✅ (`analysis/step-1-framing.md`) |
| 2 | Pick company & peers | 2–3 | ✅ (`analysis/step-2-company-peers.md`) |
| 3 | Collect data | 4–7 | ✅ (`data/` — 41 filings, OCR pipeline, DuckDB) |
| 4 | Analyse | 8–11 | ✅ (`analysis/step-4-analysis.md` + `data/metrics.csv`) |
| 5 | Excel model | 12–14 | ✅ (`model/ValueAtStake.xlsx`, live formulas, verified) |
| 6 | Client deck + walkthrough | 15–18 | ✅ (`deck/IC_Deck_Zellis_Rightsizing.pptx`; script: `deck/walkthrough_script.md`) |
| 7 | AI layer | 19–20 | ✅ (`data/ai_retrieval.py` — local retrieval with citations) |
| 8 | Package & publish | — | 🔄 git-ready; record walkthrough + push to GitHub, then update CV |

## Headline result (4-peer set, all sourced)

**Zellis generates £98.3k revenue per FTE vs a PE-peer median of £135.3k — a 27.3% gap.**
It pays *less* per head than peers (£51.4k vs £54.0k), so the gap is output, not pay — and the
staff ratio already improved 58.1% → 52.3% in four years while revenue compounded 14.2%/yr.
Value at stake: **£32.2m** (ratio route) to **£37.3m** (headcount route) annualised EBITDA; dual-method
cross-check agrees within 16%. Recommendation: a productivity-focused operating review — not a headcount cap.

## How to rebuild everything

```
python data/pull_filings.py        # download filings from Companies House (public, polite)
python data/ocr_financials.py      # OCR the scanned filings (self-throttled, page-cached)
python data/extract_financials.py  # text-based PDFs (annual reports)
python data/load_duckdb.py         # build the database from data/financials.csv
python data/analysis.py            # productivity metrics -> analysis/metrics.csv
python data/build_model.py         # rebuild model/ValueAtStake.xlsx (live formulas)
python data/verify_model.py        # independent recomputation check
python deck/build_deck.py          # rebuild the deck from the database
python data/ai_retrieval.py "average number of employees"   # research accelerator demo
```

`data/financials.csv` is the verified dataset (49 sourced rows — company, FY, metric, value, filing + page citation).
`data/data-log.md` is the audit trail. Heavy raw PDFs and the OCR page cache are git-ignored; everything analytical ships.