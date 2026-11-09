# GESTIÓN DE TAREAS QUIRÚRGICAS, ANÁLISIS ADAPTATIVO JIT Y CICLO DE VIDA DE BACKLOG

Esta guía define las directrices operativas de la metodología **High-Fidelity Task Orchestration**, orientada a garantizar máxima profundidad de razonamiento, cero pérdida de contexto y persistencia desacoplada en tareas complejas y extensas.

---

## 1. EL PROBLEMA DE LOS RESÚMENES SUPERFICIALES (*SHALLOW ABSTRACTION*)

En tareas de desarrollo complejas, la tendencia natural de los modelos de IA al planificar es comprimir el trabajo en checklists o resúmenes de 2 o 3 líneas por cada punto. Este enfoque fracasa en proyectos reales por las siguientes razones:
- **Pérdida de la Causa Raíz**: 3 líneas no capturan firmas de funciones, tipos, contratos ni efectos colaterales.
- **Amnesia Táctica**: Cuando el agente llega a la fase de implementación (varios turnos después), ya no recuerda los detalles originales y tiende a improvisar o romper módulos dependientes.
- **Falta de Control Humano**: El usuario no puede evaluar con precisión qué se va a hacer antes de que se toque el código.

---

## 2. LA SOLUCIÓN: ARQUITECTURA DE ANÁLISIS PROFUNDO DESACOPLADO

Para resolver esto, la metodología implementa una separación estricta entre **Diagnóstico e Inventario**, **Análisis Profundo Quirúrgico**, **Orquestación de Dependencias** y **Ejecución Unitaria**.

### Estructura de Directorio por Tarea:
Toda tarea de ingeniería compleja se encapsula en su propia carpeta aislada:
```text
Engineering/Tasks/[YYYYMMDD_Nombre_Tarea]/
├── 00_Inventory.md             (Tablero de control y puntero de estado)
├── Analysis_P01_[Nombre].md     (Análisis profundo dedicado de P01)
├── Analysis_P02_[Nombre].md     (Análisis profundo dedicado de P02)
├── Analysis_PN_[Nombre].md      (Análisis profundo dedicado de PN)
├── Execution_Workflow.md        (Matriz de dependencias y orden topológico)
└── Execution_Log.md             (Bitácora histórica de resolución)
```

---

## 3. CALIBRACIÓN DE SUPERVISIÓN: DEEP-TRACK VS STREAMLINED-TRACK

Para no sobrecargar al operador humano con confirmaciones innecesarias ni desatender el rigor técnico:

### A. Modo Deep-Track (1 Turno = 1 Micro-Problema)
- Utilizado en arquitecturas críticas, código de bajo nivel o tareas con alto riesgo de regresión sistémica.
- **Dedicación Exclusiva**: El agente toma un único micro-problema por interacción (`Pxx`).
- **Lujo de Detalle Técnico**: Inspecciona el código, analiza firmas, traza flujos de datos y redacta `Analysis_Pxx_[Slug].md`.
- **Hard Stop Obligatorio**: Se detiene al terminar el análisis y espera la validación explícita del usuario antes de proceder al siguiente micro-problema.

### B. Modo Streamlined-Track (Aprobación en Bloque del Roadmap)
- Utilizado en refactorizaciones de 2 a 4 problemas bien delimitados donde la arquitectura general ya es conocida y consensuada.
- **Triage Integral Inicial**: El agente descompone todos los micro-problemas (P01..PN) en `00_Inventory.md` en el primer turno.
- **Compuerta Única de Aprobación**: El usuario valida el plan global una sola vez (*"Aprobado, ejecuta"*).
- **Ejecución Continua**: El agente ejecuta secuencialmente los problemas sin detenerse en cada micro-paso, activando *Hard Stop* únicamente ante fallos de tests/linter o decisiones arquitectónicas imprevistas.

---

## 4. ORQUESTACIÓN TOPOLÓGICA DE DEPENDENCIAS

