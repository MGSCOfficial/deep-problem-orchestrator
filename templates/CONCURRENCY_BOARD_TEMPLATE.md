# TABLERO CENTRAL DE CONCURRENCIA Y CONTROL DE MÓDULOS (MULTI-AGENTE)

**Ubicación Estándar:** `Engineering/CONCURRENCY_BOARD.md` (o `.execution/concurrency_board.md`)  
**Última Actualización Global:** `[YYYY-MM-DD HH:MM]`  

---

## 1. REGISTRO DE AGENTES ACTIVOS Y RECLAMO DE MÓDULOS (LOCKS)

| Indicativo del Agente | Tarea Activa / Directorio | Módulos Reclamados (Lock) | Estado del Semáforo | Última Actividad |
| :--- | :--- | :--- | :--- | :--- |
| `AGENT-EJEMPLO-01` | `Engineering/Tasks/YYYYMMDD_TareaA/` | `Ruta/ModuloA/*` | `🔴 MODIFICANDO` | YYYY-MM-DD HH:MM |
| `AGENT-EJEMPLO-02` | `Engineering/Tasks/YYYYMMDD_TareaB/` | `Ruta/ModuloB/*` | `🟡 ANALIZANDO`  | YYYY-MM-DD HH:MM |

### Leyenda de Estados del Semáforo:
- `🟢 LIBERADO`: Tarea finalizada y certificada. Módulos disponibles sin restricción.
- `🟡 ANALIZANDO`: Bloqueo de lectura. El agente está explorando e inspeccionando código; otros agentes pueden leer pero no modificar.
- `🔴 MODIFICANDO`: Bloqueo exclusivo de escritura. Prohibido que otros agentes editen rutas dentro de este perímetro.
- `⏳ EN_ESPERA_COLA`: El agente aguarda la liberación de un módulo bloqueado para aplicar rebase y continuar.
- `🤝 DELEGADO`: Tarea transferida a otro agente titular para co-autoría y edición unificada.

---

## 2. BUZÓN ASÍNCRONO DE MENSAJES Y DELEGACIÓN (INTER-AGENT BUS)
*Canal en disco para transferir requerimientos, notificar cambios de contratos o avisar liberaciones.*

- `[YYYY-MM-DD HH:MM]` `[AVISO]` `[AGENT-ORIGEN -> AGENT-DESTINO]`: [Notificación de cambio de contrato de API o subrutina].
- `[YYYY-MM-DD HH:MM]` `[HANDOFF_REQUEST]` `[AGENT-ORIGEN -> AGENT-DESTINO]`: [Solicitud formal de delegación con archivo transferido en Inbox/].
- `[YYYY-MM-DD HH:MM]` `[LOCK_RELEASE]` `[AGENT-ORIGEN -> TODOS]`: [Módulos liberados tras certificación exitosa].

---

## 3. PROTOCOLO OPERATIVO DEL TABLERO
1. **Turno Cero Obligatorio**: Todo agente en cualquier sesión de chat debe leer este archivo antes de analizar o modificar código.
2. **Reclamo de Perímetro**: Si el módulo está libre, el agente registra su indicativo, tarea, rutas a tocar y pasa su estado a `🟡 ANALIZANDO`.
3. **Escalada a Escritura**: Al iniciar la Fase 3 de implementación, actualiza su estado a `🔴 MODIFICANDO`.
4. **Liberación Inmediata**: Al certificar y finalizar la tarea, actualiza su estado a `🟢 LIBERADO` y emite aviso `[LOCK_RELEASE]`.
5. **Detección de Bloqueos Huérfanos (*Stale Locks*)**: Si un bloqueo supera 4 horas de inactividad, el agente consultará al usuario si la sesión previa fue cerrada para purgar el reclamo.
