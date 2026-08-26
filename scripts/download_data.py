"""
Automated Data Acquisition Script
Acquires the customer-level Kaggle dataset and downloads TRAI Performance Indicator PDFs.
"""

import os
import subprocess
import zipfile
from pathlib import Path
import urllib.request
import ssl

def download_kaggle_dataset():
    raw_dir = Path("data/raw/telecom-churn")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    zip_path = Path("data/raw/telecom-churn-case-study-hackathon-gc1.zip")
    
    if not (raw_dir / "train.csv").exists():
        print("Downloading Kaggle competition dataset...")
        try:
            cmd = ["kaggle", "competitions", "download", "-c", "telecom-churn-case-study-hackathon-gc1", "-p", "data/raw/"]
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Kaggle CLI download encountered an issue: {e}")
            print("Ensure ~/.kaggle/kaggle.json exists with valid credentials.")
            
        if zip_path.exists():
            print(f"Extracting {zip_path}...")
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(raw_dir)
            print("Extraction complete.")
    else:
        print("Customer dataset train.csv already present in data/raw/telecom-churn/")

def download_trai_reports():
    trai_dir = Path("data/raw/trai")
    trai_dir.mkdir(parents=True, exist_ok=True)
    
    reports = {
        "TRAI_PIR_QE_Sep_2014.pdf": "https://www.trai.gov.in/sites/default/files/2024-09/Indicator-Reports29012015.pdf",
        "TRAI_PIR_QE_Mar_2025.pdf": "https://www.trai.gov.in/sites/default/files/2025-06/QPIR_19062025.pdf"
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for filename, url in reports.items():
        dest = trai_dir / filename
        if not dest.exists():
            print(f"Downloading {filename} from {url}...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as response, open(dest, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Saved {filename} ({dest.stat().st_size / 1e6:.2f} MB)")
        else:
            print(f"{filename} already exists in {trai_dir}")

if __name__ == "__main__":
    download_kaggle_dataset()
    download_trai_reports()
    print("Data acquisition complete.")
