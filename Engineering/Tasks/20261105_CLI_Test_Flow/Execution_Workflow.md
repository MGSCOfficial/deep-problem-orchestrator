# MATRIZ DE DEPENDENCIAS Y FLUJO DE EJECUCIÓN (WORKFLOW)

**Tarea:** `20261105_CLI_Test_Flow`  
**Agente Titular:** `AGENT-CLI-TEST`  
**Resolución del Grafo:** `Algoritmo Topológico DAG (ATLAS Engine)`  

---

## 1. ORDEN TOPOLÓGICO ÓPTIMO DE EJECUCIÓN

El motor ATLAS ha resuelto las dependencias libres de ciclos. Este es el orden matemático de resolución:

1. **`P01`** - Sonda CLI (Bloqueado por: *Ninguno (Raíz)*)

---

## 2. LOTES DE EJECUCIÓN PARALELIZABLES (CAPAS)

- **Lote 1 (Independientes entre sí)**: `P01`

---

## 3. PROTOCOLO DE EJECUCIÓN CON HARD STOP

1. Se implementa exactamente **un micro-problema por turno** siguiendo el orden anterior.
2. Al finalizar la implementación, se corre la verificación nativa oficial.
3. Tras certificar con 0 errores, el agente ejecuta `atlas resolve-micro [ID]`.
4. **HARD STOP OBLIGATORIO**: El agente se detiene, emite reporte conciso y espera orden humana.
