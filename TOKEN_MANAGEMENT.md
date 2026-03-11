# TOKEN_MANAGEMENT.md — Gestión de Tokens Hipócrates MCP

## 1. Sistema de métricas por sesión

| Tarea | Tokens Claude estimados | Agente | Tokens ahorrados vs flujo sin ecosistema | Notas |
|-------|------------------------|--------|------------------------------------------|-------|
|       |                        |        |                                          |       |

**Cómo estimar tokens Claude**: Contar intercambios de mensajes (pregunta + respuesta) × ~500 tokens promedio por intercambio.

**Agentes**: [C] Claude Sonnet | [D] Deepseek | [N] Nano-banana | [T] Inworld TTS | [G] GitHub MCP | [W] Web Search

---

## 2. Protocolo de checkpoints

**Regla**: Checkpoint obligatorio cada 4 ciclos completos (diseño→código→debug→commit).

**Qué guardar en cada checkpoint**:
- Estado actual del modelo (hiperparámetros, arquitectura)
- Métricas de evaluación (recall, precision, f1, accuracy)
- Transformaciones de features aplicadas
- Próximo paso planificado
- Lecciones aprendidas en el ciclo

**Template de checkpoint** — copiar/pegar en `EXPERIMENT_LOG.md`:
```markdown
## Checkpoint [Fecha] - Ciclo [N]

### Estado actual
- **Modelo**: [nombre/arquitectura]
- **Hiperparámetros**: [lista]
- **Métricas**:
  - Recall test: [valor]
  - Precision test: [valor]
  - F1 test: [valor]
  - Accuracy test: [valor]

### Transformaciones aplicadas
1. [transformación 1]

### Próximo paso
[Descripción clara del siguiente experimento]

### Lecciones aprendidas
- [lección 1]

### Tokens utilizados en este ciclo
- Claude [C]: [estimado]
- Delegado [D][N][G]: [estimado]
- Ahorro estimado vs flujo tradicional: [estimado]
```

---

## 3. Reglas anti-desperdicio

1. **Historial limitado**: No dejar crecer el historial más de 4 ciclos completos en una sesión
2. **Sesiones nuevas**: Abrir nueva sesión con resumen ejecutivo (template abajo) en vez de continuar sesión larga
3. **Delegación estricta**: No pedir a Claude tareas que Deepseek puede ejecutar — ver tabla en CLAUDE.md
4. **Señal de alerta `[C]×3`**: Si Claude lleva más de 3 respuestas seguidas → revisar si se puede delegar
5. **Contexto consciente**: Monitorear uso de contexto y aplicar checkpoint + resumen antes del 70%

---

## 4. Verificación pre-ejecución — Checklist Claude

Claude DEBE aplicar este checklist a TODO código generado por Deepseek antes de que Juan lo ejecute:

- [ ] **Sin data leakage**: ¿`.fit()` solo en train y `.transform()` separado en test?
- [ ] **Métrica principal**: ¿Se optimiza Recall (no Accuracy)?
- [ ] **Split estratificado**: ¿`train_test_split` usa `stratify=y`?
- [ ] **Columnas válidas**: ¿Las columnas usadas existen en Cleveland (13 features)?
- [ ] **Persistencia**: ¿El modelo se guarda con `joblib`?
- [ ] **Reproducibilidad**: ¿Hay `random_state=42` en todo?
- [ ] **Balance de clases**: ¿Se usa `class_weight='balanced'` o técnica equivalente?

> **Regla**: Si algún punto falla → Deepseek corrige. Claude NO ejecuta tareas de corrección de código.

---

## 5. Template de resumen ejecutivo — sesión nueva

Cuando el contexto llegue a ~70%, copiar este template como primer mensaje de la nueva sesión:

```
## RESUMEN EJECUTIVO — Hipócrates MCP / CardioRisk

### Estado actual
- Fase CRISP-DM: [número y nombre]
- Último modelo probado: [nombre]
- Mejor Recall obtenido: [valor]
- Transformaciones activas: [lista]

### Próximas acciones
1. [acción 1 — prioridad alta]
2. [acción 2 — prioridad media]

### Configuración técnica vigente
- Métrica objetivo: Recall ≥ 0.85
- Dataset: Cleveland Heart Disease (303 muestras, 13 features)
- Clase positiva: 1 (tiene enfermedad cardíaca)
- Validación: train_test_split estratificado, random_state=42

### Tokens última sesión
- Claude [C]: [estimado] | Delegados: [estimado] | Ahorro: [%]
```

---

*Versión: 1.0 | Creado: 2026-03-11 | Basado en lecciones de JokeGold5455 y Boris Cherny (r/ClaudeAI)*
*Lección origen: 160k tokens consumidos en 3 rondas por overhead MCP no monitoreado*
