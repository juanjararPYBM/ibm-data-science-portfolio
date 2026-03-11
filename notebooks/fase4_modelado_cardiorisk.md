# Fase 4: Modelado — CardioRisk Baseline (EXP001)

> **Ecosistema:** Hipócrates MCP | **Metodología:** CRISP-DM | **Fase:** 4 de 6  
> **Generado por:** [D] Deepseek | **Verificado por:** [C] Claude | **Commiteado por:** [G] GitHub MCP

---

## SECCIÓN 1: MÓDULO DIDÁCTICO — ¿Qué es la Fase 4 de CRISP-DM?

### 1. ¿Qué es la Fase 4 (Modeling) en CRISP-DM?

Imagina que has terminado de preparar el quirófano: los instrumentos están esterilizados, el paciente está monitorizado y los datos vitales están validados. La **Fase 4 de CRISP-DM (Modelado)** es exactamente el momento en que el cirujano (el algoritmo) entra en acción para realizar el procedimiento diagnóstico.

Aquí tomamos los datos preparados en las Fases 1-3 y entrenamos modelos de machine learning para encontrar patrones que predigan el riesgo cardiovascular. Es donde la teoría se convierte en un sistema de decisión operativo.

**Entradas:** Dataset limpio y preparado (Fase 3)  
**Salidas:** Modelos entrenados + métricas de evaluación  
**Siguiente fase:** Fase 5 — Evaluación (comparar modelos y decidir el mejor)

---

### 2. ¿Qué es un modelo de clasificación?

Es el **sistema de triage automatizado** de urgencias cardiológicas. Cuando llega un paciente con dolor torácico, el modelo analiza sus 13 signos vitales (features) y clasifica:

- **Clase 0** → Bajo riesgo (puede ir a observación)
- **Clase 1** → Alto riesgo (necesita evaluación cardiológica urgente)

Al igual que el triaje, no da un diagnóstico completo, pero **prioriza la atención basándose en probabilidades**.

---

### 3. ¿Por qué empezamos con Logistic Regression como baseline?

La Regresión Logística es el **monitor de signos vitales básico** de la unidad coronaria. Antes de solicitar pruebas complejas (TAC = Random Forest, resonancia = Red Neuronal), necesitamos:

1. Una línea base estable e interpretable
2. Saber qué variables tienen peso clínico significativo
3. Establecer el rendimiento mínimo que deben superar modelos más complejos

> Si un modelo complejo no supera el baseline → no justifica su complejidad.

---

### 4. ¿Qué es el train/test split y por qué importa?

Es el **simulacro de código azul antes de una emergencia real**.

| Conjunto | Tamaño | Función |
|----------|--------|---------|
| **Train (80%)** | ~242 pacientes | Enseñar al modelo con casos históricos |
| **Test (20%)** | ~61 pacientes | Evaluar con casos que el modelo nunca vio |

Si el modelo solo se evaluara con los datos con los que aprendió, sería como dejar que un residente se autoevaluara — no sabríamos cómo actúa ante casos reales nuevos.

**`stratify=y`** — crítico: garantiza que la proporción de enfermos/sanos sea igual en train y test.

---

### 5. ¿Qué es cross-validation?

Es **repetir el simulacro con distintos equipos y escenarios**.

En 5-fold CV dividimos el conjunto de entrenamiento en 5 partes iguales. En cada ronda, 4 partes entrenan y 1 evalúa:

```
Ronda 1: [TRAIN][TRAIN][TRAIN][TRAIN][TEST] → Recall: 0.87
Ronda 2: [TRAIN][TRAIN][TRAIN][TEST][TRAIN] → Recall: 0.83
Ronda 3: [TRAIN][TRAIN][TEST][TRAIN][TRAIN] → Recall: 0.89
Ronda 4: [TRAIN][TEST][TRAIN][TRAIN][TRAIN] → Recall: 0.85
Ronda 5: [TEST][TRAIN][TRAIN][TRAIN][TRAIN] → Recall: 0.86
                                         Media: 0.86 ± 0.02
```

Esto nos dice que el modelo **generaliza consistentemente**, no que tuvo suerte con un split favorable.

---

### 6. ¿Por qué Recall es más importante que Accuracy en cardiopatía?

Un paciente con IAM silente llega a urgencias. El modelo lo clasifica como "bajo riesgo" → se va a casa → muerte súbita 4 horas después. Eso es un **Falso Negativo (FN)** — el error más costoso en medicina cardiovascular.

