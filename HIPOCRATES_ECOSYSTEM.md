# 🏥 Hipócrates MCP Ecosystem

> Ecosistema de agentes MCP orquestados localmente con Docker para data science médico.
> Construido como parte del proyecto CardioRisk — IBM Data Science Professional Certificate.

---

## Arquitectura

```
Claude Desktop (orquestador)
        │
        ├── deepseek-mcp        → Inferencia local, generación de código
        ├── nano-banana-mcp     → Imágenes médicas (Gemini 2.5 Flash)
        ├── inworld-tts-mcp     → Síntesis de voz clínica
        ├── github-mcp          → Versionado y documentación
        └── deepseek web_search → Búsqueda web (Brave API)
                │
        mcp-gateway (nginx)
                │
        Docker network mcp-internal
```

## Stack

- **Orquestador:** Claude Desktop (Sonnet 4.6)
- **Inferencia local:** Deepseek via Node.js MCP server
- **Imágenes:** Google Gemini 2.5 Flash Image (REST API)
- **TTS:** Inworld AI TTS v1.5 Max
- **Gateway:** nginx:alpine
- **Contenedores:** Docker Compose
- **OS:** Windows 11 + Python 3.14

## Principio de diseño

**Claude Sonnet solo piensa. Los microservicios ejecutan.**

Esto maximiza la eficiencia de tokens reservando la capacidad de razonamiento de Claude para decisiones que realmente la requieren.

## Estado

- ✅ nano-banana (Gemini 2.5 Flash Image)
- ✅ inworld-tts (Inworld TTS 1.5 Max)
- ✅ deepseek (local inference)
- ✅ github (OAuth oficial Anthropic)
- ✅ deepseek web_search
- ✅ mcp-gateway (nginx)

## Documentación relacionada

- [EXPERIMENT_LOG.md](./EXPERIMENT_LOG.md) — Bitácora de sesiones y métricas de tokens
- [proyecto_medico/](./proyecto_medico/) — CardioRisk CRISP-DM
