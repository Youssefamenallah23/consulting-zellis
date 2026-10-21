# Model: Value-at-Stake Sizing (Step 5) ✅

**File: `model/ValueAtStake.xlsx`**
Built by `python data/build_model.py` from `data/financials.csv`.
Verified by `python data/verify_model.py`, which recalculates the workbook with an
independent engine (`formulas`) and asserts 24 cells against hand-computed values.

## Tabs (every calculation is a live formula, no pasted values)

| Tab | Purpose |
|---|---|
| `Cover` | The answer in one sentence, how to read the file, caveats, sources |
| `Inputs` | 16 company-years of filed accounts, with filing, page and the reason for each adjustment. Ratios are formulas |
| `Benchmarks` | Each company at its latest comparable year. Peer median and quartiles computed live over a contiguous range |
| `Assumptions` | **The only editable cells.** Three judgements: year-1 realisation, one-off cost, reconciliation tolerance |
| `Sizing` | Method A, Method B, cross-check, the range carried forward, year-1 phasing |
| `Scenarios` | 25th percentile, median, 75th percentile of peer revenue per FTE |
| `Sensitivity` | Net year-1 EBITDA: gap closed × cost to implement. Plus a steady-state grid |
| `Checks` | Ten integrity tests with PASS / FAIL |

Named ranges (`Target_Revenue`, `Peer_Median_RevFTE`, `Realisation_Y1`, …) mean the
formulas read as sentences rather than cell addresses.

## Sizing logic

- **Method A (ratio route):** (target staff-cost % − peer-median staff-cost %) × target revenue
- **Method B (headcount route):** (target FTE − FTE implied at peer-median revenue per FTE) × target staff cost per FTE
- **Cross-check:** if |A − B| > 20% of A, the peer set or the basis is wrong and the answer is not published. Currently **16%**.

## Headline numbers

- Peer median revenue per FTE **£135.3k** against target **£98.3k**: a **27.3% gap**
- Target staff-cost ratio **52.3%** against peer median **40.0%**: a **12.3-point gap**
- Target staff cost per FTE **£51.4k** against peer median **£54.0k**: Zellis pays *below* the median, so the gap is output, not pay
- Method A **£32.2m** · Method B **£37.3m** · midpoint **£34.7m**
- Year 1: 60% realisation, 25% one-off cost → net **£12.2m**
- Scenarios: 25th percentile **£33.4m** · median **£37.3m** · 75th percentile **£46.7m**

## Why the scenarios changed from v1

v1 interpolated 50% and 110% of the way to the median and called that "low" and
"high". Those fractions were invented. v2 anchors each case to an actual point in
the peer distribution, so the range describes the peer set rather than the author's
optimism.

## Why the two methods do not repeat in the scenario tab

At a fixed revenue-per-FTE anchor, the cost-ratio route and the headcount route are
the same algebra. Printing both there would fake a robustness the model does not
have. The honest range comes from the spread of the peers.

## Assumptions log

| Assumption | Value | Basis |
|---|---|---|
| Year-1 realisation | 60% | Notice periods; savings land through attrition and redeployment, not day one |
| One-off implementation cost | 25% of annualised benefit | Severance, programme office, interim management. Paid once, subtracted once |
| Reconciliation tolerance | 20% | Chosen before looking at the answer |
| Excluded | Sage (listed anchor) | Different scale and filing basis; kept as a valuation anchor only |

## Known caveats

Access is an entity that hives up acquisitions, so its productivity is flattered by
M&A. IRIS files group accounts under an s401 exemption at a different company number,
and its FY2025 covers a 13.5-month period, so FY2024 is used. OneAdvanced is on a
continuing-operations basis after the IBM disposal. Each peer sits at its latest
comparable year, so the vintages differ by up to 12 months.
