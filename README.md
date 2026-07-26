# Employee Retention & Attrition Predictive Analytics

> **Google Advanced Data Analytics Professional Certificate (Coursera)**  
> *Capstone Project*

---

## 📌 Project Overview

This repository contains the end-to-end data analytics and machine learning solution for predicting employee attrition. Using HR analytics data, the project explores key drivers behind employee turnover—such as project workload, monthly working hours, tenure, and promotion stagnation—and builds predictive models to help HR teams proactively identify retention risks.

### Key Insights & Findings
* **Workload Extremes**: Employees assigned to either **2 projects** (underutilized/disengaged, ~54.17% attrition) or **6–7 projects** (overworked/burnout, up to 100% attrition) exhibit the highest turnover rates.
* **The 4–5 Year Career Cliff**: Attrition peaks significantly among mid-tenure employees facing promotion stagnation and salary compression.
* **Model Performance**: The tuned **Random Forest Model (Round 2)** achieved an **AUC-ROC of 0.97** and an **F1-Score of 0.89**, making it the top-performing model for identifying high-risk employees without relying on subjective satisfaction scores.

---

## 📁 Project Structure

```text
Capstone_Project/
│
├── data/
│   ├── df_clean.csv                                 # Processed and deduplicated dataset
│   └── HR_capstone_dataset.csv                      # Raw initial HR dataset
│
├── reports/
│   ├── executive_summary_report.py                  # Report generation script
│   └── executive_summary_report.pdf                 # Final Executive Summary PDF
│
├── models/
│   ├── hr_rf1.pkl                                   # Trained Random Forest Model (Round 1)
│   └── hr_rf2.pkl                                   # Tuned Random Forest Model (Round 2 - Recommended)
│
├── outputs/
│   ├── charts/                                      # Saved Exploratory Data Analysis & Model Evaluation Plots
│   │   ├── avg_monthly_hrs_by_evaluation_score.png
│   │   ├── avg_monthly_hrs_by_promotion.png
│   │   ├── avg_monthly_hrs_satisfaction_level.png
│   │   ├── correlation_heatmap.png
│   │   ├── decision_tree_feature_importance.png
│   │   ├── department_status_count.png
│   │   ├── logistic_regression_confusion_matrix.png
│   │   ├── number_of_projects.png
│   │   ├── random_forest2_confusion_matrix.png
│   │   ├── random_forest2_feature_importance.png
│   │   ├── roc_curve_comparison.png
│   │   ├── salary_analysis_by_tenure.png
│   │   ├── salary_tier_composition_by_tenure.png
│   │   └── satisfaction_by_tenure.png
│   │
│   └── tables/                                      # Output statistical summary tables
│       ├── attrition_per_project.csv
│       ├── composition_matrix_of_salary.csv
│       ├── department_status_counts.csv
│       ├── model_comparison.csv
│       ├── promotion_last5yrs_statistics.csv
│       └── satisfaction_vs_leaving.csv
│
├── notebooks/
│   └── HR_DataAnalysis.ipynb                        # Main Jupyter Notebook (EDA, Modeling, Evaluation)
│
├── requirements.txt                                 # Project dependencies
└── README.md                                        # Project documentation

```
---

## 🛠️ Machine Learning Models Summary

| Model | Precision | Recall | F1-Score | Accuracy | AUC-ROC |
|--------|----------:|-------:|---------:|---------:|--------:|
| Logistic Regression | 0.44 | 0.27 | 0.33 | 0.82 | 0.88 |
| Decision Tree (Round 1) | 0.94 | 0.91 | 0.92 | 0.98 | 0.98 |
| Random Forest (Round 1) | 0.96 | 0.92 | 0.94 | 0.98 | 0.98 |
| Decision Tree (Round 2) | 0.78 | 0.92 | 0.85 | 0.94 | 0.95 |
| Random Forest (Round 2) | 0.87 | 0.90 | 0.89 | 0.96 | 0.97 |

> **Note:** Round 2 models excluded the direct subjective metric (`satisfaction_level`) to evaluate feature importance using only operational variables.

---

# 🚀 Getting Started

## Prerequisites

- Python 3.12+
- Jupyter Notebook or JupyterLab

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Capstone_Project.git
cd Capstone_Project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the analysis notebook

```bash
jupyter notebook notebooks/HR_DataAnalysis.ipynb
```

---

# 💡 HR Recommendations

Based on the analysis and machine learning results:

- **📋 Manage Project Workloads**
  - Limit active assignments to **3–5 projects per employee** to reduce both underutilization and burnout.

- **⏱️ Monitor Overtime**
  - Establish alert thresholds for employees consistently working **more than 215 hours per month**.

- **📈 Support Career Progression**
  - Conduct targeted retention reviews for high-performing employees entering **Years 3–4 of tenure**, when turnover risk increases.

---

### MIT License
Copyright (c) 2026 Aparna S Pophale

**Ethical Use Notice:**
This project is intended for educational, research, and professional learning purposes.
Any use that misrepresents authorship or is intended to deceive others is unethical.
Attribution to the original author is required under the MIT License.
