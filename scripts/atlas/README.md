# ATLAS v1.0 - Agent Task & Lock Arbitration System
**Motor de Mediación, Estado Atómico, Grafo de Dependencias y Arbitraje de Concurrencia para Agentes IA**

ATLAS es el homólogo de **CATE** para el ciclo de vida y la orquestación de tareas en Chernobil Underground y el ecosistema de agentes IA.

---

## 1. Filosofía Arquitectónica: Zero-Token Operations

* **CATE** erradicó el consumo de tokens en pruebas de código, diagnósticos y sandboxing (de miles de tokens a <20 tokens).
* **ATLAS** erradica el consumo de tokens en formateo de Markdown, tablas de inventario, cálculo de árboles de dependencias (DAG), gestión de semáforos y comunicación inter-agente.
* **El Análisis Profundo se preserva al 100%**: El agente dedica todo su presupuesto cognitivo a redactar el `Analysis_Pxx_[Slug].md` técnico (causa raíz, riesgos, contratos y código). **Cero tokens en fontanería burocrática.**

---

## 2. Componentes del Núcleo (`core/`)

| Módulo | Responsabilidad |
| :--- | :--- |
| `core.state` | Máquina de estados transaccional en JSON atómico y puntero `Engineering/Tasks/.atlas_active_task`. |
| `core.dag` | Motor matemático DAG con detección de deadlocks/ciclos y cálculo de lotes paralelos (`graphlib`). |
| `core.concurrency` | Control de semáforos (`🟡 ANALIZANDO`, `🔴 MODIFICANDO`, `🟢 LIBERADO`) en `Engineering/CONCURRENCY_BOARD.md`. |
| `core.compiler` | Compilador nativo que genera `00_Inventory.md` y `Execution_Workflow.md` en milisegundos para el humano. |
| `core.bus` | Bus de mensajería inter-agente y delegación structured handoff (`Inbox/Delegated_Analysis_Pxx.md`). |
| `core.formatters` | Telemetría dual: `--agent` (JSON ultra-compacto <25 tokens) vs `--human` (Consola visual ANSI). |

---

## 3. Catálogo de Comandos CLI

### Inicialización y Triage
```bash
# Inicializa una nueva tarea y compila el 00_Inventory.md base
python atlas.py init <task_name> --agent-name <CALLSIGN> [--agent]

# Agrega un micro-problema al inventario
python atlas.py add-micro <Pxx> --title "Título" --files "file1,file2" [--blocked-by "P01"] [--verify "cmd"] [--agent]
```

### Telemetría de Estado (Context-Switch Proof)
```bash
# Consulta el puntero de estado activo en 1 línea (<20 tokens)
python atlas.py status --agent

# Actualiza el estado de un micro-problema (regenera checks en 00_Inventory.md)
python atlas.py update-micro <Pxx> --status <ANALYZED|EXECUTING|RESOLVED> [--agent]

# Cambia la fase global (0: Triage, 1: Análisis, 2: Workflow, 3: Ejecución, 4: Certificada)
python atlas.py set-phase <0..4> [--agent]
```

### Dependencias y Orquestación DAG
```bash
# Resuelve el orden topológico y compila automáticamente Execution_Workflow.md
python atlas.py resolve-dag [--agent]
```

### Control de Concurrencia y Semáforos
```bash
# Bloquea rutas con verificación de colisiones atómica
python atlas.py lock "path1,path2" --agent-name <CALLSIGN> [--level ANALIZANDO|MODIFICANDO] [--agent]

# Libera semáforos a 🟢 LIBERADO y registra aviso en el buzón
python atlas.py unlock --agent-name <CALLSIGN> [--summary "Resumen"] [--agent]
```

### Bus Inter-Agente y Delegación
```bash
# Transfiere un micro-problema al Inbox de otra tarea sin cartas en prosa
python atlas.py delegate --to <tarea_destino> --from-agent <CALLSIGN> --micro-id <Pxx> --title "..." --contract '{"key":"val"}' [--agent]
```

---

## 4. Verificación y Calidad

Para ejecutar la suite de pruebas unitarias hermética de ATLAS (en <100 ms):
```bash
python "Gemini Workstation/ATLAS/test_atlas.py"
```
