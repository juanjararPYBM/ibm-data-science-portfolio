# TOKEN_LOG.md - Ledger de Consumo de Tokens
**Sistema Token Analytics - Proyecto CardioRisk / Hipócrates MCP**

## Descripción
Este archivo sirve como ledger manual para registrar el consumo de tokens por tarea realizada en el ecosistema Hipócrates MCP. Permite monitorear la eficiencia del uso de agentes (Claude vs Deepseek) y calcular el ROI de la delegación.

## Convenciones
- **input_est**: Tokens de entrada estimados (prompt + contexto)
- **output_est**: Tokens de salida estimados (respuesta)
- **total_est**: input_est + output_est
- **delegable**: Sí/No - si la tarea podría haberse delegado a Deepseek
- **agente**: CLAUDE o DEEPSEEK
- **session_id**: Formato SES-XXX (ej: SES-001)

## Tabla de Tipos de Tarea
| Tipo | Descripción | Delegable |
|------|-------------|-----------|
| READ_FILE_LARGE | Leer archivos grandes (>100 líneas) | No |
| READ_GITHUB_FILE | Leer archivos desde GitHub MCP | No |
| GENERATE_CONTENT | Generar código/documentación | Sí |
| CODE_REVIEW | Revisar código existente | Sí |
| DESIGN_DECISION | Diseñar arquitectura/sistemas | Parcial |
| DATA_ANALYSIS | Análisis de datos/EDA | Sí |
| MODEL_TRAINING | Entrenar modelos ML | Sí |
| COMMIT_GITHUB | Hacer commit/push a GitHub | Sí |
| DELEGATE_DEEPSEEK | Delegar tarea a Deepseek | No |
| CONVERSATION | Respuestas conversacionales | No |

## Estimaciones por Tipo de Tarea
| Tipo | Rango Input | Rango Output | Delegable |
|------|-------------|--------------|----------|
| READ_FILE_LARGE | 500-10,000 | 0 | No |
| READ_GITHUB_FILE | 1,000-5,000 | 0 | No |
| GENERATE_CONTENT | 500-3,000 | 1,000-10,000 | Sí |
| CODE_REVIEW | 1,000-5,000 | 500-3,000 | Sí |
| DESIGN_DECISION | 1,000-4,000 | 1,000-5,000 | Parcial |
| DATA_ANALYSIS | 2,000-8,000 | 1,000-6,000 | Sí |
| MODEL_TRAINING | 3,000-15,000 | 500-3,000 | Sí |
| COMMIT_GITHUB | 500-2,000 | 0-500 | Sí |
| DELEGATE_DEEPSEEK | 200-1,000 | 100-500 | No |
| CONVERSATION | 100-2,000 | 100-3,000 | No |

---

## SESSION ACTIVA
| timestamp | session_id | tarea_descripcion | tipo | agente | input_est | output_est | total_est | delegable | notas |
|-----------|------------|-------------------|------|--------|-----------|------------|-----------|-----------|-------|
| | | | | | | | | | |

---

## HISTORIAL DE SESIONES

### Sesión: 2026-03-11 (SES-003)
**Total estimado:** ~32,000 tokens Claude  
**Tokens que podrían haberse delegado:** ~5,000 tokens  
**Ahorro potencial:** ~15% si se hubiera delegado el commit  
**Nota:** Primera sesión con sistema de monitoreo activo

| timestamp | session_id | tarea_descripcion | tipo | agente | input_est | output_est | total_est | delegable | notas |
|-----------|------------|-------------------|------|--------|-----------|------------|-----------|-----------|-------|
| 2026-03-11 09:15 | SES-003 | leer master_index.py (200 líneas) | READ_FILE_LARGE | CLAUDE | 1,200 | 0 | 1,200 | No | Extracción contexto dataset |
| 2026-03-11 09:22 | SES-003 | leer fase2_data_understanding.py (2198 líneas) | READ_FILE_LARGE | CLAUDE | 8,000 | 0 | 8,000 | No | Extracción columnas reales |
| 2026-03-11 09:35 | SES-003 | leer fase3_data_preparation.py (1279 líneas) | READ_FILE_LARGE | CLAUDE | 5,000 | 0 | 5,000 | No | Extracción pipeline F3 |
| 2026-03-11 09:42 | SES-003 | leer CLAUDE.md desde GitHub MCP | READ_GITHUB_FILE | CLAUDE | 2,500 | 0 | 2,500 | No | Pre-corrección |
| 2026-03-11 09:45 | SES-003 | leer project_state.yaml desde GitHub MCP | READ_GITHUB_FILE | CLAUDE | 2,000 | 0 | 2,000 | No | Pre-corrección |
| 2026-03-11 10:10 | SES-003 | generar CLAUDE.md v1.4 corregido | GENERATE_CONTENT | CLAUDE | 1,500 | 3,500 | 5,000 | Sí | Dataset corregido |
| 2026-03-11 10:25 | SES-003 | generar project_state.yaml v2 | GENERATE_CONTENT | CLAUDE | 1,200 | 2,800 | 4,000 | Sí | Dataset corregido |
| 2026-03-11 10:40 | SES-003 | push_files CLAUDE.md + project_state.yaml | COMMIT_GITHUB | CLAUDE | 1,000 | 500 | 1,500 | Sí | Deepseek commit desde esta regla |
| 2026-03-11 11:05 | SES-003 | diseño sistema Token Analytics | DESIGN_DECISION | CLAUDE | 1,200 | 800 | 2,000 | Parcial | Arquitectura híbrida C+D |
| 2026-03-11 11:15 | SES-003 | prompt a Deepseek análisis opciones monitoreo | DELEGATE_DEEPSEEK | CLAUDE | 100 | 300 | 400 | No | Delegación correcta |
| 2026-03-11 11:30 | SES-003 | prompt a Deepseek generar 3 archivos sistema | DELEGATE_DEEPSEEK | CLAUDE | 150 | 350 | 500 | No | Delegación correcta |
| 2026-03-11 09:00-12:00 | SES-003 | respuestas conversacionales sesión | CONVERSATION | CLAUDE | 1,500 | 1,500 | 3,000 | No | Interacción general |
| **TOTALES** | SES-003 | | | | **25,350** | **9,750** | **35,100** | | **~5,500 delegables** |

