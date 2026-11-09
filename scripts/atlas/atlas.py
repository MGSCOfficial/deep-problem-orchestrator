#!/usr/bin/env python3
"""
ATLAS v1.0 - Agent Task & Lock Arbitration System
Motor de mediación, estado atómico, grafo de dependencias y concurrencia para agentes IA.
"""

import argparse
import os
import sys
import json

# Asegurar importación de módulos internos de ATLAS
atlas_dir = os.path.dirname(os.path.abspath(__file__))
if atlas_dir not in sys.path:
    sys.path.insert(0, atlas_dir)

from core.formatters import emit_agent, emit_human
from core.state import StateManager
from core.dag import DAGResolver
from core.concurrency import ConcurrencyManager
from core.bus import AgentBus
from core.compiler import MarkdownCompiler


def get_workspace_root(override_path: str = None) -> str:
    if override_path and override_path.strip():
        return os.path.abspath(override_path.strip())
    # 1. Si el directorio actual tiene carpeta Engineering, es el workspace activo
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, "Engineering")):
        return os.path.abspath(cwd)
    # 2. Compatibilidad retroactiva con Chernobil Underground si atlas.py se invoca desde Gemini Workstation
    if "Gemini Workstation" in atlas_dir:
        return os.path.abspath(os.path.join(atlas_dir, "..", ".."))
    # 3. Fallback determinista al directorio de trabajo actual
    return os.path.abspath(cwd)


def cmd_init(args, workspace_root: str):
    agent_owner = args.agent or "AGENT-CORE"
    try:
        state = StateManager.init_task(workspace_root, args.task_name, agent_owner)
        if args.is_agent:
            emit_agent({
                "status": "INITIALIZED",
                "task_name": state["task_name"],
                "task_dir": state["task_dir"],
                "owner": state["agent_owner"]
            })
        else:
            emit_human(
                title=f"Tarea Inicializada: {state['task_name']}",
                message="Directorio y tablero 00_Inventory.md creados correctamente.",
                status="SUCCESS",
                details={
                    "Directorio": state["task_dir"],
                    "Agente Titular": state["agent_owner"],
                    "Fase": "0 (Triage)"
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e), "status": "FAIL"})
        else:
            emit_human("Error al inicializar tarea", str(e), status="ERROR")
        sys.exit(1)


