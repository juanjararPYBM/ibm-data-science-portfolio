# 🏥 Hipócrates MCP Ecosystem — Reglas de Orquestación

> Este archivo es leído automáticamente por Claude Code y por Claude Desktop (vía GitHub MCP) al inicio de cada sesión.
> Define cómo se reparte el trabajo para maximizar eficiencia de tokens sin comprometer calidad.
> **Archivos de soporte:** `TOKEN_MANAGEMENT.md` | `project_state.yaml` | `EXPERIMENT_LOG.md`

---

## ⚡ Regla de Oro

**Claude piensa y ejecuta. La disciplina es de concisión, no de delegación.**

Ya no hay un modelo secundario que reciba el trabajo mecánico. Claude genera el código, lo revisa contra el checklist y lo commitea. Por lo tanto el control de tokens se traslada a **cómo** se escribe el código:

- Edición quirúrgica sobre reescritura completa — usar `Edit` sobre celdas puntuales, nunca regenerar un notebook entero por un cambio de tres líneas
- No imprimir código en la respuesta de chat si ya va a escribirse en un archivo
- No re-leer archivos recién editados para "verificar" — la herramienta ya falla si la edición no aplicó

---

## 🚦 Inicio de Sesión

Al iniciar cada sesión, Claude DEBE:
1. Leer este archivo para auto-contextualizarse
2. Leer `project_state.yaml` para conocer el estado actual del experimento
3. No pedir a Juan que explique el estado del proyecto ni el dataset
4. Verificar qué herramientas están realmente cargadas antes de prometer una capacidad

---

## 🤖 Agentes y Herramientas

### Verificados disponibles

| Herramienta | Uso |
|-------------|-----|
| `github:*` | Commits, PRs, lectura de repos, GitHub Actions |
| `WebSearch` | Búsqueda web indexada (server-side, siempre funciona) |
| `Bash` / `Read` / `Edit` / `Write` | Ejecución y edición local en el contenedor |
| `Magnific:images_*` | Generación de imágenes y visualizaciones |
| `PubMed:*` | Literatura médica — búsqueda, metadata, texto completo |
| `HappyScribe:*` | Transcripción de audio/video |

### Pendientes de verificación por sesión

`nano-banana` e `inworld-tts` aparecían en versiones previas de este archivo pero **no se han visto cargados en sesiones recientes**. Antes de planear trabajo que dependa de ellos, confirmar con `ToolSearch`. Para generación de imágenes, `Magnific` cubre la necesidad.

`Gmail` requiere autorización OAuth desde los ajustes de conectores de claude.ai.

---

## 📋 Tabla de Responsabilidades

### 🟢 Ejecución directa — Claude escribe y commitea sin ceremonia

| Tarea |
|-------|
| Código Python mecánico (sklearn pipelines, train/test split, métricas numéricas) |
| Scripts PowerShell / bash / docker / configuración |
| Formateo y limpieza de datos (pandas, valores nulos, encoding, outliers) |
| Conversión de formatos (CSV, JSON, pickle, notebooks) |
| Docstrings y comentarios de código |
| Grid search y cross-validation |
| Debugging de errores sintácticos |
| Commits y actualizaciones al repositorio |

### 🟡 Ejecución con checklist obligatorio antes de entregar

| Tarea | Qué se verifica |
|-------|-----------------|
| Ingeniería de features | Pertinencia clínica de cada feature |
| Selección de hiperparámetros | Que los rangos tengan lógica médica |
| Estructura del notebook | Narrativa CRISP-DM coherente |
| Documentación técnica | Precisión clínica del lenguaje |
| Debugging lógico ML | Data leakage o sesgos silenciosos |

### 🔴 Razonamiento que nunca se automatiza ni se apura

- Interpretación de métricas en contexto cardíaco (qué significa Recall 0.78 para un paciente real)
- Decisión de qué algoritmo usar y su justificación clínica
- Redacción del reporte CRISP-DM final
- Razonamiento sobre trade-offs Precision vs Recall en cardiopatía
- Cualquier conclusión que conecte datos con decisión clínica
- Explicaciones didácticas para el aprendizaje de Juan

---

## ✅ Checklist Pre-Ejecución — Verificación obligatoria de todo código sklearn

Claude DEBE verificar este checklist antes de que Juan ejecute cualquier código:

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

> Este checklist es la red de seguridad principal. Con un solo modelo generando y revisando, **el sesgo del autor-revisor es real**: Claude debe recorrer la lista explícitamente, punto por punto, no declararla aprobada de memoria.

---

## 💰 Economía de Tokens

> **Lección aprendida (2026-03-12):** regenerar el JSON completo de 4 notebooks costó ~15k tokens innecesarios. El andamiaje de un `.ipynb` (corchetes, metadata, `\n`, `execution_count`) es puro relleno.
> **Lección aprendida (2026-08-07):** al desaparecer el modelo secundario, la regla ya no es "delegar" sino "no reescribir".

### Reglas fijas

| Situación | Qué hacer |
|-----------|-----------|
| Cambio puntual en un notebook | `Edit` sobre la celda específica — nunca `Write` del archivo completo |
| Notebook nuevo desde cero | Escribir el `.ipynb` una sola vez, bien, con el checklist ya aplicado |
| Corrección tras error de ejecución | Editar solo la celda que falló |
| Código que va a un archivo | No duplicarlo en la respuesta de chat |
| Verificar que una edición aplicó | No re-leer el archivo — la herramienta ya habría fallado |

