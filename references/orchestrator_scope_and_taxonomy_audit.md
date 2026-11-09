# AUDITORÍA DE ALCANCE Y REFUNDACIÓN TAXONÓMICA: AGENTIC TASK ORCHESTRATOR

**Fecha de Auditoría:** 2026-11-08  
**Auditor Responsable:** `AGENT-SYSTEM-ARCHITECT`  
**Estado:** Dictamen Técnico Aprobado

---

## 1. El Diagnóstico: ¿Por qué el nombre genera fricción y confusión?

El nombre `agentic-task-orchestrator` induce a una expectativa errónea en cualquier ingeniero o IA que lo lee por primera vez:
* **La expectativa habitual**: Un motor de orquestación de enjambres multiagente autónomos (similar a CrewAI, AutoGen, LangGraph o Swarm), donde múltiples agentes se pasan mensajes y ejecutan tareas distribuidas en paralelo.
* **La realidad empírica de la Skill**: La skill **NO** es un despachador de bots ni un bus de mensajería multi-proceso. Es un **Framework de Metodología de Ingeniería, Descomposición Anatómica de Tareas y Gobernanza Quirúrgica de Calidad**.

### ¿De dónde surgió el término "Agentic"?
El componente agéntico original se limitaba estrictamente a la **gobernanza de concurrencia multi-chat en Turno Cero**:
- Evitar colisiones destructivas cuando el mismo operador humano abre múltiples chats independientes en Antigravity sobre el mismo repositorio (`Engineering/CONCURRENCY_BOARD.md`).
- Asignar un indicativo técnico canónico (`AGENT-[DOMINIO]-[ROL]`) para registrar semáforos de archivo (`🔴 MODIFICANDO`, `🟡 ANALIZANDO`, `🟢 LIBERADO`).

Todo lo demás en la skill es **Planificación Anatómica Pura**:
1. Triage inicial exhaustivo en `00_Inventory.md`.
2. Prohibición radical de la abstracción superficial (*anti-shallow abstraction*).
3. Desglose quirúrgico de micro-problemas P01..PN con contratos de datos y casos de borde (`Analysis_Pxx.md`).
4. Resolución topológica en grafo acíclico dirigido (`Execution_Workflow.md`).
5. Régimen de supervisión calibrada Tri-Track (Fast, Streamlined, Deep).
6. Compuertas de calidad en 3 capas con validación en el stack nativo.
7. Puntos de restauración físicos en disco (Git savepoints / micro-commits atómicos).

---

## 2. Dictamen Taxonómico: Delimitación de Fronteras

Para erradicar confusiones futuras, se establece la separación formal entre dos dominios de la arquitectura:

```
┌────────────────────────────────────────────────────────────────────────┐
│            CAPA 1: PLANIFICACIÓN Y GOBERNANZA DE TAREAS                │
│                 (Anatomical Task Planner - ATLAS)                      │
│  • Qué se hace: Descomposición anatómica, contratos, inventario, DAG   │
│  • Quién lo hace: Gemini 3.8 / Arquitecto Humano                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Delega micro-problema mecánico
┌───────────────────────────────────▼────────────────────────────────────┐
│            CAPA 2: EJECUCIÓN MULTI-MODELO Y ENJAMBRES                  │
│                     (OpenBridge MCP Engine)                            │
│  • Cómo se ejecuta: Despacho asíncrono a Nemotron, DeepSeek, Gemma     │
│  • Quién lo hace: OpenCode Workers en paralelo a coste $0              │
└────────────────────────────────────────────────────────────────────────┘
```

### Propuesta de Renombrado y Retrocompatibilidad:
* **Nombre Canónico Propuesto**: **`anatomical-task-planner`** (o `surgical-task-governor`).
* **Alias de Compatibilidad**: Se conserva `agentic-task-orchestrator` como alias transparente en el frontmatter para no romper llamadas preexistentes ni slash commands (`/agentic-task-orchestrator`).
* **Misión Clarificada**:
  > *"Metodología quirúrgica universal de alta fidelidad para desglosar problemas complejos en inventarios anatómicos de micro-problemas, calcular grafos topológicos de resolución (DAG) y certificar compuertas de calidad nativas sin abstracciones superficiales."*
