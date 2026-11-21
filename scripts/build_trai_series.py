"""
Extract a quarterly macro series from the TRAI Performance Indicator PDFs.

Every value is read from the report text and stored together with the page it
came from. No value is hard-coded. Run scripts/fetch_trai.py first.

Run:  python scripts/build_trai_series.py
"""

from __future__ import annotations

import json
import re
import warnings
from pathlib import Path

import pandas as pd
import pypdf

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "trai"
OUT = ROOT / "data" / "processed" / "trai_quarterly.csv"

RUPEE = r"(?:Rs\.?|`|₹)\s*"
NUM = r"([\d,]+(?:\.\d+)?)"


def num(s):
    return float(str(s).replace(",", ""))


def first(patterns, pages, flags=re.I | re.S):
    """Return (value_as_float, page_number) for the first match of any pattern."""
    for pattern in patterns:
        for i, text in pages:
            m = re.search(pattern, text, flags)
            if m:
                return num(m.group(1)), i
    return None, None


def page_text(path: Path):
    r = pypdf.PdfReader(str(path))
    # ARPU / MOU / subscriber / data snapshots are always in the front matter
    return [(i + 1, p.extract_text() or "") for i, p in enumerate(r.pages[:16])]


BLENDED = [
    rf"Monthly ARPU of\s+Wireless Service\s*:?\s*{RUPEE}{NUM}",
    rf"Monthly ARPU of Wireless Service\s*\([^)]+\)\s*:?\s*{RUPEE}{NUM}",
    rf"Monthly ARPU of Wireless Service\s*:?\s*{RUPEE}{NUM}",
    rf"Monthly ARPU GSM Full Mobility Service\s*:?\s*{RUPEE}{NUM}",
    rf"Monthly Average Revenue Per User \(ARPU\) for Access Services\s*:?\s*{RUPEE}{NUM}",
    rf"blended ARPU[^.]{{0,80}}?Rs\.?\s*{NUM}\s+in\s+Q\.?E\.?",
]
PREPAID = [
    rf"ARPU per month for the pre[\s-]?paid segment is\s*{RUPEE}{NUM}",
    rf"Prepaid ARPU for GSM service per month.{{0,160}}?to\s*{RUPEE}?{NUM}\s+in\s+QE",
]
POSTPAID = [
    rf"ARPU per month for the post[\s-]?paid segment is\s*{RUPEE}{NUM}",
    rf"Postpaid ARPU\s+per month.{{0,160}}?to\s*{RUPEE}?{NUM}\s+in\s+QE",
]
MOU = [
    rf"Minutes of Usage \(MOU\) per subscriber per month\s*-\s*Wireless Service\s*\([^)]+\)\s*{NUM}",
    rf"Minutes of Usage \(MOU\) per subscriber per month\s*-\s*Wireless Service\s*{NUM}",
    rf"Minutes of Usage \(MOU\) per subscriber per month\s*-\s*GSM Full\s+Mobility Service\s*{NUM}",
    rf"Minutes of Usage \(MOU\) per subscriber per month GSM Full\s+Mobility Service\s*{NUM}",
    rf"overall MOU per subscriber per month.{{0,160}}?to\s*{NUM}\s+in\s+QE",
    rf"Mobility Service\s+{NUM}\s*Minutes",
    # last resort: the 2019-12 snapshot puts the value before the unit on the line
    rf"Minutes of Usage \(MOU\) per\s+{NUM}\s+Minutes",
]
SUBS = [rf"Total Wireless Subscribers\s+{NUM}\s+Million"]
DATA_GB = [
    rf"Average Data Usage per unique data subscriber per month.{{0,80}}?{NUM}\s*GB",
    rf"Average Wireless Data Usage per wireless data subscriber per month\s+{NUM}\s*GB",
    rf"Average data usage per wireless data subscriber per month\s+{NUM}\s*GB",
    rf"Data Usage per subscriber per month\s*[–-]\s*Total\s*\(GSM\+CDMA\)\s*{NUM}\s*MB",
    rf"Data Usage per subscriber per month\s*-\s*GSM\s*{NUM}\s*MB",
    rf"Average Wireless Data Usage\s+{NUM}\s*GB",   # 2019-12 snapshot layout
]
RS_GB = [
    rf"Average cost to subscriber per GB wireless data during the quarter\s*{RUPEE}{NUM}",
    rf"Average outgo\(tariff\) per GB wireless data during the quarter\s*{RUPEE}{NUM}",
    rf"Average revenue realization per GB for wireless data usage during\s+the quarter\s*{RUPEE}{NUM}",
    rf"Average revenue realisation per GB for wireless data usage during\s+the quarter\s*{RUPEE}{NUM}",
    rf"revenue realization per GB[^\n]{{0,80}}?{RUPEE}{NUM}",
]


def extract(path: Path):
    pages = page_text(path)
    out = {"source_file": path.name}
    for key, pats in [("arpu_blended", BLENDED), ("arpu_prepaid", PREPAID),
                      ("arpu_postpaid", POSTPAID), ("mou", MOU),
                      ("wireless_subs_m", SUBS), ("data_value", DATA_GB),
                      ("rs_per_gb", RS_GB)]:
        val, pg = first(pats, pages)
        out[key], out[key + "_page"] = val, pg

    # The denominator changed in the TRAI reports: 2014-2017 quote data per
    # wireless subscriber, 2018 onwards per unique wireless data subscriber.
    full = " ".join(t for _, t in pages)
    m = re.search(r"Data Usage per subscriber per month\s*[–-]\s*Total\s*\(GSM\+CDMA\)\s*([\d,.]+)\s*MB", full, re.I)
    if m and out["data_value"]:
        out["data_gb"] = out["data_value"] / 1000      # 1 GB = 1,000 MB
        out["data_basis"] = "per wireless subscriber"
    elif out["data_value"]:
        out["data_gb"] = out["data_value"]
        out["data_basis"] = "per wireless data subscriber"
    else:
        out["data_gb"] = None
        out["data_basis"] = None
    return out


def main():
    files = sorted(RAW.glob("TRAI_PIR_QE_*.pdf"))
    rows = [extract(f) for f in files]
    df = pd.DataFrame(rows)
    df["quarter_end"] = df.source_file.str.extract(r"QE_([A-Za-z]+)_(\d{4})").apply(
        lambda r: f"{r[1]}-{ {'Mar':3,'Jun':6,'Sep':9,'Dec':12}[r[0]]:02d}" if isinstance(r[0], str) else None, axis=1)
    df = df.sort_values("quarter_end").reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(df[["quarter_end", "arpu_blended", "arpu_prepaid", "arpu_postpaid", "mou",
              "wireless_subs_m", "data_gb", "data_basis", "rs_per_gb"]].to_string(index=False))
    print("\nnon-null counts:")
    print(df.notna().sum().to_string())
    print(f"\nwrote {OUT} ({len(df)} quarters)")


if __name__ == "__main__":
    main()
