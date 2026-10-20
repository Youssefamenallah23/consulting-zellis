"""
Step 3 data collection: download annual accounts (AA) PDFs from Companies House.

How it works (no API key needed):
1. For each company number, fetch the public filing-history page.
2. Parse rows; keep annual-accounts filings ("Full accounts", "Group of
   companies' accounts", "Amended ...") made up to 2021-2025.
3. Download each accounts PDF into data/raw/.
4. Write a manifest (data/manifest.csv) recording every download.

Politeness: 1 request/second, custom User-Agent, small volume (public documents).

Usage:  python data/pull_filings.py
"""
import csv
import re
import time
from pathlib import Path

import requests

BASE = "https://find-and-update.company-information.service.gov.uk"
RAW = Path(__file__).parent / "raw"
RAW.mkdir(exist_ok=True)

COMPANIES = {
    "01587537": "Zellis UK Limited",
    "10975623": "Zellis Holdings Limited",  # group-level consolidation (Apax+Vitruvian holdco)
    "03196054": "IRIS Software Limited",
    "02050075": "IRIS Business Software Limited",  # files the IRIS group's consolidated accounts (PARENT_ACC)
    "02343760": "Access UK Ltd",
    "05965280": "OneAdvanced Group Limited",
    "02231246": "The Sage Group plc",
}

HEADERS = {"User-Agent": "org-effectiveness-case-study/0.1 (educational)"}
ACCOUNT_RE = re.compile(
    r"^(Amended )?(Full|Group of companies'|Group) accounts? made up to (\d{1,2} \w+ \d{4})",
    re.IGNORECASE,
)
PARENT_ACC_RE = re.compile(
    r"^Consolidated accounts of parent company for subsidiary company period ending (\d{2}/\d{2}/\d{2})",
    re.IGNORECASE,
)

# The filing history is a real table. Each <tr> holds: date, filing type (AA,
# AAMD, CS01...), description in its own <td>, and the document link.
TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
TYPE_RE = re.compile(r'<td class="filing-type[^"]*">\s*(\w+)\s*</td>')
DESC_RE = re.compile(r"<td>\s*(?:<strong>)?(.*?)(?:</strong>)?\s*</td>", re.DOTALL)
HREF_RE = re.compile(r'href="(/company/\d+/filing-history/[^"]+?/document\?format=pdf[^"]*)"')


def _clean(s: str) -> str:
    import html as _html

    return re.sub(r"\s+", " ", _html.unescape(s)).strip()


def rows_for(company_number: str):
    out = []
    for page in (1, 2, 3, 4, 5, 6, 7, 8, 9):  # listed companies have very deep histories
        url = f"{BASE}/company/{company_number}/filing-history?page={page}"
        html = None
        for attempt in range(3):  # retry with backoff (the site throttles bursts)
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                html = resp.text
                break
            print(f"  page {page} -> HTTP {resp.status_code}, retry {attempt + 1}/3 after backoff")
            time.sleep(5 * (attempt + 1))
        if html is None:
            print(f"  page {page} failed after retries")
            continue
        # stop if this page has no filings at all
        if 'There are no filings' in html or 'filing-history' not in html:
            break
        found = 0
        page_has_rows = False
        for tr in TR_RE.finditer(html):
            row = tr.group(1)
            t = TYPE_RE.search(row)
            if t:
                page_has_rows = True
            d = DESC_RE.search(row)
            h = HREF_RE.search(row)
            if not (t and d and h):
                continue
            desc = _clean(TAG_RE.sub("", d.group(1)))
            if t.group(1) not in ("AA", "AAMD", "PARENT_ACC"):
                continue
            match = ACCOUNT_RE.match(desc)
            parent = PARENT_ACC_RE.match(desc)
            if not (match or parent):
                continue
            if parent:
                d, m, y = parent.group(1).split("/")
                made_up = f"{int(d)} {'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[int(m) - 1]} 20{y}"
                out.append(
                    {
                        "description": desc,
                        "amended": False,
                        "made_up": made_up,
                        "href": h.group(1),
                    }
                )
                continue
            out.append(
                {
                    "description": desc,
                    "amended": t.group(1) == "AAMD",
                    "made_up": match.group(3),
                    "href": h.group(1),
                }
            )
            found += 1
        print(f"  page {page}: {found} accounts filings (page has rows: {page_has_rows})")
        if not page_has_rows:
            break  # history exhausted
        if found and all(fy_label(f['made_up']) < 'FY2021' for f in out[-found:]):
            break  # reached filings older than our window
        time.sleep(1)
    return out


def fy_label(made_up: str) -> str:
    """'30 April 2025' -> 'FY2025'"""
    return "FY" + made_up.split()[-1]


def main():
    manifest = []
    for number, name in COMPANIES.items():
        filings = rows_for(number)
        print(f"\n{name} ({number}): {len(filings)} accounts filings found")
        for f in filings:
            label = fy_label(f["made_up"])
            year = int(label[2:])
            if not (2021 <= year <= 2025):
                continue
            fname = f"{number}_{label}.pdf"
            dest = RAW / fname
            if dest.exists() and dest.stat().st_size > 10_000:
                print(f"  {label}: cached -> {fname}")
            else:
                resp = requests.get(BASE + f["href"], headers=HEADERS, timeout=120)
                dest.write_bytes(resp.content)
                print(f"  {label}: downloaded {len(resp.content):,} bytes -> {fname}")
                time.sleep(1)
            manifest.append(
                {
                    "company_number": number,
                    "company_name": name,
                    "fy": label,
                    "made_up_to": f["made_up"],
                    "description": f["description"],
                    "file": str(dest),
                    "source_url": BASE + f["href"],
                }
            )

    if not manifest:
        raise SystemExit("No filings collected - check parsing / connectivity.")
    with open(RAW.parent / "manifest.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)
    print(f"\nManifest written: {len(manifest)} files -> data/manifest.csv")


if __name__ == "__main__":
    main()