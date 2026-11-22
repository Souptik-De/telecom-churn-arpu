# Telecom Subscriber Churn & ARPU Analytics

A single reproducible Quarto report covering Descriptive, Diagnostic, Predictive and Prescriptive analytics for an Indian telecom subscriber sample, with the national TRAI market series as context.

**Live report:** https://telecom.souptik.xyz

**Submission:** `reports/Analysis.pdf` and `reports/Analysis.html`
**Source:** `notebooks/Analysis.qmd` — the only notebook; it contains every figure, table and line of narrative.

## What is in the report

| Section | Content |
|:---|:---|
| 1. Business Question, Data and Method | Four framed questions, provenance, what the data cannot answer, course-method map |
| 2. Descriptive | TRAI quarterly series 2014–2026, revenue-mix inversion, churn with confidence intervals, ARPU skew and Pareto curve, U-shaped risk curves, K-means and RFM segments |
| 3. Diagnostic | Welch tests and effect sizes, two-proportion tests, logistic GLM with odds ratios and VIF, two exit styles, seasonality test and structural-break regression on the macro series |
| 4. Predictive | Leakage guard, baselines, logistic regression versus random forest, calibration and log loss, cost-based threshold, lift and gains |
| 5. Prescriptive | Per-customer break-even, budget-ranked contact list, segment allocation, pilot power calculation, action playbook |
| 6. Conclusion | Findings, limitations, reproducibility appendix with the acquisition scripts |

## Reproduce

```powershell
# 1. Customer data (Kaggle credentials required)
python scripts/download_data.py
python scripts/prepare_churn.py

# 2. Market data: crawl the TRAI index and download 49 quarterly PDFs
python scripts/fetch_trai.py

# 3. Extract the quarterly series into data/processed/trai_quarterly.csv
python scripts/build_trai_series.py

# 4. Render both deliverables from the single source
.\build.ps1
```

`build.ps1` renders the QMD to HTML and PDF and moves both into `reports/`. The report only reads processed files; it never writes data during rendering.

## Scope and honesty notes

- The customer file is the labelled training split (69,999 rows) of a 2014 Kaggle competition. `circle_id` is 109 for every row: one anonymised service area, not all India.
- Churn is behavioural — zero activity in September 2014 — not a confirmed cancellation.
- TRAI figures are national regulatory statistics, used as market context and as a separate time-series investigation, never mixed into the customer model.
- Retention economics use illustrative offer cost, save rate and a 12-month revenue horizon. ARPU is revenue, not margin.

## Structure

```
notebooks/Analysis.qmd         single source for both reports
reports/Analysis.{pdf,html}    generated deliverables
data/raw/                      Kaggle files and TRAI PDFs (gitignored)
data/processed/                trai_quarterly.csv (tracked), churn_clean.csv (generated)
scripts/                       acquisition, preparation and extraction, listed in the report appendix
```
