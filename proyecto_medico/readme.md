# 🫀 Cardiovascular Risk EWS — Full CRISP-DM Project

---

> *Dear reader,*
>
> Throughout my career I have faced many challenges. The hardest one has been the frustration of watching patients leave when treatment options run out — or when it is already too late to prevent or reverse the consequences of a disease. Losing loved ones to silent conditions that go unnoticed, without a clear diagnosis or a timely intervention.
>
> This first encounter with data science and AI tools opened a completely new landscape for me. I used several AI assistants along the way — Gemini, Grok, Minimax, and finally Claude. It is genuinely exciting to discover what becomes possible when you combine medical knowledge with the power of programming, data tools, visualization, and AI — all working together. The hundreds of lines of code, the visual details, the animations: none of it would have been achievable alone. Some tools better than others, it must be said.
>
> To you, dear reader: for the full experience of this project, I warmly invite you to explore it interactively through Colab. All feedback is more than welcome. I hope that in my next projects I can refine what I have learned here, and complement it with everything I still have left to discover.
>
> — *Juan Pablo Jaramillo Ormaza, MD*

### 👋 [Welcome — Open the Full Project in Google Colab](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/Master_Index.ipynb)

---

> **Early Warning Score (EWS) system for ischemic event detection**  
> IBM Data Science Professional Certificate · CRISP-DM Methodology · juanjararPYBM

