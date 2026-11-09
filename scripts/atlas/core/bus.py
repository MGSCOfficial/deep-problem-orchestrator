import os
import re
import json
from datetime import datetime
from typing import Dict, Any, List
from core.state import StateManager
from core.concurrency import ConcurrencyManager


class AgentBus:
    """
    Bus de mensajería y delegación inter-agente de ATLAS.
    Permite transferir micro-problemas y contratos de datos atómicos entre sesiones
    y subagentes, generando automáticamente la vista en Inbox/ y actualizando el inventario.
    """

    @classmethod
    def delegate_micro(
        cls,
        workspace_root: str,
        from_agent: str,
        target_task_name_or_dir: str,
        micro_id: str,
        title: str,
        files: List[str],
        contract: Dict[str, Any],
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Transfiere un requerimiento técnico a otra tarea sin intercambio de párrafos en prosa.
        """
        # Resolver directorio destino
        if os.path.isabs(target_task_name_or_dir):
            target_dir = target_task_name_or_dir
        elif target_task_name_or_dir.startswith("Engineering"):
            target_dir = os.path.join(workspace_root, target_task_name_or_dir)
        else:
            target_dir = os.path.join(workspace_root, "Engineering", "Tasks", target_task_name_or_dir)

        if not os.path.isdir(target_dir):
            raise FileNotFoundError(f"El directorio de la tarea destino no existe: {target_dir}")

        target_state = StateManager.load_task(target_dir)
        target_agent = target_state.get("agent_owner", "AGENT-TITULAR")

        clean_micro = re.sub(r'[^a-zA-Z0-9_]', '_', micro_id).strip('_')
        clean_slug = re.sub(r'[^a-zA-Z0-9_]', '_', title).strip('_')
        inbox_dir = os.path.join(target_dir, "Inbox")
        os.makedirs(inbox_dir, exist_ok=True)

        delegated_filename = f"Delegated_Analysis_{clean_micro}_{clean_slug}.md"
        delegated_path = os.path.join(inbox_dir, delegated_filename)
        rel_inbox_path = f"Inbox/{delegated_filename}"

        # Compilar archivo Markdown legible para el humano en el Inbox
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        contract_json_str = json.dumps(contract, indent=2, ensure_ascii=False)
        files_str = "\n".join(f"- `{f}`" for f in files) if files else "- *(Sin archivos específicos)*"

        md_content = f"""# REQUERIMIENTO TÉCNICO DELEGADO: {micro_id} - {title}

**Agente Emisor:** `{from_agent}`  
**Agente Receptor (Titular):** `{target_agent}`  
**Fecha de Delegación:** `{now_str}`  
**Estado:** `[PENDIENTE_DE_ADOPCION]`  

---

## 1. DESCRIPCIÓN DEL REQUERIMIENTO
{description if description else "Requerimiento técnico transferido mediante bus de delegación ATLAS."}

## 2. ARCHIVOS IMPACTADOS
{files_str}

## 3. CONTRATO DE DATOS Y PARÁMETROS TÉCNICOS (JSON PAYLOAD)
```json
{contract_json_str}
```

---
*Este documento fue compilado automáticamente por el bus de mensajería ATLAS.*
"""
        with open(delegated_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Actualizar inbox en el estado de la tarea destino
        inbox_item = {
            "id": micro_id,
            "from_agent": from_agent,
            "title": title,
            "files": files,
            "contract": contract,
            "file_path": rel_inbox_path,
            "status": "PENDIENTE_ADOPCION",
            "delegated_at": now_str
        }

        target_state.setdefault("inbox", []).append(inbox_item)
        target_state["history"].append({
            "timestamp": now_str,
            "entry": f"Recibida tarea delegada [{micro_id}] desde {from_agent}: {title}."
        })

        StateManager.save_task(target_dir, target_state)

        # Emitir aviso al CONCURRENCY_BOARD global
        ConcurrencyManager.broadcast_notice(
            workspace_root=workspace_root,
            agent=from_agent,
            recipient=target_agent,
            message=f"Delegado requerimiento {micro_id} ({title}) en {rel_inbox_path}.",
            notice_type="HANDOFF_REQUEST"
        )

        return {
            "success": True,
            "micro_id": micro_id,
            "target_agent": target_agent,
            "inbox_file": rel_inbox_path
        }
