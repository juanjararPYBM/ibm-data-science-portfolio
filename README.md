# 👨‍⚕️ Juan Pablo Jaramillo Ormaza
### Medical Doctor → Health Data Scientist | Bridging Clinical Expertise & Data Science

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![IBM Certificate](https://img.shields.io/badge/IBM-Data%20Science%20Professional%20Certificate-054ada.svg)](https://www.coursera.org/professional-certificates/ibm-data-science)
[![Status](https://img.shields.io/badge/Status-Completed%20%E2%80%94%20CardioRisk%20%E2%9C%93-brightgreen.svg)]()
[![LinkedIn](https://img.shields.io/badge/LinkedIn-juanjararhad-0077B5.svg)](https://www.linkedin.com/in/juanjararhad/)
[![Domain](https://img.shields.io/badge/Domain-Health%20Data%20Science-red.svg)]()

📍 Medellín, Colombia &nbsp;|&nbsp; 💼 Open to Health Data Science & Clinical Analytics Roles

---

## 🧬 About Me

Private practice physician with **13+ years** of clinical experience — now transitioning into Health Data Science through the IBM Professional Certificate.

My practice had two core dimensions. In **general private medicine**, I ran my own clinic managing a broad patient population with direct, longitudinal relationships. In **oncology support and palliative care**, I served as a clinical bridge: helping patients and families understand complex diagnoses, navigate treatment decisions, and face end-of-life with clarity — often as a last resort when the system had nothing more to offer.

That means I spent 13 years making high-stakes decisions under uncertainty, with incomplete data, where the cost of a wrong call was irreversible. That experience is directly relevant to building clinical decision support systems. I understand what a false negative costs not as a metric, but as a human outcome. I know why model explainability is non-negotiable in healthcare. And I understand the gap between what an algorithm outputs and what a clinician actually needs to act on it.

**Foundation:** 3 modules of *Python for Everybody* (University of Michigan) · IBM Data Science Professional Certificate *(in progress)*

---

## 🚀 Featured Project — Cardiovascular Risk EWS

> **Early Warning Score (EWS) system for ischemic event detection | Full CRISP-DM pipeline**

A production-grade cardiovascular risk stratification system built to clinical standards — not a textbook exercise. Designed for real-world deployment with HL7/FHIR integration, HIPAA compliance, and clinician-facing explainability.

| Phase | Notebook | Status | Key Deliverable |
|---|---|---|---|
| 📋 Business Understanding | [Fase 1 ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/cardiorisk/Fase1_Business_Understanding.ipynb) | ✅ Complete | EWS strategy · stakeholder analysis · ROI $8.2M |
| 🔍 Data Understanding | [Fase 2 ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/cardiorisk/Fase2_Data_Understanding.ipynb) | ✅ Complete | EDA · Spearman heatmap (D3.js) · feature ranking |
| 🛠️ Data Preparation | [Fase 3 ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/cardiorisk/Fase3_Data_Preparation.ipynb) | ✅ Complete | Feature engineering (slope_x_oldpeak, log_oldpeak, vessels_bin) · 18 features · SMOTE |
| 🤖 Modeling | [Fase 4 ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/cardiorisk/Fase4_Modeling.ipynb) | ✅ Complete | GradientBoosting ganador · Recall=1.000 · AUC=0.997 · GridSearchCV 5-fold |
| 📊 Evaluation | [Fase 5 ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/cardiorisk/Fase5_Evaluation.ipynb) | ✅ Complete | Test set sellado · Recall=1.000 · AUC=0.9996 · FN=0 · SHAP top predictor: slope |
| 🚀 Deployment | [Fase 6 ↗](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/cardiorisk/Fase6_Deployment.ipynb) | ✅ Complete | EWS deployable · 3 niveles (Bajo/Medio/Alto) · umbrales p<0.30/0.65 · artefactos joblib |

**Dataset:** [Cardiovascular Disease — Kaggle](https://www.kaggle.com/datasets/jocelyndumlao/cardiovascular-disease-dataset) · 1,000 clinical records · **18 features** (11 original + 3 engineered + 4 OHE)

**Key findings:**
- `slope` (ST segment pendiente) confirmed as primary predictor — validated by 6 SHAP studies 2023–2026
- ECG trio `slope + oldpeak + exerciseangia` provides strongest class separation
- **11.3% of women** present ischemic risk with no classic symptoms → gender-specific thresholds required in Fase 3
- Business case: ~$504K/year per institution · $8.2M across 16 institutions at 20% mortality reduction
- Gradient Boosting logró **Recall=1.000** en test set sellado (0 falsos negativos)

👉 **[Master Index — Full Project Navigation](https://colab.research.google.com/github/juanjararPYBM/ibm-data-science-portfolio/blob/main/proyecto_medico/cardiorisk/Master_Index.ipynb)**

---

## 📂 Additional Projects

### Course 1 — Medical Appointment No-Show Prediction
**Dataset:** 110,000+ Brazilian medical appointments &nbsp;|&nbsp; **Status:** ✅ Complete  
Applied data cleaning, EDA and statistical analysis to identify no-show predictors. 20% no-show rate aligned with my private practice experience in oncology, where missed chemotherapy appointments lead to measurable disease progression.  
→ [`/LABS/course-1-medical-appointments`](./LABS/course-1-medical-appointments)

---

## 🏥 Clinical Domain Expertise

| Area | Detail |
|---|---|
| **General Private Medicine** | 13+ years running own clinic, broad patient population, direct longitudinal relationships |
| **Oncology Patient Support** | Clinical bridge between patients, families and treating physicians — translating complex diagnoses into actionable understanding |
| **Palliative & End-of-Life Care** | Last-resort support for patients the system had discharged — high-stakes decisions, limited information, irreversible outcomes |
| **Clinical Decision-Making** | 13 years of diagnostic reasoning under real uncertainty, with real consequences |
| **Health Informatics** | HL7/FHIR standards, EHR workflows, clinical interoperability |
| **Regulatory** | HIPAA · Ley 1581 Colombia · patient privacy protocols |

---

## 🎓 Certifications

| Certificate | Institution | Issued |
|---|---|---|
| IBM Data Science Professional Certificate *(in progress)* | IBM / Coursera | — |
| Tools for Data Science | IBM | Feb 2026 |
| What is Data Science? | IBM | Feb 2026 |
| Using Python to Access Web Data | University of Michigan | Jan 2026 |
| Python Data Structures | University of Michigan | Dec 2025 |
| Programming for Everybody (Getting Started with Python) | University of Michigan | Dec 2025 |

**IBM Certificate — Course Progress**

| Course | Status |
|---|---|
| Course 1: What is Data Science? | ✅ Complete |
| Course 2: Tools for Data Science | ✅ Complete |
| Course 3: Data Science Methodology | ✅ Complete |
| Course 4: Python for Data Science & AI | 🔄 In Progress |
| Course 5–10 | 📋 Upcoming |

---

## 🛠️ Technical Stack

**Languages:** Python · SQL  
**Libraries:** Pandas · NumPy · Matplotlib · Seaborn · SciPy · Scikit-learn *(in progress)*  
**Visualization:** Chart.js · D3.js · Matplotlib (dark theme) · Seaborn  
**Tools:** Jupyter Notebook · Google Colab · Git / GitHub · VS Code · Anaconda  
**Domain Standards:** HL7/FHIR · HIPAA · CRISP-DM  
**Next:** Scikit-learn ML pipelines · SHAP explainability · MLFlow

---

## 📂 Repository Structure

```
ibm-data-science-portfolio/
├── proyecto_medico/
│   └── cardiorisk/                         # CardioRisk — Cardiovascular EWS (CRISP-DM completo)
│       ├── Fase1_Business_Understanding.ipynb  # ✅ Complete
│       ├── Fase2_Data_Understanding.ipynb      # ✅ Complete
│       ├── Fase3_Data_Preparation.ipynb        # ✅ Complete | 18 features (3 engineered)
│       ├── Fase4_Modeling.ipynb                # ✅ Complete | GradientBoosting Recall=1.0
│       ├── Fase5_Evaluation.ipynb              # ✅ Complete | AUC-ROC=0.9996, FN=0
│       ├── Fase6_Deployment.ipynb              # ✅ Complete | EWS deployable
│       ├── Master_Index.ipynb                  # Navigation hub
│       └── README.md                           # Project documentation
└── LABS/
    └── course-1-medical-appointments/          # No-show prediction (110K records) ✅
```

---

## 📫 Let's Connect

- 💼 [LinkedIn — juanjararhad](https://www.linkedin.com/in/juanjararhad/)
- 📧 juanjara.r10@gmail.com
- 🐙 [GitHub — juanjararPYBM](https://github.com/juanjararPYBM)

> *"After 13 years at the bedside, the highest-leverage decision I could make was to scale clinical insight through data."*
  *Life at the service of life*
