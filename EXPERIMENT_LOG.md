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

| # | Tarea | Agente | Tokens Claude | Tokens sin ecosistema |
|---|-------|--------|---------------|-----------------------|
| 1 | Debugging MCP protocol version (0.1.0 → 2025-11-25) | `[C]` | ~2,000 | ~2,000 |
| 2 | Fix BOM en nginx.conf | `[C]` | ~1,500 | ~1,500 |
| 3 | Fix stdout Windows Store Python | `[C]` | ~1,000 | ~1,000 |
| 4 | Reescritura http_server.py nano-banana (gRPC → REST) | `[C]` | ~2,500 | ~2,500 |
| 5 | Corrección modelo Gemini (gemini-2.0-flash-exp → gemini-2.5-flash-image) | `[C]+[W]` | ~800 | ~3,000 |
| 6 | Integración GitHub OAuth | `[C]+[G]` | ~500 | ~500 |
| 7 | Scripts PowerShell de configuración (docker, nginx, config.json) | `[C]` | ~3,000 | ~3,000 |
| 8 | Creación EXPERIMENT_LOG.md + CLAUDE.md | `[C]+[G]` | ~1,500 | ~1,500 |

**Total tokens Claude esta sesión:** ~12,800  
**Total estimado sin ecosistema:** ~15,000  
**Ahorro esta sesión:** ~15%

> **Nota importante:** El ahorro en esta sesión fue mínimo porque fue 100% debugging de infraestructura — trabajo que requiere razonamiento de Claude. **Deepseek no fue usado en esta sesión** ya que aún no estaba el flujo de delegación definido. El ahorro real (proyectado >50%) comenzará en Fase 4 donde Deepseek generará todo el código sklearn.

#### Decisiones técnicas tomadas
- Deepseek web_search reemplaza open-websearch (más estable, sin API key)
- Gemini 2.5 Flash Image es el modelo correcto para generación de imágenes médicas
- GitHub OAuth oficial > MCP local con token (más robusto)
- IPs fijas en nginx son frágiles al recrear contenedores — pendiente DNS
- CLAUDE.md creado para que la delegación sea automática desde sesión 002

#### Pendientes técnicos
- [ ] Migrar nginx a nombres de servicio Docker DNS
- [ ] Primera prueba real de delegación: Deepseek genera código Fase 4
- [ ] Verificar deepseek tool-calling con tareas sklearn

---

### Sesión 002 — 2026-03-11
**Fase CRISP-DM:** Infraestructura / Pre-fase 4 (continuación)  
**Duración estimada:** ~1 hora

#### Tareas ejecutadas

| # | Tarea | Agente | Tokens Claude | Tokens sin ecosistema |
|---|-------|--------|---------------|-----------------------|
| 1 | Commit CLAUDE.md v1.2 vía GitHub MCP | `[G]` | ~800 | ~800 |
| 2 | Debugging GitHub MCP no cargaba tools (tool_search x2) | `[C]` | ~600 | ~600 |
| 3 | Reinicio Claude Desktop para recargar servidores MCP | `[👤]` | 0 | 0 |
| 4 | Actualización EXPERIMENT_LOG.md sesión 002 | `[G]` | ~400 | ~400 |

**Total tokens Claude esta sesión:** ~1,800  
**Total estimado sin ecosistema:** ~1,800  
**Ahorro esta sesión:** ~0% (tarea administrativa, no delegable)

#### 🐛 Bug Report — Confusión Claude Desktop vs claude.ai

**Descripción del problema:**  
Durante esta sesión, Claude confundió reiteradamente el entorno de ejecución. Cuando GitHub MCP no cargó sus tools en `tool_search`, Claude asumió que el problema era que "no estábamos en Claude Desktop" y propuso soluciones para claude.ai (scripts PowerShell manuales, tokens de API, etc.) — cuando en realidad **la sesión siempre fue en Claude Desktop**.

**Patrón observado:**
1. GitHub MCP no devuelve tools en `tool_search`
2. Claude concluye erróneamente → "el MCP de GitHub no está disponible en este entorno (claude.ai)"
3. Claude propone workarounds para claude.ai en vez de diagnosticar correctamente el problema real (servidor no cargado en sesión activa)
4. Juan debe corregir explícitamente: "ESTAMOS EN CLAUDE DESKTOP"
5. Solución real: reiniciar Claude Desktop → MCP recarga → problema resuelto

**Causa raíz probable:**  
Claude no tiene acceso a una señal inequívoca de en qué interfaz está corriendo. Cuando `tool_search` no devuelve las tools esperadas, Claude infiere el entorno equivocado en lugar de diagnosticar el estado del servidor MCP.

**Impacto:**  
- Tokens desperdiciados en explicaciones incorrectas
- Frustración del usuario al tener que corregir el mismo error múltiples veces
- Propuestas de solución erróneas (reinstalar MCP local, crear tokens, scripts manuales)

**Solución aplicada (workaround del usuario):**  
Reiniciar completamente Claude Desktop → todos los servidores MCP se recargan → GitHub tools disponibles.

**Recomendación para el equipo de Anthropic:**  
Claude debería, ante la ausencia de tools MCP esperadas, diagnosticar primero el estado del servidor (¿reiniciar la app?) antes de inferir que el entorno es diferente al declarado por el usuario. Si el usuario dice explícitamente "estamos en Claude Desktop", esa declaración debe tener prioridad absoluta sobre cualquier inferencia basada en tools disponibles.

#### Decisiones técnicas tomadas
- CLAUDE.md v1.2 confirmado como fuente de verdad del ecosistema
- Protocolo de Fallo de Agente ahora documentado en CLAUDE.md
- GitHub MCP OAuth oficial confirmado como suficiente (no necesita servidor local)

#### Pendientes técnicos
- [ ] Migrar nginx a nombres de servicio Docker DNS
- [ ] **Iniciar Fase 4 — Modelado CardioRisk** ← PRÓXIMO PASO
- [ ] Primera delegación real a Deepseek: código sklearn baseline

---

## 📈 Resumen Acumulado

| Métrica | Valor |
|---------|-------|
| Sesiones registradas | 2 |
| Tokens Claude totales (estimado) | ~14,600 |
| Tokens sin ecosistema (estimado) | ~16,800 |
| Ahorro acumulado | ~13% |
| Tareas delegadas a Deepseek | 0 (ecosistema aún en construcción) |
| Fases CRISP-DM completadas | 1-3 (pre-ecosistema) |
| Fases CRISP-DM en progreso | 4 |

---

## 🔬 Hipótesis a validar

1. **H1:** El ecosistema reduce el consumo de tokens de Claude en >50% para tareas de generación de código ML repetitivo
2. **H2:** La calidad del código generado por Deepseek para sklearn es suficiente sin revisión extensiva de Claude
3. **H3:** Las visualizaciones de Nano-banana son superiores a matplotlib básico para presentación de resultados clínicos

---

*Log iniciado: 2026-03-11 | Proyecto: CardioRisk | Ecosistema: Hipócrates MCP v1.0*
