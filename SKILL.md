---
name: deep-problem-orchestrator
description: Metodología quirúrgica universal de alta fidelidad para analizar a profundidad, descomponer problemas anatómicos en micro-problemas (00_Inventory.md), secuenciar y certificar tareas técnicas complejas con calidad determinista. Ofrece gobernanza Tri-Track (Fast, Streamlined, Deep), ciclo adaptativo Just-In-Time (JIT), persistencia en disco contra pérdida de contexto y compuertas de calidad nativas con el motor ATLAS integrado.
---

# DEEP PROBLEM ORCHESTRATOR & HIGH-FIDELITY DECOMPOSITION FRAMEWORK

Sistema metodológico universal para la planificación rigurosa, descomposición anatómica de alta fidelidad, gobernanza de concurrencia multi-chat y certificación sistemática de tareas en cualquier entorno de software.

Erradica de raíz el **resumen superficial (*shallow abstraction*)**, las colisiones destructivas entre múltiples chats, la fatiga del operador por paradas innecesarias y el derroche de tokens, garantizando una supervisión humana calibrada (*Human-in-the-Loop*) y persistencia desacoplada en disco.

---

## 1. PRINCIPIOS FUNDAMENTALES (LOS 8 PILARES DE ROBUSTEZ)

1. **Identidad Operativa Canónica (*Agent Call-signs*)**:
   - Queda prohibido usar denominaciones genéricas o ambiguas como "Chat 1" o "Ventana A".
   - Toda sesión o instancia asume en Turno Cero un indicativo técnico derivado de su dominio: `AGENT-[DOMINIO]-[ROL]` (ej. `AGENT-UI-OFFLINE`, `AGENT-API-GATEWAY`, `AGENT-DB-ENGINE`, `AGENT-GPU-CORE`, `AGENT-KERNEL-SYS`).
2. **Gobernanza de Concurrencia Multi-Chat en Turno Cero**:
   - Antes de modificar código, el agente audita `Engineering/CONCURRENCY_BOARD.md` para verificar qué módulos están reclamados por otros agentes en sesiones paralelas.
   - Ante colisiones en el mismo archivo, prohíbe la sobreescritura ciega y activa el **Arbitraje Inteligente en 3 Vías** (Delegación, Cola de Espera o Worktree).
3. **Cero Superficialidad (*No Shallow Abstractions*)**:
   - Queda terminantemente prohibido reducir un problema técnico a checklists genéricos de 2 o 3 líneas que omiten contratos de datos, firmas y casos de borde.
   - Cada micro-problema debe contar con especificación anatómica antes de tocar código de producción.
4. **Ciclo de Supervisión Humana Calibrado (Tri-Track)**:
   - **Deep-Track**: 1 Turno = 1 Micro-Problema con parada obligatoria (*Hard Stop*) por turno. Máximo control para arquitecturas críticas o de alto riesgo.
   - **Streamlined-Track**: Descomposición completa aprobada en bloque por el usuario; ejecución fluida continua con detención solo ante fallos o bifurcaciones de diseño. Erradica la fatiga de "ping-pong".
   - **Fast-Track**: Cambio directo en un solo archivo con verificación instantánea sin burocracia.
5. **Aislamiento por Tarea y Persistencia de Contexto (*Context-Switch Proof*)**:
   - Toda tarea estructurada reside en su directorio: `Engineering/Tasks/[YYYYMMDD_Nombre_Tarea]/`.
   - El archivo `00_Inventory.md` y el estado atómico de ATLAS actúan como puntero inmutable.
   - Se puede pausar la tarea, atender urgencias y reanudar semanas después sin pérdida de contexto ni re-análisis redundantes.
6. **Orquestación de Dependencias (Grafo Topológico Previo)**:
   - Se sintetiza la matriz de dependencias en `Execution_Workflow.md` determinando el orden topológico óptimo antes de la fase de construcción.
7. **Análisis y Ejecución Adaptativa Just-In-Time (JIT) y Micro-Rollbacks**:
   - Para evitar el diseño prematuro (*Big Design Up Front*), se permite encadenar: *Analizar Pxx ➔ Implementar Pxx ➔ Inspeccionar evidencia de runtime ➔ Analizar Pxx+1 con datos empíricos reales*.
   - **Puntos de Restauración Inmutables (Git Savepoints)**: Tras verificar exitosamente cada micro-problema (`PASS` en arnés nativo) y antes de avanzar al siguiente, el agente realiza un micro-commit atómico en Git (ej. `git commit -m "feat(Pxx): [titulo]"`). Esto crea un punto de restauración físico en disco que permite revertir cambios instantáneamente ante cualquier fallo posterior sin afectar los problemas ya certificados.
