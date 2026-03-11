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

**`stratify=y`** — crítico: garantiza que la proporción de enfermos/sanos sea igual en train y test. Sin esto, podría ocurrir que todos los enfermos caigan en train y el modelo nunca aprenda a detectarlos en test.

---

### 5. ¿Qué es cross-validation?

Es **repetir el simulacro con distintos equipos y escenarios**.

En 5-fold CV dividimos el conjunto de entrenamiento en 5 partes iguales. En cada ronda, 4 partes entrenan y 1 evalúa. Al final tenemos 5 mediciones de Recall:

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

**Costo clínico del Falso Negativo:**

Un paciente con IAM silente llega a urgencias. El modelo lo clasifica como "bajo riesgo" → se va a casa → muerte súbita 4 horas después.

Eso es un **Falso Negativo (FN)** — el error más costoso en medicina cardiovascular.

| Métrica | Fórmula | Qué mide |
|---------|---------|----------|
| **Recall** | TP / (TP + FN) | ¿Cuántos enfermos reales detectamos? |
| Precision | TP / (TP + FP) | ¿Cuántas alarmas son verdaderas? |
| Accuracy | (TP+TN) / Total | ¿Cuántos acertamos en total? |

> **Umbral CardioRisk: Recall ≥ 0.85** — inaceptable por debajo de este valor para cualquier modelo en producción.

---

### 7. ¿Qué es `class_weight='balanced'`?

En Cleveland: 164 sanos vs 139 enfermos — desbalance leve pero importante.

Sin este parámetro, el modelo aprende que "predecir siempre sano" le da ~54% de accuracy y decide ser perezoso. **`class_weight='balanced'`** le asigna más peso a cada paciente enfermo durante el entrenamiento:

```
Peso clase 0 (sano)    = n_total / (2 × n_clase_0) = 303 / (2 × 164) = 0.92
Peso clase 1 (enfermo) = n_total / (2 × n_clase_1) = 303 / (2 × 139) = 1.09
```

Analogía: **bajar el umbral de alarma del monitor cardíaco** para que un paciente borderline active la alarma aunque su patrón sea ligeramente atípico.

---

### 8. ¿Qué es una matriz de confusión?

Es el **parte de resultados del triaje**, desglosado en 4 categorías:

```
                  PREDICCIÓN DEL MODELO
                  Sano (0)    Enfermo (1)
       Sano (0) │   TN   │     FP    │
REALIDAD        │────────│───────────│
     Enfermo (1)│   FN   │     TP    │
```

| Sigla | Nombre | Consecuencia clínica |
|-------|--------|---------------------|
| **TN** | Verdadero Negativo | Paciente sano → dado de alta ✅ |
| **FP** | Falso Positivo | Sano hospitalizado → coste económico ⚠️ |
| **FN** | Falso Negativo | Enfermo dado de alta → **riesgo de muerte** 🚨 |
| **TP** | Verdadero Positivo | Enfermo detectado → tratamiento oportuno ✅ |

---

### 9. ¿Qué es un pipeline de sklearn?

Es el **protocolo de atención estandarizado (PAE)** para el preprocesamiento + modelado.

```python
Pipeline([
    ('scaler', StandardScaler()),        # Paso 1: Normalizar signos vitales
    ('classifier', LogisticRegression()) # Paso 2: Clasificar riesgo
])
```

**¿Por qué importa?** — Previene **data leakage**: si escaláramos los datos antes de hacer el split, los parámetros de escala estarían "contaminados" por el test set. El pipeline garantiza que el scaler solo aprende de train y aplica esos parámetros a test — exactamente igual que en producción real.

---

## SECCIÓN 2: CÓDIGO — Fase 4 Modelado CardioRisk (EXP001 Baseline)

```python
# ============================================================================
# CONFIGURACIÓN INICIAL Y LIBRERÍAS
# ============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import sys
from pathlib import Path

# Scikit-learn core
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    recall_score,
    precision_score,
    f1_score
)

# Configuración de estilos y semillas para reproducibilidad
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
np.random.seed(42)

print("✅ Librerías cargadas. Versión de Python:", sys.version.split()[0])
```

