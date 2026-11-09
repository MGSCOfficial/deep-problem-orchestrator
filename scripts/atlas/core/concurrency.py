import os
import re
from datetime import datetime
from typing import Dict, Any, List, Optional


class ConcurrencyManager:
    """
    Gestor atómico de concurrencia y semáforos para ATLAS.
    Lee, audita y actualiza Engineering/CONCURRENCY_BOARD.md sin errores de formato,
    garantizando cero colisiones destructivas entre múltiples sesiones o agentes.
    """

    BOARD_REL_PATH = os.path.join("Engineering", "CONCURRENCY_BOARD.md")

    SEMAPHORES = {
        "LIBERADO": "🟢 LIBERADO",
        "RELEASED": "🟢 LIBERADO",
        "FREE": "🟢 LIBERADO",
        "ANALIZANDO": "🟡 ANALIZANDO",
        "ANALYZING": "🟡 ANALIZANDO",
        "MODIFICANDO": "🔴 MODIFICANDO",
        "MODIFYING": "🔴 MODIFICANDO",
        "EN_ESPERA_COLA": "⏳ EN_ESPERA_COLA",
        "QUEUED": "⏳ EN_ESPERA_COLA",
        "DELEGADO": "🤝 DELEGADO",
        "DELEGATED": "🤝 DELEGADO"
    }

    @classmethod
    def get_board_path(cls, workspace_root: str) -> str:
        return os.path.join(workspace_root, cls.BOARD_REL_PATH)

    @classmethod
    def read_board(cls, workspace_root: str) -> str:
        path = cls.get_board_path(workspace_root)
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el tablero en {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def write_board(cls, workspace_root: str, content: str) -> None:
        path = cls.get_board_path(workspace_root)
        temp_path = path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(temp_path, path)

    @classmethod
    def parse_locks(cls, workspace_root: str) -> List[Dict[str, Any]]:
        """
        Parsea la tabla de locks de CONCURRENCY_BOARD.md.
        """
        content = cls.read_board(workspace_root)
        locks = []
        table_match = re.search(
            r'## 1\. REGISTRO DE AGENTES ACTIVOS.*?\n\n(.*?)\n\n### Leyenda',
            content,
            re.DOTALL
        )
        if not table_match:
            return locks

        lines = table_match.group(1).strip().splitlines()
        for line in lines[2:]:  # Omitir header y separador |---|
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 5:
                agent = cols[0].strip("` ")
                task_dir = cols[1].strip("` ")
                modules = cols[2].strip("` ")
                status = cols[3].strip("` ")
                last_act = cols[4].strip("` ")
                locks.append({
                    "agent": agent,
                    "task_dir": task_dir,
                    "modules": modules,
                    "status": status,
                    "last_act": last_act
                })
        return locks

    @classmethod
    def check_collision(
        cls,
        workspace_root: str,
        requested_files: List[str],
        requesting_agent: str
    ) -> Dict[str, Any]:
        """
        Evalúa si alguno de los archivos solicitados está bloqueado por otro agente.
        """
        active_locks = cls.parse_locks(workspace_root)
        normalized_requested = {f.replace("\\", "/").lower() for f in requested_files}

        for lock in active_locks:
            owner = lock["agent"]
            if owner.upper() == requesting_agent.upper():
                continue  # Es el mismo agente

            status = lock["status"]
            # Solo MODIFICANDO o ANALIZANDO constituyen bloqueo
            if "MODIFICANDO" in status or "ANALIZANDO" in status:
                raw_modules = lock["modules"]
                if raw_modules in ("-", "N/A", ""):
                    continue
                locked_modules = [m.strip("` ").replace("\\", "/").lower() for m in raw_modules.split(",")]
                
                conflicts = []
                for req in normalized_requested:
                    for locked in locked_modules:
                        if req == locked or req.startswith(locked + "/") or locked.startswith(req + "/"):
                            conflicts.append(req)

                if conflicts:
                    return {
                        "has_collision": True,
                        "conflict_agent": owner,
                        "conflict_status": status,
                        "conflict_files": conflicts,
                        "task_dir": lock["task_dir"]
                    }

        return {"has_collision": False}

    @classmethod
    def acquire_lock(
        cls,
        workspace_root: str,
        agent: str,
        task_dir: str,
        files: List[str],
        level: str = "ANALIZANDO",
        reason: str = ""
    ) -> Dict[str, Any]:
        """
        Adquiere o eleva un lock en el tablero central de forma atómica.
        """
        collision = cls.check_collision(workspace_root, files, agent)
        if collision["has_collision"]:
            return {
                "success": False,
                "error": "COLLISION_DETECTED",
                "details": collision
            }

        content = cls.read_board(workspace_root)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        now_date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        clean_level = level.upper()
        semaphore = cls.SEMAPHORES.get(clean_level, f"`{clean_level}`")
        files_str = ", ".join(f"`{f}`" for f in files) if files else "`-`"
        rel_task = task_dir.replace("\\", "/")
        if not rel_task.endswith("/"):
            rel_task += "/"

        # Buscar si el agente ya tiene fila en la tabla
        agent_pattern = rf"\| `?{re.escape(agent)}`? \|.*?\n"
        new_row = f"| `{agent}` | `{rel_task}` | {files_str} | `{semaphore}` | {now_str} |\n"

        if re.search(agent_pattern, content):
            content = re.sub(agent_pattern, new_row, content)
        else:
            # Insertar antes de la leyenda
            legend_pos = content.find("### Leyenda de Estados")
            if legend_pos != -1:
                content = content[:legend_pos] + new_row + "\n" + content[legend_pos:]
            else:
                content += new_row

        # Agregar aviso en Sección 2 Buzón
        bus_marker = "## 2. BUZÓN ASÍNCRONO DE MENSAJES Y DELEGACIÓN (INTER-AGENT BUS)\n*Canal en disco para transferir requerimientos, notificar cambios de contratos o avisar liberaciones.*\n\n"
        log_entry = f"- `[{now_date_str}]` `[LOCK_ACQUIRE]` `[{agent} -> TODOS]`: Semáforo elevado a {clean_level}. Perímetro: {files_str}. {reason}\n"
        
        bus_pos = content.find(bus_marker)
        if bus_pos != -1:
            insert_point = bus_pos + len(bus_marker)
            content = content[:insert_point] + log_entry + content[insert_point:]
        else:
            content += f"\n{log_entry}"

        # Actualizar fecha de actualización global
        content = re.sub(
            r'\*\*Última Actualización Global:\*\* `.*?`',
            f'**Última Actualización Global:** `{now_str}`',
            content
        )

        cls.write_board(workspace_root, content)
        return {
            "success": True,
            "agent": agent,
            "status": clean_level,
            "files": files
        }

    @classmethod
    def release_lock(
        cls,
        workspace_root: str,
        agent: str,
        summary: str = ""
    ) -> Dict[str, Any]:
        """
        Libera completamente los locks del agente en el tablero central.
        """
        content = cls.read_board(workspace_root)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        agent_pattern = rf"(\| `?{re.escape(agent)}`? \| `?.*?`? \|).*?(\| `?.*?`? \|).*?\n"

        # Reemplazar módulos por `-` y estado por `🟢 LIBERADO`
        def repl(match):
            return f"{match.group(1)} `-` | `🟢 LIBERADO` | {now_str} |\n"

        if re.search(agent_pattern, content):
            content = re.sub(agent_pattern, repl, content)

        # Agregar aviso de liberación en Buzón
        bus_marker = "## 2. BUZÓN ASÍNCRONO DE MENSAJES Y DELEGACIÓN (INTER-AGENT BUS)\n*Canal en disco para transferir requerimientos, notificar cambios de contratos o avisar liberaciones.*\n\n"
        reason_text = summary if summary else "Tarea certificada y finalizada."
        log_entry = f"- `[{now_str}]` `[LOCK_RELEASE]` `[{agent} -> TODOS]`: {reason_text} Módulos completamente liberados.\n"

        bus_pos = content.find(bus_marker)
        if bus_pos != -1:
            insert_point = bus_pos + len(bus_marker)
            content = content[:insert_point] + log_entry + content[insert_point:]
        else:
            content += f"\n{log_entry}"

        content = re.sub(
            r'\*\*Última Actualización Global:\*\* `.*?`',
            f'**Última Actualización Global:** `{now_str}`',
            content
        )

        cls.write_board(workspace_root, content)
        return {
            "success": True,
            "agent": agent,
            "status": "LIBERADO"
        }

    @classmethod
    def broadcast_notice(
        cls,
        workspace_root: str,
        agent: str,
        recipient: str,
        message: str,
        notice_type: str = "AVISO"
    ) -> None:
        """
        Emite un aviso estructurado al buzón global del tablero.
        """
        content = cls.read_board(workspace_root)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        bus_marker = "## 2. BUZÓN ASÍNCRONO DE MENSAJES Y DELEGACIÓN (INTER-AGENT BUS)\n*Canal en disco para transferir requerimientos, notificar cambios de contratos o avisar liberaciones.*\n\n"
        log_entry = f"- `[{now_str}]` `[{notice_type.upper()}]` `[{agent} -> {recipient}]`: {message}\n"

        bus_pos = content.find(bus_marker)
        if bus_pos != -1:
            insert_point = bus_pos + len(bus_marker)
            content = content[:insert_point] + log_entry + content[insert_point:]
        else:
            content += f"\n{log_entry}"

        cls.write_board(workspace_root, content)
