"""
Step 7 (optional): research accelerator - retrieval over the filed accounts.

A small, fully-local search tool over the OCR'd filing pages
(data/ocr_text/*.txt). Ask a question; it scores pages by term overlap and
returns the top passages WITH citations (document + page) - the pattern
Humatica calls research acceleration, and what recruiters know as RAG
without the LLM: retrieval + citation, no generated text.

Usage:
  python data/ai_retrieval.py "average number of employees"
  python data/ai_retrieval.py "turnover" --company 10975623

Design note: deliberately no external AI API - everything runs locally from
files this project already produced, so it is reproducible and free.
"""
import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

CACHE = Path(__file__).parent / "ocr_text"
STOP = set(
    "a an and are as at be by for from has have in is it its of on or that the this to was were which with".split()
)


def tokenize(text: str) -> Counter:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return Counter(w for w in words if w not in STOP and len(w) > 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--company", default=None, help="filter by company number prefix, e.g. 10975623")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    q = tokenize(args.query)
    if not q:
        raise SystemExit("empty query")

    files = sorted(CACHE.glob("*.txt"))
    if args.company:
        files = [f for f in files if f.name.startswith(args.company)]
    if not files:
        raise SystemExit("no cached pages match the filter")

    # score = cosine similarity between query vector and page vector
    scored = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        counts = tokenize(text)
        if not counts:
            continue
        common = set(q) & set(counts)
        if not common:
            continue
        dot = sum(q[w] * counts[w] for w in common)
        score = dot / (math.sqrt(sum(v * v for v in q.values())) * math.sqrt(sum(v * v for v in counts.values())))
        scored.append((score, f, text))

    scored.sort(key=lambda t: -t[0])
    if not scored:
        raise SystemExit("no matches")

    print(f"query: {args.query!r}  |  searched {len(files)} pages  |  top {args.top}:\n")
    for rank, (score, f, text) in enumerate(scored[: args.top], 1):
        flat = re.sub(r"\s+", " ", text)
        # show the densest window around the rarest query term
        best_pos, best_hits = 0, -1
        for pos in range(0, max(1, len(flat) - 400), 200):
            window = flat[pos : pos + 500].lower()
            hits = sum(1 for w in q if w in window)
            if hits > best_hits:
                best_hits, best_pos = hits, pos
        print(f"[{rank}] score={score:.3f}  citation: {f.stem.replace('_p', ' p')}")
        print(f"    ...{flat[best_pos : best_pos + 450]}...\n")


if __name__ == "__main__":
    main()