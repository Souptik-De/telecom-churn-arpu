# Telecom Subscriber Churn & ARPU Analytics

**Revenue-at-Risk Churn Prediction & Retention ROI Optimization for an Indian Telecom Operator**

This repository contains the complete, reproducible analytical pipeline for **Descriptive, Diagnostic, Predictive, and Prescriptive Analytics**, investigating subscriber attrition patterns and ARPU dynamics in the Indian telecommunications market.

---

## 🧭 Navigation Guide for Evaluators & Professors

| Deliverable | Location | Description |
|:---|:---|:---|
| 📄 **Master PDF Report (all 4 stages)** | **[reports/Analysis.pdf](reports/Analysis.pdf)** | Publication-grade standalone PDF combining descriptive, diagnostic, predictive, and prescriptive analytics. |
| 🌐 **Master HTML Report (all 4 stages)** | **[reports/Analysis.html](reports/Analysis.html)** | Interactive self-contained web report with code folding and responsive tables. |
| 📓 **Master Quarto Notebook** | **[notebooks/Analysis.qmd](notebooks/Analysis.qmd)** | Single combined computational notebook covering all four analytics types. |
| 🧹 **01 Data Prep** | **[notebooks/01_data_prep.qmd](notebooks/01_data_prep.qmd)** / [HTML](reports/01_data_prep.html) / [PDF](reports/01_data_prep.pdf) | Data cleaning, high-value filtering, and feature engineering. |
| 📊 **02 Descriptive** | **[notebooks/02_descriptive.qmd](notebooks/02_descriptive.qmd)** / [HTML](reports/02_descriptive.html) / [PDF](reports/02_descriptive.pdf) | Churn rates, ARPU distributions, segment breakdowns, TRAI benchmarks. |
| 🔍 **03 Diagnostic** | **[notebooks/03_diagnostic.qmd](notebooks/03_diagnostic.qmd)** / [HTML](reports/03_diagnostic.html) / [PDF](reports/03_diagnostic.pdf) | Hypothesis tests, effect sizes, and M8 decay attribution (why churn happens). |
| 🤖 **04 Predictive** | **[notebooks/04_predictive.qmd](notebooks/04_predictive.qmd)** / [HTML](reports/04_predictive.html) / [PDF](reports/04_predictive.pdf) | Leak-free Logistic Regression vs Random Forest on Good-Phase features, lift analysis. |
| 💰 **05 Prescriptive** | **[notebooks/05_prescriptive.qmd](notebooks/05_prescriptive.qmd)** / [HTML](reports/05_prescriptive.html) / [PDF](reports/05_prescriptive.pdf) | Retention ROI, budget-constrained targeting, and action playbook. |

---

## 🎯 Framed Business Questions

- **Descriptive:** *"What is the churn rate and ARPU across customer segments (value tier, usage, recharge, tenure), and how does ARPU differ between churned and retained subscribers?"*
- **Diagnostic:** *"Why do subscribers churn? Which Good-Phase behaviours significantly distinguish future churners, and how large are those effects?"*
- **Predictive:** *"Who will churn next month using only pre-Action-Phase information, and how much revenue does each risk decile represent?"*
- **Prescriptive:** *"Which subscribers should receive which retention action under a fixed budget to maximise net retained revenue?"*

**Leakage guard:** predictive/prescriptive models use Good-Phase M6/M7 features only; all `*_8` Action-Phase columns are excluded from training.

---

## 📂 Repository Structure