| Métrica | Fórmula | Qué mide |
|---------|---------|----------|
| **Recall** | TP / (TP + FN) | ¿Cuántos enfermos reales detectamos? |
| Precision | TP / (TP + FP) | ¿Cuántas alarmas son verdaderas? |
| Accuracy | (TP+TN) / Total | ¿Cuántos acertamos en total? |

> **Umbral CardioRisk: Recall ≥ 0.85** — inaceptable por debajo de este valor.

---

### 7. ¿Qué es `class_weight='balanced'`?

En Cleveland: 164 sanos vs 139 enfermos. Sin este parámetro, el modelo aprende que "predecir siempre sano" le da ~54% de accuracy. `class_weight='balanced'` le asigna más peso a cada paciente enfermo durante el entrenamiento — como **bajar el umbral de alarma del monitor cardíaco**.

---

### 8. ¿Qué es una matriz de confusión?

Es el **parte de resultados del triaje**, desglosado en 4 categorías:

| Sigla | Nombre | Consecuencia clínica |
|-------|--------|---------------------|
| **TN** | Verdadero Negativo | Paciente sano → dado de alta ✅ |
| **FP** | Falso Positivo | Sano hospitalizado → coste económico ⚠️ |
| **FN** | Falso Negativo | Enfermo dado de alta → **riesgo de muerte** 🚨 |
| **TP** | Verdadero Positivo | Enfermo detectado → tratamiento oportuno ✅ |

---

### 9. ¿Qué es un pipeline de sklearn?

Es el **protocolo de atención estandarizado (PAE)** para el preprocesamiento + modelado. Previene **data leakage**: garantiza que el scaler solo aprende de train y aplica esos parámetros a test.

```python
Pipeline([
    ('scaler', StandardScaler()),        # Paso 1: Normalizar signos vitales
    ('classifier', LogisticRegression()) # Paso 2: Clasificar riesgo
])
```

---

## SECCIÓN 2: CÓDIGO — Fase 4 Modelado CardioRisk (EXP001 Baseline)

```python
# ============================================================================
# CELDA 0 — INSTALACIÓN Y CARGA DE LIBRERÍAS
# ============================================================================
import subprocess, sys

# Instalar kagglehub si no está disponible
try:
    import kagglehub
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "kagglehub"])
    import kagglehub

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_curve, auc, recall_score, precision_score, f1_score
)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
np.random.seed(42)

print("✅ Librerías cargadas. Python:", sys.version.split()[0])
```

```python
# ============================================================================
# CELDA 1 — CARGA DEL DATASET VÍA KAGGLEHUB
# ============================================================================
print("📥 Descargando dataset desde Kaggle...")
dataset_path = kagglehub.dataset_download("johnsmith88/heart-disease-dataset")
print(f"   Dataset descargado en: {dataset_path}")

# Buscar el archivo CSV descargado (el path varía por sistema)
csv_files = list(Path(dataset_path).rglob("*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No se encontraron archivos CSV en {dataset_path}")

csv_path = csv_files[0]
print(f"   Archivo encontrado: {csv_path}")

df = pd.read_csv(csv_path)
print(f"   Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
print(f"   Columnas: {list(df.columns)}")
```

```python
# ============================================================================
# CELDA 2 — LIMPIEZA Y PREPARACIÓN
# ============================================================================

# Manejo de valores faltantes representados como '?'
for col in ['ca', 'thal']:
    if col in df.columns and df[col].dtype == object:
        mask = df[col] == '?'
        if mask.any():
            print(f"   '{col}': {mask.sum()} valores '?' → imputando con mediana")
            df[col] = pd.to_numeric(df[col], errors='coerce')

for col in ['ca', 'thal']:
    if col in df.columns and df[col].isnull().any():
        median_val = df[col].median()
        df[col].fillna(median_val, inplace=True)

df['ca'] = df['ca'].astype(float)
df['thal'] = df['thal'].astype(float)

# Binarización del target (0 → 0, 1-4 → 1)
target_col = 'target' if 'target' in df.columns else 'num'
df['target_binary'] = df[target_col].apply(lambda x: 0 if x == 0 else 1)
dist = df['target_binary'].value_counts().sort_index()
print(f"Distribución binaria: {dict(dist)}")
print(f"Proporción enfermos : {dist[1]/len(df):.2%}")

# Features y target
feature_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

X = df[feature_cols].copy()
y = df['target_binary'].copy()

print(f"\n✅ X: {X.shape} | y: {y.shape}")
```

