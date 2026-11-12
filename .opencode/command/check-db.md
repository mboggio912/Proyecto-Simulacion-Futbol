---
description: Ejecuta una auditoría rápida de integridad sobre base_datos.py y conmebol.py
---

Ejecuta en terminal un script inline de Python (`python -c`) que importe `BaseDatos` desde `archivossim` (configurando UTF-8 en consola si es necesario) y verifique:
1. Total de equipos cargados en memoria vs equipos definidos.
2. Total de jugadores únicos en el diccionario vs sumatoria de jugadores en las plantillas.
3. Conteo de equipos detectados por cada liga americana y europea.

Muestra los resultados en una tabla clara y alerta si algún conteo no cuadra o da 0.
