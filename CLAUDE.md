# 🏥 Hipócrates MCP Ecosystem — Reglas de Orquestación

> Este archivo es leído automáticamente por Claude Code y por Claude Desktop (vía GitHub MCP) al inicio de cada sesión.
> Define cómo delegar trabajo entre agentes para maximizar eficiencia de tokens sin comprometer calidad.
> **Archivos de soporte:** `TOKEN_MANAGEMENT.md` | `project_state.yaml` | `EXPERIMENT_LOG.md`

---

## ⚡ Regla de Oro

**Claude Sonnet solo piensa. Los microservicios ejecutan.**

Antes de generar cualquier código, script, documento o búsqueda, Claude evalúa si la tarea puede delegarse. Si puede delegarse, DEBE delegarse.

---

## 🚦 Inicio de Sesión

Al iniciar cada sesión, Claude DEBE:
1. Leer este archivo vía GitHub MCP para auto-contextualizarse
2. Leer `project_state.yaml` para conocer el estado actual del experimento
3. No pedir a Juan que explique el estado del proyecto ni el dataset
4. Confirmar qué agentes están disponibles antes de comenzar

---

## 📋 Tabla de Delegación

### ✅ Delegar SIEMPRE a Deepseek — sin revisión de Claude

| Tarea | Herramienta |
|-------|-------------|
| Código Python mecánico (sklearn pipelines, train/test split, métricas numéricas) | `deepseek:deepseek_chat` |
| Scripts PowerShell / bash / docker / configuración | `deepseek:deepseek_chat` |
| Formateo y limpieza de datos (pandas, valores nulos, encoding, outliers) | `deepseek:deepseek_chat` |
| Conversión de formatos (CSV, JSON, pickle, notebooks) | `deepseek:deepseek_chat` |
| **JSON completo de notebooks Jupyter** | `deepseek:deepseek_chat` |
| Docstrings y comentarios de código | `deepseek:deepseek_chat` |
| Grid search y cross-validation (solo el código, no la interpretación) | `deepseek:deepseek_chat` |
| Debugging errores sintácticos (SyntaxError, IndentationError, NameError, TypeError) | `deepseek:deepseek_chat` |
| Búsqueda de documentación, errores específicos, ejemplos de código | `deepseek:web_search` |
| Commits y actualizaciones al repositorio | `github:push_files` |
| Visualizaciones médicas e imágenes clínicas | `nano-banana:generate_medical_image` |
| Gráficos de riesgo cardiovascular | `nano-banana:create_risk_chart` |
| Narración de hallazgos clínicos (demos, presentaciones) | `inworld-tts:generate_speech` |

### ⚠️ Delegar a Deepseek CON revisión de Claude

| Tarea | Razón de revisión |
|-------|------------------|
| Ingeniería de features | Claude valida pertinencia clínica de cada feature |
| Selección de hiperparámetros | Claude aprueba que los rangos tienen lógica médica |
| Estructura del notebook | Claude revisa narrativa CRISP-DM |
| Documentación técnica (README, docstrings masivos) | Claude verifica precisión clínica del lenguaje |
| Debugging lógico ML (resultados inesperados sin error explícito) | Claude detecta data leakage o sesgos silenciosos |

### 🔴 Exclusivo de Claude Sonnet — nunca delegar

- Interpretación de métricas en contexto cardíaco (qué significa Recall 0.78 para un paciente real)
- Decisión de qué algoritmo usar y justificación clínica
- Redacción del reporte CRISP-DM final
- Diseño de prompts para los agentes
- Razonamiento sobre trade-offs Precision vs Recall en cardiopatía
- Cualquier conclusión que conecte datos con decisión clínica
- Explicaciones didácticas para el aprendizaje de Juan
- **Specs de notebooks** — Claude siempre escribe la spec; Deepseek siempre genera el JSON

---

## ✅ Checklist Pre-Ejecución — Verificación obligatoria de código Deepseek

Claude DEBE verificar este checklist en TODO código sklearn antes de que Juan lo ejecute:

