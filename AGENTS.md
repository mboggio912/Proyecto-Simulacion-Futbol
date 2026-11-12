# Reglas del Proyecto — Simulador de Fútbol

## Stack y Restricciones
- **Lenguaje:** Python 3 (exclusivamente librería estándar / `stdlib`). Prohibido agregar dependencias externas (`pip`).
- **Codificación:** Siempre `UTF-8` explícito al leer/escribir archivos (`encoding="utf-8"`). Atención a caracteres en español (`ñ`, tildes).
- **Estructura:** El código fuente vive dentro de `archivossim/`.

## Flujo de Trabajo Git (Estricto)
- **NUNCA** hacer commits ni editar archivos directamente en `main`.
- Cada tarea debe ejecutarse en su propia rama dedicada:
  - Bugs: `fix/bug-XX-descripcion-corta`
  - Features: `feat/sim-XX-descripcion-corta`
  - Infra/Refactor: `chore/descripcion-corta`
- Commits atómicos usando **Conventional Commits** (`fix(conmebol): ...`, `feat(motor): ...`, `test: ...`, `chore: ...`).
- **NUNCA** incluir en commits archivos generados (`*.txt`, `__pycache__/`, `*.pyc`, `venv/`).

## Estándares de Ingeniería
- **Read-before-edit:** Leer siempre los archivos afectados completos antes de proponer o aplicar cambios.
- **Fail-Fast:** Si una configuración, liga o ID no coincide o devuelve vacío, lanzar excepciones explícitas (`ValueError`, `KeyError`) en lugar de fallar en silencio.
- **Alcance cerrado:** Resolver únicamente el issue asignado sin refactorizar código no relacionado.
