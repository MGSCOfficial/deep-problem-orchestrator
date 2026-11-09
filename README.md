# Deep Problem Orchestrator 🏛️

> **Metodología Quirúrgica Universal de Alta Fidelidad para Descomposición Anatómica de Problemas de Agentes de IA.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Compatibility](https://img.shields.io/badge/Antigravity-2.0+-emerald.svg)](#)

**Deep Problem Orchestrator** es la metodología de ingeniería agéntica de máxima fidelidad para **Google Antigravity**. Resuelve de raíz los tres grandes males del desarrollo asistido por IA: la abstracción superficial (*shallow abstraction*), la pérdida de contexto tras pausas operativas (*context rot*) y el diseño prematuro masivo (*Big Design Up Front*).

Integra el **Motor ATLAS**, un compilador determinista de grafos acíclicos dirigidos (DAG), gestión de dependencias topológicas, tablero de concurrencia multi-chat y compuertas de calidad en tres capas.

---

## 🚀 Pilares y Capacidades de la Metodología

### 1. Descomposición Anatómica Previa (`00_Inventory.md`)
Prohíbe terminantemente los checklists superficiales de 3 líneas. Cada tarea se descompone en micro-problemas acotados con:
- Contratos de entrada y salida explícitos.
- Archivos involucrados y firmas de funciones exactas.
- Puntero de estado activo inmune al cambio de contexto (*Context-Switch Proof*).

### 2. Gobernanza Calibrada Tri-Track
* 🟢 **Fast-Track** (Bajo riesgo / 1 micro-problema): Ejecución directa con validación inmediata.
* 🟡 **Streamlined-Track** (2 a 4 problemas acotados): Aprobación única del roadmap y ejecución secuencial fluida.
* 🔴 **Deep-Track** (Alto riesgo / Masivo): Ciclo mono-foco estricto con **Hard Stop obligatorio** tras cada análisis y cada ejecución unitaria.

### 3. Ciclo Adaptativo Just-In-Time (JIT)
Alterna análisis e implementación empírica (*Analizar P01 ➔ Implementar P01 ➔ Aprender de runtime ➔ Analizar P02*) erradicando el diseño prematuro.

### 4. Motor ATLAS Integrado (`scripts/atlas/`)
Compilador nativo en Python para resolución y automatización del flujo de trabajo:
- `atlas compile`: Analiza `00_Inventory.md` y sintetiza el grafo DAG de resolución óptima.
- `atlas next`: Devuelve el siguiente micro-problema desbloqueado topológicamente.
- `atlas status`: Matriz de avance y semáforos de archivo.

### 5. Compuertas de Calidad en Tres Capas (Quality Gates)
1. **Linter Estático Nativo**: 0 hallazgos / 100% de archivos conformes.
2. **Suite de Pruebas Oficial**: 100% PASS en el stack nativo del proyecto.
3. **Control de Versión Determinista**: Micro-commits atómicos Git (`feat(Pxx): [titulo]`) para rollback determinista instantáneo.

---

## 📦 Estructura del Repositorio

```
deep-problem-orchestrator/
├── SKILL.md                          # Instrucciones operativas maestras
├── scripts/
│   └── atlas/                        # Motor ATLAS (Compilador DAG y CLI)
│       ├── atlas.py                  # CLI principal
│       ├── test_atlas.py             # Suite de pruebas unitarias
│       └── core/                     # Módulos: DAG, Bus de eventos, Estado
├── templates/
│   ├── 00_INVENTORY_TEMPLATE.md      # Plantilla anatómica de inventario
│   ├── EXECUTION_WORKFLOW_TEMPLATE.md # Plantilla de flujo topológico
│   ├── CONCURRENCY_BOARD_TEMPLATE.md # Tablero de semáforos de concurrencia
│   └── ANALYSIS_MICRO_TEMPLATE.md    # Plantilla de micro-análisis
└── references/
    ├── three_layer_certification.md  # Protocolo de compuertas de calidad
    ├── multiagent_orchestration.md   # Coordinación entre agentes
    └── execution_flow_and_backlog.md
```

---

## 🛠️ Instalación y Uso

### 1. Como Skill Global de Agente
Copia la carpeta `deep-problem-orchestrator` dentro de tu directorio de skills agénticas:
* **Windows**: `C:\Users\<USUARIO>\.agents\skills\deep-problem-orchestrator\`

### 2. Activación
Invoca `/deep-problem-orchestrator` al inicio de cualquier refactorización profunda, desarrollo de nuevas características multi-módulo o corrección de defectos complejos.

---

## 👤 Autor y Licencia

* **Desarrollo y Arquitectura**: **MGSC** ([@MGSCOfficial](https://github.com/MGSCOfficial))
* **Licencia**: Código abierto bajo la licencia [MIT](LICENSE).
