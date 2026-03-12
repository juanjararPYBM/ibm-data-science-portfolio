# 🤖 AGENTS.md – Protocolo de Colaboración para Proyectos de Data Science

---

## 🏆 Regla de Oro

**Claude analiza, especifica y revisa — NUNCA genera código directamente.**
**Deepseek genera todo el código y contenido, incluyendo el JSON completo de notebooks Jupyter.**
**GitHub MCP commitea — Claude no usa `create_or_update_file` con código propio.**
**Juan ejecuta y valida en el entorno final (Colab, local, etc.).**
**Business Understanding define KPIs/umbrales/nomenclatura que deben propagarse EXACTAMENTE a todas las fases posteriores.**

**🔴 Señal de alerta:** si Claude empieza a escribir código Python o JSON de notebook → **STOP** → reformular como especificación.

---

## 📋 Tabla de Delegación de Agentes

| Agente | Rol Principal | Responsabilidades Clave |
|--------|---------------|-------------------------|
| **Claude Sonnet** | Arquitecto y revisor | Análisis de dominio, specs, revisión de código, razonamiento de negocio |
| **deepseek:deepseek_chat** | Generador de código | Notebooks (código + JSON), scripts, funciones, documentación técnica, correcciones |
| **deepseek:web_search** | Investigador | Literatura, documentación de librerías, benchmarks |
| **github MCP** | Control de versiones | Commits, gestión de ramas, actualización de repositorio |
| **nano-banana** | Visualizador especializado | Gráficos de dominio, dashboards |
| **inworld-tts** | Narrador | Narración de hallazgos para demos y presentaciones |

### [PERSONALIZAR POR PROYECTO] – Agentes Adicionales o Especializados

---

## 💰 Economía de Tokens — Regla de Notebooks

> **Lección aprendida (2026-03-12, proyecto CardioRisk):** Claude generó el JSON completo de 4 notebooks (~15k tokens de input innecesarios). Esta regla aplica a TODO proyecto futuro.

### La regla es simple:

| Quién | Qué hace |
|-------|----------|
| **Claude** | Escribe SPEC del notebook en texto plano (lógica, canon, invariantes, restricciones) |
| **Deepseek** | Genera el JSON `.ipynb` completo |
| **Claude** | Revisa el código generado con el checklist |
| **GitHub MCP** | Commitea |

### Por qué funciona sin comprometer calidad:
- El JSON de Jupyter es ~70% andamiaje repetitivo (`cell_type`, `metadata`, `\n`, corchetes)
- El código Python real dentro del JSON representa solo ~30% del total de tokens
- Deepseek puede generar ese andamiaje a costo casi cero
- La calidad depende de **la spec que escribe Claude**, no del JSON que genera Deepseek
- Claude sigue revisando el resultado con el checklist — el control de calidad no se pierde

### Spec mínima que Claude debe incluir al delegar un notebook:
1. CANON de preprocesamiento — bloque Python exacto (copy-paste)
2. Estructura de bloques — qué hace cada uno
3. Invariantes — lo que no puede cambiar bajo ninguna circunstancia
4. Restricciones explícitas — qué NO hacer (ej: qué dataset cargar, qué no fabricar)
5. Estilo visual — si aplica

**Ahorro estimado: ~10–12k tokens por notebook, ~50k tokens por sesión de generación de 4–6 notebooks.**

---

## ✅ Checklist Pre-Ejecución Genérico (ML)

- [ ] **Sin data leakage** — `.fit()` solo en train, transformaciones aprendidas de train aplicadas a val/test
- [ ] **Métrica principal** definida explícitamente en Business Understanding (no asumir Accuracy)
- [ ] **Split estratificado** cuando el problema requiera representación proporcional
- [ ] **Reproducibilidad** — `random_state` fijo en splits, modelos y operaciones estocásticas
- [ ] **Persistencia de artefactos** — modelos, encoders, scalers guardados con `joblib` o equivalente
- [ ] **Consistencia de nomenclatura** — variables, métricas y niveles alineados con Business Understanding
- [ ] **Variables de identificación excluidas** — IDs, nombres u otros identificadores removidos de features
- [ ] **KPIs de Fase 1 verificados** — umbrales y métricas de Business Understanding comprobados numéricamente en Evaluación
- [ ] **Dataset verificado** — confirmar nombre, separador, dimensiones y que NO se usan datos sintéticos ni datasets alternativos