```python
# ============================================================================
# CELDA 3 — PIPELINE Y TRAIN/TEST SPLIT
# ============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"X_train: {X_train.shape} | X_test: {X_test.shape}")
print(f"Clase 1 en y_train: {y_train.mean():.2%} | y_test: {y_test.mean():.2%}")

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(
        class_weight='balanced', random_state=42,
        max_iter=1000, solver='liblinear'
    ))
])

print("✅ Pipeline creado: StandardScaler → LogisticRegression(balanced)")
```

```python
# ============================================================================
# CELDA 4 — ENTRENAMIENTO Y CROSS-VALIDATION
# ============================================================================
pipeline.fit(X_train, y_train)

cv_scores = cross_val_score(
    pipeline, X_train, y_train, cv=5, scoring='recall', n_jobs=-1
)

print(f"Recall CV 5-fold: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
print(f"Scores por fold : {np.round(cv_scores, 3)}")

y_pred = pipeline.predict(X_test)
y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
```

```python
# ============================================================================
# CELDA 5 — EVALUACIÓN COMPLETA
# ============================================================================
print("\n📊 EVALUACIÓN EN TEST SET")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=['No Enfermedad', 'Enfermedad']))

recall_test    = recall_score(y_test, y_pred, pos_label=1)
precision_test = precision_score(y_test, y_pred, pos_label=1)
f1_test        = f1_score(y_test, y_pred, pos_label=1)

print(f"Recall    : {recall_test:.3f}  {'✅ ≥0.85' if recall_test >= 0.85 else '❌ <0.85 OBJETIVO NO CUMPLIDO'}")
print(f"Precision : {precision_test:.3f}")
print(f"F1-Score  : {f1_test:.3f}")

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print(f"\nFN: {fn} enfermos dados de alta ⚠️ | FP: {fp} sanos hospitalizados")

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Pred: Sano', 'Pred: Enfermo'],
            yticklabels=['Real: Sano', 'Real: Enfermo'], ax=axes[0])
axes[0].set_title('Matriz de Confusión — EXP001', fontsize=13)

fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

axes[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.3f}')
axes[1].plot([0, 1], [0, 1], 'navy', lw=2, linestyle='--')
axes[1].set_xlabel('False Positive Rate')
axes[1].set_ylabel('Recall / Sensibilidad')
axes[1].set_title('Curva ROC — EXP001', fontsize=13)
axes[1].legend(loc='lower right')
axes[1].grid(True)

Path('./models').mkdir(exist_ok=True)
plt.tight_layout()
plt.savefig('./models/exp001_plots.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"ROC-AUC: {roc_auc:.3f}")
```

```python
# ============================================================================
# CELDA 6 — GUARDAR MODELO
# ============================================================================
joblib.dump(pipeline, './models/exp001_logistic_regression.pkl')
joblib.dump(list(X.columns), './models/exp001_feature_names.pkl')
print("✅ Modelo guardado en ./models/exp001_logistic_regression.pkl")
```

```python
# ============================================================================
# CELDA 7 — RESUMEN PARA EXPERIMENT_LOG.md
# ============================================================================
print(f"""
## EXP001: Logistic Regression Baseline

| Métrica | Valor | Objetivo |
|---------|-------|----------|
| Recall (Clase 1) | {recall_test:.3f} | {'✅' if recall_test >= 0.85 else '❌'} ≥0.85 |
| Precision (Clase 1) | {precision_test:.3f} | — |
| F1-Score (Clase 1) | {f1_test:.3f} | — |
| ROC-AUC | {roc_auc:.3f} | — |
| CV Recall 5-fold | {cv_scores.mean():.3f} ± {cv_scores.std():.3f} | — |

### Matriz de Confusión
| | Pred: 0 | Pred: 1 |
|---|---|---|
| Real: 0 | TN={tn} | FP={fp} |
| Real: 1 | FN={fn} ⚠️ | TP={tp} |

- Sensibilidad: {recall_test:.1%} — detecta {int(recall_test*100)} de cada 100 enfermos
- FN residuales: {fn} pacientes con enfermedad serían dados de alta
- Próximo paso: {'EXP002 Random Forest' if recall_test >= 0.85 else 'Ajustar threshold o SMOTE'}
""")
```
