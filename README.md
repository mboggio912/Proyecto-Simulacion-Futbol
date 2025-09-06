Simulador de Temporada Europea de Fútbol con Sistema de Jugadores

Un simulador completo escrito en Python que recrea una temporada completa de fútbol europeo con un sistema detallado de jugadores, estadísticas individuales y competiciones continentales.
🎯 Características Principales
👥 Sistema Completo de Jugadores

    Base de datos con 1000+ jugadores realistas con nombres, posiciones y niveles

    11 jugadores por equipo con atributos individuales

    Estadísticas detalladas: goles, asistencias, partidos jugados, tarjetas

    Posiciones específicas: POR (portero), DEF (defensa), MED (mediocampista), DEL (delantero)

🏆 Competiciones Simuladas

    7 Ligas Domésticas: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Primeira Liga, Eredivisie

    3 Competiciones Europeas: UEFA Champions League, UEFA Europa League, UEFA Conference League

    Sistema de Clasificación Automático basado en posiciones reales de cada liga

⚽ Estadísticas Individuales Realistas

    Top goleadores y top asistentes de la temporada

    Candidatos al Balón de Oro con sistema de puntuación basado en:

        Goles y asistencias

        Nivel del jugador

        Partidos jugados

        Títulos colectivos ganados

    Mínimos y máximos realistas: 15-35 goles para los máximos goleadores

🔄 Sistema de Simulación Mejorado

    Probabilidades realistas de gol basadas en posición y nivel del jugador

    Asistencias registradas con distribuciones realistas por posición

    Tarjetas amarillas y rojas simuladas

    Minutos jugados contabilizados para cada jugador

🛠️ Estructura del Proyecto
text

📁 simulador-futbol-europeo/
├── 📄 simuladorcompleto.py      # Simulador principal de temporada completa
├── 📄 base_datos.py             # Base de datos de equipos y jugadores
├── 📄 champions.py              # Simulador individual de partidos
└── 📄 temporada_completa_*.txt  # Resultados generados (se crean automáticamente)

🚀 Cómo Usar
Simular Temporada Completa:
bash

python simuladorcompleto.py

Simular Partido Individual:
bash

python champions.py

📊 Output Ejemplo

El simulador genera reportes detallados en formato texto que incluyen:

    Tablas de posiciones de todas las ligas con estadísticas de equipo

    Resultados de fases de grupos europeas

    Detalles de eliminatorias y finales

    Estadísticas individuales:

        Top 10 goleadores con promedio de gol por partido

        Top 10 asistentes con promedio de asistencia por partido

        Top 20 candidatos al Balón de Oro con puntuación detallada

    Resumen final de campeones de liga y competiciones europeas

🎮 Personalización

    Modificar jugadores: Edita la base de datos en base_datos.py

    Ajustar probabilidades: Modifica los umbrales en las funciones de simulación

    Cambiar fórmulas de cálculo: Ajusta los algoritmos de Balón de Oro y estadísticas

💡 Tecnologías

    Python 3.7+

    Módulos: random, collections, datetime, dataclasses

    Sistema orientado a objetos con clases Jugador, Equipo y BaseDatos

    Compatible con cualquier sistema operativo

📈 Próximas Características

    Interfaz gráfica (GUI) para visualización de resultados

    Sistema de jóvenes promesas con crecimiento de nivel

    Mercado de transferencias entre temporadas

    Lesiones y suspensiones por tarjetas

    Modo carrera multi-temporada con evolución de jugadores

    Exportación a JSON/CSV para análisis avanzado de datos
