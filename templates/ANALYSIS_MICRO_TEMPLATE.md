# ANÁLISIS PROFUNDO QUIRÚRGICO: [ID_MICRO_PROBLEMA] - [TITULO]

**Identificador:** `[P01 / P02 / ...]`  
**Tarea Principal:** `[Nombre de la Tarea / Directorio]`  
**Fecha de Análisis:** `[YYYY-MM-DD]`  
**Estado:** `[BORRADOR / REVISADO / APROBADO]`  

---

## 1. DIAGNÓSTICO Y CAUSA RAÍZ
- **Descripción del Problema**: [Explicación técnica detallada de la limitación, bug o requerimiento a resolver].
- **Archivos y Líneas Clave**:
  - `[Ruta_Archivo_1#L10-L40]`: [Qué ocurre actualmente aquí].
  - `[Ruta_Archivo_2#L100-L125]`: [Qué ocurre actualmente aquí].
- **Comportamiento Actual vs Comportamiento Esperado**:
  - *Actual*: [Comportamiento defectuoso o ausente].
  - *Esperado*: [Comportamiento técnico esperado tras la solución].

---

## 2. ÁMBITO ESTRICTO DE ARCHIVOS
Lista exhaustiva y cerrada de archivos impactados. Prohibido tocar rutas fuera de esta lista:
- **Archivos a Modificar**:
  - `[Ruta exacta 1]`
- **Archivos a Crear**:
  - `[Ruta exacta 2]`
- **Archivos de Solo Lectura / Referencia**:
  - `[Ruta exacta 3]`

---

## 3. CASOS DE BORDE, REGRESIONES Y RIESGOS
- **Interacciones con otros módulos**: [Qué otros componentes o subsistemas consumen este código].
- **Casos de Falla / Entradas Anómalas**: [Valores nulos, buffers vacíos, tipos de datos incompatibles, etc.].
- **Plan de Mitigación**: [Cómo se blinda la implementación ante estos riesgos].

---

## 4. DISEÑO TÉCNICO DETALLADO (BLUEPRINT DE IMPLEMENTACIÓN)
*Especificación previa con lujo de detalle técnico antes de escribir código de producción.*

### A. Firmas, Variables y Contratos
- Variables o constantes a incorporar/modificar:
  ```text
  [Definición de variables, tipos o estructuras]
  ```

### B. Algoritmo o Pseudocódigo de Ejecución
```text
1. Paso 1: [Acción técnica precisa]
2. Paso 2: [Acción técnica precisa]
3. Paso 3: [Acción técnica precisa]
```

### C. Diff Conceptual / Cambios Exactos Proyectados
- Detalle de bloques de código específicos que se van a sustituir o incorporar.

---

## 5. COMANDO DE VERIFICACIÓN NATIVO
*Regla de Oro: Prohibido inventar scripts temporales en Python si el proyecto no lo usa.*

- **Comando Nativo**: `[COMANDO_EXACTO_DEL_STACK]` (ej. `npm test -- ...`, `pytest ...`, `cargo test`, compilador nativo, linter, o script de prueba en runtime).
- **Criterios de Éxito / Aceptación**:
  - [ ] Compilación / Análisis sintáctico con 0 errores y 0 warnings.
  - [ ] Salida limpia con código de retorno exitoso (`exit code 0`).
  - [ ] Verificación de contrato de datos o interfaz cumplido.

---

## 6. OBSERVACIONES PARA EL USUARIO
- [Notas relevantes sobre decisiones técnicas tomadas en este análisis para facilitar la revisión del usuario].