> Si algún punto falla → Deepseek corrige. Claude NO ejecuta correcciones de código.

---

## 🔄 Flujo Estricto de Delegación

### Flujo Normal (corrección / generación de código o notebook)

```
1. [C]   Claude detecta problema y escribe SPEC exacta (sin código, sin JSON)
2. [D]   Deepseek genera el código/JSON según la spec
3. [C]   Claude revisa lógica, alineación con spec y dominio
4. [G]   GitHub MCP commitea si Claude aprueba
5. [👤]  Juan ejecuta y valida en el entorno final
```

### Flujo para Incongruencias entre Fases

```
1. [👤/C]  Se detecta discrepancia entre fases (ej: umbral F1 ≠ umbral F6)
2. [C]     Claude lista TODOS los cambios necesarios con invariantes
3. [C]     Claude escribe spec detallada para Deepseek
4. [D]     Deepseek genera el contenido corregido
5. [C]     Claude verifica consistencia con Business Understanding
6. [G]     GitHub MCP commitea
```

**Señal de alerta:** Si Claude empieza a escribir código Python o JSON de notebook → STOP. Reformular como spec.

---

## 🐛 Protocolo de Debugging

| Nivel | Intentos | Acción | Condición |
|-------|----------|--------|-----------|
| **1** | 1-2 | Deepseek solo | Errores sintácticos, tipos, importaciones |
| **2** | 3-4 | Deepseek + orientación Claude | Claude escribe spec del fix, Deepseek ejecuta |
| **3** | 5+ | Claude toma control arquitectural | Error persistente de diseño |
| **⚡ Especial** | Inmediato | Parada — Claude revisa | Data leakage, métricas infladas, error de dominio, **dataset incorrecto** |

---

## 🚨 Protocolo de Fallo de Agente

1. Si una herramienta falla en el primer intento → usar `tool_search` para recargarla
2. Claude NUNCA asume tareas delegables por fallo técnico
3. Si después de 2 reintentos el agente no responde → notificar a Juan con error exacto
4. Aplica a todos los agentes: Deepseek, nano-banana, inworld-tts, GitHub MCP

---

## 💎 Gestión de Tokens

- Prompts concisos y estructurados; specs en lugar de narrativa
- **Claude nunca genera JSON de notebooks — ver §Economía de Tokens**
- Dividir tareas grandes en subtareas para Deepseek
- Priorizar documentación en repositorio sobre explicaciones en chat
- Checkpoint cada 4 ciclos (diseño→código→debug→commit)
- Si Claude lleva >3 respuestas seguidas → revisar si se puede delegar

---

## [PERSONALIZAR POR PROYECTO]

### 📌 Datos del Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | *[Insertar nombre]* |
| **Objetivo de Negocio** | *[Descripción breve]* |
| **Metodología** | *[CRISP-DM / TDSP / otro]* |
| **Métrica Principal** | *[Recall / AUC-ROC / F1 / MAE / otro]* |
| **Umbral de Éxito (KPI)** | *[Ej: Recall > 0.80]* |
| **Variables de ID a Excluir** | *[Lista de columnas]* |
| **Entorno de Ejecución** | *[Colab / local / cloud]* |
| **Dataset** | *[Fuente + N muestras + N columnas + separador]* |
| **Artefactos a Persistir** | *[model.pkl, scaler.pkl, features.pkl, ...]* |

### 🔗 Archivos de soporte
- Business Understanding: *[link o archivo]*
- Diccionario de datos: *[link o archivo]*
- Estado del proyecto: `project_state.yaml`
- Log de experimentos: `EXPERIMENT_LOG.md`

---

*Plantilla base — generada en proyecto CardioRisk (2026-03-11).*
*Actualizada 2026-03-12: agregada regla de economía de tokens para notebooks, checklist ampliado con validación de dataset, señal de alerta extendida a JSON de notebooks.*
*Copiar a cada nuevo repositorio y completar sección [PERSONALIZAR POR PROYECTO].*