### Antes de escribir un notebook, tener resuelto:
1. CANON de preprocesamiento — bloque de código exacto
2. Estructura de bloques — título, objetivo, qué hace cada bloque
3. Invariantes — dataset, features, `random_state`
4. Restricciones explícitas — nunca `np.random` para fabricar columnas, nunca `cardio_train.csv`
5. Estilo visual — colores, `rcParams` si aplica

> Pensar la estructura antes de escribir sigue siendo la mejor inversión: un notebook mal planteado se paga en ciclos de debugging, que cuestan más que el archivo original.

---

## 🔧 Protocolo de Escalación de Debugging

> Principio: el paramédico intenta estabilizar, si no escala al médico, si no al especialista.

| Nivel | Intentos | Acción |
|-------|----------|--------|
| **1** | 1–2 | Fix directo — errores sintácticos, tipos, importaciones, stack traces obvios |
| **2** | 3–4 | Releer el contexto completo del bloque antes de tocar nada |
| **3** | 5+ | Parar. Replantear la arquitectura del bloque en vez de parchar |
| **⚡ Especial** | Inmediato | Data leakage, métricas infladas o errores de lógica médica — se atienden antes que cualquier otra cosa, sin agotar intentos |

> Si un error persiste más de 4 intentos, el problema casi nunca es la línea que falla — es una suposición equivocada más arriba.

---

## 🚨 Protocolo de Fallo de Herramienta

> Surgido en sesión 2026-03-11: GitHub MCP no cargó tools en sesión activa.

1. Si una herramienta falla en el primer intento, Claude DEBE usar `ToolSearch` para recargarla
2. Si tras 2 reintentos no responde → notificar a Juan con el error exacto y esperar instrucciones
3. Claude NUNCA reporta una capacidad como disponible sin haberla verificado
4. Claude NUNCA reporta una capacidad como imposible sin haber intentado recargarla

---

## 🌐 Entorno de Ejecución — Límites de red

> **Descubierto en sesión 2026-08-07.** Aplica a Claude Code on the web / entornos remotos.

El contenedor remoto tiene **egress restringido por política de red**. Verificado por sondeo:

| Destino | Estado |
|---------|--------|
| `api.anthropic.com`, `github.com`, `registry.npmjs.org`, `pypi.org` | ✅ Alcanzable |
| Cualquier otro dominio (incluido `example.com`) | ❌ `EGRESS_BLOCKED` |

**Consecuencias prácticas:**
- `WebFetch` falla contra sitios externos. `WebSearch` sí funciona (corre server-side).
- Chromium y Playwright **están instalados** (`/opt/pw-browsers/chromium`) pero no pueden navegar fuera del allowlist.
- Instalar un MCP de navegador local no lo resuelve: correría dentro del mismo contenedor.

**Vía de escape cuando se necesita internet abierto:** GitHub Actions. Los runners tienen egress libre. El patrón es: Claude pushea el workflow → el runner ejecuta y commitea resultados → Claude los lee vía GitHub MCP. Ningún paso toca el proxy bloqueado.

**Limitación de ese patrón:** los runners usan IPs de datacenter de Azure, que los antibot comerciales filtran. Funciona bien contra sitios `.gov.co` y APIs abiertas; mal contra portales con Cloudflare/DataDome.

---

## 🔬 Protocolo de Investigación y Literatura

`WebSearch` y `PubMed` para el trabajo de campo. Claude valida al cerrar:
1. ¿La fuente es confiable?
2. ¿El dato tiene contexto clínico correcto?
3. ¿Hay contradicción entre fuentes?

> Con `WebFetch` bloqueado en entorno remoto, `WebSearch` y `PubMed` son las únicas vías de investigación. Si una búsqueda exige leer páginas completas, decirlo explícitamente en vez de entregar un resultado incompleto sin avisar.

---

## 🔄 Flujo de Trabajo

### Para cualquier cambio de código o notebook:

```
1. [C]   Claude analiza el problema y define el cambio exacto
         (qué cambiar, por qué, invariantes que no tocar)
2. [C]   Claude escribe el código
3. [C]   Claude recorre el checklist pre-ejecución punto por punto
4. [G]   GitHub MCP commitea
5. [👤]  Juan ejecuta/valida en Colab
```

### Para análisis e incongruencias entre fases (como F1 vs F6):

```
1. [👤/C] Se detecta la incongruencia
2. [C]    Claude analiza TODAS las fases afectadas y lista los cambios exactos
3. [C]    Claude aplica los cambios con edición quirúrgica
4. [C]    Claude verifica consistencia clínica y técnica cruzada entre fases
5. [G]    GitHub MCP commitea
```

### Señales de alerta:
- Si Claude va a reescribir un archivo completo por un cambio menor → STOP, usar `Edit`
- Si Claude declara el checklist aprobado sin recorrerlo → STOP, recorrerlo explícitamente
- Si Claude promete una capacidad sin verificar la herramienta → STOP, verificar primero

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

---

*Versión: 2.0 | Actualizado: 2026-08-07 | Ecosistema: Hipócrates MCP v2.0*
*Cambio v1.4: Dataset corregido a jocelyndumlao (1000 muestras, 14 features).*
*Cambio v1.5: Reglas de flujo de trabajo reforzadas.*
*Cambio v1.6: Regla de economía de tokens para notebooks.*
*Cambio v2.0: **Deepseek eliminado del ecosistema.** Claude asume generación y revisión de código. La economía de tokens pasa de "delegar" a "editar en vez de reescribir". Checklist reforzado por riesgo de sesgo autor-revisor. Nueva sección §Entorno de Ejecución con los límites de red descubiertos y el patrón GitHub Actions como vía de escape. Tabla de agentes ajustada a lo verificable.*