```
telecom-churn-arpu/
│
├── reports/                   # Compiled final deliverables (self-contained HTML + standalone PDF)
│   ├── Analysis.pdf / .html   # Master combined report (all 4 stages)
│   ├── 01_data_prep.pdf / .html
│   ├── 02_descriptive.pdf / .html
│   ├── 03_diagnostic.pdf / .html
│   ├── 04_predictive.pdf / .html
│   └── 05_prescriptive.pdf / .html
│
├── notebooks/                 # Source Quarto documents & computational notebooks
│   ├── Analysis.qmd           # Master end-to-end analytical document (all 4 stages)
│   ├── 01_data_prep.qmd       # Modular data preparation & feature engineering
│   ├── 02_descriptive.qmd     # Modular descriptive analytics
│   ├── 03_diagnostic.qmd      # Modular diagnostic analytics
│   ├── 04_predictive.qmd      # Modular predictive modelling (sklearn LogReg + RF)
│   └── 05_prescriptive.qmd    # Modular prescriptive ROI & targeting
│
├── data/
│   ├── raw/
│   │   ├── README.md          # Full data provenance, source URLs & dates
│   │   ├── telecom-churn/     # Micro customer dataset (train.csv, test.csv)
│   │   └── trai/              # Macro regulatory reports (2014 & 2025 PDFs)
│   └── processed/
│       ├── trai_arpu_timeseries.csv  # Extracted TRAI ARPU & subscriber series
│       └── churn_clean.csv           # Cleaned & feature-engineered dataset (git-ignored, 57 MB)
│
├── scripts/
│   ├── download_data.py       # Automated Kaggle & TRAI downloader
│   └── extract_trai_data.py   # PDF parser extracting TRAI timeseries
│
├── styles.css                 # Clean modern typography & table styling for HTML
├── requirements.txt           # Python dependency specification
├── _quarto.yml                # Global Quarto configuration (HTML embed-resources & Typst PDF)
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
# Render every notebook to self-contained HTML (guaranteed)
for f in notebooks/01_data_prep notebooks/02_descriptive notebooks/03_diagnostic notebooks/04_predictive notebooks/05_prescriptive notebooks/Analysis; do
  quarto render $f.qmd --to html
done

# Render to standalone PDF via bundled Typst engine (best-effort)
for f in notebooks/01_data_prep notebooks/02_descriptive notebooks/03_diagnostic notebooks/04_predictive notebooks/05_prescriptive notebooks/Analysis; do
  quarto render $f.qmd --to typst
done

# Copy rendered deliverables into reports/ (Linux/macOS)
cp -f notebooks/01_data_prep.html notebooks/01_data_prep.pdf \
      notebooks/02_descriptive.html notebooks/02_descriptive.pdf \
      notebooks/03_diagnostic.html notebooks/03_diagnostic.pdf \
      notebooks/04_predictive.html notebooks/04_predictive.pdf \
      notebooks/05_prescriptive.html notebooks/05_prescriptive.pdf \
      notebooks/Analysis.html notebooks/Analysis.pdf reports/
# HTML files are self-contained (embed-resources: true); no *_files folders needed.
```

---

## 📊 Summary of Key Findings

1. **Baseline Churn Rate:** Overall subscriber attrition is **10.19%** (7,132 churners out of 69,999 base).
2. **High-Value Concentration:** The top 30% high-value customer segment (average recharge $\ge$ ₹477.50 in months 6 & 7) exhibits an **8.28% churn rate** with **₹558.59 mean ARPU**, generating over 60% of total operator cash flow.
3. **Pre-Churn Revenue Collapse:** Churned subscribers experience a severe **62.95% drop in ARPU** from June (₹308.29) to August (₹114.23), while retained subscribers maintain steady growth (+6.16%, from ₹280.28 to ₹297.54).
4. **Tenure Loyalty Effect:** Early-tenure subscribers (<1 year) churn at **15.85%**, whereas long-tenure customers (4+ years) churn at only **4.71%** (>3x retention stability).
5. **Data Service Stickiness:** Subscribers with 2G/3G mobile data packs exhibit lower churn (**8.72%**) and higher revenue (**₹368.52 ARPU**) compared to voice-only accounts (**10.88% churn**, **₹239.16 ARPU**).
6. **Macro Regulatory Context:** The dataset's 2014 ARPU (₹283.13) represents active revenue-generating accounts, realistically tracking above the TRAI 2014 national blended average (₹115.72). Modern TRAI ARPU (₹182.95 in 2025) reflects post-Jio market recovery following the transformative September 2016 structural break.
7. **Diagnostic Drivers:** Tenure dominates protection; recharge frequency beats raw spend (churners can be high-ARPU but infrequent); M7→M8 collapse of 55-70% on ARPU/MOU/recharge mediates M9 silence.
8. **Predictive Performance:** Leak-free Random Forest (Good-Phase only, 200 trees, 5-fold CV) beats balanced Logistic Regression on ROC-AUC and PR-AUC; operating threshold **0.3-0.4**; top 20-30% of scores capture the majority of churners and revenue at risk.
9. **Prescriptive ROI:** Contact rule `p x V x 20% > Rs 160` maximises net retained revenue at Rs 150 offer cost; rank by expected saving (`p x V`) under fixed budgets; prioritise HVC and sub-1-year voice-only cohorts; pilot with 10% control, retrain quarterly.
