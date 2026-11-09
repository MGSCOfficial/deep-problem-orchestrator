# PROTOCOLO DE ORQUESTACIÓN MULTIAGENTE Y CONCURRENCIA MULTI-CHAT

Esta guía define las normas de coordinación técnica entre agentes en dos dimensiones críticas:
1. **Concurrencia Inter-Chat (Sesiones Concurrentes)**: Múltiples chats/instancias independientes operando sobre el mismo repositorio.
2. **Delegación Intra-Chat (Master-Worker)**: Un agente orquestador principal que invoca subagentes especializados dentro de una misma sesión.

---

## 1. IDENTIDAD OPERATIVA: INDICATIVOS DE AGENTE (*AGENT CALL-SIGNS*)

Para evitar ambigüedades derivadas de nombres genéricos como "Chat 1" o "Ventana A", toda sesión activa adopta en su Turno Cero un **Indicativo Técnico Canónico**:

```text
AGENT-[DOMINIO]-[ROL_O_ENFOQUE]
```

### Ejemplos Estándar por Dominio:
- **Frontend / UI**: `AGENT-UI-OFFLINE`, `AGENT-WEB-SHELL`, `AGENT-REACT-CORE`.
- **Backend / APIs**: `AGENT-API-GATEWAY`, `AGENT-AUTH-SERVICE`, `AGENT-DB-ENGINE`.
- **Sistemas / Hardware**: `AGENT-GPU-CORE`, `AGENT-STORAGE-NVME`, `AGENT-KERNEL-TWEAKS`.
- **Orquestación Global**: `AGENT-TASK-ORCHESTRATOR`, `AGENT-RELEASE-MGR`.

*Ante múltiples instancias en el mismo dominio, se sufijan correlativamente:* `AGENT-API-01`, `AGENT-API-02`.

---

## 2. EL TABLERO CENTRAL DE CONCURRENCIA (`CONCURRENCY_BOARD.md`)

Ubicación: `Engineering/CONCURRENCY_BOARD.md` (o `.execution/concurrency_board.md`).

### Protocolo de Turno Cero:
Antes de descomponer o modificar código, el agente **DEBE LEER** este archivo para auditar el estado del repositorio:
1. **Comprobar Reclamos**: Verificar si las rutas o archivos a modificar están marcados como `🔴 MODIFICANDO`.
2. **Registrar Reclamo**: Si están libres, registrar su indicativo, tarea activa y rutas bajo el estado `🟡 ANALIZANDO`.
3. **Escalar a Escritura**: Al iniciar la Fase 3 de implementación de código, actualizar a `🔴 MODIFICANDO`.
4. **Liberar al Concluir**: Tras certificar la tarea con éxito, actualizar a `🟢 LIBERADO` y emitir aviso `[LOCK_RELEASE]`.

---

## 3. ARBITRAJE INTELIGENTE ANTE CONFLICTOS EN EL MISMO ARCHIVO

Cuando un agente entrante (ej. `AGENT-UI-SHELL`) detecta que el archivo que necesita editar está bajo `🔴 MODIFICANDO` por otro agente titular (ej. `AGENT-GPU-CORE`), **se prohíbe terminantemente la sobreescritura ciega**.

El agente presenta al usuario las **3 Vías de Arbitraje**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ⚠️ CONFLICTO DE CONCURRENCIA DETECTADO               │
│ Archivo en disputa: [Ruta_Archivo]                                     │
│ Bloqueado por: [AGENT-TITULAR] (Tarea: [Nombre_Tarea])                 │
├────────────────────────────────────────────────────────────────────────┤
│ ¿Cómo deseas resolver el cruce de responsabilidades?                   │
│                                                                        │
│ 1. [DELEGAR AL AGENTE TITULAR] (Fusión y Co-autoría):                  │
│    Redactar 'Delegated_Analysis_Pxx.md' con el cambio requerido,       │
│    transferirlo a la carpeta del titular y notificar por el buzón.     │
│    -> El titular asume ambas modificaciones de forma unificada.        │
│                                                                        │
│ 2. [COLA DE ESPERA Y REBASE] (Secuencial):                             │
│    Registrar '⏳ EN_ESPERA_COLA'. Pausar la edición hasta que el       │
│    titular pase a '🟢 LIBERADO'. Al reanudar, se absorben los         │
│    cambios y se aplican los propios sin colisiones.                    │
│                                                                        │
│ 3. [BIFURCAR POR WORKTREE] (Desarrollo Paralelo Aislado):              │
│    Crear una rama de trabajo aislada en Git. Ambos agentes operan      │
│    simultáneamente en árboles físicos desacoplados.                    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. PROTOCOLO DE TRASPASO Y ADOPCIÓN DE TAREAS DELEGADAS

### A. Procedimiento del Agente Emisor:
1. Redacta el análisis profundo de su requerimiento: `Delegated_Analysis_[Slug].md`.
2. Deposita el archivo en la carpeta del receptor:  
   `Engineering/Tasks/[Tarea_Receptor]/Inbox/Delegated_Analysis_[Slug].md`.
3. Registra en la sección de buzón de `CONCURRENCY_BOARD.md`:
   ```markdown
   [YYYY-MM-DD HH:MM] [HANDOFF_REQUEST] [AGENT-EMISOR -> AGENT-RECEPTOR]: Tarea transferida a tu carpeta Inbox/ para resolución unificada.
   ```
4. Actualiza su estado en el tablero a `🤝 DELEGADO` y notifica al usuario que la ventana quedó liberada.

### B. Procedimiento del Agente Receptor:
1. Al iniciar su siguiente turno o subfase, audita su carpeta `Inbox/` y el buzón del tablero.
2. Incorpora la tarea delegada a su `00_Inventory.md` en la sección **Bandeja de Tareas Delegadas**.
3. Añade la tarea a su `Execution_Workflow.md` y unifica la edición del archivo compartido de forma coherente.

---

## 5. GESTIÓN DE BLOQUEOS HUÉRFANOS (*STALE LOCKS*)

- Si un reclamo en el tablero no registra actividad durante **más de 4 horas** o data de una sesión cerrada:
  - El agente activo **no se bloquea indefinidamente**.
  - Pregunta al usuario:
    > *"El módulo [X] figura reclamado por [AGENT-PREVIO] hace más de 4 horas. ¿Esa sesión concluyó? Si es así, puedo purgar el bloqueo y continuar."*
  - Con el visto bueno del usuario, purga el registro y toma posesión del módulo.

---

## 6. DELEGACIÓN A SUBAGENTES EN LA MISMA SESIÓN (MASTER-WORKER)

Cuando un agente orquestador principal delega tareas a subagentes (`invoke_subagent`):
1. **Límites Estrictos de Archivos**: Cada subagente recibe un `AGENT_TASK_BLUEPRINT.md` con un perímetro cerrado de rutas a crear/modificar.
2. **Prohibición de Herramientas Parásitas**: El subagente valida con el arnés nativo oficial del proyecto. Prohibido inventar comprobadores en Python.
3. **Formato Obligatorio de Retorno**:
   ```markdown
   ### REPORTE DE SUBAGENTE: [ROL]
   - **Archivos Modificados**: [Rutas exactas]
   - **Comando de Verificación**: `[Comando nativo ejecutado]`
   - **Resultado**: [100% PASS / EXIT CODE 0 / Sin hallazgos]
   - **Observaciones Técnicas**: [Notas críticas]
   ```
4. **Circuit Breaker**: Máximo 2 intentos de corrección ante un fallo del subagente antes de que el orquestador principal intervenga.
