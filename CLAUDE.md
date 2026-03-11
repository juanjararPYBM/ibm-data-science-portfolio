# Hipócrates MCP Ecosystem — Reglas de Orquestación

> Este archivo es leído automáticamente por Claude Code y por Claude Desktop (vía GitHub MCP) al inicio de cada sesión.
> Define cómo delegar trabajo entre agentes para maximizar eficiencia de tokens.

---

## Regla de Oro

**Claude Sonnet solo piensa. Los microservicios ejecutan.**

Antes de generar cualquier código, script o archivo de configuración, Claude debe evaluar si la tarea puede delegarse a Deepseek. Si puede delegarse, DEBE delegarse.

---

## Tabla de Delegación Obligatoria

| Tipo de tarea | Agente | Nunca usar Claude para esto |
|---------------|--------|-----------------------------|
| Generar código Python (sklearn, pandas, matplotlib) | `deepseek:deepseek_chat` | ✅ Delegar siempre |
| Scripts de PowerShell / bash / shell | `deepseek:deepseek_chat` | ✅ Delegar siempre |
| Boilerplate de notebooks Jupyter | `deepseek:deepseek_chat` | ✅ Delegar siempre |
| Debugging de errores de sintaxis | `deepseek:deepseek_chat` | ✅ Delegar siempre |
| Búsqueda de documentación / errores | `deepseek:web_search` | ✅ Delegar siempre |
| Visualizaciones médicas e imágenes | `nano-banana:generate_medical_image` | ✅ Delegar siempre |
| Gráficos de riesgo cardiovascular | `nano-banana:create_risk_chart` | ✅ Delegar siempre |
| Commits y actualizaciones al repo | `github:push_files` | ✅ Delegar siempre |
| Narración de hallazgos clínicos | `inworld-tts:generate_speech` | ✅ Delegar siempre |

## Tareas Exclusivas de Claude Sonnet

- Decisiones arquitecturales del modelo ML
- Interpretación clínica de métricas (Recall, AUC-ROC en contexto médico)
- Redacción del reporte CRISP-DM final
- Diseño de prompts para los agentes
- Razonamiento sobre trade-offs (Precision vs Recall en cardiopatía)
- Explicaciones didácticas para el aprendizaje de Juan

---

## Flujo de Trabajo para Fase 4 (Modelado)

```
1. Claude diseña la estrategia del modelo [C]
2. Deepseek genera el código sklearn [D]
3. Juan ejecuta el código
4. Si hay error → Deepseek debuggea [D]
5. Claude interpreta los resultados clínicamente [C]
6. Nano-banana visualiza las métricas [N]
7. GitHub MCP commitea el notebook [G]
8. Claude actualiza EXPERIMENT_LOG.md [C+G]
```

---

## Contexto del Proyecto

- **Proyecto:** CardioRisk — Sistema de clasificación de riesgo cardiovascular
- **Metodología:** CRISP-DM
- **Estado actual:** Fases 1-3 completas, iniciando Fase 4 (Modelado)
- **Stack:** Python, sklearn, pandas, GitHub Pages
- **Dataset:** Cleveland Heart Disease Dataset (UCI)
- **Métrica prioritaria:** Recall (minimizar falsos negativos en cardiopatía)
- **Alumno:** Juan — médico de urgencias en transición a data science
- **Plan Claude:** Pro ($20/mes) — tokens limitados, usar con criterio

---

## Hardware Disponible

- CPU: Ryzen 9 7950X3D
- RAM: 32GB
- GPU: RTX 4070 12GB VRAM
- OS: Windows 11
- Deepseek local: deepseek-coder-v2:16b-lite-instruct-q4_K_M (Ollama)

---

## Registro de Eficiencia

Cada sesión debe actualizarse en `EXPERIMENT_LOG.md` con:
- Tareas ejecutadas por cada agente
- Tokens Claude estimados consumidos
- Tokens estimados sin ecosistema
- Decisiones técnicas relevantes

*Versión: 1.0 | Actualizado: 2026-03-11*
