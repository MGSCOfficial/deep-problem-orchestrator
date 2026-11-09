import os
from typing import Dict, Any, List


class MarkdownCompiler:
    """
    Compilador determinista de documentación Markdown para operadores humanos.
    Genera 00_Inventory.md y Execution_Workflow.md en milisegundos sin consumir
    un solo token del modelo de lenguaje.
    """

    PHASE_NAMES = {
        0: "FASE 0: TRIAGE E INVENTARIO INICIAL",
        1: "FASE 1: CICLO DE ANÁLISIS PROFUNDO",
        2: "FASE 2: ORQUESTACIÓN Y FLUJO DE DEPENDENCIAS",
        3: "FASE 3: CICLO DE EJECUCIÓN QUIRÚRGICA",
        4: "FASE 4: CERTIFICACIÓN Y TAREA COMPLETADA"
    }

    STATUS_BADGES = {
        "PENDING": "`PENDIENTE_ANALISIS`",
        "PENDIENTE": "`PENDIENTE_ANALISIS`",
        "ANALYZING": "`🟡 EN_ANALISIS`",
        "ANALYZED": "`🟢 ANALIZADO_APROBADO`",
        "EXECUTING": "`🔴 EN_EJECUCION`",
        "RESOLVED": "`✅ RESUELTO`",
        "RESUELTO": "`✅ RESUELTO`"
    }

    @classmethod
    def compile_inventory(cls, state: Dict[str, Any]) -> str:
        """
        Compila el contenido completo de 00_Inventory.md siguiendo la plantilla oficial.
        """
        task_name = state.get("task_name", "TAREA_SIN_NOMBRE")
        task_dir = state.get("task_dir", "")
        agent_owner = state.get("agent_owner", "AGENT-GENERAL")
        start_date = state.get("created_at", "")[:10]
        phase = state.get("phase", 0)
        phase_str = cls.PHASE_NAMES.get(phase, f"FASE {phase}")

        active_micro = state.get("active_micro", "-")
        active_status = state.get("active_status", "PENDIENTE")
        next_action = state.get("next_action", "Definir próximos micro-problemas.")

        lines = [
            "# TABLERO DE CONTROL Y REGISTRO DE TAREA (INVENTORY)",
            "",
            f"**Tarea:** `{task_name}`  ",
            f"**Directorio de Trabajo:** `{task_dir}/`  ",
            f"**Agente Titular:** `{agent_owner}`  ",
            f"**Fecha de Inicio:** `{start_date}`  ",
            f"**Estado General:** `[{phase_str}]`  ",
            "",
            "---",
            "",
            "## 1. PUNTERO DE ESTADO ACTIVO (CONTEXT-SWITCH ANCHOR)",
            "*Este bloque permite pausar la tarea, atender otras prioridades y reanudar sin pérdida de contexto.*",
            "",
            f"- **Fase Activa:** `[{phase_str}]`",
            f"- **Micro-Problema en Curso:** `[{active_micro}]`",
            f"- **Estado del Micro-Problema:** `[{active_status}]`",
            f"- **Próxima Acción al Reanudar:** `{next_action}`",
            "",
            "---",
            "",
            "## 2. INVENTARIO DE MICRO-PROBLEMAS",
            "",
            "| ID | Título del Micro-Problema | Archivo de Análisis | Estado | Verificación |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        micros = state.get("micros", {})
        if not micros:
            lines.append("| `-` | *(No hay micro-problemas registrados todavía)* | `-` | `PENDIENTE` | `-` |")
        else:
            for m_id, m_data in micros.items():
                title = m_data.get("title", f"Micro-problema {m_id}")
                slug = m_data.get("slug", m_id)
                analysis_file = m_data.get("analysis_file", f"Analysis_{m_id}_{slug}.md")
                raw_status = m_data.get("status", "PENDING").upper()
                badge = cls.STATUS_BADGES.get(raw_status, f"`{raw_status}`")
                verify_cmd = m_data.get("verification", "Verificación nativa")
                if not verify_cmd:
                    verify_cmd = "Verificación nativa"
                lines.append(f"| **{m_id}** | {title} | `{analysis_file}` | {badge} | `{verify_cmd}` |")

        lines.extend([
            "",
            "*(Estados válidos: `PENDIENTE_ANALISIS`, `EN_ANALISIS`, `ANALIZADO_APROBADO`, `EN_EJECUCION`, `RESUELTO`).*",
            "",
            "---",
            "",
            "## 3. BANDEJA DE TAREAS DELEGADAS (INBOX / CO-AUTHORING)",
            "*Micro-problemas adoptados desde otros agentes para edición unificada sin colisiones.*",
            "",
            "| ID Delegado | Agente Emisor | Título del Requerimiento | Archivo de Análisis Transferido | Estado de Adopción |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ])

        inbox = state.get("inbox", [])
        if not inbox:
            lines.append("| `-` | `-` | *(Bandeja vacía - Ninguna tarea delegada)* | `-` | `-` |")
        else:
            for item in inbox:
                del_id = item.get("id", "P0X-DEL")
                from_agent = item.get("from_agent", "AGENT-EXTERNO")
                title = item.get("title", "Requerimiento delegado")
                file_path = item.get("file_path", "Inbox/Delegated_xxx.md")
                status = item.get("status", "ADOPTED")
                lines.append(f"| `{del_id}` | `{from_agent}` | {title} | `{file_path}` | `[{status}]` |")

        lines.extend([
            "",
            "---",
            "",
            "## 4. HISTORIAL DE EJECUCIÓN CONSOLIDADO"
        ])

        history = state.get("history", [])
        if not history:
            lines.append("- *(Sin historial registrado todavía)*")
        else:
            for h in history:
                timestamp = h.get("timestamp", start_date)
                entry = h.get("entry", "")
                lines.append(f"- `[{timestamp}]` - {entry}")

        lines.append("")
        return "\n".join(lines)

    @classmethod
    def compile_workflow(cls, state: Dict[str, Any], order: List[str], batches: List[List[str]]) -> str:
        """
        Compila Execution_Workflow.md con el grafo de dependencias y orden topológico resuelto.
        """
        task_name = state.get("task_name", "TAREA")
        agent_owner = state.get("agent_owner", "AGENT-TITULAR")
        lines = [
            f"# MATRIZ DE DEPENDENCIAS Y FLUJO DE EJECUCIÓN (WORKFLOW)",
            "",
            f"**Tarea:** `{task_name}`  ",
            f"**Agente Titular:** `{agent_owner}`  ",
            f"**Resolución del Grafo:** `Algoritmo Topológico DAG (ATLAS Engine)`  ",
            "",
            "---",
            "",
            "## 1. ORDEN TOPOLÓGICO ÓPTIMO DE EJECUCIÓN",
            "",
            "El motor ATLAS ha resuelto las dependencias libres de ciclos. Este es el orden matemático de resolución:",
            ""
        ]

        micros = state.get("micros", {})
        for idx, m_id in enumerate(order, 1):
            m_data = micros.get(m_id, {})
            title = m_data.get("title", "")
            blockers = m_data.get("blocked_by", [])
            blockers_str = ", ".join(f"`{b}`" for b in blockers) if blockers else "*Ninguno (Raíz)*"
            lines.append(f"{idx}. **`{m_id}`** - {title} (Bloqueado por: {blockers_str})")

        lines.extend([
            "",
            "---",
            "",
            "## 2. LOTES DE EJECUCIÓN PARALELIZABLES (CAPAS)",
            ""
        ])

        for lvl, batch in enumerate(batches):
            batch_str = ", ".join(f"`{b}`" for b in batch)
            lines.append(f"- **Lote {lvl + 1} (Independientes entre sí)**: {batch_str}")

        lines.extend([
            "",
            "---",
            "",
            "## 3. PROTOCOLO DE EJECUCIÓN CON HARD STOP",
            "",
            "1. Se implementa exactamente **un micro-problema por turno** siguiendo el orden anterior.",
            "2. Al finalizar la implementación, se corre la verificación nativa oficial.",
            "3. Tras certificar con 0 errores, el agente ejecuta `atlas resolve-micro [ID]`.",
            "4. **HARD STOP OBLIGATORIO**: El agente se detiene, emite reporte conciso y espera orden humana.",
            ""
        ])

        return "\n".join(lines)
