"""
Step 3 extraction: pull turnover, staff costs and average headcount from
filed accounts PDFs into a tidy CSV.

Strategy: search each PDF's text for the consolidated P&L ("Turnover") and the
employees note ("Average number of employees"). Records every hit with the page
number so a human can verify against the PDF (extraction is a *proposal*, the
data log is the source of truth).

Usage:  python data/extract_financials.py
"""
import csv
import re
from pathlib import Path

import pymupdf  # robust PDF text extraction (pypdf chokes on CH filings)

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "extracted_hits.csv"

NUMBER_PAT = re.compile(r"\(?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?")


def open_doc(pdf: Path):
    return pymupdf.open(str(pdf))


def page_text(doc, i: int) -> str:
    try:
        return doc[i].get_text() or ""
    except Exception:  # noqa: BLE001
        return ""


def find_pages(doc, needles: list[str]) -> dict[str, list[int]]:
    hits: dict[str, list[int]] = {n: [] for n in needles}
    for i in range(len(doc)):
        text_flat = re.sub(r"\s+", " ", page_text(doc, i))
        for n in needles:
            if n.lower() in text_flat.lower():
                hits[n].append(i)
    return hits


def context_on(doc, page_no: int, needle: str, span: int = 700) -> str:
    text = re.sub(r"\s+", " ", page_text(doc, page_no))
    i = text.lower().find(needle.lower())
    if i < 0:
        return ""
    return text[i : i + span]


def main():
    rows = []
    for pdf in sorted(RAW.glob("*.pdf")):
        name = pdf.stem
        print(f"\n=== {name} ===")
        try:
            doc = open_doc(pdf)
        except Exception as exc:  # noqa: BLE001
            print("  FAILED to open:", exc)
            continue
        pages = find_pages(doc, ["Turnover", "Average number of employees", "Staff costs", "Wages and salaries"])
        for needle, pnos in pages.items():
            print(f"  '{needle}': pages {[p + 1 for p in pnos][:6]}")
        # capture the first turnover statement + employee note context
        for needle in ("Turnover", "Average number of employees", "Staff costs"):
            if pages[needle]:
                snippet = context_on(doc, pages[needle][0], needle)
                rows.append(
                    {
                        "file": name,
                        "metric_hint": needle,
                        "page": pages[needle][0] + 1,
                        "context": snippet[:1000],
                    }
                )
                print(f"  {needle} @ p{pages[needle][0] + 1}: {snippet[:200]}")

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["file", "metric_hint", "page", "context"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {len(rows)} hit records -> {OUT}")


if __name__ == "__main__":
    main()