# Token Analytics — ROI del Ecosistema Hipócrates MCP

> **Meta-proyecto:** el ecosistema analiza su propio consumo para optimizarse.

## Descripción

**Token Analytics** es un proyecto de análisis de datos aplicado al monitoreo de eficiencia del ecosistema Hipócrates MCP. Mide el costo real de operar con múltiples agentes de IA (Claude Sonnet + Deepseek) y cuantifica el ROI de la delegación inteligente de tareas.

Este proyecto demuestra un principio clave: **un sistema de IA maduro debe ser capaz de monitorear y optimizar su propia operación con datos reales.**

---

## Fuentes de Datos

### 1. `TOKEN_LOG.md` — Ledger manual (Claude)
- **Tipo:** Markdown con tablas estructuradas
- **Actualización:** Manual por Claude al final de cada tarea
- **Campos:** timestamp, session_id, tarea, tipo, agente, input_est, output_est, total_est, delegable, notas
- **Limitación:** Estimaciones ±15-20% de margen de error
- **Ventaja:** Captura contexto cualitativo (delegable, notas)

### 2. `deepseek_log.csv` — Log automático (Deepseek)
- **Tipo:** CSV generado por `deepseek_wrapper.py`
- **Actualización:** Automática en cada llamada API
- **Campos:** timestamp, session_id, task_type, model, prompt_tokens, completion_tokens, total_tokens, cost_usd, claude_equiv_tokens, claude_equiv_cost_usd, savings_tokens, savings_usd, task_description
- **Precisión:** Tokens reales de la API (sin estimación)

---

## Preguntas de Negocio

### Q1. ¿Cuántos tokens ahorra delegar a Deepseek?
- Métrica: `savings_tokens = claude_equiv_tokens - total_tokens`
- Por sesión, por tipo de tarea, tendencia histórica

### Q2. ¿Qué tipo de tareas tienen mayor ROI de delegación?
- Ranking de `savings_usd / cost_usd` por `task_type`
- Resultado: matriz de decisión para delegación óptima

### Q3. ¿Cuál es el costo real por sesión?
- Costo Claude estimado (TOKEN_LOG) + Costo Deepseek real (CSV)
- Comparación: costo actual vs costo sin ecosistema

### Q4. ¿Cómo evoluciona la eficiencia con el tiempo?
- Serie temporal del % de ahorro por sesión
- Hipótesis: la eficiencia mejora a medida que se optimizan los protocolos

### Q5. ¿Cuál es el punto de equilibrio Claude vs Deepseek?
- Umbral de complejidad a partir del cual vale la pena usar Claude
- Modelo: regresión `costo ~ tokens + task_type + complexity_score`

---

## Stack Técnico

```
python 3.9+ | pandas | numpy | matplotlib | seaborn | scikit-learn | jupyter
```

---

## Metodología CRISP-DM

| Fase | Contenido |
|------|-----------|
| 1. Business Understanding | KPIs de eficiencia del ecosistema, stakeholders, objetivos de ahorro |
| 2. Data Understanding | EDA de TOKEN_LOG + deepseek_log.csv, calidad, consistencia |
| 3. Data Preparation | Unificación de fuentes, normalización task_type, feature engineering |
| 4. Modeling | Regresión costo, clustering patrones de uso, serie temporal |
| 5. Evaluation | Validación cruzada, A/B testing estrategias de delegación |
| 6. Deployment | Dashboard Streamlit/Plotly, alertas automáticas, integración repo |

---

## Estructura del Proyecto

```
token_analytics/
├── README.md                  # Este archivo
├── deepseek_wrapper.py        # Wrapper automático Deepseek
├── deepseek_log.csv           # Log generado automáticamente
├── session_counter.txt        # Contador de sesiones
├── notebooks/
│   ├── 01_eda_token_analytics.ipynb
│   ├── 02_modelado_costos.ipynb
│   └── 03_dashboard_roi.ipynb
TOKEN_LOG.md                   # Ledger manual Claude (raíz del repo)
```

---

## Cierre Contable Diario

Al final de cada sesión (trigger: "me voy a dormir" o hora fija):

1. Claude genera tabla de cierre en `TOKEN_LOG.md`
2. Deepseek commitea el log al repo
3. El CSV de Deepseek ya está actualizado en tiempo real

---

## Valor como Portfolio IBM

- **Caso real:** datos propios, problema concreto, impacto medible
- **Innovación:** sistema que se analiza a sí mismo (meta-análisis)
- **Recursividad:** el ecosistema trabaja para mejorarse
- **Reproducible:** cualquier equipo con agentes MCP puede replicarlo
- **ROI demostrable:** ahorro estimado inicial ~15-20% por sesión

---

*Proyecto iniciado: 2026-03-11 | Ecosistema: Hipócrates MCP v1.0 | CardioRisk CRISP-DM*
