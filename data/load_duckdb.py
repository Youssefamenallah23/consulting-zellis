"""
Step 3: load the verified financials into DuckDB.

Input:  data/financials.csv  (one row per company x financial year x metric)
Output: data/org_effectiveness.duckdb (table: financials)

Every row in financials.csv must have a source (filing PDF name + page) so the
whole database is traceable. See data/README.md for the rebuild instructions.

Usage:  python data/load_duckdb.py
"""
from pathlib import Path

import duckdb

DATA = Path(__file__).parent
DB_PATH = DATA / "org_effectiveness.duckdb"
CSV_PATH = DATA / "financials.csv"

REQUIRED_COLUMNS = [
    "company_number",
    "company_name",
    "role",          # target / peer / public_anchor
    "fy",            # FY2021..FY2025 (label)
    "period_end",    # e.g. 2025-04-30
    "metric",        # revenue_gbp / staff_costs_gbp / avg_headcount
    "value",
    "unit",
    "source_file",   # PDF in data/raw/
    "source_page",
    "source_url",
    "notes",
]


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit("financials.csv not found - populate it first (see README).")
    con = duckdb.connect(str(DB_PATH))
    con.execute("DROP TABLE IF EXISTS financials")
    con.execute(
        f"""
        CREATE TABLE financials AS
        SELECT * FROM read_csv_auto('{CSV_PATH.as_posix()}', header=true, all_varchar=false)
        """
    )
    cols = [c[0] for c in con.execute("DESCRIBE financials").fetchall()]
    missing = [c for c in REQUIRED_COLUMNS if c not in cols]
    if missing:
        raise SystemExit(f"financials.csv is missing required columns: {missing}")

    print("Loaded financials table:")
    print(con.execute("SELECT * FROM financials ORDER BY company_name, fy, metric").fetchdf())

    print("\nSanity check - latest FY revenue by company:")
    print(
        con.execute(
            """
            SELECT company_name, fy, metric, value
            FROM financials
            WHERE metric = 'revenue_gbp'
            QUALIFY fy = max(fy) OVER (PARTITION BY company_number)
            ORDER BY company_name
            """
        ).fetchdf()
    )
    con.close()
    print(f"\nDatabase written -> {DB_PATH}")


if __name__ == "__main__":
    main()