def cmd_status(args, workspace_root: str):
    try:
        state = StateManager.load_active(workspace_root)
        if not state:
            if args.is_agent:
                emit_agent({"active_task": None, "status": "NO_ACTIVE_TASK"})
            else:
                emit_human("Sin Tarea Activa", "No se encontró ningún puntero en Engineering/Tasks/.atlas_active_task", status="WARNING")
            return

        if args.is_agent:
            micros_summary = {
                m_id: m["status"] for m_id, m in state.get("micros", {}).items()
            }
            emit_agent({
                "task": state["task_name"],
                "phase": state["phase"],
                "active_micro": state["active_micro"],
                "active_status": state["active_status"],
                "next_action": state["next_action"],
                "micros_count": len(state.get("micros", {})),
                "micros": micros_summary
            })
        else:
            emit_human(
                title=f"Estado de Tarea: {state['task_name']}",
                message=f"Puntero activo en Fase {state['phase']}",
                status="INFO",
                details={
                    "Micro en Curso": state["active_micro"],
                    "Estado Micro": state["active_status"],
                    "Próxima Acción": state["next_action"],
                    "Total Micros": len(state.get("micros", {}))
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al consultar estado", str(e), status="ERROR")
        sys.exit(1)


def cmd_add_micro(args, workspace_root: str):
    try:
        files = [f.strip() for f in args.files.split(",") if f.strip()] if args.files else []
        blocked_by = [b.strip().upper() for b in args.blocked_by.split(",") if b.strip()] if args.blocked_by else []
        
        state = StateManager.add_micro(
            workspace_root=workspace_root,
            micro_id=args.micro_id,
            title=args.title,
            files=files,
            blocked_by=blocked_by,
            slug=args.slug or "",
            verification=args.verify or ""
        )
        m_id = args.micro_id.upper().strip()
        if not m_id.startswith("P"):
            m_id = f"P{m_id}"

        if args.is_agent:
            emit_agent({
                "added": m_id,
                "title": args.title,
                "analysis_file": state["micros"][m_id]["analysis_file"],
                "total_micros": len(state["micros"])
            })
        else:
            emit_human(
                title=f"Micro-Problema Registrado: {m_id}",
                message=f"Tablero 00_Inventory.md sincronizado automáticamente.",
                status="SUCCESS",
                details={
                    "Título": args.title,
                    "Archivo de Análisis": state["micros"][m_id]["analysis_file"],
                    "Archivos": files or "Ninguno declarado"
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al agregar micro-problema", str(e), status="ERROR")
        sys.exit(1)


def cmd_update_micro(args, workspace_root: str):
    try:
        state = StateManager.update_micro(
            workspace_root=workspace_root,
            micro_id=args.micro_id,
            status=args.status,
            next_action=args.next or ""
        )
        m_id = args.micro_id.upper().strip()
        if not m_id.startswith("P"):
            m_id = f"P{m_id}"

        if args.is_agent:
            emit_agent({
                "updated": m_id,
                "new_status": state["micros"][m_id]["status"],
                "next_action": state["next_action"]
            })
        else:
            emit_human(
                title=f"Micro-Problema Actualizado: {m_id}",
                message=f"Estado avanzado a [{state['micros'][m_id]['status']}]",
                status="SUCCESS",
                details={
                    "Próxima Acción": state["next_action"]
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al actualizar micro-problema", str(e), status="ERROR")
        sys.exit(1)


def cmd_set_phase(args, workspace_root: str):
    try:
        state = StateManager.set_phase(
            workspace_root=workspace_root,
            phase=args.phase,
            next_action=args.next or ""
        )
        if args.is_agent:
            emit_agent({
                "phase": state["phase"],
                "next_action": state["next_action"]
            })
        else:
            emit_human(
                title=f"Fase de Tarea Actualizada",
                message=f"Avanzado a Fase {state['phase']}",
                status="SUCCESS"
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al cambiar fase", str(e), status="ERROR")
        sys.exit(1)


def cmd_resolve_dag(args, workspace_root: str):
    try:
        state = StateManager.load_active(workspace_root)
        if not state:
            raise RuntimeError("No hay tarea activa.")

        micros = state.get("micros", {})
        if not micros:
            raise RuntimeError("La tarea no tiene micro-problemas registrados.")

        order, cycles = DAGResolver.resolve_order(micros)
        if cycles:
            if args.is_agent:
                emit_agent({"error": "CYCLE_DETECTED", "cycles": cycles})
            else:
                emit_human("Ciclo Detectado en Dependencias (Deadlock)", f"Nodos en ciclo: {', '.join(cycles)}", status="ERROR")
            sys.exit(1)

        unblocked = DAGResolver.get_unblocked(micros)
        batches = DAGResolver.compute_execution_batches(micros)

        # Compilar y guardar Execution_Workflow.md automáticamente en el directorio de la tarea
        active_dir = StateManager.get_active_task_dir(workspace_root)
        workflow_md = MarkdownCompiler.compile_workflow(state, order, batches)
        workflow_path = os.path.join(active_dir, "Execution_Workflow.md")
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.write(workflow_md)

        # Actualizar fase a 2 si estaba en 1
        if state.get("phase", 0) < 2:
            StateManager.set_phase(workspace_root, 2, next_action=f"Iniciar ejecución quirúrgica de {order[0]}.")

        if args.is_agent:
            emit_agent({
                "dag_status": "RESOLVED",
                "order": order,
                "unblocked": unblocked,
                "batches": batches,
                "workflow_file": "Execution_Workflow.md"
            })
        else:
            emit_human(
                title="Grafo DAG Resuelto (Cero Ciclos)",
                message="Execution_Workflow.md generado automáticamente.",
                status="SUCCESS",
                details={
                    "Orden Topológico": " ➔ ".join(order),
                    "Desbloqueados Listos": ", ".join(unblocked) or "Ninguno",
                    "Capas de Paralelismo": len(batches)
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al resolver DAG", str(e), status="ERROR")
        sys.exit(1)


def cmd_lock(args, workspace_root: str):
    try:
        files = [f.strip() for f in args.files.split(",") if f.strip()]
        state = StateManager.load_active(workspace_root)
        task_dir = state["task_dir"] if state else "Engineering/"
        agent = args.agent or (state["agent_owner"] if state else "AGENT-CORE")
        level = args.level or "ANALIZANDO"
        reason = args.reason or ""

        res = ConcurrencyManager.acquire_lock(
            workspace_root=workspace_root,
            agent=agent,
            task_dir=task_dir,
            files=files,
            level=level,
            reason=reason
        )

        if not res.get("success"):
            if args.is_agent:
                emit_agent(res)
            else:
                emit_human(
                    title="Colisión de Locks Detectada",
                    message=f"El agente {res['details'].get('conflict_agent')} ya bloqueó este perímetro.",
                    status="ERROR",
                    details=res["details"]
                )
            sys.exit(1)

        if args.is_agent:
            emit_agent({
                "lock_status": "ACQUIRED",
                "agent": agent,
                "level": level,
                "files": files
            })
        else:
            emit_human(
                title=f"Lock Adquirido: {level}",
                message="Engineering/CONCURRENCY_BOARD.md actualizado.",
                status="LOCK",
                details={
                    "Agente": agent,
                    "Archivos": files
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al adquirir lock", str(e), status="ERROR")
        sys.exit(1)


def cmd_unlock(args, workspace_root: str):
    try:
        state = StateManager.load_active(workspace_root)
        agent = args.agent or (state["agent_owner"] if state else "AGENT-CORE")
        summary = args.summary or ""

        res = ConcurrencyManager.release_lock(
            workspace_root=workspace_root,
            agent=agent,
            summary=summary
        )

        if args.is_agent:
            emit_agent({
                "lock_status": "RELEASED",
                "agent": agent
            })
        else:
            emit_human(
                title=f"Locks Liberados: {agent}",
                message="Engineering/CONCURRENCY_BOARD.md marcado como 🟢 LIBERADO.",
                status="SUCCESS"
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al liberar locks", str(e), status="ERROR")
        sys.exit(1)


def cmd_delegate(args, workspace_root: str):
    try:
        contract_data = json.loads(args.contract) if args.contract else {}
        files = [f.strip() for f in args.files.split(",") if f.strip()] if args.files else []
        from_agent = args.from_agent or "AGENT-CALLER"

        res = AgentBus.delegate_micro(
            workspace_root=workspace_root,
            from_agent=from_agent,
            target_task_name_or_dir=args.to,
            micro_id=args.micro_id,
            title=args.title,
            files=files,
            contract=contract_data,
            description=args.desc or ""
        )

        if args.is_agent:
            emit_agent(res)
        else:
            emit_human(
                title=f"Tarea Delegada Exitosamente: {args.micro_id}",
                message=f"Generado {res['inbox_file']} en la tarea receptora.",
                status="SUCCESS",
                details={
                    "De": from_agent,
                    "Para": res["target_agent"],
                    "Requerimiento": args.title
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al delegar tarea", str(e), status="ERROR")
        sys.exit(1)


def cmd_render(args, workspace_root: str):
    try:
        state = StateManager.load_active(workspace_root)
        if not state:
            raise RuntimeError("No hay tarea activa.")
        active_dir = StateManager.get_active_task_dir(workspace_root)
        StateManager.save_task(active_dir, state)

        if args.is_agent:
            emit_agent({"status": "RENDERED", "file": "00_Inventory.md"})
        else:
            emit_human("Tablero Compilado", "00_Inventory.md actualizado con éxito.", status="SUCCESS")
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e)})
        else:
            emit_human("Error al compilar", str(e), status="ERROR")
        sys.exit(1)


def cmd_finish(args, workspace_root: str):
    summary = args.summary or ""
    try:
        state = StateManager.finish_task(workspace_root, summary)
        if args.is_agent:
            emit_agent({
                "status": "FINISHED",
                "task_name": state["task_name"],
                "task_dir": state["task_dir"],
                "phase": 4,
                "summary": summary
            })
        else:
            emit_human(
                title=f"Tarea Concluida: {state['task_name']}",
                message="Tarea certificada y archivada con éxito. Puntero activo liberado.",
                status="SUCCESS",
                details={
                    "Directorio": state["task_dir"],
                    "Fase": "4 (Completada)",
                    "Resumen": summary or "Certificación total"
                }
            )
    except Exception as e:
        if args.is_agent:
            emit_agent({"error": str(e), "status": "FAIL"})
        else:
            emit_human("Error al finalizar tarea", str(e), status="ERROR")
        sys.exit(1)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="ATLAS v1.0 - Agent Task & Lock Arbitration System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--agent", action="store_true", dest="is_agent", help="Emite telemetría compacta JSON de ultra-baja densidad")
    parser.add_argument("--workspace", "-w", type=str, default="", help="Ruta raíz del workspace (por defecto: directorio actual de trabajo o detectado)")
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = subparsers.add_parser("init", help="Inicializa una nueva tarea y genera 00_Inventory.md")
    p_init.add_argument("task_name", type=str, help="Nombre de la tarea (ej. 'GPU_Overhaul')")
    p_init.add_argument("--agent-name", type=str, dest="agent", default="", help="Indicativo canónico del agente titular")

    # status
    subparsers.add_parser("status", help="Consulta el puntero de estado activo de la tarea")

    # add-micro
    p_add = subparsers.add_parser("add-micro", help="Agrega un micro-problema al inventario")
    p_add.add_argument("micro_id", type=str, help="ID del micro-problema (ej. 'P01')")
    p_add.add_argument("--title", type=str, required=True, help="Título del micro-problema")
    p_add.add_argument("--files", type=str, default="", help="Archivos afectados separados por coma")
    p_add.add_argument("--blocked-by", type=str, default="", help="IDs bloqueantes separados por coma (ej. 'P01,P02')")
    p_add.add_argument("--slug", type=str, default="", help="Slug identificador para el nombre de archivo")
    p_add.add_argument("--verify", type=str, default="", help="Comando nativo de verificación")

    # update-micro
    p_upd = subparsers.add_parser("update-micro", help="Actualiza el estado de un micro-problema")
    p_upd.add_argument("micro_id", type=str, help="ID del micro-problema (ej. 'P01')")
    p_upd.add_argument("--status", type=str, required=True, help="Nuevo estado (ANALYZING, ANALYZED, EXECUTING, RESOLVED)")
    p_upd.add_argument("--next", type=str, default="", help="Descripción de la próxima acción al reanudar")

    # set-phase
    p_phase = subparsers.add_parser("set-phase", help="Actualiza la fase global de la tarea")
    p_phase.add_argument("phase", type=int, choices=[0, 1, 2, 3, 4], help="Número de fase (0..4)")
    p_phase.add_argument("--next", type=str, default="", help="Próxima acción")

    # resolve-dag
    subparsers.add_parser("resolve-dag", help="Resuelve el orden topológico y genera Execution_Workflow.md")

    # lock
    p_lock = subparsers.add_parser("lock", help="Adquiere o eleva un lock en CONCURRENCY_BOARD.md")
    p_lock.add_argument("files", type=str, help="Rutas de archivos a bloquear separadas por coma")
    p_lock.add_argument("--agent-name", type=str, dest="agent", default="", help="Indicativo del agente")
    p_lock.add_argument("--level", type=str, default="ANALIZANDO", choices=["ANALIZANDO", "MODIFICANDO"], help="Nivel de lock")
    p_lock.add_argument("--reason", type=str, default="", help="Motivo o fase del bloqueo")

    # unlock
    p_unlock = subparsers.add_parser("unlock", help="Libera todos los locks del agente")
    p_unlock.add_argument("--agent-name", type=str, dest="agent", default="", help="Indicativo del agente")
    p_unlock.add_argument("--summary", type=str, default="", help="Resumen del trabajo realizado")

    # delegate
    p_del = subparsers.add_parser("delegate", help="Delega un requerimiento técnico al Inbox de otra tarea")
    p_del.add_argument("--to", type=str, required=True, help="Directorio o nombre de la tarea destino")
    p_del.add_argument("--from-agent", type=str, required=True, help="Indicativo del agente emisor")
    p_del.add_argument("--micro-id", type=str, required=True, help="ID de la tarea delegada (ej. 'P0X-DEL')")
    p_del.add_argument("--title", type=str, required=True, help="Título del requerimiento")
    p_del.add_argument("--files", type=str, default="", help="Archivos afectados")
    p_del.add_argument("--contract", type=str, default="{}", help="Payload JSON con especificaciones y variables")
    p_del.add_argument("--desc", type=str, default="", help="Descripción del requerimiento")

    # render
    subparsers.add_parser("render", help="Recompila manualmente 00_Inventory.md")

    # finish
    p_finish = subparsers.add_parser("finish", help="Concluye y certifica la tarea activa, compila el inventario final y libera el puntero")
    p_finish.add_argument("--summary", type=str, default="", help="Resumen final de la certificación y entrega")

    args = parser.parse_args()
    workspace_root = get_workspace_root(args.workspace)

    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "add-micro": cmd_add_micro,
        "update-micro": cmd_update_micro,
        "set-phase": cmd_set_phase,
        "resolve-dag": cmd_resolve_dag,
        "lock": cmd_lock,
        "unlock": cmd_unlock,
        "delegate": cmd_delegate,
        "render": cmd_render,
        "finish": cmd_finish,
    }

    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args, workspace_root)


if __name__ == "__main__":
    main()