```python
# ============================================================================
# 1. CARGA Y PREPARACIÓN DEL DATASET CLEVELAND
# ============================================================================
def load_and_prepare_cleveland_data(filepath='heart.csv'):
    """
    Carga el dataset Cleveland Heart Disease.
    Realiza limpieza, imputación de valores faltantes y binarización del target.
    """
    print("📥 Cargando dataset Cleveland Heart Disease...")
    
    try:
        df = pd.read_csv(filepath)
        print(f"   Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    except FileNotFoundError:
        print(f"❌ Archivo '{filepath}' no encontrado.")
        print("   Descargando desde UCI original...")
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        column_names = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
        ]
        df = pd.read_csv(url, names=column_names)
        print(f"   Dataset descargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    
    # Manejo de valores faltantes representados como '?'
    print("🔍 Buscando valores faltantes ('?')...")
    for col in ['ca', 'thal']:
        if df[col].dtype == object:
            mask = df[col] == '?'
            if mask.any():
                print(f"   Columna '{col}': {mask.sum()} valores '?' encontrados.")
                df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Imputar con la mediana (robusta a outliers)
    for col in ['ca', 'thal']:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"   Columna '{col}': imputados con mediana={median_val:.1f}")
    
    df['ca'] = df['ca'].astype(float)
    df['thal'] = df['thal'].astype(float)
    
    # Binarización del target (0 → 0, 1-4 → 1)
    print("🎯 Binarizando variable target...")
    df['target_binary'] = df['target'].apply(lambda x: 0 if x == 0 else 1)
    binary_dist = df['target_binary'].value_counts().sort_index()
    print(f"   Distribución binaria: {dict(binary_dist)}")
    print(f"   Proporción enfermedad: {binary_dist[1] / len(df):.2%}")
    
    feature_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    
    X = df[feature_cols].copy()
    y = df['target_binary'].copy()
    
    print(f"\n✅ Preparación completada. X shape: {X.shape}\n")
    return X, y, df

X, y, df = load_and_prepare_cleveland_data('heart.csv')
```

```python
# ============================================================================
# 2. PIPELINE Y TRAIN/TEST SPLIT
# ============================================================================

# Split estratificado
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,       # ← CRÍTICO: mantiene balance de clases
    random_state=42
)

print(f"X_train: {X_train.shape} | X_test: {X_test.shape}")
print(f"Proporción clase 1 en y_train: {y_train.mean():.2%}")
print(f"Proporción clase 1 en y_test : {y_test.mean():.2%}")

# Pipeline: StandardScaler → Logistic Regression
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(
        class_weight='balanced',   # ← Ajuste por desbalance de clases
        random_state=42,
        max_iter=1000,
        solver='liblinear'
    ))
])

print("\n✅ Pipeline creado: StandardScaler → LogisticRegression(class_weight='balanced')")
```

```python
# ============================================================================
# 3. ENTRENAMIENTO Y VALIDACIÓN CRUZADA
# ============================================================================

pipeline.fit(X_train, y_train)

# 5-fold CV (métrica: recall)
cv_scores = cross_val_score(
    pipeline, X_train, y_train,
    cv=5, scoring='recall', n_jobs=-1
)

print(f"Recall CV 5-fold: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
print(f"Scores por fold : {np.round(cv_scores, 3)}")

y_pred = pipeline.predict(X_test)
y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
```

