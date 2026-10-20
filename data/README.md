# Data layer

## Pipeline (rebuild from scratch)

```
1. python data/pull_filings.py        # downloads accounts PDFs -> data/raw/, manifest -> data/manifest.csv
2. python data/extract_financials.py  # text-based PDFs (annual reports) -> extracted_hits.csv
3. python data/ocr_financials.py      # CH filings are image scans -> OCR with page cache -> ocr_text/, ocr_hits.csv
4. python data/_grep_ocr.py           # harvest key-term snippets from the OCR cache -> probe_out.txt
5. (human check) verify snippets against PDFs, write final numbers -> data/financials.csv
6. python data/load_duckdb.py         # builds org_effectiveness.duckdb (table: financials)
```

Files:

| File | What it is |
|---|---|
| `raw/*.pdf` | Filed accounts from Companies House (public documents) |
| `manifest.csv` | Every downloaded PDF: company, FY, description, source URL |
| `extracted_hits.csv` | Raw text snippets around key terms (proposal, not verified) |
| `financials.csv` | **The verified dataset** — one row per company × FY × metric |
| `org_effectiveness.duckdb` | DuckDB database for analysis in Step 4 |

## financials.csv schema

`company_number, company_name, role, fy, period_end, metric, value, unit, source_file, source_page, source_url, notes`

- **role:** `target` (Zellis) / `peer` (IRIS, OneAdvanced, Access) / `public_anchor` (Sage — listed, excluded from PE medians)
- **metric:** `revenue_gbp` (turnover) / `staff_costs_gbp` (wages+salaries+social security+pensions) / `avg_headcount` (average number of employees)
- **unit:** `GBP_m` for money, `count` for headcount
- Every value must cite `source_file` + `source_page` — no exceptions.

## Known data caveats (carried from the issue tree, Branch D)

1. **Different FY ends:** 30 Apr (Zellis, IRIS), 30 Jun (Access), 28 Feb (OneAdvanced), 30 Sep (Sage). Comparisons use FY labels; a ~2-month misalignment is accepted and noted.
2. **Entity vs group:** we use the **operating/trading entity** for Zellis (01587537) and IRIS (03196054), and the **consolidated group accounts** for OneAdvanced (05965280) and Access (02343760, which is the main trading entity of the Access Group). Where a consolidated group report exists outside CH (Zellis Holdings annual report, `zellis_uk_fy2025.pdf`), it is kept as a cross-check.
3. **OneAdvanced FY2023 was amended (AAMD)** — use the amended figures.
4. **Sage is a listed public company** (~10x larger than peers) — context anchor only, never in PE medians.

## Politeness & compliance

Public documents, fetched one per second with a descriptive User-Agent, small volume (31 files). This is normal use of public filings; no login-walled or bulk content.

## Ops note: don't melt the laptop (learned the hard way)

OCR is CPU-heavy. ONNX Runtime spawns one worker thread per core by default — a single OCR process took **99–100% of all 12 cores** and froze the machine. Controls now in place:

1. **CPU affinity** — the script pins itself to a subset of cores via `SetProcessAffinityMask` (env `OCR_AFFINITY`, default `0xF` = 4 cores). Two parallel instances use disjoint sets: `0xF` (cores 0–3, FY2025 files) and `0xF0` (cores 4–7, FY2024 files).
2. **Below-normal priority** — `SetPriorityClass(BELOW_NORMAL)`: the OS always gives your foreground apps the CPU first.
3. **Page cache** — `data/ocr_text/` stores every OCR'd page, so crashes/restarts never redo work (verified across 3 crashes).
4. Lesson: *always* check what a library's default thread behaviour is before running long jobs — "it uses all my cores" is the default, not the exception.