[![CRISP-DM](https://img.shields.io/badge/Methodology-CRISP--DM-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Phases%201--2%20Complete-brightgreen.svg)]()
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle%201K%20records-20beff.svg)](https://www.kaggle.com/datasets/jocelyndumlao/cardiovascular-disease-dataset)
[![Domain](https://img.shields.io/badge/Domain-Clinical%20Decision%20Support-red.svg)]()

---

### 🚀 Launch Project

[![Open Master Index](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/Master_Index.ipynb)
&nbsp;&nbsp;
[![Fase 1](https://img.shields.io/badge/Fase%201-Business%20Understanding-00b4d8?style=flat)](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/Fase1_Business_Understanding.ipynb)
&nbsp;&nbsp;
[![Fase 2](https://img.shields.io/badge/Fase%202-Data%20Understanding-00f5d4?style=flat)](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/Fase2_Data_Understanding.ipynb)

---

## 🎯 Project Overview

A production-grade cardiovascular risk stratification system designed to detect ischemic events before clinical collapse. Built under the full CRISP-DM framework with real-world deployment constraints: HL7/FHIR integration, HIPAA compliance, sub-200ms inference latency, and clinician-facing explainability.

**The clinical problem:** Current hospital systems are reactive. By the time a cardiac event is detected, the intervention window has often closed. This EWS aims to stratify patient risk 6–12 hours in advance, enabling proactive triage and UCI resource optimization.

**Business case:** ~$504K/year per institution · $8.2M across 16 institutions at a projected 20% mortality reduction.

---

## 📊 Dataset

| Property | Value |
|---|---|
| Source | [Cardiovascular Disease Dataset — Kaggle](https://www.kaggle.com/datasets/jocelyndumlao/cardiovascular-disease-dataset) |
| Author | jocelyndumlao |
| Records | 1,000 clinical observations |
| Variables | 13 (4 categorical · 2 binary · 6 numerical · 1 target) |
| Target | `target` — Binary: 0 = Healthy, 1 = Cardiovascular Risk |
| Standard | HL7/FHIR compatible |

**Variables:**

| Variable | Type | Clinical Meaning |
|---|---|---|
| `gender` | Categorical | Biological sex (0=F, 1=M) |
| `age` | Numerical | Patient age (range: 20–80 years) |
| `chestpain` | Categorical | Chest pain type (0=Typical → 3=Asymptomatic) |
| `restingBP` | Numerical | Resting systolic blood pressure (94–200 mmHg) |
| `serumcholestrol` | Numerical | Total serum cholesterol (0–602 mg/dl) |
| `fastingbloodsugar` | Binary | Fasting glucose > 120 mg/dl |
| `restingrelectro` | Categorical | Resting ECG (0=Normal, 1=ST-T, 2=LVH) |
| `maxheartrate` | Numerical | Maximum heart rate achieved (71–202 bpm) |
| `exerciseangia` | Binary | Exercise-induced angina |
| `oldpeak` | Numerical | ST segment depression (0.0–6.2) |
| `slope` | Categorical | ST segment slope (1=Up, 2=Flat, 3=Down) |
| `noofmajorvessels` | Numerical | Major vessels by fluoroscopy (0–3) |
| `target` | **Target** | Cardiovascular risk diagnosis |

---

## 🗺️ CRISP-DM Pipeline

| Phase | Notebook | Status | Key Output |
|---|---|---|---|
| 📋 **1. Business Understanding** | [Open in Colab ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/Fase1_Business_Understanding.ipynb) | ✅ Complete | EWS strategy · stakeholder cards · ROI methodology |
| 🔍 **2. Data Understanding** | [Open in Colab ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/Fase2_Data_Understanding.ipynb) | ✅ Complete | Full EDA · Spearman heatmap · feature ranking |
| 🛠️ **3. Data Preparation** | Fase 3 | 🔄 In Progress | Feature engineering · class imbalance |
| 🤖 **4. Modeling** | Fase 4 | 📋 Planned | Random Forest · XGBoost · SHAP |
| 📊 **5. Evaluation** | Fase 5 | 📋 Planned | Clinical validation · Recall > 80% |
| 🚀 **6. Deployment** | Fase 6 | 📋 Planned | HL7/FHIR · real-time scoring |

👉 **[Master Index — Full Navigation Hub](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/Master_Index.ipynb)**

---

## 📋 Phase 1 — Business Understanding

**Objective:** Define the clinical and business problem with enough precision to drive all downstream modeling decisions.

### EWS Risk Stratification

| Level | Threshold | Action |
|---|---|---|
| 🟢 Low Risk | p < 0.30 | Standard monitoring |
| 🟡 Medium Risk | 0.30 ≤ p ≤ 0.65 | Intensive surveillance |
| 🔴 High Risk | p > 0.65 | Immediate UCI alert |

### Success Criteria

**Technical KPIs:** Recall > 80% on High Risk class · AUC-ROC > 0.85 · Type II error < 5% · Inference latency < 200ms

**Business KPIs:** 20% mortality reduction · >70% clinical adoption rate · Positive ROI within 12 months

### Stakeholders

| Stakeholder | Priority Concern | Key Metric |
|---|---|---|
| 👨‍⚕️ Physicians | Model accuracy in real workflow | Recall > 80% · 6–12h detection window |
| 🏥 Hospital Admin | Demonstrable ROI | $45K investment → $8.2M return |
| 💾 IT Department | Security & integration | HIPAA · HL7/FHIR · <200ms latency |
| 🫀 Patients | Privacy + early detection | −20% mortality · no overdiagnosis |

### ROI Methodology
```
UCI cost ~$1,200/day × 20% reduction × 150 patients/year × 14 days = ~$504K/year
$504K/year × 16 institutions = $8.2M
Investment breakdown: $20K development · $15K infrastructure · $10K training = $45K total
ROI: 320% in 12 months
```

### Constraints
- Inference time < 200ms for real-time EHR integration
- Full HIPAA compliance + Ley 1581 (Colombia)
- Model must be explainable — black-box models not acceptable for clinical validation

---

## 🔍 Phase 2 — Data Understanding

**Architecture:** 8 modular blocks, each executable as an independent Colab cell.

### Key Findings

**1. Primary Predictor — `slope` (ST Segment)**

`slope` holds the highest Spearman correlation with `target` in the dataset. A descending ST slope is the electrophysiological signature of obstructive ischemia — confirmed by SHAP importance rankings across 6 independent studies (2023–2026).

**2. The Electrical Trio**

`slope + oldpeak + exerciseangia` together form the strongest combination for class separation. These three ECG-derived features are the priority candidates for feature engineering in Phase 3:
- `slope × oldpeak` interaction (electrical pair)
- `log(oldpeak + 1)` transformation (right skew correction)
- `noofmajorvessels` binary encoding (≥2 vessels)

**3. Silent Female Risk**

**11.3% of women** in the dataset present cardiovascular risk with no classic symptoms (asymptomatic chest pain profile). Asymptomatic presentation ranks as the #2 SHAP predictor in related studies. Gender-specific thresholds are required in Phase 3 to avoid systematic underdiagnosis in female patients.

**4. Spearman Justification**

Spearman correlation was chosen over Pearson because the variables contain ordinal data (`slope`, `chestpain`, `restingrelectro`) and non-normal distributions. Spearman's monotonic ranking approach is appropriate and validates the use of non-parametric models (Random Forest, XGBoost) in Phase 4.

### Visualizations (Phase 2)

| Block | Type | Technology |
|---|---|---|
| B3 — Prevalence + Age distribution | Animated bar/histogram | Chart.js |
| B4 — Spearman correlation matrix | Interactive heatmap | D3.js |
| B5 — Categorical EDA | Animated bar charts | Chart.js |
| B6 — Gender × Age stratification | Multi-panel grid | Matplotlib (dark theme) |
| B7 — Conclusions + F3 roadmap | Evidence cards with citations | HTML/CSS |

### Scientific References

| # | Study | Finding | Link |
|---|---|---|---|
| 1 | Springer 2026 | `slope` confirmed as primary SHAP predictor | [DOI](https://doi.org/10.1007/s10791-026-09973-3) |
| 2 | PMC / RF+SHAP 2025 | Random Forest + SHAP for cardiovascular risk | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12204762/) |
| 3 | Nature Sci Reports 2025 | Silent ischemic risk in women | [Nature](https://www.nature.com/articles/s41598-025-97547-6) |
| 4 | Nature Sci Reports 2024 | ECG features + exercise variables | [DOI](https://doi.org/10.1038/s41598-024-69071-6) |
| 5 | Frontiers Medicine 2023 | SHAP explainability in cardiac ML models | [DOI](https://doi.org/10.3389/fmed.2023.1150933) |

---

## 🛠️ Phase 3 — Data Preparation *(In Progress)*

**Priority engineering tasks derived from Phase 2 findings:**

- `slope × oldpeak` — interaction feature (electrical pair)
- `log(oldpeak + 1)` — correct right skew
- `noofmajorvessels_bin` — binary encoding (0 vs ≥1, and ≥2)
- Gender-stratified risk thresholds
- Class imbalance handling (SMOTE or class weights)
- Train/validation/test split with stratification on `target`

---

## 🤖 Phase 4 — Modeling *(Planned)*

**Candidate models:**
- Random Forest Classifier (interpretable, handles ordinal vars)
- XGBoost (gradient boosting, strong baseline)
- Logistic Regression (clinical interpretability benchmark)

**Explainability:** SHAP values for all final models — required for clinical validation.

**Primary optimization target:** Recall on High Risk class (minimize false negatives — the highest-cost error in this domain).

---

## 🏗️ Technical Stack

```python
# Core
import pandas as pd
import numpy as np
from scipy import stats

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
# + Chart.js (animated) + D3.js (interactive heatmap)

# Modeling (Phase 4)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, roc_auc_score
import shap
```

**Environment:** Google Colab · Python 3.10+  
**Data loading:** Robust 3-method fallback (`%store` → `kagglehub` → manual CSV)  
**Standards:** HL7/FHIR · HIPAA · CRISP-DM


## 🛠️ Languages & Libraries

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

**Python Libraries**

![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4c72b0?style=flat&logo=python&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat&logo=scipy&logoColor=white)
![IPython](https://img.shields.io/badge/IPython-3776AB?style=flat&logo=jupyter&logoColor=white)

**Visualization & Animation**

![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)
![D3.js](https://img.shields.io/badge/D3.js-F9A03C?style=flat&logo=d3dotjs&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=flat&logo=greensock&logoColor=white)

**Tools & Environment**

![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=flat&logo=googlecolab&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=flat&logo=kaggle&logoColor=white)

---

## 📫 Contact

- 💼 [LinkedIn — juanjararhad](https://www.linkedin.com/in/juanjararhad/)
- 🐙 [GitHub — juanjararPYBM](https://github.com/juanjararPYBM)
- 📧 juanjara.r10@gmail.com

---

*Part of the [IBM Data Science Professional Certificate Portfolio](https://github.com/juanjararPYBM/ibm-data-science-portfolio)*