```python
# ============================================================================
# 4. EVALUACIÓN COMPLETA
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

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print(f"\nFalsos Negativos (FN): {fn} → pacientes enfermos dados de alta ⚠️")
print(f"Falsos Positivos (FP): {fp} → sanos hospitalizados innecesariamente")

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Pred: Sano', 'Pred: Enfermo'],
            yticklabels=['Real: Sano', 'Real: Enfermo'],
            ax=axes[0])
axes[0].set_title('Matriz de Confusión — CardioRisk EXP001', fontsize=13)
axes[0].set_ylabel('Valor Real')
axes[0].set_xlabel('Predicción del Modelo')

fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

axes[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.3f}')
axes[1].plot([0, 1], [0, 1], 'navy', lw=2, linestyle='--', label='Random')
axes[1].set_xlabel('False Positive Rate (1 - Especificidad)')
axes[1].set_ylabel('True Positive Rate (Recall)')
axes[1].set_title('Curva ROC — CardioRisk EXP001', fontsize=13)
axes[1].legend(loc='lower right')
axes[1].grid(True)

plt.tight_layout()
plt.savefig('./models/exp001_evaluation_plots.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"\nROC-AUC: {roc_auc:.3f}")
```

```python
# ============================================================================
# 5. GUARDAR MODELO
# ============================================================================
Path('./models').mkdir(exist_ok=True)

joblib.dump(pipeline, './models/exp001_logistic_regression.pkl')
joblib.dump(list(X.columns), './models/exp001_feature_names.pkl')

print("✅ Modelo guardado en ./models/exp001_logistic_regression.pkl")
```

```python
# ============================================================================
# 6. RESUMEN PARA EXPERIMENT_LOG.md
# ============================================================================
print(f"""
## EXP001: Logistic Regression Baseline

| Métrica | Valor | Objetivo |
|---------|-------|----------|
| Recall (Clase 1) | {recall_test:.3f} | {'✅' if recall_test >= 0.85 else '❌'} ≥0.85 |
| Precision (Clase 1) | {precision_test:.3f} | — |
| F1-Score (Clase 1) | {f1_test:.3f} | — |
| ROC-AUC | {roc_auc:.3f} | — |
| CV Recall (5-fold) | {cv_scores.mean():.3f} ± {cv_scores.std():.3f} | — |

### Matriz de Confusión (Test)
| | Pred: 0 | Pred: 1 |
|---|---|---|
| Real: 0 | TN={tn} | FP={fp} |
| Real: 1 | FN={fn} ⚠️ | TP={tp} |

### Interpretación clínica
- Sensibilidad del {recall_test:.1%}: de cada 100 enfermos, detecta {int(recall_test*100)}
- Falsos negativos: {fn} pacientes con enfermedad serían dados de alta
- Próximo paso: {'EXP002 Random Forest' if recall_test >= 0.85 else 'Ajustar threshold o aplicar SMOTE'}
""")
```

```python
# ============================================================================
# 7. FUNCIÓN DE INFERENCIA (PRODUCCIÓN-READY)
# ============================================================================
def predict_cardiorisk(patient_features, model_path='./models/exp001_logistic_regression.pkl'):
    """
    Inferencia para un paciente individual.
    patient_features: dict con las 13 features clínicas.
    """
    pipeline = joblib.load(model_path)
    feature_names = joblib.load('./models/exp001_feature_names.pkl')
    patient_df = pd.DataFrame([patient_features], columns=feature_names)
    pred = pipeline.predict(patient_df)[0]
    proba = pipeline.predict_proba(patient_df)[0][1]
    
    return {
        'prediction': int(pred),
        'probability': round(float(proba), 4),
        'risk_level': 'ALTO RIESGO' if pred == 1 else 'BAJO RIESGO'
    }

# Ejemplo: paciente masculino, 55 años, angina, depresión ST
example_patient = {
    'age': 55, 'sex': 1, 'cp': 3, 'trestbps': 130, 'chol': 250,
    'fbs': 0, 'restecg': 0, 'thalach': 150, 'exang': 1,
    'oldpeak': 2.3, 'slope': 2, 'ca': 1.0, 'thal': 3.0
}

result = predict_cardiorisk(example_patient)
print(f"Paciente: {example_patient['age']}a, sexo {'M' if example_patient['sex']==1 else 'F'}")
print(f"Resultado: {result['risk_level']} (P={result['probability']:.1%})")
```
