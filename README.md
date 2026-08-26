# Telecom Subscriber Churn & ARPU Analytics

**Revenue-at-Risk Churn Prediction & Retention ROI Optimization for an Indian Telecom Operator**

This repository contains the complete, reproducible analytical pipeline for **Task 1 (Data Acquisition)** and **Task 2 (Descriptive Analytics)**, investigating subscriber attrition patterns and ARPU dynamics in the Indian telecommunications market.

---

## 📑 Core Analytical Reports

The full descriptive analytics investigation is rendered into unified, publication-grade formats:

- 🌐 **[Analysis.html](Analysis.html)**: Interactive HTML report featuring custom styling, data tables, code tools, and interactive visual diagnostics.
- 📄 **[Analysis.pdf](Analysis.pdf)**: Complete, standalone PDF document with embedded high-resolution figures, statistical distribution tables, and macroeconomic benchmarking.

---

## 🎯 Framed Business Question (Descriptive Analytics)

> **"What is the churn rate and average revenue per user (ARPU) across different customer segments (e.g. by customer value tier, usage level, recharge behavior, and tenure), and how does ARPU differ between customers who churn and those who don't, for an Indian telecom operator?"**

---

## 📂 Repository Structure

```
telecom-churn-arpu/
│
├── Analysis.qmd               # Master continuous Quarto analytical document
├── Analysis.html              # Rendered interactive HTML report
├── Analysis.pdf               # Rendered publication-ready PDF report
├── _quarto.yml                # Global Quarto configuration (HTML & Typst PDF)
├── styles.css                 # Clean modern typography & styling for HTML
├── requirements.txt           # Python dependency specification
├── README.md                  # Project overview & execution guide
│
├── data/
│   ├── raw/
│   │   ├── README.md          # Full data provenance, source URLs & dates
│   │   ├── telecom-churn/     # Micro customer dataset (train.csv, test.csv)
│   │   └── trai/              # Macro regulatory reports (2014 & 2025 PDFs)
│   └── processed/
│       ├── trai_arpu_timeseries.csv  # Extracted TRAI ARPU & subscriber series
│       └── churn_clean.csv           # Cleaned & feature-engineered dataset
│
├── notebooks/
│   ├── 01_data_prep.qmd       # Modular data cleaning & feature engineering
│   └── 02_eda.qmd             # Modular exploratory data analysis
│
└── scripts/
    ├── download_data.py       # Automated Kaggle & TRAI downloader
    └── extract_trai_data.py   # PDF parser extracting TRAI timeseries
```

---

## ⚡ Quickstart & Reproducibility Guide

Follow these steps to recreate the entire analytical pipeline from scratch:

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/Souptik-De/telecom-churn-arpu.git
cd telecom-churn-arpu

# Create & activate Python virtual environment
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Data Acquisition
```bash
# Ensure ~/.kaggle/kaggle.json has your Kaggle credentials
python scripts/download_data.py
python scripts/extract_trai_data.py
```

### 3. Render Reports (HTML & PDF)
```bash
# Render to interactive HTML
quarto render Analysis.qmd --to html

# Render to publication PDF (via Typst)
quarto render Analysis.qmd --to typst --output Analysis.pdf
```

---

## 📊 Summary of Key Findings

1. **Baseline Churn Rate:** Overall subscriber attrition is **10.19%** (7,132 churners / 69,999 base).
2. **High-Value Concentration:** The top 30% high-value customer segment (average recharge $\ge$ ₹477.50 in months 6 & 7) exhibits an **8.28% churn rate** with **₹558.59 mean ARPU**, driving over 60% of total operator cash flow.
3. **Pre-Churn Revenue Collapse:** Churned subscribers experience a severe **62.95% drop in ARPU** from June (₹308.29) to August (₹114.23), providing a critical leading indicator prior to complete cessation of activity in Month 9.
4. **Tenure Loyalty Effect:** Early-tenure subscribers (<1 year) churn at **15.85%**, whereas long-tenure customers (4+ years) churn at only **4.71%** (>3x retention stability).
5. **Data Service Stickiness:** Subscribers with 2G/3G mobile data packs exhibit lower churn (**8.72%**) and higher revenue (**₹368.52 ARPU**) compared to voice-only accounts (**10.88% churn**, **₹239.16 ARPU**).
6. **Macro Regulatory Context:** The dataset's 2014 ARPU (₹283.13) represents active revenue-generating accounts, realistically tracking above the TRAI 2014 national blended average (₹115.72). Modern TRAI ARPU (₹182.95 in 2025) reflects post-Jio market recovery following the September 2016 structural break.
