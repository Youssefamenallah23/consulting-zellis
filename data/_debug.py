"""Probe text-based PDFs for key financial terms.
Usage: python _debug.py "term1|term2" file1.pdf [file2.pdf ...]
"""
import re
import sys
from pathlib import Path

import pymupdf

TERMS = sys.argv[1].lower().split("|")
for arg in sys.argv[2:]:
    path = Path(arg)
    if not path.exists():
        print(f"{arg}: NOT FOUND")
        continue
    doc = pymupdf.open(str(path))
    print(f"\n=== {path.name}: {len(doc)} pages ===")
    for i in range(len(doc)):
        t = doc[i].get_text()
        if not t.strip():
            continue
        low = t.lower()
        if any(term in low for term in TERMS):
            flat = re.sub(r"\s+", " ", t)
            print(f"--- page {i+1} ---")
            print(flat[:1300])
            print()
    doc.close()