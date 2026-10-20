"""Grep the OCR page cache for key financial terms and show hits.
Terms are read from data/_terms.txt (one per line, '|' separated on one line also OK).
"""
import re
import sys
from pathlib import Path

CACHE = Path(__file__).parent / "ocr_text"
TERMS_FILE = Path(__file__).parent / "_terms.txt"
if TERMS_FILE.exists():
    raw = TERMS_FILE.read_text(encoding="utf-8")
    TERMS = [t.strip().lower() for t in re.split(r"[\n|]", raw) if t.strip()]
else:
    TERMS = ["turnover", "average number", "staff costs"]
print("terms:", TERMS)

for f in sorted(CACHE.glob("*.txt")):
    text = re.sub(r"\s+", " ", f.read_text(encoding="utf-8"))
    low = text.lower()
    for term in TERMS:
        pos = low.find(term)
        if pos >= 0:
            print(f"--- {f.stem} [{term}] ---")
            print(text[max(0, pos - 120) : pos + 300])
            print()
            break