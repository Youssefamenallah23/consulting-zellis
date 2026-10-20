# PLAN.md — 20-Day Org-Effectiveness Rightsizing Diagnostic

Framed as a Humatica-style engagement: the output is a memo + deck to the **Investment Committee (IC)** of a PE fund deciding whether (or how) to act on a portfolio company's staffing productivity gap.

## The vocabulary we mirror (from Humatica's own service pages)

- **Services:** Alignment & Activation · Operating Model Re-design · Commercial Engine Activation · **Rightsizing** · AI Operating Model · Due Diligence
- **Their language:** "case-for-change", "fact-based transparency on resource allocations", "scale-adjusted benchmarking", "top-down savings target", "management dialogues", "value creation plan"
- Their claim: **97% of PE respondents** say organizational issues delay realization of the investment plan. Their "Third Wave" thesis: value creation moved from financial engineering → operational excellence → **organizational excellence**.

## Steps

### Step 1 — Frame the question (Days 1–2) ✅
One-sentence IC question; MECE issue tree (4 branches incl. "data artefact"); 3 falsifiable hypotheses with kill tests. → `analysis/step-1-framing.md`

### Step 2 — Pick company & peers (Days 2–3)
- Target: PE-backed UK firm, £20–500m revenue, files **full (non-abridged) accounts**, ≥3 years data.
- 4–5 peers: same SIC code, same sector, mixed ownership (PE + public comps for context).
- PE-backing verified via deal press releases / fund portfolio pages.
- Data log started day 1 (`data/data-log.md`).

### Step 3 — Collect data (Days 4–7)
- Companies House API: revenue (turnover), staff costs, average headcount, period ends, account type.
- Job-posting counts: manual counts from public boards only (no scraping).
- Document: filing lags, UK audit-threshold changes, part-year periods, abridged accounts.

### Step 4 — Analyse (Days 8–11)
Metrics: revenue per FTE, staff cost % of revenue, staff cost per FTE, 3-yr CAGR.
Views: peer median + IQR, **scale-adjusted** (within revenue bands), 2×2 growth-vs-productivity map.
Output: 3 findings, each a full sentence with a number.

### Step 5 — Excel model (Days 12–14)
- Value at stake = **dual method**: (a) staff-cost-ratio gap × revenue, (b) headcount delta × cost per FTE. Methods must roughly agree.
- Scenarios anchored to peer percentiles (25th / median / 75th), not arbitrary %s.
- Live formulas only; visible assumptions tab; 2-way sensitivity (productivity gap × cost-to-implement).

### Step 6 — IC deck (Days 15–18)
10 slides, every title a conclusion. Exec summary · context · 3 finding slides (1 chart each) · recommendations · risks · **"What we would validate in management dialogues"** · next steps. Record a 5-minute walkthrough.

### Step 7 — AI accelerator (Days 19–20, optional)
Retrieval tool over filings, answers with citations. Framed as research acceleration supporting Humatica's **AI Operating Model** narrative — not the headline.

### Step 8 — Package
Excel + deck PDF + README + data log → GitHub → CV link (after Step 6 only).

## Quality bar
1. Every number has a source and an assumption note.
2. A stranger can rebuild the model from the README.
3. The recommendation fits in 3 sentences.
4. The "under-invested vs under-productive" alternative is tested, not assumed.

## Reading
- Barbara Minto, *The Pyramid Principle* (structure, exec summaries)
- Humatica: "Rightsizing the right way" (6 steps) & "The Third Wave" study
- Any free Excel financial-modelling course (scenarios + sensitivities)
- Practise 5–10 market-sizing cases out loud while building