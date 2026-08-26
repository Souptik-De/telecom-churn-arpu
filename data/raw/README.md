# Raw Data Provenance & Metadata

This directory stores the raw micro-level (customer data) and macro-level (TRAI regulator reports) datasets used in the Telecom Subscriber Churn and ARPU Analytics project.

> **Note on Version Control:** Large raw CSV and PDF files are excluded from Git commits via `.gitignore` to maintain repository lightweight performance. All raw files can be completely reproduced using the download instructions and automated scripts below.

---

## 1. Micro-Level Dataset (Customer Usage & Churn)

| Attribute | Specification |
|:---|:---|
| **Dataset Name** | Telecom Churn Case Study Hackathon (GC1) |
| **Source Platform** | Kaggle Competitions |
| **Exact Source URL** | https://www.kaggle.com/competitions/telecom-churn-case-study-hackathon-gc1/data |
| **Acquisition Command** | `kaggle competitions download -c telecom-churn-case-study-hackathon-gc1 -p data/raw/` |
| **Acquisition Date** | August 26, 2026 |
| **Time Horizon Covered** | June 2014 – September 2014 (Months 6, 7, 8, 9) |
| **Geographic Scope** | Indian Telecom Operator Subscriber Base |
| **Granularity** | Customer-level (daily & monthly aggregated KPIs) |
| **Extracted Raw Files** | `train.csv` (69,999 rows × 172 columns, 50.5 MB)<br>`test.csv` (30,000 rows × 171 columns, 21.6 MB)<br>`data_dictionary.csv` (36 KPI definitions, 1.5 KB)<br>`sample.csv` (240 KB) |

---

## 2. Macro-Level Datasets (TRAI Performance Indicators)

Official quarterly reports published by the Telecom Regulatory Authority of India (TRAI):

### A. 2014 Benchmark Report (Pre-Jio Era)
| Attribute | Specification |
|:---|:---|
| **Report Title** | The Indian Telecom Services Performance Indicators Report July – September, 2014 |
| **Source Organisation** | Telecom Regulatory Authority of India (TRAI), Government of India |
| **Exact Source URL** | https://www.trai.gov.in/sites/default/files/2024-09/Indicator-Reports29012015.pdf |
| **Saved Local Filename** | `data/raw/trai/TRAI_PIR_QE_Sep_2014.pdf` (3.48 MB) |
| **Acquisition Date** | August 26, 2026 |
| **Reference Period** | Quarter Ending September 2014 (Q2 FY 2014-15) |
| **Market Relevance** | Coincides directly with the observation window of the customer-level dataset (June–September 2014), providing a like-for-like macroeconomic benchmark. |

### B. Recent Market Report (Modern 4G/5G Era)
| Attribute | Specification |
|:---|:---|
| **Report Title** | The Indian Telecom Services Performance Indicators January – March, 2025 |
| **Source Organisation** | Telecom Regulatory Authority of India (TRAI), Government of India |
| **Exact Source URL** | https://www.trai.gov.in/sites/default/files/2025-06/QPIR_19062025.pdf |
| **Saved Local Filename** | `data/raw/trai/TRAI_PIR_QE_Mar_2025.pdf` (5.47 MB) |
| **Acquisition Date** | August 26, 2026 |
| **Reference Period** | Quarter Ending March 2025 (Q4 FY 2024-25) |
| **Market Relevance** | Modern telecommunications benchmark reflecting nationwide 4G/5G penetration, consolidated market structure, and higher data consumption. |

---

## 3. Structural Break Note & Macro Sanity Caution

> **CRITICAL CAVEAT:**
> Direct numerical comparisons between the 2014 customer dataset ARPU and modern TRAI ARPU must account for the **Reliance Jio market entry in September 2016**. Jio's launch introduced free voice calling, bundled 4G high-speed data, and aggressive promotional pricing, permanently altering the Indian telecom revenue structure and industry ARPU trajectories.
