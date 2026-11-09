# PLANO DE TRABAJO DE SUBAGENTE DELEGADO (BLUEPRINT)

**Identificador de Tarea:** `[TASK-ID-O-SUBFASE]`  
**Rol del Subagente:** `[Ej. Core Engineer / Frontend Specialist / Protocol Architect]`  
**Agente Orquestador:** Master Orchestrator  
**Fecha / Versión:** `[YYYY-MM-DD / vX.Y]`  

---

## 1. OBJETIVO Y CONTEXTO
- **Propósito**: [Descripción precisa del entregable técnico a producir].
- **Archivos de Referencia**: [Rutas de archivos de consulta o documentación técnica relevante].

---

## 2. ÁMBITO ESTRICTO DE ARCHIVOS PERMITIDOS
El subagente tiene estrictamente restringida la escritura a las siguientes rutas:
- **Archivos a Crear**:
  - `[Ruta 1]`
- **Archivos a Modificar**:
  - `[Ruta 2]`
*(Queda terminantemente prohibido modificar cualquier otro archivo del proyecto sin aprobación del orquestador).*

---

## 3. FLUJO INTERNO DE EJECUCIÓN (PASO A PASO)
1. **Paso 1: Diagnóstico e Inspección**:
   - [Lectura quirúrgica de contratos y dependencias].
2. **Paso 2: Implementación**:
   - [Acción técnica específica aplicando estándares del repositorio].
3. **Paso 3: Verificación Nativa**:
   - [Ejecución del comando de prueba oficial o validación de sintaxis].

---

## 4. CONVENCIONES Y REGLAS ARQUITECTÓNICAS
- **Codificación y Formato**: UTF-8 sin BOM, saltos de línea coherentes (LF/CRLF según el repositorio).
- **Prohibición de Slop y Comprobadores Huérfanos**:
  - No generar archivos temporales ni scripts caseros de testing en Python.
  - Usar exclusivamente las herramientas nativas del proyecto.
- **Respeto a Convenciones del Proyecto**: Respetar patrones de diseño, nombres y estilos propios del repositorio activo.

---

## 5. COMANDO DE VERIFICACIÓN Y FORMATO DE REPORTE

### Comando Requerido:
`[COMANDO_EXACTO_NATIVO]` (ej. `npm test`, `pytest`, `cargo test`, `cate.py --delta`, compilador nativo).

### Formato Obligatorio de Retorno al Orquestador:
```markdown
### REPORTE DE SUBAGENTE: [ROL]
- **Archivos Modificados**: [Lista de rutas]
- **Comando de Verificación**: `[Comando ejecutado]`
- **Resultado**: [PASS (100%) / EXIT CODE 0 / Sin hallazgos]
- **Observaciones Técnicas**: [Detalles o notas críticas]
```
