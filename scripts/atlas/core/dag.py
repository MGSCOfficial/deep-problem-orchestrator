from graphlib import TopologicalSorter, CycleError
from typing import Dict, List, Set, Tuple, Any


class DAGResolver:
    """
    Motor matemático de grafo acíclico dirigido (DAG) para orquestación de tareas.
    Resuelve el orden topológico de dependencias, detecta ciclos (deadlocks)
    y calcula lotes de ejecución óptimos en milisegundos.
    """

    @staticmethod
    def resolve_order(micros: Dict[str, Dict[str, Any]]) -> Tuple[List[str], List[str]]:
        """
        Resuelve el orden topológico óptimo de ejecución.
        Retorna (orden_topologico, nodos_en_ciclo).
        Si hay ciclos, la lista de orden estará vacía y la de ciclos contendrá los nodos conflictivos.
        """
        graph: Dict[str, Set[str]] = {}
        for m_id, data in micros.items():
            blockers = set(data.get("blocked_by", []))
            # Filtrar bloqueantes que realmente existan en los micro-problemas
            valid_blockers = {b for b in blockers if b in micros}
            graph[m_id] = valid_blockers

        ts = TopologicalSorter(graph)
        try:
            order = list(ts.static_order())
            return order, []
        except CycleError as e:
            cycle_nodes = list(e.args[1]) if len(e.args) > 1 else []
            return [], cycle_nodes

    @staticmethod
    def get_unblocked(micros: Dict[str, Dict[str, Any]], completed_statuses: Set[str] = None) -> List[str]:
        """
        Retorna la lista de micro-problemas cuyas dependencias ya han sido completamente resueltas.
        """
        if completed_statuses is None:
            completed_statuses = {"RESOLVED", "RESUELTO"}

        unblocked = []
        for m_id, data in micros.items():
            current_status = data.get("status", "PENDING").upper()
            if current_status in completed_statuses:
                continue

            blockers = data.get("blocked_by", [])
            all_resolved = True
            for b in blockers:
                if b in micros:
                    b_status = micros[b].get("status", "PENDING").upper()
                    if b_status not in completed_statuses:
                        all_resolved = False
                        break
            if all_resolved:
                unblocked.append(m_id)

        return unblocked

    @staticmethod
    def compute_execution_batches(micros: Dict[str, Dict[str, Any]]) -> List[List[str]]:
        """
        Agrupa los micro-problemas en capas/lotes secuenciales (niveles de profundidad).
        Todos los problemas dentro de un lote son independientes entre sí y pueden
        ejecutarse en paralelo o en cualquier orden sin interferencia.
        """
        order, cycles = DAGResolver.resolve_order(micros)
        if cycles or not order:
            return []

        levels: Dict[str, int] = {}
        for m_id in order:
            blockers = [b for b in micros[m_id].get("blocked_by", []) if b in micros]
            if not blockers:
                levels[m_id] = 0
            else:
                levels[m_id] = max(levels[b] for b in blockers) + 1

        max_level = max(levels.values()) if levels else -1
        batches: List[List[str]] = []
        for lvl in range(max_level + 1):
            batch = [m_id for m_id, l in levels.items() if l == lvl]
            batches.append(batch)

        return batches
