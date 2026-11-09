# COMPUERTAS DE CERTIFICACIÓN DE TRES CAPAS (QUALITY GATES)

Esta guía define el estándar de certificación de tres capas aplicable a cualquier proyecto, garantizando máxima robustez técnica, prevención de regresiones y **cero derroche de tokens** por artefactos de prueba inventados.

---

## 1. LAS TRES CAPAS DE VALIDACIÓN UNIVERSAL

```text
┌────────────────────────────────────────────────────────┐
│                        CAPA 1                          │
│               Linter y Análisis Estático               │
│  - Sintaxis estricta, tipos, comillas y directivas     │
│  - Codificación UTF-8 y saltos de línea consistentes   │
│  - Criterio de Pase: 0 HALLAZGOS (100% Conforme)       │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                        CAPA 2                          │
│      Verificación Funcional en Stack Nativo            │
│  - Ejecución con arnés oficial preexistente            │
│  - Validación estática/humo nativa si no hay arnés     │
│  - ¡PROHIBIDO crear comprobadores caseros en Python!   │
│  - Criterio de Pase: 100% PASS (0 Fallos)              │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                        CAPA 3                          │
│         Trazabilidad, Versionado y Changelogs          │
│  - Incremento determinista de estampa de versión       │
│  - Registro en CHANGELOG bajo taxonomía estricta       │
│  - Criterio de Pase: Sincronización Total Verificada   │
└────────────────────────────────────────────────────────┘
```

---

## 2. CAPA 1: AUDITORÍA ESTÁTICA Y LINTERS NATIVOS

- **Objetivo**: Detectar errores de tipografía, tipos, variables sin declarar, comillas faltantes o violaciones de formato antes de ejecutar el código.
- **Herramientas por Stack**:
  - **TypeScript / JavaScript**: `eslint`, `biome`, `tsc --noEmit`.
  - **Python**: `ruff check`, `flake8`, `mypy`.
  - **Rust / Go**: `cargo clippy`, `go vet`.
  - **Batch / PowerShell**: Linters estáticos locales (ej. `batch-power-validator`), `pwsh -Command "[ScriptBlock]::Create(...)"`.
  - **C / C++**: `clang-tidy`, `cppcheck`, flags `-Wall -Wextra -Werror`.
- **Regla Inmutable**: Cero tolerancia a advertencias o errores en los archivos modificados.

---

## 3. CAPA 2: VERIFICACIÓN FUNCIONAL Y EL ANTI-PATRÓN DE "COMPROBADORES PYTHON"

### ⚠️ Regla de Oro Anti-Alucinación (Anti-CATE Hallucination)
CATE (Chernobil Agent Test Engine) es un arnés específico y propietario diseñado exclusivamente para el proyecto **Chernobil Underground** (`Gemini Workstation\CATE\cate.py`).

**QUEDA TERMINANTEMENTE PROHIBIDO**:
1. Inventar, generar o escribir archivos `.py` ad-hoc (ej. `test_check.py`, `verify.py`, scripts temporales de mock) en otros proyectos para "imitar a CATE" o simular que se corre una suite de pruebas automatizadas.
2. Gastar turnos y tokens de contexto creando y luego depurando scripts en Python que no forman parte de la arquitectura del repositorio del usuario.
3. Forzar pruebas unitarias automatizadas de caja negra inventadas cuando el proyecto carece de una suite oficial configurada.

### Protocolo de Verificación Funcional según la Realidad del Proyecto:

#### Escenario A: El proyecto TIENE un arnés de pruebas oficial configurado
- Ejecutar el comando oficial del repositorio:
  - Node/TS: `npm test`, `pnpm test`, `npx vitest run [ruta]`, `npx jest [ruta]`.
  - Python: `pytest tests/test_xxx.py` o `python -m unittest`.
  - Rust: `cargo test -- [filtro]`.
  - Go: `go test -v ./[paquete]`.
  - Chernobil Underground: `python "Gemini Workstation\CATE\cate.py" --delta --agent`.
- **Criterio de Pase**: 100% PASS sobre las suites afectadas.

#### Escenario B: El proyecto NO TIENE un arnés de pruebas configurado
- **NO crear un framework de pruebas casero**.
- Aplicar **Verificación Nativa en 3 Pasos**:
  1. **Validación de Compilación / Carga**:
     - Node: `node --check <archivo.js>`
     - Python: `python -m py_compile <archivo.py>`
     - Shell: `bash -n <script.sh>`
     - Batch: Comprobación sintáctica con `batch-power-validator` o subproceso de carga.
  2. **Prueba de Humo No Destructiva (Smoke Test)**:
     - Invocar el módulo/comando con flags no destructivos (`--help`, `--version`, flag de simulación o dry-run).
     - Si es una subrutina o función pura, invocarla directamente con parámetros de prueba temporales en su propio entorno nativo.
  3. **Inspección de Diferenciales y Contratos**:
     - Auditar el diff con `git diff` para certificar que cumple exactamente los contratos definidos.

---

## 4. CAPA 3: VERSIONADO Y REGISTRO EN CHANGELOGS

- **Objetivo**: Garantizar trazabilidad absoluta del ciclo de vida del software.
- **Reglas Operativas**:
  1. **Sincronización de Versión**:
     - En proyectos con versionado híbrido (CalVer / SemVer), incrementar la estampa correspondiente según las directrices del proyecto.
  2. **Taxonomía Semántica Obligatoria**:
     - `[AÑADIDO]`: Nuevas características, endpoints o módulos.
     - `[OPTIMIZADO]`: Refactorizaciones de rendimiento, poda de memoria o simplificación de algoritmos.
     - `[CORREGIDO]`: Solución de errores, parches y corrección de comportamientos anómalos.
     - `[CAMBIADO]`: Modificaciones de comportamiento preexistente o contratos de API.
     - `[ELIMINADO]`: Componentes o funciones obsoletas extirpadas.
     - `[SEGURIDAD]`: Parches de vulnerabilidades, sanitización o blindaje.