Antes o durante la ejecución de los micro-problemas:
1. El agente cruza dependencias técnicas: determina qué componentes deben existir primero antes de que otros puedan funcionar.
2. Redacta o compila `Execution_Workflow.md` mediante ATLAS (`atlas resolve-dag`) estableciendo la secuencia óptima de resolución.
3. El usuario revisa y autoriza el orden de trabajo.

---

## 5. MODALIDADES DE EJECUCIÓN: CASCADA (WATERFALL) VS ADAPTATIVO (JIT)

Para evitar la trampa del **diseño prematuro (*Big Design Up Front - BDUF*)**:

1. **Modo Cascada Clásico**:
   - Analizar P01..PN completos ➔ Workflow ➔ Ejecutar P01..PN.
   - Ideal cuando los contratos entre módulos están perfectamente estandarizados y cerrados desde el principio.
2. **Modo Adaptativo Just-In-Time (JIT)**:
   - Analizar P01 ➔ Implementar P01 ➔ Inspeccionar evidencia empírica de runtime ➔ Analizar P02 alimentado con los hallazgos reales de P01 ➔ Implementar P02.
   - Ideal cuando la implementación de los primeros problemas puede alterar o refinar la arquitectura de los siguientes, evitando el derroche de re-analizar supuestos obsoletos.

### 5.1. Puntos de Restauración Inmutables (Atomic Micro-Commits en Git)
- Tras certificar cada micro-problema con 100% PASS en el arnés nativo oficial, el agente realiza un micro-commit atómico en Git:
  ```bash
  git commit -m "feat(Pxx): [titulo_del_micro_problema]"
  ```
- **Ventaja Operativa**: Cada micro-problema resuelto queda sellado como un punto de restauración físico inmutable. Si durante la resolución de un problema posterior ocurre una regresión destructiva, es trivial hacer rollback limpio (`git reset --hard HEAD~1` o `git revert`) sin perder el trabajo previamente verificado.

---

## 6. PROTOCOLO DE CONGELAMIENTO, REANUDACIÓN Y CIERRE FORMAL (*CONTEXT-SWITCH PROOF*)

### Congelamiento y Reanudación:
Si el usuario decide pausar la tarea para atender una urgencia o si la sesión se interrumpe durante días:
- El estado queda **congelado en disco** gracias al puntero activo en `00_Inventory.md` y al estado JSON de ATLAS.
- Para reanudar, el usuario solo indica: *"Reanudar tarea [Nombre_Tarea]"*.
- El agente consulta el puntero atómico:
  `python "C:\Users\MGSCO\.agents\skills\agentic-task-orchestrator\scripts\atlas\atlas.py" --agent status`
  recuperando el 100% del contexto exacto en milisegundos (<20 tokens) sin re-analizar todo el repositorio.

### Cierre Formal de Tarea (`atlas finish`):
Al certificar el último micro-problema y verificar que todas las compuertas de calidad pasaron:
- El agente ejecuta:
  ```bash
  python "C:\Users\MGSCO\.agents\skills\agentic-task-orchestrator\scripts\atlas\atlas.py" finish --summary "Certificación final exitosa"
  ```
- Esto actualiza la fase a 4 (Completada), compila el `00_Inventory.md` final y retira el puntero `.atlas_active_task`, dejando el repositorio limpio y listo para futuras tareas sin estados huérfanos.

---

## 7. CICLO DE VIDA DEL BANCO DE IDEAS (`Backlog_Ideas.txt`)

- Ubicación estándar: `Engineering/Backlog_Ideas.txt`.
- **Propósito**: Capturar ideas volátiles, optimizaciones o sugerencias colaterales descubiertas durante el trabajo sin desviar la atención de la tarea activa.
- **Regla Inmutable**: Tan pronto como una idea es implementada y certificada, **SE ELIMINA FÍSICAMENTE DE INMEDIATO DEL ARCHIVO**. Queda prohibido acumular ideas "completadas" en el backlog (el historial pertenece a los changelogs).
- **Descarte Explícito**: Si una idea es evaluada y rechazada por decisión técnica o del usuario, se purga del backlog documentando brevemente el motivo en la bitácora o changelog para no dejar ideas huérfanas indefinidamente.
