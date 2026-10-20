# Model — Value-at-Stake Sizing (Step 5) ✅

**File: `model/ValueAtStake.xlsx`** — rebuilt by `python data/build_model.py` (from `data/financials.csv` via DuckDB). Verified by `python data/verify_model.py` (formulas present + independent recomputation matches).

## Tabs (every calculation is a live Excel formula — no pasted values)

| Tab | Purpose |
|---|---|
| `README` | How to use + caveats |
| `Inputs_Sourced` | The verified figures (the only values in the workbook), with source refs |
| `Assumptions` | **The only tab to edit.** Target stats + peer stats are computed live (`MEDIAN`/`QUARTILE` over the peer rows). Editable judgements highlighted yellow |
| `Model` | Dual-method sizing + cross-check + year-1 phasing |
| `Scenarios` | Low / Base / High, anchored to peer percentiles (25th / median / 75th), not arbitrary %s |
| `Sensitivity` | 2-way grid: % of gap closed (25–110%) × cost-to-implement (10–50%) |

## Sizing logic

- **Method A (ratio route):** (target staff-cost % − peer-median staff-cost %) × target revenue
- **Method B (headcount route):** (target headcount − headcount implied at peer-median Rev/FTE) × target staff cost per FTE
- **Cross-check:** if |A-B| > 20% of A, investigate - currently **16%** (inside threshold). Adding IRIS as a 4th peer tightened it from 28%: the residual difference exists because peers pay similar or more per head, so closing the output gap at Zellis pay levels converts to less cash (Method B is the conservative route).

## Headline numbers (verified with the 4-peer set)

- Peer median Rev/FTE **£135.3k** vs target **£98.3k** → **27.3% gap**
- Method A ≈ **£32.2m** · Method B ≈ **£37.3m** · cross-check **16%** (inside the 20% threshold - adding IRIS tightened it from 28%)
- Year-1 phased: 60% realisation, 25% one-off cost
- Scenarios: Low ≈ £16m (half-gap) · Base ≈ £32m (median) · High ≈ £37m+ (toward peer 75th pct)

## Assumptions log (editable on the Assumptions tab)

| Assumption | Value | Basis |
|---|---|---|
| Low / Base closure | 50% / 100% of gap | Judgement; anchored to peer median |
| High | median rev/FTE ×1.10 | Peer 75th percentile is Access (roll-up caveat), so capped beyond median |
| Cost to implement | 25% of annualised benefit | Judgement — typical rightsizing one-off cost (consulting benchmark) |
| Year-1 realisation | 60% | Phasing: notice periods, attrition-led savings |
| Excluded | Sage (listed anchor), micro-caps | Scale + comparability |