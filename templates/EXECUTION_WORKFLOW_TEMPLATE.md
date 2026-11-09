# MATRIZ DE DEPENDENCIAS Y FLUJO DE EJECUCIÓN (WORKFLOW)

**Tarea Principal:** `[Nombre de la Tarea / Directorio]`  
**Directorio de Trabajo:** `Engineering/Tasks/[YYYYMMDD_Nombre_Tarea]/`  
**Fecha de Orquestación:** `[YYYY-MM-DD]`  
**Estado de la Orquestación:** `[PROPUESTO / APROBADO POR EL USUARIO / EN PROGRESO / COMPLETADO]`  

---

## 1. MATRIZ DE DEPENDENCIAS CRUZADAS
Análisis de interacciones entre los micro-problemas analizados:

| ID | Título | Depende de | Razón Técnica de la Dependencia |
| :--- | :--- | :--- | :--- |
| **P01** | [Título P01] | `[Ninguno / P0X]` | [Por qué debe resolverse antes o después] |
| **P02** | [Título P02] | `[P01]` | [Por qué requiere los cambios de P01 primero] |
| **P03** | [Título P03] | `[P02]` | [Por qué requiere los cambios de P02 primero] |

---

## 2. SECUENCIA ORDENADA DE EJECUCIÓN TOPOLÓGICA
*Orden estricto de resolución determinado tras el análisis integral de dependencias.*

```text
[Paso 1: P01] ────► [Paso 2: P02] ────► [Paso 3: P03]
```

### Detalle de la Secuencia:
1. **PASO 1: Resolver [P01 - Título]**
   - *Análisis de Referencia*: `Analysis_P01_[Slug].md`
   - *Comando de Verificación*: `[Comando nativo P01]`
   - *Regla*: Al terminar, emitir reporte y **HACER HARD STOP**. No pasar a Paso 2 sin orden.

2. **PASO 2: Resolver [P02 - Título]**
   - *Análisis de Referencia*: `Analysis_P02_[Slug].md`
   - *Comando de Verificación*: `[Comando nativo P02]`
   - *Regla*: Al terminar, emitir reporte y **HACER HARD STOP**. No pasar a Paso 3 sin orden.

3. **PASO 3: Resolver [P03 - Título]**
   - *Análisis de Referencia*: `Analysis_P03_[Slug].md`
   - *Comando de Verificación*: `[Comando nativo P03]`
   - *Regla*: Al terminar, emitir reporte y **HACER HARD STOP**. Proceder a certificación final.

---

## 3. COMPUERTA DE APROBACIÓN DEL USUARIO
- [ ] El usuario ha revisado la secuencia propuesta y ha otorgado su visto bueno para iniciar la resolución del Paso 1.