---

### CIERRE CONTABLE — SES-003
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | ~35,100 |
| Tokens efectivamente delegados | ~4,500 (Deepseek) |
| Tokens que debieron delegarse (commit) | ~1,500 |
| Ahorro real obtenido | ~11% |
| Ahorro potencial si se delega todo lo delegable | ~17% |
| Hora de cierre | Pendiente — primer cierre contable |

---

## REGLAS DE CIERRE CONTABLE

### Triggers de cierre
1. **Automático:** 12:00am COT diario via Windows Task Scheduler → daily_close.py → commitea TOKEN_LOG.md

### Formato del resumen de cierre
```
### CIERRE CONTABLE — SES-XXX — YYYY-MM-DD HH:MM
| Métrica | Valor |
|---------|-------|
| Total tokens Claude | X,XXX |
| Total tokens Deepseek (real) | X,XXX |
| Ahorro real % | XX% |
| Tareas delegadas correctamente | X |
| Tareas que debieron delegarse | X |
| Costo estimado Claude (USD) | $X.XX |
| Costo real Deepseek (USD) | $X.XX |
```
---

### CIERRE CONTABLE — SES-004 — 2026-03-11 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-11 00:00 COT |
---

### CIERRE CONTABLE — SES-005 — 2026-03-12 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-12 00:00 COT |
---

### CIERRE CONTABLE — SES-006 — 2026-03-13 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-13 00:00 COT |
---

### CIERRE CONTABLE — SES-007 — 2026-03-14 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-14 00:00 COT |
---

### CIERRE CONTABLE — SES-008 — 2026-03-15 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-15 00:00 COT |
---

### CIERRE CONTABLE — SES-009 — 2026-03-16 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-16 00:00 COT |
---

### CIERRE CONTABLE — SES-010 — 2026-03-17 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-17 00:00 COT |
---

### CIERRE CONTABLE — SES-011 — 2026-03-18 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-18 00:00 COT |
---

### CIERRE CONTABLE — SES-012 — 2026-03-19 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-19 00:00 COT |
---

### CIERRE CONTABLE — SES-013 — 2026-03-20 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-20 00:00 COT |
---

### CIERRE CONTABLE — SES-014 — 2026-03-21 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-21 00:00 COT |
---

### CIERRE CONTABLE — SES-015 — 2026-03-22 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-22 00:00 COT |
---

### CIERRE CONTABLE — SES-016 — 2026-03-23 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-23 00:00 COT |
---

### CIERRE CONTABLE — SES-017 — 2026-03-24 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-24 00:00 COT |
---

### CIERRE CONTABLE — SES-018 — 2026-03-25 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-25 00:00 COT |
---

### CIERRE CONTABLE — SES-019 — 2026-03-26 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-26 00:00 COT |
---

### CIERRE CONTABLE — SES-020 — 2026-03-27 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-27 00:00 COT |
---

### CIERRE CONTABLE — SES-021 — 2026-03-28 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-28 00:00 COT |
---

### CIERRE CONTABLE — SES-022 — 2026-03-29 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-29 00:00 COT |
---

### CIERRE CONTABLE — SES-023 — 2026-03-30 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-30 00:00 COT |
---

### CIERRE CONTABLE — SES-024 — 2026-03-31 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-03-31 00:00 COT |
---

### CIERRE CONTABLE — SES-025 — 2026-04-01 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-01 00:00 COT |
---

### CIERRE CONTABLE — SES-026 — 2026-04-02 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-02 00:00 COT |
---

### CIERRE CONTABLE — SES-027 — 2026-04-03 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-03 00:00 COT |
---

### CIERRE CONTABLE — SES-028 — 2026-04-04 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-04 00:00 COT |
---

