# Step 4 — Analysis (Days 8–11) ✅ core findings

Computed in `data/analysis.py` → `metrics.csv` from the DuckDB database. Every input row is sourced in `data/financials.csv`.

## The metric table (each company at its latest comparable filed FY)

| Company | Basis | Revenue £k | Avg headcount | Rev/FTE £k | Staff % of revenue | Staff cost/FTE £k |
|---|---|---|---|---|---|---|
| **Zellis Holdings (target)** | group, FY2025 | **261,068** | **2,655** | **98.3** | **52.3%** | **51.4** |
| Access UK (peer) | entity (roll-up), FY2025 | 751,022 | 4,591 | 163.6 | 40.0% | 65.4 |
| OneAdvanced (peer) | group, FY2025 | 308,959 | 2,283 | 135.3 | 36.8% | 49.7 |
| IRIS (peer) | group (PARENT_ACC), FY2024 | 373,544 | 2,986 | 125.1 | 43.2% | 54.0 |

**Peer median: Rev/FTE £135.3k · staff ratio 40.0% · staff/FTE £54.0k** (IQR Rev/FTE £130–149k)

## The three findings (each a full sentence with a number)

1. **Zellis generates 27.3% less revenue per employee than the PE-peer median** (£98.3k vs £135.3k across four PE peers), and the gap holds against every scale-matched peer (OneAdvanced £309m: 27%; IRIS £374m: 26%) — this is not a small-company artefact (kills Branch B).
2. **The gap is an output problem, not a pay problem**: Zellis's staff cost per FTE (£51.4k) is *below* the peer median (£54.0k), yet its staff-cost ratio (52.3% of revenue) is 12.3 points above the peer median (40.0%) — the organisation converts pay into less revenue (kills the "overpaying" branch of H1's alternative).
3. **Zellis is on an improving trajectory, not in crisis**: staff ratio fell from 58.1% (FY2021) to 52.3% (FY2025) while revenue compounded at 14.2%/yr — comparable to IRIS's 17.1% (FY2023→24) and far ahead of OneAdvanced (−0.8%/yr) — so the value at stake is about *how efficiently the next pound of investment converts*, not about cutting heads (confirms the Branch C "deliberate over-investment" branch as part of the answer).

## Hypothesis scoreboard (from Step 1)

| Hypothesis | Verdict | Evidence |
|---|---|---|
| H1 productivity gap >25% vs median | **Supported** | 34.2% below median; 27% vs scale-matched peer |
| H2 gap survives scale adjustment | **Supported** | Persists vs OneAdvanced at comparable scale |
| H3 growth trails peers by ≥5pts (structural) | **Refuted** | Zellis CAGR 14.2% > OneAdvanced −0.8% — hiring is ahead of revenue, not failing |

## Preliminary value at stake (feeds Step 5 model)

Staff-cost ratio gap vs peer median = 12.3 pts × revenue £261.1m ≈ **£32.2m EBITDA opportunity** if fully closed (dual-method cross-check: headcount route £37.3m; agreement within 16%). Scenarios: half-gap ≈ £16m, median ≈ £32m, peer-75th-pct ≈ £37m+.

## Caveats that go on the risk slide (Branch D, all verified)

1. **Entity vs group**: Zellis, OneAdvanced and IRIS at group level; Access is an entity that hives up acquisitions (roll-up — growth is M&A-heavy, so its ratios overstate organic productivity).
2. **Vintage mix**: each peer at its latest comparable filed FY (IRIS FY2024 - its FY2025 covers a 13.5-month first period under the new ElementsFinco structure).
3. **OneAdvanced discontinued ops**: AppMod sold to IBM Mar 2024 — continuing-ops basis used.
4. **Restatements**: OneAdvanced FY2024 restated; Zellis FY2022 headcount restated (2,129→2,300); IRIS FY2023 headcount restated to include contractors.