# TABLERO DE CONTROL Y REGISTRO DE TAREA (INVENTORY)

**Tarea:** `[NOMBRE_O_IDENTIFICADOR_DE_LA_TAREA]`  
**Directorio de Trabajo:** `Engineering/Tasks/[YYYYMMDD_Nombre_Tarea]/`  
**Agente Titular:** `[AGENT-DOMINIO-ROL]`  
**Fecha de Inicio:** `[YYYY-MM-DD]`  
**Estado General:** `[FASE 0: TRIAGE / FASE 1: ANÁLISIS / FASE 2: ORQUESTACIÓN / FASE 3: EJECUCIÓN / PAUSADO / COMPLETADO]`  

---

## 1. PUNTERO DE ESTADO ACTIVO (CONTEXT-SWITCH ANCHOR)
*Este bloque permite pausar la tarea, atender otras prioridades y reanudar sin pérdida de contexto.*

- **Fase Activa:** `[FASE 1: Análisis Profundo / FASE 3: Ejecución]`
- **Micro-Problema en Curso:** `[P01 / P02 / ...]`
- **Estado del Micro-Problema:** `[EN ANÁLISIS / ANÁLISIS COMPLETADO (PENDIENTE APROBACIÓN) / EN EJECUCIÓN / RESUELTO]`
- **Próxima Acción al Reanudar:** `[Descripción concreta del siguiente paso inmediato]`

---

## 2. INVENTARIO DE MICRO-PROBLEMAS

| ID | Título del Micro-Problema | Archivo de Análisis | Estado | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| **P01** | [Título conciso de P01] | `Analysis_P01_[Slug].md` | `[PENDIENTE / LISTO / RESUELTO]` | `[Comando nativo]` |
| **P02** | [Título conciso de P02] | `Analysis_P02_[Slug].md` | `[PENDIENTE / LISTO / RESUELTO]` | `[Comando nativo]` |
| **P03** | [Título conciso de P03] | `Analysis_P03_[Slug].md` | `[PENDIENTE / LISTO / RESUELTO]` | `[Comando nativo]` |

*(Estados válidos: `PENDIENTE_ANALISIS`, `EN_ANALISIS`, `ANALIZADO_APROBADO`, `EN_EJECUCION`, `RESUELTO`).*

---

## 3. BANDEJA DE TAREAS DELEGADAS (INBOX / CO-AUTHORING)
*Micro-problemas adoptados desde otros agentes para edición unificada sin colisiones.*

| ID Delegado | Agente Emisor | Título del Requerimiento | Archivo de Análisis Transferido | Estado de Adopción |
| :--- | :--- | :--- | :--- | :--- |
| `P0X-DEL` | `[AGENT-EMISOR]` | [Requerimiento delegado] | `Inbox/Delegated_Analysis_xxx.md` | `[PENDIENTE / INTEGRADO EN FLUJO / RESUELTO]` |

---

## 4. HISTORIAL DE EJECUCIÓN CONSOLIDADO
- `[YYYY-MM-DD HH:MM]` - Triage completado por [AGENT-DOMINIO-ROL]. Creado inventario con [N] micro-problemas.
- *(Se agregan entradas breves de una línea tras certificar cada micro-problema).*
