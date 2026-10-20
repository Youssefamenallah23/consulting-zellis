# Data Log

Rule: **every figure** used anywhere in the project gets a row here. If it's not in this log, it doesn't go in a slide.

| # | Date pulled | Company | Metric | Value | Period | Source (URL/dataset) | Source date | Notes / assumptions |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-20 | Zellis UK Ltd (01587537) | account_type | Full accounts | FY2025 (to 30 Apr 2025) | CH filing history /company/01587537/filing-history | filed 03 Feb 2026 | 55pp; FY2021–FY2025 all full accounts |
| 2 | 2026-10-20 | Zellis Group | ownership | Apax Funds acquired from Bain Capital | Apr 2024 | apax.com/news-views/apax-funds-to-acquire-zellis-group-from-bain-capital | Apr 2024 | £1.25bn valuation (Bloomberg 15 Apr 2024) |
| 3 | 2026-10-20 | IRIS Software Ltd (03196054) | ownership | Hg majority; Leonard Green & Partners invested at £3.2bn valuation | Dec 2023 | hgcapital.com/insights/iris-software-group-secures-major-us-investment-from-leonard-green-and | Dec 2023 | Note: IRIS Software Group Ltd (06295385) is a dormant holdco — use 03196054 |
| 4 | 2026-10-20 | OneAdvanced Group Ltd (05965280) | account_type | Group of companies' accounts (consolidated) | FY2025 (to 28 Feb 2025) | CH filing history /company/05965280/filing-history | filed 03 Dec 2025 | 79pp; AAMD amended accounts for FY2023 filed 21 Feb 2024 |
| 5 | 2026-10-20 | OneAdvanced Group Ltd | ownership | Vista Equity Partners + BC Partners (50%, 2019) | 2014–present | vistaequitypartners.com/about/companies/oneadvanced; bcpartners.com/portfolio/advanced | 2019 | formerly Advanced Computer Software plc (LSE-listed) |
| 6 | 2026-10-20 | Access UK Ltd (02343760) | ownership | Hg substantial investment at £9.2bn valuation; prior TA Associates (2015) | Jun 2022 | hgcapital.com/insights/the-access-group-announces-substantial-investment | Jun 2022 | account type to confirm in Step 3 |
| 7 | 2026-10-20 | The Sage Group plc (02231246) | status | Publicly listed (context anchor, not a PE peer) | — | CH profile /company/02231246 | — | registered name includes trailing "." — search carefully |
| 8 | 2026-10-20 | Zellis Holdings (group) | revenue | FY2025 £261.1m; FY2024 £226.6m (reported revenue) | FY2025 | Zellis Annual Report p.6 (data/raw/zellis_uk_fy2025.pdf) | 2025 | Group-level; cross-check vs CH entity filings after OCR |
| 9 | 2026-10-20 | Zellis Holdings (group) | staff_costs | FY2025 £136,488k; FY2024 £122,418k | FY2025 | Zellis Annual Report p.86, Note 5 Operating costs | 2025 | Group-level staff costs |
| 10 | 2026-10-20 | Zellis Holdings (group) | ownership_detail | Owned by Apax Partners AND Vitruvian Partners | FY2025 | Zellis Annual Report p.11 ("new ownership of Apax Partners LLP and Vitruvian Partners LLP") | 2025 | Corrects row 2: not Apax alone |
| 11 | 2026-10-20 | OneAdvanced Group (Aston Midco) | revenue | FY2025 £308,818k; FY2024 £320,089k (continuing basis, FY24 restated) | FY2025 (to 28 Feb 2025) | Aston Midco consolidated P&L p.35 of PDF (data/raw/oneadvanced_midco_fy2025.pdf) | 2025 | Group-level; FY24 restated for error (note 2); AppMod sold to IBM Mar 2024 → discontinued ops |
| 12 | 2026-10-20 | OneAdvanced Group (Aston Midco) | staff_costs | FY2025 £113,549k (continuing); FY2024 £143,607k (continuing) | FY2025 | Aston Midco note 4, p.60 of PDF | 2025 | wages 96,964 + soc sec 11,449 + pensions 5,136 |
| 13 | 2026-10-20 | OneAdvanced Group (Aston Midco) | avg_headcount | FY2025 2,283 (continuing); FY2024 2,753 (continuing) | FY2025 | Aston Midco note 4, p.60 of PDF | 2025 | Headcount drop reflects AppMod disposal, not productivity change |
| 14 | 2026-10-20 | OneAdvanced Group (Aston Midco) | ownership_detail | BC European Capital X (BC Partners) + Vista Equity Partners Fund VII | FY2025 | Aston Midco directors' report p.5 | 2025 | Primary-source confirmation of rows 5 |
| 15 | 2026-10-20 | OneAdvanced Group | restatement | FY2024 restated due to error (note 2); FY2023 also amended (AAMD) | FY2024 | Aston Midco accounts p.35 fn **; CH filing history | 2025 | Branch-D watchlist: use restated figures only |
| 16 | 2026-10-20 | Zellis UK Ltd (01587537) | revenue | FY2021 £98.8m (FY2020: £98.3m) | FY2021 | CH full accounts OCR, strategic report p.7 (data/ocr_text/01587537_FY2021_p007.txt) | 2025 | Entity-level; OCR'd from scanned filing |
| 17 | 2026-10-20 | Zellis UK Ltd (01587537) | ownership_detail | FY2021: "Shareholders are primarily Bain Capital" | FY2021 | CH full accounts OCR p.19 (data/ocr_text/01587537_FY2021_p019.txt) | 2025 | Confirms ownership history: Bain (FY2021) → Bain sale to Apax+Vitruvian (2024) |
| 18 | 2026-10-20 | Zellis UK Ltd (01587537) | revenue | FY2025 £129,773k; FY2024 £121,307k (entity) | FY2025 | CH full accounts OCR income statement p.21 (data/ocr_text/01587537_FY2025_p021.txt) | 2025 | Entity is ~half of group (£261.1m) → comparability decision: use Zellis Holdings group accounts as primary for Zellis |
| 19 | 2026-10-20 | Zellis Holdings Ltd (10975623) | data_collection | Group consolidated accounts FY2021–FY2025 downloaded from CH | FY2021–FY2025 | CH filing history /company/10975623 | 2025 | 5 PDFs (4.1–6.2MB each); group-level = like-for-like with OneAdvanced group accounts |
| 20 | 2026-10-20 | IRIS Software Ltd | comparability_note | Group consolidation sits at Jersey topco (Elements Topco, BR026778 UK estab.) — but the group's consolidated accounts ARE filed at CH under s401 (PARENT_ACC) via IRIS Business Software Ltd (02050075) | — | CH filing history 02050075 | 2025 | Decision: use IRIS group PARENT_ACC accounts; FY2025 (ElementsFinco, 13.5-month first period) not comparable — FY2024 used |
| 21 | 2026-10-20 | IRIS Business Software Ltd (group) | revenue | FY2024 £373,544k; FY2023 £319,080k | FY2024 | IRIS Debtco consolidated income statement, p.39 (data/ocr_text/02050075_FY2024_p039.txt) | 2024 | 12-month period; Management Revenue 375,078k; Mgmt EBITDA 166,215k |
| 22 | 2026-10-20 | IRIS Business Software Ltd (group) | staff_costs | FY2024 £161,282k; FY2023 £131,648k | FY2024 | IRIS Debtco staff note, p.55 (data/ocr_text/02050075_FY2024_p055.txt) | 2024 | components sum 160,505 — OCR uncertainty ~£1m on one component; totals as filed |
| 23 | 2026-10-20 | IRIS Business Software Ltd (group) | avg_headcount | FY2024 2,986; FY2023 2,638 (restated, incl contractors) | FY2024 | IRIS Debtco staff note, p.55 | 2024 | totals row OCR-swapped — component sums confirm assignment |
| 24 | 2026-10-20 | PEER SET | final_stats | 4 PE peers; median Rev/FTE £135.3k; median staff% 40.0% | latest filed FY each | analysis/metrics.csv | 2025 | Zellis gap 27.3%; value at stake £32.2m (Method A) / £37.3m (Method B); cross-check 16% |

## Field definitions (keep consistent)
- **Metric:** revenue / staff_costs / avg_headcount / period_end / account_type / job_postings / ownership
- **Period:** the financial year end the figure relates to (e.g., FY2024 = year ended 30 Apr 2024 for Zellis)
- **Notes:** anything a stranger would need — e.g., "abridged accounts, no turnover disclosed", "9-month period due to year-end change", "restated/amended accounts"

## Data-quality watchlist (from Step 1 issue tree, Branch D)
- [x] Target and peers all file full accounts? — Zellis ✅, OneAdvanced ✅; IRIS + Access to confirm in Step 3
- [ ] Period ends aligned / normalised? — mixed: 30 Apr (Zellis, IRIS), 28 Feb (OneAdvanced), 30 Sep (Sage) → normalise to nearest FY, note in every comparison
- [x] Any year-end changes or restatements? — OneAdvanced FY2023 amended (AAMD)
- [ ] UK audit & filing threshold changes affecting comparability?