"""
Fetch the official TRAI Performance Indicator reports (quarterly + yearly)
from the TRAI publications index into data/raw/trai/.

The index is a Drupal view with 30 items per page. Report titles encode the
quarter; we parse them into (year, quarter-end month) and keep QE Mar/Jun/Sep/Dec
from 2014 onwards. A manifest with the source URL and SHA-256 is written so the
extraction step can be audited against the exact files used.

Run:  python scripts/fetch_trai.py
"""

from __future__ import annotations

import hashlib
import html
import re
import time
import warnings
from pathlib import Path

import requests

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "trai"
INDEX = "https://trai.gov.in/release-publication/reports/performance-indicators-reports"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Explicit skip list: reports that are not performance-indicator quarterlies or
# yearlies (errata, QoS surveys, press kits, etc.).
SKIP_PAT = re.compile(r"errata|survey|assessment|custome|congestion|press kit|qos", re.I)

MONTHS = {
    "march": 3, "mar": 3,
    "june": 6, "jun": 6,
    "september": 9, "sep": 9, "sept": 9,
    "december": 12, "dec": 12, "decemberr": 12,
}
MONTH_ABBR = {3: "Mar", 6: "Jun", 9: "Sep", 12: "Dec"}


def parse_quarter(title: str):
    """Return (year, month) for a quarterly PIR title, else None."""
    t = html.unescape(title).lower()
    if "yearly" in t or "quarter" not in t and "january" not in t and "april" not in t and "july" not in t and "october" not in t:
        return None
    months = [(m.start(), mon) for word, mon in MONTHS.items() for m in re.finditer(r"\b" + word + r"\b", t)]
    if not months:
        return None
    # use the last month mentioned (titles are "... January - March, 2019")
    pos, month = max(months)
    years = [int(x) for x in re.findall(r"\b(20\d{2})\b", t[pos:])]
    if not years:
        years = [int(x) for x in re.findall(r"\b(20\d{2})\b", t)]
    if not years:
        return None
    return years[0], month


def crawl_index(max_pages: int = 6) -> list[dict]:
    found, seen = [], set()
    for p in range(max_pages):
        url = INDEX if p == 0 else f"{INDEX}?page={p}"
        r = requests.get(url, headers=HEADERS, timeout=90, verify=False)
        r.raise_for_status()
        chunks = r.text.split('<div class="views-view-grid__item">')[1:]
        if not chunks:
            break
        for c in chunks:
            tm = re.search(r'views-field-title"><div class="field-content">(.*?)</div>', c, re.S)
            dm = re.search(r'views-field-field-date"><div class="field-content">(.*?)</div>', c, re.S)
            hm = re.search(r'href="([^"]+\.pdf)"', c)
            if not (tm and hm):
                continue
            title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", tm.group(1))).strip()
            href = html.unescape(hm.group(1))
            if href in seen or SKIP_PAT.search(title):
                continue
            seen.add(href)
            found.append({
                "title": title,
                "release_date": re.sub(r"\s+", " ", dm.group(1)).strip() if dm else "",
                "url": requests.compat.urljoin(INDEX, href),
            })
        print(f"index page {p}: {len(chunks)} blocks, {len(found)} unique reports", flush=True)
    return found


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    reports = crawl_index()
    selected = []
    for rep in reports:
        q = parse_quarter(rep["title"])
        if not q:
            continue
        year, month = q
        if year < 2014 or (year, month) > (2026, 3):
            continue
        rep["year"], rep["month"] = year, month
        rep["filename"] = f"TRAI_PIR_QE_{MONTH_ABBR[month]}_{year}.pdf"
        selected.append(rep)

    # one report per quarter; prefer the earlier release when duplicates exist
    best = {}
    for rep in selected:
        k = (rep["year"], rep["month"])
        if k not in best or rep["release_date"] < best[k]["release_date"]:
            best[k] = rep
    selected = sorted(best.values(), key=lambda r: (r["year"], r["month"]))
    print(f"selected {len(selected)} quarterly reports", flush=True)

    manifest = []
    for i, rep in enumerate(selected, 1):
        path = RAW / rep["filename"]
        if not path.exists():
            print(f"[{i}/{len(selected)}] GET {rep['filename']}", flush=True)
            for attempt in range(3):
                try:
                    rr = requests.get(rep["url"], headers=HEADERS, timeout=180, verify=False)
                    rr.raise_for_status()
                    path.write_bytes(rr.content)
                    break
                except Exception as exc:
                    print(f"   retry {attempt+1}: {exc}", flush=True)
                    time.sleep(2)
            else:
                print(f"   FAILED {rep['filename']}", flush=True)
                continue
        manifest.append({
            "filename": rep["filename"], "quarter_end": f"{rep['year']}-{rep['month']:02d}",
            "title": rep["title"], "release_date": rep["release_date"], "url": rep["url"],
            "bytes": path.stat().st_size, "sha256": sha256(path),
        })
        print(f"   ok {path.stat().st_size/1e6:.1f} MB", flush=True)

    import pandas as pd
    out = RAW / "trai_download_manifest.csv"
    pd.DataFrame(manifest).to_csv(out, index=False)
    print(f"manifest -> {out}", flush=True)


if __name__ == "__main__":
    main()
