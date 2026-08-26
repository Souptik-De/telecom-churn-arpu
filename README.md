# Telecom Subscriber Churn & ARPU Analytics

**Revenue-at-Risk Churn Prediction & Retention ROI Optimization for an Indian Telecom Operator**

This repository contains the complete, reproducible analytical pipeline for **Task 1 (Data Acquisition)** and **Task 2 (Descriptive Analytics)**, investigating subscriber attrition patterns and ARPU dynamics in the Indian telecommunications market.

---

## 🧭 Navigation Guide for Evaluators & Professors

| Deliverable | Location | Description |
|:---|:---|:---|
| 📄 **Final PDF Report** | **[reports/Analysis.pdf](reports/Analysis.pdf)** | Publication-grade, typography-optimized standalone PDF with complete methodology, visual diagnostics, and regulatory benchmarks. |
| 🌐 **Interactive HTML Report** | **[reports/Analysis.html](reports/Analysis.html)** | Interactive web report with code folding, responsive tables, and styling. |
| 📓 **Master Quarto Notebook** | **[notebooks/Analysis.qmd](notebooks/Analysis.qmd)** | Master computational notebook combining data acquisition, feature engineering, and descriptive analytics. |
| 🧹 **Data Prep Notebook** | **[notebooks/01_data_prep.qmd](notebooks/01_data_prep.qmd)** | Modular notebook focusing on data cleaning, high-value filtering, and feature engineering. |
| 📊 **EDA Notebook** | **[notebooks/02_eda.qmd](notebooks/02_eda.qmd)** | Modular exploratory data analysis answering the framed business questions. |

---

## 🎯 Framed Business Question (Descriptive Analytics)

> **"What is the churn rate and average revenue per user (ARPU) across different customer segments (e.g., by customer value tier, usage level, recharge behavior, and tenure), and how does ARPU differ between customers who churn and those who don't, for an Indian telecom operator?"**

---

## 📂 Repository Structure

```
telecom-churn-arpu/
│
├── reports/                   # Compiled final deliverables
│   ├── Analysis.pdf           # Standalone publication-ready PDF report
│   ├── Analysis.html          # Interactive HTML report
│   └── Analysis_files/        # Assets and styling for HTML report
│
├── notebooks/                 # Source Quarto documents & computational notebooks
│   ├── Analysis.qmd           # Master end-to-end continuous analytical document
│   ├── 01_data_prep.qmd       # Modular data preparation & feature engineering
│   └── 02_eda.qmd             # Modular exploratory data analysis
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
├── scripts/
│   ├── download_data.py       # Automated Kaggle & TRAI downloader
│   └── extract_trai_data.py   # PDF parser extracting TRAI timeseries
│
├── styles.css                 # Clean modern typography & table styling for HTML
├── requirements.txt           # Python dependency specification
├── _quarto.yml                # Global Quarto configuration (HTML & Typst PDF)
└── README.md                  # Project overview & evaluator guide
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
# Ensure ~/.kaggle/kaggle.json has your Kaggle API key
python scripts/download_data.py
python scripts/extract_trai_data.py
```

### 3. Render Reports (HTML & PDF)
```bash
# Render to publication PDF (via Typst engine)
quarto render notebooks/Analysis.qmd --to typst

# Render to interactive HTML
quarto render notebooks/Analysis.qmd --to html

# Copy rendered deliverables into reports/
Copy-Item notebooks/Analysis.pdf reports/Analysis.pdf -Force
Copy-Item notebooks/Analysis.html reports/Analysis.html -Force
Copy-Item -Recurse notebooks/Analysis_files reports/Analysis_files -Force
```

---

## 📊 Summary of Key Findings

1. **Baseline Churn Rate:** Overall subscriber attrition is **10.19%** (7,132 churners out of 69,999 base).
2. **High-Value Concentration:** The top 30% high-value customer segment (average recharge $\ge$ ₹477.50 in months 6 & 7) exhibits an **8.28% churn rate** with **₹558.59 mean ARPU**, generating over 60% of total operator cash flow.
3. **Pre-Churn Revenue Collapse:** Churned subscribers experience a severe **62.95% drop in ARPU** from June (₹308.29) to August (₹114.23), while retained subscribers maintain steady growth (+6.16%, from ₹280.28 to ₹297.54).
4. **Tenure Loyalty Effect:** Early-tenure subscribers (<1 year) churn at **15.85%**, whereas long-tenure customers (4+ years) churn at only **4.71%** (>3x retention stability).
5. **Data Service Stickiness:** Subscribers with 2G/3G mobile data packs exhibit lower churn (**8.72%**) and higher revenue (**₹368.52 ARPU**) compared to voice-only accounts (**10.88% churn**, **₹239.16 ARPU**).
6. **Macro Regulatory Context:** The dataset's 2014 ARPU (₹283.13) represents active revenue-generating accounts, realistically tracking above the TRAI 2014 national blended average (₹115.72). Modern TRAI ARPU (₹182.95 in 2025) reflects post-Jio market recovery following the transformative September 2016 structural break.