- [ ] **Sin data leakage** — `.fit()` solo en train, `.transform()` separado en test
- [ ] **Métrica principal** — se optimiza Recall, no Accuracy
- [ ] **Split estratificado** — `train_test_split` usa `stratify=y`
- [ ] **Columnas válidas** — deben existir en FEATURES_FINALES (ver project_state.yaml §dataset.features_finales)
- [ ] **Persistencia** — modelo guardado con `joblib`
- [ ] **Reproducibilidad** — `random_state=42` en todo
- [ ] **Balance de clases** — SMOTE ya aplicado en train; no aplicar `class_weight='balanced'` doble
- [ ] **Carga de datos** — usar `kagglehub.dataset_download("jocelyndumlao/cardiovascular-disease-dataset")`
- [ ] **Dataset correcto** — el dataset es `jocelyndumlao/cardiovascular-disease-dataset` (1000 filas, sep=`,`). NUNCA usar `cardio_train.csv` (sep=`;`, 70k filas) ni fabricar columnas con `np.random`
- [ ] **Consistencia entre fases** — EWS umbrales en F6 coinciden con los definidos en F1 (EWS_BAJO=0.30, EWS_MEDIO=0.65)
- [ ] **Nombres de niveles** — usar "Bajo Riesgo / Riesgo Medio / Alto Riesgo" (no BAJO/MODERADO/ALTO)
- [ ] **KPIs completos** — verificar los 3 KPIs de F1: Recall>0.80, AUC-ROC>0.85, Error tipo II<5%
- [ ] **patientid excluido** — siempre en feature_cols: `c not in [TARGET, 'patientid']`

> Si algún punto falla → Deepseek corrige. Claude NO ejecuta correcciones de código.

---

## 💰 Economía de Tokens — Regla de Generación de Notebooks

> **Lección aprendida (2026-03-12):** Claude generó el JSON completo de 4 notebooks (~15k tokens de input) cuando ese trabajo debió delegarse íntegramente a Deepseek. El JSON de un notebook Jupyter es estructura repetitiva y mecánica — no requiere razonamiento de Claude.

### Regla fija para todos los proyectos:

| Quién | Qué hace | Por qué |
|-------|----------|---------|
| **Claude** | Escribe la SPEC del notebook en texto plano | Requiere razonamiento de dominio, coherencia entre fases, validación clínica |
| **Deepseek** | Genera el JSON `.ipynb` completo | Mecánico, verboso, no requiere razonamiento |
| **Claude** | Revisa el código generado (checklist) | Detecta errores lógicos como dataset incorrecto, data leakage silencioso |
| **GitHub MCP** | Commitea el JSON aprobado | Mecánico |

### Ahorro estimado por notebook:
- JSON Jupyter de un notebook completo: ~3,000–5,000 tokens de código Python real + ~10,000–12,000 tokens de andamiaje Jupyter (corchetes, metadata, `\n`, `execution_count`, etc.)
- **Delegando a Deepseek: ahorro de ~10–12k tokens de input por notebook**
- Para un proyecto con 4–6 notebooks: ahorro de **~50k tokens por sesión de generación**

### Spec mínima que Claude debe incluir al delegar:
1. CANON de preprocesamiento — bloque de código Python exacto (copy-paste)
2. Estructura de bloques — título, objetivo, qué hace cada bloque
3. Invariantes que no se pueden romper — dataset, features, random_state, etc.
4. Restricciones explícitas — qué NO hacer (ej: "nunca usar np.random para fabricar columnas", "nunca cardio_train.csv")
5. Estilo visual — colores, rcParams si aplica

> **Recordatorio:** la calidad no viene del JSON — viene de que la spec esté bien escrita. Una spec incompleta produce código incorrecto aunque Claude revise después. Invertir tiempo en la spec = ahorrar tiempo en debugging.

---

## 🔧 Protocolo de Escalación de Debugging

> Principio: el paramédico intenta estabilizar, si no escala al médico, si no al especialista.

| Nivel | Intentos | Acción | Condición |
|-------|----------|--------|-----------|
| **1** | 1–2 | Deepseek solo | Errores sintácticos, tipos, importaciones, stack traces obvios |
| **2** | 3–4 | Deepseek + supervisión Claude | Claude orienta la dirección del fix, Deepseek ejecuta |
| **3** | 5+ | Claude toma el control | Error persistente que requiere razonamiento arquitectural |
| **⚡ Especial** | Inmediato | Claude interviene sin escalar | Data leakage, métricas infladas, errores en lógica médica |

---

## 🚨 Protocolo de Fallo de Agente

> Surgido en sesión 2026-03-11: GitHub MCP no cargó tools en sesión activa.

1. Si una herramienta falla en el primer intento, Claude DEBE usar `tool_search` para recargarla
2. Claude NUNCA asume tareas delegables por fallo técnico
3. Si después de 2 reintentos el agente no responde → notificar a Juan con error exacto y esperar instrucciones
4. Aplica a TODOS los agentes: Deepseek, Nano-banana, Inworld TTS, GitHub MCP

---

## 📊 Protocolo de Gestión de Tokens

> Ver detalle completo en `TOKEN_MANAGEMENT.md`

