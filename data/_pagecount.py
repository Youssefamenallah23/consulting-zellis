"""Exact page counts for the OCR queue."""
from pathlib import Path

import pymupdf

ocr = [
    p
    for p in (Path(__file__).parent / "raw").glob("*.pdf")
    if not p.name.startswith(("zellis_uk", "oneadvanced_midco", "sage", "02231246"))
]
total = 0
for p in sorted(ocr):
    n = pymupdf.open(str(p)).page_count
    total += n
    print(f"{p.name:28s} {n:4d} pages")
print(f"\nTOTAL: {len(ocr)} docs, {total} pages")