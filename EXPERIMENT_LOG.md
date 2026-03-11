# 📊 Experiment Log — CardioRisk + Hipócrates MCP Ecosystem

> **Propósito:** Registrar cada sesión de trabajo del proyecto CardioRisk, documentando qué agente ejecutó cada tarea, tokens de Claude consumidos, y comparativa contra un flujo tradicional sin ecosistema MCP.
>
> Este log es un caso de estudio en eficiencia de tokens para la comunidad de data science.

---

## 🏗️ Arquitectura del Ecosistema

| Agente | Rol | Costo Claude |
|--------|-----|--------------|
| **Claude Sonnet** | Razonamiento clínico, decisiones arquitecturales, interpretación de resultados | Tokens Pro |
| **Deepseek** (local) | Generación de código, boilerplate sklearn, iteración de errores | 0 tokens Claude |
| **Nano-banana** (Gemini 2.5 Flash) | Visualizaciones médicas, gráficos clínicos | 0 tokens Claude |
| **Inworld TTS** | Narración de hallazgos clínicos | 0 tokens Claude |
| **GitHub MCP** | Commits, versionado, documentación | 0 tokens Claude |
| **Deepseek Web Search** | Documentación, papers, solución de errores | 0 tokens Claude |

---

## 📏 Metodología de Medición

### Estimación de tokens Claude
- **Real:** Tokens visibles en el uso del plan Pro (reseteo semanal)
- **Estimado sin ecosistema:** Basado en el número de intercambios que hubiesen requerido Claude si no hubiera delegación

### Categorías de tareas
- `[C]` Claude Sonnet — razonamiento, diseño, interpretación
- `[D]` Deepseek — código, debugging, boilerplate
- `[N]` Nano-banana — visualizaciones
- `[T]` Inworld TTS — narración
- `[G]` GitHub MCP — commits y documentación
- `[W]` Web Search — investigación

---

## 📅 Sesiones

---

### Sesión 001 — 2026-03-11
**Fase CRISP-DM:** Infraestructura / Pre-fase 4
**Duración estimada:** ~6 horas

#### Tareas ejecutadas

| # | Tarea | Agente | Tokens Claude estimados | Tokens sin ecosistema |
|---|-------|--------|------------------------|-----------------------|
| 1 | Debugging MCP protocol version (0.1.0 → 2025-11-25) | `[C]` | ~2,000 | ~2,000 |
| 2 | Fix BOM en nginx.conf (WriteAllText sin BOM) | `[C]` | ~1,500 | ~1,500 |
| 3 | Fix stdout Windows Store Python | `[C]` | ~1,000 | ~1,000 |
| 4 | Reescritura http_server.py nano-banana (gRPC → REST) | `[C]` | ~2,500 | ~2,500 |
| 5 | Corrección modelo Gemini (gemini-2.0-flash-exp → gemini-2.5-flash-image) | `[C]+[W]` | ~800 | ~3,000 |
| 6 | Integración GitHub OAuth | `[C]+[G]` | ~500 | ~500 |
| 7 | Creación EXPERIMENT_LOG.md | `[C]+[G]` | ~1,000 | ~1,000 |

**Total tokens Claude esta sesión:** ~9,300
**Total estimado sin ecosistema:** ~11,500
**Ahorro esta sesión:** ~19%

> **Nota:** El ahorro es bajo en esta sesión porque era principalmente debugging de infraestructura — trabajo que requiere razonamiento de Claude. El ahorro real se verá en las fases de modelado donde Deepseek genera código repetitivo.

#### Decisiones técnicas tomadas
- Deepseek web_search reemplaza open-websearch (más estable)
- Gemini 2.5 Flash Image es el modelo correcto para generación de imágenes médicas
- GitHub OAuth oficial > MCP local con token (más robusto)
- IPs fijas en nginx son técnicamente correctas pero frágiles — pendiente migrar a nombres DNS del compose

#### Pendientes técnicos
- [ ] Migrar nginx a nombres de servicio Docker DNS (nano-banana, inworld-tts) en vez de IPs fijas
- [ ] Verificar deepseek tool-calling compatibility con tareas de ML
- [ ] Primera prueba real de delegación: Deepseek genera código de Fase 4

---

## 📈 Resumen Acumulado

| Métrica | Valor |
|---------|-------|
| Sesiones registradas | 1 |
| Tokens Claude totales (estimado) | ~9,300 |
| Tokens sin ecosistema (estimado) | ~11,500 |
| Ahorro acumulado | ~19% |
| Fases CRISP-DM completadas | 1-3 (pre-ecosistema) |
| Fases CRISP-DM en progreso | 4 |

---

## 🔬 Hipótesis a validar

1. **H1:** El ecosistema reduce el consumo de tokens de Claude en >50% para tareas de generación de código ML repetitivo
2. **H2:** La calidad del código generado por Deepseek para sklearn es suficiente sin revisión extensiva de Claude
3. **H3:** Las visualizaciones de Nano-banana son superiores a matplotlib básico para presentación de resultados clínicos

---

*Log iniciado: 2026-03-11 | Proyecto: CardioRisk | Ecosistema: Hipócrates MCP v1.0*
