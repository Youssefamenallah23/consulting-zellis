"""
Step 4 analysis: organisational productivity metrics from the DuckDB database.

Outputs (printed and saved to analysis/metrics.csv):
- revenue per FTE (GBP k) by company-year
- staff cost as % of revenue
- staff cost per FTE (GBP k)
- 3-year revenue CAGR
- peer medians (PE peers only - Sage excluded) and target vs median gap
"""
from pathlib import Path

import duckdb
import pandas as pd

DATA = Path(__file__).parent
OUT = Path(__file__).parent.parent / "analysis" / "metrics.csv"

con = duckdb.connect(str(DATA / "org_effectiveness.duckdb"), read_only=True)

df = con.execute(
    """
    SELECT company_number, company_name, role, fy, period_end,
           MAX(CASE WHEN metric='revenue_gbp' THEN value END) AS revenue,
           MAX(CASE WHEN metric='staff_costs_gbp' THEN value END) AS staff_costs,
           MAX(CASE WHEN metric='avg_headcount' THEN value END) AS headcount
    FROM financials
    GROUP BY 1,2,3,4,5
    ORDER BY company_name, fy
    """
).fetchdf()

df["rev_per_fte_gbpk"] = (df["revenue"] / df["headcount"]).round(1)
df["staff_pct_rev"] = (100 * df["staff_costs"] / df["revenue"]).round(1)
df["staff_per_fte_gbpk"] = (df["staff_costs"] / df["headcount"]).round(1)

print("\n=== Productivity metrics by company-year ===")
print(df[["company_name", "fy", "revenue", "headcount", "rev_per_fte_gbpk", "staff_pct_rev", "staff_per_fte_gbpk"]].to_string(index=False))

print("\n=== Peer medians (PE peers only, each at its latest filed FY) ===")
latest = df[df["fy"] == df.groupby("company_number")["fy"].transform("max")]
peers = latest[latest["role"] == "peer"]
print(peers[["company_name", "rev_per_fte_gbpk", "staff_pct_rev", "staff_per_fte_gbpk"]].to_string(index=False))
print(
    "median rev/FTE:",
    peers["rev_per_fte_gbpk"].median(),
    "| median staff%:",
    peers["staff_pct_rev"].median(),
    "| IQR rev/FTE:",
    peers["rev_per_fte_gbpk"].quantile([0.25, 0.75]).tolist(),
)

print("\n=== Target (Zellis Holdings) FY2025 vs peer median ===")
tgt = df[(df["role"] == "target") & (df["fy"] == "FY2025")].iloc[0]
med_rev_fte = peers["rev_per_fte_gbpk"].median()
med_staff_pct = peers["staff_pct_rev"].median()
print(f"target rev/FTE {tgt['rev_per_fte_gbpk']:.1f} vs peer median {med_rev_fte:.1f} "
      f"-> gap {(1 - tgt['rev_per_fte_gbpk'] / med_rev_fte) * 100:.1f}%")
print(f"target staff% {tgt['staff_pct_rev']:.1f} vs peer median {peers['staff_pct_rev'].median():.1f}")
print(f"target staff/FTE {tgt['staff_per_fte_gbpk']:.1f} vs peer median {peers['staff_per_fte_gbpk'].median():.1f}")

print("\n=== 3-year revenue CAGR (FY2022->FY2025) ===")
for name in df["company_name"].unique():
    sub = df[(df["company_name"] == name) & (df["fy"].isin(["FY2022", "FY2025"]))]
    if name.startswith("IRIS"):
        sub = df[(df["company_name"] == name) & (df["fy"].isin(["FY2023", "FY2024"]))]
        if len(sub) == 2 and sub["revenue"].notna().all():
            r0 = sub[sub["fy"] == "FY2023"]["revenue"].iloc[0]
            r1 = sub[sub["fy"] == "FY2024"]["revenue"].iloc[0]
            print(f"{name} (FY2023->FY2024): {((r1 / r0) - 1) * 100:.1f}%/yr")
        continue
    if len(sub) == 2 and sub["revenue"].notna().all():
        r0 = sub[sub["fy"] == "FY2022"]["revenue"].iloc[0]
        r1 = sub[sub["fy"] == "FY2025"]["revenue"].iloc[0]
        print(f"{name}: {((r1 / r0) ** (1 / 3) - 1) * 100:.1f}%/yr")

OUT.parent.mkdir(exist_ok=True)
df.to_csv(OUT, index=False)
print(f"\nsaved -> {OUT}")