### CIERRE CONTABLE — SES-029 — 2026-04-05 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-05 00:00 COT |
---

### CIERRE CONTABLE — SES-030 — 2026-04-06 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-06 00:00 COT |
---

### CIERRE CONTABLE — SES-031 — 2026-04-07 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-07 00:00 COT |
---

### CIERRE CONTABLE — SES-032 — 2026-04-08 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-08 00:00 COT |
---

### CIERRE CONTABLE — SES-033 — 2026-04-09 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-09 00:00 COT |
---

### CIERRE CONTABLE — SES-034 — 2026-04-10 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-10 00:00 COT |
---

### CIERRE CONTABLE — SES-035 — 2026-04-11 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-11 00:00 COT |
---

### CIERRE CONTABLE — SES-036 — 2026-04-12 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-12 00:00 COT |
---

### CIERRE CONTABLE — SES-037 — 2026-04-13 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-13 00:00 COT |
---

### CIERRE CONTABLE — SES-038 — 2026-04-14 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-14 00:00 COT |
---

### CIERRE CONTABLE — SES-039 — 2026-04-15 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-15 00:00 COT |
---

### CIERRE CONTABLE — SES-040 — 2026-04-17 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-17 00:00 COT |
---

### CIERRE CONTABLE — SES-041 — 2026-04-18 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-18 00:00 COT |
---

### CIERRE CONTABLE — SES-042 — 2026-04-19 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-19 00:00 COT |
---

### CIERRE CONTABLE — SES-043 — 2026-04-20 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-20 00:00 COT |
---

### CIERRE CONTABLE — SES-044 — 2026-04-21 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-21 00:00 COT |
---

### CIERRE CONTABLE — SES-045 — 2026-04-22 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-22 00:00 COT |
---

### CIERRE CONTABLE — SES-046 — 2026-04-23 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-23 00:00 COT |
---

### CIERRE CONTABLE — SES-047 — 2026-04-24 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-24 00:00 COT |
---

### CIERRE CONTABLE — SES-048 — 2026-04-25 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-25 00:00 COT |
---

### CIERRE CONTABLE — SES-049 — 2026-04-26 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-26 00:00 COT |
---

### CIERRE CONTABLE — SES-050 — 2026-04-27 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-27 00:00 COT |
---

### CIERRE CONTABLE — SES-051 — 2026-04-28 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-28 00:00 COT |
---

### CIERRE CONTABLE — SES-052 — 2026-04-29 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-29 00:00 COT |
---

### CIERRE CONTABLE — SES-053 — 2026-04-30 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-04-30 00:00 COT |
---

### CIERRE CONTABLE — SES-054 — 2026-05-01 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-01 00:00 COT |
---

### CIERRE CONTABLE — SES-055 — 2026-05-02 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-02 00:00 COT |
---

### CIERRE CONTABLE — SES-056 — 2026-05-03 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-03 00:00 COT |
---

### CIERRE CONTABLE — SES-057 — 2026-05-04 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-04 00:00 COT |
---

### CIERRE CONTABLE — SES-058 — 2026-05-05 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-05 00:00 COT |
---

### CIERRE CONTABLE — SES-059 — 2026-05-06 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-06 00:00 COT |
---

### CIERRE CONTABLE — SES-060 — 2026-05-07 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-07 00:00 COT |
---

### CIERRE CONTABLE — SES-061 — 2026-05-11 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-11 00:00 COT |
---

### CIERRE CONTABLE — SES-062 — 2026-05-12 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-12 00:00 COT |
---

### CIERRE CONTABLE — SES-063 — 2026-05-13 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-13 00:00 COT |
---

### CIERRE CONTABLE — SES-064 — 2026-05-14 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-14 00:00 COT |
---

### CIERRE CONTABLE — SES-065 — 2026-05-15 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-15 00:00 COT |
---

### CIERRE CONTABLE — SES-066 — 2026-05-16 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-16 00:00 COT |
---

### CIERRE CONTABLE — SES-067 — 2026-05-17 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-17 00:00 COT |
---

### CIERRE CONTABLE — SES-068 — 2026-05-18 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-18 00:00 COT |
---

### CIERRE CONTABLE — SES-069 — 2026-05-19 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-19 00:00 COT |
---

### CIERRE CONTABLE — SES-070 — 2026-05-20 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-20 00:00 COT |
---

### CIERRE CONTABLE — SES-071 — 2026-05-21 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-21 00:00 COT |
---

### CIERRE CONTABLE — SES-072 — 2026-05-22 00:00 COT
| Métrica | Valor |
|---------|-------|
| Total tokens Claude estimados | 0 |
| Total tokens Deepseek (real) | 0 |
| Costo real Deepseek (USD) | $0.00000 |
| Ahorro vs Claude (tokens) | 0 |
| Ahorro vs Claude (USD) | $0.00000 |
| Ahorro % | 0.0% |
| Tareas delegadas a Deepseek | 0 |
| Hora de cierre | 2026-05-22 00:00 COT |
