"""
Simulación de Libertadores y Sudamericana solo con equipos latinoamericanos.
Premio Mejor Jugador de América separado.
"""

from base_datos import base_datos
from random import random, shuffle
from datetime import datetime

# Lista de ligas latinoamericanas (ajusta según tu base de datos)
LIGAS_LATINAS = [
    "Liga Argentina",
    "Liga Brasileña",
    "Liga Chilena",
    "Liga Uruguaya",
    "Liga MX",
    "Liga Paraguaya",
    "Liga Dimayor",
    "Liga Ecuatoriana"
]

def obtener_equipos_latinos(base_datos_instancia=None):
    datos = base_datos if base_datos_instancia is None else base_datos_instancia
    equipos_por_liga = datos.obtener_ligas()
    equipos_latinos = []
    for liga in LIGAS_LATINAS:
        equipos_liga = equipos_por_liga.get(liga, {})
        if not equipos_liga:
            raise ValueError(
                f"La liga configurada '{liga}' no existe en BaseDatos o no tiene equipos."
            )
        equipos_latinos += list(equipos_liga.keys())
    return equipos_latinos

def _resolver_penales(equipo1, equipo2, datos):
    """Resuelve una tanda aleatoria; los penales no cuentan como goles del partido."""
    nivel1 = datos.obtener_nivel_equipo(equipo1)
    nivel2 = datos.obtener_nivel_equipo(equipo2)
    probabilidad_equipo1 = max(0.4, min(0.6, 0.5 + (nivel1 - nivel2) / 200))

    goles1 = sum(random() < probabilidad_equipo1 for _ in range(5))
    goles2 = sum(random() < 1 - probabilidad_equipo1 for _ in range(5))
    if goles1 != goles2:
        return equipo1 if goles1 > goles2 else equipo2

    while True:
        convierte1 = random() < probabilidad_equipo1
        convierte2 = random() < 1 - probabilidad_equipo1
        if convierte1 != convierte2:
            return equipo1 if convierte1 else equipo2


def simular_copa_latina(nombre_copa, archivo=None, base_datos_instancia=None):
    datos = base_datos if base_datos_instancia is None else base_datos_instancia
    equipos = obtener_equipos_latinos(datos)
    shuffle(equipos)

    # 16 equipos por torneo, puedes extender a + equipos si lo prefieres
    equipos = equipos[:16]
    ronda = equipos

    resultados = []
    # Import local para evitar el ciclo: simuladorcompleto importa este módulo.
    from simuladorcompleto import simular_partido_con_jugadores

    while len(ronda) > 1:
        siguiente_ronda = []
        for i in range(0, len(ronda), 2):
            eq1, eq2 = ronda[i], ronda[i+1]
            goles1, goles2, _ = simular_partido_con_jugadores(
                eq1, eq2, base_datos_instancia=datos
            )
            resultado = f"{eq1.upper()} {goles1}-{goles2} {eq2.upper()}"
            if goles1 > goles2:
                ganador = eq1
            elif goles2 > goles1:
                ganador = eq2
            else:
                ganador = _resolver_penales(eq1, eq2, datos)
                resultado += f" - {ganador.upper()} por penales"
            resultados.append(f"{resultado} -> GANADOR: {ganador.upper()}")
            siguiente_ronda.append(ganador)
        ronda = siguiente_ronda
    
    campeon = ronda[0]
    datos.registrar_campeon(nombre_copa, campeon)
    if archivo:
        archivo.write(f"🏆 CAMPEÓN {nombre_copa.upper()}: {campeon.upper()}\n\n")
        for resultado in resultados:
            archivo.write(f"{resultado}\n")
    return campeon, resultados

def seleccionar_mejor_jugador_america(base_datos_instancia=None):
    datos = base_datos if base_datos_instancia is None else base_datos_instancia
    equipos_latinos = obtener_equipos_latinos(datos)
    # Leer las plantillas evita perder jugadores si hay IDs repetidos en el diccionario.
    jugadores_latinos = [
        jugador
        for codigo in equipos_latinos
        for jugador in datos.obtener_equipo(codigo).jugadores
        if jugador.goles + jugador.asistencias > 0
    ]
    if jugadores_latinos:
        return max(jugadores_latinos, key=lambda jugador: jugador.goles + jugador.asistencias)
    return None
