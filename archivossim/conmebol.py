"""
Simulación de Libertadores y Sudamericana solo con equipos latinoamericanos.
Premio Mejor Jugador de América separado.
"""

from base_datos import base_datos
from random import shuffle
from datetime import datetime

# Lista de ligas latinoamericanas (ajusta según tu base de datos)
LIGAS_LATINAS = [
    "Liga Argentina",
    "Liga Brasileira",
    "Liga Chilena",
    "Liga Uruguaya",
    "Liga Mexicana",
    "Liga Paraguaya",
    "Liga Colombiana",
    "Liga Peruana",
    "Liga Ecuatoriana"
]

def obtener_equipos_latinos():
    equipos_por_liga = base_datos.obtener_ligas()
    equipos_latinos = []
    for liga in LIGAS_LATINAS:
        if liga in equipos_por_liga:
            equipos_latinos += list(equipos_por_liga[liga].keys())
    return equipos_latinos

def simular_copa_latina(nombre_copa, archivo=None):
    equipos = obtener_equipos_latinos()
    shuffle(equipos)

    # 16 equipos por torneo, puedes extender a + equipos si lo prefieres
    equipos = equipos[:16]
    ronda = equipos

    resultados = []
    while len(ronda) > 1:
        siguiente_ronda = []
        for i in range(0, len(ronda), 2):
            eq1, eq2 = ronda[i], ronda[i+1]
            # Usa tu función de simulación existente, pero añade distinción para equipos latinos
            nivel1 = base_datos.obtener_nivel_equipo(eq1)
            nivel2 = base_datos.obtener_nivel_equipo(eq2)
            resultado = f"{eq1.upper()} {nivel1} vs {eq2.upper()} {nivel2}"
            if nivel1 + (2 if nivel1 > nivel2 else 0) > nivel2 + (2 if nivel2 > nivel1 else 0):
                ganador = eq1
            else:
                ganador = eq2
            resultados.append(f"{resultado} -> GANADOR: {ganador.upper()}")
            siguiente_ronda.append(ganador)
        ronda = siguiente_ronda
    
    campeon = ronda[0]
    base_datos.registrar_campeon(nombre_copa, campeon)
    if archivo:
        archivo.write(f"🏆 CAMPEÓN {nombre_copa.upper()}: {campeon.upper()}\n\n")
        for resultado in resultados:
            archivo.write(f"{resultado}\n")
    return campeon, resultados

def seleccionar_mejor_jugador_america():
    # Seleccionas el mejor goleador y/o asistente solo de equipos latinos
    equipos_latinos = set(obtener_equipos_latinos())
    jugadores_latinos = [j for j in base_datos.jugadores.values() if j.equipo_codigo in equipos_latinos]
    # Puedes mejorar el criterio de selección aquí
    if jugadores_latinos:
        return max(jugadores_latinos, key=lambda x: x.goles + x.asistencias)
    return None