**Reglas críticas:**
- Checkpoint obligatorio cada 4 ciclos (diseño→código→debug→commit)
- Si Claude lleva >3 respuestas seguidas → señal `[C]×3` → revisar si se puede delegar
- Contexto al 70% → aplicar template de resumen ejecutivo y abrir sesión nueva
- Actualizar `project_state.yaml` al cierre de cada sesión o checkpoint
- **Claude NUNCA genera JSON de notebooks directamente** — ver §Economía de Tokens

---

## 🔬 Protocolo de Investigación y Literatura

**Deepseek maneja todo el trabajo bruto:** búsqueda web, extracción PDFs, resúmenes técnicos, datasets.

**Claude interviene UNA SOLA VEZ al final** validando:
1. ¿La fuente es confiable?
2. ¿El dato tiene contexto clínico correcto?
3. ¿Hay contradicción entre fuentes?

---

## 🔄 Flujo de Trabajo — Regla Estricta de Delegación

> **Lección aprendida (2026-03-11):** Claude ejecutó directamente correcciones de código que debieron pasar por Deepseek.
> **Lección aprendida (2026-03-12):** Claude generó JSON de notebooks directamente (~15k tokens innecesarios). La spec debe ir a Deepseek; Deepseek produce el JSON; Claude revisa.

### ❌ Claude NO debe NUNCA:
- Generar código Python directamente en su respuesta
- **Generar JSON de notebooks Jupyter directamente** — siempre via Deepseek
- Commitear código que él mismo generó sin revisión de Deepseek
- Ejecutar correcciones de notebooks sin pasar por el flujo delegado
- Usar `github:create_or_update_file` con código generado por Claude mismo

### ✅ Flujo obligatorio para cualquier corrección de código o notebook:

```
1. [C]   Claude analiza el problema y redacta la SPEC exacta
         (qué cambiar, por qué, invariantes que no tocar, restricciones explícitas)
2. [D]   Deepseek genera el contenido completo según la spec
3. [C]   Claude revisa lo que generó Deepseek (checklist pre-ejecución)
4. [C]   Claude aprueba o pide corrección a Deepseek
5. [G]   GitHub MCP commitea el contenido aprobado
6. [👤]  Juan ejecuta/valida en Colab
```

### ✅ Flujo para análisis e incongruencias (como F1 vs F6):

```
1. [👤]  Juan detecta o Claude detecta una incongruencia
2. [C]   Claude analiza TODAS las fases afectadas y lista los cambios exactos
3. [C]   Claude escribe spec detallada para Deepseek
4. [D]   Deepseek genera el contenido corregido
5. [C]   Claude revisa consistencia clínica y técnica
6. [G]   GitHub MCP commitea
```

### Señal de alerta:
Si Claude empieza a escribir código Python en su respuesta → STOP. Debe reformular como spec para Deepseek.
Si Claude empieza a escribir JSON de notebook → STOP. Debe redactar spec y pasar a Deepseek.

---

## 📁 Contexto del Proyecto

| Campo | Valor |
|-------|-------|
| **Proyecto** | CardioRisk — Clasificación de riesgo cardiovascular |
| **Metodología** | CRISP-DM |
| **Estado** | Fases 1–6 completas ✓ \| Proyecto CardioRisk TERMINADO |
| **Stack** | Python, sklearn, pandas, Google Colab, GitHub Pages |
| **Dataset** | `jocelyndumlao/cardiovascular-disease-dataset` (KaggleHub) |
| **Métrica prioritaria** | Recall ≥ 0.85 — minimizar falsos negativos en cardiopatía |
| **Alumno** | Juan — médico de urgencias en transición a data science |
| **Plan Claude** | Pro ($20/mes) — tokens limitados, usar con criterio |

### Hardware
- CPU: Ryzen 9 7950X3D | RAM: 32GB | GPU: RTX 4070 12GB VRAM | OS: Windows 11
- Deepseek local: `deepseek-coder-v2:16b-lite-instruct-q4_K_M` (Ollama)

---

*Versión: 1.6 | Actualizado: 2026-03-12 | Ecosistema: Hipócrates MCP v1.0*
*Cambio v1.4: Dataset corregido a jocelyndumlao (1000 muestras, 14 features). Columnas reales extraídas de Fase2/Fase3. Checklist actualizado con carga via kagglehub y SMOTE.*
*Cambio v1.5: Reglas de flujo de trabajo reforzadas. Claude NO genera código ni contenido directamente. Sección §Flujo de Trabajo actualizada a Fases 1-6 completas.*
*Cambio v1.6: Regla de economía de tokens para notebooks. Claude NUNCA genera JSON de notebooks — escribe specs, Deepseek genera JSON. Ahorro estimado ~50k tokens por sesión de generación de notebooks. Checklist ampliado con validación de dataset correcto.*