8. **Verificación en Stack Nativo (Cero Comprobadores Huérfanos en Python)**:
   - **PROHIBICIÓN ESTRICTA**: Queda terminantemente prohibido inventar o alucinar scripts en Python (`test_check.py`, `verify.py`, etc.) para simular que se corre una suite de pruebas en proyectos ajenos que no usan Python o no tienen arnés preexistente.
   - Emplear exclusivamente el arnés nativo oficial del repositorio (`npm test`, `pytest`, `cargo test`, `go test`, `CATE` en Chernobil Underground, etc.). Si no existe arnés, validar mediante análisis sintáctico nativo (`node --check`, `py_compile`, `bash -n`, linters) y pruebas de humo no destructivas.

---

## 2. MODALIDADES DE FLUJO DE TRABAJO

### A. Régimen Deep-Track (Alta Cirugía / Alto Riesgo / Múltiples Módulos)
Diseñado para cambios estructurales profundos donde cada paso requiere supervisión humana interactiva:
```text
[Fase 0: Triage Inicial] ➔ Creación de 00_Inventory.md
          │
          ▼
┌────────────────────────────────────────────────────────┐
│ Fase 1: Análisis Profundo Quirúrgico (1 Turno = 1 Pxx) │
│ - Redacción de Analysis_Pxx_[Slug].md                 │
│ - HARD STOP obligatorio tras cada micro-problema      │
│ - Aprobación del usuario antes de pasar a Pxx+1       │
└──────────────────────────┬─────────────────────────────┘
                           ▼
[Fase 2: Grafo Topológico] ➔ Execution_Workflow.md
                           ▼
┌────────────────────────────────────────────────────────┐
│ Fase 3: Ejecución Quirúrgica Unitaria                  │
│ - Resolución guiada de 1 problema                      │
│ - Verificación con arnés nativo (0 errores)            │
│ - Micro-commit Git atómico: feat(Pxx): [titulo]        │
│ - HARD STOP obligatorio tras cada problema resuelto   │
└────────────────────────────────────────────────────────┘
```

### B. Régimen Streamlined-Track (2 a 4 Micro-Problemas Delimitados)
Diseñado para refactorizaciones acotadas, desacoplamientos o integraciones claras, erradicando la fatiga de aprobaciones repetitivas:
```text
[Fase 0: Triage y Plan Completo] ➔ 00_Inventory.md con todos los P01..PN
          │
          ▼
[Compuerta Única de Aprobación Humana] ➔ Usuario: "Aprobado, ejecuta"
          │
          ▼
┌────────────────────────────────────────────────────────┐
│ Fase de Ejecución Secuencial Autónoma                  │
│ - Ejecuta P01 ➔ Verifica ➔ Micro-commit ➔ [RESUELTO]   │
│ - Ejecuta P02 ➔ Verifica ➔ Micro-commit ➔ [RESUELTO]   │
│ - Ejecuta PN  ➔ Verifica ➔ Micro-commit ➔ [RESUELTO]   │
│ (Hard Stop SOLO si falla un test o linter)             │
└──────────────────────────┬─────────────────────────────┘
                           ▼
[Certificación Final y Cierre] ➔ Reporte consolidado único al usuario
```

---

## 3. ARBITRAJE DE CONCURRENCIA Y DELEGACIÓN DE TAREAS (*TASK HANDOFF*)

Cuando un agente entrante necesita modificar un archivo reclamado como `🔴 MODIFICANDO` por un agente titular, debe presentar las **3 Vías de Arbitraje**:

1. **Vía 1: Delegación al Titular (Fusión de Contexto y Co-Autoría)**:
   - El agente emisor redacta `Delegated_Analysis_Pxx.md` con su requerimiento técnico detallado.
   - Transfiere el archivo a la carpeta del titular:  
     `Engineering/Tasks/[Tarea_Titular]/Inbox/Delegated_Analysis_Pxx.md`.
   - Registra en el buzón de `CONCURRENCY_BOARD.md` el aviso `[HANDOFF_REQUEST]`.
   - Marca su estado como `🤝 DELEGADO` y libera su ventana.
   - El titular adopta la tarea en su inventario y flujo, unificando ambas modificaciones.
2. **Vía 2: Cola de Espera y Rebase (Secuencial)**:
   - El agente pasa a `⏳ EN_ESPERA_COLA`.
   - Espera a que el titular certifique y libere el archivo (`🟢 LIBERADO`).
   - Al reanudar, lee los cambios introducidos por el titular y aplica los suyos de forma segura.
3. **Vía 3: Bifurcación por Worktree (Paralelo Real)**:
   - Crea un Worktree de Git aislado (ej. `.worktrees/feature-branch`).
   - Ambos agentes trabajan en paralelo en copias físicas separadas sin interferencia.

---

## 4. CALIBRACIÓN TRI-TRACK

