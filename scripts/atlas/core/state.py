import os
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.compiler import MarkdownCompiler


class StateManager:
    """
    Gestor transaccional del estado de tareas para ATLAS.
    Mantiene el estado atómico en JSON y sincroniza automáticamente
    el tablero 00_Inventory.md para la lectura del operador humano.
    """

    POINTER_FILE = ".atlas_active_task"

    @classmethod
    def get_tasks_dir(cls, workspace_root: str) -> str:
        return os.path.join(workspace_root, "Engineering", "Tasks")

    @classmethod
    def get_active_task_dir(cls, workspace_root: str) -> Optional[str]:
        pointer_path = os.path.join(cls.get_tasks_dir(workspace_root), cls.POINTER_FILE)
        if os.path.exists(pointer_path):
            with open(pointer_path, "r", encoding="utf-8") as f:
                rel_dir = f.read().strip()
                full_dir = os.path.join(workspace_root, rel_dir)
                if os.path.isdir(full_dir):
                    return full_dir
        return None

    @classmethod
    def set_active_task_dir(cls, workspace_root: str, task_dir: str) -> None:
        tasks_dir = cls.get_tasks_dir(workspace_root)
        os.makedirs(tasks_dir, exist_ok=True)
        pointer_path = os.path.join(tasks_dir, cls.POINTER_FILE)
        rel_dir = os.path.relpath(task_dir, workspace_root)
        with open(pointer_path, "w", encoding="utf-8") as f:
            f.write(rel_dir.replace("\\", "/"))

    @classmethod
    def clear_active_task_dir(cls, workspace_root: str) -> None:
        pointer_path = os.path.join(cls.get_tasks_dir(workspace_root), cls.POINTER_FILE)
        if os.path.exists(pointer_path):
            os.remove(pointer_path)

    @classmethod
    def init_task(cls, workspace_root: str, task_name: str, agent_owner: str) -> Dict[str, Any]:
        """
        Inicializa una nueva tarea, creando el directorio y los archivos base.
        """
        today_prefix = datetime.now().strftime("%Y%m%d")
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', task_name).strip('_')
        
        if not clean_name.startswith(today_prefix):
            folder_name = f"{today_prefix}_{clean_name}"
        else:
            folder_name = clean_name

        tasks_dir = cls.get_tasks_dir(workspace_root)
        task_dir = os.path.join(tasks_dir, folder_name)
        os.makedirs(task_dir, exist_ok=True)

        rel_task_dir = os.path.relpath(task_dir, workspace_root).replace("\\", "/")
        now_iso = datetime.now().isoformat()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        state: Dict[str, Any] = {
            "schema_version": "1.0",
            "task_name": folder_name,
            "task_dir": rel_task_dir,
            "agent_owner": agent_owner,
            "created_at": now_iso,
            "updated_at": now_iso,
            "phase": 0,
            "active_micro": "-",
            "active_status": "PENDIENTE_TRIAGE",
            "next_action": "Descomponer la tarea en micro-problemas cohesivos (P01..PN).",
            "micros": {},
            "inbox": [],
            "history": [
                {
                    "timestamp": now_str,
                    "entry": f"Tarea inicializada por {agent_owner}. Modo Fase 0 activado."
                }
            ]
        }

        cls.save_task(task_dir, state)
        cls.set_active_task_dir(workspace_root, task_dir)
        return state

    @classmethod
    def load_active(cls, workspace_root: str) -> Optional[Dict[str, Any]]:
        active_dir = cls.get_active_task_dir(workspace_root)
        if active_dir:
            return cls.load_task(active_dir)
        return None

    @classmethod
    def load_task(cls, task_dir: str) -> Dict[str, Any]:
        state_file = os.path.join(task_dir, "atlas_state.json")
        if not os.path.exists(state_file):
            raise FileNotFoundError(f"No se encontró atlas_state.json en {task_dir}")
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def save_task(cls, task_dir: str, state: Dict[str, Any]) -> None:
        """
        Persiste el estado atómicamente y recompila 00_Inventory.md.
        """
        state["updated_at"] = datetime.now().isoformat()
        state_file = os.path.join(task_dir, "atlas_state.json")
        temp_state_file = state_file + ".tmp"

        with open(temp_state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        os.replace(temp_state_file, state_file)

        # Compilar 00_Inventory.md
        inventory_content = MarkdownCompiler.compile_inventory(state)
        inventory_path = os.path.join(task_dir, "00_Inventory.md")
        temp_inventory = inventory_path + ".tmp"
        with open(temp_inventory, "w", encoding="utf-8") as f:
            f.write(inventory_content)
        os.replace(temp_inventory, inventory_path)

    @classmethod
    def add_micro(
        cls,
        workspace_root: str,
        micro_id: str,
        title: str,
        files: List[str],
        blocked_by: List[str] = None,
        slug: str = "",
        verification: str = ""
    ) -> Dict[str, Any]:
        """
        Agrega un nuevo micro-problema al estado de la tarea activa.
        """
        active_dir = cls.get_active_task_dir(workspace_root)
        if not active_dir:
            raise RuntimeError("No hay una tarea activa en ATLAS. Ejecuta 'atlas init' primero.")

        state = cls.load_task(active_dir)
        m_id = micro_id.upper().strip()
        if not m_id.startswith("P"):
            m_id = f"P{m_id}"

        clean_slug = slug if slug else re.sub(r'[^a-zA-Z0-9_]', '_', title).strip('_')
        analysis_filename = f"Analysis_{m_id}_{clean_slug}.md"

        state["micros"][m_id] = {
            "id": m_id,
            "title": title,
            "slug": clean_slug,
            "files": files,
            "blocked_by": blocked_by or [],
            "status": "PENDIENTE_ANALISIS",
            "verification": verification,
            "analysis_file": analysis_filename
        }

        # Si es el primer micro o no había activo, marcarlo
        if state.get("active_micro") in ("-", "", None):
            state["active_micro"] = m_id
            state["active_status"] = "PENDIENTE_ANALISIS"
            state["next_action"] = f"Iniciar ciclo de análisis profundo para {m_id} ({analysis_filename})."

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        state["history"].append({
            "timestamp": now_str,
            "entry": f"Registrado {m_id}: {title} (Afecta: {', '.join(files) if files else 'N/A'})."
        })

        cls.save_task(active_dir, state)
        return state

    @classmethod
    def update_micro(
        cls,
        workspace_root: str,
        micro_id: str,
        status: str,
        next_action: str = ""
    ) -> Dict[str, Any]:
        """
        Actualiza el estado de un micro-problema.
        """
        active_dir = cls.get_active_task_dir(workspace_root)
        if not active_dir:
            raise RuntimeError("No hay una tarea activa en ATLAS.")

        state = cls.load_task(active_dir)
        m_id = micro_id.upper().strip()
        if not m_id.startswith("P"):
            m_id = f"P{m_id}"

        if m_id not in state["micros"]:
            raise KeyError(f"El micro-problema {m_id} no existe en la tarea activa.")

        raw_status = status.upper().strip()
        state["micros"][m_id]["status"] = raw_status
        state["active_micro"] = m_id
        state["active_status"] = raw_status

        if next_action:
            state["next_action"] = next_action
        else:
            if raw_status == "ANALYZED":
                state["next_action"] = f"Esperar aprobación del usuario para {m_id} o avanzar al siguiente análisis."
            elif raw_status == "RESOLVED":
                state["next_action"] = f"{m_id} resuelto y certificado. Consultar siguiente acción al usuario."

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        state["history"].append({
            "timestamp": now_str,
            "entry": f"Micro-problema {m_id} actualizado a [{raw_status}]."
        })

        cls.save_task(active_dir, state)
        return state

    @classmethod
    def set_phase(cls, workspace_root: str, phase: int, next_action: str = "") -> Dict[str, Any]:
        """
        Actualiza la fase global de la tarea.
        """
        active_dir = cls.get_active_task_dir(workspace_root)
        if not active_dir:
            raise RuntimeError("No hay una tarea activa en ATLAS.")

        state = cls.load_task(active_dir)
        state["phase"] = int(phase)
        if next_action:
            state["next_action"] = next_action

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        phase_label = MarkdownCompiler.PHASE_NAMES.get(phase, f"Fase {phase}")
        state["history"].append({
            "timestamp": now_str,
            "entry": f"Transición de estado: Tarea avanzada a [{phase_label}]."
        })

        cls.save_task(active_dir, state)
        return state

    @classmethod
    def finish_task(cls, workspace_root: str, summary: str = "") -> Dict[str, Any]:
        """
        Marca la tarea activa como Fase 4 (Completada), archiva el historial final,
        compila 00_Inventory.md y retira el puntero activo .atlas_active_task.
        """
        active_dir = cls.get_active_task_dir(workspace_root)
        if not active_dir:
            raise RuntimeError("No hay una tarea activa en ATLAS para finalizar.")

        state = cls.load_task(active_dir)
        state["phase"] = 4
        state["active_micro"] = "-"
        state["active_status"] = "COMPLETADO"
        state["next_action"] = "Tarea certificada y finalizada con éxito."

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = "Tarea finalizada y certificada al 100%."
        if summary:
            log_entry += f" Resumen: {summary}"
        state["history"].append({
            "timestamp": now_str,
            "entry": log_entry
        })

        # Guarda el estado final y compila el 00_Inventory.md definitivo
        cls.save_task(active_dir, state)

        # Retira el puntero de tarea activa para que 'atlas status' reporte NO_ACTIVE_TASK
        cls.clear_active_task_dir(workspace_root)

        return state
