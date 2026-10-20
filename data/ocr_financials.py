"""
Step 3b: OCR the image-only Companies House filings and locate the key figures.

Companies House PDFs are CCITT TIFF scans (no text layer), so we:
1. Render each page with PyMuPDF at ~200 dpi grayscale
2. OCR it with RapidOCR (ONNX models, CPU)
3. Cache the recognised text per page (data/ocr_text/) so re-runs are free
4. Harvest text snippets around the terms we need into ocr_hits.csv

This is slow (~1-3 s/page) -> run in background, harvest incrementally.

Usage:  python data/ocr_financials.py [max_docs]
"""
import csv
import ctypes
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pymupdf

# --- self-throttling: never grab all cores / starve the OS (PC crashed once) ---
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
if sys.platform == "win32":
    _k32 = ctypes.windll.kernel32
    _AFFINITY = int(os.environ.get("OCR_AFFINITY", "0xF"), 16)  # cores to use, e.g. 0xF or 0xF0
    _k32.SetProcessAffinityMask(_k32.GetCurrentProcess(), _AFFINITY)
    _k32.SetPriorityClass(_k32.GetCurrentProcess(), 0x00004000)  # BELOW_NORMAL_PRIORITY_CLASS

from rapidocr_onnxruntime import RapidOCR  # noqa: E402  (import after thread-limit env vars)

RAW = Path(__file__).parent / "raw"
CACHE = Path(__file__).parent / "ocr_text"
CACHE.mkdir(exist_ok=True)
OUT = Path(__file__).parent / "ocr_hits.csv"

NEEDLES = [
    "turnover",
    "revenue",
    "average number of employees",
    "staff costs",
    "wages and salaries",
    "social security",
    "pension",
]


def page_image(doc, i: int) -> np.ndarray:
    pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), colorspace=pymupdf.csGRAY)
    arr = np.frombuffer(pix.samples, dtype=np.uint8)
    return arr.reshape(pix.height, pix.width, pix.n)


def ocr_page(ocr, doc, i: int) -> str:
    result, _ = ocr(page_image(doc, i))
    if not result:
        return ""
    # sort recognised fragments top-to-bottom, then left-to-right
    items = []
    for box, text, score in result:
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        items.append((min(ys), min(xs), text))
    items.sort(key=lambda t: (t[0], t[1]))
    return " ".join(t for _, _, t in items)


def get_page_text(ocr, doc, pdf_name: str, i: int) -> str:
    cache_file = CACHE / f"{pdf_name}_p{i + 1:03d}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")
    text = ocr_page(ocr, doc, i)
    cache_file.write_text(text, encoding="utf-8")
    return text


def main() -> None:
    doc_filter = sys.argv[1] if len(sys.argv) > 1 else ""
    max_docs = int(sys.argv[2]) if len(sys.argv) > 2 else None
    ocr = RapidOCR()
    pdfs = sorted(
        p
        for p in RAW.glob("*.pdf")
        if not p.name.startswith(("zellis_uk", "oneadvanced_midco", "02231246", "sage"))
        and doc_filter.lower() in p.name.lower()
    )
    # FY2025 filings first (base year for the model), then FY2024, FY2023, ...
    # casefold() so 'FY2025' and 'fy2025' group together
    pdfs.sort(key=lambda p: p.name.split("_")[-1].casefold(), reverse=True)
    if max_docs:
        pdfs = pdfs[:max_docs]

    hits = []
    for pdf in pdfs:
        print(f"\n=== {pdf.name} ===", flush=True)
        doc = pymupdf.open(str(pdf))
        for i in range(len(doc)):
            text = get_page_text(ocr, doc, pdf.stem, i)
            flat = re.sub(r"\s+", " ", text).strip()
            if not flat:
                continue
            lowered = flat.lower()
            for needle in NEEDLES:
                pos = lowered.find(needle)
                if pos >= 0:
                    hits.append(
                        {
                            "file": pdf.stem,
                            "page": i + 1,
                            "needle": needle,
                            "context": flat[max(0, pos - 150) : pos + 350],
                        }
                    )
        doc.close()

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["file", "page", "needle", "context"])
        writer.writeheader()
        writer.writerows(hits)
    print(f"\n{len(hits)} hits -> {OUT}", flush=True)


if __name__ == "__main__":
    started = time.time()
    main()
    print(f"done in {(time.time() - started) / 60:.1f} min", flush=True)