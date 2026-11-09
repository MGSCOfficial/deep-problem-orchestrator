#!/usr/bin/env python3
"""
Suite de Pruebas Unitarias Hermética para ATLAS v1.0
Valida inicialización, DAG, máquina de estados, colisión de locks y compilación Markdown.
Ejecuta bajo sandbox y garantiza 100% inmutabilidad (limpieza total al finalizar).
"""

import os
import sys
import shutil
import tempfile
import unittest

# Importar módulos de ATLAS
atlas_dir = os.path.dirname(os.path.abspath(__file__))
if atlas_dir not in sys.path:
    sys.path.insert(0, atlas_dir)

from core.dag import DAGResolver
from core.state import StateManager
from core.compiler import MarkdownCompiler
from core.concurrency import ConcurrencyManager
from core.bus import AgentBus


class TestAtlasCore(unittest.TestCase):

    def setUp(self):
        # Crear un entorno temporal aislado (Sandbox)
        self.temp_dir = tempfile.mkdtemp(prefix="atlas_test_")
        self.engineering_dir = os.path.join(self.temp_dir, "Engineering")
        self.tasks_dir = os.path.join(self.engineering_dir, "Tasks")
        os.makedirs(self.tasks_dir, exist_ok=True)

        # Tablero base mínimo para pruebas
        self.board_path = os.path.join(self.engineering_dir, "CONCURRENCY_BOARD.md")
        base_board = """# TABLERO CENTRAL DE CONCURRENCIA
**Última Actualización Global:** `2026-10-23 20:00`

## 1. REGISTRO DE AGENTES ACTIVOS Y RECLAMO DE MÓDULOS (LOCKS)

| Indicativo del Agente | Tarea Activa / Directorio | Módulos Reclamados (Lock) | Estado del Semáforo | Última Actividad |
| :--- | :--- | :--- | :--- | :--- |
| `AGENT-EXISTENTE` | `Engineering/Tasks/Test/` | `Modules/GPU.bat` | `🔴 MODIFICANDO` | 2026-10-23 20:00 |

### Leyenda de Estados del Semáforo:
- `🟢 LIBERADO`: Tarea finalizada.

## 2. BUZÓN ASÍNCRONO DE MENSAJES Y DELEGACIÓN (INTER-AGENT BUS)
*Canal en disco para transferir requerimientos, notificar cambios de contratos o avisar liberaciones.*

- `[2026-10-23 20:00]` `[AVISO]`: Base.
"""
        with open(self.board_path, "w", encoding="utf-8") as f:
            f.write(base_board)

    def tearDown(self):
        # Limpieza absoluta del sandbox temporal
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_dag_resolution_and_cycle_detection(self):
        micros = {
            "P01": {"blocked_by": []},
            "P02": {"blocked_by": ["P01"]},
            "P03": {"blocked_by": ["P01"]},
            "P04": {"blocked_by": ["P02", "P03"]}
        }
        order, cycles = DAGResolver.resolve_order(micros)
        self.assertEqual(cycles, [])
        self.assertEqual(order[0], "P01")
        self.assertEqual(order[-1], "P04")

        # Batches
        batches = DAGResolver.compute_execution_batches(micros)
        self.assertEqual(len(batches), 3)
        self.assertEqual(batches[0], ["P01"])
        self.assertCountEqual(batches[1], ["P02", "P03"])
        self.assertEqual(batches[2], ["P04"])

        # Ciclo
        cyclic_micros = {
            "P01": {"blocked_by": ["P02"]},
            "P02": {"blocked_by": ["P01"]}
        }
        c_order, c_cycles = DAGResolver.resolve_order(cyclic_micros)
        self.assertEqual(c_order, [])
        self.assertTrue(len(c_cycles) > 0)

    def test_task_lifecycle_and_markdown_compiler(self):
        # 1. Init
        state = StateManager.init_task(self.temp_dir, "Test_Optimization", "AGENT-TEST-01")
        task_dir = os.path.join(self.temp_dir, state["task_dir"])
        self.assertTrue(os.path.isdir(task_dir))
        self.assertTrue(os.path.exists(os.path.join(task_dir, "00_Inventory.md")))
        self.assertTrue(os.path.exists(os.path.join(task_dir, "atlas_state.json")))

        # 2. Add Micros
        StateManager.add_micro(
            workspace_root=self.temp_dir,
            micro_id="P01",
            title="Sonda de memoria",
            files=["Subroutines/MemProbe.bat"],
            blocked_by=[],
            verification="cate --suite 1"
        )
        StateManager.add_micro(
            workspace_root=self.temp_dir,
            micro_id="P02",
            title="Alineación de buffer",
            files=["Subroutines/Buffer.bat"],
            blocked_by=["P01"],
            verification="cate --suite 2"
        )

        loaded = StateManager.load_active(self.temp_dir)
        self.assertIn("P01", loaded["micros"])
        self.assertIn("P02", loaded["micros"])

        # Verificar contenido de 00_Inventory.md generado
        with open(os.path.join(task_dir, "00_Inventory.md"), "r", encoding="utf-8") as f:
            inv_text = f.read()
        self.assertIn("Sonda de memoria", inv_text)
        self.assertIn("Analysis_P01_Sonda_de_memoria.md", inv_text)

        # 3. Update Micro
        StateManager.update_micro(self.temp_dir, "P01", "RESOLVED")
        loaded_after = StateManager.load_active(self.temp_dir)
        self.assertEqual(loaded_after["micros"]["P01"]["status"], "RESOLVED")

    def test_concurrency_lock_and_collision_detection(self):
        # Colisión esperada: AGENT-NUEVO intenta bloquear Modules/GPU.bat que está en MODIFICANDO por AGENT-EXISTENTE
        collision = ConcurrencyManager.check_collision(
            workspace_root=self.temp_dir,
            requested_files=["Modules/GPU.bat"],
            requesting_agent="AGENT-NUEVO"
        )
        self.assertTrue(collision["has_collision"])
        self.assertEqual(collision["conflict_agent"], "AGENT-EXISTENTE")

        # Archivo libre: Subroutines/Audio.bat
        collision_free = ConcurrencyManager.check_collision(
            workspace_root=self.temp_dir,
            requested_files=["Subroutines/Audio.bat"],
            requesting_agent="AGENT-NUEVO"
        )
        self.assertFalse(collision_free["has_collision"])

        # Adquirir lock legítimo
        res = ConcurrencyManager.acquire_lock(
            workspace_root=self.temp_dir,
            agent="AGENT-NUEVO",
            task_dir="Engineering/Tasks/Test_New/",
            files=["Subroutines/Audio.bat"],
            level="ANALIZANDO",
            reason="Auditoría de latencia"
        )
        self.assertTrue(res["success"])

        # Verificar que el tablero fue actualizado
        board_text = ConcurrencyManager.read_board(self.temp_dir)
        self.assertIn("AGENT-NUEVO", board_text)
        self.assertIn("🟡 ANALIZANDO", board_text)

        # Liberar lock
        rel_res = ConcurrencyManager.release_lock(
            workspace_root=self.temp_dir,
            agent="AGENT-NUEVO",
            summary="Auditoría completada."
        )
        self.assertTrue(rel_res["success"])
        board_after_rel = ConcurrencyManager.read_board(self.temp_dir)
        self.assertIn("🟢 LIBERADO", board_after_rel)

    def test_inter_agent_delegation_bus(self):
        # Crear tarea receptora
        state = StateManager.init_task(self.temp_dir, "Target_Task", "AGENT-TARGET")
        target_dir = os.path.join(self.temp_dir, state["task_dir"])

        # Delegar micro desde AGENT-SENDER
        res = AgentBus.delegate_micro(
            workspace_root=self.temp_dir,
            from_agent="AGENT-SENDER",
            target_task_name_or_dir=target_dir,
            micro_id="P09-DEL",
            title="Optimizar TDR delay",
            files=["Modules/GPU.bat"],
            contract={"reg_key": "TdrDelay", "val": 8},
            description="Ajuste requerido para prevenir cuelgues."
        )
        self.assertTrue(res["success"])
        self.assertTrue(os.path.exists(os.path.join(target_dir, "Inbox", "Delegated_Analysis_P09_DEL_Optimizar_TDR_delay.md")))

        # Verificar que 00_Inventory.md de la tarea receptora tiene la tarea delegada en la Sección 3
        with open(os.path.join(target_dir, "00_Inventory.md"), "r", encoding="utf-8") as f:
            inv_text = f.read()
        self.assertIn("P09-DEL", inv_text)
        self.assertIn("AGENT-SENDER", inv_text)

    def test_cli_end_to_end_flow(self):
        import subprocess
        import json

        atlas_cli = os.path.join(atlas_dir, "atlas.py")

        # 1. Init vía CLI --agent
        cmd_init = [sys.executable, atlas_cli, "--agent", "init", "CLI_Test_Flow", "--agent-name", "AGENT-CLI-TEST"]
        p = subprocess.run(cmd_init, cwd=self.temp_dir, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        data = json.loads(p.stdout.strip())
        self.assertEqual(data["status"], "INITIALIZED")

        # 2. Add-Micro vía CLI --agent
        cmd_add = [
            sys.executable, atlas_cli, "--agent", "add-micro", "P01",
            "--title", "Sonda CLI", "--files", "Subroutines/Test.bat", "--verify", "cate --suite 01"
        ]
        p = subprocess.run(cmd_add, cwd=self.temp_dir, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        add_data = json.loads(p.stdout.strip())
        self.assertEqual(add_data["added"], "P01")

        # 3. Status vía CLI --agent
        cmd_status = [sys.executable, atlas_cli, "--agent", "status"]
        p = subprocess.run(cmd_status, cwd=self.temp_dir, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        status_data = json.loads(p.stdout.strip())
        self.assertEqual(status_data["active_micro"], "P01")
        self.assertEqual(status_data["phase"], 0)

        # 4. Update-micro
        cmd_upd = [sys.executable, atlas_cli, "--agent", "update-micro", "P01", "--status", "RESOLVED"]
        p = subprocess.run(cmd_upd, cwd=self.temp_dir, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        upd_data = json.loads(p.stdout.strip())
        self.assertEqual(upd_data["new_status"], "RESOLVED")

        # 5. Resolve-DAG
        cmd_dag = [sys.executable, atlas_cli, "--agent", "resolve-dag"]
        p = subprocess.run(cmd_dag, cwd=self.temp_dir, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        dag_data = json.loads(p.stdout.strip())
        self.assertEqual(dag_data["dag_status"], "RESOLVED")
        self.assertEqual(dag_data["order"], ["P01"])

        # 6. Finish vía CLI --agent
        cmd_finish = [sys.executable, atlas_cli, "--agent", "finish", "--summary", "Prueba de cierre"]
        p = subprocess.run(cmd_finish, cwd=self.temp_dir, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        fin_data = json.loads(p.stdout.strip())
        self.assertEqual(fin_data["status"], "FINISHED")
        self.assertEqual(fin_data["phase"], 4)

        # 7. Status post-finish debe reportar NO_ACTIVE_TASK
        p = subprocess.run(cmd_status, cwd=self.temp_dir, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        post_status = json.loads(p.stdout.strip())
        self.assertEqual(post_status["status"], "NO_ACTIVE_TASK")


if __name__ == "__main__":
    unittest.main()