| Parámetro | Fast-Track (< 3 min) | Streamlined-Track (2 a 4 Micro-Problemas) | Deep-Track (Tareas Críticas / Masivas) |
| :--- | :--- | :--- | :--- |
| **Alcance** | Tweak atómico, bug puntual, 1 archivo | Desacoplamientos, refactors medianos, módulos acotados | Nuevas arquitecturas, refactors multi-módulo, riesgo de regresión |
| **Concurrencia** | Verificación en `CONCURRENCY_BOARD.md` sin lock prolongado | Registro de Call-sign, lock en `CONCURRENCY_BOARD.md` (`ANALIZANDO` ➔ `MODIFICANDO`) | Registro formal de Call-sign, lock estricto, buzón inter-chat y semáforos |
| **Interacción Humana** | 1 Interacción (Directa) | **1 Aprobación del Plan**. Ejecución continua; parada solo ante fallo o bloqueo. | **Hard Stop en Cada Turno**. 1 micro-problema por turno con validación paso a paso. |
| **Artefactos en Disco** | Cero archivos Markdown | `00_Inventory.md` + análisis consolidado o JIT en carpeta de tarea | `00_Inventory.md` + `Analysis_Pxx.md` individuales + `Execution_Workflow.md` |
| **Consumo de Tokens** | Mínimo | Balance óptimo: cero fatiga humana, trazabilidad completa | Máxima fidelidad y control granular |

---

## 5. ATLAS: MOTOR NATIVO DE MEDIACIÓN Y ZERO-TOKEN ORCHESTRATION

Para erradicar el derroche de tokens en formateo manual de tablas Markdown, cálculo de árboles de dependencias y gestión de semáforos, el framework integra el motor nativo **ATLAS** (`scripts/atlas/atlas.py`):

1. **Ruta Canónica de Invocación Universal**:
   - En cualquier proyecto vía CLI directo en PATH:  
     `atlas [comando]`
   - Vía Python directo:  
     `python "C:\Users\MGSCO\.agents\skills\agentic-task-orchestrator\scripts\atlas\atlas.py" [comando]`
2. **Detección Dinámica de Workspace**:
   - ATLAS opera automáticamente sobre el directorio actual (`os.getcwd()`), o sobre la ruta indicada explícitamente mediante `--workspace <ruta>`.
3. **Compilación Determinista para Humanos (0 Tokens)**:
   - El agente **no escribe tablas Markdown a mano** para `00_Inventory.md`, `CONCURRENCY_BOARD.md` ni `Execution_Workflow.md`.
   - Utiliza comandos CLI nativos:
     - `atlas init <task_name> --agent-name <callsign>`
     - `atlas add-micro <micro_id> --title "<titulo>" --files "<rutas>"`
     - `atlas lock "<rutas>" --agent-name <callsign> --level MODIFICANDO`
     - `atlas update-micro <micro_id> --status RESOLVED`
     - `atlas resolve-dag`
     - `atlas unlock --agent-name <callsign>`
      - `atlas finish --summary "<resumen>"` (archiva tarea, compila inventario final y libera puntero activo)
   - ATLAS actualiza el estado atómico en disco y renderiza automáticamente los tableros Markdown para el usuario humano.
4. **Telemetría Zero-Token para Agentes (`--agent`)**:
   - Para consultar el puntero de estado o reanudar una tarea sin releer archivos masivos:  
     `python "C:\Users\MGSCO\.agents\skills\agentic-task-orchestrator\scripts\atlas\atlas.py" --agent status`
   - Devuelve una sola línea JSON compacta (<20 tokens) con el problema activo, estado y próxima acción.
5. **Fallback Manual Resiliente**:
   - Si se opera en un entorno donde Python no esté disponible de inmediato en el PATH, el agente aplicará las plantillas manuales en `templates/` garantizando que la metodología nunca se detenga.

---

## 6. DOCUMENTOS Y PLANTILLAS DE REFERENCIA

- [templates/CONCURRENCY_BOARD_TEMPLATE.md](./templates/CONCURRENCY_BOARD_TEMPLATE.md) - Tablero maestro de concurrencia y semáforos.
- [templates/00_INVENTORY_TEMPLATE.md](./templates/00_INVENTORY_TEMPLATE.md) - Cuadro de mando, puntero de estado y bandeja de tareas delegadas.
- [templates/ANALYSIS_MICRO_TEMPLATE.md](./templates/ANALYSIS_MICRO_TEMPLATE.md) - Plantilla del análisis profundo por micro-problema.
- [templates/EXECUTION_WORKFLOW_TEMPLATE.md](./templates/EXECUTION_WORKFLOW_TEMPLATE.md) - Plantilla de matriz de dependencias y flujo.
- [templates/AGENT_TASK_BLUEPRINT.md](./templates/AGENT_TASK_BLUEPRINT.md) - Plano de trabajo para subagentes delegados intra-sesión.
- [templates/BACKLOG_IDEAS_TEMPLATE.txt](./templates/BACKLOG_IDEAS_TEMPLATE.txt) - Banco temporal de ideas volátiles.
- [references/multiagent_orchestration.md](./references/multiagent_orchestration.md) - Guía completa de concurrencia inter-chat y delegación.
- [references/execution_flow_and_backlog.md](./references/execution_flow_and_backlog.md) - Ciclo de vida de tareas, análisis adaptativo JIT y reanudación.
- [references/three_layer_certification.md](./references/three_layer_certification.md) - Protocolo de compuertas nativas sin comprobadores Python inventados.
